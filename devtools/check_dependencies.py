"""Read-only preflight of required runtime metadata, Conda routes and CI sources."""

import json
import re
import subprocess
import tomllib
from pathlib import Path

import yaml
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version


def bounds(specifiers):
    lower, upper = None, None
    for spec in specifiers:
        op, text = spec.operator, spec.version
        if op == "==" and text.endswith(".*"):
            parts = list(map(int, text[:-2].split(".")))
            next_parts = [*parts[:-1], parts[-1] + 1]
            candidates = [
                (">=", Version(text[:-2])),
                ("<", Version(".".join(map(str, next_parts)))),
            ]
        elif op in {">=", ">", "<=", "<", "=="}:
            candidates = [(op, Version(text))]
        else:
            raise ValueError(f"unsupported preflight constraint: {spec}")
        for operator, version in candidates:
            if operator in {">=", ">", "=="}:
                candidate = (version, operator != ">")
                if (
                    lower is None
                    or candidate[0] > lower[0]
                    or (candidate[0] == lower[0] and not candidate[1])
                ):
                    lower = candidate
            if operator in {"<=", "<", "=="}:
                candidate = (version, operator != "<")
                if (
                    upper is None
                    or candidate[0] < upper[0]
                    or (candidate[0] == upper[0] and not candidate[1])
                ):
                    upper = candidate
    if (
        lower
        and upper
        and (lower[0] > upper[0] or (lower[0] == upper[0] and not (lower[1] and upper[1])))
    ):
        raise ValueError("empty runtime constraint")
    return lower, upper


def contained(candidate, required):
    lo, hi = bounds(candidate)
    rlo, rhi = bounds(required)
    return not (
        rlo
        and (lo is None or lo[0] < rlo[0] or (lo[0] == rlo[0] and lo[1] and not rlo[1]))
        or rhi
        and (hi is None or hi[0] > rhi[0] or (hi[0] == rhi[0] and hi[1] and not rhi[1]))
    )


def conda_requirement(text):
    match = re.fullmatch(r"([A-Za-z0-9_-]+)\s*(.*)", text)
    if not match:
        raise ValueError(f"invalid Conda dependency: {text}")
    name, constraint = match.groups()
    if constraint.startswith("=") and not constraint.startswith("=="):
        version = constraint[1:].split("=", 1)[0]
        if len(version.split(".")) < 3:
            version += ".*"
        constraint = "==" + version
    return Requirement(name + constraint.replace(" ", ""))


def check_source_candidate(name, version, commit, required):
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError(f"{name}: sibling source needs a full commit SHA")
    requirement = required.get(canonicalize_name(name))
    if requirement is None or not requirement.specifier.contains(version):
        raise ValueError(f"{name}: source version {version} violates {requirement}")


def audit(root):
    root = Path(root)
    project = tomllib.loads((root / "pyproject.toml").read_text())["project"]
    required = {canonicalize_name(r.name): r for r in map(Requirement, project["dependencies"])}
    required["python"] = Requirement("python" + project["requires-python"])
    inventory = json.loads((root / "devtools/dependency_routes.json").read_text())
    discovered_envs = {
        str(p.relative_to(root)) for p in (root / "devtools/conda-envs").glob("*.yaml")
    }
    discovered_recipes = {
        str(p.relative_to(root)) for p in (root / "conda-recipe").rglob("meta.yaml")
    }
    if discovered_envs != set(inventory["environments"]) or discovered_recipes != set(
        inventory["recipes"]
    ):
        raise ValueError("unclassified or missing Conda runtime route")
    for kind, paths in (
        ("recipes", inventory["recipes"]),
        ("environments", inventory["environments"]),
    ):
        for path in paths:
            data = yaml.safe_load((root / path).read_text())
            entries = data["requirements"]["run"] if kind == "recipes" else data["dependencies"]
            supplied = {
                canonicalize_name(r.name): r
                for r in map(conda_requirement, filter(lambda e: isinstance(e, str), entries))
            }
            for name, requirement in required.items():
                candidate = supplied.get(name)
                if candidate is None or not contained(candidate.specifier, requirement.specifier):
                    raise ValueError(f"{path}: {name} has {candidate}, requires {requirement}")
            if kind == "recipes" and (
                data["package"]["name"] != project["name"]
                or str(data["package"]["version"]) != project["version"]
            ):
                raise ValueError(f"{path}: recipe package identity differs from pyproject")
    sources = {entry["repository"]: entry for entry in inventory["sibling_sources"]}
    observed_sources = set()
    for workflow in (root / ".github/workflows").glob("*.yml"):
        jobs = yaml.safe_load(workflow.read_text()).get("jobs", {})
        for job in jobs.values():
            steps = job.get("steps", [])
            environments = [
                s.get("with", {}).get("environment-file")
                for s in steps
                if s.get("uses", "").startswith("mamba-org/setup-micromamba@")
            ]
            if any(p not in inventory["environments"] for p in environments):
                raise ValueError(f"{workflow.name}: unclassified CI environment")
            installs = any(
                re.search(r"pip install[^\n]*\s\.\s*(?:$|\n)", s.get("run", "")) for s in steps
            )
            if installs and not environments:
                raise ValueError(f"{workflow.name}: required Conda closure is not provisioned")
            for step in steps:
                if not step.get("uses", "").startswith("actions/checkout@"):
                    continue
                options = step.get("with", {})
                repository = options.get("repository")
                if repository is None or repository in inventory["non_runtime_checkouts"]:
                    continue
                entry = sources.get(repository)
                if entry is None or options.get("ref") != entry["commit"]:
                    raise ValueError(f"{repository}: unclassified or changed sibling source")
                source = root / options["path"]
                actual = subprocess.check_output(
                    ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
                ).strip()
                source_project = tomllib.loads((source / "pyproject.toml").read_text())["project"]
                if actual != entry["commit"]:
                    raise ValueError(f"{repository}: checked-out source identity differs")
                check_source_candidate(
                    source_project["name"], source_project["version"], actual, required
                )
                observed_sources.add(repository)
    if observed_sources != set(sources):
        raise ValueError("declared sibling source has no maintained CI installation route")
    return {
        "recipes": len(inventory["recipes"]),
        "environments": len(inventory["environments"]),
        "sibling_sources": len(sources),
    }


if __name__ == "__main__":
    print(json.dumps(audit(Path(__file__).resolve().parents[1]), sort_keys=True))
