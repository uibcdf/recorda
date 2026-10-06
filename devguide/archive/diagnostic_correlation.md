---
summary: Evaluate selected SMonitor diagnostics associated with declared operations.
issue: uibcdf/recorda#15
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [diagnostics, correlation, native-references]
blocked_by: []
supersedes: []
---

# Producer diagnostic correlation analysis

## What

Compare application-retained SMonitor bundles with a live adapter for the question
“Which selected diagnostics accompanied this declared attempt of a fit?” This is
separate from Recorda recovery advice and post-inspection presentation.

## How / evidence

The owning issue precedes this report. Inspected published SMonitor 0.19.0 py_1,
current Recorda and existing independent Lab fitting source. Twenty bounded
public-API research cases and 15 unchanged recovery/import/view guards pass with
published pytest-receptor 1.1.0 on Linux Python 3.14.7. Exact provenance, hashes,
commands and checks are preserved in `../evidence/diagnostic_correlation_analysis.json`.
The public reproducer is `../evidence/diagnostic_correlation_probe.py`.

## Why

Diagnostics describe observations under application policy; scientific attempts,
native results and diagnostic artifacts have distinct identities and owners.

## Alternatives

Compared native bundle references, selected operation-local sidecars, and a
reusable automatic live adapter. Existing public explicit boundaries and
references suffice for a controlled application-owned comparison. A session-wide
bundle alone cannot identify a particular attempt. A reusable automatic adapter
needs separate evidence and a public boundary/context decision; private observers
and private Recorda context are rejected integration dependencies.

## Acceptance criteria

- Concrete consumer question and bundle/bridge comparison.
- Identity mapping, attachment/detachment and declared coverage.
- Concurrency, filtering, duplicates and recursion.
- Bounded safe persisted fields and native semantic ownership.
- Failure precedence and explicit incomplete diagnostic capture.
- Missing contracts routed to owning repositories.
- Recommendation and separately owned Lab scope if justified.

## Resolution

All architectural criteria are answered in
[../DIAGNOSTIC_CORRELATION.md](../DIAGNOSTIC_CORRELATION.md). The decision specifies
identity/ownership, attachment, bounded selection, concurrency/lifetime, delivery
coverage, aggregate counts, fault precedence and recursion. The existing-reference
probe links a reviewed synthetic native bundle without copying payloads into the
journal and preserves execution outcome after artifact removal.

Recommend separately owned `uibcdf/recorda-lab#14`: compare reviewed native bundle
references with a bounded consumer-owned association sidecar, retaining the native
dummy library and independent scientific oracle. Existing SciPy retry source
motivates distinct attempts but supplies no native SMonitor emission contract.
No scientific diagnostic bridge, notebook/default promotion or human usability
study is qualified by this analysis.

Provider opportunities/defects are routed to `uibcdf/smonitor#40` (strict bounded
nonemitting export), `uibcdf/smonitor#41` (buffer resizing), and `uibcdf/smonitor#42`
(handler degradation warning precedence). `uibcdf/moli#62` receives the direct-
consumer impact notice. No shared platform restructuring or MOLI runtime
dependency is needed for this controlled comparison. No provider code or release
is changed. Local governance/canonical-guide and Ruff checks pass; declared or
historical CI is not new executed bridge evidence. Recorda runtime, dependencies,
scientific code and previous evidence remain unchanged.
