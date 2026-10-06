"""Default configuration digestion with published providers; scientific calls stay native."""

import importlib
import json
import os
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import recorda


class Opaque:
    def __repr__(self):
        raise AssertionError("opaque repr must not run")

    def __str__(self):
        raise AssertionError("opaque str must not run")

    def __iter__(self):
        raise AssertionError("opaque iterator must not run")


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
def factory(configured):
    return recorda.CapturePolicy


@pytest.mark.parametrize(
    "profiles, expected",
    [
        (None, None),
        ([], ()),
        (["b", "a", "b"], ("a", "b")),
        (("b", "a"), ("a", "b")),
        ({"b", "a"}, ("a", "b")),
        (frozenset({"a", "b"}), ("a", "b")),
    ],
)
def test_constructor_canonicalizes_accepted_collections(factory, profiles, expected):
    result = factory(profiles, inputs=False, exception_references=False)
    assert result.profiles == expected and result.inputs is False
    assert result.exception_references is False
    assert type(result) is recorda.CapturePolicy


def test_bounds_copy_and_immutability(factory):
    labels = ["x" * 256] * 64
    policy = factory(labels)
    labels.clear()
    assert policy.profiles == ("x" * 256,)
    with pytest.raises(FrozenInstanceError):
        policy.inputs = False
    # The bound applies before deduplication.
    with pytest.raises(ValueError, match="64 profiles"):
        factory(["x"] * 65)


@pytest.mark.parametrize(
    "profiles, error",
    [
        (Opaque(), TypeError),
        ("analysis", TypeError),
        ({"analysis": True}, TypeError),
        (iter(["analysis"]), TypeError),
        ([Opaque()], ValueError),
        ([None], ValueError),
        ([""], ValueError),
        (["x" * 257], ValueError),
        (["x"] * 65, ValueError),
    ],
)
def test_constructor_rejects_invalid_collections_without_opaque_inspection(
    factory, profiles, error
):
    with pytest.raises(error):
        factory(profiles)


@pytest.mark.parametrize("name", ["inputs", "parameters", "outputs", "exception_references"])
@pytest.mark.parametrize("value", [0, None, "false", Opaque()])
def test_detail_switches_require_actual_booleans(factory, name, value):
    with pytest.raises(TypeError, match="switches must be bool"):
        factory(**{name: value})


def test_no_public_bypass_or_extra_keywords(factory):
    with pytest.raises(TypeError):
        factory(skip_digestion=True, inputs=Opaque())
    with pytest.raises(TypeError):
        factory(unknown=Opaque())
    # Unwrapping the private decorated function cannot bypass mandatory guards.
    from recorda._arguments import capture_profiles

    bare = capture_profiles
    while hasattr(bare, "__wrapped__"):
        bare = bare.__wrapped__
    with pytest.raises(TypeError):
        bare(Opaque(), True, True, True, True)


def test_import_and_factory_preserve_application_and_ignore_global_defaults(
    configured, monkeypatch
):
    import argdigest.core.config as config
    from argdigest import DigestConfig

    smonitor, manager, _ = configured
    before = manager.config

    def forbidden(caller, kwargs):
        pytest.fail("application standardizer must not change Recorda configuration")

    monkeypatch.setenv("ARGDIGEST_CONFIG", "nonexistent.application.config")
    monkeypatch.setattr(config, "_DEFAULTS", DigestConfig(standardizer=forbidden, profiling=True))
    module = importlib.import_module("recorda._arguments")
    module = importlib.reload(module)
    assert recorda.CapturePolicy(["b", "a"]).profiles == ("a", "b")
    assert manager.config is before
    assert smonitor.get_capture_policy() == smonitor.CapturePolicy()


def test_diagnostics_exclude_values_and_inherited_context(factory, configured):
    smonitor, manager, handler = configured
    before = manager.config
    private_label = "PRIVATE_PROFILE_MARKER"

    @smonitor.signal(extra_factory=lambda args, kwargs: {"private": "PRIVATE_FRAME_MARKER"})
    def producer():
        assert factory([private_label]).profiles == (private_label,)
        with pytest.raises(TypeError):
            factory(Opaque())
        with pytest.raises(ValueError):
            factory([private_label] * 65)

    producer()
    events = [event for event in handler.events if event.get("code", "").startswith("ARG-")]
    assert events
    serialized = json.dumps(events)
    assert private_label not in serialized and "PRIVATE_FRAME_MARKER" not in serialized
    for event in events:
        assert not {"value", "all_args", "cause_message", "detail"} & event.get("extra", {}).keys()
    assert manager.config is before


def test_diagnostic_delivery_failure_preserves_validation_and_success(factory, monkeypatch):
    import smonitor

    def broken(*args, **kwargs):
        raise RuntimeError("PRIVATE_DELIVERY_MARKER")

    monkeypatch.setattr(smonitor, "emit", broken)
    assert factory(["b", "a"]).profiles == ("a", "b")
    with pytest.warns(RuntimeWarning, match="Diagnostic emission failed"):
        with pytest.raises(TypeError, match="bounded collection"):
            factory(Opaque())


def test_native_calls_selected_facts_and_disabled_adapters(factory, tmp_path):
    value, native = Opaque(), ValueError("PRIVATE_NATIVE_MARKER")
    cause = LookupError("cause")

    def forbidden(value):
        pytest.fail("disabled adapter was invoked")

    @recorda.record("selected", profile="analysis")
    def selected(value):
        return value

    @recorda.record("excluded", profile="other")
    def excluded(value):
        return value

    policy = factory(
        ["analysis"], inputs=False, outputs=False, parameters=False, exception_references=False
    )
    assert selected(value) is value  # Inactive path retains native arguments.
    with recorda.session(
        "test",
        path=tmp_path / "run.jsonl",
        capture_policy=policy,
        reference_adapters={Opaque: forbidden, ValueError: forbidden},
    ) as handle:
        assert selected(value) is value and excluded(value) is value
        with pytest.raises(ValueError) as caught:
            with handle.operation("failure", profile="analysis"):
                raise native from cause
    assert caught.value is native and native.__cause__ is cause
    result = recorda.inspect(handle.path)
    assert result.status == "failed" and len(result.operations) == 2
    for operation in result.operations:
        assert operation["id"] and operation["start"] and operation["end"]
        assert operation["inputs"] == operation["outputs"] == operation["parameters"] == {}
    assert result.operations[-1]["exception"]["reference"]["reason"] == "capture_policy"
    assert "PRIVATE_NATIVE_MARKER" not in handle.path.read_text()


def _subprocess(code, *, provider_paths=True):
    env = os.environ.copy()
    paths = []
    if provider_paths:
        paths.extend(filter(None, env.get("PYTHONPATH", "").split(os.pathsep)))
    # An installed Recorda shares site-packages with the older published providers.
    # Preserve the qualified source precedence before adding Recorda's import root.
    paths.append(str(Path(recorda.__file__).resolve().parents[1]))
    env["PYTHONPATH"] = os.pathsep.join(paths)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)


def test_fresh_import_has_no_scientific_dependencies():
    result = _subprocess(
        "from recorda.integrations.argdigest import capture_policy; import sys; assert capture_policy(['a']).profiles == ('a',); assert not {'numpy', 'pint', 'pyunitwizard', 'pandas'} & sys.modules.keys()"
    )
    assert result.returncode == 0, result.stderr


def test_core_import_is_independent_of_providers():
    result = _subprocess(
        "import recorda, sys; assert not {'argdigest', 'smonitor', 'depdigest'} & sys.modules.keys()",
        provider_paths=False,
    )
    assert result.returncode == 0, result.stderr


def test_first_configuration_does_not_enable_global_scientific_capture():
    result = _subprocess(
        "import recorda; recorda.CapturePolicy(); import smonitor; "
        "config = smonitor.get_manager().config; "
        "assert not config.capture_logging and not config.capture_warnings and not config.capture_exceptions"
    )
    assert result.returncode == 0, result.stderr


def test_missing_provider_fails_at_configuration_use():
    result = _subprocess(
        "import sys, importlib.abc\n"
        "class Missing(importlib.abc.MetaPathFinder):\n"
        " def find_spec(self, fullname, path=None, target=None):\n"
        "  if fullname == 'argdigest': raise ModuleNotFoundError('missing argdigest')\n"
        "sys.meta_path.insert(0, Missing())\n"
        "import recorda\n"
        "try:\n recorda.CapturePolicy()\n"
        "except ModuleNotFoundError:\n pass\n"
        "else:\n raise AssertionError('missing provider must fail at use')\n"
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("provider", ["smonitor", "argdigest"])
def test_old_provider_is_rejected_before_configuration_values(provider):
    # Emulate precisely the absent APIs, without requiring old packages in CI.
    code = {
        "smonitor": "import smonitor; del smonitor.diagnostic_scope",
        "argdigest": "import argdigest; from dataclasses import dataclass; argdigest.DigestConfig = dataclass(type('OldConfig', (), {'__annotations__': {}}))",
    }[provider]
    code += "\nimport recorda\ntry:\n recorda.CapturePolicy()\nexcept (ImportError, TypeError):\n pass\nelse:\n raise AssertionError('old provider must fail')\n"
    result = _subprocess(code)
    assert result.returncode == 0, result.stderr


def test_compatibility_factory_uses_the_default_contract():
    from recorda.integrations.argdigest import capture_policy

    assert capture_policy(["b", "a"], inputs=False) == recorda.CapturePolicy(
        ["b", "a"], inputs=False
    )
    with pytest.raises(TypeError):
        capture_policy(skip_digestion=True)
    with pytest.raises(TypeError):
        capture_policy(None, False)


def test_journal_inspection_works_with_blocked_provider_imports(tmp_path):
    path = tmp_path / "read-only.jsonl"
    with recorda.session("test", path=path):
        pass
    code = (
        "import sys, importlib.abc\n"
        "class Missing(importlib.abc.MetaPathFinder):\n"
        " def find_spec(self, fullname, path=None, target=None):\n"
        "  if fullname.split('.')[0] in {'argdigest','smonitor','depdigest'}: raise ModuleNotFoundError(fullname)\n"
        "sys.meta_path.insert(0, Missing())\n"
        f"import recorda\nassert recorda.inspect({str(path)!r}).status == 'succeeded'\n"
        "assert not {'argdigest','smonitor','depdigest'} & sys.modules.keys()\n"
    )
    result = _subprocess(code, provider_paths=False)
    assert result.returncode == 0, result.stderr
