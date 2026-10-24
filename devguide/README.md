# Recorda Development Guide

Recorda has an **experimental standalone prototype**; its public API and schema remain provisional.

This directory is the entry point for developers and agents working on Recorda. Do not infer a frozen public API or implementation architecture from illustrative examples.

## Read first

[Diagnostic setup decision](DIAGNOSTIC_SETUP.md) records #29's retained safe
baseline, registration/emission distinction and optional receiving dispositions.

Start with [`CHECKPOINT.md`](CHECKPOINT.md) for the published source pair,
executed evidence, resumption checklist and prioritized remaining work.

Latest source receiving, [uibcdf/recorda#34](https://github.com/uibcdf/recorda/issues/34),
admits ArgDigest 0.17 / SMonitor 0.22 for the shared editable refresh, with
aligned metadata, recipe, environment pins and provider provenance. Three local
lanes each pass 378 tests and exact-source CI passes 14/14 jobs. Read
[LATEST_SUPPORT_RECEIVING.md](LATEST_SUPPORT_RECEIVING.md); this is separate
from the unchanged public 0.3.2 package below.

The later accepted [dependency policy](DEPENDENCY_POLICY.md), owned by
`uibcdf/recorda#35`, permits later provider versions from the required floors,
retains reproducible qualification pins and adds separate latest-public
monitoring. Local 68/408/408 checks pass; hosted qualification passes 14 source
jobs and two latest-public cells with 408 tests each. The
[receipt](evidence/dependency_policy_35_hosted.json) binds the exact source and
actual installed identities.
Independent domain evaluations are uibcdf/moli#76 and uibcdf/molsyssuite#137.

Current delivered release is 0.3.2 (`uibcdf/recorda#33`), resolving published
receptor receiving (#31) and stable packaged description (#32). Read
[TEST_TOOL_RECEIVING.md](TEST_TOOL_RECEIVING.md) and
[PACKAGED_DESCRIPTION.md](PACKAGED_DESCRIPTION.md). Fresh source, actual artifact
and installed gates passed; the [release receipt](evidence/release_0_3_2.json)
records public metadata/assets and the MolSysSuite #130 handoff. Earlier receipts
remain historical and immutable.
Read [`STANDALONE_ACCEPTANCE.md`](STANDALONE_ACCEPTANCE.md) for the current
completed original standalone acceptance matrix, consumer questions and separately
scoped scientific qualification.

[`RELEASING.md`](RELEASING.md) describes the 0.3.0 stabilization qualification
and exact-file publication route. Its [release receipt](evidence/release_0_3_0.json)
records executed gates and independently observed publication. Current work is
the **published 0.3.2 maintenance release** in `uibcdf/recorda#33`.
Its [release receipt](evidence/release_0_3_2.json) records fresh source, exact-Conda,
public installation and GitHub asset checks; the historical 0.3.0 package retains
its original ceilings. Receiving is communicated in `uibcdf/molsyssuite#130`.
Read the current checkpoint before following older adoption
sequences. MOLI #62 coordination and Recorda #29 receiving are complete;
consumer adoption and a new public artifact keep their own qualification.

For future public GitHub Releases, check that the visible title is exactly
the `X.Y.Z` version, matching the tag and package version; descriptions
belong in the release notes.

At task and release closeout, review temporary qualification environments,
test output, build trees and downloaded copies. Remove owned disposable
resources after their last needed use; retain exact candidate artifacts and
useful evidence with an owner and review trigger. Follow
`../MOLI_GUIDE.md#temporary-development-resources` and the local environment
and release routes.

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
