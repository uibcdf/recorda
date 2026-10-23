"""Exercise published test-output contracts in fresh processes, including failure."""

import os
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest
from pytest_receptor import read_artifact


@pytest.mark.parametrize("profile", ["llm", "ci"])
@pytest.mark.parametrize("fails", [False, True])
@pytest.mark.parametrize("stats", [False, True])
def test_published_receptor_preserves_exit_counts_and_complete_artifact(
    tmp_path, profile, fails, stats
):
    module = tmp_path / "test_receiving_case.py"
    module.write_text(
        "import pytest\n\n"
        "def test_ok():\n    assert 2 + 2 == 4\n\n"
        "@pytest.mark.skip(reason='declared receiving exclusion')\n"
        "def test_skip():\n    pass\n"
        + (
            "\ndef test_failure():\n    assert False, 'controlled receiving failure'\n"
            if fails
            else ""
        )
    )
    config = tmp_path / "pytest.ini"
    config.write_text("[pytest]\n")
    events = tmp_path / "events.jsonl"
    junit = tmp_path / "junit.xml"
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "pytest_receptor.plugin",
        "-c",
        str(config),
        f"--receptor={profile}",
        f"--receptor-events={events}",
        f"--junitxml={junit}",
        str(module),
    ]
    if stats:
        command.append("--receptor-stats")
    environment = os.environ.copy()
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    environment["PYTHONWARNINGS"] = "always::ResourceWarning"
    environment.pop("PYTEST_ADDOPTS", None)
    result = subprocess.run(
        command, cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=60
    )
    assert result.returncode == int(fails), result.stdout + result.stderr
    assert ("FAIL exit=1" if fails else "PASS exit=0") in result.stdout
    assert "ResourceWarning" not in result.stdout + result.stderr
    assert "I/O operation on closed file" not in result.stdout + result.stderr
    artifact = read_artifact(events)
    assert artifact.complete and artifact.integrity_valid
    assert artifact.final.data["exitstatus"] == result.returncode
    counts = artifact.final.data["counts"]
    assert counts["passed"] == 1 and counts["skipped"] == 1
    assert counts.get("failed", 0) == int(fails)
    suites = ET.parse(junit).findall(".//testsuite")
    assert sum(int(s.attrib["tests"]) for s in suites) == 2 + int(fails)
    assert sum(int(s.attrib["failures"]) for s in suites) == int(fails)
    assert sum(int(s.attrib["skipped"]) for s in suites) == 1
