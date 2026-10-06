---
summary: Prototype explicit read-only technical inspection findings and SMonitor resolution.
issue: uibcdf/recorda#21
status: active
opened: 2026-10-06
closed:
verification: measured
area: [inspection, presentation, diagnostics]
blocked_by: []
supersedes: []
---

# Read-only inspection view

## What

Implement the #14 recommendation using an exact inspected ScientificRecord and an
explicit optional same-snapshot reference report. Preserve original facts and
execution status, with bounded findings and nonemitting SMonitor catalog resolution.

## How / evidence

Public entry point is `inspection_view(record, *, reference_report=None)`.
It introduces no audience normalization/configuration option: the application's
SMonitor audience governs resolution. Native exact-type/domain/schema guards
validate the copied facts; no new argument-digestion transformation is needed.
Existing CapturePolicy/reference ArgDigest boundaries remain unchanged.

A fresh published ArgDigest 0.15.0 import bootstraps an unconfigured application's
SMonitor policy and changes logging/warning hooks. The provider owns the proposed
registration-only improvement, coordinated with MOLI #62. Do not patch provider
internals or bootstrap the application just to validate a new presentation option.

## Why

Users need to distinguish execution, current reference observations, incomplete
work, expected omissions and presentation faults without rewriting provenance or
loading scientific producers. Repeated references need occurrence and unique counts.

## Alternatives

Resolve-only presentation avoids manufacturing events for SMonitor report. A full
second text catalog is unnecessary; structured state/count fallback is sufficient.
An explicit local audience option can follow a public nonbootstrapping ArgDigest
route; the initial prototype respects the existing application audience.

## Acceptance criteria

Implement bounded copied snapshots, complete same-snapshot report validation,
all current/unknown reference states, coverage/omission facts, deterministic groups
and numeric source pointers. Preserve hook/config/handler state and lazy plain
imports. Retain structured facts on ordinary provider faults, validate input before
provider import, and propagate user interrupts/cancellation. Execute source and
installed tests, governance/Ruff, published providers and exact-head CI with receptors.

## Resolution

Core implementation and local qualification are complete: 83 new regressions,
304 full source/installed recovery tests, or 292 installed default tests with
12 explicit recovery skips. Published Python 3.14.7/provider provenance, ordinary
wheel/source/installed payload equality (15 runtime files), pip check, governance,
shared MOLI core, Ruff and dependency preflight pass. Evidence is retained in
`devguide/evidence/inspection_view_local.json`. Exact-head hosted qualification
is pending before resolution.

Laboratory receiving/user-view evaluation is separately owned by
uibcdf/recorda-lab#13, opened before notebook/consumer changes. The registration-only
provider proposal is uibcdf/argdigest#32, coordinated with uibcdf/moli#62.
Lab's default core remains b3a53770e3b9917e5ff399dbfc00a9c53f2a37ac.
