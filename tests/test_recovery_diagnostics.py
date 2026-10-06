"""Recovery diagnostics cannot replace scientific failures or expose their payloads."""

import asyncio
import traceback

import pytest

import recorda


class NativeFailure(ValueError):
    def __str__(self):
        raise AssertionError("native text must not be inspected")

    def __repr__(self):
        raise AssertionError("native repr must not be inspected")

    def add_note(self, note):
        raise AssertionError("a native override must not intercept recovery")


@pytest.mark.parametrize("stage", ["operation", "session"])
@pytest.mark.parametrize("diagnostic_fault", [None, OSError, KeyboardInterrupt])
def test_recovery_preserves_native_failure_and_incomplete_journal(
    tmp_path, monkeypatch, stage, diagnostic_fault
):
    seen = []
    native = NativeFailure("scientific secret")
    cause = LookupError("cause secret")

    def diagnostics(code, **facts):
        seen.append((code, facts))
        if diagnostic_fault:
            raise diagnostic_fault("diagnostic secret")

    handle = recorda.session(
        "dummy", path=tmp_path / "record.jsonl", recovery_diagnostics=diagnostics
    )
    append = handle._append

    def broken(event, **data):
        if event == f"{stage}_finished":
            raise OSError("private disk path")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)

    def target():
        raise native from cause

    with pytest.raises(NativeFailure) as caught:
        with handle:
            with handle.operation("dummy.fail"):
                target()
    assert caught.value is native
    assert native.__cause__ is cause
    assert traceback.extract_tb(native.__traceback__)[-1].name == "target"
    assert len(seen) == 1
    code, facts = seen[0]
    assert code == f"RECORDA-RECOVERY-{stage.upper()}-001"
    assert facts["session_id"] == handle.id
    assert set(facts) == (
        {"session_id", "operation_id"} if stage == "operation" else {"session_id"}
    )
    assert all(type(value) is str for value in facts.values())
    assert any(f"persist {stage} completion" in note for note in native.__notes__)
    assert handle.record.status == "incomplete"
    assert handle._file is None
    assert "secret" not in handle.path.read_text()
    following = recorda.start("next", path=tmp_path / "next.jsonl")
    assert following.stop().status == "succeeded"


def test_success_and_ordinary_native_failure_do_not_emit_recovery(tmp_path):
    seen = []
    native = ValueError("private")
    handle = recorda.start(
        "dummy", path=tmp_path / "record.jsonl", recovery_diagnostics=lambda *a, **k: seen.append(k)
    )
    try:
        with handle.operation("dummy.success"):
            pass
        with pytest.raises(ValueError) as caught:
            with handle.operation("dummy.failure"):
                raise native
        assert caught.value is native
    finally:
        result = handle.stop()
    assert seen == []
    assert result.status == "failed"


def test_diagnostic_feedback_does_not_reenter_sink(tmp_path, monkeypatch):
    seen = []
    inner_error, outer_error = ValueError("inner private"), ValueError("outer private")

    def diagnostics(code, **facts):
        seen.append(code)
        with pytest.raises(ValueError) as caught:
            with recorda.session(
                "inner", path=tmp_path / "inner.jsonl", recovery_diagnostics=diagnostics
            ) as inner:
                monkeypatch.setattr(inner, "_append", fail)
                raise inner_error
        assert caught.value is inner_error

    def fail(*args, **kwargs):
        raise OSError("disk private")

    with pytest.raises(ValueError) as caught:
        with recorda.session(
            "outer", path=tmp_path / "outer.jsonl", recovery_diagnostics=diagnostics
        ) as outer:
            monkeypatch.setattr(outer, "_append", fail)
            raise outer_error
    assert caught.value is outer_error
    assert len(seen) == 1
    assert outer.record.status == recorda.inspect(tmp_path / "inner.jsonl").status == "incomplete"
    assert inner_error.__notes__


def test_invalid_sink_is_rejected_before_creating_a_journal(tmp_path):
    path = tmp_path / "record.jsonl"
    with pytest.raises(TypeError, match="recovery_diagnostics"):
        recorda.start("dummy", path=path, recovery_diagnostics=42)
    assert not path.exists()


def test_task_created_by_sink_can_deliver_after_parent_delivery_ends(tmp_path, monkeypatch):
    async def run():
        tasks, seen = [], []

        def diagnostics(code, **facts):
            seen.append(facts["session_id"])
            if not tasks:
                tasks.append(asyncio.create_task(fail("child")))

        async def fail(name):
            native = ValueError("private")
            with pytest.raises(ValueError) as caught:
                with recorda.session(
                    "dummy", path=tmp_path / f"{name}.jsonl", recovery_diagnostics=diagnostics
                ) as handle:

                    def broken(*args, **kwargs):
                        raise OSError("disk private")

                    monkeypatch.setattr(handle, "_append", broken)
                    raise native
            assert caught.value is native
            return handle.id

        parent = await fail("parent")
        child = await tasks[0]
        assert seen == [parent, child]

    asyncio.run(run())


@pytest.mark.parametrize("kind", ["async", "async-object", "generator"])
def test_deferred_diagnostic_sinks_are_rejected_before_activation(tmp_path, kind):
    async def async_sink(*args, **kwargs):
        pass

    class AsyncSink:
        async def __call__(self, *args, **kwargs):
            pass

    def generator_sink(*args, **kwargs):
        yield

    sink = {"async": async_sink, "async-object": AsyncSink(), "generator": generator_sink}[kind]
    path = tmp_path / "record.jsonl"
    with pytest.raises(TypeError, match="synchronous"):
        recorda.start("dummy", path=path, recovery_diagnostics=sink)
    assert not path.exists()
