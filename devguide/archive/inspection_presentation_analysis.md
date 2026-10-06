---
summary: Evaluate explicit technical inspection presentation with published SMonitor resolution.
issue: uibcdf/recorda#14
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [inspection, diagnostics, presentation]
blocked_by: []
supersedes: []
---

# Inspection presentation architectural evaluation

## What

Evaluate user-facing information after inspection independently of recovery advice
and live producer-event correlation. Preserve the structured scientific record,
current reference observations, expected omissions and native ownership.

## How / evidence

The issue precedes this report. Inspect current Recorda source, exact published
SMonitor 0.19.0 py_1 source/guide and its receiving tests. Thirteen focused research
probes pass with published pytest-receptor on Linux Python 3.14.7. Five unchanged
existing recovery/first-use/import guards pass. Rerun the unchanged Lab #9 reference
scenario with the current installed pair for real example facts; no new Lab feature
or scientific scenario is introduced. The complete boundary, proposed examples,
state/code table, comparison and failure contract are in
[../INSPECTION_PRESENTATION.md](../INSPECTION_PRESENTATION.md); exact evidence and
commands are in `../evidence/inspection_presentation_analysis.json`.

## Why

Execution success, current retained-byte observations and presentation availability
answer different questions. Two occurrences can refer to one missing artifact.
Expected omissions should remain visible without generating a warning storm.
Technical explanations must not infer scientific outcomes or rewrite provenance.

## Alternatives

A small Recorda-only renderer is feasible but repeats audience/message policy.
A Recorda finding/layout layer plus nonemitting SMonitor resolution reuses the
existing provider. Emitting artificial events for SMonitor report/coalescing would
mix unrelated diagnostics and couple the view to delivery; it is rejected here.

## Acceptance criteria

- Representative questions and proposed outputs are derived from existing scenarios.
- Compare the Recorda-only renderer and SMonitor; give a bounded recommendation.
- Specify provisional structured findings, catalog ownership, safe fields and grouping.
- Preserve machine-readable facts independently of prose and diagnostic delivery.
- Define opt-in behavior, absence/failure handling, expected omissions and duplicates.
- Separate technical explanations from domain interpretation and scientific communication.
- Record the gate required before implementation and before useful-user-view claims.

## Resolution

All architectural evaluation criteria are addressed. Recommend explicit read-only
post-inspection findings with Recorda-owned codes/states/counts/source pointers and
a lazy resolve-only SMonitor adapter, preserving default JSON and provider-free
plain reading. No runtime, CLI, journal, dependency or scientific-provider change
is implemented by this analysis. Existing references/recovery are unchanged.

Current safe profile messages work; safe hints are shared. Improvement proposal
`uibcdf/smonitor#39` requests explicitly declared safe audience templates without
weakening metadata-only capture. It is not a blocker and entails no provider patch
here. Prototype implementation is separately queued in `uibcdf/recorda#21`; Lab
receiving must receive its own issue before notebook/consumer changes. Live
correlation remains `uibcdf/recorda#15`. No MOLI restructuring is needed for this
bounded view. Governance, Ruff, dependency preflight and the shared MOLI checker
are verified locally; declared CI is not new executed evidence.
