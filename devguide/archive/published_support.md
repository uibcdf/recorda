---
summary: Qualify published SMonitor and ArgDigest for the explicit Recorda integrations.
issue: uibcdf/recorda#18
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [engineering, distribution, arguments, diagnostics]
blocked_by: []
supersedes: []
---

# Published support-provider qualification

## What and evidence

Published SMonitor 0.19.0 build 1 and ArgDigest 0.15.0 build 0 contain the scoped
APIs previously tested with provider sources in `uibcdf/recorda#16` / #17.
With published DepDigest 0.13.0 build 0, they solve on the public Conda channels
`uibcdf` and `conda-forge` without a required scientific package or reverse cycle.
The isolated Python 3.14 environment resolves provider imports to its own installed
files, matching the qualified archive identities and installed-file hashes.
The existing 158 receiving/core regressions pass without provider PYTHONPATH.

Separate optional extras now express the explicit integration contract, including
SMonitor's new floor even though ArgDigest's generic dependency floor is older.
The two provider CI lanes use maintained Conda environment specifications and
verify exact artifacts/file hashes before installing Recorda and running tests.
No scientific boundary or default-core validation is changed. The original source
receipts and archives remain historical evidence.

## Acceptance and remaining scope

Require installed-Recorda local evidence, safe existing regression behavior,
metadata/Conda route agreement, and hosted Python 3.11–3.14 provider lanes inspected
with published gh-run-receptor. Preserve both positive and rejected-old/source
provenance checks in a new receipt.

The explicit integrations remain caller-selected. Default ArgDigest adoption and
reference-check options remain in `uibcdf/recorda#2`; public Recorda packaging,
recipe/preflight and release/OS qualification remain in #3 / #4. This work does
not publish Recorda, promote MOLI's registry or add a quantity/backend boundary.

## Resolution

Local source and installed-Recorda suites pass 158 tests with both integrations;
the disabled suite passes 104 with 54 explicit skips, and the recovery-only suite
passes 116 with 42 explicit skips. Published pytest-receptor 1.1.0, Ruff and
local/shared governance checks pass under Python 3.14.7.

[CI 37529525379](https://github.com/uibcdf/recorda/actions/runs/37529525379)
passes all 15 jobs at `2b8b3deecc43dc65e6c34e440dfeb0cbe3d29891`, including
the eight published-provider lanes on Linux Python 3.11–3.14. Published
gh-run-receptor 1.2.0 inspected that completed run. Provider archive hashes,
installed-file identities and optional-feature requirements passed before tests.

The closing documentation checkpoint changes no tested runtime, tool, metadata,
environment, workflow or wheel README bytes. No Recorda release or broader
default ArgDigest adoption is implied; those remaining contracts retain their
owning umbrella issues.
Receipt: [../evidence/published_support_local.json](../evidence/published_support_local.json).
