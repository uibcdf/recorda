"""Select public stable providers separately from the fixed qualification cohort."""

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from packaging.version import Version

from devtools.verify_support_environment import ARTIFACTS, verify

CHANNEL = "https://conda.anaconda.org/uibcdf/noarch"
SCHEMA = "recorda.latest-support@1"


def identity(name, filename, record):
    """Accept only a canonical public noarch coordinate, never arbitrary URLs/specs."""
    assert name in ARTIFACTS and record["name"] == name, "unexpected provider"
    version, build = record["version"], record["build"]
    assert all(re.fullmatch(r"[A-Za-z0-9_.+\-]+", text) for text in (version, build)), (
        "invalid provider version/build"
    )
    assert record.get("subdir", "noarch") == "noarch", "expected noarch provider"
    assert filename in {
        f"{name}-{version}-{build}.tar.bz2",
        f"{name}-{version}-{build}.conda",
    }, "invalid provider filename"
    assert re.fullmatch(r"[0-9a-f]{64}", record["sha256"]), "invalid provider digest"
    return {
        "name": name,
        "version": version,
        "build": build,
        "file": filename,
        "sha256": record["sha256"],
        "url": f"{CHANNEL}/{filename}",
    }


def select_providers(repodata):
    """Choose highest stable version, then build number/timestamp/filename."""
    candidates = {name: [] for name in ARTIFACTS}
    for table in ("packages", "packages.conda"):
        for filename, record in repodata.get(table, {}).items():
            name = record.get("name")
            if name not in candidates:
                continue
            version = Version(record["version"])
            if version.is_prerelease or version.is_devrelease or version.local is not None:
                continue
            item = identity(name, filename, record)
            key = (version, record["build_number"], record.get("timestamp", 0), filename)
            candidates[name].append((key, item))
    selected = {}
    for name, options in candidates.items():
        assert options, f"no public stable provider: {name}"
        selected[name] = max(options, key=lambda item: item[0])[1]
    return selected


def validate_manifest(manifest):
    assert manifest["schema"] == SCHEMA and manifest["channel"] == CHANNEL, "unexpected source"
    assert re.fullmatch(r"[0-9a-f]{64}", manifest["repodata_sha256"]), "invalid index digest"
    assert set(manifest["providers"]) == set(ARTIFACTS), "unexpected provider set"
    for name, item in manifest["providers"].items():
        assert identity(name, item["file"], item) == item, "changed provider coordinate"
        version = Version(item["version"])
        assert not (version.is_prerelease or version.is_devrelease or version.local), (
            "expected stable provider"
        )
        assert manifest["archives"][item["file"]] == item, "missing selected archive"
    for filename, item in manifest["archives"].items():
        name = item["name"]
        assert name in ARTIFACTS, "unexpected provider"
        selected = manifest["providers"][name]
        assert (item["version"], item["build"]) == (selected["version"], selected["build"]), (
            "archive differs from selected version/build"
        )
        assert identity(name, filename, item) == item, "changed archive coordinate"
    return manifest["providers"]


def installed_identities(manifest, prefix):
    """Check the actual archive format against the retained public index snapshot."""
    selected = validate_manifest(manifest)
    result = {}
    for name in selected:
        records = list((prefix / "conda-meta").glob(f"{name}-*.json"))
        assert len(records) == 1, f"{name}: expected one Conda installation record"
        filename = json.loads(records[0].read_text())["fn"]
        item = manifest["archives"].get(filename)
        assert item is not None and item["name"] == name, f"{name}: unselected archive"
        result[name] = item
    return result


def select():
    with urllib.request.urlopen(f"{CHANNEL}/repodata.json", timeout=30) as response:
        raw = response.read()
    data = json.loads(raw)
    providers = select_providers(data)
    archives = {}
    for table in ("packages", "packages.conda"):
        for filename, record in data.get(table, {}).items():
            selected = providers.get(record.get("name"))
            if selected and (record["version"], record["build"]) == (
                selected["version"],
                selected["build"],
            ):
                archives[filename] = identity(record["name"], filename, record)
    return {
        "schema": SCHEMA,
        "channel": CHANNEL,
        "selected_at": datetime.now(timezone.utc).isoformat(),
        "repodata_sha256": hashlib.sha256(raw).hexdigest(),
        "providers": providers,
        "archives": archives,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    selector = commands.add_parser("select")
    selector.add_argument("--output", type=Path, required=True)
    selector.add_argument("--github-output", type=Path)
    verifier = commands.add_parser("verify")
    verifier.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "select":
        manifest = select()
        providers = validate_manifest(manifest)
        args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        if args.github_output is not None:
            specs = " ".join(
                f"{name}={item['version']}={item['build']}" for name, item in providers.items()
            )
            with args.github_output.open("a") as stream:
                stream.write(f"specs={specs}\n")
        print(json.dumps(manifest, sort_keys=True))
    else:
        manifest = json.loads(args.manifest.read_text())
        verify("argdigest", identities=installed_identities(manifest, Path(sys.prefix)))


if __name__ == "__main__":
    main()
