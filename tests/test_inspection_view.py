"""Presentation preserves observations, policy and native ownership boundaries."""

import asyncio
import copy
import hashlib
import json
import logging
import os
import subprocess
import sys
import warnings
from pathlib import Path

import pytest

import recorda


@pytest.fixture
def snapshot(tmp_path):
    payload = b"retained native input"
    reference = recorda.Reference(
        "private owner", "private identifier", "r1", hashlib.sha256(payload).hexdigest()
    )
    path = tmp_path / "native.bin"
    path.write_bytes(payload)
    with recorda.session("private session", path=tmp_path / "record.jsonl") as handle:
        with handle.operation(
            "private operation", inputs={"first": reference, "second": reference}
        ):
            pass
    resolver = recorda.LocalFileResolver(
        tmp_path, {reference: path.name}, digest_algorithm="sha256"
    )
    return handle.record, resolver, path


def test_current_missing_bytes_do_not_relabel_execution_or_repeat_checking(snapshot, monkeypatch):
    record, resolver, path = snapshot
    path.unlink()
    report = recorda.check_references(record, resolver=resolver)
    before = copy.deepcopy((record, report))
    import recorda.references as references

    def forbidden(*args, **kwargs):
        raise AssertionError("presentation must not check references")

    monkeypatch.setattr(references, "_check_reference", forbidden)
    view = recorda.inspection_view(record, reference_report=report)
    assert view["execution"]["status"] == "succeeded"
    assert view["references"]["by_status"] == {"missing": 2}
    (finding,) = view["findings"]
    assert finding["state"] == "missing"
    assert finding["count"] == 2 and finding["distinct_references"] == 1
    assert finding["source_indices"] == [0, 1]
    assert "private" not in json.dumps(finding)
    assert view == recorda.inspection_view(record, reference_report=report)
    assert (record, report) == before
    view["record"]["operations"][0]["inputs"].clear()
    view["reference_report"]["references"].clear()
    assert (record, report) == before


@pytest.mark.parametrize("state", ["matched", "mismatched", "missing"])
def test_real_byte_observations_keep_the_original_record(snapshot, state):
    record, resolver, path = snapshot
    if state == "mismatched":
        path.write_bytes(b"different")
    elif state == "missing":
        path.unlink()
    report = recorda.check_references(record, resolver=resolver)
    view = recorda.inspection_view(record, reference_report=report)
    assert view["record"]["status"] == "succeeded"
    assert view["reference_report"] == report
    assert view["references"]["by_status"] == {state: 2}
    assert bool(view["findings"]) == (state != "matched")


def test_saved_observation_message_does_not_claim_fresh_checking(snapshot, configured):
    record, resolver, path = snapshot
    original = path.read_bytes()
    path.unlink()
    saved = recorda.check_references(record, resolver=resolver)
    path.write_bytes(original)
    fresh = recorda.check_references(record, resolver=resolver)
    assert {row["status"] for row in fresh["references"]} == {"matched"}
    view = recorda.inspection_view(record, reference_report=saved)
    assert view["reference_report"] == saved
    assert view["execution"]["status"] == "succeeded"
    (finding,) = view["findings"]
    assert finding["state"] == "missing" and finding["count"] == 2
    message = finding["presentation"]["message"]
    assert message.startswith("Supplied reference check: ")
    assert "now" not in message


@pytest.mark.parametrize(
    "state",
    [
        "matched",
        "missing",
        "mismatched",
        "unresolved",
        "available_unverified",
        "unsupported_digest",
        "too_large",
        "not_a_file",
        "outside_root",
        "invalid_reference",
        "unreadable",
        "unstable",
        "future_observation",
    ],
)
def test_all_states_and_unknown_observations_remain_structured(snapshot, state):
    record, _, _ = snapshot
    if state == "invalid_reference":
        for value in record.operations[0]["inputs"].values():
            value["owner"] = ""
    report = recorda.check_references(record)
    for row in report["references"]:
        row["status"] = state
    view = recorda.inspection_view(record, reference_report=report)
    assert view["references"]["by_status"] == {state: 2}
    if state == "matched":
        assert view["findings"] == []
    else:
        (finding,) = view["findings"]
        assert finding["state"] == ("unclassified" if state == "future_observation" else state)
        assert finding["count"] == 2
        if state == "invalid_reference":
            assert finding["distinct_references"] is None
        assert view["reference_report"]["references"][0]["status"] == state


def test_no_check_input_does_not_imply_an_empty_verified_report(snapshot):
    record, _, _ = snapshot
    view = recorda.inspection_view(record)
    assert view["reference_report"] is None
    assert view["references"]["check_state"] == "not_requested"
    assert view["references"]["declared_occurrences"] == 2
    assert view["references"]["checked_occurrences"] is None
    assert view["findings"] == []


def test_expected_omissions_and_excluded_calls_are_coverage(tmp_path):
    policy = recorda.CapturePolicy(profiles=["included"], inputs=False, outputs=False)
    with recorda.session(
        "selected", path=tmp_path / "selected.jsonl", capture_policy=policy
    ) as handle:
        with handle.operation("omitted", profile="included", inputs={"x": 1}):
            pass
        with handle.operation("excluded", profile="excluded"):
            pass
    record = handle.record
    unchecked = recorda.inspection_view(record)
    checked = recorda.inspection_view(record, reference_report=recorda.check_references(record))
    assert unchecked["coverage"] == checked["coverage"]
    assert checked["coverage"]["omissions_by_reason"] == {"capture_policy": 2}
    assert checked["coverage"]["excluded_calls"] == 1
    assert checked["references"]["checked_occurrences"] == 0
    assert checked["findings"] == []


def test_failed_exception_omission_and_incomplete_prefix_preserve_lifecycle(tmp_path):
    path = tmp_path / "failed.jsonl"
    with pytest.raises(ValueError):
        with recorda.session("native failure", path=path) as handle:
            with handle.operation("native"):
                raise ValueError("private exception")
    record = recorda.inspect(path)
    view = recorda.inspection_view(record, reference_report=recorda.check_references(record))
    assert view["execution"]["status"] == "failed"
    assert view["coverage"]["omissions_by_reason"] == {"unsupported_type": 1}
    lines = path.read_bytes().splitlines(keepends=True)
    path.write_bytes(b"".join(lines[:2]) + b'{"unfinished')
    record = recorda.inspect(path)
    view = recorda.inspection_view(record, reference_report=recorda.check_references(record))
    assert view["execution"]["status"] == "incomplete"
    assert [(f["domain"], f["state"], f["count"]) for f in view["findings"]] == [
        ("operations", "incomplete", 1),
        ("problems", "truncated_tail", 1),
    ]
    record.problems.append("future_problem")
    view = recorda.inspection_view(record)
    assert view["findings"][-1]["state"] == "unclassified"
    assert view["record"]["problems"][-1] == "future_problem"


@pytest.mark.parametrize(
    "mutation",
    [
        "session_id",
        "session_status",
        "coverage",
        "scope",
        "omissions",
        "incomplete_operations",
        "row_count",
        "operation_id",
        "operation_name",
        "operation_status",
        "group",
        "field",
        "owner",
        "identifier",
        "revision",
        "digest",
        "bytes_checked",
        "digest_algorithm",
        "extra_key",
        "conflicting_duplicate",
    ],
)
def test_report_binding_uses_complete_snapshot_not_only_session_id(snapshot, mutation):
    record, resolver, _ = snapshot
    report = recorda.check_references(record, resolver=resolver)
    row = report["references"][0]
    if mutation in {"session_id", "session_status", "scope"}:
        report[mutation] = "different"
    elif mutation == "coverage":
        report["coverage"]["known_gaps"].append("different")
    elif mutation in {"omissions", "incomplete_operations"}:
        report[mutation].append("different")
    elif mutation == "row_count":
        report["references"].pop()
    elif mutation in {"owner", "identifier", "revision", "digest"}:
        row["reference"][mutation] = "different"
    elif mutation == "bytes_checked":
        row[mutation] = True
    elif mutation == "extra_key":
        row[mutation] = "private"
    elif mutation == "conflicting_duplicate":
        row["status"] = "missing"
    else:
        row[mutation] = "different"
    with pytest.raises(ValueError):
        recorda.inspection_view(record, reference_report=report)


def test_mutated_snapshot_cannot_use_a_previous_report(snapshot):
    record, _, _ = snapshot
    report = recorda.check_references(record)
    record.operations[0]["inputs"].pop("second")
    with pytest.raises(ValueError):
        recorda.inspection_view(record, reference_report=report)


class Opaque:
    def __repr__(self):
        raise AssertionError("repr called")

    def __str__(self):
        raise AssertionError("str called")

    def __deepcopy__(self, memo):
        raise AssertionError("copy hook called")

    def __iter__(self):
        raise AssertionError("iteration hook called")


@pytest.mark.parametrize("value", [Opaque(), {"x": Opaque()}, float("nan"), 2**257, "x" * 4097])
def test_unsafe_input_is_rejected_before_provider_use(snapshot, monkeypatch, value):
    import recorda.presentation as presentation

    record, _, _ = snapshot
    record.operations[0]["outputs"]["unsafe"] = value
    monkeypatch.setattr(presentation, "_present", lambda findings: pytest.fail("provider reached"))
    with pytest.raises((TypeError, ValueError)):
        recorda.inspection_view(record)


def test_subclasses_and_structural_budgets_are_rejected(snapshot):
    class PretendList(list):
        def __iter__(self):
            raise AssertionError("subclass iteration")

    record, _, _ = snapshot
    record.problems = PretendList()
    with pytest.raises(TypeError):
        recorda.inspection_view(record)
    record.problems = []
    nested = []
    for _ in range(26):
        nested = [nested]
    record.operations[0]["outputs"]["deep"] = nested
    with pytest.raises(ValueError, match="structural budget"):
        recorda.inspection_view(record)
    record.operations[0]["outputs"] = {"wide": [list(range(10000)) for _ in range(12)]}
    with pytest.raises(ValueError, match="structural budget"):
        recorda.inspection_view(record)


def test_closed_public_options(snapshot):
    record, _, _ = snapshot
    for kwargs in ({"profile": "dev"}, {"skip_digestion": True}):
        with pytest.raises(TypeError):
            recorda.inspection_view(record, **kwargs)
    with pytest.raises(TypeError):
        recorda.inspection_view(record, {})
    with pytest.raises(TypeError):
        recorda.inspection_view({})


@pytest.fixture
def configured():
    smonitor = pytest.importorskip("smonitor")
    from smonitor.handlers.memory import MemoryHandler

    handler = MemoryHandler()
    manager = smonitor.configure(
        handlers=[handler],
        profile="user",
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
    return smonitor, manager, handler


def test_resolving_uses_only_counts_and_keeps_application_policy(snapshot, configured, monkeypatch):
    import recorda.integrations.smonitor as adapter

    smonitor, manager, handler = configured
    record, _, _ = snapshot
    report = recorda.check_references(record)
    policy = manager.config
    hook, handlers = warnings.showwarning, tuple(logging.getLogger().handlers)
    original = adapter.resolve
    original_scope = adapter.diagnostic_scope
    calls, scopes = [], []

    def observe(**kwargs):
        calls.append(kwargs)
        return original(**kwargs)

    def observe_scope(**kwargs):
        scopes.append(kwargs)
        return original_scope(**kwargs)

    monkeypatch.setattr(adapter, "diagnostic_scope", observe_scope)
    monkeypatch.setattr(adapter, "resolve", observe)
    with smonitor.diagnostic_scope(safe_extra={"private": "producer secret"}):
        view = recorda.inspection_view(record, reference_report=report)
    (finding,) = view["findings"]
    assert finding["presentation"]["status"] == "resolved"
    assert "2" in finding["presentation"]["message"]
    assert "private" not in json.dumps(finding)
    assert calls == [{"code": finding["code"]}]
    assert scopes == [{"safe_extra": {"count": 2}}]
    assert handler.events == [] and manager.config is policy
    assert hook is warnings.showwarning and handlers == tuple(logging.getLogger().handlers)
    smonitor.configure(profile="dev", enabled=False, level="CRITICAL", handlers=[handler])
    policy = manager.config
    dev = recorda.inspection_view(record, reference_report=report)
    assert dev["findings"][0]["presentation"]["message"] != finding["presentation"]["message"]
    assert manager.config is policy and handler.events == []


@pytest.mark.parametrize(
    "result",
    [
        None,
        ("", None),
        ["message", "hint"],
        (Opaque(), None),
        ("x" * 4097, "hint"),
        ("generic fallback", "hint"),
    ],
)
def test_malformed_resolution_keeps_facts_and_fixed_fallback(
    snapshot, configured, monkeypatch, result
):
    import recorda.integrations.smonitor as adapter

    record, _, _ = snapshot
    monkeypatch.setattr(adapter, "resolve", lambda **kwargs: result)
    view = recorda.inspection_view(record, reference_report=recorda.check_references(record))
    (finding,) = view["findings"]
    assert finding["presentation"] == {
        "status": "unavailable",
        "reason": "invalid_resolution",
        "message": None,
        "hint": None,
    }
    assert finding["fallback"] == "references/unresolved: 2"
    assert view["execution"]["status"] == "succeeded"


@pytest.mark.parametrize("fault", ["registration", "resolution", "missing_code"])
def test_provider_faults_do_not_replace_facts(snapshot, configured, monkeypatch, fault):
    import recorda.integrations.smonitor as adapter

    class ProviderFailure(RuntimeError, Opaque):
        __str__ = Opaque.__str__
        __repr__ = Opaque.__repr__

    def broken(*args, **kwargs):
        raise ProviderFailure()

    if fault == "registration":
        monkeypatch.setattr(adapter, "register_provider", broken)
    elif fault == "resolution":
        monkeypatch.setattr(adapter, "resolve", broken)
    else:
        monkeypatch.setattr(configured[1], "get_codes", lambda: {})
    record, _, _ = snapshot
    view = recorda.inspection_view(record, reference_report=recorda.check_references(record))
    (finding,) = view["findings"]
    assert finding["count"] == 2
    assert (
        finding["presentation"]["reason"]
        == {
            "registration": "catalog_unavailable",
            "resolution": "rendering_failed",
            "missing_code": "invalid_resolution",
        }[fault]
    )


@pytest.mark.parametrize("fault", [KeyboardInterrupt, SystemExit, asyncio.CancelledError])
@pytest.mark.parametrize("stage", ["registration", "resolution"])
def test_interruptions_propagate(snapshot, configured, monkeypatch, fault, stage):
    import recorda.integrations.smonitor as adapter

    def broken(*args, **kwargs):
        raise fault()

    monkeypatch.setattr(
        adapter, "register_provider" if stage == "registration" else "resolve", broken
    )
    record, _, _ = snapshot
    with pytest.raises(fault):
        recorda.inspection_view(record, reference_report=recorda.check_references(record))


def _fresh(tmp_path, script):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(recorda.__file__).resolve().parents[1])
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def test_plain_import_and_inspection_remain_provider_free(tmp_path):
    output = _fresh(
        tmp_path,
        """
import importlib.abc, sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'smonitor','argdigest','depdigest','numpy','scipy','pyunitwizard'}:
            raise AssertionError('provider reached')
sys.meta_path.insert(0, Block())
import recorda
from pathlib import Path
Path('record.jsonl').write_text("""
        + repr(
            json.dumps(
                {
                    "schema": "recorda.journal/0.1",
                    "sequence": 0,
                    "event": "session_started",
                    "session_id": "s",
                    "name": "read-only",
                    "coverage": {"mode": "declared_boundaries", "known_gaps": []},
                }
            )
            + "\n"
        )
        + """)
assert recorda.inspect('record.jsonl').status == 'incomplete'
print('ok')
""",
    )
    assert output.strip() == "ok"


@pytest.mark.parametrize("missing", [False, True])
def test_fresh_view_neither_bootstraps_nor_imports_argdigest(tmp_path, missing):
    if not missing:
        pytest.importorskip("smonitor")
    output = _fresh(
        tmp_path,
        """
import importlib.abc, json, logging, sys, warnings
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        root = fullname.split('.')[0]
        if root in {'argdigest','depdigest','numpy','scipy','pyunitwizard'}:
            raise AssertionError('unneeded provider reached')
        if root == 'smonitor' and """
        + repr(missing)
        + """:
            raise ModuleNotFoundError('missing provider', name='smonitor')
sys.meta_path.insert(0, Block())
import recorda
hook, handlers = warnings.showwarning, tuple(logging.getLogger().handlers)
if not """
        + repr(missing)
        + """:
    import smonitor
    manager = smonitor.get_manager()
    config = manager.config
record = recorda.ScientificRecord('s','native','incomplete',
                                 {'mode':'declared_boundaries','known_gaps':[]},[],[])
view = recorda.inspection_view(record)
assert warnings.showwarning is hook and tuple(logging.getLogger().handlers) == handlers
if not """
        + repr(missing)
        + """:
    assert manager.config is config
print(json.dumps(view['findings'][0]['presentation']))
""",
    )
    presentation = json.loads(output)
    assert presentation["status"] == ("unavailable" if missing else "resolved")
    if missing:
        assert presentation["reason"] == "provider_missing"


def test_catalog_collision_is_atomic_and_preserves_application_policy(tmp_path):
    pytest.importorskip("smonitor")
    output = _fresh(
        tmp_path,
        """
import json
from pathlib import Path
import smonitor
from smonitor.handlers.memory import MemoryHandler
from smonitor.integrations import register_provider
import recorda
handler = MemoryHandler()
manager = smonitor.configure(handlers=[handler], profile='dev', enabled=True, level='DEBUG',
                            capture_logging=False, capture_warnings=False, capture_exceptions=False)
package = Path('conflict')
package.mkdir()
(package / '_smonitor.py').write_text("CODES = {'RECORDA-INSPECT-INCOMPLETE': {'user_message': 'conflict'}}\\n")
register_provider(package, provider='other')
policy, codes, providers = manager.config, manager.get_codes(), manager.get_providers()
record = recorda.ScientificRecord('s','native','incomplete',
                                 {'mode':'declared_boundaries','known_gaps':[]},[],[])
view = recorda.inspection_view(record)
assert view['findings'][0]['presentation']['reason'] == 'catalog_unavailable'
assert manager.config is policy and manager.get_codes() == codes
assert manager.get_providers() == providers and handler.events == []
print('ok')
""",
    )
    assert output.strip() == "ok"


@pytest.mark.parametrize("target", ["snapshot", "report"])
def test_total_text_budget_is_explicit_and_never_truncates(snapshot, target):
    record, _, _ = snapshot
    report = recorda.check_references(record)
    large = ["x" * 4096 for _ in range(257)]
    if target == "snapshot":
        record.operations[0]["outputs"]["large"] = large
    else:
        report["large"] = large
    with pytest.raises(ValueError, match="text budget"):
        recorda.inspection_view(record, reference_report=report)


@pytest.mark.parametrize(
    "mutation", ["status", "coverage", "operations", "parent", "duplicate", "capture", "exception"]
)
def test_malformed_native_shapes_are_rejected(snapshot, mutation):
    record, _, _ = snapshot
    if mutation == "status":
        record.status = "future_outcome"
    elif mutation == "coverage":
        record.coverage["known_gaps"] = "wrong"
    elif mutation == "operations":
        record.operations = {}
    elif mutation == "parent":
        record.operations[0]["parent_id"] = ["opaque parent"]
    elif mutation == "duplicate":
        record.operations.append(copy.deepcopy(record.operations[0]))
    elif mutation == "capture":
        record.operations[0]["capture"] = {"inputs": "future_policy"}
    else:
        record.operations[0]["exception"] = "private text"
    with pytest.raises(ValueError):
        recorda.inspection_view(record)


def test_report_coverage_equality_requires_exact_json_types(snapshot):
    record, _, _ = snapshot
    record.coverage["future_count"] = 1
    report = recorda.check_references(record)
    report["coverage"]["future_count"] = True
    with pytest.raises(ValueError):
        recorda.inspection_view(record, reference_report=report)


def test_distinct_references_include_all_four_fields(snapshot):
    record, _, _ = snapshot
    record.operations[0]["inputs"]["second"]["revision"] = "r2"
    report = recorda.check_references(record)
    view = recorda.inspection_view(record, reference_report=report)
    (finding,) = view["findings"]
    assert finding["count"] == 2 and finding["distinct_references"] == 2


@pytest.mark.parametrize("profile", ["user", "dev", "qa", "agent"])
def test_application_audience_resolves_without_events(snapshot, configured, profile):
    smonitor, manager, handler = configured
    smonitor.configure(profile=profile)
    policy = manager.config
    record, _, _ = snapshot
    (finding,) = recorda.inspection_view(record, reference_report=recorda.check_references(record))[
        "findings"
    ]
    assert finding["presentation"]["status"] == "resolved"
    assert manager.config is policy and handler.events == []
