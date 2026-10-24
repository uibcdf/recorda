# Runtime dependency policy — 2026-10-24

Owner: [uibcdf/recorda#35](https://github.com/uibcdf/recorda/issues/35).
Diego accepts this Recorda-local decision. Independent evaluation requests are
[MolI #76](https://github.com/uibcdf/moli/issues/76) and
[MolSysSuite #137](https://github.com/uibcdf/molsyssuite/issues/137); neither
issue establishes platform-wide or suite-wide adoption.

## Permitted installation and executed qualification

Declare the required consumed API floors: `argdigest>=0.15.0` and
`smonitor>=0.19.0`. Do not automatically reject every untested next provider
minor. An upper bound or exclusion requires a demonstrated incompatibility or
a concrete incompatible provider contract, with an owning issue and receiving
evidence. Any such change must be represented by the dependency preflight too.
This decision does not remove the independently admitted Python 3.11–3.14 bounds
or justify changing unrelated native/scientific dependency contracts.

Permitting package resolution does not certify compatibility with unexecuted
future versions. Keep the consumed safety/configuration/recovery/reader tests
and report discovered provider regressions to their owners. Scientific objects,
native failures and Recorda's recording boundaries are unchanged.

The Conda recipe must express the same public intervals as Python metadata;
it cannot silently retain a narrower ceiling. Development/test environments
may pin an exact supported closure. `devtools/check_dependencies.py` checks
both rules. Regression fixtures reject missing or weakened floors and stale
recipe ceilings, while admitting later provider versions in metadata.

## Reproducible qualification

The five existing environment specifications retain ArgDigest 0.17.0 py_0,
SMonitor 0.22.0 py_0 and DepDigest 0.15.1 py_0. The default
`verify_support_environment.py` remains tied to those original coordinates and
digests. Release gates continue to qualify the exact committed source and the
same original built artifact. A passing run with a different closure does not
replace that evidence or rewrite historical archives.

## Latest public compatibility monitoring

The separate `latest_support.yml` workflow runs weekly and by manual dispatch,
on Linux x86_64 and macOS arm64 with Python 3.14. It installs Recorda from the
checked-out source into its environment and tests the installed runtime with
recovery explicitly enabled and published pytest-receptor 1.2.1.

Before provisioning, `python -m devtools.latest_support select` reads the
canonical `uibcdf/noarch/repodata.json`, chooses the highest stable provider
version/build and records the actual index digest and public archive identities.
It ignores prerelease/development/local versions, does not rely on the registry's
`latest_version` field, and exports exact version/build specifications to the
solver. The sixth environment, `latest_support_env.yaml`, declares only runtime
floors; the selected specifications are supplied for that execution.

`python -m devtools.latest_support verify --manifest <selection.json>` checks
the actual installed archive against that retained index snapshot, including
equivalent `.conda` / `.tar.bz2` files for the same selected version/build.
It reuses the managed-file, digest, public-coordinate and import-ownership
checks without changing the default qualified cohort. Modified files and shadow
imports remain failures. The workflow also verifies installed Recorda bytes,
architecture, dependency closure and retains selection/installation JSON plus
complete pytest JSONL and JUnit output even when tests fail.

The latest lane has no tolerated failure. A solver/provider/runtime failure is
visible in GitHub and must be reported through the owning issue with the retained
identities; do not silence it or relabel the selected providers as qualified.
Tests against synthetic later-version metadata prove resolution policy only.

## Publication boundary

Public 0.3.2 and the completed #34 receipt remain immutable with their original
provider constraints. This policy changes source/editable requirements; its
public delivery needs a separately qualified release, proposed for 0.3.3.

## Executed receiving

Implementation source: `3c2dbc462fda451459e6b8f0af7d5d354ec50cd7`.
Local Linux/Python 3.14.9 targeted tests pass 68 cases; source and installed-wheel
suites each pass 408, recovery enabled, with clean dependency closure and
complete integrity-valid receptor/JUnit/native agreement.

[Source CI 40133093885](https://github.com/uibcdf/recorda/actions/runs/40133093885)
passes 14 jobs: eight fixed-cohort installed Linux/macOS arm64 Python 3.11–3.14
cells pass 390 tests with 18 explicit recovery skips; four Linux recovery cells
and coverage each pass all 408.
[Latest-public CI 40133098600](https://github.com/uibcdf/recorda/actions/runs/40133098600)
passes both Linux/macOS arm64 Python 3.14 cells with all 408 tests and zero
failures/skips/warnings. Downloaded selection/installation artifacts and complete
JSONL/JUnit verify the actual public cohort. Native steps, twelve full-capture
members and all 50 locally tested input hashes are independently checked.

Receipts: [local](evidence/dependency_policy_35_local.json),
[hosted](evidence/dependency_policy_35_hosted.json),
[resources](evidence/dependency_policy_35_resources.json).
The five qualified environment files and 15 runtime files are unchanged.
GitHub's nonblocking Node.js 20 action annotations are separately owned in
[Recorda #36](https://github.com/uibcdf/recorda/issues/36); no native gate failure
is attributed to those warnings. Wider policy evaluation remains open with
the two governance owners.
