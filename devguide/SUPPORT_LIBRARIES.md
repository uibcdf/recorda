# Support-library boundary review — 2026-10-06

Owned by [uibcdf/recorda#2](https://github.com/uibcdf/recorda/issues/2).
This is the current-runtime assessment, replacing the initial blanket description
of basic guards and future diagnostics in [ENGINEERING_REVIEW.md](ENGINEERING_REVIEW.md).
The classification is complete for the inspected prototype; adoption remains
partial. No exception or registry promotion is established by this assessment.

The normative rule is MOLI's
[Python support libraries policy](https://github.com/uibcdf/moli/blob/d94ba1cc63ba4e90775c6364629af889fe9533b0/devguide/policies/python_support_libraries_policy.md).
It requires adoption where a boundary exists and forbids unused dependencies.
Recorda is governed directly by MOLI. Provider guides describe their APIs;
their MolSysSuite synchronization instructions do not govern Recorda.

## Decisions for the current core

| Library | Current boundary | Assessment and remaining work |
| --- | --- | --- |
| ArgDigest | `CapturePolicy.__post_init__` accepts several collection forms and produces a sorted, deduplicated tuple of validated profiles. Reference-check APIs also constrain resolver, digest and byte-limit options. | Applicable to Recorda-owned argument contracts; not adopted. Specify both function and value contracts before replacing public normalization. Preserve mandatory capture, path and lifecycle invariants. |
| DepDigest | Core runtime imports are stdlib-only; `pyproject.toml` has no dependencies or optional backend loader. | No present core boundary. Caller-supplied exact-type reference adapters are trusted callbacks, not discovered packages. Reassess when Recorda itself loads an optional/heavy/backend dependency. |
| SMonitor | `RecordingSession._finish` and `Operation.__exit__` add recovery advice to an existing native exception after a persistence fault. | Applicable to those diagnostics; not adopted. Review catalog-based presentation and safe structured fields while preserving native exceptions and recording failure visibility. |
| PyUnitWizard | The core records bounded scalars, safe references and omissions. It parses, converts and dimensionally validates no physical quantity. | No present core boundary. An unregistered quantity object remains unsupported, and a reference does not certify its producer's unit schema. Reassess before a quantity adapter or persisted quantity representation is introduced. |

The two non-applicability decisions concern the present core, not every laboratory
consumer or a future provider dependency closure. SciPy/NumPy, notebook kernels
and frozen Sabueso sources belong to Lab's controlled lanes. Recorda's stdlib
reader does not import those producers. No current scientific fixture justifies
routine recording of unit conversions.

## Argument adoption boundary

The profile canonicalization is more than an ordinary Python type error, so the
initial review's general non-applicability rationale no longer covers it.
An ArgDigest adoption must declare the accepted public inputs and their value
rules, including `None`, collection forms, 64-profile and 256-character bounds,
exact boolean detail switches, stable sorted uniqueness and defensive copying.
Reference checker contracts include a positive non-boolean byte limit, an
explicit supported digest algorithm and the accepted resolver/reference forms.

Do not digest arguments of the scientific function wrapped by `recorda.record`.
The scientific provider owns its call contract, defaults and native errors.
Inactive and excluded calls must continue to bypass capture and argument binding.
Scope adoption to Recorda's own configuration and inspection APIs.

Capture redaction before adapter invocation, omission of opaque values, journal
schema validation, context ownership and filesystem confinement are correctness
and confidentiality invariants. Keep them enforced even if a digestion layer is
bypassed internally. In particular, an unchecked public `skip_digestion` route
must not disable them. Ordinary signature binding remains Python's responsibility.

## Diagnostic adoption boundary

There are two existing advice sites in `runtime.py`, in the handlers for failed
operation completion and failed session completion. They retain the scientific
exception and append a fixed note explaining the provenance gap. They are a
diagnostic use, even though no logging framework or warning system exists.
The historical description that SMonitor matters only before adding advice is
therefore insufficient for today's implementation.

A bounded adoption must:

- Keep native exception identity, cause and traceback; diagnostic failures cannot
  replace the scientific failure or convert an incomplete journal into success.
- Use catalog-owned messages and explicit safe fields. Never pass scientific
  exception text, arguments, outputs, adapter details, file contents or paths
  into automatic exception telemetry or a diagnostic fallback.
- Preserve structured execution outcomes, capture omissions and reference
  observations as Recorda data. A SMonitor event does not replace the journal.
- Qualify message rendering, emission faults and import/configuration behavior.
  A broad `@signal` around the scientific target is not justified by this review.

Returned `ScientificRecord.status`, reference-check observations and the CLI's
JSON inspection snapshot are structured results. They do not establish adoption
of the separate recovery-advice boundary. Native scientific failures are not
automatically Recorda diagnostic events.

## Evidence and exit criteria

The downloaded public Conda archives match the solver's `uibcdf/noarch` index:

| Candidate | Required package dependencies | Declared Python bounds |
| --- | --- | --- |
| SMonitor 0.18.0 | none beyond Python | `>=3.11,<3.15` |
| ArgDigest 0.14.0 | DepDigest `>=0.11.0`, SMonitor `>=0.16.0` | `>=3.11,<3.15` |
| DepDigest 0.13.0 | SMonitor `>=0.13.0` | `>=3.11,<3.15` |

The receipt retains archive hashes, index records and distribution metadata.
This candidate closure has no required scientific dependency or reverse runtime
cycle. It is metadata inspection, not a solve, installation or integration test.
ArgDigest's science extras are optional in 0.14.0. SMonitor's optional pytest
bridge requires pytest-receptor `>=1.2,<2`; it is outside this runtime adoption
and the present 1.1.0 test-tool qualification.

Do not select versions from the Anaconda API's `latest_version` field alone:
the responses here report older versions although their own file lists and the
solver index contain the archives above. Use exact file/index/digest evidence.

[evidence/ecosystem_boundaries_local.json](evidence/ecosystem_boundaries_local.json)
records the inspected source identities, runtime/test hashes, import inventory,
published test tooling and executed core regressions. The baseline is Recorda
`c695b39f655f55ca1928f7fd5f7735ba8ab21a8d`. Runtime imports are all stdlib and
required project dependencies are empty; these facts describe implementation,
not a policy exemption. This review does not qualify installed support-library
behavior: the shared environment's provider installations are editable sources,
and the inspected archives were not substituted into that environment.

Existing tests cover immutable capture configuration, minimal/excluded calls,
native return/exception identity, secret and opaque-value omissions, missing or
altered references, persistence faults and later session activation. They prove
current behavior; they cannot prove an integration that has not been implemented.

Keep `uibcdf/recorda#2` open and MOLI's `python_ecosystem_review` state `partial`
until applicable boundaries have implementation and test evidence, or a governed
bounded exception records its rationale, owner and exit condition. The next
implementation should start with the small recovery-advice boundary, then the
configuration argument contract. The candidate metadata above admits the required
Python minors; execute clean installation and integration checks before adopting
those versions. Source guides or editable imports do not provide that evidence.
Any required dependency
change also updates the distribution work in `uibcdf/recorda#3`.

Reassess DepDigest during that dependency review if adoption adds an optional or
backend loader. Reassess PyUnitWizard only when quantities cross a Recorda-owned
boundary, following its codec and MOLI's quantity policy. Shared context, routing,
reliability policy and replay remain separate MOLI integration work.
