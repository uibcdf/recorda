---
summary: Adopt published ArgDigest for default CapturePolicy construction.
issue: uibcdf/recorda#19
status: active
opened: 2026-10-06
closed:
verification: reproduced
area: [arguments, diagnostics, distribution, confidentiality]
blocked_by: []
supersedes: []
---

# Default configuration adoption

## Implementation and ownership

Ordinary CapturePolicy construction now uses the same scoped value pipelines
qualified through the earlier explicit factory. Providers load lazily at
configuration use; scientific calls and independent journal/reference reading
retain their ownership and import behavior. The compatibility factory delegates
to the constructor. Body/final guards preserve invariants through private
unwrapping and no public bypass is exposed.

ArgDigest's first-use bootstrap otherwise enables global logging capture. Before
its import, Recorda uses public SMonitor ensure_configured with its own safe
baseline to disable global logging/warning/exception capture when no application
or project policy exists. Existing application configuration is preserved; this
uses the resolved provider API rather than a provider patch/private-state workaround.

Required ArgDigest/SMonitor metadata, all inventoried Conda routes and a local
noarch source-development recipe agree. The early read-only preflight includes
negative missing-dependency, stale/weak environment, unsupported Python, source
version below floor and unclassified runtime-route cases. Public Recorda release
qualification remains separate in #3/#4; the local recipe is not publication.

## Acceptance and evidence

Require source and installed-wheel regressions under Python 3.14 with published
pytest-receptor, executed default installed-package Linux Python 3.11–3.14 and
existing macOS lanes, opt-in recovery lanes, and inspection with published
gh-run-receptor. Keep scientific native behavior, confidentiality, application
policy and provider-free read paths verified. Preserve evidence in
[../evidence/default_arguments_local.json](../evidence/default_arguments_local.json).

## Resolution

Local source and installed-wheel checks pass 171 tests with recovery enabled,
or 159 with 12 explicit-recovery skips in the default lane. Ruff, both governance
checks, dependency preflight and installed provenance/pip checks pass. Hosted
qualification remains in progress. Reference-check contract analysis is recorded separately in #20;
the wider ecosystem review remains partial until that adoption is complete.
