---
summary: Receive ArgDigest 0.17 and SMonitor 0.22 for the editable workspace.
issue: uibcdf/recorda#34
status: active
opened: 2026-10-24
closed:
verification: measured
area: [engineering, distribution, arguments, diagnostics]
blocked_by: []
supersedes: []
---

# Support-provider cohort receiving

## What

Public ArgDigest 0.17.0 and SMonitor 0.22.0 are excluded by Recorda 0.3.2's
metadata. The independently reported audit passes all 376 unchanged tests but
reproduces those two dependency conflicts. This blocks coherent editable
workspace refresh in uibcdf/molsyssuite#135; Praxis owns its separate #14.
The completed uibcdf/recorda#24 cohort and all public artifacts remain intact.

## How / evidence

Review provider tag diffs and consumed APIs; widen only the bounded upper limits,
align the Conda recipe, five environments and exact-provider digests, then test
fresh public dependency provisioning, source and installed-wheel behavior and
actual runtime origins. Preserve the diagnostic configuration decision from #29.
Read [current receiving](../LATEST_SUPPORT_RECEIVING.md) for exact files and
the distinction between source receiving and public package availability.

## Acceptance criteria

- The reviewed minors are admitted; unreviewed next minors remain excluded.
- Provider coordinates and all managed Python bytes match public Conda records.
- Native exits, receptor artifacts and JUnit agree with explicit recovery enabled.
- Dependency routes, clean installed closure, quality/governance and applicable
  exact-source CI pass; return the commit and evidence to both requesting owners.
- Preserve the shared environment, primary providers and immutable public files.

## Alternatives

Unbounded upgrades would admit unreviewed future APIs. Rewriting 0.3.2 would
invalidate immutable evidence. Neither is selected. New provider features are
not needed for this compatibility receiving.

## Resolution

Local fresh public Conda provisioning verifies all three original archives and
97 managed provider Python files. Source and private installed-wheel suites each
pass 378 tests with recovery explicitly enabled and zero failures/skips/warnings.
A separate clean venv installs actual editable snapshots of the audited provider
commits; all 378 tests and dependency closure pass with runtime origins asserted
both normally and under `python -I`. All 15 Recorda runtime files are unchanged.
Receipts: [public](../evidence/support_cohort_34_local.json) and
[editable](../evidence/support_cohort_34_editable.json).

The initial inherited-venv source attempt reproduced the known editable-finder
shadowing trap from the opening issue and was rejected by the runtime-origin
assertion before any test claim. The accepted lane has no inherited site-packages.
No primary provider tree or shared environment was changed.

Pending exact-source hosted gates and owner handoff. No release is selected.
