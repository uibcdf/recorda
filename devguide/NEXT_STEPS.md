# Recorda — Next Steps

## Status and scope

Recorda has an **EXPERIMENTAL STANDALONE PROTOTYPE**. The first implementation experiment is specified in [`FIRST_SLICE.md`](FIRST_SLICE.md) and tracked in [Recorda #1](https://github.com/uibcdf/recorda/issues/1).

The architecture in [`DESIGN.md`](DESIGN.md) is intentionally broader. Build the smallest correct standalone recording substrate, learn from a library outside MOLI, and only then add platform integration.

## Current resumption order — 2026-10-06

The current resumption order is in [CHECKPOINT.md](CHECKPOINT.md): consolidate
standalone acceptance (`uibcdf/recorda#1` / `uibcdf/recorda-lab#1`), finish ecosystem
boundaries (`uibcdf/recorda#2`), then complete release reviews (`uibcdf/recorda#3`,
`uibcdf/recorda#4`, `uibcdf/recorda#6`) before any distributable release. Choose the
next scoped experiment before implementation. The small workflow linking native
references across steps is implemented and qualified in `uibcdf/recorda-lab#10`;
read [STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md) for evidence and remaining
scope. It uses the current core API and does not complete broader acceptance.

The current support-library audit is in
[SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md), owned by `uibcdf/recorda#2`.
Classification is complete for today's runtime; wider ArgDigest/SMonitor adoption
is pending. The explicit recovery adapter in [RECOVERY_DIAGNOSTICS.md](RECOVERY_DIAGNOSTICS.md)
was first qualified with provider sources in `uibcdf/recorda#16`, followed by
explicit configuration in [ARGUMENT_CONFIGURATION.md](ARGUMENT_CONFIGURATION.md)
under `uibcdf/recorda#17`. The new published SMonitor 0.19.0 / ArgDigest 0.15.0
closure replaces that source route in `uibcdf/recorda#18`. Default CapturePolicy
adoption is complete in `uibcdf/recorda#19`, with all 11 installed-package/quality
CI jobs passing. Continue with the reference-check
contracts in `uibcdf/recorda#20`. Keep dependency metadata,
environment specifications and executed provider evidence aligned.
Before advancing Lab's Recorda candidate, provision its required provider closure
and qualify the new exact pair in `uibcdf/recorda-lab#12`.

The experiment sections below record completed slices and design constraints;
they are not a queue of unimplemented work. MOLI integration, API freezing,
generic replay and distributed routing remain later decisions.

## Do not do yet

Do **not** begin by:

- implementing the complete architecture in `DESIGN.md` or freezing the public API;
- creating the complete recording-profile catalog or a large storage framework;
- promising automatic capture of uninstrumented library calls from `start()` alone;
- implementing full replay/export/import machinery;
- implementing MOLI-specific routing before standalone recording works;
- instrumenting every helper function in a scientific package;
- requiring an existing component to replace its own records with Recorda records.

## First experiment — controlled standalone laboratory

Use deterministic dummy operations from `uibcdf/recorda-lab`. Keep that library independent
of Recorda; explicit and decorated boundaries belong to its experimental consumers.
A session makes declared calls inspectable without implying unwrapped calls were captured.
The recommended library usage is start once, call decorated semantic functions normally,
and stop recording. Optional context managers share that lifecycle. The activation
experiment additionally exercises session-local native-reference adapters and semantic
profile labels, without implementing the broader profile/policy catalog.
PyUnitWizard is not modified or instrumented. A real external library follows the laboratory
to establish practical utility before Sabueso or platform integration.

Build only:

1. one RecordingSession lifecycle and a local durable ScientificRecord;
2. one explicit operation boundary usable around unmodified library code;
3. one opt-in decorator or equivalent hook sharing the same operation model;
4. operation identity, implementation identity, start/terminal status, safe input/output references, failure, parent/correlation identity where needed, and visible omissions;
5. incremental persistence of a started operation so interruption leaves a detectable incomplete record;
6. inactive instrumentation with normal library behavior and negligible practical overhead.

Keep exact API, file format, serializer protocol, and packaging details provisional. Recorda should never blindly serialize credentials or large runtime objects. A recorded reference does not itself guarantee retained bytes or replay.

The acceptance cases in [`FIRST_SLICE.md`](FIRST_SLICE.md) cover success, exception, interruption, inactive behavior, nesting, redaction, native-record coexistence, and coverage gaps. Inspect the record with Recorda alone; no MOLI dependency or project context.

The laboratory now retains usage notebooks, real IPykernel cell/fault acceptance
and repeated direct/inactive/active timing measurements, tracked by
`uibcdf/recorda-lab#3` and `uibcdf/recorda-lab#2`. Local evidence is scoped to the
tested kernel/client and storage. Active synchronous recording costs milliseconds
per declared call in the dummy experiment; reference hashing adds input-dependent
work. This reinforces semantic boundary selection before real-library validation.
Do not infer a universal negligible-overhead guarantee or browser support.

## Real external-library experiment — controlled SciPy fitting

`uibcdf/recorda-lab#4` exercises unmodified SciPy parameter estimation through a
caller-local decorated alias. Native/dormant/active fits agree with an independent
least-squares oracle. An actual failed attempt/retry remains visible, with referenced
model/input/solver/native-result files. A notebook simulates usage; a Recorda/stdlib
inspector checks trial receipts. This qualifies that scenario, not arbitrary SciPy
outputs or general research workflows. See `evidence/scipy_local.json` and the
laboratory's `devguide/SCIPY_TRIAL.md`. No core runtime dependency is added.

## Controlled Sabueso semantic boundaries

`uibcdf/recorda-lab#5` now exercises native UniProt retrieval and Sabueso entity
resolution with three attributed frozen public responses and no source connections.
Resolution actually consumes the retrieved primary accession. The trial retains
ambiguity, organism-based selection and discarded alternatives, returned semantic
errors and a native source exception. Sabueso owns Cards, decisions and acquisition
traces; Recorda references them at seven declared operation boundaries. Direct,
dormant and active scientific content agrees. An eight-cell fourth notebook uses
start/stop across cells. The independent reader requires Recorda and stdlib only
and detects removed or modified native files.

Read the laboratory's `devguide/SABUESO_TRIAL.md` and
`devguide/evidence/sabueso_linux_py314.json` for Linux Python 3.14 co-development
identities and source hashes. Final receipts use frozen copies of the scientific
development packages because their live checkouts changed concurrently. These are
local development sources, not evidence
for published Sabueso/provider packages, complete pipeline capture or MOLI routing.
The full local pair passed 54 tests, including all four usage notebooks.

## Native exception provenance

`uibcdf/recorda#7` adds opt-in native exception references using the existing session
mapping. Failed operations retain `exception.reference` without new scientific
function arguments or caller recording statements. Unknown types and callback faults
are visible omissions; the native exception, cause and traceback propagate unchanged.
No arbitrary exception messages, dictionaries or repr are captured. The controlled
Sabueso adoption in `uibcdf/recorda-lab#6` removes manual trace-sidecar retention from
the runner and fourth notebook. The provisional API has no new MOLI dependency.

## Manual recovery from incomplete operation persistence

`uibcdf/recorda#8` fixes a pre-existing limitation found during exception-capture
regressions. Running execution is now tracked independently of writer failure, so
manual stop can finish incomplete after an operation's terminal write fails.
Owner-context and genuinely active async-operation barriers remain enforced.
Seven regressions cover before-line and after-line fsync faults, original errors,
failed finalization, subsequent activation and nested operation lineage. See
`archive/manual_persistence_finalization.md` and `evidence/manual_recovery_local.json`.
Broader reliability policies remain a later platform concern.

## Bounded capture selection

`uibcdf/recorda#11` and `uibcdf/recorda-lab#8` compare two session policies over
the same unchanged dummy calculation. Selected lifecycle/implementation facts
remain mandatory; profile selection and payload-group switches expose explicit
coverage and omissions. The fifth notebook keeps ordinary calls across cells.
See `CAPTURE_SELECTION.md` for the limits: excluded outcomes are unobserved,
minimal detail loses native dependencies, and timing is scenario-specific.
This is not the broader MOLI profile/routing/reliability engine.

## Declared local reference checks

uibcdf/recorda#12 and uibcdf/recorda-lab#9 introduce a common explicit local
reference index and bounded byte checker. The sixth notebook distinguishes
intact, missing, altered, unverified and unresolved files, omissions and incomplete
work. Existing SciPy/Sabueso inspectors reuse the checker without transferring
native semantic ownership. Read REFERENCE_CHECKS.md: hash algorithm declaration,
recorded execution status and reference observations remain separate. This is
not authenticated integrity, generic manifest traversal or replay.

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

Do not let packaging drive scientific design. License, `pyproject.toml`, tests, CI
configuration and Python policy are present. Before a distributable release, finish
versioning/release policy, Conda packaging and the distribution/OS reviews with
executed evidence under the applicable engineering/governance policies.

## Gate for broad implementation

Do not broaden Recorda substantially until the experiments show that standalone recording is useful beyond MOLI, uninstrumented coverage is represented honestly, inactive instrumentation is unobtrusive, failures and interrupted work are visible, and component-owned records remain authoritative. MOLI should be able to enrich the same substrate later without requiring a second, incompatible provenance model.
