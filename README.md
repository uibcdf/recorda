# Recorda

**Scientific recording and provenance for reproducible computational work.**

Recorda is a lightweight recording layer for scientific software. It is useful with libraries outside MOLI, including libraries that cannot be modified. A caller can explicitly wrap a meaningful operation; a library author may instead instrument its own semantic API boundary. Both paths produce a standalone record that can be inspected without MOLI.

Conceptually, a caller of an unmodified library could write:

```python
with recorda.session("protein_analysis") as session:
    with session.operation("external_library.analyze", inputs={"model": model_ref}) as operation:
        result = external_library.analyze(model, settings)
        operation.output("result", result_ref)
```

This is illustrative syntax, not a published API. Starting a session does not automatically capture arbitrary uninstrumented calls. The caller declares the boundary and safe references; Recorda reports omissions and incomplete operations rather than implying complete coverage.

Existing scientific results and native provenance remain owned by their libraries. Recorda can reference them without replacing or copying them. Inside MOLI, the same substrate may later be enriched with ProjectContext, ExecutionPlan/Run, component references, Nextia ProjectGraph mutations, EventLedger, authorization, and ProjectRecord routing.

## Status

Recorda is currently at the **architecture/design stage**. The API above is illustrative, not frozen.

See [`devguide/DESIGN.md`](devguide/DESIGN.md) for the broad design and [`devguide/FIRST_SLICE.md`](devguide/FIRST_SLICE.md) for the first experiment ([Recorda #1](https://github.com/uibcdf/recorda/issues/1)).

## Core direction

- standalone scientific reproducibility for MOLI and third-party libraries;
- caller-owned explicit boundaries for unmodified libraries and opt-in instrumentation at semantic API boundaries;
- `start()/stop()`, context-manager, and managed activation over one RecordingSession model;
- dormant/negligible-overhead behavior when recording is inactive;
- safe capture with stable references and secret redaction;
- honest coverage, cross-library lineage, and nested-operation correlation;
- standalone inspect/audit/verify/export/computational replay;
- MOLI integration without making MOLI a dependency of scientific libraries.

## Relationship with MOLI

Recorda originated from MOLI's provenance requirements but is intentionally useful outside MOLI.

```text
Third-party library --caller boundary--> Recorda
Library-owned boundary -----------> Recorda
MOLI project context -------------> Recorda
```

A scientific component should not need to depend on MOLI merely to participate in reproducible recording.

## License

The repository license and packaging metadata will be finalized before the first release.
