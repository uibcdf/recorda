"""Release preparation must not expose credentials or reuse an old coordinate."""

import os
import re
import subprocess
import tomllib
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github/workflows"


def load(name):
    return yaml.load((WORKFLOWS / name).read_text(), Loader=yaml.BaseLoader)


def test_candidate_source_build_has_no_publication_secret():
    # candidate_sha selects repository code to execute; build/test needs no secret.
    text = (WORKFLOWS / "release_candidate.yml").read_text()
    assert "secrets." not in text


def test_presence_probe_is_manual_main_only_and_checks_no_repository_code():
    workflow = load("publication_readiness.yml")
    assert set(workflow["on"]) == {"workflow_dispatch"}
    job = workflow["jobs"]["presence"]
    assert job["if"] == "github.ref == 'refs/heads/main'"
    assert len(job["steps"]) == 1
    assert "uses" not in job["steps"][0]
    assert job["steps"][0]["env"] == {"MOLI_CONDA_TOKEN": "${{ secrets.ANACONDA_UIBCDF_TOKEN }}"}


@pytest.mark.parametrize("token", [None, "", "disposable-probe-value"])
def test_presence_probe_fails_closed_and_never_discloses_value(token):
    script = load("publication_readiness.yml")["jobs"]["presence"]["steps"][0]["run"]
    environment = {"PATH": os.defpath}
    if token is not None:
        environment["MOLI_CONDA_TOKEN"] = token
    result = subprocess.run(["bash", "-e", "-c", script], env=environment, capture_output=True)
    assert result.returncode == (0 if token else 1)
    assert b"disposable-probe-value" not in result.stdout + result.stderr
    assert (b"available (presence only" in result.stdout) == bool(token)


def test_candidate_and_publication_routes_use_the_current_package_coordinate():
    version = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"]
    filename = f"recorda-{version}-py_0.tar.bz2"
    for name in ("release_candidate.yml", "build_and_upload_conda_packages.yaml"):
        text = (WORKFLOWS / name).read_text()
        assert filename in text
        assert set(re.findall(r"recorda-(\d+\.\d+\.\d+)-py_0\.tar\.bz2", text)) == {version}
    publisher = (WORKFLOWS / "build_and_upload_conda_packages.yaml").read_text()
    assert f"'{version}^{{}}'" in publisher
    assert f"uibcdf/recorda/{version}/noarch/{filename}" in publisher
    assert f"recorda={version}=py_0" in publisher


def test_publisher_checks_canonical_presence_before_checkout_or_upload():
    text = (WORKFLOWS / "build_and_upload_conda_packages.yaml").read_text()
    assert "secrets.ANACONDA_TOKEN" not in text
    workflow = load("build_and_upload_conda_packages.yaml")
    assert set(workflow["on"]) == {"workflow_dispatch"}
    assert workflow["jobs"]["publish"]["if"] == "github.ref == 'refs/heads/main'"
    first = workflow["jobs"]["publish"]["steps"][0]
    assert first["env"] == {"MOLI_CONDA_TOKEN": "${{ secrets.ANACONDA_UIBCDF_TOKEN }}"}
    assert "uses" not in first
    assert "exit 1" in first["run"]
