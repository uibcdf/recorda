"""Observable contracts for the provisional standalone recording slice."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import recorda


def test_success_reopens_with_native_reference_and_declared_coverage(tmp_path):
    path = tmp_path / "success.jsonl"
    native = recorda.Reference(owner="dummy", identifier="result:1", revision="v1")
    with recorda.session("analysis", path=path, gaps=["unwrapped calls"]) as session:
        with session.operation(
            "dummy.mean", inputs={"samples": 3}, parameters={"scale": 2}
        ) as operation:
            operation.output("result", native)
    record = recorda.inspect(path)
    assert record.status == "succeeded"
    assert record.coverage == {"mode": "declared_boundaries", "known_gaps": ["unwrapped calls"]}
    assert record.operations[0]["status"] == "succeeded"
    assert record.operations[0]["outputs"]["result"]["identifier"] == "result:1"
    assert record.operations[0]["inputs"]["samples"] == 3


def test_original_exception_is_preserved_and_message_is_not_persisted(tmp_path):
    path = tmp_path / "failure.jsonl"
    error = ValueError("secret=do-not-save")
    with pytest.raises(ValueError) as caught:
        with recorda.session("failure", path=path) as session:
            with session.operation("dummy.fail"):
                raise error
    assert caught.value is error
    record = recorda.inspect(path)
    assert record.status == "failed"
    assert record.operations[0]["status"] == "failed"
    assert record.operations[0]["exception"]["type"] == "builtins.ValueError"
    assert "do-not-save" not in path.read_text()


def test_started_state_survives_hard_process_exit(tmp_path):
    path = tmp_path / "interrupted.jsonl"
    code = """
import os, sys, recorda
with recorda.session('interruption', path=sys.argv[1]) as session:
    with session.operation('dummy.interrupted'):
        os._exit(23)
"""
    env = dict(os.environ, PYTHONPATH=str(Path(recorda.__file__).resolve().parents[1]))
    process = subprocess.run([sys.executable, "-c", code, str(path)], check=False, env=env)
    assert process.returncode == 23
    record = recorda.inspect(path)
    assert record.status == "incomplete"
    assert record.operations[0]["status"] == "incomplete"


def test_inactive_decorator_does_not_capture_or_change_return_identity(tmp_path):
    sentinel = object()

    @recorda.record("dummy.identity")
    def identity(value):
        return value

    assert identity(sentinel) is sentinel
    assert list(tmp_path.iterdir()) == []


def test_decorator_and_explicit_boundary_share_parent_context(tmp_path):
    path = tmp_path / "nested.jsonl"

    @recorda.record("dummy.double")
    def double(value):
        return value * 2

    with recorda.session("nested", path=path) as session:
        with session.operation("workflow"):
            assert double(3) == 6
    parent, child = recorda.inspect(path).operations
    assert child["parent_id"] == parent["id"]
    assert child["outputs"]["return"] == 6
    assert child["implementation"]["callable"].endswith("double")


def test_secret_unsupported_and_oversized_values_are_omitted_without_repr(tmp_path):
    class Opaque:
        def __repr__(self):
            raise AssertionError("capture must not call repr")

    path = tmp_path / "safe.jsonl"
    with recorda.session("safe", path=path) as session:
        with session.operation(
            "dummy.safe",
            inputs={"api_key": "never-save", "client": Opaque(), "bulk": list(range(10000))},
        ):
            pass
    inputs = recorda.inspect(path).operations[0]["inputs"]
    assert inputs["api_key"]["reason"] == "sensitive_name"
    assert inputs["client"]["reason"] == "unsupported_type"
    assert inputs["bulk"]["reason"] == "unsupported_type"
    assert "never-save" not in path.read_text()


def test_existing_record_is_never_overwritten(tmp_path):
    path = tmp_path / "existing.jsonl"
    path.write_text("original")
    with pytest.raises(FileExistsError):
        with recorda.session("new", path=path):
            pass
    assert path.read_text() == "original"


def test_storage_failure_before_start_prevents_target_execution(tmp_path, monkeypatch):
    with recorda.session("io", path=tmp_path / "io.jsonl") as session:
        original = session._append

        def broken(event, **fields):
            if event == "operation_started":
                raise OSError("disk unavailable")
            return original(event, **fields)

        monkeypatch.setattr(session, "_append", broken)
        executed = False
        with pytest.raises(OSError):
            with session.operation("dummy.never"):
                executed = True
        assert not executed
    assert recorda.inspect(tmp_path / "io.jsonl").status == "incomplete"


def test_terminal_storage_failure_remains_incomplete(tmp_path, monkeypatch):
    path = tmp_path / "terminal.jsonl"
    with recorda.session("terminal", path=path) as session:
        original = session._append

        def broken(event, **fields):
            if event == "operation_finished":
                raise OSError("disk unavailable")
            return original(event, **fields)

        monkeypatch.setattr(session, "_append", broken)
        with pytest.raises(OSError):
            with session.operation("dummy.finished_computation"):
                pass
    assert recorda.inspect(path).status == "incomplete"
    assert recorda.inspect(path).operations[0]["status"] == "incomplete"


def test_truncated_tail_preserves_prior_started_operation(tmp_path):
    path = tmp_path / "tail.jsonl"
    with recorda.session("tail", path=path) as session:
        with session.operation("dummy.ok"):
            pass
    lines = path.read_bytes().splitlines(keepends=True)
    path.write_bytes(b"".join(lines[:2]) + b'{"unfinished":')
    record = recorda.inspect(path)
    assert record.status == "incomplete"
    assert record.operations[0]["status"] == "incomplete"
    assert record.problems == ["truncated_tail"]


def test_fsync_failure_after_complete_write_keeps_journal_inspectable(tmp_path, monkeypatch):
    path = tmp_path / "sync_failure.jsonl"
    original = os.fsync
    calls = 0

    def fail_operation_completion(fd):
        nonlocal calls
        calls += 1
        if calls == 3:
            raise OSError("fsync failed after the complete outcome line was written")
        original(fd)

    monkeypatch.setattr(os, "fsync", fail_operation_completion)
    with recorda.session("sync_failure", path=path) as session:
        with pytest.raises(OSError, match="fsync failed"):
            with session.operation("dummy.done"):
                pass
    assert recorda.inspect(path).status == "incomplete"
    events = [json.loads(line) for line in path.read_text().splitlines()]
    assert [event["sequence"] for event in events] == list(range(len(events)))


def test_nested_session_restores_outer_context(tmp_path):
    @recorda.record("dummy.call")
    def call():
        return 1

    with recorda.session("outer", path=tmp_path / "outer.jsonl"):
        call()
        with recorda.session("inner", path=tmp_path / "inner.jsonl"):
            call()
        call()
    assert len(recorda.inspect(tmp_path / "outer.jsonl").operations) == 2
    assert len(recorda.inspect(tmp_path / "inner.jsonl").operations) == 1


def test_reference_validation_and_metadata_omit_secrets(tmp_path):
    with pytest.raises(ValueError):
        recorda.Reference(owner="", identifier="r1")
    path = tmp_path / "metadata.jsonl"
    with recorda.session("meta", path=path) as session:
        with session.operation(
            "dummy.call", implementation={"package": "dummy", "token": "hidden"}
        ):
            pass
    assert "hidden" not in path.read_text()
    assert recorda.inspect(path).operations[0]["implementation"]["token"]["kind"] == "omitted"


def test_journal_writes_are_ordered_and_fsynced(tmp_path, monkeypatch):
    calls = []
    original = os.fsync

    def synced(fd):
        calls.append(fd)
        original(fd)

    monkeypatch.setattr(os, "fsync", synced)
    path = tmp_path / "ordered.jsonl"
    with recorda.session("ordered", path=path) as session:
        with session.operation("dummy.call"):
            events = [json.loads(line) for line in path.read_text().splitlines()]
            assert events[-1]["event"] == "operation_started"
            assert len(calls) >= 2
    events = [json.loads(line) for line in path.read_text().splitlines()]
    assert [event["sequence"] for event in events] == list(range(len(events)))


def test_scientific_failure_is_not_replaced_when_storage_also_fails(tmp_path, monkeypatch):
    path = tmp_path / "double_failure.jsonl"
    scientific_error = ValueError("private scientific detail")
    with pytest.raises(ValueError) as caught:
        with recorda.session("double", path=path) as session:
            original = session._append

            def broken(event, **fields):
                if event == "operation_finished":
                    raise OSError("private storage detail")
                return original(event, **fields)

            monkeypatch.setattr(session, "_append", broken)
            with session.operation("dummy.fail"):
                raise scientific_error
    assert caught.value is scientific_error
    assert recorda.inspect(path).status == "incomplete"
    assert "private" not in path.read_text()


def test_decorator_coroutines_keep_sibling_correlation_separate(tmp_path):
    import asyncio

    @recorda.record("dummy.child")
    async def child(value):
        await asyncio.sleep(0)
        return value

    @recorda.record("dummy.parent")
    async def parent(value):
        return await child(value)

    async def run():
        with recorda.session("tasks", path=tmp_path / "tasks.jsonl"):
            assert await asyncio.gather(parent(1), parent(2)) == [1, 2]

    asyncio.run(run())
    operations = recorda.inspect(tmp_path / "tasks.jsonl").operations
    parents = {op["id"]: op for op in operations if op["name"] == "dummy.parent"}
    assert len(parents) == 2
    assert all(op["parent_id"] is None for op in parents.values())
    for op in operations:
        if op["name"] == "dummy.child":
            assert op["inputs"]["value"] == parents[op["parent_id"]]["inputs"]["value"]


def test_unknown_schema_and_corruption_are_rejected(tmp_path):
    path = tmp_path / "corrupt.jsonl"
    with recorda.session("corrupt", path=path):
        pass
    events = [json.loads(line) for line in path.read_text().splitlines()]
    events[0]["schema"] = "future/1"
    path.write_text("".join(json.dumps(event) + "\n" for event in events))
    with pytest.raises(ValueError, match="unsupported schema"):
        recorda.inspect(path)


def test_generator_decorator_does_not_claim_unexecuted_body_as_success():
    with pytest.raises(TypeError, match="generator"):

        @recorda.record()
        def generate():
            yield 1
