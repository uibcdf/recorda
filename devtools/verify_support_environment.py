"""Check optional-feature metadata and exact published Conda provider provenance."""

import argparse
import hashlib
import importlib
import json
import sys
import tomllib
from importlib.metadata import distribution
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

ARTIFACTS = {
    "smonitor": (
        "0.19.0",
        "py_1",
        "4b876b4993b1e2caeed40851402a931f3b245ed7c1916d9483d81bc90274e31c",
    ),
    "argdigest": (
        "0.15.0",
        "py_0",
        "b0f22038a8ad1c888dca10adedaca0fa14d2383a685a97c0602b7ca05f29d6a1",
    ),
    "depdigest": (
        "0.13.0",
        "py_0",
        "e011d725c8a831ae46cd6b8d114185d04248e32b4d6701c70f988d19cc69f67b",
    ),
}


def verify(feature):
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    assert not project["dependencies"], "this lane expects the provider-independent core"
    assert SpecifierSet(project["requires-python"]).contains(
        ".".join(map(str, sys.version_info[:3]))
    )
    for text in project["optional-dependencies"][feature]:
        requirement = Requirement(text)
        assert requirement.specifier.contains(distribution(requirement.name).version), text

    prefix = Path(sys.prefix).resolve()
    names = ("smonitor",) if feature == "smonitor" else tuple(ARTIFACTS)
    evidence = {}
    for name in names:
        version, build, sha = ARTIFACTS[name]
        records = list((prefix / "conda-meta").glob(f"{name}-*.json"))
        assert len(records) == 1, f"{name}: expected one Conda installation record"
        record = json.loads(records[0].read_text())
        filename = f"{name}-{version}-{build}.tar.bz2"
        assert record["fn"] == filename and record["sha256"] == sha, name
        assert record["url"] == f"https://conda.anaconda.org/uibcdf/noarch/{filename}", name
        assert distribution(name).version == version, name
        module = importlib.import_module(name)
        module_path = Path(module.__file__).resolve()
        assert module_path.is_relative_to(prefix), f"{name}: source/provider shadowing"
        managed = {item["_path"]: item for item in record["paths_data"]["paths"]}
        assert str(module_path.relative_to(prefix)) in managed, name
        checked = 0
        for item in managed.values():
            path = prefix / item["_path"]
            if path.suffix == ".py" and path.is_relative_to(module_path.parent):
                expected = item.get("sha256_in_prefix", item["sha256"])
                assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, str(path)
                checked += 1
        assert checked, name
        evidence[name] = {
            "version": version,
            "file": filename,
            "sha256": sha,
            "python_files": checked,
        }
    for name in ("numpy", "pint", "pyunitwizard", "pandas"):
        assert name not in sys.modules, f"unexpected scientific import: {name}"
    print(json.dumps({"feature": feature, "providers": evidence}, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature", choices=("smonitor", "argdigest"))
    verify(parser.parse_args().feature)
