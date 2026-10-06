"""Read journals independently of the target library; preserve incomplete work."""

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ScientificRecord:
    """An inspection snapshot, not an integrity or replayability certification."""

    session_id: str
    name: str
    status: str
    coverage: dict
    operations: list[dict]
    problems: list[str]


def inspect(path):
    """Inspect one experimental JSONL journal, retaining a detectable truncated tail."""
    lines = Path(path).read_bytes().splitlines(keepends=True)
    problems = []
    events = []
    for index, line in enumerate(lines):
        if not line.endswith(b"\n") and index == len(lines) - 1:
            problems.append("truncated_tail")
            break
        try:
            event = json.loads(line)
        except (ValueError, UnicodeDecodeError) as error:
            raise ValueError("invalid journal event") from error
        if (
            type(event) is not dict
            or event.get("schema") != "recorda.journal/0.1"
            or event.get("sequence") != index
        ):
            raise ValueError("unsupported schema or invalid event sequence")
        events.append(event)
    if not events or events[0].get("event") != "session_started":
        raise ValueError("journal has no durable session start")
    start = events[0]
    operations = {}
    terminal = None
    coverage = dict(start["coverage"])
    for event in events[1:]:
        if event.get("session_id") != start["session_id"] or terminal is not None:
            raise ValueError("event outside its session")
        kind = event.get("event")
        operation_id = event.get("operation_id")
        if kind == "operation_started":
            if operation_id in operations:
                raise ValueError("duplicate operation start")
            parent = event["parent_id"]
            if parent is not None and (
                parent not in operations or operations[parent]["status"] != "incomplete"
            ):
                raise ValueError("operation has no active parent")
            operations[operation_id] = {
                "id": operation_id,
                "name": event["name"],
                "profile": event.get("profile"),
                "parent_id": parent,
                "inputs": event["inputs"],
                "parameters": event["parameters"],
                "implementation": event["implementation"],
                "start": event["time"],
                "status": "incomplete",
                "outputs": {},
            }
            if "capture" in event:
                operations[operation_id]["capture"] = event["capture"]
        elif kind in {"operation_output", "operation_finished"}:
            if operation_id not in operations or operations[operation_id]["status"] != "incomplete":
                raise ValueError("event has no active operation")
            operation = operations[operation_id]
            if kind == "operation_output":
                operation["outputs"][event["name"]] = event["value"]
            else:
                if event["status"] not in {"succeeded", "failed"}:
                    raise ValueError("invalid operation outcome")
                operation["status"] = event["status"]
                operation["end"] = event["time"]
                if "exception" in event:
                    operation["exception"] = event["exception"]
        elif kind == "session_finished":
            if event["status"] not in {"succeeded", "failed", "incomplete"}:
                raise ValueError("invalid session outcome")
            terminal = event["status"]
            if "excluded_boundaries" in event:
                coverage["excluded_boundaries"] = event["excluded_boundaries"]
        else:
            raise ValueError("unknown journal event")
    status = terminal or "incomplete"
    if problems or any(operation["status"] == "incomplete" for operation in operations.values()):
        status = "incomplete"
    elif (
        any(operation["status"] == "failed" for operation in operations.values())
        and status == "succeeded"
    ):
        status = "failed"
    return ScientificRecord(
        start["session_id"],
        start["name"],
        status,
        coverage,
        list(operations.values()),
        problems,
    )
