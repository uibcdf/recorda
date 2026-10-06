---
summary: Prove a minimal standalone recording substrate with a controlled dummy library.
issue: uibcdf/recorda#1
status: partial
opened: 2026-10-05
closed:
verification: reproduced
area: [recording, persistence, laboratory]
blocked_by: []
supersedes: []
---

# Standalone laboratory slice

## What

Build one experimental explicit operation/session model and optional decorator, tested
against an independent dummy library in `uibcdf/recorda-lab`. PyUnitWizard is not
instrumented or modified. Laboratory success does not establish utility in real science.

## How / evidence

The local JSONL prototype fsyncs operation starts before target execution, records
outputs and terminal outcomes incrementally, and reports unclosed operations as incomplete.
Safe capture accepts bounded ordinary scalars and caller-issued references. Opaque objects
and sensitive named fields are omitted; exception messages are omitted to protect secrets.

The agreed library-facing procedure activates once with start/stop and calls decorated
semantic functions normally. `tests/test_activation.py` checks manual lifecycle,
context ownership, repeated-start refusal, running-operation refusal, failures and
unclosed sessions. Session-local exact-type adapters capture native references while
preserving scientific return identity; their faults remain visible omissions.
`recorda-lab/experiments/run_activation.py` is the corresponding checked laboratory.
The context manager remains a convenience interface over the same lifecycle.

`tests/test_recording.py` guards success, native references, target exceptions, hard exit,
inactive behavior, nesting, secret/opaque omissions, storage failures, truncated tails,
schema rejection and coroutine correlation. Recorda Lab executes independent scenarios,
preserves a native result, and writes an inspectable acceptance report.

## Why

A small controlled laboratory makes lifecycle and coverage failures reproducible before
adding real-library, project or distributed integration. Individual quantity conversions
are not selected as permanent production recording boundaries.

## Alternatives

PyUnitWizard was considered and set aside as a laboratory host. Controlled SciPy
and offline Sabueso trials have since completed. Building all MOLI infrastructure
first remains deferred.

## Current progress — 2026-10-06

The controlled slices are published: manual activation, notebooks/cost trials,
SciPy, offline Sabueso, native exception references, persistence recovery,
capture selection and explicit local reference checks. [../CHECKPOINT.md](../CHECKPOINT.md)
identifies the exact source pair, 112 local passing tests, six notebooks/45 cells,
successful hosted core/Jupyter/SciPy checks and the local-only provider limits.
Resolved slice analyses remain in `../archive/`; this broader coordination report
stays open for standalone acceptance consolidation and engineering review.

`uibcdf/recorda-lab#10` now prepares a multi-step scientific workflow using
the existing core API. [../STANDALONE_ACCEPTANCE.md](../STANDALONE_ACCEPTANCE.md)
records local qualification, useful native dependency links and remaining limits.
Owner review and hosted evidence for that new Lab source remain separate.

## Acceptance criteria

- Persist starts before calls and detect process interruption without inferring success.
- Preserve original scientific exceptions and expose recording faults as incomplete work.
- Exercise both caller and opt-in boundaries, inactive behavior and parent identity.
- Link the dummy's native record without copying it into an operation output.
- Expose declared coverage and omissions; inspect without the producing library.
- Verify clean installed-package experiments and applicable governance/quality checks.
- Keep API/schema provisional and collect real-science evidence before broadening.

## Resolution

Partial. Completed trials and hosted checks qualify their recorded scenarios;
consolidation of broader standalone usefulness remains in uibcdf/recorda#1.
Distribution and engineering reviews have separate owning issues. No public
release, MOLI routing implementation or full replay guarantee is established.
