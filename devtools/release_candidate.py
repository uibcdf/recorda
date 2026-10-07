"""Inspect, install-check and independently observe a digest-bound Conda candidate."""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import subprocess
import sys
import sysconfig
import tarfile
import tempfile
import tomllib
import xml.etree.ElementTree as ET
from email.parser import BytesParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

from devtools.check_dependencies import conda_requirement, contained

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspect_archive(path, root, source_sha):
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    version = project["version"]
    assert re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version), "noncanonical public version"
    assert path.name == f"recorda-{version}-py_0.tar.bz2", "unexpected artifact coordinate"
    with tarfile.open(path) as archive:
        index = json.load(archive.extractfile("info/index.json"))
        assert (index["name"], index["version"], index["build"], index["noarch"]) == (
            "recorda",
            version,
            "py_0",
            "python",
        ), "artifact identity differs from candidate"
        dependencies = {r.name: r for r in map(conda_requirement, index["depends"])}
        required = [Requirement(text) for text in project["dependencies"]]
        required.append(Requirement("python" + project["requires-python"]))
        for requirement in required:
            assert requirement.name in dependencies and contained(
                dependencies[requirement.name].specifier, requirement.specifier
            ), f"artifact dependency: {requirement}"
        metadata = BytesParser().parsebytes(
            archive.extractfile(f"site-packages/recorda-{version}.dist-info/METADATA").read()
        )
        assert metadata["Name"] == "recorda" and metadata["Version"] == version
        assert SpecifierSet(metadata["Requires-Python"]) == SpecifierSet(project["requires-python"])
        wheel_requirements = [Requirement(text) for text in metadata.get_all("Requires-Dist", [])]
        assert {str(r) for r in wheel_requirements if r.marker is None} == set(
            map(str, map(Requirement, project["dependencies"]))
        ), "installed metadata dependencies differ"
        sources = {
            path.relative_to(root / "src").as_posix(): sha256(path)
            for path in sorted((root / "src/recorda").rglob("*.py"))
        }
        delivered = {
            name.removeprefix("site-packages/")
            for name in archive.getnames()
            if name.startswith("site-packages/recorda/") and name.endswith(".py")
        }
        assert delivered == set(sources), "missing or extra runtime Python files"
        for relative, expected in sources.items():
            assert (
                hashlib.sha256(archive.extractfile("site-packages/" + relative).read()).hexdigest()
                == expected
            ), f"stale runtime bytes: {relative}"
    return {
        "source_sha": source_sha,
        "version": version,
        "coordinate": f"uibcdf/recorda/{version}/noarch/{path.name}",
        "filename": path.name,
        "sha256": sha256(path),
        "runtime_sha256": sources,
        "conda_dependencies": index["depends"],
        "python_requires": project["requires-python"],
        "required_metadata": project["dependencies"],
        "resources": "No generated or vendored runtime resources; all Python files checked.",
    }


def verify_file(path, manifest, source_sha):
    assert manifest["source_sha"] == source_sha, "different candidate source"
    assert path.name == manifest["filename"] and sha256(path) == manifest["sha256"], (
        "different candidate artifact bytes"
    )


def coverage_paths(path, manifest):
    """Map measured installed files to their byte-identical repository sources."""
    document = ET.parse(path)
    for item in document.findall(".//class"):
        measured = Path(item.attrib["filename"])
        if measured.is_absolute():
            relative = (
                measured.resolve().relative_to(Path(sysconfig.get_path("purelib"))).as_posix()
            )
        else:
            relative = measured.as_posix().removeprefix("src/")
        if not relative.startswith("recorda/"):
            relative = "recorda/" + relative
        assert relative in manifest["runtime_sha256"], "coverage outside candidate runtime"
        assert sha256(ROOT / "src" / relative) == manifest["runtime_sha256"][relative]
        if measured.is_absolute():
            assert sha256(measured) == manifest["runtime_sha256"][relative]
        item.set("filename", "src/" + relative)
    for source in document.findall("sources/source"):
        source.text = str(ROOT)
    document.write(path, encoding="utf-8", xml_declaration=True)
    return {"runtime_sources": "src/recorda", "measured_counts": "unchanged"}


def registry_file(document, manifest, *, published):
    entries = [] if document is None else document["distributions"]
    assert isinstance(entries, list), "incomplete registry inventory"
    basename = "noarch/" + manifest["filename"]
    matches = [entry for entry in entries if entry["basename"] == basename]
    assert len(matches) <= 1, "duplicate registry coordinate"
    if not published:
        assert not matches, "immutable coordinate occupied under some label"
        return None
    assert matches, "public coordinate unavailable"
    entry = matches[0]
    assert entry["sha256"] == manifest["sha256"] and "main" in entry["labels"], (
        "public digest/label differs from candidate"
    )
    return {key: entry[key] for key in ("basename", "sha256", "labels")}


def observe_registry(manifest, *, published):
    version = manifest["version"]
    url = f"https://api.anaconda.org/release/uibcdf/recorda/{version}"
    try:
        with urlopen(url, timeout=20) as response:
            document = json.load(response)
    except HTTPError as error:
        if error.code != 404:
            raise
        document = None
    return {"url": url, "file": registry_file(document, manifest, published=published)}


def installed(manifest):
    import recorda

    prefix = Path(sys.prefix).resolve()
    package = Path(recorda.__file__).resolve().parent
    assert package.is_relative_to(prefix), "source import instead of installed candidate"
    assert recorda.__version__ == importlib.metadata.version("recorda") == manifest["version"]
    for relative, expected in manifest["runtime_sha256"].items():
        assert sha256(package.parent / relative) == expected, relative
    records = list((prefix / "conda-meta").glob("recorda-*.json"))
    assert len(records) == 1, "expected one installed Conda candidate"
    record = json.loads(records[0].read_text())
    assert record["fn"] == manifest["filename"] and record["sha256"] == manifest["sha256"]
    if platform.system() == "Darwin":
        assert platform.machine() == "arm64", "macOS candidate requires arm64"
    with tempfile.TemporaryDirectory() as destination:
        journal = Path(destination) / "smoke.jsonl"

        @recorda.record("release.double")
        def double(value):
            return 2 * value

        session = recorda.start("release", path=journal)
        assert double(3) == 6
        assert session.stop().status == "succeeded"
        result = subprocess.check_output([sys.executable, "-m", "recorda", str(journal)], text=True)
        assert json.loads(result)["operations"][0]["outputs"]["return"] == 6
    return {
        "source_sha": manifest["source_sha"],
        "sha256": manifest["sha256"],
        "version": recorda.__version__,
        "python": sys.version,
        "prefix": str(prefix),
        "system": platform.system(),
        "machine": platform.machine(),
        "runtime_files": len(manifest["runtime_sha256"]),
        "recording_and_cli": "passed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("inspect", "verify", "installed", "unoccupied", "public", "coverage")
    )
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--source-sha")
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "inspect":
        assert subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True) == ""
        source = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        result = inspect_archive(args.artifact, ROOT, source)
    else:
        manifest = json.loads(args.manifest.read_text())
        if args.command == "verify":
            verify_file(args.artifact, manifest, args.source_sha)
            result = manifest
        elif args.command == "installed":
            result = installed(manifest)
        elif args.command == "coverage":
            result = coverage_paths(args.coverage, manifest)
        else:
            result = observe_registry(manifest, published=args.command == "public")
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"command": args.command, "result": "passed", "output": str(args.output)}))


if __name__ == "__main__":
    main()
