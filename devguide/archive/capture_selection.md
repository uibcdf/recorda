---
summary: Select declared profiles and payload groups once per standalone session.
issue: uibcdf/recorda#11
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [recording, capture, profiles, coverage]
blocked_by: []
supersedes: []
---

## Problem and decision

The existing profile argument only labels operations. Users need to control journal
volume without editing scientific function bodies or losing declared coverage.
Use a bounded immutable session CapturePolicy, separating semantic labels from
selection. A full MOLI catalog, routing and strict/buffered reliability policies
remain outside this standalone experiment.

Selected operations always retain identity, implementation, parent, times and
lifecycle outcome; safe exception type remains mandatory. Input/parameter/output
and native exception-reference groups are selectable and expose policy omissions.
Disabled capture never runs its adapter. Excluded boundaries preserve scientific
behavior and contribute only invocation counts, with no captured payload/outcome.
The nearest selected ancestor remains the recorded parent.

## Alternatives and limits

Logging every excluded invocation would recreate the volume problem. Counts are
aggregated until finalization, bounded to 64 profiles plus an overflow total. A
missing terminal marker leaves counts unknown. Excluded errors are unobserved,
so session success describes selected work, not every arbitrary call. Excluded
async work is not joined by stop; its caller remains responsible for awaiting it.
Writer faults continue blocking selected execution and are not cleared by policy.

A minimal payload-free mode loses native input/output dependencies. This is
explicit in metadata and useful for examining the tradeoff, not a claim of full
scientific provenance. Group switches were selected before a per-field policy
engine. The default behavior and prior journal shape remain unchanged without
capture_policy; old journals remain readable. No release tag is changed.

## Resolution and verification

CapturePolicy is available on start/session/RecordingSession, with copied labels
and exact boolean validation. Additive capture/coverage fields remain in provisional
recorda.journal/0.1. Sixteen new cases cover immutable/invalid configuration,
sync/async/explicit selection, adapter suppression, safe selected failure and native
excluded errors, nearest recorded ancestry, bounded counts, missing final markers,
all-profile native references and unchanged selected writer-fault behavior.

All 69 core tests and 20 controlled laboratory tests pass locally on Linux Python
3.14.7, using published pytest-receptor 1.1.0. Five real-kernel notebooks execute
37 code cells; the SciPy and frozen-source Sabueso lanes remain enabled. Dummy
and scientific provider sources are unchanged. Source manifests, commands,
measurements and notebook receipts are in ../evidence/capture_selection_local.json.
The laboratory owns its scenario and fifth notebook under uibcdf/recorda-lab#8.
See ../CAPTURE_SELECTION.md for current usage and limits.
