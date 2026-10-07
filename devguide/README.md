# Recorda Development Guide

Recorda has an **experimental standalone prototype**; its public API and schema remain provisional.

This directory is the entry point for developers and agents working on Recorda. Do not infer a frozen public API or implementation architecture from illustrative examples.

## Read first

Start with [`CHECKPOINT.md`](CHECKPOINT.md) for the published source pair,
executed evidence, resumption checklist and prioritized remaining work.
Read [`STANDALONE_ACCEPTANCE.md`](STANDALONE_ACCEPTANCE.md) for the current
completed original standalone acceptance matrix, consumer questions and separately
scoped scientific qualification.

1. [`DESIGN.md`](DESIGN.md) — current general/standalone architecture and design seed for Recorda.
2. [`FIRST_SLICE.md`](FIRST_SLICE.md) — the first standalone implementation experiment.
3. [`NEXT_STEPS.md`](NEXT_STEPS.md) — the sequence of experiments and implementation work.
4. [`ENGINEERING_REVIEW.md`](ENGINEERING_REVIEW.md) — MOLI engineering applicability and remaining qualification; [`SUPPORT_LIBRARIES.md`](SUPPORT_LIBRARIES.md) records current boundary decisions and qualified adoption.
5. [`reporting_protocol.md`](reporting_protocol.md) — owning issues, report queues and archive.
6. [`PYTHON_SUPPORT.md`](PYTHON_SUPPORT.md) — Python 3.11–3.14 and the tracked MOLI transition.
7. [`ACTIVATION.md`](ACTIVATION.md) — recommended start/stop, context ownership and native adapters.

8. [`CAPTURE_SELECTION.md`](CAPTURE_SELECTION.md) — bounded session selection and detail.

9. [`REFERENCE_CHECKS.md`](REFERENCE_CHECKS.md) — declared local reference availability and byte checks.

10. [`RECOVERY_DIAGNOSTICS.md`](RECOVERY_DIAGNOSTICS.md) — explicitly selected
    SMonitor recovery diagnostics and published-provider qualification.

11. [`ARGUMENT_CONFIGURATION.md`](ARGUMENT_CONFIGURATION.md) — default ArgDigest
    capture configuration, lazy imports and published-provider qualification.

12. [`INSPECTION_PRESENTATION.md`](INSPECTION_PRESENTATION.md) — experimental
    read-only technical findings and SMonitor message resolution; laboratory
    receiving evaluation is tracked in Recorda Lab #13.

13. [`DIAGNOSTIC_CORRELATION.md`](DIAGNOSTIC_CORRELATION.md) — completed producer
    diagnostic association analysis and completed application-owned comparison
    in `uibcdf/recorda-lab#14`, followed by native Sabueso receiving qualification
    in `uibcdf/recorda-lab#15`; a reusable core live adapter needs a new decision.

## MOLI integration contract

Recorda is independently useful for reproducible computational work, but MOLI uses Recorda as its recording/provenance substrate.

Developers changing Recorda behavior that affects context, profiles, routing, operation identity, event emission, lifecycle, integrity, replay, persistence, or semantic-change recording must also read:

**MOLI — Recorda Provenance Integration**  
https://github.com/uibcdf/moli/blob/main/devguide/RECORDA.md

The responsibilities are intentionally separated:

    recorda/devguide/DESIGN.md
        general / standalone Recorda design

    recorda/devguide/FIRST_SLICE.md
        first standalone experiment

    recorda/devguide/NEXT_STEPS.md
        current implementation sequence

    moli/devguide/RECORDA.md
        MOLI-specific integration requirements

Recorda must remain usable without MOLI. MOLI enriches the common recording substrate with ProjectContext, ProjectRecord, EventLedger, Nextia ProjectGraph, authority, and project-level replay semantics.

## Current rule

Do not implement the complete design at once.

The implementation began with deterministic dummy operations in `uibcdf/recorda-lab`,
with explicit caller-owned capture and an opt-in consumer example. Controlled SciPy
and offline Sabueso trials have since completed; their evidence remains bounded
to the recorded scenarios. Do not instrument PyUnitWizard or adopt routine
quantity-conversion recording as a production boundary.
