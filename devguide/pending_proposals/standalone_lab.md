---
summary: Prove a minimal standalone recording substrate with a controlled dummy library.
issue: uibcdf/recorda#1
status: active
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

PyUnitWizard was considered and set aside as a laboratory host. A real third-party
library remains a later usability check. Building all MOLI infrastructure first is deferred.

## Acceptance criteria

- Persist starts before calls and detect process interruption without inferring success.
- Preserve original scientific exceptions and expose recording faults as incomplete work.
- Exercise both caller and opt-in boundaries, inactive behavior and parent identity.
- Link the dummy's native record without copying it into an operation output.
- Expose declared coverage and omissions; inspect without the producing library.
- Verify clean installed-package experiments and applicable governance/quality checks.
- Keep API/schema provisional and collect real-science evidence before broadening.

## Resolution

Open. Local prototype and laboratory evidence are not a public release, hosted CI result,
MOLI routing implementation or full replay guarantee.
