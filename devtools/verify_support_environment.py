"""Check required-feature metadata and exact published Conda provider provenance."""

import argparse
import hashlib
import importlib
import json
import sys
import sysconfig
import tomllib
from importlib.metadata import distribution
from pathlib import Path

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

ARTIFACTS = {
    "smonitor": (
        "0.21.0",
        "py_2",
        "62b6cbae37f7fa06374af87923792f00253020955d000294b1a7d37eb9d04e56",
    ),
    "argdigest": (
        "0.16.0",
        "py_0",
        "e82d82680d79ae3d5df9917b1662d2855ed8485128943b72ddec87a5769a467d",
    ),
    "depdigest": (
        "0.15.1",
        "py_0",
        "2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850",
    ),
}


def managed_paths(record, prefix):
    """Map noarch archive paths while checking actual installation ownership."""
    purelib = Path(sysconfig.get_path("purelib")).resolve()
    installed = set(record["files"])
    managed = {}
    for item in record["paths_data"]["paths"]:
        relative = Path(item["_path"])
        assert not relative.is_absolute() and ".." not in relative.parts, item["_path"]
        if relative.parts[0] == "site-packages":
            assert record.get("noarch") == "python", "expected Python noarch metadata"
            path = purelib.joinpath(*relative.parts[1:])
        else:
            path = prefix / relative
        assert path.is_relative_to(prefix) and path.resolve().is_relative_to(prefix), (
            f"outside environment: {path}"
        )
        assert path.relative_to(prefix).as_posix() in installed, (
            f"not a managed installation file: {path}"
        )
        assert path not in managed, f"duplicate managed path: {path}"
        managed[path] = item
    return managed


def verify(feature):
    root = Path(__file__).resolve().parents[1]
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    assert SpecifierSet(project["requires-python"]).contains(
        ".".join(map(str, sys.version_info[:3]))
    )
    for text in project["dependencies"] + project["optional-dependencies"][feature]:
        requirement = Requirement(text)
        assert requirement.specifier.contains(distribution(requirement.name).version), text

    prefix = Path(sys.prefix).resolve()
    names = tuple(ARTIFACTS)
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
        managed = managed_paths(record, prefix)
        assert module_path in managed, f"{name}: source/provider shadowing"
        checked = 0
        for path, item in managed.items():
            if path.suffix == ".py" and path.is_relative_to(module_path.parent):
                assert path.resolve().is_relative_to(module_path.parent), (
                    f"{name}: Python file outside provider: {path}"
                )
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
