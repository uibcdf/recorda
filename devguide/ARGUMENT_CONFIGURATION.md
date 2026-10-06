# ArgDigest capture configuration — experimental source integration

Owned by [uibcdf/recorda#17](https://github.com/uibcdf/recorda/issues/17), under
the ecosystem review `uibcdf/recorda#2`.

The explicit factory `recorda.integrations.argdigest.capture_policy` uses
ArgDigest to validate Recorda-owned configuration and returns an ordinary frozen
`recorda.CapturePolicy`. Scientific function arguments, defaults, native objects
and errors remain owned by their scientific provider.

## Explicit use and contracts

```python
import recorda
from recorda.integrations.argdigest import capture_policy

policy = capture_policy(
    ["scientific_analysis", "scientific_workflow"],
    inputs=False,
    outputs=False,
)
handle = recorda.start("analysis", path="analysis.jsonl", capture_policy=policy)
# Execute declared semantic boundaries and stop using the ordinary session API.
result = handle.stop()
```

The factory's closed signature accepts `profiles` positionally or by keyword and
four keyword-only detail switches. It exposes no `skip_digestion` parameter or
arbitrary keywords. This supplies the function-contract axis. The registered
`recorda.capture` pipelines supply the value-contract axis:

- Profiles accept `None` or an exact built-in list, tuple, set or frozenset.
  `None` selects all declared profiles; an empty collection selects none.
- The input collection contains at most 64 entries, before deduplication. Each
  entry is an exact nonempty string of at most 256 characters. The output is a
  copied, sorted tuple of unique labels.
- All detail switches require exact booleans; no truth-value coercion occurs.

Pipelines share the core's validators and preserve their fixed `TypeError` and
`ValueError` refusals. Direct `CapturePolicy` construction keeps those same
mandatory checks. Even an internal bypass or unwrapping cannot admit an invalid
core policy. Session capture, redaction, schema, path and lifecycle guards remain
enforced by Recorda. Scientific targets are never decorated with ArgDigest here.

The adapter explicitly selects `argument_digestion=False`: this disables digester
discovery while retaining binding, the closed function contract and pipelines.
An explicit `DigestConfig` prevents application defaults or `ARGDIGEST_CONFIG`
from rewriting Recorda's configuration. Pipelines use direct registered callables,
so another consumer replacing a registry name does not change this factory.

## Diagnostic and dependency boundary

Provider imports, registration and decorator construction run within SMonitor's
metadata-only scope. The decorated helper requests that same restrictive policy
for every invocation. Validation does not inspect opaque repr, str or iterators;
diagnostics omit values, native error text and inherited producer context.
Application level, profile and handlers remain selected by the application.
This cannot undo diagnostics produced independently by enclosing scientific code.

An absent or older provider fails on explicit adapter import, before caller
configuration values reach digestion. Ordinary `import recorda`, direct core
policy construction, recording and independent reading import none of ArgDigest,
DepDigest or SMonitor. No dependency extra or supported published floor has been
selected. There is no automatic optional-backend loader to which DepDigest must
be added; ArgDigest itself retains its provider-owned DepDigest integration.
Basic configuration neither imports nor requires NumPy, Pint or PyUnitWizard.

## Qualification and remaining work

On 2026-10-06, the latest checked published ArgDigest 0.14.0 and SMonitor 0.18.0
lack the required APIs from `uibcdf/argdigest#29` / #30 and
`uibcdf/smonitor#37` / #38. The controlled development route uses:

| Provider | Qualified route |
| --- | --- |
| ArgDigest | source `5e7925ddcd14922d00647d39b6a97eed2499bc23` |
| SMonitor | source `6feac9728cc35d57cbc92f284d7040d7f04cb35b` |
| DepDigest | published Conda 0.13.0, `uibcdf` with `conda-forge` |

The separate CI lane provisions the published DepDigest closure with Conda and
tests installed Recorda using both exact source commits on Linux Python
3.11–3.14. The SMonitor-only and ordinary installed-core lanes remain available.
All lanes use published pytest-receptor 1.1.0. Local Python 3.14 qualification:

```bash
RECORDA_TEST_ARGDIGEST=1 RECORDA_TEST_SMONITOR=1 \
PYTHONDONTWRITEBYTECODE=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=/path/to/pinned/argdigest:/path/to/pinned/smonitor \
python -m pytest -p pytest_receptor.plugin --receptor=llm
```

The receiving tests cover accepted forms, bounds before deduplication, copying,
exact booleans, native refusals, opaque values, public bypass rejection, diagnostic
delivery faults, application configuration, inherited telemetry, native calls,
mandatory recorded facts, disabled adapters, import isolation and older providers.
Executed evidence is in
[evidence/argument_configuration_local.json](evidence/argument_configuration_local.json).
Local source and installed-Recorda suites pass **158 tests** on Python 3.14.7;
the baseline passes 104 with 54 explicit provider skips. Code/test commit
`4ad2531b84373f83a81ca69d0861ce2e106fefc0` passes
[all 15 hosted jobs](https://github.com/uibcdf/recorda/actions/runs/37505815276),
including the four installed-Recorda ArgDigest lanes on Linux Python 3.11–3.14.
Published gh-run-receptor 1.2.0 inspected that completed run. The resolved analysis
is in [archive/argument_configuration_source.md](archive/argument_configuration_source.md).

This factory is an opt-in experiment, not default-core ArgDigest adoption or a
public-provider qualification. The wider review remains partial. Select and
qualify published artifacts before changing dependency metadata or replacing
default normalization; review reference-check options as their own slice in
`uibcdf/recorda#2`. Distribution remains `uibcdf/recorda#3`.
