"""Latest public selection is explicit, reproducible and distinct from qualification."""

import copy
import hashlib
import io
import json
import sys

import pytest
from packaging.version import InvalidVersion

from devtools import latest_support as latest


@pytest.fixture
def repodata():
    records = {}
    for name in latest.ARTIFACTS:
        for version in ("0.9.0", "0.99.0", "1.0.0rc1", "1.0.0.dev1", "1.0.0+local"):
            filename = f"{name}-{version}-py_0.tar.bz2"
            records[filename] = {
                "name": name,
                "version": version,
                "build": "py_0",
                "build_number": 0,
                "sha256": "a" * 64,
                "subdir": "noarch",
            }
    return {"packages": records}


@pytest.fixture
def manifest(repodata):
    providers = latest.select_providers(repodata)
    return {
        "schema": latest.SCHEMA,
        "channel": latest.CHANNEL,
        "repodata_sha256": "b" * 64,
        "providers": providers,
        "archives": {item["file"]: item for item in providers.values()},
    }


def test_latest_stable_uses_numeric_version_order_and_ignores_prerelease_local(repodata):
    selected = latest.select_providers(repodata)
    assert all(item["version"] == "0.99.0" for item in selected.values())


def test_latest_build_supports_both_conda_archive_formats(repodata):
    record = copy.deepcopy(repodata["packages"]["smonitor-0.99.0-py_0.tar.bz2"])
    record.update(build="py_2", build_number=2, timestamp=1)
    repodata["packages.conda"] = {"smonitor-0.99.0-py_2.conda": record}
    assert latest.select_providers(repodata)["smonitor"]["file"] == "smonitor-0.99.0-py_2.conda"


def test_equal_build_selection_is_deterministic(repodata):
    record = copy.deepcopy(repodata["packages"]["smonitor-0.99.0-py_0.tar.bz2"])
    record["timestamp"] = 2
    repodata["packages.conda"] = {"smonitor-0.99.0-py_0.conda": record}
    assert latest.select_providers(repodata)["smonitor"]["file"].endswith(".conda")


def test_no_stable_provider_does_not_fall_back_to_a_prerelease(repodata):
    repodata["packages"] = {
        name: item
        for name, item in repodata["packages"].items()
        if item["name"] != "argdigest" or "rc" in item["version"]
    }
    with pytest.raises(AssertionError, match="no public stable provider: argdigest"):
        latest.select_providers(repodata)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("version", "0.99.0\nspecs=other"),
        ("build", "py_0 other"),
        ("sha256", "unknown"),
        ("subdir", "linux-64"),
    ],
)
def test_invalid_public_coordinate_is_rejected(repodata, field, value):
    repodata["packages"]["smonitor-0.99.0-py_0.tar.bz2"][field] = value
    with pytest.raises((AssertionError, InvalidVersion)):
        latest.select_providers(repodata)


def test_index_filename_cannot_escape_the_canonical_channel(repodata):
    record = repodata["packages"].pop("smonitor-0.99.0-py_0.tar.bz2")
    repodata["packages"]["../smonitor-0.99.0-py_0.tar.bz2"] = record
    with pytest.raises(AssertionError, match="filename"):
        latest.select_providers(repodata)


@pytest.mark.parametrize("field", ("schema", "channel", "repodata_sha256"))
def test_manifest_source_and_index_identity_are_required(manifest, field):
    manifest[field] = "changed"
    with pytest.raises(AssertionError):
        latest.validate_manifest(manifest)


def test_manifest_cannot_redirect_an_archive_to_another_host(manifest):
    manifest["providers"]["smonitor"]["url"] = "https://example.invalid/other"
    with pytest.raises(AssertionError, match="coordinate"):
        latest.validate_manifest(manifest)


def test_manifest_provider_set_is_closed(manifest):
    manifest["providers"].pop("depdigest")
    with pytest.raises(AssertionError, match="provider set"):
        latest.validate_manifest(manifest)


def test_selection_hashes_the_actual_public_index(repodata, monkeypatch):
    raw = json.dumps(repodata).encode()
    calls = []

    def request(url, timeout):
        calls.append((url, timeout))
        return io.BytesIO(raw)

    monkeypatch.setattr(latest.urllib.request, "urlopen", request)
    result = latest.select()
    assert calls == [(latest.CHANNEL + "/repodata.json", 30)]
    assert result["repodata_sha256"] == hashlib.sha256(raw).hexdigest()
    assert latest.validate_manifest(result) == latest.select_providers(repodata)


def test_cli_exports_exact_selected_specs_without_mutating_fixed_cohort(
    manifest, monkeypatch, tmp_path
):
    original = dict(latest.ARTIFACTS)
    output, github = tmp_path / "selection.json", tmp_path / "github-output"
    monkeypatch.setattr(latest, "select", lambda: manifest)
    monkeypatch.setattr(
        sys,
        "argv",
        ["latest_support", "select", "--output", str(output), "--github-output", str(github)],
    )
    latest.main()
    assert json.loads(output.read_text()) == manifest
    assert github.read_text().strip() == "specs=" + " ".join(
        f"{name}=0.99.0=py_0" for name in manifest["providers"]
    )
    assert latest.ARTIFACTS == original


def test_cli_verification_uses_only_the_selected_manifest(manifest, monkeypatch, tmp_path):
    output = tmp_path / "selection.json"
    output.write_text(json.dumps(manifest))
    calls = []
    monkeypatch.setattr(latest, "installed_identities", lambda data, prefix: data["providers"])
    monkeypatch.setattr(latest, "verify", lambda feature, **kwargs: calls.append((feature, kwargs)))
    monkeypatch.setattr(sys, "argv", ["latest_support", "verify", "--manifest", str(output)])
    latest.main()
    assert calls == [("argdigest", {"identities": manifest["providers"]})]


def test_actual_archive_format_must_be_in_the_selected_index_snapshot(manifest, tmp_path):
    records = tmp_path / "conda-meta"
    records.mkdir()
    for name, item in manifest["providers"].items():
        (records / f"{name}-record.json").write_text(json.dumps({"fn": item["file"]}))
    assert latest.installed_identities(manifest, tmp_path) == manifest["providers"]
    alternate = dict(manifest["providers"]["smonitor"])
    alternate.update(
        file="smonitor-0.99.0-py_0.conda",
        url=latest.CHANNEL + "/smonitor-0.99.0-py_0.conda",
        sha256="c" * 64,
    )
    (records / "smonitor-record.json").write_text(json.dumps({"fn": alternate["file"]}))
    with pytest.raises(AssertionError, match="unselected archive"):
        latest.installed_identities(manifest, tmp_path)
    manifest["archives"][alternate["file"]] = alternate
    assert latest.installed_identities(manifest, tmp_path)["smonitor"] == alternate


def test_equivalent_archive_cannot_smuggle_a_different_version(manifest):
    alternate = dict(manifest["providers"]["smonitor"])
    alternate.update(version="0.9.0", file="smonitor-0.9.0-py_0.conda")
    manifest["archives"][alternate["file"]] = alternate
    with pytest.raises(AssertionError, match="selected version/build"):
        latest.validate_manifest(manifest)
