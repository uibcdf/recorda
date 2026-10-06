"""Opt-in installed/source provider qualification; baseline needs no SMonitor."""

import asyncio
import json
import os
import subprocess
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

import recorda

pytestmark = pytest.mark.skipif(
    os.environ.get("RECORDA_TEST_SMONITOR") != "1",
    reason="explicit SMonitor source qualification lane",
)


class NativeFailure(ValueError):
    def __str__(self):
        raise AssertionError("native text must not be inspected")

    def __repr__(self):
        raise AssertionError("native repr must not be inspected")


@pytest.fixture
def configured():
    import smonitor
    from smonitor.handlers.memory import MemoryHandler

    handler = MemoryHandler()
    manager = smonitor.configure(
        handlers=[handler],
        level="ERROR",
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


def test_adapter_registers_without_replacing_application_policy(configured):
    from recorda.integrations.smonitor import SMonitorRecoveryDiagnostics

    smonitor, manager, handler = configured
    before = manager.config
    SMonitorRecoveryDiagnostics()
    SMonitorRecoveryDiagnostics()
    assert manager.config is before
    assert handler.events == []
    message, _ = smonitor.resolve(code="RECORDA-RECOVERY-SESSION-001", profile="user")
    assert "persist session completion" in message
    assert manager.config is before


@pytest.mark.parametrize("stage", ["operation", "session", "both"])
@pytest.mark.parametrize("write_stage", ["before-line", "after-line-fsync"])
def test_native_failure_and_recording_gap_survive_safe_emission(
    tmp_path, monkeypatch, configured, stage, write_stage
):
    from recorda.integrations.smonitor import SMonitorRecoveryDiagnostics

    smonitor, manager, handler = configured
    policy = manager.config
    native, cause = NativeFailure("scientific secret"), ValueError("cause secret")
    handle = recorda.session(
        "private label",
        path=tmp_path / "private.jsonl",
        recovery_diagnostics=SMonitorRecoveryDiagnostics(),
    )
    append = handle._append

    def broken(event, **data):
        if event.endswith("_finished") and (stage == "both" or event == f"{stage}_finished"):
            if write_stage == "after-line-fsync":

                def fail_fsync(fd):
                    raise OSError("private disk path")

                with monkeypatch.context() as patch:
                    patch.setattr(os, "fsync", fail_fsync)
                    return append(event, **data)
            raise OSError("private disk path")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)

    @smonitor.signal(extra_factory=lambda a, k: {"private": "producer secret"})
    def provider():
        # The enclosing producer owns its own error telemetry. Catch inside that
        # frame so the test isolates Recorda's emission rather than native logging.
        with pytest.raises(NativeFailure) as caught:
            with handle:
                with handle.operation("private operation"):
                    raise native from cause
        return caught.value

    assert provider() is native and native.__cause__ is cause
    events = [event for event in handler.events if event["source"] == "recorda.recovery"]
    assert len(events) == (2 if stage == "both" else 1)
    for event in events:
        assert event["context"] is None
        assert event["message"]
        assert event["extra"]["recorda_session_id"] == handle.id
        assert "private" not in json.dumps(event)
        assert "secret" not in json.dumps(event)
    assert manager.config is policy
    # Failed durability after a full final line cannot be inferred by a reader.
    if write_stage == "before-line" or stage == "operation":
        assert handle.record.status == "incomplete"
    assert handle._file is None
    assert smonitor.get_capture_policy() == smonitor.CapturePolicy()


@pytest.mark.parametrize("fault", [RuntimeError, KeyboardInterrupt])
def test_emission_faults_keep_fixed_note_and_native_failure(
    tmp_path, monkeypatch, configured, fault
):
    import recorda.integrations.smonitor as adapter

    native = NativeFailure("scientific secret")
    sink = adapter.SMonitorRecoveryDiagnostics()

    def broken_emit(*args, **kwargs):
        raise fault("diagnostic secret")

    monkeypatch.setattr(adapter, "emit", broken_emit)
    with pytest.raises(NativeFailure) as caught:
        with recorda.session(
            "dummy", path=tmp_path / "record.jsonl", recovery_diagnostics=sink
        ) as handle:
            monkeypatch.setattr(handle, "_append", broken_emit)
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                raise native
    assert caught.value is native
    assert any("persist session completion" in note for note in native.__notes__)
    assert handle.record.status == "incomplete"


def test_interleaved_task_and_thread_diagnostics_keep_recorda_identities(tmp_path, configured):
    from recorda.integrations.smonitor import SMonitorRecoveryDiagnostics

    _, _, handler = configured
    sink = SMonitorRecoveryDiagnostics()

    def fail(index):
        native = NativeFailure("scientific secret")
        with pytest.raises(NativeFailure) as caught:
            with recorda.session(
                "dummy", path=tmp_path / f"{index}.jsonl", recovery_diagnostics=sink
            ) as handle:

                def broken(*args, **kwargs):
                    raise OSError("private disk path")

                handle._append = broken
                raise native
        assert caught.value is native
        return handle.id

    async def run():
        async def work(index):
            native = NativeFailure("scientific secret")
            with pytest.raises(NativeFailure) as caught:
                with recorda.session(
                    "dummy", path=tmp_path / f"{index}.jsonl", recovery_diagnostics=sink
                ) as handle:

                    def broken(*args, **kwargs):
                        raise OSError("private disk path")

                    handle._append = broken
                    await asyncio.sleep(0)
                    raise native
            assert caught.value is native
            return handle.id

        return await asyncio.gather(*(work(index) for index in range(3)))

    ids = asyncio.run(run())
    with ThreadPoolExecutor(max_workers=3) as pool:
        ids.extend(pool.map(fail, range(3, 6)))
    assert sorted(event["extra"]["recorda_session_id"] for event in handler.events) == sorted(ids)
    assert len(set(ids)) == 6


def test_filtered_delivery_does_not_remove_recovery_note(tmp_path, monkeypatch, configured):
    from recorda.integrations.smonitor import SMonitorRecoveryDiagnostics

    smonitor, _, handler = configured
    sink = SMonitorRecoveryDiagnostics()
    smonitor.configure(level="CRITICAL")
    native = NativeFailure("scientific secret")

    def broken(*args, **kwargs):
        raise OSError("private disk path")

    with pytest.raises(NativeFailure) as caught:
        with recorda.session(
            "dummy", path=tmp_path / "record.jsonl", recovery_diagnostics=sink
        ) as handle:
            monkeypatch.setattr(handle, "_append", broken)
            raise native
    assert caught.value is native
    assert native.__notes__
    assert handler.events == []
    assert handle.record.status == "incomplete"


def test_core_import_is_independent_and_old_provider_fails_before_activation():
    code = """
import sys, types, recorda
assert "smonitor" not in sys.modules
old = types.ModuleType("smonitor")
old.emit = lambda *a, **k: None
sys.modules["smonitor"] = old
try:
    import recorda.integrations.smonitor
except ImportError:
    pass
else:
    raise AssertionError("missing scoped API must fail before recording")
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path(recorda.__file__).resolve().parents[1])
    subprocess.run(
        [sys.executable, "-c", code], check=True, capture_output=True, text=True, env=env
    )
