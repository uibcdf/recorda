"""Research probes for #14; no Recorda presentation implementation.

Run with a verified published SMonitor 0.19.0 installation and published receptor:
python -m pytest -p pytest_receptor.plugin --receptor=llm <this-file>
"""

import json

import pytest

CODES = {
    "RECORDA-PRESENTATION-PROBE-MISSING": {
        "user_message": "{count} retained reference occurrences are missing now.",
        "dev_message": "Local reference observation: missing ({count} occurrences).",
        "user_hint": "Restore retained bytes or supply the correct local index.",
        "dev_hint": "Review the trusted index and retained native artifacts.",
        "metadata_hint": "Check retained files and the supplied local index; execution is unchanged.",
    },
    "RECORDA-PRESENTATION-PROBE-SHARED": {
        "user_message": "User audience: {count} missing references.",
        "dev_message": "Developer audience: {count} missing references.",
        "metadata_message": "Shared safe audience: {count} missing references.",
        "metadata_hint": "Shared safe action.",
    },
    "RECORDA-PRESENTATION-PROBE-PROFILE-HINT": {
        "user_message": "{count} missing reference occurrences.",
        "user_hint": "Restore retained bytes.",
        "dev_hint": "Review local index binding.",
    },
    "RECORDA-PRESENTATION-PROBE-TRAVERSAL": {
        "user_message": "Do not evaluate {count.secret}.",
        "metadata_hint": "Do not evaluate {count[0]}.",
    },
}


@pytest.fixture
def provider(tmp_path):
    import smonitor
    from smonitor.handlers.memory import MemoryHandler
    from smonitor.integrations import register_provider

    handler = MemoryHandler()
    # Explicit application policy is test setup only. A future Recorda renderer
    # would register its provider and resolve, never configure the application.
    manager = smonitor.configure(
        handlers=[handler],
        profile="qa",
        enabled=True,
        level="DEBUG",
        args_summary=True,
        capture_logging=False,
        capture_warnings=False,
        capture_exceptions=False,
        profiling=False,
        filters=[],
        routes=[],
    )
    before = manager.config
    package = tmp_path / "provider"
    package.mkdir()
    (package / "_smonitor.py").write_text("CODES = " + json.dumps(CODES) + "\nSIGNALS = {}\n")
    register_provider(package)
    register_provider(package)
    assert manager.config is before
    assert handler.events == []
    return smonitor, manager, handler, before


@pytest.mark.parametrize("profile", ["user", "dev", "qa", "agent"])
def test_safe_resolution_is_nonemitting_and_preserves_application_policy(provider, profile):
    smonitor, manager, handler, before = provider
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        message, hint = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-MISSING", profile=profile)
    assert "2" in message and message
    assert hint == CODES["RECORDA-PRESENTATION-PROBE-MISSING"]["metadata_hint"]
    assert manager.config is before and handler.events == []


def test_profiles_can_differ_without_shared_metadata_message(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        user = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-MISSING", profile="user")
        dev = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-MISSING", profile="dev")
    assert user[0] != dev[0] and user[1] == dev[1]
    assert handler.events == []


def test_resolution_survives_delivery_filtering_without_changing_it(provider):
    smonitor, manager, handler, _ = provider
    smonitor.configure(enabled=False, level="CRITICAL", handlers=[handler])
    filtered = manager.config
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        message, hint = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-MISSING", profile="user")
    assert message and hint and handler.events == []
    assert manager.config is filtered


def test_shared_metadata_message_overrides_the_audience(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        user = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-SHARED", profile="user")
        dev = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-SHARED", profile="dev")
    assert user == dev == ("Shared safe audience: 2 missing references.", "Shared safe action.")
    assert handler.events == []


def test_ordinary_profile_hints_are_absent_in_metadata_only_resolution(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        for profile in ("user", "dev"):
            message, hint = smonitor.resolve(
                code="RECORDA-PRESENTATION-PROBE-PROFILE-HINT", profile=profile
            )
            assert message == "2 missing reference occurrences." and hint is None
    assert handler.events == []


def test_missing_approved_field_does_not_echo_context_or_template(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope(safe_extra={"private": "SECRET"}):
        message, hint = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-MISSING")
    assert message and "SECRET" not in message and "{count}" not in message
    assert hint == CODES["RECORDA-PRESENTATION-PROBE-MISSING"]["metadata_hint"]
    assert handler.events == []


def test_unknown_catalog_code_returns_safe_generic_fallback(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope():
        message, hint = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-UNKNOWN")
    assert message and hint is None and handler.events == []


def test_safe_template_refuses_attribute_and_index_traversal(provider):
    smonitor, _, handler, _ = provider
    with smonitor.diagnostic_scope(safe_extra={"count": 2}):
        message, hint = smonitor.resolve(code="RECORDA-PRESENTATION-PROBE-TRAVERSAL")
    assert message and "{count" not in message and hint is None and handler.events == []


def test_opaque_values_are_rejected_without_stringification(provider):
    smonitor, _, handler, _ = provider

    class Opaque:
        def __str__(self):
            raise AssertionError("native text must not be evaluated")

        def __repr__(self):
            raise AssertionError("native repr must not be evaluated")

    with pytest.raises(smonitor.CapturePolicyError):
        with smonitor.diagnostic_scope(safe_extra={"count": Opaque()}):
            pytest.fail("invalid facts must not reach rendering")
    assert handler.events == []


def test_catalog_collision_is_atomic_and_does_not_reconfigure(provider, tmp_path):
    from smonitor.integrations import register_provider

    _, manager, handler, before = provider
    codes_before = manager.get_codes()
    providers_before = manager.get_providers()
    package = tmp_path / "conflicting-provider"
    package.mkdir()
    conflicting = {
        "RECORDA-PRESENTATION-PROBE-MISSING": {"user_message": "Different definition."},
        "RECORDA-PRESENTATION-PROBE-PARTIAL": {"user_message": "Must not be registered."},
    }
    (package / "_smonitor.py").write_text("CODES = " + json.dumps(conflicting) + "\n")
    with pytest.raises(ValueError):
        register_provider(package)
    assert manager.get_codes() == codes_before
    assert manager.get_providers() == providers_before
    assert manager.config is before and handler.events == []
