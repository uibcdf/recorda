---
summary: Check declared references against explicit local file receipts.
issue: uibcdf/recorda#12
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [inspection, references, local-files]
blocked_by: []
supersedes: []
---

## Problem and accepted scope

SciPy and Sabueso laboratory readers duplicate local file availability and byte
checks. Extract that narrow mechanism into standalone Recorda, leaving native
manifest traversal and scientific identity/meaning with their owning inspectors.
An explicit local index binds the full Reference to relative locations. Journal
identifiers are never treated as paths or URIs. SHA256 must be explicitly declared
by the index; a digest string's length does not establish its algorithm.

## Alternatives and limits

Do not turn a local byte match into an authenticated identity, a complete native
dependency graph or replay claim. Unknown references remain unresolved and files
without digests remain available_unverified. Domain-specific receipt schemas are
adapted by the laboratory, not interpreted by core. Native checks remain separate
from recorded execution status; absent retained bytes do not rewrite history.

The locator is caller-owned trusted code/configuration, not a filesystem sandbox.
Resolved containment and nonregular-file checks limit the controlled local scope.
Hashing is streamed and bounded; reports omit paths, contents and arbitrary I/O
error text. Repeated references are checked once per report, with no global cache.

## Resolution and verification

LocalFileResolver, check_reference and check_references expose availability/byte
states, reference occurrences, explicit omissions and incomplete operation ids.
Default recording, inspection and the journal schema are unchanged. Old failures
without exception references report not_recorded rather than invented provenance.
Reports are independent of the inspected snapshot.

Twenty-two new regressions cover exact full-key lookup, digest/algorithm uncertainty,
missing/modified bytes, bounded and nonregular reads, rooted paths/symlinks, safe
I/O/opaque-value handling, files changed during checking, occurrence deduplication,
report independence, omissions, incomplete work and historical failures.
All 91 core and 21 Lab tests pass locally on Linux Python 3.14.7, with published
pytest-receptor 1.1.0. Six real-kernel notebooks execute 45 code cells. Existing
SciPy/Sabueso native semantics and the independent dummy are unchanged; frozen
scientific source fingerprints match before/after the run.

See ../REFERENCE_CHECKS.md and ../evidence/reference_checks_local.json for current
usage, exact tested source hashes/commands and controlled reports. The Lab adoption
and sixth notebook are owned by uibcdf/recorda-lab#9. This is source work after
immutable 0.2.0, without a new public artifact or platform/replay claim.
