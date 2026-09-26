# Recorda — Next Steps

## Status and scope

Recorda is currently **DESIGN-STAGE**. The first implementation experiment is specified in [`FIRST_SLICE.md`](FIRST_SLICE.md) and tracked in [Recorda #1](https://github.com/uibcdf/recorda/issues/1).

The architecture in [`DESIGN.md`](DESIGN.md) is intentionally broader. Build the smallest correct standalone recording substrate, learn from a library outside MOLI, and only then add platform integration.

## Do not do yet

Do **not** begin by:

- implementing the complete architecture in `DESIGN.md` or freezing the public API;
- creating the complete recording-profile catalog or a large storage framework;
- promising automatic capture of uninstrumented library calls from `start()` alone;
- implementing full replay/export/import machinery;
- implementing MOLI-specific routing before standalone recording works;
- instrumenting every helper function in a scientific package;
- requiring an existing component to replace its own records with Recorda records.

## First experiment — standalone with an external library

Use a deterministic scientific operation from a library outside MOLI. Do not modify that library's source. The caller owns an explicit semantic boundary around the operation. A session must make the declared call inspectable without implying that unwrapped calls were captured.

Build only:

1. one RecordingSession lifecycle and a local durable ScientificRecord;
2. one explicit operation boundary usable around unmodified library code;
3. one opt-in decorator or equivalent hook sharing the same operation model;
4. operation identity, implementation identity, start/terminal status, safe input/output references, failure, parent/correlation identity where needed, and visible omissions;
5. incremental persistence of a started operation so interruption leaves a detectable incomplete record;
6. inactive instrumentation with normal library behavior and negligible practical overhead.

Keep exact API, file format, serializer protocol, and packaging details provisional. Recorda should never blindly serialize credentials or large runtime objects. A recorded reference does not itself guarantee retained bytes or replay.

The acceptance cases in [`FIRST_SLICE.md`](FIRST_SLICE.md) cover success, exception, interruption, inactive behavior, nesting, redaction, native-record coexistence, and coverage gaps. Inspect the record with Recorda alone; no MOLI dependency or project context.

## Second experiment — Sabueso semantic boundaries

Use the same standalone substrate on exactly enough real functionality to test two patterns:

- one knowledge-retrieval boundary, including source/query, retrieval time, implementation/version, safe response identity or snapshot reference, produced Sabueso object reference, and failure;
- one entity-resolution boundary, including input entity/query, decision or ambiguity status, produced object/reference, and operation lineage.

Sabueso owns Knowledge semantics. Recorda records the declared operation and its provenance. Use a controlled scientific workflow to ask whether the record is useful to a scientist, whether missing dependencies and failures are visible, and whether instrumentation is low-friction.

## Later — MolSysSuite and MOLI

Before adding Recorda to any MolSysSuite component, inspect that component's existing records and identify a concrete missing provenance link. Component-owned records and Results remain authoritative. Decide case by case whether a Recorda hook, a reference to a native record, or another adapter adds value. Do not impose a suite-wide recording pattern from this prototype.

After standalone records prove useful, test a small cross-component computational workflow for operation correlation and native-record references. Separately, test MOLI ProjectContext, EventLedger routing, and composed ProjectRecord linkage. Nextia ProjectGraph mutations and scientific meaning remain owned by Nextia.

## Only after evidence

Then evaluate, in an order informed by the experiments:

1. stabilizing the minimal operation/record schema and public API;
2. lifecycle recovery and reliable persistence policy;
3. serializer/reference and redaction contracts;
4. a small semantic-profile catalog and persistence/backend boundary;
5. integrity/verification, export, and computational replay;
6. standalone-record import/reference into MOLI;
7. project routing, cross-process context, and distributed/HPC buffering.

## Packaging and repository infrastructure

Do not let packaging drive scientific design. Before the first distributable release, add a license, `pyproject.toml`, tests, CI, supported Python policy, versioning/release policy, and documentation under the applicable engineering/governance policies.

## Gate for broad implementation

Do not broaden Recorda substantially until the experiments show that standalone recording is useful beyond MOLI, uninstrumented coverage is represented honestly, inactive instrumentation is unobtrusive, failures and interrupted work are visible, and component-owned records remain authoritative. MOLI should be able to enrich the same substrate later without requiring a second, incompatible provenance model.
