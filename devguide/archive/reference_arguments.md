---
summary: Adopt ArgDigest for Recorda-owned local reference-check configuration.
issue: uibcdf/recorda#20
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [arguments, references, diagnostics, confidentiality]
blocked_by: []
supersedes: []
---

# Reference-check argument adoption

## Decision and compatibility

Retain the public closed signatures, exact resolver/record identities, positive
non-boolean byte limits and explicit sha256-or-None algorithm. An exact index
dictionary uses exact Reference keys and existing str/Path location forms.
Root str/os.PathLike inputs retain native Path conversion; invalid option shapes
are refused before conversion, relative confinement before root resolution.
No opaque coercion or new index-size bound is introduced.

Individual reference representations retain structured invalid_reference
observations. Scientific identity/manifest validity stays producer-owned.
ArgDigest validates options once at a public checking boundary; the guarded
private byte-check core serves cached distinct references without re-digestion.
Containment, streamed byte limits, observed status and independent report data
remain mandatory even through private unwrapping.

## Imports and diagnostic authority

Resolver construction and checking calls load the already-required published
providers lazily. Plain import and journal inspection stay provider-free.
The #19 receipt's earlier checking-call import behavior remains historical.
Use the existing safe SMonitor first-use baseline, preserve application/project
policy and omit configuration values, paths, record content and inherited context
through metadata-only construction/invocation. No provider patch or new dependency
floor is needed.

## Acceptance

Require native compatibility, invalid-reference observations, no I/O for invalid
options, bypass/confidentiality/application/delivery-fault regressions, source and
installed-wheel checks on Python 3.14 with published pytest-receptor, and all
installed-package/recovery CI lanes inspected with published gh-run-receptor.
Keep a separate receipt and archive the resolved analysis; old receipts are not
rewritten. Laboratory receiving remains in uibcdf/recorda-lab#12.

## Resolution and evidence

The 50 new receiving regressions pass locally, as do all 221 source and installed
development-wheel tests with recovery enabled on Python 3.14.7 using published
pytest-receptor 1.1.0. Default tests pass 209 with 12 explicit recovery skips.
Ruff, local/shared governance, dependency preflight, exact public-provider
provenance and pip checks pass. [CI 37534456487](https://github.com/uibcdf/recorda/actions/runs/37534456487)
passes all 11 jobs at `c6248686815bd405a08955565e4fdc232bcef906`, inspected
with published gh-run-receptor 1.2.0. Six default lanes cover Linux Python
3.11–3.14/macOS 3.13–3.14; four Linux recovery lanes and quality also pass.
Public checker signatures and the guarded native byte-check body are structurally
unchanged from the #19 checkpoint. The separate receipt is
[../evidence/reference_arguments_local.json](../evidence/reference_arguments_local.json).

Closing documentation preserves every receipt-selected runtime, test, tool,
metadata, Conda, workflow and wheel README byte. This completes the present
ArgDigest reference boundary without qualifying a public Recorda release or a
new Lab candidate. Core applicability/adoption evidence can now be reconciled
with MOLI's still-partial registry through `uibcdf/moli#62`; future presentation
and provider-operation correlation remain separate #14/#15 evaluations.
