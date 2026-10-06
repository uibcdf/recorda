"""Bounded, read-only facts with explicitly requested diagnostic presentation."""

import math
from collections import Counter
from dataclasses import asdict

from ._inspection_catalog import CODES, reference_code
from .reader import ScientificRecord
from .references import _OMISSION_REASONS, _reference

_OUTCOMES = {"succeeded", "failed", "incomplete"}
_REFERENCE_STATES = {
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
}
_REPORT_KEYS = {
    "session_id",
    "session_status",
    "coverage",
    "references",
    "omissions",
    "incomplete_operations",
    "scope",
}


def _copy_json(value, budget, depth=0):
    """Never dispatch to arbitrary copying, iteration, repr or conversion hooks."""
    budget[0] -= 1
    if budget[0] < 0 or depth > 24:
        raise ValueError("inspection input exceeds the structural budget")
    kind = type(value)
    if value is None or kind is bool:
        return value
    if kind is str:
        if len(value) > 4096:
            raise ValueError("inspection strings exceed the supported bound")
        budget[1] -= len(value)
        if budget[1] < 0:
            raise ValueError("inspection input exceeds the text budget")
        return value
    if kind is int and value.bit_length() <= 256:
        return value
    if kind is float and math.isfinite(value):
        return value
    if kind is list and len(value) <= 10000:
        return [_copy_json(item, budget, depth + 1) for item in value]
    if kind is dict and len(value) <= 10000:
        result = {}
        for key, item in value.items():
            if type(key) is not str:
                raise TypeError("inspection mapping keys must be native strings")
            result[_copy_json(key, budget, depth + 1)] = _copy_json(item, budget, depth + 1)
        return result
    raise TypeError("inspection inputs must contain bounded native JSON values")


def _require(condition):
    if not condition:
        raise ValueError("invalid inspection snapshot or reference report")


def _label(value):
    return type(value) is str and bool(value)


def _same(left, right):
    """JSON equality must not equate booleans, integers and floats."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(_same(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(
            _same(a, b) for a, b in zip(left, right, strict=True)
        )
    return left == right


def _snapshot(record):
    if type(record) is not ScientificRecord:
        raise TypeError("record must be an inspected ScientificRecord")
    data = _copy_json(
        {
            key: getattr(record, key)
            for key in ("session_id", "name", "status", "coverage", "operations", "problems")
        },
        [100000, 1048576],
    )
    _require(_label(data["session_id"]) and _label(data["name"]))
    _require(type(data["status"]) is str and data["status"] in _OUTCOMES)
    coverage = data["coverage"]
    _require(type(coverage) is dict and coverage.get("mode") == "declared_boundaries")
    gaps = coverage.get("known_gaps")
    _require(type(gaps) is list and all(type(gap) is str for gap in gaps))
    excluded = coverage.get("excluded_boundaries")
    if excluded is not None:
        _require(type(excluded) is dict and set(excluded) == {"by_profile", "other_calls"})
        _require(type(excluded["other_calls"]) is int and excluded["other_calls"] >= 0)
        _require(type(excluded["by_profile"]) is list)
        for row in excluded["by_profile"]:
            _require(type(row) is dict and set(row) == {"profile", "calls"})
            _require(row["profile"] is None or type(row["profile"]) is str)
            _require(type(row["calls"]) is int and row["calls"] >= 0)
    _require(type(data["problems"]) is list)
    _require(all(_label(problem) for problem in data["problems"]))
    _require(type(data["operations"]) is list)
    seen = set()
    for operation in data["operations"]:
        _require(type(operation) is dict)
        _require(_label(operation.get("id")) and _label(operation.get("name")))
        _require(operation["id"] not in seen)
        parent = operation.get("parent_id")
        _require(parent is None or (_label(parent) and parent in seen))
        seen.add(operation["id"])
        _require(type(operation.get("status")) is str and operation["status"] in _OUTCOMES)
        for group in ("inputs", "parameters", "outputs"):
            _require(type(operation.get(group)) is dict)
        capture = operation.get("capture", {})
        _require(type(capture) is dict)
        _require(set(capture) <= {"inputs", "parameters", "outputs", "exception_references"})
        _require(
            all(
                type(state) is str and state in {"enabled", "omitted_by_policy"}
                for state in capture.values()
            )
        )
        if "exception" in operation:
            _require(type(operation["exception"]) is dict)
    _require(
        not any(op["status"] == "incomplete" for op in data["operations"])
        or data["status"] == "incomplete"
    )
    _require(not data["problems"] or data["status"] == "incomplete")
    _require(
        data["status"] != "succeeded"
        or not any(op["status"] == "failed" for op in data["operations"])
    )
    return data


def _declarations(data):
    """Mirror the declared top-level scope, without resolving or reading bytes."""
    references, omissions, incomplete = [], [], []
    for operation in data["operations"]:
        if operation["status"] == "incomplete":
            incomplete.append(operation["id"])
        for group in ("inputs", "parameters", "outputs", "exception"):
            context = {
                "operation_id": operation["id"],
                "operation_name": operation["name"],
                "operation_status": operation["status"],
                "group": group,
            }
            if group == "exception" and "exception" not in operation:
                continue
            policy_group = "exception_references" if group == "exception" else group
            if operation.get("capture", {}).get(policy_group) == "omitted_by_policy":
                omissions.append({**context, "field": None, "reason": "capture_policy"})
                continue
            if group == "exception":
                if "reference" not in operation["exception"]:
                    omissions.append({**context, "field": "reference", "reason": "not_recorded"})
                    continue
                values = {"reference": operation["exception"]["reference"]}
            else:
                values = operation[group]
            for field, value in values.items():
                row = {**context, "field": field}
                if type(value) is dict and value.get("kind") == "reference":
                    reference = _reference(value)
                    references.append(
                        {**row, "reference": None if reference is None else asdict(reference)}
                    )
                elif type(value) is dict and value.get("kind") == "omitted":
                    reason = value.get("reason")
                    omissions.append(
                        {
                            **row,
                            "reason": reason
                            if type(reason) is str and reason in _OMISSION_REASONS
                            else "unspecified",
                        }
                    )
    return references, omissions, incomplete


def _identity(reference):
    return (
        None
        if reference is None
        else tuple(reference[key] for key in ("owner", "identifier", "revision", "digest"))
    )


def _report(report, data, declarations, omissions, incomplete):
    if report is None:
        return None
    copied = _copy_json(report, [100000, 1048576])
    _require(type(copied) is dict and set(copied) == _REPORT_KEYS)
    _require(copied["session_id"] == data["session_id"])
    _require(copied["session_status"] == data["status"])
    _require(_same(copied["coverage"], data["coverage"]))
    _require(copied["scope"] == "declared_references_and_local_file_bytes")
    _require(
        _same(copied["omissions"], omissions) and _same(copied["incomplete_operations"], incomplete)
    )
    rows = copied["references"]
    _require(type(rows) is list and len(rows) == len(declarations))
    seen = {}
    for row, expected in zip(rows, declarations, strict=True):
        _require(
            type(row) is dict
            and set(row) == set(expected) | {"status", "bytes_checked", "digest_algorithm"}
        )
        _require(all(_same(row[key], value) for key, value in expected.items()))
        _require(_label(row["status"]))
        _require(type(row["bytes_checked"]) is int and 0 <= row["bytes_checked"] < 2**64)
        _require(row["digest_algorithm"] is None or row["digest_algorithm"] == "sha256")
        identity = _identity(row["reference"])
        if identity is None:
            _require(row["status"] == "invalid_reference")
        else:
            _require(row["status"] != "invalid_reference")
            observation = (row["status"], row["bytes_checked"], row["digest_algorithm"])
            _require(identity not in seen or seen[identity] == observation)
            seen[identity] = observation
    return copied


def _finding(domain, state, code, indices, *, count=None, distinct=None):
    return {
        "domain": domain,
        "state": state,
        "code": code,
        "level": CODES[code]["level"],
        "count": len(indices) if count is None else count,
        "distinct_references": distinct,
        "source_indices": indices,
        "fallback": f"{domain}/{state}: {len(indices) if count is None else count}",
    }


def _present(findings):
    if not findings:
        return
    reason = None
    renderer = None
    try:
        from .integrations.smonitor import SMonitorInspectionPresentation

        renderer = SMonitorInspectionPresentation()
    except ModuleNotFoundError as error:
        reason = "provider_missing" if error.name == "smonitor" else "catalog_unavailable"
    except Exception:
        reason = "catalog_unavailable"
    for finding in findings:
        presentation = {"status": "unavailable", "reason": reason, "message": None, "hint": None}
        if renderer is not None:
            try:
                result = renderer(finding["code"], count=finding["count"])
                if result is None:
                    presentation["reason"] = "invalid_resolution"
                else:
                    presentation.update(
                        status="resolved", reason=None, message=result[0], hint=result[1]
                    )
            except Exception:
                presentation["reason"] = "rendering_failed"
        finding["presentation"] = presentation


def inspection_view(record, *, reference_report=None):
    """Project an inspected snapshot and optional same-snapshot reference report.

    This experimental JSON-compatible view preserves a bounded copy of source
    facts. It neither checks bytes nor authenticates caller-supplied observations.
    Explicit presentation uses the application's existing SMonitor audience;
    ordinary provider faults leave state/count fallbacks beside the facts.
    """
    data = _snapshot(record)
    declarations, omissions, incomplete = _declarations(data)
    report = _report(reference_report, data, declarations, omissions, incomplete)
    findings = []
    if data["status"] == "incomplete":
        indices = [i for i, op in enumerate(data["operations"]) if op["status"] == "incomplete"]
        findings.append(_finding("operations", "incomplete", "RECORDA-INSPECT-INCOMPLETE", indices))
    for state in ("truncated_tail", "unclassified"):
        indices = [
            i
            for i, problem in enumerate(data["problems"])
            if (problem == "truncated_tail") == (state == "truncated_tail")
        ]
        if indices:
            code = (
                "RECORDA-INSPECT-JOURNAL-TAIL"
                if state == "truncated_tail"
                else "RECORDA-INSPECT-UNCLASSIFIED"
            )
            findings.append(_finding("problems", state, code, indices))
    rows = [] if report is None else report["references"]
    for state in sorted(_REFERENCE_STATES - {"matched"}) + ["unclassified"]:
        indices = [
            i
            for i, row in enumerate(rows)
            if (
                row["status"] == state
                if state != "unclassified"
                else row["status"] not in _REFERENCE_STATES
            )
        ]
        if indices:
            distinct = (
                None
                if any(rows[i]["reference"] is None for i in indices)
                else len({_identity(rows[i]["reference"]) for i in indices})
            )
            findings.append(
                _finding(
                    "references",
                    state,
                    "RECORDA-INSPECT-UNCLASSIFIED"
                    if state == "unclassified"
                    else reference_code(state),
                    indices,
                    distinct=distinct,
                )
            )
    _present(findings)
    excluded = data["coverage"].get("excluded_boundaries")
    return {
        "record": data,
        "reference_report": report,
        "execution": {
            "status": data["status"],
            "operations": len(data["operations"]),
            "by_status": dict(Counter(op["status"] for op in data["operations"])),
        },
        "references": {
            "check_state": "not_requested" if report is None else "provided",
            "declared_occurrences": len(declarations),
            "checked_occurrences": None if report is None else len(rows),
            "distinct_declared_references": len(
                {
                    _identity(row["reference"])
                    for row in declarations
                    if row["reference"] is not None
                }
            ),
            "by_status": dict(Counter(row["status"] for row in rows)),
        },
        "coverage": {
            "known_gap_count": len(data["coverage"]["known_gaps"]),
            "excluded_calls": None
            if excluded is None
            else excluded["other_calls"] + sum(row["calls"] for row in excluded["by_profile"]),
            "omissions": omissions,
            "omissions_by_reason": dict(Counter(row["reason"] for row in omissions)),
        },
        "findings": findings,
    }
