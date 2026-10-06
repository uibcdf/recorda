"""Inspect declared references against an explicitly supplied local file index."""

import copy
import hashlib
import os
import re
import stat
from dataclasses import asdict
from pathlib import Path

from .capture import Reference
from .reader import ScientificRecord

_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")
_OMISSION_REASONS = {
    "sensitive_name",
    "unsupported_type",
    "caller_omitted",
    "oversized_value",
    "nonfinite_value",
    "reference_adapter_failed",
    "invalid_reference_adapter_result",
    "capture_policy",
}
_DEFAULT_MAX_BYTES = 64 * 1024 * 1024


def _index_root(value):
    if not isinstance(value, (str, os.PathLike)):
        raise TypeError("local root must be a string or path-like object")
    return value


def _index_entries(value):
    if type(value) is not dict:
        raise TypeError("local entries must map Reference objects to relative file paths")
    for reference, location in value.items():
        if type(reference) is not Reference:
            raise TypeError("local index keys must be Reference objects")
        if not isinstance(location, (str, Path)):
            raise TypeError("local locations must be relative file paths")
    return value


def _digest_algorithm(value):
    if value is not None and (type(value) is not str or value != "sha256"):
        raise ValueError("only an explicitly declared sha256 algorithm is supported")
    return value


def _resolver(value):
    if value is not None and type(value) is not LocalFileResolver:
        raise TypeError("resolver must be a LocalFileResolver")
    return value


def _max_bytes(value):
    if type(value) is not int or value < 1:
        raise ValueError("max_bytes must be a positive integer")
    return value


def _inspected_record(value):
    if type(value) is not ScientificRecord:
        raise TypeError("record must be an inspected ScientificRecord")
    return value


def _reference(value):
    if type(value) is Reference:
        value = {key: getattr(value, key) for key in ("owner", "identifier", "revision", "digest")}
    if type(value) is not dict or any(type(key) is not str for key in value):
        return None
    if set(value) - {"kind", "owner", "identifier", "revision", "digest"}:
        return None
    if "kind" in value and value["kind"] != "reference":
        return None
    data = {key: value.get(key) for key in ("owner", "identifier", "revision", "digest")}
    for key, field in data.items():
        if field is None and key in {"revision", "digest"}:
            continue
        if type(field) is not str or not field or len(field) > 1024:
            return None
    return Reference(**data)


class LocalFileResolver:
    """Caller-owned exact-reference index; never derive paths from identifiers."""

    def __init__(self, root, entries, *, digest_algorithm=None):
        from ._arguments import reference_index_options

        root, entries, digest_algorithm = reference_index_options(
            digest_algorithm=digest_algorithm, entries=entries, root=root
        )
        # Core guards and confinement remain mandatory after provider validation.
        self._digest_algorithm = _digest_algorithm(digest_algorithm)
        entries = _index_entries(entries)
        root = _index_root(root)
        self._entries = {}
        for reference, location in entries.items():
            location = Path(location)
            if location.is_absolute() or ".." in location.parts:
                raise ValueError("local locations must stay inside their root")
            self._entries[reference] = location
        self._root = Path(root).resolve()

    @property
    def references(self):
        return tuple(self._entries)

    def path_for(self, reference):
        reference = _reference(reference)
        if reference is None or reference not in self._entries:
            return None
        path = (self._root / self._entries[reference]).resolve()
        if not path.is_relative_to(self._root):
            raise ValueError("local location resolves outside its root")
        return path


def _options(resolver, max_bytes):
    _resolver(resolver)
    _max_bytes(max_bytes)


def check_reference(reference, *, resolver=None, max_bytes=_DEFAULT_MAX_BYTES):
    """Return local availability/byte-check facts, without exposing paths or file contents."""
    from ._arguments import reference_check_options

    resolver, max_bytes = reference_check_options(resolver, max_bytes=max_bytes)
    return _check_reference(reference, resolver=resolver, max_bytes=max_bytes)


def _check_reference(reference, *, resolver, max_bytes):
    """Guarded native byte checker; record-level caching does not repeat digestion."""
    _options(resolver, max_bytes)
    reference = _reference(reference)
    result = {
        "reference": None if reference is None else asdict(reference),
        "status": "invalid_reference",
        "bytes_checked": 0,
        "digest_algorithm": None if resolver is None else resolver._digest_algorithm,
    }
    if reference is None:
        return result

    def outcome(status):
        result["status"] = status
        return result

    if resolver is None:
        return outcome("unresolved")
    try:
        path = resolver.path_for(reference)
        if path is None:
            return outcome("unresolved")
        flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode):
                return outcome("not_a_file")
            with os.fdopen(fd, "rb", closefd=False) as stream:
                if reference.digest is None:
                    return outcome("available_unverified")
                if resolver._digest_algorithm != "sha256" or not _SHA256.fullmatch(
                    reference.digest
                ):
                    return outcome("unsupported_digest")
                if before.st_size > max_bytes:
                    return outcome("too_large")
                digest = hashlib.sha256()
                while block := stream.read(min(65536, max_bytes - result["bytes_checked"] + 1)):
                    result["bytes_checked"] += len(block)
                    if result["bytes_checked"] > max_bytes:
                        return outcome("too_large")
                    digest.update(block)
                after = os.fstat(stream.fileno())
                if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                    after.st_size,
                    after.st_mtime_ns,
                    after.st_ctime_ns,
                ):
                    return outcome("unstable")
                return outcome(
                    "matched" if digest.hexdigest() == reference.digest.lower() else "mismatched"
                )
        finally:
            os.close(fd)
    except FileNotFoundError:
        return outcome("missing")
    except ValueError:
        return outcome("outside_root")
    except (OSError, RuntimeError):
        return outcome("unreadable")


def check_references(record, *, resolver=None, max_bytes=_DEFAULT_MAX_BYTES):
    """Check declared top-level reference occurrences, preserving omission and lifecycle scope."""
    from ._arguments import record_check_options

    resolver, max_bytes, record = record_check_options(resolver, max_bytes=max_bytes, record=record)
    _options(resolver, max_bytes)
    _inspected_record(record)
    references, omissions, incomplete, cache = [], [], [], {}
    for operation in record.operations:
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
                if "exception" not in operation:
                    continue
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
                    if reference is None:
                        checked = _check_reference(value, resolver=resolver, max_bytes=max_bytes)
                    else:
                        if reference not in cache:
                            cache[reference] = _check_reference(
                                reference, resolver=resolver, max_bytes=max_bytes
                            )
                        checked = cache[reference]
                    references.append({**row, **copy.deepcopy(checked)})
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
    return {
        "session_id": record.session_id,
        "session_status": record.status,
        "coverage": copy.deepcopy(record.coverage),
        "references": references,
        "omissions": omissions,
        "incomplete_operations": incomplete,
        "scope": "declared_references_and_local_file_bytes",
    }
