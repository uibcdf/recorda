"""Opt-in failure provenance never replaces native errors or inspects unknown ones."""

import asyncio
import json

import pytest

import recorda


class SourceFailure(Exception):
    def __str__(self):
        raise AssertionError("exception text must not be inspected")

    def __repr__(self):
        raise AssertionError("exception repr must not be inspected")


@pytest.mark.parametrize("boundary", ["decorated", "explicit", "async"])
def test_native_reference_preserves_error_traceback_and_cause(tmp_path, boundary):
    native = SourceFailure("secret scientific detail")
    cause = ValueError("private cause")
    reference = recorda.Reference("source", "trace:1", digest="retained-by-owner")
    observed = []

    def retain(error):
        observed.append(error)
        return reference

    def target():
        raise native from cause

    @recorda.record("source.fail")
    def decorated():
        target()

    @recorda.record("source.async_fail")
    async def async_target():
        await asyncio.sleep(0)
        target()

    async def async_run():
        return await async_target()

    handle = recorda.start(
        "failure", path=tmp_path / "failure.jsonl", reference_adapters={SourceFailure: retain}
    )
    try:
        with pytest.raises(SourceFailure) as raised:
            if boundary == "decorated":
                decorated()
            elif boundary == "async":
                asyncio.run(async_run())
            else:
                with handle.operation("source.fail"):
                    target()
        assert raised.value is native and native.__cause__ is cause
        frames = []
        traceback = native.__traceback__
        while traceback is not None:
            frames.append(traceback.tb_frame.f_code.co_name)
            traceback = traceback.tb_next
        assert frames[-1] == "target"
    finally:
        result = handle.stop()
    assert observed == [native]
    assert result.status == "failed"
    failure = result.operations[0]["exception"]
    assert failure["reference"] == {
        "kind": "reference",
        "owner": "source",
        "identifier": "trace:1",
        "revision": None,
        "digest": "retained-by-owner",
    }
    assert "secret scientific" not in handle.path.read_text()
    assert "private cause" not in handle.path.read_text()


@pytest.mark.parametrize("fault", ["invalid", "omitted", "exception", "interrupt"])
def test_adapter_faults_are_safe_omissions_and_preserve_original_failure(tmp_path, fault):
    native = SourceFailure("native secret")

    def adapter(error):
        if fault == "invalid":
            return {"api_key": "adapter secret"}
        if fault == "omitted":
            return recorda.Omitted("adapter secret")
        if fault == "interrupt":
            raise KeyboardInterrupt("adapter secret")
        raise ValueError("adapter secret")

    @recorda.record("source.fail")
    def target():
        raise native

    handle = recorda.start(
        "fault", path=tmp_path / "fault.jsonl", reference_adapters={SourceFailure: adapter}
    )
    try:
        with pytest.raises(SourceFailure) as raised:
            target()
        assert raised.value is native
    finally:
        result = handle.stop()
    reason = {"invalid": "invalid_reference_adapter_result", "omitted": "caller_omitted"}.get(
        fault, "reference_adapter_failed"
    )
    assert result.operations[0]["exception"]["reference"] == {"kind": "omitted", "reason": reason}
    assert "secret" not in handle.path.read_text()


def test_inactive_unknown_and_subclass_errors_do_not_call_adapters(tmp_path):
    class UnknownFailure(SourceFailure):
        pass

    def forbidden(value):
        raise AssertionError("unregistered or inactive error must not call the adapter")

    native = UnknownFailure("secret")
    calls = []

    def adapter(value):
        calls.append(value)
        return forbidden(value)

    @recorda.record("source.fail")
    def fail(error):
        raise error

    for error in [SourceFailure("secret"), native]:
        with pytest.raises(type(error)) as raised:
            fail(error)
        assert raised.value is error
    adapters = {SourceFailure: adapter}
    handle = recorda.start("unknown", path=tmp_path / "unknown.jsonl", reference_adapters=adapters)
    adapters[UnknownFailure] = adapter
    try:
        with pytest.raises(UnknownFailure) as raised:
            fail(native)
        assert raised.value is native
    finally:
        result = handle.stop()
    assert not calls
    assert result.operations[0]["exception"]["reference"]["reason"] == "unsupported_type"


def test_nested_async_cancellation_keeps_native_identity_and_lineage(tmp_path):
    native = asyncio.CancelledError("secret")
    calls = []

    def retain(error):
        calls.append(error)
        return recorda.Reference("scheduler", "cancellation:1")

    @recorda.record("source.child")
    async def child():
        raise native

    @recorda.record("source.parent")
    async def parent():
        return await child()

    async def run():
        handle = recorda.start(
            "cancel",
            path=tmp_path / "cancel.jsonl",
            reference_adapters={asyncio.CancelledError: retain},
        )
        try:
            with pytest.raises(asyncio.CancelledError) as raised:
                await parent()
            assert raised.value is native
        finally:
            result = handle.stop()
        return result

    result = asyncio.run(run())
    assert result.operations[1]["parent_id"] == result.operations[0]["id"]
    assert calls == [native, native]
    assert all(op["exception"]["reference"]["owner"] == "scheduler" for op in result.operations)
    assert result.status == "failed"


def test_storage_failure_keeps_native_error_and_visible_incomplete_record(tmp_path, monkeypatch):
    native = SourceFailure("secret")
    handle = recorda.session(
        "storage",
        path=tmp_path / "storage.jsonl",
        reference_adapters={SourceFailure: lambda error: recorda.Reference("source", "trace:1")},
    )
    original = handle._append

    def broken(event, **data):
        if event == "operation_finished":
            raise OSError("private storage detail")
        return original(event, **data)

    monkeypatch.setattr(handle, "_append", broken)
    with handle:
        with pytest.raises(SourceFailure) as raised:
            with handle.operation("source.fail"):
                raise native
        assert raised.value is native
    result = handle.record
    assert result.status == "incomplete"
    assert result.operations[0]["status"] == "incomplete"
    assert any("Recorda" in note for note in native.__notes__)
    assert "private storage" not in handle.path.read_text()


def test_historical_type_only_failure_remains_readable(tmp_path):
    path = tmp_path / "historical.jsonl"
    handle = recorda.start("historical", path=path)
    try:
        with pytest.raises(ValueError):
            with handle.operation("source.fail"):
                raise ValueError("private")
    finally:
        handle.stop()
    events = [json.loads(line) for line in path.read_text().splitlines()]
    for event in events:
        if "exception" in event:
            event["exception"].pop("reference")
    path.write_text("".join(json.dumps(event) + "\n" for event in events))
    record = recorda.inspect(path)
    assert record.status == "failed" and "reference" not in record.operations[0]["exception"]
