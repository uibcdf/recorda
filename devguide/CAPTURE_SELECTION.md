# Standalone capture selection

Tracked by `uibcdf/recorda#11` and `uibcdf/recorda-lab#8`. This is a bounded
experimental session policy. Semantic profiles remain category labels; it does
not define MOLI profiles, routing, authority or reliability policies.

```python
policy = recorda.CapturePolicy(
    profiles=["scientific_workflow", "scientific_analysis"],
    inputs=False,
    parameters=False,
    outputs=False,
    exception_references=False,
)
handle = recorda.start("analysis", path="analysis.jsonl", capture_policy=policy)
result = analyze(samples)
record = handle.stop()
```

Libraries keep their normal decorated calls and native results. Configuration is
chosen once by the caller. A policy is frozen and copies its profile collection;
all four detail switches require actual booleans. The provisional public argument
is available on start, session and RecordingSession.

## Mandatory and selectable facts

Every selected operation retains id, declared name/profile, nearest recorded
parent, implementation metadata, timestamps and start/outcome. A selected failure
retains safe exception type and the existing omitted-message marker. A missing
outcome remains incomplete. These facts cannot be disabled by CapturePolicy.

Inputs, parameters, outputs and native exception references are independently
selectable groups. Disabled groups do not run their adapters. No input signature
binding is performed solely for capture when inputs are disabled. Empty payload
dictionaries then mean intentional policy omission, recorded explicitly in the
operation's capture metadata as omitted_by_policy. Disabled exception references
use an omitted value with reason capture_policy. Enabled groups keep the existing
bounded capture, secret-name redaction and exact-type native adapters.

The minimal laboratory policy removes native input/output references. It records
execution identity and status but loses scientific dependency information. The
full policy preserves those references without retaining native bytes itself.
Choose detail according to the questions the record must answer; small journals
alone do not establish adequate scientific provenance or replayability.

## Selection, coverage and lifecycle

profiles=None selects all declared categories, including unlabelled boundaries.
A collection selects only those labels; an empty collection selects none. No
per-function catalog or superclass/profile inheritance is inferred. Omitting the
capture_policy argument retains the prior journal shape and capture behavior.

Excluded decorators bypass capture, binding and implementation lookup. Excluded
explicit boundaries also avoid payload adapters; their output calls are discarded.
Both execute normally and preserve native returns and exceptions. Their failures
are unobserved unless they propagate through a selected enclosing operation.
Session success describes selected outcomes, not every scientific call.

The durable session start states configuration and known gaps. At invocation,
exclusions increment aggregate counts, without a journal event per excluded call.
A final session marker stores up to 64 profile counts and an other_calls overflow
count. These are invoked-boundary counts, not completed or successful calls.
Before a complete final marker is present, excluded_boundaries is None (unknown),
including after interruption or a failed pre-line finalization. A zero count is
not substituted for missing evidence. Uninstrumented calls are never counted.

A selected descendant of excluded code uses its nearest selected ancestor. The
record does not manufacture a parent operation for excluded work. Only selected
execution participates in the recorded-running-work stop barrier; excluded async
work is unobserved and is not joined by stop. Callers remain responsible for
awaiting their scientific tasks. Owner-context checks and persistence failures
for selected operations are unchanged. Excluded calls may continue when the
writer is broken; selected calls still fail before target execution.

## Compatibility and evidence

The optional coverage/capture metadata is additive in recorda.journal/0.1.
Historical journals remain readable. Inspection needs Recorda and stdlib, without
the producing library. This is source work after 0.2.0, without a new release tag.

The laboratory runner run_selection.py and fifth notebook compare exactly the
same population statistics (mean 2.5, variance 1.25) with minimal/detailed sessions.
They preserve native files and journals and measure actual bytes, events, fsync,
adapter calls and wall/CPU time. Timings include activation, execution, stop and
inspection, in fixed minimal/detailed order; no speed-ratio threshold is asserted.
See evidence/capture_selection_local.json for the qualified sources and commands.
