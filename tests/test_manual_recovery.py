"""Execution may end while its durable outcome remains incomplete."""

import asyncio
import json
import os
from contextvars import copy_context

import pytest

import recorda


@pytest.mark.parametrize("write_stage", ["before-line", "after-line-fsync"])
@pytest.mark.parametrize("native_failure", [False, True], ids=["returned", "raised"])
def test_stop_after_terminal_fault_preserves_prefix_and_allows_next_session(
    tmp_path, monkeypatch, write_stage, native_failure
):
    native = ValueError("private scientific detail")
    handle = recorda.start("fault", path=tmp_path / "fault.jsonl")
    append = handle._append
    original_fsync = os.fsync
    attempts = []

    def broken(event, **data):
        if event == "operation_finished":
            if write_stage == "before-line":
                raise OSError("private disk detail")
            with monkeypatch.context() as patch:

                def fail_fsync(fd):
                    raise OSError("private disk detail")

                patch.setattr(os, "fsync", fail_fsync)
                return append(event, **data)
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)

    @recorda.record("dummy.target")
    def target():
        attempts.append("executed")
        if native_failure:
            raise native
        return 23

    try:
        with pytest.raises(ValueError if native_failure else OSError) as raised:
            target()
        if native_failure:
            assert raised.value is native
        prefix = handle.path.read_bytes()
        # A broken writer must still prevent subsequent declared execution.
        with pytest.raises(OSError, match="unresolved persistence"):
            target()
        assert attempts == ["executed"]
    finally:
        record = handle.stop()
    assert os.fsync is original_fsync
    assert handle.path.read_bytes().startswith(prefix)
    assert record.status == "incomplete"
    assert record.operations[0]["status"] == (
        "incomplete"
        if write_stage == "before-line"
        else "failed"
        if native_failure
        else "succeeded"
    )
    events = [json.loads(line) for line in handle.path.read_text().splitlines()]
    assert events[-1]["status"] == "incomplete"
    assert [event["sequence"] for event in events] == list(range(len(events)))
    assert "private" not in handle.path.read_text()
    with pytest.raises(RuntimeError):
        handle.stop()
    next_session = recorda.start("next", path=tmp_path / "next.jsonl")
    assert next_session.stop().status == "succeeded"


def test_failed_stop_after_terminal_fault_detaches_owner_and_closes_journal(tmp_path, monkeypatch):
    native = ValueError("private")
    handle = recorda.start("failed_stop", path=tmp_path / "failed-stop.jsonl")
    append = handle._append

    def broken(event, **data):
        if event in {"operation_finished", "session_finished"}:
            raise OSError("private disk detail")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)
    with pytest.raises(ValueError) as raised:
        with handle.operation("dummy.fail"):
            raise native
    assert raised.value is native
    stream = handle._file
    with pytest.raises(OSError):
        handle.stop()
    assert stream.closed
    assert handle.record.status == "incomplete"
    next_session = recorda.start("next", path=tmp_path / "next.jsonl")
    assert next_session.stop().status == "succeeded"


def test_broken_writer_does_not_allow_stop_with_live_async_work_or_wrong_owner(
    tmp_path, monkeypatch
):
    native = ValueError("private")

    async def run():
        started, release = asyncio.Event(), asyncio.Event()
        completed = []

        @recorda.record("dummy.pending")
        async def pending():
            started.set()
            await release.wait()
            completed.append("executed")
            return 23

        handle = recorda.start("async_fault", path=tmp_path / "async.jsonl")
        append = handle._append

        def broken(event, **data):
            if event == "operation_finished":
                raise OSError("private disk detail")
            return append(event, **data)

        monkeypatch.setattr(handle, "_append", broken)
        task = asyncio.create_task(pending())
        await started.wait()
        try:
            with pytest.raises(ValueError) as raised:
                with handle.operation("dummy.fail"):
                    raise native
            assert raised.value is native
            with pytest.raises(RuntimeError, match="operations are running"):
                handle.stop()
            assert not task.done() and not completed
        finally:
            release.set()
            with pytest.raises(OSError):
                await task
        with pytest.raises(RuntimeError, match="context that activated"):
            copy_context().run(handle.stop)
        record = handle.stop()
        assert completed == ["executed"] and record.status == "incomplete"
        assert all(op["status"] == "incomplete" for op in record.operations)
        next_session = recorda.start("next", path=tmp_path / "next.jsonl")
        assert next_session.stop().status == "succeeded"

    asyncio.run(run())


def test_nested_terminal_faults_end_execution_without_losing_lineage(tmp_path, monkeypatch):
    native = ValueError("private")

    @recorda.record("dummy.child")
    def child():
        raise native

    @recorda.record("dummy.parent")
    def parent():
        child()

    handle = recorda.start("nested_fault", path=tmp_path / "nested.jsonl")
    append = handle._append

    def broken(event, **data):
        if event == "operation_finished":
            raise OSError("private disk detail")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)
    try:
        with pytest.raises(ValueError) as raised:
            parent()
        assert raised.value is native
    finally:
        record = handle.stop()
    assert record.status == "incomplete"
    assert record.operations[1]["parent_id"] == record.operations[0]["id"]
    assert all(op["status"] == "incomplete" for op in record.operations)
    next_session = recorda.start("next", path=tmp_path / "next.jsonl")
    with next_session.operation("dummy.new_root"):
        pass
    assert next_session.stop().operations[0]["parent_id"] is None
