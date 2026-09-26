# Recorda Development Guide

Recorda is currently in the **design stage**.

This directory is the entry point for developers and agents working on Recorda. Do not infer a frozen public API or implementation architecture from illustrative examples.

## Read first

1. [`DESIGN.md`](DESIGN.md) — current general/standalone architecture and design seed for Recorda.
2. [`FIRST_SLICE.md`](FIRST_SLICE.md) — the first standalone implementation experiment.
3. [`NEXT_STEPS.md`](NEXT_STEPS.md) — the sequence of experiments and implementation work.

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

The first implementation should be driven by a real operation from a library outside MOLI, with explicit caller-owned capture. It should preserve room to revise the API and internal representation as evidence accumulates.
