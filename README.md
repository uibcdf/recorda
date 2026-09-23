# Recorda

**Scientific recording and provenance for reproducible computational work.**

Recorda is a lightweight recording layer for scientific software. Instrumented libraries remain usable on their own; when Recorda is activated, it captures the operations, inputs, parameters, environments, dependencies, outputs, failures, and lineage needed to inspect, audit, export, and replay computational work.

```python
import recorda

recorda.start("tim_analysis")

system = molsysmt.convert(...)
pockets = topomt.detect_pockets(system)
features = topomt.characterize(pockets)

record = recorda.stop()
```

When no recording session is active, instrumented APIs behave normally. Inside MOLI, the same recording substrate is enriched with ProjectContext, ExecutionPlan/Run, Sabueso/Praxis references, Nextia ProjectGraph mutations, EventLedger, authorization, and ProjectRecord routing.

## Status

Recorda is currently at the **architecture/design stage**. The API above is illustrative, not frozen.

See [`devguide/DESIGN.md`](devguide/DESIGN.md) for the complete design.

## Core direction

- standalone scientific reproducibility;
- low-friction instrumentation at semantic API boundaries;
- `start()/stop()`, context-manager, and managed activation over one RecordingSession model;
- dormant/negligible-overhead behavior when recording is inactive;
- safe capture with stable references and secret redaction;
- cross-library lineage and nested-operation correlation;
- standalone inspect/audit/verify/export/computational replay;
- MOLI integration without making MOLI a dependency of scientific libraries.

## Relationship with MOLI

Recorda originated from MOLI's provenance requirements but is intentionally useful outside MOLI.

```text
TopoMT ------> Recorda
MolSysMT ----> Recorda
Sabueso -----> Recorda
Nextia ------> Recorda

MOLI --------> Recorda
```

A scientific component should not need to depend on MOLI merely to participate in reproducible recording.

## License

The repository license and packaging metadata will be finalized before the first release.
