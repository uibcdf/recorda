"""A release/build route must not weaken the public runtime contract."""

import json
import shutil
from pathlib import Path

import pytest
import yaml
from packaging.requirements import Requirement

from devtools.check_dependencies import audit, check_source_candidate

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def tree(tmp_path):
    inventory = json.loads((ROOT / "devtools/dependency_routes.json").read_text())
    files = [
        "pyproject.toml",
        "devtools/dependency_routes.json",
        ".github/workflows/tests.yml",
        *inventory["recipes"],
        *inventory["environments"],
    ]
    for file in files:
        destination = tmp_path / file
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / file, destination)
    return tmp_path


def test_committed_runtime_routes_match_metadata():
    assert audit(ROOT) == {"recipes": 1, "environments": 4, "sibling_sources": 0}


def test_missing_recipe_dependency_blocks_preflight(tree):
    path = tree / "conda-recipe/meta.yaml"
    data = yaml.safe_load(path.read_text())
    data["requirements"]["run"] = [
        text for text in data["requirements"]["run"] if not text.startswith("argdigest")
    ]
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="meta.yaml: argdigest"):
        audit(tree)


@pytest.mark.parametrize(
    "constraint", ["argdigest>=0.14,<0.16", "argdigest>=0.15", "argdigest=0.14.0=py_0"]
)
def test_stale_or_weaker_environment_constraint_blocks_preflight(tree, constraint):
    path = tree / "devtools/conda-envs/test_env.yaml"
    data = yaml.safe_load(path.read_text())
    data["dependencies"] = [
        constraint if str(item).startswith("argdigest") else item for item in data["dependencies"]
    ]
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="test_env.yaml: argdigest"):
        audit(tree)


def test_python_outside_public_bounds_is_rejected(tree):
    path = tree / "devtools/conda-envs/test_env.yaml"
    path.write_text(path.read_text().replace("python>=3.11,<3.15", "python>=3.10,<3.15"))
    with pytest.raises(ValueError, match="test_env.yaml: python"):
        audit(tree)


def test_new_environment_requires_inventory_review(tree):
    shutil.copyfile(
        tree / "devtools/conda-envs/test_env.yaml", tree / "devtools/conda-envs/new_env.yaml"
    )
    with pytest.raises(ValueError, match="unclassified"):
        audit(tree)


def test_pip_only_runtime_lane_is_rejected(tree):
    path = tree / ".github/workflows/tests.yml"
    data = yaml.safe_load(path.read_text())
    data["jobs"]["tests"]["steps"] = [{"run": "python -m pip install --no-deps ."}]
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="Conda closure is not provisioned"):
        audit(tree)


def test_new_sibling_source_requires_review(tree):
    path = tree / ".github/workflows/tests.yml"
    data = yaml.safe_load(path.read_text())
    data["jobs"]["tests"]["steps"].append(
        {
            "uses": "actions/checkout@v4",
            "with": {"repository": "uibcdf/argdigest", "ref": "main", "path": "provider"},
        }
    )
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError, match="unclassified or changed sibling source"):
        audit(tree)


def test_exact_source_commit_cannot_hide_version_below_runtime_floor():
    required = {"argdigest": Requirement("argdigest>=0.15,<0.16")}
    with pytest.raises(ValueError, match="source version 0.14.0"):
        check_source_candidate("argdigest", "0.14.0", "a" * 40, required)
    with pytest.raises(ValueError, match="full commit SHA"):
        check_source_candidate("argdigest", "0.15.0", "main", required)
