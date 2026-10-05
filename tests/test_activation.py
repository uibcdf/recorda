"""Manual activation, ownership and safe decorator-driven capture contracts."""

import asyncio
import json
import os
import subprocess
import sys
from contextvars import copy_context
from dataclasses import dataclass
from pathlib import Path

import pytest

import recorda


@dataclass(frozen=True)
class NativeResult:
    identifier: str


def test_start_stop_observes_normal_calls_and_returns_native_identity(tmp_path):
    native = NativeResult("result:1")
    adapted = []

    def reference(value):
        adapted.append(value)
        return recorda.Reference(owner="dummy", identifier=value.identifier)

    @recorda.record("dummy.analyze", profile="scientific_analysis")
    def analyze(count=4):
        return native

    assert analyze() is native
    handle = recorda.start(
        "manual", path=tmp_path / "manual.jsonl", reference_adapters={NativeResult: reference}
    )
    try:
        assert analyze() is native
        assert handle.record.status == "incomplete"
        assert analyze(8) is native
    finally:
        recorded = recorda.stop()
    assert recorded.status == "succeeded"
    assert [operation["inputs"]["count"] for operation in recorded.operations] == [4, 8]
    assert all(operation["profile"] == "scientific_analysis" for operation in recorded.operations)
    assert all(
        operation["outputs"]["return"]["identifier"] == "result:1"
        for operation in recorded.operations
    )
    assert analyze() is native
    assert adapted == [native, native]
    assert len(recorda.inspect(handle.path).operations) == 2


def test_session_handle_owns_start_stop_and_cannot_be_reopened(tmp_path):
    handle = recorda.session("handle", path=tmp_path / "handle.jsonl")
    assert handle.start() is handle
    assert handle.stop().status == "succeeded"
    with pytest.raises(RuntimeError, match="cannot be reopened"):
        handle.start()
    with pytest.raises(RuntimeError, match="not active"):
        handle.stop()
    with pytest.raises(RuntimeError, match="no recording session"):
        recorda.stop()


def test_second_start_preserves_active_session_and_does_not_create_file(tmp_path):
    handle = recorda.start("first", path=tmp_path / "first.jsonl")
    try:
        with pytest.raises(RuntimeError, match="already active"):
            recorda.start("second", path=tmp_path / "second.jsonl")
        assert not (tmp_path / "second.jsonl").exists()
        with handle.operation("dummy.first"):
            pass
    finally:
        recorded = handle.stop()
    assert recorded.session_id == handle.id
    assert recorded.status == "succeeded"


def test_manual_stop_refuses_running_operation_and_can_retry_after_completion(tmp_path):
    handle = recorda.start("running", path=tmp_path / "running.jsonl")
    try:
        with handle.operation("dummy.running"):
            with pytest.raises(RuntimeError, match="operations are running"):
                recorda.stop()
            assert handle.record.status == "incomplete"
    finally:
        recorded = handle.stop()
    assert recorded.status == "succeeded"
    assert recorded.operations[0]["status"] == "succeeded"


def test_nested_context_manager_restores_manual_session(tmp_path):
    @recorda.record("dummy.call")
    def call():
        return 1

    handle = recorda.start("outer", path=tmp_path / "outer.jsonl")
    try:
        call()
        with recorda.session("inner", path=tmp_path / "inner.jsonl"):
            with pytest.raises(RuntimeError, match="not active"):
                handle.stop()
            call()
        call()
    finally:
        recorded = handle.stop()
    assert len(recorded.operations) == 2
    assert len(recorda.inspect(tmp_path / "inner.jsonl").operations) == 1


def test_inherited_context_cannot_finalize_activating_context_session(tmp_path):
    handle = recorda.start("owner", path=tmp_path / "owner.jsonl")
    try:
        with pytest.raises(RuntimeError, match="context that activated"):
            copy_context().run(recorda.stop)
        assert handle.record.status == "incomplete"
        with handle.operation("dummy.still_active"):
            pass
    finally:
        recorded = handle.stop()
    assert recorded.status == "succeeded"


def test_child_task_cannot_stop_owner_and_keeps_nested_calls_correlated(tmp_path):
    @recorda.record("dummy.child")
    async def child(value):
        await asyncio.sleep(0)
        return value

    @recorda.record("dummy.parent")
    async def parent(value):
        return await child(value)

    async def attempt_stop():
        with pytest.raises(RuntimeError, match="context that activated"):
            recorda.stop()

    async def run():
        handle = recorda.start("tasks", path=tmp_path / "tasks.jsonl")
        try:
            await asyncio.create_task(attempt_stop())
            assert await asyncio.gather(parent(1), parent(2)) == [1, 2]
        finally:
            recorded = handle.stop()
        return recorded

    recorded = asyncio.run(run())
    assert recorded.status == "succeeded"
    parents = {op["id"]: op for op in recorded.operations if op["name"] == "dummy.parent"}
    assert len(parents) == 2
    for operation in recorded.operations:
        if operation["name"] == "dummy.child":
            assert (
                operation["inputs"]["value"] == parents[operation["parent_id"]]["inputs"]["value"]
            )


def test_decorated_failure_preserves_exception_and_manual_session_records_failure(tmp_path):
    failure = ValueError("private scientific detail")

    @recorda.record("dummy.fail")
    def fail():
        raise failure

    handle = recorda.start("failure", path=tmp_path / "failure.jsonl")
    try:
        with pytest.raises(ValueError) as caught:
            fail()
        assert caught.value is failure
    finally:
        recorded = handle.stop()
    assert recorded.status == "failed"
    assert recorded.operations[0]["exception"]["type"] == "builtins.ValueError"
    assert "private scientific" not in handle.path.read_text()


@pytest.mark.parametrize("interrupt", [False, True], ids=["missing-stop", "hard-exit"])
def test_unclosed_manual_session_survives_process_exit(tmp_path, interrupt):
    path = tmp_path / "unclosed.jsonl"
    script = """
import os, sys, recorda
@recorda.record('dummy.call')
def call():
    if sys.argv[2] == 'interrupt':
        os._exit(23)
    return 1
recorda.start('unclosed', path=sys.argv[1])
call()
"""
    env = dict(os.environ, PYTHONPATH=str(Path(recorda.__file__).resolve().parents[1]))
    process = subprocess.run(
        [sys.executable, "-c", script, str(path), "interrupt" if interrupt else "normal"],
        env=env,
        check=False,
    )
    assert process.returncode == (23 if interrupt else 0)
    recorded = recorda.inspect(path)
    assert recorded.status == "incomplete"
    assert recorded.operations[0]["status"] == ("incomplete" if interrupt else "succeeded")


def test_completion_storage_failure_detaches_context_and_preserves_incomplete_record(
    tmp_path, monkeypatch
):
    handle = recorda.start("io", path=tmp_path / "io.jsonl")
    original = handle._append

    def broken(event, **fields):
        if event == "session_finished":
            raise OSError("storage unavailable")
        return original(event, **fields)

    monkeypatch.setattr(handle, "_append", broken)
    with pytest.raises(OSError):
        handle.stop()
    assert handle.record.status == "incomplete"
    next_handle = recorda.start("next", path=tmp_path / "next.jsonl")
    assert next_handle.stop().status == "succeeded"


def test_failed_start_does_not_activate_a_session(tmp_path, monkeypatch):
    handle = recorda.session("broken", path=tmp_path / "broken.jsonl")

    def broken(*args, **kwargs):
        raise OSError("storage unavailable")

    monkeypatch.setattr(handle, "_append", broken)
    with pytest.raises(OSError):
        handle.start()
    with pytest.raises(RuntimeError, match="no recording session"):
        recorda.stop()
    next_handle = recorda.start("next", path=tmp_path / "next.jsonl")
    assert next_handle.stop().status == "succeeded"


def test_adapter_configuration_is_snapshotted_and_does_not_inspect_unregistered_types(tmp_path):
    class Unknown(NativeResult):
        def __repr__(self):
            raise AssertionError("must not inspect unknown objects")

    calls = []

    def reference(value):
        calls.append(value)
        return recorda.Reference(owner="dummy", identifier=value.identifier)

    adapters = {NativeResult: reference}
    with recorda.session(
        "adapters", path=tmp_path / "adapters.jsonl", reference_adapters=adapters
    ) as handle:
        adapters.clear()
        with handle.operation(
            "dummy.inputs",
            inputs={
                "result": NativeResult("r1"),
                "token": NativeResult("secret"),
                "opaque": Unknown("r2"),
            },
        ):
            pass
    inputs = handle.record.operations[0]["inputs"]
    assert inputs["result"]["identifier"] == "r1"
    assert inputs["token"]["reason"] == "sensitive_name"
    assert inputs["opaque"]["reason"] == "unsupported_type"
    assert len(calls) == 1
    assert "secret" not in handle.path.read_text()


@pytest.mark.parametrize("broken", [False, True], ids=["invalid-return", "callback-error"])
def test_adapter_faults_are_explicit_omissions_and_leave_native_result_unchanged(tmp_path, broken):
    native = NativeResult("native")

    def faulty(value):
        if broken:
            raise ValueError("private adapter detail")
        return {"secret": "private adapter detail"}

    @recorda.record("dummy.result")
    def result():
        return native

    handle = recorda.start(
        "faulty_adapter", path=tmp_path / "faulty.jsonl", reference_adapters={NativeResult: faulty}
    )
    try:
        assert result() is native
    finally:
        recorded = handle.stop()
    omitted = recorded.operations[0]["outputs"]["return"]
    assert omitted["reason"] == (
        "reference_adapter_failed" if broken else "invalid_reference_adapter_result"
    )
    assert "private adapter" not in handle.path.read_text()


def test_invalid_reference_adapter_configuration_never_creates_journal(tmp_path):
    path = tmp_path / "bad.jsonl"
    with pytest.raises(TypeError, match="reference_adapters"):
        recorda.start("bad", path=path, reference_adapters={"NativeResult": object()})
    assert not path.exists()


def test_older_journal_without_profile_remains_readable(tmp_path):
    path = tmp_path / "old.jsonl"
    with recorda.session("old", path=path) as handle:
        with handle.operation("dummy.old"):
            pass
    events = [json.loads(line) for line in path.read_text().splitlines()]
    for event in events:
        event.pop("profile", None)
    path.write_text("".join(json.dumps(event) + "\n" for event in events))
    recorded = recorda.inspect(path)
    assert recorded.status == "succeeded"
    assert recorded.operations[0]["profile"] is None
