"""Installed provider checks retain ownership and byte checks across Conda layouts."""

import hashlib
import json
from types import SimpleNamespace

import pytest

from devtools import verify_support_environment as checker


@pytest.fixture(params=("installed", "noarch"))
def closure(tmp_path, monkeypatch, request):
    prefix = tmp_path / "environment"
    purelib = prefix / "lib/python3.14/site-packages"
    records = prefix / "conda-meta"
    records.mkdir(parents=True)
    modules = {}
    for name, (version, build, sha) in checker.ARTIFACTS.items():
        paths = []
        files = []
        for relative in (f"{name}/__init__.py", f"{name}/implementation.py"):
            path = purelib / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"# published provider\n")
            installed = path.relative_to(prefix).as_posix()
            files.append(installed)
            paths.append(
                {
                    "_path": f"site-packages/{relative}"
                    if request.param == "noarch"
                    else installed,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        filename = f"{name}-{version}-{build}.tar.bz2"
        record = {
            "fn": filename,
            "sha256": sha,
            "url": f"https://conda.anaconda.org/uibcdf/noarch/{filename}",
            "noarch": "python",
            "files": files,
            "paths_data": {"paths": paths},
        }
        (records / f"{name}-{version}-{build}.json").write_text(json.dumps(record))
        modules[name] = SimpleNamespace(__file__=str(purelib / name / "__init__.py"))
    monkeypatch.setattr(checker.sys, "prefix", str(prefix))
    monkeypatch.setattr(checker.sysconfig, "get_path", lambda key: str(purelib))
    monkeypatch.setattr(checker.importlib, "import_module", modules.__getitem__)
    monkeypatch.setattr(
        checker, "distribution", lambda name: SimpleNamespace(version=checker.ARTIFACTS[name][0])
    )
    return SimpleNamespace(prefix=prefix, purelib=purelib, modules=modules, records=records)


def edit_record(closure, change):
    path = next(closure.records.glob("smonitor-*.json"))
    record = json.loads(path.read_text())
    change(record)
    path.write_text(json.dumps(record))


@pytest.mark.parametrize("feature", ("smonitor", "argdigest"))
def test_published_provider_bytes_in_both_conda_layouts(closure, feature, capsys):
    checker.verify(feature)
    evidence = json.loads(capsys.readouterr().out)
    assert evidence["feature"] == feature
    assert {name: value["python_files"] for name, value in evidence["providers"].items()} == {
        name: 2 for name in checker.ARTIFACTS
    }


def test_modified_non_entrypoint_python_file_is_rejected(closure):
    (closure.purelib / "smonitor/implementation.py").write_bytes(b"# modified\n")
    with pytest.raises(AssertionError, match="implementation.py"):
        checker.verify("argdigest")


def test_installed_prefix_hash_is_used_after_relocation(closure):
    path = closure.purelib / "smonitor/implementation.py"
    path.write_bytes(b"# relocated provider\n")
    edit_record(
        closure,
        lambda record: record["paths_data"]["paths"][1].update(
            sha256_in_prefix=hashlib.sha256(path.read_bytes()).hexdigest()
        ),
    )
    checker.verify("argdigest")


@pytest.mark.parametrize("inside", (False, True))
def test_import_shadowing_is_rejected(closure, inside):
    path = (closure.prefix if inside else closure.prefix.parent) / "shadow/smonitor/__init__.py"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"# shadow\n")
    closure.modules["smonitor"].__file__ = str(path)
    with pytest.raises(AssertionError, match="smonitor"):
        checker.verify("argdigest")


def test_missing_installation_ownership_is_rejected(closure):
    edit_record(closure, lambda record: record["files"].pop())
    with pytest.raises(AssertionError, match="managed installation file"):
        checker.verify("argdigest")


def test_symlink_to_external_python_file_is_rejected(closure):
    external = closure.prefix.parent / "external.py"
    external.write_bytes(b"# published provider\n")
    path = closure.purelib / "smonitor/implementation.py"
    path.unlink()
    path.symlink_to(external)
    with pytest.raises(AssertionError, match="outside environment"):
        checker.verify("argdigest")


@pytest.mark.parametrize("field", ("fn", "sha256", "url"))
def test_changed_published_artifact_identity_is_rejected(closure, field):
    edit_record(closure, lambda record: record.update({field: "other-provider"}))
    with pytest.raises(AssertionError, match="smonitor"):
        checker.verify("argdigest")


def test_duplicate_mapped_path_is_rejected(closure):
    edit_record(
        closure,
        lambda record: record["paths_data"]["paths"].append(
            {**record["paths_data"]["paths"][0], "sha256": "other-bytes"}
        ),
    )
    with pytest.raises(AssertionError, match="duplicate managed path"):
        checker.verify("argdigest")


def test_parent_path_traversal_is_rejected(closure):
    edit_record(
        closure,
        lambda record: record["paths_data"]["paths"][1].update(
            _path="site-packages/../../external.py"
        ),
    )
    with pytest.raises(AssertionError, match="external.py"):
        checker.verify("argdigest")
