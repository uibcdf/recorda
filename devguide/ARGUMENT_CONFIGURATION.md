# Default ArgDigest capture configuration

Owned by [uibcdf/recorda#19](https://github.com/uibcdf/recorda/issues/19), under
the ecosystem review `uibcdf/recorda#2`. The earlier explicit experiment and
published-provider qualification remain archived under #17 / #18.

Ordinary `recorda.CapturePolicy` construction now uses ArgDigest. Scientific
function arguments, defaults, native objects and errors remain owned by their
scientific provider. The inactive scientific call path performs no digestion.

```python
import recorda

policy = recorda.CapturePolicy(
    ["scientific_analysis", "scientific_workflow"],
    inputs=False,
    outputs=False,
)
handle = recorda.start("analysis", path="analysis.jsonl", capture_policy=policy)
# Execute declared semantic boundaries using the ordinary API.
result = handle.stop()
```

## Both argument contracts

The existing closed dataclass constructor signature supplies the function
contract; positional/keyword compatibility is preserved. There is no public
`skip_digestion` or arbitrary keyword route. Registered `recorda.capture`
pipelines supply the value contract:

- Profiles accept `None` or an exact built-in list, tuple, set or frozenset.
  `None` selects all declared profiles; an empty collection selects none.
- At most 64 input entries are accepted before deduplication. Every entry is an
  exact nonempty string of at most 256 characters. The copied result is a sorted
  tuple of unique labels.
- Detail switches require exact booleans; values are never truth-value coerced.

Shared validators preserve the fixed native `TypeError`/`ValueError` refusals.
The private normalization body's checks and final policy guards remain mandatory
even when that private helper is unwrapped. Capture, redaction, schema, filesystem
and lifecycle invariants remain in the core. The old explicit
`recorda.integrations.argdigest.capture_policy` factory delegates to this same
constructor and retains its keyword-only switch signature for compatibility.

Explicit `argument_digestion=False` disables global digester discovery while
keeping binding and value pipelines active. A local `DigestConfig` isolates
application defaults and `ARGDIGEST_CONFIG`. Direct registered rule callables
prevent another consumer's registry replacement from rewriting this contract.

## Lazy imports and diagnostic authority

Argument providers load at configuration use, including the default policy
created when recording starts. Plain `import recorda`, independent journal
inspection and today's reference byte checks load none of ArgDigest, DepDigest
or SMonitor. That import property does not make those declared installation
dependencies optional, and there is no silent validation fallback if missing.

Provider bootstrap, registration and decorator construction run within
SMonitor's metadata-only scope; every validation invocation requests the same
restriction. Opaque repr, str and arbitrary iterators are never consulted.
Diagnostic payloads omit configuration values, native error text and inherited
producer context. No scientific target is wrapped in ArgDigest or SMonitor here.

Before importing ArgDigest, Recorda uses public `ensure_configured` for its own
provider. When neither application nor project policy is selected, Recorda's
safe first-use baseline disables global logging, warning and exception capture.
An existing application/project configuration wins; no level, profile, handler
or capture setting is overwritten. The explicit recovery adapter still registers
declarations only and activates recovery events only when selected. Configuration
validation does not turn scientific calls into automatic diagnostic boundaries.

## Dependency and qualification route

Required metadata now declares ArgDigest `>=0.15.0,<0.16` and SMonitor
`>=0.19.0,<0.20`. The stricter SMonitor floor is needed for restrictive capture
even though ArgDigest's general provider floor remains older. ArgDigest owns its
DepDigest dependency use; no Recorda-owned optional/backend loader is introduced.
Basic configuration requires no NumPy, Pint or PyUnitWizard.

All development/test Conda routes provide published ArgDigest 0.15.0 build 0,
SMonitor 0.19.0 build 1 and DepDigest 0.13.0 build 0 from `uibcdf` with
`conda-forge`. Install this unpublished checkout with
`python -m pip install --no-deps --editable .` after provisioning the environment.
The local noarch recipe expresses the required closure but is not a qualified
public release candidate. The route inventory and read-only preflight detect
missing/stale constraints and unreviewed CI/source routes before package builds.

Use Python 3.14 and published pytest-receptor 1.1.0 locally:

```bash
python devtools/check_dependencies.py
python devtools/verify_support_environment.py argdigest
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest -p pytest_receptor.plugin --receptor=llm
```

Default ArgDigest regressions run in every installed-package CI lane on Linux
Python 3.11–3.14 and the existing macOS 3.13/3.14 lanes. The recovery matrix also
enables `RECORDA_TEST_SMONITOR=1`. No provider source substitution is used.
Current evidence is [evidence/default_arguments_local.json](evidence/default_arguments_local.json).
Earlier source and public-provider receipts remain historical:
[archive/argument_configuration_source.md](archive/argument_configuration_source.md),
[archive/published_support.md](archive/published_support.md).

Reference-check contracts are the next independent boundary in
`uibcdf/recorda#20`. The umbrella ecosystem review stays partial; public Recorda
distribution/release and OS qualification remain in #3 / #4.
