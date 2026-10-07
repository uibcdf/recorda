# Recorda — Next Steps

## Status and scope

Recorda has an **EXPERIMENTAL STANDALONE PROTOTYPE**. The first implementation experiment is specified in [`FIRST_SLICE.md`](FIRST_SLICE.md) and tracked in [Recorda #1](https://github.com/uibcdf/recorda/issues/1).

The architecture in [`DESIGN.md`](DESIGN.md) is intentionally broader. Build the smallest correct standalone recording substrate, learn from a library outside MOLI, and only then add platform integration.

## Current resumption order — 2026-10-07

The original standalone acceptance (`uibcdf/recorda#1` / `uibcdf/recorda-lab#1`)
is resolved with a criterion/evidence matrix and archived coordination reports.
Version 0.3.0 completes packaging/distribution and installed-platform/coverage
qualification (`uibcdf/recorda#3`, `uibcdf/recorda#4`, `uibcdf/recorda#6`), with
[executed release evidence](evidence/release_0_3_0.json). The maintainer's current
direction is to wait for consumer-owned adoption by MOLI components and MolSysMT.
Track shared registry reconciliation in `uibcdf/moli#62`; choose a new scoped
experiment only when a receiving consumer has a concrete question. The small workflow linking native
references across steps is implemented and qualified in `uibcdf/recorda-lab#10`;
read [STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md) for evidence and remaining
scope. It uses the current core API; the bounded native Sabueso follow-on also
contributes to the completed original acceptance. Wider usability and shared
integration require their own scientific questions and contracts.

The current support-library audit is in
[SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md), owned by `uibcdf/recorda#2`.
Classification and adoption are complete for today's core; MOLI registry
reconciliation is proposed in `uibcdf/moli#62`. The explicit recovery adapter in [RECOVERY_DIAGNOSTICS.md](RECOVERY_DIAGNOSTICS.md)
was first qualified with provider sources in `uibcdf/recorda#16`, followed by
explicit configuration in [ARGUMENT_CONFIGURATION.md](ARGUMENT_CONFIGURATION.md)
under `uibcdf/recorda#17`. The new published SMonitor 0.19.0 / ArgDigest 0.15.0
closure replaces that source route in `uibcdf/recorda#18`. Default CapturePolicy
adoption is complete in `uibcdf/recorda#19`, with all 11 installed-package/quality
CI jobs passing. Reference-check contracts in `uibcdf/recorda#20` are also complete,
with 221 source/installed tests and all 11 CI jobs passing. Keep dependency metadata,
environment specifications and executed provider evidence aligned.
Lab's required-provider receiving adoption is complete in `uibcdf/recorda-lab#12`:
242 local installed-pair tests pass, and both explicit-candidate and subsequent
default Jupyter/SciPy runs pass all nine jobs. The current exact pair and separate
receipts are identified in `CHECKPOINT.md`; Sabueso remains historical evidence.
SMonitor inspection presentation analysis (#14) is complete. The explicit
read-only core prototype in `uibcdf/recorda#21` now implements grouped findings
and nonemitting message resolution; read
[INSPECTION_PRESENTATION.md](INSPECTION_PRESENTATION.md). Its core source/installed and all 11 exact-head CI checks pass;
receiving/user-view evaluation and default promotion are complete in
`uibcdf/recorda-lab#13`, with 333 local installed-pair passes/four Sabueso skips,
six notebooks/49 cells and two passing nine-job hosted runs. Safe audience-hint improvement
is proposed in `uibcdf/smonitor#39` and is not a blocker. The nonbootstrapping
ArgDigest registration opportunity is `uibcdf/argdigest#32`, coordinated with
`uibcdf/moli#62`; the initial view uses native fact guards and existing audience. Provider-operation
correlation analysis (#15) is complete in
[DIAGNOSTIC_CORRELATION.md](DIAGNOSTIC_CORRELATION.md): compare application-retained
native bundles with a bounded consumer-owned association sidecar. That comparison
is now qualified in `uibcdf/recorda-lab#14`: 364 local installed-pair passes/four
Sabueso skips, seven notebooks/55 cells and nine exact-pair hosted jobs. Existing
explicit references suffice for the controlled question; a real producer/user
question is required before choosing any reusable core live adapter.
The native follow-up question is now exercised in `uibcdf/recorda-lab#15`: actual
Sabueso source partial/failure diagnostics beside its retained Cards and acquisition
traces. Corrected local qualification passes 380 tests/four historical Sabueso skips;
[exact-pair CI](https://github.com/uibcdf/recorda-lab/actions/runs/37584430143)
passes all 13 jobs, with 47 native passes per Python 3.11–3.14 minor. Existing explicit references suffice for
this bounded real-library question. The separately owned development preflight
mapping in `uibcdf/recorda#23` is resolved; its exact source
and hosted qualification are recorded in [CHECKPOINT.md](CHECKPOINT.md).
No core automatic adapter or MOLI routing implementation is queued by this trial.
Published-provider probes expose independently owned SMonitor export/buffer/
degradation opportunities in `uibcdf/smonitor#40`, `uibcdf/smonitor#41` and
`uibcdf/smonitor#42`; a controlled application-owned trial needs no MOLI restructure.

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
configuration and Python policy are present. The 0.3.0 release has a qualified
Conda artifact and publication route, exact installed OS/minor evidence and an
accepted live coverage producer. Follow [RELEASING.md](RELEASING.md) for a future
candidate; source or build-input changes require their own qualification.

## Gate for broad implementation

Do not broaden Recorda substantially until the experiments show that standalone recording is useful beyond MOLI, uninstrumented coverage is represented honestly, inactive instrumentation is unobtrusive, failures and interrupted work are visible, and component-owned records remain authoritative. MOLI should be able to enrich the same substrate later without requiring a second, incompatible provenance model.
