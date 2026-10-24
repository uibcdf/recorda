---
summary: Permit later provider versions and monitor current public compatibility.
issue: uibcdf/recorda#35
status: active
opened: 2026-10-24
closed:
verification: inspected
area: [engineering, distribution, dependencies]
blocked_by: []
supersedes: []
---

# Permissive runtime provider requirements

## Decision and motivation

Diego accepts minimum-only ArgDigest/SMonitor runtime dependencies, exact
qualification pins and separate latest-public compatibility monitoring. The
completed #34 admitted a new public cohort without changing any runtime file,
but automatic next-minor ceilings would repeat that metadata conflict.

Read [the maintained policy](../DEPENDENCY_POLICY.md). The owning domain
evaluations are uibcdf/moli#76 and uibcdf/molsyssuite#137; they are notices and
evaluation requests, not adoption outside Recorda.

## Acceptance

- Python metadata and the recipe admit later versions while preserving floors;
  negative route fixtures reject weakened floors and hidden recipe ceilings.
- Existing exact-cohort environments and provenance guards remain intact.
- A weekly/manual latest-public installed lane selects stable canonical Conda
  coordinates, checks actual provider/runtime bytes and origins, enables recovery,
  preserves native test outcomes and retains auditable identity/test artifacts.
- Execute relevant Python 3.14 local source/installed checks, quality/governance,
  exact-source CI and the new latest workflow; archive meaningful evidence and
  return the measured result to the three owning issues.

## Resolution

Implementation and verification in progress. No public release is selected by
this implementation task; the 0.3.3 candidate needs its own qualification.
