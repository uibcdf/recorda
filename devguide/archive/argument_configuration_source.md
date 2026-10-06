---
summary: Qualify explicit ArgDigest CapturePolicy construction with safe diagnostics.
issue: uibcdf/recorda#17
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [arguments, diagnostics, confidentiality]
blocked_by: []
supersedes: []
---

# Explicit source-provider argument configuration

## What and ownership

Introduce an explicit factory for Recorda-owned capture configuration using both
ArgDigest contract axes. Keep scientific calls and mandatory capture invariants
under their existing owners. The public dependency/adoption decision belongs to
the umbrella ecosystem/distribution issues `uibcdf/recorda#2` / #3.

## Implementation and evidence

[../ARGUMENT_CONFIGURATION.md](../ARGUMENT_CONFIGURATION.md) documents the closed
factory signature, reusable bounded value pipelines, defensive canonicalization
and metadata-only construction/invocation. Shared validators keep core guards
active even through private bypasses. An explicit config isolates application
defaults without changing SMonitor policy. Tests check recording behavior and
native errors as well as configuration and diagnostics.

The provider route pins ArgDigest `5e7925ddcd14922d00647d39b6a97eed2499bc23`,
SMonitor `6feac9728cc35d57cbc92f284d7040d7f04cb35b` and published DepDigest
0.13.0. The source APIs are absent from the checked published ArgDigest 0.14.0
and SMonitor 0.18.0. The local receipt identifies source/installed checks and a
development wheel and executed hosted qualification.

## Alternatives and acceptance

An unpublished required dependency cannot establish a supported public route.
An implicit fallback would silently change validation/telemetry guarantees.
Keep the source experiment explicitly selected until published artifacts are
qualified. Mandatory checks remain in the core; a decorative digestion bypass
cannot switch off confidentiality or lifecycle correctness.

Close this bounded experiment after local source and installed-Recorda evidence,
governance/Ruff checks, and executed Linux Python 3.11–3.14 provider CI inspected
with published gh-run-receptor. Preserve the partial umbrella adoption status.

## Resolution

The experiment passes 158 local source and installed-Recorda tests on Python
3.14.7 with published pytest-receptor 1.1.0, plus Ruff and local/shared governance.
[CI 37505815276](https://github.com/uibcdf/recorda/actions/runs/37505815276)
passes all 15 jobs at `4ad2531b84373f83a81ca69d0861ce2e106fefc0`, including
the four Linux Python 3.11–3.14 ArgDigest lanes. Published gh-run-receptor 1.2.0
inspected the completed run.

The initial hosted run exposed a subprocess test helper that placed shared
site-packages before pinned provider sources. It was reproduced with an ordinary
isolated-environment Recorda installation and corrected before the passing run;
the receipt preserves that failure and its cause. The closing documentation
checkpoint changes no runtime/test/metadata/workflow byte from the passing commit.

No release, public dependency floor, default-core adoption or platform exception
is claimed. Wider adoption, reference-check contracts and publication qualification
remain in `uibcdf/recorda#2` / #3.
