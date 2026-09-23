> **Canonical design:** This document is derived from the original MOLI Scribe design and is now maintained in Recorda. Recorda is a standalone scientific recording/provenance library; MOLI enriches it with project and Discovery context.

# Recorda — Scientific Recording and Provenance

## Status

**Recorda** is the working name for a lightweight scientific recording and provenance layer for reproducible computational work. MOLI uses Recorda as its instrumentation substrate and enriches it with project, knowledge, methodology, discovery, authority, and cross-component context.

Recorda may therefore be useful both **standalone** and **inside MOLI**.

Recorda is an **implementation direction**, not a new scientific component alongside Sabueso, Praxis, Nextia, or MolSysSuite, and this document does not yet freeze a package/repository boundary or exact Python API.

The name evokes a scribe whose role is to observe and faithfully record what happens without deciding what the science means.

## MOLI integration requirements

Recorda is independently useful for standalone scientific reproducibility, but it is also the recording/provenance substrate used by MOLI.

Developers changing Recorda's context model, profiles, routing, operation identity, event emission, lifecycle, integrity, replay, or persistence behavior **must also read the MOLI-side integration specification**:

**MOLI — Recorda Provenance Integration:**  
https://github.com/uibcdf/moli/blob/main/devguide/RECORDA.md

That document defines what MOLI requires from Recorda for:

- ProjectContext propagation;
- ownership-aware routing;
- EventLedger and ProjectRecord integration;
- ExecutionPlan / Run correlation;
- scoped ProjectRecord views;
- semantic consumption provenance;
- Nextia ProjectGraph mutation recording;
- human/agent attribution and approvals;
- strict versus buffered recording;
- Audit / Trace / Replay;
- Scientific Communication provenance.

The two documents have different authority:

    recorda/devguide/DESIGN.md
        general / standalone Recorda design

    moli/devguide/RECORDA.md
        MOLI integration requirements for Recorda

Recorda should remain usable without MOLI. MOLI-specific requirements should enrich/configure the common recording substrate rather than force standalone scientific libraries to depend on MOLI.


## Purpose

MOLI requires distributed components to preserve enough structured provenance for ProjectRecord, EventLedger, Audit, Trace, Replay, ProjectRelease, and Scientific Communication.

Requiring every scientific function to hand-write this infrastructure would create duplicated boilerplate and inconsistent records.

Recorda should provide a common, low-friction way to instrument **scientifically meaningful operations** across MOLI components.

Conceptually:

    Sabueso --------┐
    Praxis ---------|
    Nextia ---------|
    MolSysMT -------|
    TopoMT ---------|
    DockingMT ------|
    ...             |
                    v
                 Recorda
       context + instrumentation
       profiles + safe capture
       routing + event emission
                    |
                    v
        MOLI Provenance Contract
                    |
          +---------+---------+
          v                   v
      EventLedger        ProjectRecord

Component-owned scientific objects remain owned by their components.

## Recorda records; it does not interpret

Recorda's central boundary is:

    AUTOMATIC / STRUCTURED RECORDING

    what happened
    where it happened
    who/what executed it
    with what inputs/parameters
    with what software/environment
    what it produced
    whether it failed
    how it relates operationally to parent work

versus:

    EXPLICIT DISCOVERY SEMANTICS

    what a Result means scientifically
    which Hypothesis it bears on
    whether it supports/contradicts
    what Decision should follow

The second category belongs to Nextia Discovery semantics and must not be inferred merely because Recorda observed a computation.

For example, TopoMT may produce Result R71 and Recorda may record the complete operation. Only an explicit Nextia operation should create an Observation or Evidence relationship saying what R71 means for a Hypothesis.

> **Components own scientific meaning; Recorda records consequential operations and semantic changes.**

> **Nextia owns Discovery meaning; Recorda records the provenance and evolution of that meaning in the ProjectGraph.**

Recorda therefore remains active when work enters Nextia. It can instrument the explicit operation that creates an Observation, links Evidence to a Hypothesis, records a Decision, rejects/supersedes a Hypothesis, or otherwise mutates the ProjectGraph. What Recorda must not do is invent that Discovery meaning merely because it observed an upstream computation.



## Standalone reproducibility and MOLI-enriched provenance

Recorda should not exist only as hidden MOLI plumbing.

A researcher using MolSysSuite components independently should be able to activate Recorda and obtain a reproducible scientific record without installing or adopting the MOLI platform.

Conceptually:

                    Recorda
          scientific recording runtime
                      |
           +----------+----------+
           |                     |
           v                     v
      standalone mode         MOLI mode
           |                     |
    researcher records       ProjectContext
    scientific operations         |
           |                     v
           v                ProjectRecord
    standalone record         EventLedger
    replay metadata          ProjectGraph changes

The same instrumented component APIs should work in both modes.

### Standalone example

Conceptually:

    import recorda

    recorda.start("tim_analysis")

    system = molsysmt.convert(...)
    pockets = topomt.detect_pockets(system)
    features = topomt.characterize(pockets)

    record = recorda.stop()

Recorda may capture:

    MolSysMT / TopoMT versions
    operation identities
    inputs / stable references
    parameters
    environment
    operation dependencies
    outputs / Artifacts
    hashes
    timestamps
    warnings / failures

This has scientific value independently of MOLI.

### Cross-component standalone records

A standalone recording may span several instrumented libraries:

    ScientificRecord
        |
        +-- OP1 MolSysMT.convert
        |       input -> output MS1
        |
        +-- OP2 TopoMT.detect_pockets
        |       consumes MS1
        |       produces R1
        |
        +-- OP3 TopoMT.characterize
                consumes R1
                produces R2

Recorda can therefore improve reproducibility across MolSysSuite even when no MOLI ProjectGraph or ProjectRecord exists.

## Lightweight runtime and dependency direction

Instrumented scientific libraries must not depend on MOLI merely to use Recorda.

A desirable dependency direction is conceptually:

    TopoMT -------> Recorda
    MolSysMT -----> Recorda
    Sabueso ------> Recorda
    Nextia -------> Recorda

    MOLI ---------> Recorda
    MOLI ---------> Sabueso / Nextia / MolSysSuite / ...

and not:

    TopoMT -------> MOLI

Recorda should therefore be capable of becoming a lightweight MOLI-independent runtime/distribution if implementation experience supports that boundary.

Its core concerns may include:

    operation identity
    recording sessions
    context propagation
    capture
    serialization / stable references
    redaction
    lifecycle
    correlation
    events
    routing hooks

MOLI can then enrich/configure Recorda with richer project semantics, profiles, destinations, authorization, and ProjectRecord/EventLedger integration.

The final repository/package boundary remains open until tested.

## Dormant instrumentation

A component may remain instrumented even when no recorder is active.

Conceptually:

    instrumented function called
              |
              v
      active recording context?
          /             \
        no               yes
        |                 |
        v                 v
    execute normally   capture + route

The inactive path should have negligible practical overhead and should not change scientific behavior.

This allows ordinary users to call:

    topomt.detect_pockets(system)

without knowing that the function is Recorda-aware.

Instrumentation is activated only when a recording session/context/backend is active.

## RecordingSession

The activation mechanisms should converge on one underlying concept: a **RecordingSession** or equivalent runtime state.

A session may carry:

    recording identity
    name / label
    start / stop time
    active context
    correlation state
    recording profiles
    routing/backend configuration
    lifecycle/status
    integrity state

The exact object/API is not frozen.

Different user interfaces should open/configure/close the same underlying recording mechanism.

## Activation mode 1 — start / stop

For notebooks and exploratory scientific work, explicit recorder-style activation should be first-class.

Conceptually:

    recorda.start("my_analysis")

    ... scientific work across cells/functions ...

    record = recorda.stop()

This matches the mental model of switching on a recorder, doing the work, and switching it off.

It is particularly appropriate for Jupyter because a Python `with` block is inconvenient across multiple notebook cells.

All instrumented semantic operations between start and stop are associated with the active RecordingSession according to context/routing policy.

### Interrupted sessions

A missing `stop()` must not erase provenance.

If the kernel/process fails or the user forgets to stop recording, the session should remain detectable as something such as:

    interrupted
    incomplete
    unclosed

rather than appearing as a successfully closed complete record.

Recovery/reconciliation behavior remains an implementation question.

## Activation mode 2 — context manager

Scripts and bounded operations may prefer:

    with recorda.recording("my_analysis"):
        ...

The context manager provides reliable cleanup/finalization semantics when exceptions occur.

An exception can close the session with an appropriate failed/partial status rather than losing the record.

The context manager is a convenience interface, not the mandatory Recorda usage pattern.

## Activation mode 3 — MOLI-managed recording

Inside MOLI, users should not normally need to manually start Recorda for every operation.

Opening/executing a MOLI project/run may activate and configure the RecordingSession automatically.

Conceptually:

    project = moli.open_project(...)

    ... project execution ...

MOLI supplies the richer active context:

    Project
    Workspace
    Campaign / work scope
    ExecutionPlan
    Run
    actor
    authorization
    correlation
    routing
    EventLedger
    ProjectRecord

The scientific component APIs remain the same ones used standalone.

Thus:

    standalone:
        researcher explicitly activates Recorda

    MOLI:
        platform activates/configures Recorda

The recording substrate remains shared.

## Pause and resume

Standalone recording may eventually support:

    recorda.pause()
    ...
    recorda.resume()

This can be useful during exploratory notebook work when a researcher deliberately does not want selected activity included in the active scientific recording.

However, pause/resume must never create invisible gaps.

Recorda should record explicit lifecycle events such as:

    RecordingPaused
    RecordingResumed

and the resulting record must reveal that recording was discontinuous.

Under a MOLI `strict` recording policy, pause may be forbidden for a Run or other consequential scope whose provenance is required to be complete.

The exact policy is open.



## Standalone ScientificRecord capabilities

A completed standalone RecordingSession should expose a durable **ScientificRecord** or equivalent object representing the captured computational work.

The exact class/API name is not frozen.

Its purpose is to make Recorda useful for reproducibility even when no MOLI project exists.

Conceptually, a standalone record should support capabilities such as:

### Inspect

Determine what was recorded:

    operations
    inputs
    outputs
    Artifacts
    implementations / versions
    environment
    lifecycle / failures
    recording gaps

### Timeline

Reconstruct the chronological order of recorded operations and lifecycle events.

This is a computational recording timeline, not a Nextia Discovery timeline.

### Dependencies / lineage

Follow meaningful operation and data dependencies:

    OP1
      ↓ produces
    MS1
      ↓ consumed_by
    OP2
      ↓ produces
    R1

This should support cross-component records such as MolSysMT → TopoMT.

### Audit

Answer computational provenance questions such as:

    What was executed?
    With which inputs?
    With which parameters?
    With which software/environment?
    In what order?
    What failed or was retried?
    What outputs were produced?

Standalone Recorda audit does not reconstruct scientific rationale that was never recorded by an owning semantic component.

### Verify

Check integrity and availability of recorded inputs, outputs, Artifacts, manifests, and other content-addressed objects where applicable.

### Export

Package or serialize the ScientificRecord for sharing, archival, later inspection, or later import/reference into MOLI.

Large/external Artifacts may remain referenced according to the record/store model.

### Computational replay

Where the recorded operations, inputs, implementations, environments, and resources permit, Recorda may support replay of recorded computational operations.

Conceptually, future APIs might resemble:

    record.inspect()
    record.timeline()
    record.dependencies(...)
    record.audit()
    record.verify()
    record.export(...)
    record.replay(...)

These names are illustrative only.

## Recorda replay versus MOLI replay

The word `replay` has different scope depending on available context.

### Recorda standalone replay

Reproduces **recorded computation**.

For example:

    MolSysMT.convert
        ↓
    TopoMT.detect_pockets
        ↓
    TopoMT.characterize

Recorda can know what operations were executed, their dependencies, inputs, parameters, environment, outputs, and failures.

It does not inherently know why a scientist chose that computational path unless the relevant semantic owner explicitly recorded that information.

### MOLI replay

Reproduces a **recorded scientific project trajectory** using the richer ProjectRecord:

    Decision
        ↓
    ExecutionPlan
        ↓
    computational operations / Runs
        ↓
    Results
        ↓
    recorded project progression

MOLI replay can therefore use Recorda computational provenance as part of a larger trajectory containing Nextia Discovery semantics, Praxis methodology, Sabueso Knowledge dependencies, approvals, and project context.

Thus:

    Recorda standalone
        computational provenance
        +
        computational reproducibility

    MOLI + Recorda
        computational provenance
        +
        scientific provenance
        +
        Discovery trajectory
        +
        project-level replay

> **Recorda replay reproduces recorded computation; MOLI replay reproduces a recorded scientific project trajectory.**

The two should share underlying execution/provenance machinery rather than becoming incompatible replay systems.


## Standalone record import into MOLI

A standalone Recorda record may later become useful inside a MOLI project.

Conceptually:

    standalone Recorda record
            |
            | import / attach / reference
            v
       MOLI ProjectRecord
            |
            v
    Nextia ProjectGraph interpretation

For example, computational Results generated earlier with MolSysMT + TopoMT + Recorda may already have robust execution provenance.

A later MOLI project may reference/import that record, after which Nextia can create project-specific Observations, Evidence, Decisions, or other Discovery semantics without rewriting the original execution history.

Import does not automatically turn standalone Results into Evidence.

The exact import/reference mechanism and trust/integrity validation remain open.

## One recording substrate, different context richness

Standalone Recorda and MOLI-integrated Recorda must not become two incompatible provenance systems.

Conceptually:

    Recorda standalone
        operation
        inputs
        parameters
        environment
        outputs
        dependencies
        lifecycle

    Recorda inside MOLI
        all of the above
            +
        Project
        Campaign / work scope
        ExecutionPlan / Run
        KnowledgeSnapshot references
        Praxis references
        Nextia ProjectGraph mutations
        authorization
        EventLedger
        ProjectRecord

MOLI enriches the context; it does not replace the underlying recording model.


## Instrumentation mechanisms

Recorda should support more than one instrumentation mechanism because not all scientific work has the same shape.

### Decorators

A natural Python mechanism for stable semantic API boundaries:

    @recorda.record(profile="scientific_analysis")
    def detect_pockets(...):
        ...

The decorator may capture invocation metadata before/after execution.

### Context managers

Useful for establishing inherited project/execution scope:

    with recorda.context(...):
        ...

or conceptually:

    with project.run(execution_plan):
        ...

Operations executed inside inherit the active context.

### Explicit recording API

Manual scientific actions, external processes, notebooks, or operations that cannot be cleanly decorated need an explicit API.

The final syntax is open. Decorators are an important convenience mechanism, not the only provenance mechanism.

## Instrument semantic boundaries, not every function

Recorda should not decorate every private helper.

Avoid producing provenance noise for implementation details such as internal string normalization or trivial utility calls.

Prefer instrumentation at semantic boundaries such as:

- knowledge retrieval;
- entity resolution;
- knowledge derivation;
- molecular-system transformation;
- model construction;
- scientific analysis;
- comparison;
- simulation;
- Capability execution;
- Protocol execution;
- Result/Artifact production;
- ProjectGraph mutation;
- manual scientific action;
- communication generation where relevant.

The exact catalog should remain small enough to preserve meaning.

## Recording profiles

Recorda should use **semantic recording profiles**.

A profile answers:

> What kind of operation is this, and what provenance fields/behaviors are expected?

Candidate profiles include:

    knowledge_retrieval
    entity_resolution
    knowledge_derivation

    transformation
    scientific_analysis
    comparison
    simulation

    capability_execution
    protocol_execution

    project_graph_mutation
    decision
    manual_action

    communication

These names are provisional.

Profiles should not be one-per-function. They should describe reusable semantic categories.

### Example: knowledge retrieval

May expect:

- external source;
- query/request;
- source/service version when available;
- retrieval timestamp;
- response/snapshot/hash;
- produced SourceAssertions/objects;
- licensing/retention constraints.

### Example: scientific analysis

May expect:

- scientific inputs/references;
- parameters;
- implementation/version;
- environment;
- random seeds where relevant;
- Results/Artifacts;
- timing/status/failure.

### Example: transformation

May expect:

- input object references;
- transformation identity;
- parameters;
- output object references;
- lineage.

### Example: ProjectGraph mutation

May expect:

- Nextia semantic object type;
- previous graph state/version where relevant;
- created/updated node/relationship;
- actor;
- rationale/approval where semantically required.

The profile does not transfer semantic ownership to Recorda.

## Component detection and explicit ownership metadata

Recorda may automatically detect implementation metadata such as:

    package
    module
    function
    package version
    Git commit

For example, instrumentation inside TopoMT may normally infer that the executing implementation belongs to TopoMT.

However, automatic detection must not be the final authority for semantic ownership.

Prefer the precedence:

    explicit metadata
        ↓
    registered package/component metadata
        ↓
    automatic detection fallback

This allows instrumentation to remain convenient while preserving correctness in wrappers, plugins, delegated execution, tests, or unusual packaging.

## Safe automatic capture of function inputs

Decorators can use Python signatures to bind arguments and capture scientifically relevant invocation state.

For example:

    detect_pockets(
        molecular_system,
        probe_radius=...,
        threshold=...
    )

may record:

    molecular_system:
        stable reference / content identity

    probe_radius:
        value + unit where available

    threshold:
        value

Recorda must not blindly serialize arbitrary Python arguments.

Inputs may include:

- secrets/API keys;
- huge NumPy arrays;
- trajectories;
- file handles;
- GPU/runtime objects;
- callbacks;
- database/service clients;
- objects with sensitive fields.

Recorda therefore requires pluggable **serializers/reference adapters** and **redaction policies**.

Large/persistent scientific objects should normally be represented by stable reference/version/hash rather than bulk serialization.

Secrets must never be persisted merely because they were function arguments.

## Output capture

Instrumentation may observe return values and created objects.

A recorded operation may capture/reference:

- Result objects;
- Artifact objects;
- transformed scientific objects;
- stable references;
- content hashes;
- status;
- exceptions/failures.

The component remains responsible for creating the authoritative domain object. Recorda records its provenance and routing relationships.

## Project context propagation

Recorda should understand the currently active MOLI project scope without requiring every scientific API to add project-specific arguments.

A propagated context may include:

    Project
    Workspace
    Campaign
    Experiment / scientific work unit
    ExecutionPlan
    Run
    actor
    correlation identity
    authorization scope
    record/event destinations

The exact vocabulary must align with final Nextia/project semantics; for example, an `Experiment` object should not be introduced solely by Recorda if Nextia does not define it.

Python `contextvars` or equivalent mechanisms may be appropriate for local propagation, but implementation is open.

## Nested execution and correlation

Scientific operations are frequently nested:

    Campaign
        ↓
    ExecutionPlan
        ↓
    Run
        ├── MolSysMT prepare
        ├── TopoMT detect
        ├── TopoMT characterize
        └── MolSysViewer scene

Nested instrumented operations should inherit project/run/correlation context while preserving their own:

- component;
- operation identity;
- parent operation;
- inputs;
- outputs;
- status.

This can produce a reproducible execution DAG without forcing one component to own all nested operations.

Correlation identity is particularly important for partial failure and distributed execution.

## Semantic routing

Recorda should know **where different parts of a record belong**, based on active context, semantic profile, component ownership, and routing policy.

Routing is distinct from capture.

### TopoMT scientific analysis

Conceptually:

    component = TopoMT
    profile = scientific_analysis
    project = TcTIM
    campaign = C3
    work scope = E7

may route to:

    TopoMT local provenance / authoritative Result
    MOLI EventLedger
    MOLI ProjectRecord
    current Run / correlation scope

It does **not** automatically create Nextia Observation/Evidence.

### Nextia ProjectGraph mutation

Conceptually:

    component = Nextia
    profile = project_graph_mutation

may result in:

    authoritative Nextia ProjectGraph mutation
    EventLedger event
    ProjectRecord provenance

### Sabueso knowledge retrieval

Conceptually:

    component = Sabueso
    profile = knowledge_retrieval

may result in:

    authoritative Sabueso retrieval/SourceAssertions
    EventLedger event
    ProjectRecord provenance

A later Nextia operation may explicitly connect a Sabueso SourceAssertion to project Evidence.

## End-to-end example: execution to Discovery meaning

Consider a TopoMT analysis whose Result is later interpreted inside Nextia.

    TopoMT.detect_pockets(...)
            |
            | Recorda: scientific_analysis
            v
        Result R71
            |
            +--> TopoMT authoritative Result/provenance
            +--> EventLedger: ResultCreated
            +--> ProjectRecord: execution provenance
            |
            v
    human / MOLI Agent interprets R71
            |
            v
    Nextia.add_observation(...)
            |
            | Recorda: project_graph_mutation
            v
        Observation O17
        ProjectGraph v17 -> v18
        EventLedger: ObservationCreated
        ProjectRecord: GraphMutation provenance
            |
            v
    Nextia.add_evidence(...)
            |
            | Recorda: project_graph_mutation
            v
        Evidence E21
        E21 --supports--> H3
        ProjectGraph v18 -> v19
        EventLedger: EvidenceCreated / EvidenceLinked
        ProjectRecord: GraphMutation provenance

The first Recorda record does not infer that R71 supports H3.

The later Recorda records state that **Nextia authoritatively created** O17, E21, and the `supports` relationship. Recorda records those semantic changes because they occurred; Nextia defines and owns their Discovery meaning.

### ProjectGraph mutation provenance

For a consequential Nextia mutation, Recorda should be able to capture/reference, as applicable:

    actor
    Nextia operation
    Project / Campaign / active work scope
    graph version/snapshot before mutation
    created / modified semantic objects
    created / modified typed relationships
    graph version/snapshot after mutation
    explicit rationale where supplied/required
    approval where required
    timestamp
    correlation identity
    referenced upstream objects

For example, Recorda may record that Nextia created:

    Evidence E21
        --supports--> Hypothesis H3

but Recorda does not independently define what `supports` means, decide that the relation should exist, or infer it from R71. Those semantics and validation rules belong to Nextia.

The same principle applies to other ProjectGraph changes:

    Hypothesis rejected
    Hypothesis superseded
    Decision created / approved
    Campaign stopped
    Conclusion created
    Conclusion challenged / superseded
    new Question opened

Recorda should make the evolution of Discovery meaning auditable without becoming the owner or interpreter of that meaning.

## Routing policy must preserve ownership

Recorda is not permission to write arbitrary objects into every destination.

Routing must respect the architecture:

    Sabueso owns Knowledge semantics
    Praxis owns Know-how semantics
    Nextia owns Discovery semantics
    MolSysSuite components own modeling/execution-specific domain outputs
    MOLI owns cross-platform provenance composition

Recorda may coordinate/event-record these actions but must not silently cross semantic ownership boundaries.

## Structured records before human language

Recorda should emit structured records/events, not final human-facing prose.

Avoid making provenance depend on phrases such as:

    "TopoMT identified a pocket..."

Instead record structured facts and references.

Scientific Communication may later transform the same ProjectGraph/ProjectRecord into:

- scientist-facing explanation;
- technical report;
- ProgressBrief;
- audit view;
- slides;
- narrated video.

> **Recording and communication are separate concerns.**

## Operation lifecycle

Instrumentation should preserve lifecycle states and failures, including:

    requested
    accepted
    started
    partial
    completed
    failed
    cancelled
    superseded / abandoned

A decorator/context should record exceptions and failed attempts rather than emitting only successful completion.

Retries remain separate Runs/operations linked through correlation/provenance.

## ExecutionPlan and Run integration

Recorda should integrate naturally with the Architecture 1.0 boundary:

    Decision
        ↓
    ExecutionPlan
        ↓
    Run
        ↓
    Result / Artifact
        ↓
    Observation / Evidence

Within a Run, Recorda can capture the actual API/CLI operations that implement the ExecutionPlan.

This makes replay independent of re-running agent reasoning.

Recorda does not itself decide the scientific Decision or interpret the resulting Evidence.

## Event emission

Recorda may provide the common mechanism through which participating components emit consequential events such as:

    RetrievalStarted
    RetrievalCompleted
    SourceAssertionCreated

    RunStarted
    RunCompleted
    RunFailed

    ResultCreated
    ArtifactCreated

    ObservationCreated
    EvidenceLinked
    DecisionApproved

Event names/schema remain open and should be governed centrally enough to avoid incompatible vocabularies.

Events should reference authoritative objects rather than duplicate their complete content.

## Operation outside a MOLI project

MOLI must not become a mandatory gateway to component APIs.

For example:

    topomt.detect_pockets(system)

should remain scientifically usable outside an active MOLI Workspace.

Possible behavior:

    no active MOLI project
        ↓
    function executes normally
        ↓
    optional local provenance / no project routing

versus:

    active MOLI project context
        ↓
    same function executes
        +
    project provenance/events automatically captured

> **Instrumentation must not make MOLI a mandatory gateway to component APIs.**

## Manual actions

Not all scientific work is a decorated Python call.

Recorda should support explicit recording of:

- manual inspection;
- manual curation;
- manual selection/exclusion;
- human approval;
- external GUI/CLI work;
- imported experimental results.

Manual records must preserve actor, timestamp, referenced objects, rationale/context, and relevant outputs/relationships.

## Notebooks

Phase 1 notebooks are a primary environment in which Recorda should prove useful.

A notebook should be able to call normal Sabueso/Praxis/Nextia/MolSysSuite APIs while Recorda captures the underlying scientifically meaningful operations.

The notebook remains a human-readable orchestration document; Recorda helps ensure it is not the only provenance record.

## Profiles and routing are configuration, not prose

Recorda may maintain centrally governed profile definitions and routing rules.

These definitions should specify:

- expected semantic fields;
- capture behavior;
- serializer/reference behavior;
- redaction;
- event type(s);
- allowed/required destinations;
- ownership constraints;
- lifecycle behavior.

Human-facing phrases belong to Scientific Communication templates/renderers, not Recorda recording profiles.

## Extensibility

A future component such as a quantum-chemistry package should be able to participate by:

1. registering component identity/ownership metadata;
2. satisfying the MOLI Provenance Contract;
3. instrumenting its semantic boundaries;
4. using common profiles or defining governed extensions;
5. emitting references/events into active project context.

MOLI should not need intimate knowledge of the component's internal storage implementation.

## Minimal first experiment

Do not implement all Recorda capabilities before testing the design.

Sabueso is a good first proving ground.

For example, instrument one real knowledge-retrieval boundary and one entity-resolution boundary.

The experiment should test whether Recorda can capture:

- component/function/version;
- active project context;
- input references/parameters;
- external source/query;
- retrieval time;
- response hash/snapshot reference;
- produced authoritative Sabueso objects;
- status/failure;
- EventLedger routing;
- ProjectRecord linkage;
- secret redaction.

Then use the TcTIM Phase 1 notebook to expose missing semantics.

A similar later experiment in TopoMT should test scientific-analysis capture, nested MolSysSuite execution, Results/Artifacts, and Run correlation.





## Scoped ProjectRecord views

Project context and correlation metadata should make it possible to reconstruct the complete record associated with a meaningful scientific scope without requiring each component to know how that record will later be presented.

Conceptually, MOLI should be able to derive views such as:

    ProjectRecord for Project
    ProjectRecord for Campaign
    ProjectRecord for Run
    ProjectRecord for ExecutionPlan
    ProjectRecord for an active scientific work scope

If Nextia eventually defines an `Experiment` or equivalent semantic object, the same mechanism may provide an experiment-scoped record. Recorda must not invent that Discovery concept solely for reporting convenience.

A scoped record may cross component boundaries:

    work scope E7
        |
        +-- MolSysMT
        |     prepare(...)
        |
        +-- TopoMT
        |     detect_pockets(...)
        |     characterize(...)
        |
        +-- MolSysViewer
        |     create_scene(...)
        |
        +-- Nextia
              Observation O17
              Evidence E21

This is possible because the relevant operations/objects carry sufficient project scope, parent/correlation identity, and stable references.

Conceptually, future APIs might resemble:

    project.record.for_campaign(C1)
    project.record.for_run(R2)
    project.record.for_scope(E7)

The exact API is not frozen.

### Scoped record is not a report

Recorda does not generate a human-facing report merely because it can reconstruct a scoped record.

The separation is:

    Recorda + ProjectContext
            ↓
    scope/correlation-aware records
            ↓
    Scoped ProjectRecord view
            ↓
    Scientific Communication / Audit / Trace
            ↓
    optional human-facing view

Possible future renderings might include a Campaign report, Run report, experiment/work-scope report, Protocol-execution report, or audit view.

Those are communication/view concerns, not new Recorda semantic ownership.

> **Recorda should preserve enough scope and correlation metadata that MOLI can reconstruct the complete cross-component record of a meaningful scientific work unit after the fact.**


## Routing is resolved from context, not hard-coded destinations

Instrumentation should not normally encode project-specific destinations inside decorators.

Prefer the separation:

    recording profile
        says WHAT kind of operation is being recorded

    active ProjectContext
        says WHERE in the current project scope it belongs

    ownership / routing policy
        says WHAT Recorda may record, reference, or route

For example, avoid coupling a reusable TopoMT function to a specific project path such as:

    @recorda.record(destination="TcTIM/C3/E7")

The same instrumented function should be reusable in another project without modification.

Project/campaign/run/work-scope destinations are resolved from propagated context and Workspace configuration.

Explicit destination overrides may exist for exceptional cases, but should not become the normal integration mechanism.

## Operation identity versus scientific-object identity

A recorded operation has an identity independent of the scientific objects it may create.

For example:

    Operation OP17
        TopoMT.detect_pockets(...)
        status = failed

        Result = none

The failed operation remains part of provenance even though no Result exists.

Likewise, nested execution may contain:

    Run R1
        ├── Operation OP1 — MolSysMT.prepare
        ├── Operation OP2 — TopoMT.detect
        └── Operation OP3 — MolSysViewer.scene

Each operation may reference parent operation, Run, ExecutionPlan, correlation identity, inputs, outputs, lifecycle, and implementation metadata.

Scientific objects such as Result R71 or Artifact A12 retain their own component-owned identities.

> **Operation identity records that an action occurred or was attempted; scientific-object identity records the domain objects created or referenced by that action.**

## Semantic consumption provenance

Reproducibility and audit may require recording not only what an operation created, but also which existing scientific objects it **meaningfully consumed**.

This must not become instrumentation of every Python read/access.

Record semantic consumption when an object's use materially contributes to a consequential scientific operation, decision, interpretation, context assembly, or generated output.

Examples include a Decision or AgentAction consuming:

    KnowledgeSnapshot KS7
    Evidence E3
    Evidence E4
    Protocol P2
    Result R19

or a Scientific Communication operation consuming a particular ProjectStateSnapshot and Conclusions.

This is especially important for reconstructing ContextAssembly:

    what information was available
        ↓
    what subset was selected
        ↓
    what consequential operation consumed it

Consumption references should preserve stable object/version/snapshot identity where appropriate.

> **Recorda records meaningful scientific dependencies, not incidental implementation-level reads.**

## Recording reliability policy

Not every provenance event has the same tolerance for recording failure.

Recorda should support a governed reliability policy, conceptually including at least:

### Strict recording

The consequential operation must not be considered committed/successful if required provenance cannot be durably recorded.

Likely candidates include operations such as:

    DecisionApproved
    ProjectGraph mutation
    ProjectRelease
    irreversible/external consequential action

The exact catalog is policy-driven and not frozen here.

### Best-effort / buffered recording

The scientific operation may proceed when immediate provenance persistence is temporarily unavailable, provided Recorda can safely buffer and later reconcile the record.

Potential examples include selected local/HPC execution telemetry where blocking the scientific calculation would be disproportionate.

Buffered records must preserve ordering/correlation/integrity sufficiently for reconciliation, and the ProjectRecord must expose unresolved provenance gaps rather than silently treating them as complete.

### Policy resolution

Recording reliability may depend on:

    profile
    operation type
    active project policy
    authorization
    destination availability
    deployment mode

The decorator should not independently decide whether an operation is strict.

> **A provenance failure must never be silently indistinguishable from successful complete recording.**


## What Recorda should not become

Recorda should not become:

- a scientific reasoning agent;
- a replacement for Nextia;
- a generic logging framework with no scientific semantics;
- a shared mutable scientific megastore;
- the owner of Sabueso/Praxis/Nextia/MolSysSuite objects;
- a report-writing system;
- a requirement that all component APIs be invoked through MOLI;
- a mechanism that serializes every argument indiscriminately;
- instrumentation on every internal helper function.

## Open implementation questions

Before freezing an API/package, Phase 1 pilots should help determine:

- package/repository boundary: lightweight independent `recorda`, MOLI-embedded infrastructure, `moli-recorda`, or another distribution;
- standalone recording schema and persistence backend;
- RecordingSession lifecycle and crash/interruption recovery;
- inactive/no-recorder overhead;
- standalone record import/reference into MOLI and integrity/trust validation;
- pause/resume semantics and strict-policy restrictions;
- decorator/context-manager/explicit API balance;
- exact profile catalog;
- component registration/discovery;
- context propagation across processes/jobs/remote execution;
- event schema/versioning;
- serializer/reference adapter protocol;
- secret/sensitive-data redaction;
- routing configuration and authorization;
- integration with ExecutionPlan/Run;
- integration with notebooks;
- async/distributed/nested execution;
- performance/overhead;
- failure behavior when provenance storage is temporarily unavailable;
- strict versus best-effort recording policy and which semantic operations require each;
- buffering, ordering, integrity, and reconciliation of offline/distributed records;
- testing strategy for provenance completeness.

## Guiding principles

> **Components own meaning; Recorda records consequential operations and semantic changes.**

> **Nextia owns Discovery meaning; Recorda records the provenance and evolution of that meaning in the ProjectGraph.**

> **Capture and routing are distinct: profiles describe semantic operation types; routing decides where records/events belong under current project context and ownership rules.**

> **Prefer stable references over bulk serialization of scientific objects.**

> **Instrumentation should be low-friction but never silently violate semantic ownership, authorization, or confidentiality.**

> **Recorda should make provenance easier to do correctly than to omit, while keeping component APIs independently usable outside MOLI.**

> **Recorda is useful standalone for reproducible scientific computation; MOLI enriches the same recording substrate with project and Discovery context.**

> **A standalone ScientificRecord should be independently inspectable, auditable, verifiable, exportable, and computationally replayable where the recorded environment permits.**

> **Recorda replay reproduces recorded computation; MOLI replay reproduces a recorded scientific project trajectory.**

> **Instrumented component APIs remain normal standalone APIs when no recording context is active.**

> **Start/stop, context-manager recording, and MOLI-managed activation are interfaces to the same underlying RecordingSession concept.**

> **Recording gaps, interruption, pause, and provenance failure must be explicit rather than silently disappearing from the record.**

> **Structured records come before human-readable reporting.**

> **Profiles describe what is recorded; active context and ownership/routing policy determine where it belongs.**

> **Operation identity is distinct from the identities of scientific objects produced or consumed by the operation.**

> **Record meaningful scientific consumption/dependencies, not incidental implementation reads.**

> **Recording reliability is policy-driven; provenance failure must never masquerade as a complete successful record.**

> **Scope and correlation metadata must be sufficient to derive complete cross-component ProjectRecord views for meaningful scientific work units without coupling component code to future report formats.**
