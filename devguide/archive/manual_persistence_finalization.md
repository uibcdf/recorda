---
summary: Allow manual finalization after an operation terminal-write fault.
issue: uibcdf/recorda#8
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [recording, lifecycle, persistence]
blocked_by: []
supersedes: []
---

## What and evidence

An operation whose terminal event cannot be persisted used to retain its id in
_open_operations even after its execution exited. Manual stop consequently rejected
an idle session as running, leaving it attached and blocking later activation.
Context-managed cleanup already allowed incomplete finalization. This defect was
found during the exception-reference work, without requiring any reference adapter.

The pre-fix regression run reproduced the stop barrier after an injected terminal
write failure. That first failed finalization leaked activation into subsequent
cases; those cascading failures were not independent defect reproductions.

## Alternatives

Bypassing the running-operation barrier whenever the writer is broken would let
the owner stop while an inherited async task is still executing. Clearing the
writer fault after execution would falsely suggest complete persistence. Neither
is acceptable. A second incomplete-operation registry is unnecessary: the broken
writer already tracks persistence failure, and inspection retains durable starts
without outcomes as incomplete operations.

## Resolution and verification

The private running-operation set now tracks execution until operation exit and
removes the id in its finally cleanup, including after a terminal write fault.
The independent broken-writer flag remains set. Manual stop still checks running
work and the activating context, then attempts an incomplete final session marker.
If that marker also fails, the error propagates after detachment and file closure.
No public API, schema, storage backend or reliability policy is added.

Seven regressions cover errors before writing a terminal line and fsync faults
after its complete line, with native success and failure; prefix and sequence
preservation; rejection of further declared execution; failed stop and later
activation; genuinely live async work and wrong-owner stop; and nested lineage.
Original scientific exceptions propagate by identity, and arbitrary error text
is absent from persisted records.

All 53 core tests and the unchanged 19 Recorda Lab tests passed locally on Linux
Python 3.14.7 using published pytest-receptor 1.1.0. This includes four actual
usage notebooks (29 code cells), SciPy and frozen-source Sabueso trials. Scientific
provider and laboratory sources matched their before/after fingerprints. See
`../evidence/manual_recovery_local.json` for commands, source hashes and scope.
The immutable 0.2.0 checkpoint predates this correction; this is unreleased source
work and does not establish a new artifact or platform-support claim.
