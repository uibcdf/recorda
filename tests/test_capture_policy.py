"""Selected lifecycle is durable; excluded outcomes and payload are unobserved."""

import asyncio
import json
from dataclasses import FrozenInstanceError

import pytest

import recorda


@pytest.mark.parametrize(
    "options",
    [
        {"profiles": "analysis"},
        {"profiles": [None]},
        {"profiles": ["x" * 257]},
        {"profiles": [str(i) for i in range(65)]},
        {"inputs": 1},
        {"outputs": None},
    ],
)
def test_invalid_selection_is_rejected(options):
    with pytest.raises((TypeError, ValueError)):
        recorda.CapturePolicy(**options)


def test_configuration_is_frozen_and_copied_before_activation(tmp_path):
    profiles = ["analysis"]
    policy = recorda.CapturePolicy(profiles=profiles)
    profiles.append("inspection")
    assert policy.profiles == ("analysis",)
    with pytest.raises(FrozenInstanceError):
        policy.inputs = False
    with pytest.raises(TypeError):
        recorda.start("invalid", path=tmp_path / "unused.jsonl", capture_policy={})
    assert not (tmp_path / "unused.jsonl").exists()


def test_minimal_selected_boundary_keeps_identity_without_payload_adapters(tmp_path):
    value = object()

    def forbidden(value):
        pytest.fail("disabled adapter was invoked")

    @recorda.record("analyze", profile="analysis")
    def analyze(samples):
        return samples

    policy = recorda.CapturePolicy(inputs=False, parameters=False, outputs=False)
    handle = recorda.start(
        "minimal",
        path=tmp_path / "minimal.jsonl",
        capture_policy=policy,
        reference_adapters={object: forbidden},
    )
    try:
        assert analyze(value) is value
        with handle.operation("explicit", parameters={"sensitive": value}) as operation:
            operation.output("result", value)
    finally:
        result = recorda.stop()
    assert result.status == "succeeded" and len(result.operations) == 2
    for operation in result.operations:
        assert operation["id"] and operation["start"] and operation["end"]
        assert operation["status"] == "succeeded"
        assert operation["inputs"] == operation["parameters"] == operation["outputs"] == {}
        assert operation["capture"]["outputs"] == "omitted_by_policy"
    assert result.operations[0]["implementation"]["callable"].endswith("analyze")
    assert result.coverage["excluded_boundaries"] == {"by_profile": [], "other_calls": 0}
    assert "operation_output" not in handle.path.read_text()


def test_filtered_parent_keeps_nearest_recorded_ancestor_and_native_result(tmp_path):
    sentinel = object()

    @recorda.record("leaf", profile="analysis")
    def leaf(value):
        return value

    @recorda.record("middle", profile="inspection")
    def middle(value):
        return leaf(value)

    @recorda.record("root", profile="analysis")
    def root(value):
        return middle(value)

    handle = recorda.start(
        "nested",
        path=tmp_path / "nested.jsonl",
        capture_policy=recorda.CapturePolicy(profiles=["analysis"]),
    )
    try:
        assert root(sentinel) is sentinel
    finally:
        result = handle.stop()
    parent, child = result.operations
    assert [parent["name"], child["name"]] == ["root", "leaf"]
    assert child["parent_id"] == parent["id"]
    assert result.coverage["excluded_boundaries"]["by_profile"] == [
        {"profile": "inspection", "calls": 1}
    ]


def test_excluded_explicit_and_unprofiled_calls_preserve_unobserved_errors(tmp_path):
    native = ValueError("private native detail")

    @recorda.record("excluded")
    def excluded():
        raise native

    def forbidden(value):
        pytest.fail("excluded payload adapter invoked")

    handle = recorda.start(
        "excluded",
        path=tmp_path / "excluded.jsonl",
        capture_policy=recorda.CapturePolicy(profiles=[]),
        reference_adapters={object: forbidden, ValueError: forbidden},
    )
    try:
        with pytest.raises(ValueError) as raised:
            excluded()
        assert raised.value is native
        with pytest.raises(ValueError) as raised:
            with handle.operation("explicit", inputs={"value": object()}) as operation:
                operation.output("value", object())
                raise native
        assert raised.value is native
    finally:
        result = handle.stop()
    assert result.operations == [] and result.status == "succeeded"
    assert result.coverage["excluded_boundaries"]["by_profile"] == [{"profile": None, "calls": 2}]
    assert "private" not in handle.path.read_text()
    with pytest.raises(RuntimeError):
        operation.output("value", object())
    with pytest.raises(RuntimeError):
        operation.__enter__()


def test_async_selected_failure_preserves_native_error_with_disabled_reference(tmp_path):
    native = ValueError("private native detail")
    calls = []

    def forbidden(value):
        pytest.fail("disabled exception adapter invoked")

    @recorda.record("analysis", profile="analysis")
    async def analyze():
        await asyncio.sleep(0)
        raise native

    @recorda.record("inspection", profile="inspection")
    async def inspect():
        calls.append("executed")
        return 7

    async def run():
        handle = recorda.start(
            "async",
            path=tmp_path / "async.jsonl",
            capture_policy=recorda.CapturePolicy(profiles=["analysis"], exception_references=False),
            reference_adapters={ValueError: forbidden},
        )
        try:
            assert await inspect() == 7
            with pytest.raises(ValueError) as raised:
                await analyze()
            assert raised.value is native
        finally:
            result = handle.stop()
        assert result.status == "failed" and calls == ["executed"]
        error = result.operations[0]["exception"]
        assert error["type"] == "builtins.ValueError"
        assert error["reference"] == {"kind": "omitted", "reason": "capture_policy"}
        assert "private" not in handle.path.read_text()

    asyncio.run(run())


def test_exclusion_counts_are_bounded_and_unavailable_before_durable_finalization(tmp_path):
    handle = recorda.start(
        "counts", path=tmp_path / "counts.jsonl", capture_policy=recorda.CapturePolicy(profiles=[])
    )
    try:
        for index in range(70):
            with handle.operation("declared", profile=f"profile{index}"):
                pass
        assert handle.record.coverage["excluded_boundaries"] is None
        assert handle.record.status == "incomplete"
    finally:
        result = handle.stop()
    counts = result.coverage["excluded_boundaries"]
    assert len(counts["by_profile"]) == 64 and counts["other_calls"] == 6
    assert sum(row["calls"] for row in counts["by_profile"]) + counts["other_calls"] == 70
    assert len(handle.path.read_text().splitlines()) == 2


def test_policy_does_not_relax_selected_writer_faults(tmp_path, monkeypatch):
    calls = []

    @recorda.record("analysis", profile="analysis")
    def selected():
        calls.append("selected")
        return 1

    @recorda.record("inspection", profile="inspection")
    def excluded():
        calls.append("excluded")
        return 2

    handle = recorda.start(
        "fault",
        path=tmp_path / "fault.jsonl",
        capture_policy=recorda.CapturePolicy(profiles=["analysis"]),
    )
    append = handle._append

    def broken(event, **data):
        if event == "operation_finished":
            raise OSError("disk unavailable")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)
    try:
        with pytest.raises(OSError):
            selected()
        with pytest.raises(OSError, match="unresolved persistence"):
            selected()
        assert excluded() == 2
    finally:
        result = handle.stop()
    assert calls == ["selected", "excluded"] and result.status == "incomplete"
    assert result.coverage["excluded_boundaries"]["by_profile"][0]["calls"] == 1


def test_all_profiles_policy_records_unlabelled_calls_and_safe_reference(tmp_path):
    sentinel = object()
    reference = recorda.Reference(owner="dummy", identifier="result1")

    @recorda.record("unlabelled")
    def target(value):
        return value

    handle = recorda.start(
        "all",
        path=tmp_path / "all.jsonl",
        capture_policy=recorda.CapturePolicy(),
        reference_adapters={object: lambda value: reference},
    )
    try:
        assert target(sentinel) is sentinel
    finally:
        result = handle.stop()
    operation = result.operations[0]
    assert operation["profile"] is None
    assert operation["outputs"]["return"]["identifier"] == "result1"
    assert (
        json.loads(handle.path.read_text().splitlines()[0])["coverage"]["capture_policy"][
            "profiles"
        ]
        is None
    )


def test_failed_session_marker_leaves_excluded_counts_unknown(tmp_path, monkeypatch):
    handle = recorda.start(
        "unclosed",
        path=tmp_path / "unclosed.jsonl",
        capture_policy=recorda.CapturePolicy(profiles=[]),
    )
    with handle.operation("excluded", profile="inspection"):
        pass
    append = handle._append

    def broken(event, **data):
        if event == "session_finished":
            raise OSError("disk unavailable")
        return append(event, **data)

    monkeypatch.setattr(handle, "_append", broken)
    with pytest.raises(OSError):
        handle.stop()
    assert handle.record.coverage["excluded_boundaries"] is None
    assert handle.record.status == "incomplete"


def test_excluded_async_failure_is_native_and_has_no_recorded_outcome(tmp_path):
    native = ValueError("private")

    @recorda.record("excluded", profile="inspection")
    async def excluded():
        await asyncio.sleep(0)
        raise native

    async def run():
        handle = recorda.start(
            "excluded_async",
            path=tmp_path / "async.jsonl",
            capture_policy=recorda.CapturePolicy(profiles=["analysis"]),
        )
        try:
            with pytest.raises(ValueError) as raised:
                await excluded()
            assert raised.value is native
        finally:
            result = handle.stop()
        assert result.operations == [] and result.status == "succeeded"
        assert result.coverage["excluded_boundaries"]["by_profile"] == [
            {"profile": "inspection", "calls": 1}
        ]

    asyncio.run(run())
