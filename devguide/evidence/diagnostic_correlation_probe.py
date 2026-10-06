"""Public SMonitor 0.19.0 research probes for uibcdf/recorda#15.

These characterize provider contracts, including limitations. They implement no
Recorda bridge. Configuration is explicit application-owned test setup.
"""

import asyncio
import hashlib
import json
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from contextvars import Context, copy_context

import pytest

CODE = "RECORDA-CORRELATION-PROBE-WARNING"
SOURCE = "recorda_correlation_probe.fit"
CODES = {CODE: {"user_message": "Selected fit diagnostic.", "metadata_message": "Fit diagnostic."}}


@pytest.fixture
def provider():
    import smonitor
    from smonitor.handlers.memory import MemoryHandler

    manager = smonitor.get_manager()
    # Flush earlier probe aggregates before configuring this application's sink.
    manager.flush_coalesced_warnings()
    manager.flush_duplicate_summaries()
    handler = MemoryHandler()
    manager = smonitor.configure(
        handlers=[handler],
        codes=CODES,
        profile="user",
        enabled=True,
        level="DEBUG",
        capture_logging=False,
        capture_warnings=False,
        capture_exceptions=False,
        profiling=False,
        filters=[],
        routes=[],
        silence=[],
        event_buffer_size=32,
        warning_coalesce_window_s=0,
        duplicate_policy="off",
        handler_error_threshold=0,
    )
    return smonitor, manager, handler


def emit(sm, **kwargs):
    return sm.emit("WARNING", "", code=CODE, source=SOURCE, **kwargs)


def test_public_handler_attach_detach_preserves_configuration(provider):
    from smonitor.handlers.memory import MemoryHandler

    sm, manager, original = provider
    observer = MemoryHandler()
    before = manager.config
    manager.add_handler(observer)
    try:
        emit(sm)
    finally:
        manager.remove_handler(observer)
    emit(sm)
    assert len(observer.events) == 1 and len(original.events) == 2
    assert manager.config is before


def test_explicit_application_reconfiguration_can_replace_attached_handler(provider):
    from smonitor.handlers.memory import MemoryHandler

    sm, manager, original = provider
    observer = MemoryHandler()
    manager.add_handler(observer)
    sm.configure(handlers=[original])
    emit(sm)
    assert len(original.events) == 1 and observer.events == []
    manager.remove_handler(observer)


def test_detailed_safe_facts_preserve_message_and_distinct_native_ids(provider):
    sm, manager, handler = provider
    before = manager.get_runtime_identifiers()
    facts = {"recorda_session_id": "rs-1", "recorda_operation_id": "op-1"}
    with sm.diagnostic_scope(sm.CapturePolicy(), safe_extra=facts):
        event = sm.emit("WARNING", "Native producer text.", code=CODE, source=SOURCE)
    assert event["message"] == "Native producer text."
    assert event["extra"]["recorda_operation_id"] == "op-1"
    assert event["session_id"] == before["session_id"] != "rs-1"
    assert manager.get_runtime_identifiers() == before
    assert len(handler.events) == 1
    assert "event_id" not in event


def test_metadata_only_changes_presentation_and_excludes_payload_before_delivery(provider):
    sm, _, handler = provider

    class Opaque:
        def __repr__(self):
            raise AssertionError("opaque repr must not run")

        def __str__(self):
            raise AssertionError("opaque str must not run")

    with sm.diagnostic_scope(safe_extra={"recorda_operation_id": "op-safe"}):
        event = sm.emit(
            "WARNING",
            "SYNTHETIC_MESSAGE_CANARY",
            code=CODE,
            source=SOURCE,
            extra={"payload": Opaque()},
            tags=["SYNTHETIC_TAG_CANARY"],
        )
    assert event["message"] == "Fit diagnostic."
    assert event["context"] is None and event["tags"] is None
    assert "payload" not in event["extra"]
    assert "CANARY" not in json.dumps(handler.events)


def test_task_interleaving_and_nested_restoration(provider):
    sm, _, handler = provider

    async def worker(identity):
        with sm.diagnostic_scope(sm.CapturePolicy(), safe_extra={"recorda_operation_id": identity}):
            await asyncio.sleep(0)
            emit(sm)
            with sm.diagnostic_scope(
                sm.CapturePolicy(), safe_extra={"recorda_operation_id": "child"}
            ):
                emit(sm)
            emit(sm)

    async def run():
        await asyncio.gather(worker("left"), worker("right"))

    asyncio.run(run())
    identities = [e["extra"]["recorda_operation_id"] for e in handler.events]
    assert identities.count("left") == identities.count("right") == identities.count("child") == 2
    assert "recorda_operation_id" not in emit(sm)["extra"]


def test_child_task_inherits_facts_after_parent_scope_ends(provider):
    sm, _, handler = provider

    async def run():
        ready = asyncio.Event()

        async def late():
            await ready.wait()
            emit(sm)

        with sm.diagnostic_scope(sm.CapturePolicy(), safe_extra={"recorda_operation_id": "ended"}):
            child = asyncio.create_task(late())
        ready.set()
        await child

    asyncio.run(run())
    assert handler.events[0]["extra"]["recorda_operation_id"] == "ended"


def test_thread_context_must_be_propagated_explicitly(provider):
    sm, _, _ = provider
    with sm.diagnostic_scope(sm.CapturePolicy(), safe_extra={"recorda_operation_id": "thread-op"}):
        inherited = copy_context()
        with ThreadPoolExecutor(max_workers=1) as pool:
            independent = pool.submit(Context().run, emit, sm).result()
            propagated = pool.submit(inherited.run, emit, sm).result()
    assert "recorda_operation_id" not in independent["extra"]
    assert propagated["extra"]["recorda_operation_id"] == "thread-op"


@pytest.mark.parametrize(
    "policy", [{"enabled": False}, {"level": "CRITICAL"}, {"silence": [SOURCE]}]
)
def test_early_suppression_has_no_handler_delivery(provider, policy):
    sm, _, handler = provider
    sm.configure(**policy)
    emit(sm)
    assert handler.events == []


def test_filter_drop_differs_from_native_buffer_retention(provider):
    sm, manager, handler = provider
    sm.configure(filters=[{"when": {"source": SOURCE}, "drop": True}])
    event = emit(sm)
    assert handler.events == []
    assert manager.recent_events(1)[0]["timestamp"] == event["timestamp"]


def test_route_selection_can_exclude_added_handler(provider):
    from smonitor.handlers.memory import MemoryHandler

    sm, manager, original = provider
    observer = MemoryHandler()
    observer.name = "probe_observer"
    manager.add_handler(observer)
    try:
        sm.configure(routes=[{"when": {"source": SOURCE}, "send_to": ["memory"]}])
        emit(sm)
        assert len(original.events) == 1 and observer.events == []
    finally:
        manager.remove_handler(observer)


@pytest.mark.parametrize(
    "config", [{"duplicate_policy": "emit_summary"}, {"warning_coalesce_window_s": 60}]
)
def test_aggregation_separates_safe_operation_facts_and_preserves_deferred_origin(provider, config):
    sm, manager, handler = provider
    sm.configure(**config)
    for identity in ("aggregate-left", "aggregate-right"):
        with sm.diagnostic_scope(safe_extra={"recorda_operation_id": identity}):
            emit(sm)
            emit(sm)
    assert len(handler.events) == 2
    assert handler.events[0]["fingerprint"] == handler.events[1]["fingerprint"]
    manager.flush_coalesced_warnings()
    manager.flush_duplicate_summaries()
    summaries = handler.events[2:]
    assert len(summaries) == 2
    assert {e["extra"]["recorda_operation_id"] for e in summaries} == {
        "aggregate-left",
        "aggregate-right",
    }
    assert all(e["extra"]["suppressed_count"] == 1 for e in summaries)


def test_ordinary_handler_failure_does_not_replace_native_return_or_exception(provider):
    sm, manager, _ = provider
    result = object()
    error = ValueError()

    class Faulty:
        name = "probe_faulty_ordinary"

        def handle(self, event, *, profile):
            raise OSError()

    observer = Faulty()
    manager.add_handler(observer)
    try:

        def success():
            emit(sm)
            return result

        def failure():
            emit(sm)
            raise error

        assert success() is result
        with pytest.raises(ValueError) as caught:
            failure()
        assert caught.value is error
        assert manager.report()["handler_errors"][observer.name] == 2
    finally:
        manager.remove_handler(observer)


def test_handler_degradation_warning_can_escape_direct_emit(provider):
    sm, manager, _ = provider

    class Faulty:
        name = "probe_faulty_threshold"

        def handle(self, event, *, profile):
            raise OSError()

    observer = Faulty()
    sm.configure(handler_error_threshold=1)
    manager.add_handler(observer)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            with pytest.raises(RuntimeWarning):
                emit(sm)
    finally:
        manager.remove_handler(observer)


def test_lower_buffer_limit_keeps_old_capacity_but_latest_window_is_selectable(provider):
    sm, manager, _ = provider
    for _ in range(4):
        emit(sm)
    sm.configure(event_buffer_size=2)
    for identity in ("old", "middle", "latest"):
        with sm.diagnostic_scope(sm.CapturePolicy(), safe_extra={"recorda_operation_id": identity}):
            emit(sm)
    assert [e["extra"]["recorda_operation_id"] for e in manager.recent_events(2)] == [
        "middle",
        "latest",
    ]
    # Existing backlog is popped one item per insertion. Lowering the limit
    # does not enforce the new capacity on that backlog (owning provider issue).
    assert len(manager.recent_events()) > 2


def test_bundle_event_redaction_does_not_redact_top_level_argv(provider, monkeypatch):
    sm, _, _ = provider
    monkeypatch.setattr(sys, "argv", ["probe", "SYNTHETIC_ARGV_CANARY"])
    sm.emit(
        "WARNING",
        "SYNTHETIC_MESSAGE_CANARY",
        code=CODE,
        source=SOURCE,
        extra={"payload": "SYNTHETIC_EXTRA_CANARY"},
    )
    bundle = sm.collect_bundle(
        drop_extra=True, drop_context=True, redact_fields=["message", "human_summary"]
    )
    assert bundle["argv"] == ["probe", "SYNTHETIC_ARGV_CANARY"]
    assert bundle["events"][-1]["message"] == "***"
    assert "extra" not in bundle["events"][-1] and "context" not in bundle["events"][-1]


def test_collecting_bundle_flushes_and_delivers_deferred_diagnostics(provider):
    sm, _, handler = provider
    sm.configure(duplicate_policy="emit_summary")
    with sm.diagnostic_scope(safe_extra={"recorda_operation_id": "bundle-flush"}):
        emit(sm)
        emit(sm)
    assert len(handler.events) == 1
    sm.collect_bundle()
    assert len(handler.events) == 2
    assert handler.events[-1]["code"] == "SMONITOR-EVENT-DUPLICATE-SUMMARY"
    assert handler.events[-1]["extra"]["recorda_operation_id"] == "bundle-flush"


def test_existing_explicit_boundary_can_reference_a_reviewed_native_bundle(
    provider, tmp_path, monkeypatch
):
    import recorda

    sm, _, _ = provider
    monkeypatch.setattr(sys, "argv", ["synthetic-bundle-probe"])
    journal = tmp_path / "record.jsonl"
    artifact = tmp_path / "native.json"
    with recorda.session("correlation-research", path=journal) as session:
        with session.operation("declared-probe") as operation:
            with sm.diagnostic_scope(
                sm.CapturePolicy(),
                safe_extra={
                    "recorda_session_id": session.id,
                    "recorda_operation_id": operation.id,
                },
            ):
                sm.emit("WARNING", "SYNTHETIC_NATIVE_TEXT", code=CODE, source=SOURCE)
            # Synthetic, reviewed fixture only; ordinary collect_bundle is not
            # a general safe export contract. Artifact bytes remain outside the journal.
            bundle = sm.collect_bundle(max_events=1)
            payload = json.dumps(bundle, sort_keys=True).encode()
            artifact.write_bytes(payload)
            reference = recorda.Reference(
                owner="smonitor",
                identifier="synthetic-bundle-1",
                revision="1",
                digest=hashlib.sha256(payload).hexdigest(),
            )
            operation.output("diagnostics", reference)
    event = bundle["events"][0]
    assert event["extra"]["recorda_operation_id"] == operation.id
    assert event["extra"]["recorda_session_id"] == session.id
    assert "SYNTHETIC_NATIVE_TEXT" not in journal.read_text()
    assert "argv" not in journal.read_text()
    inspected = recorda.inspect(journal)
    assert inspected.status == "succeeded" and len(inspected.operations) == 1
    assert inspected.operations[0]["outputs"]["diagnostics"]["owner"] == "smonitor"
    resolver = recorda.LocalFileResolver(
        tmp_path, {reference: artifact.name}, digest_algorithm="sha256"
    )
    assert recorda.check_reference(reference, resolver=resolver)["status"] == "matched"
    artifact.unlink()
    assert recorda.check_reference(reference, resolver=resolver)["status"] == "missing"
    assert recorda.inspect(journal).status == "succeeded"
