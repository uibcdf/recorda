"""Local byte checks do not certify scientific identities, execution or replay."""

import hashlib
import json
import os
from dataclasses import replace

import pytest

import recorda


def retained(tmp_path, payload=b"native bytes"):
    path = tmp_path / "native.bin"
    path.write_bytes(payload)
    reference = recorda.Reference(
        owner="native",
        identifier="object1",
        revision="r1",
        digest=hashlib.sha256(payload).hexdigest(),
    )
    return reference, path


def test_reinspection_detects_changes_and_loss_without_changing_reference(tmp_path):
    reference, path = retained(tmp_path)
    entries = {reference: path.name}
    files = recorda.LocalFileResolver(tmp_path, entries, digest_algorithm="sha256")
    entries.clear()
    assert files.references == (reference,)
    assert recorda.check_reference(reference, resolver=files)["status"] == "matched"
    path.write_bytes(b"altered")
    assert recorda.check_reference(reference, resolver=files)["status"] == "mismatched"
    path.unlink()
    assert recorda.check_reference(reference, resolver=files)["status"] == "missing"
    assert reference.identifier == "object1"  # Owner identity is independent of SHA256.


@pytest.mark.parametrize("field", ["owner", "identifier", "revision", "digest"])
def test_lookup_requires_the_complete_declared_reference(tmp_path, field):
    reference, path = retained(tmp_path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    changed = replace(reference, **{field: "different"})
    assert recorda.check_reference(changed, resolver=files)["status"] == "unresolved"


@pytest.mark.parametrize(
    "digest,status", [(None, "available_unverified"), ("opaque-digest", "unsupported_digest")]
)
def test_availability_without_supported_digest_is_not_verified(tmp_path, digest, status):
    reference, path = retained(tmp_path)
    reference = replace(reference, identifier="sha256:" + reference.digest, digest=digest)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    checked = recorda.check_reference(reference, resolver=files)
    assert checked["status"] == status and checked["bytes_checked"] == 0


def test_hash_reads_are_bounded_and_do_not_return_paths_or_contents(tmp_path):
    reference, path = retained(tmp_path, b"private contents" * 100)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    checked = recorda.check_reference(reference, resolver=files, max_bytes=10)
    assert checked["status"] == "too_large" and checked["bytes_checked"] == 0
    assert "private" not in json.dumps(checked) and str(tmp_path) not in json.dumps(checked)


@pytest.mark.parametrize("location", ["../outside.bin", "/absolute/private.bin"])
def test_relative_index_rejects_paths_outside_root(tmp_path, location):
    reference, _ = retained(tmp_path)
    with pytest.raises(ValueError, match="inside their root"):
        recorda.LocalFileResolver(tmp_path, {reference: location})


def test_late_symlink_outside_root_is_not_read(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    reference, path = retained(root)
    files = recorda.LocalFileResolver(root, {reference: path.name}, digest_algorithm="sha256")
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"private outside contents")
    path.unlink()
    path.symlink_to(outside)
    checked = recorda.check_reference(reference, resolver=files)
    assert checked["status"] == "outside_root" and checked["bytes_checked"] == 0


@pytest.mark.parametrize("kind", ["directory", "fifo"])
def test_nonregular_files_are_not_read_or_waited_on(tmp_path, kind):
    reference = recorda.Reference(owner="native", identifier="nonregular", digest="0" * 64)
    path = tmp_path / "nonregular"
    if kind == "directory":
        path.mkdir()
    else:
        if not hasattr(os, "mkfifo"):
            pytest.skip("FIFO fixture requires os.mkfifo")
        os.mkfifo(path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    assert recorda.check_reference(reference, resolver=files)["status"] == "not_a_file"


def test_io_error_text_is_not_reported(tmp_path, monkeypatch):
    reference, path = retained(tmp_path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")

    def forbidden(*args, **kwargs):
        raise PermissionError("private filesystem detail")

    monkeypatch.setattr(os, "open", forbidden)
    checked = recorda.check_reference(reference, resolver=files)
    assert checked["status"] == "unreadable"
    assert "private" not in json.dumps(checked)


def test_mutation_during_read_is_not_certified_as_matching(tmp_path, monkeypatch):
    reference, path = retained(tmp_path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    original = os.fstat
    calls = []

    def stat_after_mutation(fd):
        calls.append(fd)
        if len(calls) == 2:
            path.write_bytes(b"changed during checking")
        return original(fd)

    monkeypatch.setattr(os, "fstat", stat_after_mutation)
    assert recorda.check_reference(reference, resolver=files)["status"] == "unstable"


def test_invalid_reference_does_not_inspect_opaque_values_or_unknown_fields():
    class Opaque:
        def __repr__(self):
            raise AssertionError("repr called")

        def __deepcopy__(self, memo):
            raise AssertionError("deepcopy called")

    for reference in [
        Opaque(),
        {"owner": Opaque(), "identifier": "native"},
        {"owner": "native", "identifier": "object", "api_key": "private"},
    ]:
        assert recorda.check_reference(reference) == {
            "reference": None,
            "status": "invalid_reference",
            "bytes_checked": 0,
            "digest_algorithm": None,
        }


def test_record_reports_references_omissions_and_incomplete_without_mutation(tmp_path, monkeypatch):
    reference, path = retained(tmp_path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="sha256")
    native = ValueError("private scientific error")
    handle = recorda.start(
        "record",
        path=tmp_path / "journal.jsonl",
        reference_adapters={ValueError: lambda error: reference},
    )
    with pytest.raises(ValueError):
        with handle.operation(
            "failed",
            inputs={"source": reference, "api_key": "private"},
            parameters={"model": reference},
        ) as operation:
            operation.output("result", reference)
            raise native
    record = handle.stop()
    import recorda.references as checks

    original, calls = checks.check_reference, []

    def counted(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(checks, "check_reference", counted)
    report = recorda.check_references(record, resolver=files)
    assert len(calls) == 1 and len(report["references"]) == 4
    assert {row["group"] for row in report["references"]} == {
        "inputs",
        "parameters",
        "outputs",
        "exception",
    }
    assert {row["status"] for row in report["references"]} == {"matched"}
    assert report["session_status"] == "failed" and record.status == "failed"
    assert report["omissions"][0]["reason"] == "sensitive_name"
    report["coverage"]["known_gaps"].append("changed report")
    report["references"][0]["reference"]["owner"] = "changed report"
    assert record.coverage["known_gaps"] == []
    assert report["references"][1]["reference"]["owner"] == "native"
    path.unlink()
    assert {
        row["status"] for row in recorda.check_references(record, resolver=files)["references"]
    } == {"missing"}
    assert record.status == "failed"


def test_policy_omissions_and_unclosed_operations_remain_distinct(tmp_path):
    handle = recorda.start(
        "minimal",
        path=tmp_path / "minimal.jsonl",
        capture_policy=recorda.CapturePolicy(inputs=False, outputs=False),
    )
    with handle.operation("completed"):
        pass
    report = recorda.check_references(handle.stop())
    assert report["references"] == [] and report["incomplete_operations"] == []
    assert {row["group"] for row in report["omissions"]} == {"inputs", "outputs"}
    reference, _ = retained(tmp_path)
    handle = recorda.start("unclosed", path=tmp_path / "unclosed.jsonl")
    operation = handle.operation("pending", inputs={"source": reference})
    operation.__enter__()
    try:
        report = recorda.check_references(handle.record)
        assert report["session_status"] == "incomplete"
        assert report["incomplete_operations"] == [operation.id]
        assert report["references"][0]["status"] == "unresolved"
    finally:
        operation.__exit__(None, None, None)
        handle.stop()


def test_historical_failure_without_reference_is_not_recorded(tmp_path):
    handle = recorda.start("historical", path=tmp_path / "historical.jsonl")
    with pytest.raises(ValueError):
        with handle.operation("failure"):
            raise ValueError("private")
    handle.stop()
    events = [json.loads(line) for line in handle.path.read_text().splitlines()]
    next(event for event in events if "exception" in event)["exception"].pop("reference")
    handle.path.write_text("".join(json.dumps(event) + "\n" for event in events))
    report = recorda.check_references(recorda.inspect(handle.path))
    assert report["omissions"] == [
        {
            "operation_id": report["omissions"][0]["operation_id"],
            "operation_name": "failure",
            "operation_status": "failed",
            "group": "exception",
            "field": "reference",
            "reason": "not_recorded",
        }
    ]


def test_configuration_errors_are_rejected(tmp_path):
    with pytest.raises(TypeError):
        recorda.LocalFileResolver(tmp_path, {"not a reference": "native.bin"})
    with pytest.raises(TypeError):
        recorda.check_reference({}, resolver=lambda value: tmp_path)
    with pytest.raises(ValueError):
        recorda.check_reference({}, max_bytes=True)
    with pytest.raises(TypeError):
        recorda.check_references(tmp_path)


def test_digest_algorithm_is_declared_by_the_index_not_guessed_from_length(tmp_path):
    reference, path = retained(tmp_path)
    files = recorda.LocalFileResolver(tmp_path, {reference: path.name})
    checked = recorda.check_reference(reference, resolver=files)
    assert checked["status"] == "unsupported_digest" and checked["bytes_checked"] == 0
    assert checked["digest_algorithm"] is None
    with pytest.raises(ValueError):
        recorda.LocalFileResolver(tmp_path, {reference: path.name}, digest_algorithm="unknown")


def test_symlink_loop_reports_an_unreadable_location_without_path_text(tmp_path):
    reference = recorda.Reference(owner="native", identifier="loop", digest="0" * 64)
    location = tmp_path / "private-loop.bin"
    location.symlink_to(location.name)
    files = recorda.LocalFileResolver(
        tmp_path, {reference: location.name}, digest_algorithm="sha256"
    )
    checked = recorda.check_reference(reference, resolver=files)
    assert checked["status"] == "unreadable" and checked["bytes_checked"] == 0
    assert "private" not in json.dumps(checked)
