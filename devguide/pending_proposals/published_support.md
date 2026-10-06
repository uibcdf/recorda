---
summary: Qualify published SMonitor and ArgDigest for the explicit Recorda integrations.
issue: uibcdf/recorda#18
status: active
opened: 2026-10-06
closed:
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

Local published-provider receiving checks pass; hosted acceptance is pending.
Receipt: [../evidence/published_support_local.json](../evidence/published_support_local.json).
