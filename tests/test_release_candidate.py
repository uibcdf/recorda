"""A release must reject stale/missing payloads and occupied or altered coordinates."""

import io
import json
import tarfile
import xml.etree.ElementTree as ET

import pytest

from devtools import release_candidate
from devtools.release_candidate import coverage_paths, inspect_archive, registry_file, verify_file


@pytest.fixture
def candidate(tmp_path):
    (tmp_path / "src/recorda").mkdir(parents=True)
    (tmp_path / "src/recorda/__init__.py").write_text('__version__ = "0.3.0"\n')
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname="recorda"\nversion="0.3.0"\nrequires-python=">=3.11,<3.15"\n'
        'dependencies=["argdigest>=0.15.0,<0.16", "smonitor>=0.19.0,<0.20"]\n'
    )
    entries = {
        "info/index.json": json.dumps(
            {
                "name": "recorda",
                "version": "0.3.0",
                "build": "py_0",
                "noarch": "python",
                "depends": [
                    "python >=3.11,<3.15",
                    "argdigest >=0.15.0,<0.16",
                    "smonitor >=0.19.0,<0.20",
                ],
            }
        ).encode(),
        "site-packages/recorda/__init__.py": (tmp_path / "src/recorda/__init__.py").read_bytes(),
        "site-packages/recorda-0.3.0.dist-info/METADATA": (
            "Name: recorda\nVersion: 0.3.0\nRequires-Python: >=3.11,<3.15\n"
            "Requires-Dist: argdigest<0.16,>=0.15.0\nRequires-Dist: smonitor<0.20,>=0.19.0\n"
        ).encode(),
    }

    def build():
        path = tmp_path / "recorda-0.3.0-py_0.tar.bz2"
        with tarfile.open(path, "w:bz2") as archive:
            for name, data in entries.items():
                item = tarfile.TarInfo(name)
                item.size = len(data)
                archive.addfile(item, io.BytesIO(data))
        return path

    return tmp_path, entries, build


def test_exact_candidate_archive_and_digest_are_qualified(candidate):
    root, _, build = candidate
    path = build()
    manifest = inspect_archive(path, root, "a" * 40)
    verify_file(path, manifest, "a" * 40)
    assert manifest["coordinate"] == "uibcdf/recorda/0.3.0/noarch/recorda-0.3.0-py_0.tar.bz2"
    assert len(manifest["runtime_sha256"]) == 1


@pytest.mark.parametrize("defect", ("missing", "stale", "extra", "version", "dependencies"))
def test_archive_defects_block_release(candidate, defect):
    root, entries, build = candidate
    if defect == "missing":
        del entries["site-packages/recorda/__init__.py"]
    elif defect == "stale":
        entries["site-packages/recorda/__init__.py"] = b'__version__ = "0.2.0"\n'
    elif defect == "extra":
        entries["site-packages/recorda/unreviewed.py"] = b"# unexpected runtime\n"
    elif defect == "version":
        entries["site-packages/recorda-0.3.0.dist-info/METADATA"] = entries[
            "site-packages/recorda-0.3.0.dist-info/METADATA"
        ].replace(b"Version: 0.3.0", b"Version: 0.2.0")
    else:
        index = json.loads(entries["info/index.json"])
        index["depends"] = [text for text in index["depends"] if not text.startswith("smonitor")]
        entries["info/index.json"] = json.dumps(index).encode()
    with pytest.raises(AssertionError):
        inspect_archive(build(), root, "a" * 40)


def test_changed_file_or_source_cannot_reuse_candidate_receipt(candidate):
    root, _, build = candidate
    path = build()
    manifest = inspect_archive(path, root, "a" * 40)
    with pytest.raises(AssertionError, match="candidate source"):
        verify_file(path, manifest, "b" * 40)
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(AssertionError, match="artifact bytes"):
        verify_file(path, manifest, "a" * 40)


@pytest.mark.parametrize("label", ("main", "staging", "withdrawn"))
def test_occupied_coordinate_blocks_upload_under_every_label(candidate, label):
    root, _, build = candidate
    manifest = inspect_archive(build(), root, "a" * 40)
    document = {
        "distributions": [
            {
                "basename": "noarch/" + manifest["filename"],
                "sha256": manifest["sha256"],
                "labels": [label],
            }
        ]
    }
    with pytest.raises(AssertionError, match="occupied"):
        registry_file(document, manifest, published=False)


def test_independent_public_poststate_rejects_changed_digest(candidate):
    root, _, build = candidate
    manifest = inspect_archive(build(), root, "a" * 40)
    assert registry_file(None, manifest, published=False) is None
    document = {
        "distributions": [
            {
                "basename": "noarch/" + manifest["filename"],
                "sha256": "other-bytes",
                "labels": ["main"],
            }
        ]
    }
    with pytest.raises(AssertionError, match="digest/label"):
        registry_file(document, manifest, published=True)
    document["distributions"][0]["sha256"] = manifest["sha256"]
    assert registry_file(document, manifest, published=True)["sha256"] == manifest["sha256"]


@pytest.mark.parametrize("absolute", (False, True))
def test_installed_coverage_mapping_preserves_measured_counts(candidate, monkeypatch, absolute):
    root, _, build = candidate
    manifest = inspect_archive(build(), root, "a" * 40)
    monkeypatch.setattr(release_candidate, "ROOT", root)
    monkeypatch.setattr(release_candidate.sysconfig, "get_path", lambda _: str(root / "src"))
    filename = str(root / "src/recorda/__init__.py") if absolute else "__init__.py"
    report = root / "coverage.xml"
    report.write_text(
        '<coverage lines-covered="7" branches-covered="3"><sources><source>/installed</source>'
        f'</sources><packages><package><classes><class filename="{filename}">'
        '<lines><line number="1" hits="2" branch="true" condition-coverage="50% (1/2)"/>'
        "</lines></class></classes></package></packages></coverage>"
    )
    original = ET.parse(report)
    coverage_paths(report, manifest)
    mapped = ET.parse(report)
    assert mapped.find(".//class").attrib["filename"] == "src/recorda/__init__.py"
    assert mapped.find("sources/source").text == str(root)
    assert mapped.getroot().attrib == original.getroot().attrib
    assert mapped.find(".//line").attrib == original.find(".//line").attrib


def test_coverage_rejects_files_outside_exact_runtime(candidate, monkeypatch):
    root, _, build = candidate
    manifest = inspect_archive(build(), root, "a" * 40)
    monkeypatch.setattr(release_candidate, "ROOT", root)
    report = root / "coverage.xml"
    report.write_text('<coverage><class filename="foreign.py"/></coverage>')
    with pytest.raises(AssertionError, match="outside candidate runtime"):
        coverage_paths(report, manifest)
