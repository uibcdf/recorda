---
summary: Permit later provider versions and monitor current public compatibility.
issue: uibcdf/recorda#35
status: resolved
opened: 2026-10-24
closed: 2026-10-24
verification: measured
area: [engineering, distribution, dependencies]
guard: tests/test_dependency_contract.py::test_reviewed_provider_cohort_is_admitted
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

Implemented at `3c2dbc462fda451459e6b8f0af7d5d354ec50cd7`. Local targeted/source/
installed tests pass 68/408/408 under Python 3.14.9 with published receptor 1.2.1.
The [source CI](https://github.com/uibcdf/recorda/actions/runs/40133093885) passes
all 14 jobs; [latest-public CI](https://github.com/uibcdf/recorda/actions/runs/40133098600)
passes Linux/macOS arm64 Python 3.14 with all 408 tests in each. Downloaded
complete integrity-valid JSONL, JUnit and native exits agree. Actual public
selection, installed managed bytes/origins and dependency closure are verified.
The [hosted receipt](../evidence/dependency_policy_35_hosted.json) checks twelve
capture members and all 50 locally tested input hashes against the source.

The guard requires precisely the consumed provider floors and permits later
minor/major versions in metadata; restoring automatic next-minor ceilings fails
its assertions. The dependency-contract module rejects hidden recipe ceilings
and weakened floors. `tests/test_latest_support.py` protects stable selection,
canonical public coordinates, retained index identities and archive-format
handling. `tests/test_support_environment.py` proves changed bytes, wrong
coordinates and source shadowing still fail; the default qualification checker
continues to reject an unqualified cohort. Synthetic future-version fixtures
prove the policy, not future runtime compatibility.

The initial mixed-URL installer dry-run was not selected: the maintained lane
exports validated exact version/build specs, then verifies the actual archive
format/digest against the retained public-index snapshot. No source or weaker
provenance fallback is used. The five existing pinned environments and 15
Recorda runtime files are unchanged. Domain issues MolI #76 / MolSysSuite #137
receive the result without an adoption claim. Separately reported nonblocking
Actions annotations are `uibcdf/recorda#36`.

No public release is selected by this implementation task; the 0.3.3 candidate
needs its own exact-artifact qualification. Useful evidence is retained with an
owner/review trigger after retiring disposable resources; see
[resource closeout](../evidence/dependency_policy_35_resources.json).
