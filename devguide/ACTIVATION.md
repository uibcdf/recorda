# Activation and native-reference experiment

Tracked by `uibcdf/recorda#1` and `uibcdf/recorda-lab#1`. This implements the original
design's primary start/stop interface and dormant semantic decorators. API/schema
remain provisional; local results do not qualify publication or public OS support.

## Recommended library usage

```python
import recorda


@recorda.record("analysis", profile="scientific_analysis")
def analyze(value):
    return value * 2


session = recorda.start("my_analysis", path="my_analysis.jsonl")
result = analyze(3)
record = recorda.stop()
```

The caller or platform activates the session; a scientific library instruments its
selected operations. Calls retain their signature, return object and target exceptions.
Inactive decorators bypass argument binding and capture. Activate once across ordinary
calls; the prototype records only instrumented or explicitly declared boundaries.

`recorda.start()` returns the owning `RecordingSession`. `recorda.stop()` and
`session.stop()` finalize it and return `ScientificRecord`. A handle can alternatively
be created with `recorda.session(...)` or `RecordingSession(...)`, then started with
`session.start()`. Existing journal paths are never overwritten; sessions are single-use.

## Context and lifecycle boundaries

- A second manual start in an active context raises before creating another journal.
- Manual stop with running recorded operations raises and leaves the session active;
  wait for completion and retry. This includes operations in inherited async tasks.
- Finalization must occur in the context that activated the session. An inherited
  task or copied context cannot close its owner's journal, even while it is idle.
- An optional nested context-managed session restores the previous session on exit.
  Its owner cannot manually close the outer session while the inner one is active.
- Stop without an active session, repeated stop and reopening a used session raise.
- A failed decorated call is re-raised and leaves failure in the active session.
  Catching the exception does not erase it; stopping afterwards yields a failed record.
- Without stop, durable starts and outcomes remain inspectable, but session status is
  incomplete. Neither normal process exit nor an exit hook manufactures successful closure.
- Completion persistence errors propagate and detach/close the journal so a new session
  can start. Inspect the stored prefix; do not assume completion was persisted.

Context activation is local. New processes/threads need an explicit future propagation
contract. Async work must finish before its owner stops the session. This experiment
qualifies separate-cell activation on Linux Python 3.14.7 with IPykernel 7.3.0 and
jupyter-client 8.10.0. The laboratory checks top-level await, child ownership,
uncaught failure, SIGINT and kernel loss. Browser frontends and other kernel/context
implementations need their own qualification; this is not universal notebook support.

The context manager remains useful for bounded scripts and exception cleanup:

```python
with recorda.session("bounded", path="bounded.jsonl"):
    result = analyze(3)
```

It uses the same lifecycle and preserves the target exception. A manual interface
does not wrap arbitrary caller code: an error outside an instrumented operation is
not observed automatically. Finalize explicitly when appropriate, or inspect the
unclosed record as incomplete after interruption. Choose one finalization interface;
do not manually stop inside a context-managed session.

## Reference adapters and semantic labels

Configure known domain types once on the session:

```python
recorda.start(
    "native_results",
    path="native_results.jsonl",
    reference_adapters={NativeResult: native_result_reference},
)
```

The producer can supply its mapping and adapter functions from an integration module.
The experimental laboratory keeps these in `experiments/consumer.py`, separate from
the independent dummy library. There is no process-global adapter registry in this slice.

Adapters match exact types and return `recorda.Reference` or `recorda.Omitted`. They
apply to declared inputs, parameters and outputs; implementation metadata retains
ordinary bounded capture. Existing scalar limits and reference validation remain.
Sensitive named fields are omitted before adapter invocation. Unregistered types
are omitted without inspecting them. Callback exceptions and invalid returns become
explicit omissions without persisting callback error text or replacing the native return.

Callbacks are trusted integration code. They must provide safe identities and avoid
changing scientific objects or performing scientific work. Reference capture does
not preserve or resolve source bytes; the owner retains the native result/file.

## Native exception references

The 0.2.0 extension tracked by `uibcdf/recorda#7` uses the same exact-type mapping:

```python
recorda.start(
    "source_analysis",
    path="source_analysis.jsonl",
    reference_adapters={NativeSourceError: retain_native_failure_reference},
)
```

The trusted producer adapter receives the original exception and returns `Reference`
or `Omitted`. It may retain an existing native trace using the producer's supported
serialization; Recorda writes only the safe reference under `exception.reference`
on the failed operation. Scientific code and the caller's normal error handling need
no new recording statements. Explicit boundaries, synchronous decorators and async
decorators share this behavior. An adapter is not invoked for inactive instrumentation
or unregistered exception subclasses. No superclass fallback is inferred.

Without an exact registration, the reference is explicitly omitted as
`unsupported_type`. Invalid adapter results, explicit omission and callback failures
have the same bounded omission reasons as other reference capture. Even a
`BaseException` raised inside this exception-capture callback becomes an omission
so it cannot replace the native error already propagating. This containment is
specific to failure capture; it does not change normal input/output interrupt behavior.

The original error, cause and traceback propagate. Its message, repr, dictionary,
cause text and traceback content are not persisted. Callbacks remain trusted code:
they must avoid scientific mutation and unsafe identities. Storage failure is still
visible as incomplete recording; this extension does not implement a reliability
policy, exception-group traversal or retention/replay guarantee. Historical journals
without `exception.reference` remain readable. The additive field stays in the
provisional `recorda.journal/0.1` schema.

The Sabueso adoption is tracked by `uibcdf/recorda-lab#6`. Its exact ConnectorError
adapter retains the native acquisition trace and its inspector reads the reference
from the failed operation, while still accepting historical caller-owned indices.

`profile=` is a bounded semantic label on an operation, supported by decorators and
explicit operations. It is stored and exposed by inspection. It does not yet select
fields, filter events, route records or resolve strict/buffered policy. Readers accept
older prototype operations without a profile and expose `None` for that field.

## Evidence

Run core tests with the published receptor and the controlled `run_activation.py`
experiment. Check normal calls before/after activation, several decorated calls in one
session, native references, nested parents, actual dummy failure, hard exit and omissions.
Preserve results and fingerprints in `evidence/`. Recorda Lab's `notebooks/` keeps
runnable usage simulations; `run_examples.py` executes their cells in real kernels.
`run_notebook.py` owns the disposable-kernel fault checks and `run_performance.py`
retains raw wall/CPU timings with unchanged synchronous persistence. See
`evidence/notebook_performance_local.json` and the laboratory's
`devguide/NOTEBOOK_AND_PERFORMANCE.md`. A real external scientific library,
real-workload performance and richer MOLI activation remain follow-ons.
