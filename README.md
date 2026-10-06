# Recorda

**Scientific recording and provenance for reproducible computational work.**

Recorda is a lightweight recording layer for scientific software. Activate a session
once, call instrumented scientific functions normally, and stop recording. Library
authors add a decorator at selected semantic boundaries; the function body and its
scientific return value retain their normal behavior.

The current experimental recommended usage is:

```python
import recorda


@recorda.record("example.double", profile="scientific_analysis")
def double(value):
    return value * 2


session = recorda.start("analysis", path="analysis.jsonl")
result = double(3)
record = recorda.stop()  # Or session.stop(), in the activating context.
```

This is implemented prototype syntax, not a published stable API. Without an active
session the same function executes directly. Starting a session observes declared
instrumented boundaries; coverage and omissions remain explicit. A missing stop leaves
an inspectable incomplete session. For bounded scripts, the context manager remains
an optional interface to the same session lifecycle.

Existing scientific results and native provenance remain owned by their libraries. Recorda can reference them without replacing or copying them. Inside MOLI, the same substrate may later be enriched with ProjectContext, ExecutionPlan/Run, component references, Nextia ProjectGraph mutations, EventLedger, authorization, and ProjectRecord routing.

## Status

Version **0.2.0** is the experimental source checkpoint for native exception
references ([uibcdf/recorda#9](https://github.com/uibcdf/recorda/issues/9)). Package metadata,
runtime version and the Git tag use the same identity. Version `0.1.0` remains the
historical first checkpoint. See [the changelog](CHANGELOG.md). Distribution and public OS
qualification remain open in [uibcdf/recorda#3](https://github.com/uibcdf/recorda/issues/3)
and [uibcdf/recorda#4](https://github.com/uibcdf/recorda/issues/4).

Recorda now has an **experimental first standalone implementation**. Its API and journal
schema are provisional. The controlled laboratory lives in `uibcdf/recorda-lab`;
laboratory evidence does not establish real scientific utility or complete workflow capture.

See [`devguide/DESIGN.md`](devguide/DESIGN.md) for the broad design and [`devguide/FIRST_SLICE.md`](devguide/FIRST_SLICE.md) for the first experiment ([Recorda #1](https://github.com/uibcdf/recorda/issues/1)).

## Capture and complementary interfaces

Create the declared development environment, then install this unreleased checkout with
`python -m pip install --no-deps --editable .`. For an unmodified external library,
the caller can explicitly wrap an operation:

```python
import recorda

with recorda.session("analysis", path="analysis.jsonl", gaps=["unwrapped calls"]) as session:
    with session.operation("external_library.analyze", inputs={"model": model_ref}) as operation:
        result = external_library.analyze(model, settings)
        operation.output("result", result_ref)

record = recorda.inspect("analysis.jsonl")
```

Supply safe `recorda.Reference(owner=..., identifier=..., revision=..., digest=...)`
objects or bounded ordinary scalars. Existing journal paths are never overwritten.
`python -m recorda analysis.jsonl` inspects a journal without its producing library.
`@recorda.record("operation.name")` is the opt-in function boundary; inactive calls
bypass capture. Session activation alone observes no arbitrary calls.

Capture configuration uses published ArgDigest 0.15.0 and SMonitor 0.19.0 by
default. Recovery diagnostics remain explicitly selected. Provision the declared
Conda environment before installing this checkout; see
[environment routes](devtools/conda-envs/README.md),
[recovery diagnostics](devguide/RECOVERY_DIAGNOSTICS.md) and
[argument configuration](devguide/ARGUMENT_CONFIGURATION.md).
The providers are required installation dependencies, loaded at configuration use.
Importing Recorda and reading a saved journal keep independent, light imports.

Session-local `reference_adapters={NativeResult: adapter}` lets decorated calls
capture references without adding recording statements inside scientific functions.
An adapter matches an exact declared type and returns `Reference` or `Omitted`.
Scientific inputs/results stay owned by their producer. Adapter failures or invalid
returns produce explicit omissions; credential-named fields are omitted before any
adapter runs. Configuration is copied at session creation. Adapter callbacks are
trusted integration code and must themselves avoid secrets and scientific side effects.

Version 0.2.0 also accepts exact exception types in that mapping.
Their adapter supplies a safe native trace reference under `exception.reference`
on the failed operation. It preserves the original exception; unsupported errors and
adapter faults produce explicit omissions without capturing exception messages or repr.
See [`native exception references`](devguide/ACTIVATION.md#native-exception-references).

`profile=` currently records a semantic label; it does not implement the broad
profile catalog, filtering, routing or reliability-policy engine described in the design.
See [`devguide/ACTIVATION.md`](devguide/ACTIVATION.md) for lifecycle and ownership rules.
The laboratory's `experiments/run_activation.py` exercises the recommended usage;
`experiments/run_slice.py` retains the explicit-boundary experiment.
The laboratory also keeps usage notebooks in `notebooks/`, a real-kernel cell/fault
runner and a repeated performance runner. See
[`local notebook/performance evidence`](devguide/evidence/notebook_performance_local.json)
for the qualified environment; broader notebook and real-library claims remain open.
The controlled SciPy fitting trial retains a failed attempt/retry, native arrays,
solver/model references and a runnable scientific notebook. Its local qualification
is indexed in [`SciPy trial evidence`](devguide/evidence/scipy_local.json).

The local JSONL writer fsyncs operation starts before executing the target. Exceptions,
recording faults and hard process exits remain failed or incomplete. This is a single-process
local experiment, not distributed durability, tamper-proof integrity or replay.
Secrets named as credentials and unsupported objects are explicitly omitted. Caller-supplied
labels, references and ordinary strings must already be safe; name-based redaction cannot
recognize every secret in arbitrary text. Exception messages are omitted by default.

Recorda is directly governed by MOLI, with no MOLI runtime dependency. Read
`MOLI_GUIDE.md`, `AGENTS.md` and `devguide/ENGINEERING_REVIEW.md`.
Python 3.11–3.14 is the current target; development uses Python 3.14. Public OS support
and distribution remain unqualified. See [the tracked Python transition](devguide/PYTHON_SUPPORT.md).

The broad direction remains:

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

MIT. See [`LICENSE`](LICENSE). No public package distribution or archival claim is made yet.
