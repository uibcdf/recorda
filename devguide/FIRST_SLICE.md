# Recorda: first standalone slice

**Status:** design proposal for the first implementation experiment, tracked in [Recorda #1](https://github.com/uibcdf/recorda/issues/1). It narrows, but does not replace, [`DESIGN.md`](DESIGN.md).

## What this slice must prove

Recorda is useful to a scientist using a library outside MOLI. The library may be unmodified, may already maintain its own provenance, or may later opt into Recorda instrumentation. Recorda must remain installable and inspectable without MOLI.

The first result is a local, durable record of *declared semantic operations*. Opening a session establishes recording context; it does not observe arbitrary Python calls. The caller must explicitly wrap an operation, or the library author must instrument its boundary. Coverage and omissions must be visible so the record never implies that an unobserved workflow was captured completely.

## Two entry paths, one operation model

1. **Caller-owned boundary for an unmodified library.** The caller identifies a meaningful operation and wraps its call with Recorda's explicit operation mechanism. Recorda observes invocation, outcome, and chosen references at that boundary. It does not monkey-patch the library, infer its internals, or claim to know intermediate calls.
2. **Library-owned boundary.** A library author can opt in with one decorator or equivalent hook at a semantic API boundary. With no active session, that function behaves normally. The hook and the explicit boundary write the same kind of operation record.

The public syntax remains open. An example of the intended *shape*, not a frozen API:

```python
with recorda.session("protein_analysis") as session:
    with session.operation("external_library.analyze", inputs={"model": model_ref}) as operation:
        result = external_library.analyze(model, settings)
        operation.output("result", result_ref)

local_record = session.record
```

`model_ref` and `result_ref` are caller-supplied safe references or descriptors. Recorda should not inspect `model` or `result` recursively by default. A library's existing result and provenance remain its own; their stable identifiers can be linked from the Recorda operation. The same operation should not be presented as two independent scientific actions merely because both systems recorded it.

## Minimal durable facts

For each session and operation, the prototype needs only enough information to answer what was attempted, by which implementation, with which declared inputs, what happened, and what can be inspected later:

- unique session and operation identifiers; parent/correlation identifier when nested;
- caller-declared semantic operation name and implementation package, module/function, version when knowable; unknown values stay unknown;
- start time and a persisted `started` state **before** invoking the target;
- terminal `succeeded` or `failed` state, end time, safe output references, and safe exception summary;
- on inspection or recovery, an operation with a persisted start and no terminal outcome is reported as `incomplete`, never inferred success;
- safe input/output descriptors and references to native records, with capture omissions or redactions made explicit;
- enough ordering information to inspect the sequence without assigning scientific meaning to the result.

The exact file format and public schema are not frozen. The local persistence mechanism must write incrementally enough that a crash does not erase the fact that an operation began. An exception should be re-raised with the library's normal behavior after Recorda records the failure; recording failures must not silently produce a record marked complete.

Recorda captures only what the caller or instrumented boundary declares and what its safe adapters can represent. Credentials, raw large objects, and unsupported values are omitted or represented by stable references with a reason. A hash or reference is useful only if its source and resolution conditions are clear; neither implies that the source bytes were preserved or that replay is possible.

## Ownership and later integration

Third-party and MolSysSuite components may keep their own scientific records. Those records remain authoritative for the component's domain outputs and internal execution details. Recorda can later correlate its operation identity with a component record reference, preserving owner, identifier, and revision or integrity information when available. It should not copy the whole component record, overwrite it, or require the component to abandon existing provenance.

Whether a particular MolSysSuite component should expose a Recorda hook, link a native record, or use another adapter is a later decision based on its actual records and workflows. This first slice does not set a suite-wide integration contract.

MOLI adds project scope, authorization, EventLedger routing, and composed ProjectRecord views in a separate experiment. No MOLI package, project identifier, or platform profile is required for this slice. Recorda does not turn a component result into Nextia Evidence or decide its scientific meaning.

## Evidence required before broadening

Use a deterministic operation from a library outside MOLI, with an unmodified source, and a small opt-in instrumented example. Inspect the stored record after each case:

1. successful call with safe input and output references;
2. target exception, preserving the exception for the caller and recording failure;
3. process interruption after the persisted start, leaving a detectable incomplete operation;
4. inactive decorator behavior and nested correlation under an active session;
5. a secret or unsupported object omitted with an explicit reason;
6. a native provenance/result reference linked without copying or changing the native record;
7. a clear statement of instrumented coverage and known gaps.

Only then apply the same substrate to a Sabueso retrieval and an entity-resolution boundary. Evaluate component-owned MolSysSuite records before any MolSysSuite integration. Test MOLI routing after standalone records prove useful. Stabilize public API, schema, storage, and replay claims from the evidence, not from this sketch.
