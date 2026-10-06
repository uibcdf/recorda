# Technical inspection presentation — experimental view

Architectural evaluation: [uibcdf/recorda#14](https://github.com/uibcdf/recorda/issues/14).
Prototype: [uibcdf/recorda#21](https://github.com/uibcdf/recorda/issues/21).
The core prototype is implemented. Its API remains experimental; the completed
laboratory receiving/user-view evaluation is separately owned by
[uibcdf/recorda-lab#13](https://github.com/uibcdf/recorda-lab/issues/13).
The architectural research below retains the reasoning and original evidence.

## Current API and limits

```python
record = recorda.inspect("analysis.jsonl")
view = recorda.inspection_view(record)
# Checking remains a separate, explicit call with a caller-owned resolver.
report = recorda.check_references(record, resolver=local_files)
view = recorda.inspection_view(record, reference_report=report)
```

The returned JSON-compatible dictionary contains independent copies of `record`
and optional `reference_report`, execution totals, reference totals, coverage
omissions and grouped `findings`. `references.check_state` is `not_requested` or
`provided`; absent checking has `checked_occurrences=None`. Matched observations
remain totals, without a new diagnostic. Expected omissions and excluded calls
remain coverage facts, without one warning per deliberately omitted value.

Each finding keeps a fixed domain/state/code/level, occurrence count, distinct
full reference count where applicable, numeric `source_indices`, a minimal
state/count `fallback`, and `presentation` status/reason/message/hint. Operation
indices address `record.operations`, problem indices address `record.problems`,
and reference indices address `reference_report.references`. Unknown reference
states/problems retain their raw source values and an `unclassified` finding.
Distinct totals count valid full identities; an invalid-reference finding uses
`distinct_references=None` because its identity cannot be established.
The codes are defined in Recorda's `_inspection_catalog.py`; reference codes use
the original state uppercased with hyphens under `RECORDA-INSPECT-REFERENCE-`.

The first slice has **no local audience option**. It respects the application's
existing SMonitor audience and validates native facts without a new digestion
transformation. Importing published ArgDigest 0.15.0 in a previously unconfigured
process can bootstrap SMonitor and change warning/logging hooks. The public
registration-only opportunity is
[uibcdf/argdigest#32](https://github.com/uibcdf/argdigest/issues/32), coordinated
with [uibcdf/moli#62](https://github.com/uibcdf/moli/issues/62). Existing ArgDigest
configuration/checking boundaries are unchanged. Do not add an explicit audience
option through private provider imports, monkeypatching or bootstrap side effects.

Inputs require the exact `ScientificRecord` type and bounded native JSON values;
no arbitrary copying/string/iteration hooks or scalar conversions are used.
Each snapshot/report has at most 100,000 visited nodes, depth 24, 10,000 items per
collection, 4,096 characters per string and 1,048,576 aggregate string characters.
Integers have at most 256 bits, floats must be finite, and observed byte counts
must be nonnegative integers below 2**64. Exceeding a bound rejects input instead
of silently truncating facts. These prototype limits may reject larger journals.

Before provider access, validation checks the snapshot's consumed lifecycle and
coverage fields, complete ordered declared-reference/omission scope, report
session/status/coverage/scope, full identities and context, incomplete-operation
IDs and consistent duplicate observations. JSON equality preserves exact types.
Reference explanation messages explicitly identify the supplied check; they do
not claim a fresh observation when the caller supplies an older report. This
receiving correction is tracked in [Recorda #22](https://github.com/uibcdf/recorda/issues/22),
revealed by Lab #13 after restoring native bytes. The
[correction receipt](evidence/inspection_view_wording.json) records 305 passing
source/installed recovery tests and all 11
[exact-head CI jobs](https://github.com/uibcdf/recorda/actions/runs/37544021836)
at `48a6c9a0630027f0f2c3d8d82215de8e27764913`, with published receptors.

A report does not include every nonreference value in the snapshot: this checks
all facts it declares, **not** report provenance, freshness, a full-snapshot
fingerprint or authenticity of the claimed byte observations. Unknown observation
states remain explicit; impossible reference identities and malformed shapes fail.

Presentation is lazy when findings need explanations. Public `register_provider`
registers the catalog; public `resolve` runs in a metadata-only diagnostic scope
with only computed counts. Current catalog definitions and resolved templates are
checked to distinguish missing/malformed catalog output from valid explanations.
Registration may read its trusted provider declaration; the view never resolves
scientific references, reads their bytes or reruns work. No events or handlers are
created and no application configuration is selected. Plain import/inspection
remains provider-free; ordinary CLI JSON and journal/schema are unchanged.

A finding's presentation is `resolved`, or `unavailable` with `provider_missing`,
`catalog_unavailable`, `invalid_resolution` or `rendering_failed`. Missing SMonitor
is an installation fault, not an optional package contract. Facts and the minimal
fallback survive ordinary faults without native exception text. Invalid input,
KeyboardInterrupt, SystemExit and cancellation propagate. An incomplete session
can have zero incomplete operations; neither that count nor a truncated tail
identifies an interruption cause.

The [implementation receipt](evidence/inspection_view_local.json) records 83 new
regressions and 304 passing source/ordinary-installed recovery tests on Python
3.14.7, or 292 installed default tests with 12 recovery skips. All 15 runtime
files match source, wheel and installation. Published providers, pytest-receptor,
governance, Ruff and dependency preflight pass. [Exact-head CI](https://github.com/uibcdf/recorda/actions/runs/37541857485) passes
all 11 jobs at `80ef3dd337cd7db901132007c390ced8b7980b9c`, inspected with published
gh-run-receptor 1.2.0 and actual installed-test verdicts. The resolved report is
[archive/inspection_view.md](archive/inspection_view.md). Research evidence below remains historical;
it is separate from the completed receiving evaluation in Lab #13. Live provider-event
correlation stays in Recorda #15.

## Recommendation

Build an explicitly requested, read-only technical view **after inspection**.
Recorda derives structured findings from its existing snapshot and explicitly
supplied reference observations. A lazy SMonitor adapter resolves catalog
messages/hints alongside those facts. Keep the journal, `ScientificRecord`,
reference reports and ordinary CLI JSON unchanged. Do not add live diagnostic
capture, scientific interpretation, hidden file checking or reexecution.

SMonitor is already required in current package metadata; optional activation
of presentation does not mean an optional installation dependency. No new
version floor, DepDigest loader, quantity schema or MOLI runtime is needed.
This differs from recovery advice during persistence failure and from associating
producer diagnostics with operations (`uibcdf/recorda#15`).

## Consumer questions and observed examples

The unchanged Lab #9 reference scenario was rerun with ordinary installed packages
on Linux Python 3.14.7. Its accepted mean/variance remain 2.5/1.25. Examples below
are proposed summaries derived from real observations, not output of a working view.

| User question | Observed facts | Proposed summary/action |
| --- | --- | --- |
| Did the recorded execution succeed despite lost input bytes? | `missing_input/full`: succeeded; two missing occurrences of one distinct reference; two matched occurrences. | Recorded execution succeeded. One retained reference is missing now, affecting two occurrences. Check retained files and the supplied local index. |
| Does a changed output mean the computation failed? | `modified_output/full`: succeeded; two mismatched occurrences of one distinct reference. | Execution remains succeeded. Current bytes differ from the declared digest for one reference/two occurrences. Recover the intended retained bytes or review their provenance. |
| Is minimal capture broken? | `intact/minimal`: succeeded; six `capture_policy` omissions; zero checked reference occurrences. | Six groups were deliberately omitted. No reference-byte verification is established for those groups. Informational coverage, not six warnings. |
| Is an unverified reference corrupt? | `intact/limits`: one available_unverified and one unresolved occurrence. | One file is available without byte verification; another reference has no supplied index binding. Declare a supported digest or supply a matching trusted index as appropriate. |
| What completed before interruption? | `intact/interrupted`: incomplete session; one incomplete operation; one matched reference occurrence. | One operation has no recorded completion. A matched retained input does not establish its execution outcome. Inspect incomplete work without inferring why completion is absent. |
| Does restoration fix the execution history? | `restored/full`: succeeded; all four occurrences matched again. | Current reference observations recover; the original recorded execution outcome is unchanged. |

A truncated tail is separately a journal-prefix observation. It does not prove
power loss, a particular writer fault or scientific failure. A failed operation
is an execution fact; do not convert every native failure into a new Recorda error.

## Proposed fact-to-code contract

Use Recorda-owned catalog codes, separate from recovery codes. A finding retains
its technical domain, fixed condition/state, level, occurrence count, distinct
reference count where meaningful, and numeric pointers to source occurrences.
Rendering adds message/hint plus an explicit presentation availability/reason;
prose never becomes the source of truth. Names below are provisional.

| Source condition | Candidate code suffix under RECORDA-INSPECT | Treatment |
| --- | --- | --- |
| Incomplete session/operations | INCOMPLETE | One warning with session state and incomplete-operation count; do not invent a cause. |
| `truncated_tail` | JOURNAL-TAIL | Warning about the readable prefix; retain the original problem. |
| `missing` | REFERENCE-MISSING | Warning; check retained bytes/index. |
| `mismatched` | REFERENCE-MISMATCHED | Warning about current bytes; do not relabel execution. |
| `unresolved` | REFERENCE-UNRESOLVED | Informational unresolved locator; request a matching caller-owned index. |
| `available_unverified` | REFERENCE-UNVERIFIED | Informational availability without a verified digest. |
| `unsupported_digest` | REFERENCE-DIGEST | Informational check limitation; review declared algorithm/format. |
| `too_large` | REFERENCE-LIMIT | Informational byte-bound limitation; deliberate bound changes remain explicit. |
| `not_a_file`, `outside_root`, `invalid_reference` | REFERENCE-CONFIGURATION | Warning with each original state retained; review caller configuration without guessing a malicious cause. |
| `unreadable`, `unstable` | REFERENCE-OBSERVATION | Warning about unreadable/changing bytes; do not guess permissions or reexecute scientific work. |
| `matched` | ordinary reference totals | A byte-match observation, not scientific correctness, authenticity or replay certification. |
| Expected omissions and excluded boundaries | ordinary coverage totals | Group by fixed reason; no warning per omitted value or deliberately excluded call. |
| Missing reference-check input | ordinary check-state marker | Explicitly not requested/provided; do not treat an empty list as verification. |
| Unknown problem/state | UNCLASSIFIED | Preserve the structured observation and identify the unsupported presentation; never report success by omission. |

All twelve current reference states have a treatment. Group deterministically by
condition; preserve occurrence details. Deduplicate reference identities using all
four declared fields (owner, identifier, revision, digest), never a name or path.
Incomplete/session/tail findings may coexist; group related explanations without
discarding either fact. Repeated rendering produces the same findings, no new events.

Validate same-snapshot inputs, declared report scope and shapes before combining
results. Equal session IDs alone do not authenticate a snapshot or report. Caller
supplied dictionaries, unknown shapes and manually mutated records must not silently
become trusted findings. This projection needs bounded validation, not a new schema
for arbitrary scientific objects. Implementation options need closed contracts and
applicable ArgDigest checks plus mandatory native guards.

## SMonitor benefit and cost

| Option | Benefit | Cost/limit |
| --- | --- | --- |
| Small Recorda renderer alone | Pure explicit formatting; easy isolation; useful basic state/count view. | Recorda owns audience templates, hints and their policy itself; a second full catalog would duplicate the existing diagnostic provider. |
| Recorda findings + SMonitor resolve-only adapter | Reuses catalog and audience resolution; registration preserves application policy; already published/required provider. | Shared catalog registration and lazy imports can fail. Safe hints are currently common across audiences. Requires a small Recorda grouping/layout layer anyway. |
| Emit findings and call SMonitor report | Existing event cards and event aggregation. | Would manufacture diagnostics, depend on filtering/handlers/coalescing and mix this view with unrelated execution events; rejected for this slice. |

Choose the second option with a minimal independent state/count fallback, not two
complete message catalogs. SMonitor owns template resolution; Recorda owns
findings, coverage, ordering, layout and grouping. Audience profiles are not a
language translation system. Domain scientific interpretation stays producer-owned.

## Safe activation and failure behavior

Programmatic use first requests presentation explicitly from an already useful
inspection snapshot. A notebook displays its returned view; default CLI continues
printing JSON. A later explicit CLI summary mode can follow qualified implementation.
Reference checks are explicitly supplied; absent checking never causes filesystem I/O.

Register the Recorda catalog via public `register_provider`; call public `resolve`
inside `diagnostic_scope`. Do not configure the application, bootstrap policy via
ensure_configured, install handlers, emit events, decorate producers or inspect
private manager/context state. Preserve configured application audience when no
explicit local audience is requested. Validate explicit audience options. Library
import/ordinary inspection keeps its existing provider-free lazy boundary.

SMonitor receives only computed, validated bounded primitives, initially counts.
Keep record/session/operation names, paths, object values, full references/digests,
exception text and arbitrary repr out of templates/provider facts. Numeric source
pointers link details to the original structured view. Small output limits must be
explicit; truncated presentation never implies complete coverage. Scoped safety
cannot undo unrelated producer conversions that happened earlier.

Registration conflicts, missing required packages, unsafe scope budgets, unknown
codes and empty/malformed rendering return a fixed unavailable/fallback reason
alongside existing structured findings. Missing SMonitor remains an installation
fault, not a newly declared optional dependency. Do not stringify native provider
faults or recursively send them through the same renderer. Ordinary rendering faults
must not replace recorded outcomes; input validation errors and user interruption/
cancellation/SystemExit retain their own behavior. No blanket BaseException catch
is justified by an already completed read-only inspection.

## Published provider findings and improvement

Thirteen research probes pass with published SMonitor 0.19.0 py_1, Python 3.14.7
and published pytest-receptor 1.1.0. Provider coordinates/managed Python hashes are
verified. Enabled DEBUG delivery with MemoryHandler establishes no events are
emitted by resolution; a separate disabled/CRITICAL test confirms delivery policy
does not suppress an explicitly requested preview. Registration is idempotent,
conflicts are atomic, and the preselected application config is preserved.

Under metadata-only resolution, `metadata_message` overrides audience variants.
If absent, safe profile-specific messages work; ordinary `user_hint`/`dev_hint`
are not used, and `metadata_hint` supplies one common safe action. Unknown code/
missing fields have a generic safe fallback; attribute/index traversal is refused;
opaque values fail before repr/str evaluation. A renderer must handle these fallback
states rather than treating any nonempty resolved string as a qualified explanation.

Use safe profile messages and a shared metadata_hint for the first slice.
[uibcdf/smonitor#39](https://github.com/uibcdf/smonitor/issues/39) proposes explicit
safe audience templates, especially hints. It preserves existing restrictive
semantics and is an improvement opportunity, not a prerequisite or provider patch.
No platform restructuring is required for this presentation slice.

## Evidence and next gate

Research reproducer: [evidence/inspection_presentation_probe.py](evidence/inspection_presentation_probe.py).
Receipt: [evidence/inspection_presentation_analysis.json](evidence/inspection_presentation_analysis.json).
Pinned upstream guide: [SMonitor 0.19.0 guide](https://github.com/uibcdf/smonitor/blob/f604b940ab281df4554869fdd24f796ea6d42c27/standards/SMONITOR_GUIDE.md).
The unchanged existing recovery/import guards also pass (five selected tests).
These are provider API probes and source-fact observations, not a working renderer
or useful-user-view qualification. No new CI run is required or claimed for analysis.

`uibcdf/recorda#21` owns the prototype and its installed exact-head regressions.
`uibcdf/recorda-lab#13` owns the subsequent receiving experiment to
compare the proposed view with JSON on the existing missing/modified/unverified/
omitted/incomplete scenarios, including hostile fields, failures and duplicates.
Only that experiment can establish the view's practical value. Live producer-event
correlation, shared MOLI routing, scientific narrative and replay remain outside scope.


## Completed laboratory receiving evaluation

[Lab #13](https://github.com/uibcdf/recorda-lab/issues/13) compares actual reference
JSON, technical messages and independent native oracles. It exposed the stale
“missing now” ambiguity, fixed in Recorda #22 by explicitly scoping explanations
to the supplied check. Local installed-pair checks pass 333 with four Sabueso skips,
six notebooks/49 cells and 14 kernel fault cells. Both nine-job candidate/default
runs pass; exact sources and receipts are in CHECKPOINT.md and Lab's maintained
INSPECTION_VIEW.md. The view answers those fixed technical questions, without
claiming a human usability study, fresh/authenticated reports or scientific meaning.
