# Recorda — Next Steps

## Status

Recorda is currently **DESIGN-STAGE**.

The architecture is intentionally richer than the implementation we should build first. The next task is to discover the smallest correct recording substrate through real scientific use.

## Do not do yet

Do **not** begin by:

- implementing the complete architecture in `DESIGN.md`;
- freezing the public API;
- creating the complete recording-profile catalog;
- building a large persistence/storage framework;
- implementing full replay/export/import machinery;
- implementing MOLI-specific routing before standalone recording works;
- instrumenting every helper function in a scientific package;
- adding infrastructure merely because it may be useful later.

Implementation should follow evidence from real semantic operations.

## First prototype — minimal Recorda core

Build only enough to test the fundamental recording model.

### RecordingSession

Support the conceptual lifecycle behind:

    recorda.start("analysis")
    ...
    record = recorda.stop()

A context-manager interface may share the same underlying session model, but it need not be the first user-facing feature if that slows the prototype.

### Dormant instrumentation

An instrumented function must behave normally when no RecordingSession is active.

The inactive path should not materially change scientific behavior and should have negligible practical overhead.

### One instrumentation mechanism

Prototype one decorator or equivalent semantic-boundary hook, conceptually:

    @recorda.record(...)
    def scientific_operation(...):
        ...

Do not freeze the final decorator signature yet.

### Minimal operation record

Capture enough to establish:

- operation identity;
- component/package/module/function identity;
- package/version and, where practical, code/Git identity;
- start/end/lifecycle status;
- bound input arguments using safe serialization/reference rules;
- outputs/references;
- exception/failure state;
- parent/correlation identity where already needed.

Secrets and unsuitable large runtime objects must not be blindly serialized.

### Minimal local ScientificRecord

Persist or expose a local record sufficient to inspect:

- recorded operations;
- chronological order;
- inputs/outputs;
- dependencies/lineage that can already be inferred;
- versions;
- failures and incomplete sessions.

Do not implement the full final storage architecture yet.

## First scientific integration — Sabueso

Use Sabueso as the first proving ground.

Instrument exactly enough real functionality to test two different semantic patterns:

### Knowledge retrieval

Choose one real external-knowledge retrieval boundary.

Test whether Recorda can capture/reference:

- source/service;
- query/request;
- retrieval time;
- implementation/version;
- response identity/hash or snapshot reference where appropriate;
- produced authoritative Sabueso objects;
- failure state;
- safe handling of credentials/secrets.

### Entity resolution

Choose one real entity-resolution boundary.

Test:

- component/function identity;
- input entity/query;
- relevant dependencies;
- produced resolution object/reference;
- ambiguity/failure state;
- operation lineage.

Recorda records the operation; Sabueso remains owner of Knowledge semantics.

## Validate through the TcTIM Phase-1 pilot

Use a real TcTIM Phase-1 notebook to determine whether the minimal Recorda record is useful to a scientist.

Questions to answer include:

- Can we see exactly what Sabueso did?
- Can we identify the inputs and versions?
- Can we follow meaningful dependencies?
- Are failures visible?
- Is the notebook no longer the only provenance record?
- Is the instrumentation low-friction?
- Are we capturing too much or too little?
- Which design concepts in `DESIGN.md` become necessary in practice?

Missing requirements discovered here should refine the design before broad implementation.

## Second scientific integration — TopoMT / MolSysSuite

After the Sabueso prototype is useful, test a computational-analysis path in TopoMT.

This should exercise different pressure:

- scientific-analysis recording;
- molecular-system inputs by stable reference/content identity;
- parameters;
- Results and Artifacts;
- nested MolSysSuite operations;
- parent/child operation identity;
- cross-component lineage;
- Run/correlation concepts where justified;
- failures/retries.

A useful target is a small MolSysMT → TopoMT workflow whose standalone ScientificRecord can reconstruct the computational lineage.

## Only after evidence from the first integrations

Then evaluate, in approximately this order:

1. stabilize the minimal operation/record schema;
2. refine RecordingSession lifecycle and crash recovery;
3. stabilize serializer/reference and redaction contracts;
4. define the smallest useful semantic profile catalog;
5. choose persistence/backend boundaries;
6. add integrity/verification;
7. add export;
8. add computational replay;
9. test standalone-record import/reference into MOLI;
10. implement MOLI ProjectContext/routing/EventLedger/ProjectRecord integration;
11. test Nextia ProjectGraph mutation recording;
12. evaluate distributed/HPC buffering and strict versus best-effort policies.

This ordering is guidance, not a frozen release roadmap. Evidence may justify reordering.

## Packaging and repository infrastructure

Do not let packaging work drive the scientific design.

Before the first distributable release, Recorda will need normal project infrastructure such as:

- license;
- `pyproject.toml`;
- tests;
- CI;
- supported Python policy;
- versioning/release policy;
- documentation;
- PyPI/conda-forge planning as appropriate.

Those should be introduced under the applicable engineering/governance policies when implementation begins, not guessed during the design-only stage.

## Gate for broad implementation

Do not broaden Recorda substantially until the first real integrations demonstrate that:

- standalone recording is scientifically useful;
- inactive instrumentation is unobtrusive;
- operation identity and lineage are adequate;
- ownership boundaries remain clean;
- Recorda does not require MOLI for standalone use;
- MOLI can plausibly enrich the same substrate rather than needing a second provenance system.

The goal of the first implementation is **learning**, not feature completeness.
