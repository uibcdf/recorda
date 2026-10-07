# Selected producer diagnostics — architectural decision, 2026-10-06

The analysis in [uibcdf/recorda#15](https://github.com/uibcdf/recorda/issues/15)
recommends a controlled **application-owned Lab comparison** before a reusable
Recorda live adapter. Public explicit operation boundaries, native references,
SMonitor local scopes and handlers already suffice for that comparison. No core
bridge, journal/schema change, new dependency or shared platform policy is
implemented by this analysis.

## Consumer question and evidence

“Which selected diagnostics were observed for this particular declared attempt
of the fit, and where can I inspect the retained native diagnostic artifact?”

Lab's existing SciPy/workflow scenarios have an actual failed optimizer attempt
and a later successful retry. They establish why attempt identity matters.
They do **not** establish native SMonitor emission by SciPy. The first controlled
producer must be separately attributed; a consumer message or Python warning
must not be described as a native SciPy SMonitor diagnostic.

The [research probes](evidence/diagnostic_correlation_probe.py) execute public
SMonitor 0.19.0 py_1 APIs and the installed current Recorda prototype on Linux
Python 3.14.7. **20 cases pass** with published pytest-receptor 1.1.0. Several
assert observed limitations. **15 unchanged recovery/import/view guards pass**
separately. The [receipt](evidence/diagnostic_correlation_analysis.json) preserves
versions, public archive coordinates/hashes, source identities, commands and
output hashes. No new scientific scenario, automatic live bridge, hosted CI or
human usability study is qualified here.

| Functionality | Owner and question |
| --- | --- |
| Recovery diagnostics | Recorda advises about its own failed persistence; the native failure remains authoritative. |
| Inspection presentation | Recorda groups retained technical facts; SMonitor resolves their explanations without emitting events. |
| Producer diagnostic association | A consumer relates selected observed producer diagnostics to a declared operation; producer diagnostics and scientific outcomes remain distinct. |

## Alternatives and recommendation

| Alternative | Benefit | Limit / decision |
| --- | --- | --- |
| Reference an application-retained native bundle | Existing `Reference`/local index preserves ownership and byte observations; no live core API is needed. | A session-wide bundle alone does not identify an attempt. Its bounded events need explicit operation facts or an owner-supplied association. Ordinary export is not a strict safe snapshot. Include this baseline in Lab. |
| Explicit operation plus consumer-owned selected-diagnostic sidecar | Fixed codes and bounded association facts can answer the attempt question beside retained native references. Public handlers and scopes suffice under controlled application policy. | Sidecar coverage is delivered selected diagnostics, not all emitted warnings. Application owns selection, retention, lifetime and gaps. Compare this in Lab first. |
| Reusable automatic Recorda live adapter | Could associate diagnostics at ordinary decorated semantic boundaries. | Current decorated calls expose no public active-operation subscription/context contract. Private Recorda context and private SMonitor observers are unsuitable dependencies. Defer core/provider API design until the comparison demonstrates added value. |

The completed controlled comparison is
[uibcdf/recorda-lab#14](https://github.com/uibcdf/recorda-lab/issues/14).
The native dummy scientific library remains unchanged and independent. Scientific
and deterministic diagnostic-selection oracles are separately qualified. Read
[Lab's maintained trial](https://github.com/uibcdf/recorda-lab/blob/main/devguide/DIAGNOSTIC_ASSOCIATION.md)
for the result; the original analysis evidence below retains its own historical scope.
Broader automatic attachment, notebook/default promotion and provider rollout
require their own implementation and receiving evidence.

## Identity and attachment

Use public `session.id` and the `operation.id` returned by explicit
`session.operation(...)`. They identify the recording and one attempt. Parent
identity comes from the recorded operation tree; it is not inferred from an
SMonitor breadcrumb. Each retry remains a new operation. A task/thread identity,
if needed by the experiment, is an application-generated bounded opaque label,
not a thread name, object repr, address or scientific parameter.

SMonitor's native `run_id` and `session_id` remain its own. Do not configure these
globally for each Recorda attempt or overwrite a producer's `correlation_id`.
An explicit scope can add `recorda_session_id` / `recorda_operation_id` through
`safe_extra`. An application registry corroborates those facts against its known
declared boundaries. They are associations, not authenticated producer identity.

The current event has no public per-occurrence `event_id`. A fingerprint groups
diagnostic characteristics: probes show identical fingerprints for two distinct
operations. It must not identify an operation, artifact or unique warning.
An association sidecar owns its artifact/revision identity and observation
ordinals. A native artifact reference preserves all four existing fields:
owner, identifier, revision and digest. The application retains/indexes bytes;
SMonitor owns its native diagnostic format and code meanings. Recorda owns only
the declared operation and reference occurrence.

The proposed controlled lifecycle is:

1. Application configures SMonitor once and declares producer/source/code
   selection and capture permissions. Publish the comparison's intended coverage.
2. Attach a bounded application-owned handler with public `add_handler`; keep a
   strong owner reference. Record attachment success before claiming observation.
3. Enter an explicit operation, register its lifetime, and enter a local scope
   with caller-approved opaque identities. Leave nested scopes by token restoration.
4. Close the application lifetime when the operation ends, retaining any allowed
   deferred-summary origin separately. Preserve native success/failure.
5. Application finalizes selected sidecars/reviewed bundles and references them
   using existing APIs where the operation/lifecycle permits. A failed attempt
   needs a deliberately tested retention path; a success-only output is insufficient.
6. Remove the exact handler in `finally`, including failed attachment/finalization
   paths. Mark interrupted or absent finalization explicitly.

`configure(handlers=...)` can replace an attached handler, and routing can exclude
it. A controlled application must own that lifecycle; a generic downstream
library cannot claim continuous attachment across arbitrary reconfiguration.
No private observer or handler-list polling is part of the recommendation.

## Capture policy and bounded representation

`diagnostic_scope(CapturePolicy(), safe_extra=...)` keeps the current detailed
capture permissions and adds bounded facts. Those facts also separate duplicate
aggregation groups; this is an observable application policy choice even when
rendered messages remain unchanged. An existing restrictive parent still wins.

The default `diagnostic_scope()` is metadata-only. It suppresses ordinary
messages/extras/context and can change producer-facing messages. Never silently
wrap scientific calls in that stricter policy as a side effect of recording.
Applications may explicitly choose it before provider collection; selection
after delivery cannot undo repr/stringification already performed by a producer.
No broad `@signal` is added by the analysis or proposed first slice.

The sidecar below is a **proposed Lab contract**, not a current core API:

| Retained facts | Proposed bound / meaning |
| --- | --- |
| Schema and artifact/revision identity | Fixed schema plus application-generated opaque identifiers, each at most 128 characters. |
| Recording/operation/parent association | Caller-owned opaque IDs, at most 128 characters; match declared registry entries. Optional task labels follow the same bound. |
| Diagnostic entries | At most 256 per operation; ordinal, exact allowlisted source/code (at most 128 characters), fixed severity, `event` or `aggregate` kind. |
| Summary numbers | Optional approved nonnegative exact builtin integers, at most 63 bits; retain as producer summary facts, not an invented warning count. |
| Coverage/fault facts | Fixed state/reason enums and bounded counters; report overflow/incomplete observation, never silently truncate into “complete”. |
| Native artifacts | Existing safe `Reference` identities and separate explicit local index; no path or artifact content in the association entries. |
| Aggregate budget | At most 1 MiB serialized sidecar and 32 operations per trial; at most 32 active and 128 closed deferred origins. Exceeding any bound gives an explicit gap/eviction fact. |

Exclude message, hint, human_summary, context/frames, arguments, exception text,
ordinary extra, tags, paths and arbitrary native objects. Do not coerce unknown
values with `str`/`repr`; reject or count the fixed omission. Producer source/code
strings are approved through an explicit small selection map, not merely truncated
and declared safe. Safe primitives can still contain secrets: approval is a
caller responsibility, not a semantic redaction service. Resolve any future
technical explanation from a known catalog separately from durable facts.

The existing-reference research case retains a reviewed synthetic bundle outside
the journal, associates its event with public explicit IDs, writes only its full
reference into Recorda, and checks matched/missing bytes. Removing the bundle
does not change recorded execution success. This demonstrates substrate adequacy
for that synthetic case; it does not make all native bundles safe to retain.

## Concurrency, coverage, duplicates and feedback

Immutable SMonitor scopes restore nested facts and separate interleaved async
tasks. Child tasks inherit creation context, including after the parent scope
ends. Therefore presence of an operation ID is insufficient proof that the
operation is still active. The application needs a closed-lifetime check: late
ordinary events are unassigned/stale, unless an independently declared lifetime
is explicitly supported. Deferred SMonitor summaries preserve originating safe
facts; allow known origins only and label those observations as aggregates.

For threads use one explicit `copy_context().run` per submission; use a fresh
`Context().run` for independence. Do not assume executor/version propagation.
Cross-process/distributed propagation is outside this slice. A handler must
protect its own mutable buffers/registry without writing the core journal or
calling providers while holding its observation lock.

The actual delivery pipeline matters:

- Disabled emission, level threshold and silenced source can prevent all handler
  delivery. A constructed return event is not proof of observation.
- Coalescing/duplicate policies act before handlers. Separate safe operation
  facts partition aggregation; deferred summaries can arrive after an attempt.
- Policy filters/routes can exclude the handler. A dropped handler event can
  still be retained in SMonitor's native buffer, as the probe demonstrates.
- Bounded native buffers lose older observations; their contents differ from a
  handler's selected sidecar. Do not subtract global report counters to derive
  operation totals under concurrent work.

Report **selected delivered observations** and producer aggregate facts
separately. A summary's total can include a first occurrence already delivered;
do not add summaries to individual entries as if each were a distinct warning.
Keep observation ordinals; do not deduplicate distinct attempts by fingerprint.

Coverage distinguishes `not_requested`, `unattached`, `observed_under_policy`,
`limited` and `incomplete`, with fixed reasons such as sink fault, overflow,
stale/unmatched identity or missing finalization. Zero selected observations does
not mean “no warnings occurred”; suppressed/uninstrumented events remain unknown.
These are proposed diagnostic states, separate from Recorda's execution status.

Allowlist the controlled scientific/consumer producer; exclude Recorda recovery
codes, inspection explanations, SMonitor runtime fault announcements and the
observer itself. The handler produces no new scientific operation and emits no
diagnostic about its own faults. Use a reentrancy guard and bounded independent
gap facts; do not recursively record a persistence failure while handling it.

## Failure and native-bundle limits

Ordinary observer/sidecar-writer faults must be contained at the consumer boundary,
leaving exact native return/exception objects intact. Preserve interrupts,
SystemExit and cancellation; do not indiscriminately swallow BaseException.
Expose diagnostic gaps in the consumer receipt where possible. If retention or
finalization cannot be established, no complete diagnostic artifact is claimed.
Core journal persistence keeps its existing reliability behavior; this analysis
does not redefine core writer faults as universally best effort.

Current SMonitor isolates ordinary handler exceptions, but a degradation warning
promoted to an error can escape direct emission. A fault-contained application
sink avoids relying on that general failure path; Lab must test its own behavior.
The provider defect is [uibcdf/smonitor#42](https://github.com/uibcdf/smonitor/issues/42).

Ordinary `collect_bundle()` includes argv, configuration, catalogs, provider paths
and report/triage sections. `drop_extra`, `drop_context` and event redaction do not
sanitize all sections. It also flushes/delivers deferred summaries. Do not export
it automatically as a harmless read. Review application-owned fixtures/artifacts
explicitly, or retain a separate narrow association sidecar. A strict bounded,
nonemitting export opportunity is
[uibcdf/smonitor#40](https://github.com/uibcdf/smonitor/issues/40).

Lowering `event_buffer_size` on an existing backlog currently keeps the older
capacity. [uibcdf/smonitor#41](https://github.com/uibcdf/smonitor/issues/41) owns
the reproduced defect. An explicit `recent_events(n)` / bundle `max_events=n`
limits selection count, not aggregate bytes, safety or capture completeness.

## Owner proposals and next gate

These three provider issues contain sanitized executed reproducers. The existing
[uibcdf/moli#62](https://github.com/uibcdf/moli/issues/62) receives the direct-consumer
impact notice. No new shared semantic authority, ProjectContext, EventLedger,
routing or reliability contract is selected; no platform restructuring is needed
for the controlled standalone comparison. A later shared/distributed contract
change requires its own MOLI proposal. ArgDigest, DepDigest and PyUnitWizard gain
no new applicable runtime boundary from associating these dimensionless diagnostic
identities; their current decisions remain in SUPPORT_LIBRARIES.md.

The seven architectural criteria of core #15 are answered. Lab #14 has qualified
both existing-reference alternatives at Lab `214a68d93a878bfe2b0d70a3aa90f81e00620db1`
with Recorda `48a6c9a0630027f0f2c3d8d82215de8e27764913`: 364 local installed-pair
passes/four Sabueso skips, 31 new cases, seven notebooks/55 cells and 14 real-kernel
fault cells. [Exact-pair CI](https://github.com/uibcdf/recorda-lab/actions/runs/37581680564)
passes nine jobs, inspected with published gh-run-receptor 1.2.0; published
pytest-receptor 1.1.0 supplies actual verdicts. No workflow default/provider/core
runtime changes or automatic bridge are made. Selected sidecars provide bounded
facts/gaps; reviewed native bundle subsets retain more detail. This synthetic
consumer evidence requires a real producer/user question before a reusable
automatic integration decision. Broader standalone acceptance (#1),
distribution (#3), OS (#4), coverage (#6) and replay remain separately open.
