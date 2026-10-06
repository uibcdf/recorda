"""One local writer with incremental fsync and context-local operation correlation."""

import inspect as python_inspect
import json
import os
from contextvars import ContextVar
from datetime import datetime, timezone
from functools import wraps
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from threading import RLock
from uuid import uuid4

from .capture import capture, exception_reference, fields, label

_ACTIVE = ContextVar("recorda_session", default=None)
_PARENTS = ContextVar("recorda_parents", default=())


def _exception(error, reference_adapters):
    return {
        "type": f"{type(error).__module__}.{type(error).__qualname__}",
        "message": {"kind": "omitted", "reason": "exception_message_may_be_sensitive"},
        "reference": exception_reference(error, reference_adapters=reference_adapters),
    }


class RecordingSession:
    """One journal, activated manually or through an optional context manager."""

    def __init__(self, name, *, path, gaps=(), reference_adapters=None):
        self.name = label(name)
        self.path = Path(path)
        if isinstance(gaps, str):
            raise TypeError("gaps must be a sequence of non-sensitive labels")
        self.gaps = [label(gap) for gap in gaps]
        if len(self.gaps) > 64:
            raise ValueError("at most 64 known gaps may be declared")
        if reference_adapters is None:
            reference_adapters = {}
        if type(reference_adapters) is not dict or any(
            not isinstance(kind, type) or not callable(adapter)
            for kind, adapter in reference_adapters.items()
        ):
            raise TypeError("reference_adapters must map exact types to callables")
        self._reference_adapters = dict(reference_adapters)
        self.id = str(uuid4())
        self._sequence = 0
        self._file = None
        self._used = False
        self._broken = False
        self._failed = False
        self._open_operations = set()
        self._lock = RLock()

    def _append(self, event, **data):
        with self._lock:
            payload = {
                "schema": "recorda.journal/0.1",
                "event": event,
                "session_id": self.id,
                "sequence": self._sequence,
                "time": datetime.now(timezone.utc).isoformat(),
                **data,
            }
            encoded = (json.dumps(payload, allow_nan=False, ensure_ascii=True) + "\n").encode()
            remaining = memoryview(encoded)
            while remaining:
                written = self._file.write(remaining)
                if not written:
                    raise OSError("journal write made no progress")
                remaining = remaining[written:]
            # A complete line is visible even if the following fsync fails. Reserve
            # its sequence so a best-effort incomplete marker cannot reuse it.
            self._sequence += 1
            os.fsync(self._file.fileno())

    def _write(self, event, **data):
        if self._broken:
            raise OSError("recording has an unresolved persistence failure")
        try:
            self._append(event, **data)
        except BaseException:
            self._broken = True
            raise

    def start(self):
        """Activate in this execution context; reject replacing an active session."""
        return self._start(allow_nested=False)

    def _start(self, *, allow_nested):
        if self._used:
            raise RuntimeError("a recording session cannot be reopened")
        if _ACTIVE.get() is not None and not allow_nested:
            raise RuntimeError("a recording session is already active in this context")
        self._used = True
        fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        self._file = os.fdopen(fd, "wb", buffering=0)
        try:
            self._write(
                "session_started",
                name=self.name,
                coverage={"mode": "declared_boundaries", "known_gaps": self.gaps},
            )
        except BaseException:
            self._file.close()
            self._file = None
            raise
        self._active_token = _ACTIVE.set(self)
        self._parent_token = _PARENTS.set(())
        return self

    def _detach(self):
        # Reset before writing completion: an inherited task/context may see this
        # session but must not close the journal belonging to its activating context.
        try:
            _ACTIVE.reset(self._active_token)
        except ValueError as error:
            raise RuntimeError("stop must run in the context that activated the session") from error
        _PARENTS.reset(self._parent_token)

    def _finish(self, error=None, *, allow_incomplete=False):
        with self._lock:
            if self._file is None or _ACTIVE.get() is not self:
                raise RuntimeError("this session is not active in the current context")
            if self._open_operations and not allow_incomplete:
                raise RuntimeError("cannot stop while recorded operations are running")
            self._detach()
            status = "failed" if error is not None or self._failed else "succeeded"
            if self._broken or self._open_operations:
                status = "incomplete"
            # A final marker may be attempted after a recording fault; it never clears it.
            try:
                try:
                    self._append("session_finished", status=status)
                except BaseException:
                    if error is None:
                        raise
                    error.add_note(
                        "Recorda could not persist session completion; inspect for gaps."
                    )
            finally:
                self._file.close()
                self._file = None

    def stop(self):
        """Finalize an idle session and return its independently readable record."""
        self._finish()
        return self.record

    def __enter__(self):
        return self._start(allow_nested=True)

    def __exit__(self, exc_type, error, traceback):
        self._finish(error, allow_incomplete=True)
        return False

    def operation(self, name, *, inputs=None, parameters=None, implementation=None, profile=None):
        return Operation(self, name, inputs, parameters, implementation, profile)

    @property
    def record(self):
        from .reader import inspect

        return inspect(self.path)


class Operation:
    def __init__(self, session, name, inputs, parameters, implementation, profile):
        self.session = session
        self.name = label(name)
        self.inputs = fields(inputs, reference_adapters=session._reference_adapters)
        self.parameters = fields(parameters, reference_adapters=session._reference_adapters)
        self.implementation = fields(implementation)
        self.profile = None if profile is None else label(profile)
        self.id = str(uuid4())
        self._active = False
        self._used = False

    def __enter__(self):
        with self.session._lock:
            if self._used or _ACTIVE.get() is not self.session or self.session._file is None:
                raise RuntimeError(
                    "operation requires its active session and may be entered only once"
                )
            self._used = True
            parents = _PARENTS.get()
            self.session._write(
                "operation_started",
                operation_id=self.id,
                name=self.name,
                profile=self.profile,
                parent_id=parents[-1] if parents else None,
                inputs=self.inputs,
                parameters=self.parameters,
                implementation=self.implementation,
            )
            self.session._open_operations.add(self.id)
        self._token = _PARENTS.set((*parents, self.id))
        self._active = True
        return self

    def output(self, name, value):
        if not self._active or self.session._file is None:
            raise RuntimeError("outputs require an active operation")
        name = label(name)
        self.session._write(
            "operation_output",
            operation_id=self.id,
            name=name,
            value=capture(value, name, reference_adapters=self.session._reference_adapters),
        )

    def __exit__(self, exc_type, error, traceback):
        try:
            if error is not None:
                self.session._failed = True
            data = {
                "operation_id": self.id,
                "status": "failed" if error is not None else "succeeded",
            }
            if error is not None:
                data["exception"] = _exception(error, self.session._reference_adapters)
            try:
                self.session._write("operation_finished", **data)
            except BaseException:
                if error is None:
                    raise
                error.add_note("Recorda could not persist operation completion; inspect for gaps.")
            else:
                self.session._open_operations.discard(self.id)
        finally:
            self._active = False
            _PARENTS.reset(self._token)
        return False


def session(name, *, path, gaps=(), reference_adapters=None):
    """Create a session; context-manager activation remains available as a convenience."""
    return RecordingSession(name, path=path, gaps=gaps, reference_adapters=reference_adapters)


def start(name, *, path, gaps=(), reference_adapters=None):
    """Activate recording for instrumented calls and return the session handle."""
    return session(name, path=path, gaps=gaps, reference_adapters=reference_adapters).start()


def stop():
    """Finalize the session activated in this context and return its record."""
    active = _ACTIVE.get()
    if active is None:
        raise RuntimeError("no recording session is active in this context")
    return active.stop()


def record(name=None, *, profile=None):
    """Opt-in function boundary. Inactive calls bypass binding and capture entirely."""

    def decorate(function):
        if python_inspect.isgeneratorfunction(function) or python_inspect.isasyncgenfunction(
            function
        ):
            raise TypeError("generator execution requires an explicit operation boundary")
        operation_name = label(name or f"{function.__module__}.{function.__qualname__}")
        operation_profile = None if profile is None else label(profile)

        def boundary(active, args, kwargs):
            bound = python_inspect.signature(function).bind(*args, **kwargs)
            bound.apply_defaults()
            package = function.__module__.split(".")[0]
            try:
                package_version = version(package)
            except PackageNotFoundError:
                package_version = None
            return active.operation(
                operation_name,
                inputs=dict(bound.arguments),
                profile=operation_profile,
                implementation={
                    "package": package,
                    "callable": f"{function.__module__}.{function.__qualname__}",
                    "version": package_version,
                },
            )

        if python_inspect.iscoroutinefunction(function):

            @wraps(function)
            async def observed(*args, **kwargs):
                active = _ACTIVE.get()
                if active is None:
                    return await function(*args, **kwargs)
                with boundary(active, args, kwargs) as operation:
                    result = await function(*args, **kwargs)
                    operation.output("return", result)
                    return result
        else:

            @wraps(function)
            def observed(*args, **kwargs):
                active = _ACTIVE.get()
                if active is None:
                    return function(*args, **kwargs)
                with boundary(active, args, kwargs) as operation:
                    result = function(*args, **kwargs)
                    operation.output("return", result)
                    return result

        return observed

    return decorate
