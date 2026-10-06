"""Receiving reference contracts preserve native checks and metadata-only diagnostics."""

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path, PurePath

import pytest

import recorda


class Opaque:
    def __repr__(self):
        raise AssertionError("opaque repr must not run")

    def __str__(self):
        raise AssertionError("opaque str must not run")

    def __iter__(self):
        raise AssertionError("opaque iterator must not run")

    def __deepcopy__(self, memo):
        raise AssertionError("opaque copying must not run")


class Root:
    def __init__(self, path):
        self.path = path
        self.calls = 0

    def __fspath__(self):
        self.calls += 1
        return self.path


class IntSubclass(int):
    pass


@pytest.fixture
def configured():
    import smonitor
    from smonitor.handlers.memory import MemoryHandler

    handler = MemoryHandler()
    manager = smonitor.configure(
        handlers=[handler],
        level="DEBUG",
        profile="qa",
        enabled=True,
        args_summary=True,
        capture_logging=False,
        capture_warnings=False,
        capture_exceptions=False,
        profiling=False,
        routes=[],
        filters=[],
    )
    return smonitor, manager, handler


@pytest.fixture
def snapshot(tmp_path):
    with recorda.session("PRIVATE_SESSION", path=tmp_path / "journal.jsonl") as handle:
        with handle.operation("PRIVATE_OPERATION", parameters={"value": "PRIVATE_RECORD"}):
            pass
    return handle.record


@pytest.mark.parametrize("form", [str, Path, PurePath, Root])
def test_native_root_forms_and_index_copy_are_preserved(tmp_path, form):
    reference = recorda.Reference("native", "object")
    entries = {reference: Path("native.bin")}
    root = form(str(tmp_path))
    resolver = recorda.LocalFileResolver(root, entries)
    entries.clear()
    assert resolver.references == (reference,)
    assert resolver.path_for(reference) == tmp_path / "native.bin"
    if isinstance(root, Root):
        assert root.calls == 1


@pytest.mark.parametrize("bad", [None, b"private-root", 0, Opaque()])
def test_unrelated_root_values_are_not_coerced(tmp_path, bad):
    with pytest.raises(TypeError, match="local root"):
        recorda.LocalFileResolver(bad, {})


@pytest.mark.parametrize("bad", ["sha512", True, Opaque()])
def test_algorithm_errors_precede_native_root_conversion(tmp_path, bad):
    root = Root(str(tmp_path))
    with pytest.raises(ValueError, match="explicitly declared sha256"):
        recorda.LocalFileResolver(root, {}, digest_algorithm=bad)
    assert root.calls == 0


@pytest.mark.parametrize(
    "entries,error",
    [
        (Opaque(), TypeError),
        ({"not-reference": "native.bin"}, TypeError),
        ({recorda.Reference("native", "object"): Opaque()}, TypeError),
        ({recorda.Reference("native", "object"): PurePath("native.bin")}, TypeError),
        ({recorda.Reference("native", "object"): "../outside.bin"}, ValueError),
        ({recorda.Reference("native", "object"): "/absolute.bin"}, ValueError),
    ],
)
def test_invalid_index_does_not_process_root(tmp_path, entries, error):
    root = Root(str(tmp_path))
    with pytest.raises(error):
        recorda.LocalFileResolver(root, entries)
    assert root.calls == 0


def test_authorized_path_protocol_retains_native_error_identity():
    native = OSError("PRIVATE_PATH_FAILURE")

    class BrokenRoot:
        def __fspath__(self):
            raise native

    with pytest.raises(OSError) as caught:
        recorda.LocalFileResolver(BrokenRoot(), {})
    assert caught.value is native


@pytest.mark.parametrize("bad", [True, False, 0, -1, 1.0, "1", IntSubclass(1), Opaque()])
@pytest.mark.parametrize("boundary", ["single", "record"])
def test_byte_limits_require_exact_positive_int_before_io(
    tmp_path, snapshot, monkeypatch, bad, boundary
):
    def forbidden(*args, **kwargs):
        pytest.fail("invalid options must not open a file")

    monkeypatch.setattr("recorda.references.os.open", forbidden)
    with pytest.raises(ValueError, match="positive integer"):
        if boundary == "single":
            recorda.check_reference(Opaque(), max_bytes=bad)
        else:
            recorda.check_references(snapshot, max_bytes=bad)


def test_exact_resolver_record_and_index_types(tmp_path, snapshot):
    class ResolverSubclass(recorda.LocalFileResolver):
        pass

    class RecordSubclass(recorda.ScientificRecord):
        pass

    class EntriesSubclass(dict):
        pass

    class ReferenceSubclass(recorda.Reference):
        pass

    resolver = ResolverSubclass(tmp_path, {})
    for check, value in ((recorda.check_reference, Opaque()), (recorda.check_references, snapshot)):
        with pytest.raises(TypeError, match="resolver must"):
            check(value, resolver=resolver)
    record = RecordSubclass(**vars(snapshot))
    with pytest.raises(TypeError, match="inspected ScientificRecord"):
        recorda.check_references(record)
    with pytest.raises(TypeError, match="local entries"):
        recorda.LocalFileResolver(tmp_path, EntriesSubclass())
    with pytest.raises(TypeError, match="index keys"):
        recorda.LocalFileResolver(tmp_path, {ReferenceSubclass("native", "a"): "a"})


def test_closed_signatures_keep_unknown_skip_and_positional_options_out(tmp_path, snapshot):
    for call in (
        lambda: recorda.LocalFileResolver(tmp_path, {}, skip_digestion=True),
        lambda: recorda.check_reference(Opaque(), skip_digestion=True),
        lambda: recorda.check_references(snapshot, unknown=Opaque()),
        lambda: recorda.LocalFileResolver(tmp_path, {}, "sha256"),
        lambda: recorda.check_reference(Opaque(), None),
        lambda: recorda.check_references(snapshot, None),
    ):
        with pytest.raises(TypeError):
            call()


def test_report_validates_once_and_cache_uses_guarded_core(tmp_path, monkeypatch):
    reference = recorda.Reference("native", "object")
    with recorda.session("cache", path=tmp_path / "cache.jsonl") as handle:
        with handle.operation("duplicates", inputs={"a": reference, "b": reference}):
            pass
    import recorda._arguments as arguments
    import recorda.references as checks

    original_options, original_check = arguments.record_check_options, checks._check_reference
    option_calls, byte_calls = [], []

    def options(*args, **kwargs):
        option_calls.append(1)
        return original_options(*args, **kwargs)

    def checked(*args, **kwargs):
        byte_calls.append(1)
        return original_check(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("the report must not re-digest each reference")

    monkeypatch.setattr(arguments, "record_check_options", options)
    monkeypatch.setattr(arguments, "reference_check_options", forbidden)
    monkeypatch.setattr(checks, "_check_reference", checked)
    report = recorda.check_references(handle.record)
    assert len(report["references"]) == 2 and option_calls == byte_calls == [1]


def test_private_unwrapping_and_provider_bypass_keep_native_guards(tmp_path, snapshot, monkeypatch):
    import recorda._arguments as arguments
    import recorda.references as checks

    for fn, args, kwargs, error in (
        (arguments.reference_index_options, (None, Opaque(), tmp_path), {}, TypeError),
        (arguments.reference_check_options, (None,), {"max_bytes": True}, ValueError),
        (arguments.record_check_options, (None,), {"max_bytes": 1, "record": Opaque()}, TypeError),
    ):
        while hasattr(fn, "__wrapped__"):
            fn = fn.__wrapped__
        with pytest.raises(error):
            fn(*args, **kwargs)
    monkeypatch.setattr(arguments, "reference_check_options", lambda *a, **k: (None, True))
    with pytest.raises(ValueError, match="positive integer"):
        recorda.check_reference(Opaque())
    monkeypatch.setattr(arguments, "record_check_options", lambda *a, **k: (None, 1, Opaque()))
    with pytest.raises(TypeError, match="inspected ScientificRecord"):
        recorda.check_references(snapshot)
    reference = recorda.Reference("native", "a")
    monkeypatch.setattr(
        arguments,
        "reference_index_options",
        lambda **k: (tmp_path, {reference: "../outside"}, None),
    )
    with pytest.raises(ValueError, match="inside their root"):
        recorda.LocalFileResolver(tmp_path, {})
    with pytest.raises(ValueError, match="positive integer"):
        checks._check_reference(reference, resolver=None, max_bytes=False)


def test_private_values_and_inherited_context_are_absent_from_diagnostics(
    tmp_path, snapshot, configured
):
    smonitor, manager, handler = configured
    before = manager.config
    root = tmp_path / "PRIVATE_ROOT"
    reference = recorda.Reference("PRIVATE_OWNER", "PRIVATE_IDENTIFIER")

    @smonitor.signal(extra_factory=lambda args, kwargs: {"private": "PRIVATE_FRAME"})
    def producer():
        resolver = recorda.LocalFileResolver(root, {reference: "PRIVATE_LOCATION"})
        assert recorda.check_reference(reference, resolver=resolver)["status"] == "missing"
        assert recorda.check_references(snapshot)["session_status"] == "succeeded"
        with pytest.raises(TypeError):
            recorda.LocalFileResolver(root, {reference: Opaque()})
        with pytest.raises(ValueError):
            recorda.check_reference({"PRIVATE_KEY": Opaque()}, max_bytes=Opaque())
        with pytest.raises(TypeError):
            recorda.check_references(Opaque())

    producer()
    events = [event for event in handler.events if event.get("code", "").startswith("ARG-")]
    assert len(events) >= 3 and "PRIVATE_" not in json.dumps(events)
    assert manager.config is before
    assert smonitor.get_capture_policy() == smonitor.CapturePolicy()


def test_application_defaults_and_registry_replacement_cannot_rewrite_contract(
    tmp_path, configured, monkeypatch
):
    import argdigest.core.config as config
    from argdigest import DigestConfig, get_pipelines, register_pipeline

    smonitor, manager, _ = configured
    before = manager.config

    def forbidden(*args, **kwargs):
        pytest.fail("application digestion must not rewrite Recorda's rules")

    monkeypatch.setenv("ARGDIGEST_CONFIG", "nonexistent.application.config")
    monkeypatch.setattr(config, "_DEFAULTS", DigestConfig(standardizer=forbidden, profiling=True))
    arguments = importlib.reload(importlib.import_module("recorda._arguments"))
    old = get_pipelines("recorda.references")["max_bytes"]
    register_pipeline(kind="recorda.references", name="max_bytes")(forbidden)
    try:
        resolver = recorda.LocalFileResolver(tmp_path, {})
        assert (
            recorda.check_reference(
                recorda.Reference("native", "a"), resolver=resolver, max_bytes=1
            )["status"]
            == "unresolved"
        )
        with pytest.raises(ValueError):
            arguments.reference_check_options(None, max_bytes=True)
    finally:
        register_pipeline(kind="recorda.references", name="max_bytes")(old)
    assert manager.config is before
    assert smonitor.get_capture_policy() == smonitor.CapturePolicy()


def test_delivery_fault_preserves_validation_and_observation(tmp_path, configured, monkeypatch):
    import smonitor

    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_DELIVERY")

    resolver = recorda.LocalFileResolver(tmp_path, {})
    monkeypatch.setattr(smonitor, "emit", broken)
    assert (
        recorda.check_reference(recorda.Reference("native", "a"), resolver=resolver)["status"]
        == "unresolved"
    )
    with pytest.warns(RuntimeWarning, match="Diagnostic emission failed") as warnings:
        with pytest.raises(ValueError, match="positive integer"):
            recorda.check_reference(Opaque(), max_bytes=True)
    assert all("PRIVATE_DELIVERY" not in str(warning.message) for warning in warnings)


_FIRST_CALLS = [
    "recorda.LocalFileResolver('.', {})",
    "recorda.check_reference(recorda.Reference('native', 'a'))",
    "recorda.check_references(recorda.ScientificRecord('a', 'a', 'succeeded', {}, [], []))",
]


def _fresh_process(code, tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(recorda.__file__).resolve().parents[1])
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "-c", code], cwd=tmp_path, env=env, capture_output=True, text=True
    )


@pytest.mark.parametrize("call", _FIRST_CALLS)
def test_reference_first_use_keeps_safe_baseline_and_no_scientific_imports(tmp_path, call):
    result = _fresh_process(
        "import recorda,sys\n"
        "assert not {'argdigest','smonitor','depdigest'} & sys.modules.keys()\n"
        f"{call}\n"
        "import smonitor\n"
        "config=smonitor.get_manager().config\n"
        "assert not config.capture_logging and not config.capture_warnings and not config.capture_exceptions\n"
        "assert not {'numpy','pint','pyunitwizard','pandas'} & sys.modules.keys()\n",
        tmp_path,
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("call", _FIRST_CALLS)
@pytest.mark.parametrize("provider", ["argdigest", "smonitor"])
def test_missing_provider_fails_at_reference_use(tmp_path, call, provider):
    result = _fresh_process(
        "import sys,importlib.abc\n"
        "class Missing(importlib.abc.MetaPathFinder):\n"
        " def find_spec(self, fullname, path=None, target=None):\n"
        f"  if fullname == {provider!r}: raise ModuleNotFoundError(fullname)\n"
        "sys.meta_path.insert(0,Missing())\nimport recorda\n"
        f"try:\n {call}\n"
        "except ModuleNotFoundError:\n pass\n"
        "else:\n raise AssertionError('missing provider must fail at use')\n",
        tmp_path,
    )
    assert result.returncode == 0, result.stderr
