# Diagnostic setup decision — 2026-10-22

Owner: [Recorda #29](https://github.com/uibcdf/recorda/issues/29).
Coordination: [MolI #62](https://github.com/uibcdf/moli/issues/62).

## Retained current behavior

Keep the existing safe first-use baseline. Plain import and journal reading
remain provider-free. `CapturePolicy` and reference-option validation load the
explicit ArgDigest pipelines inside restrictive capture and call
`ensure_configured` before importing ArgDigest. Without an application/project
policy, Recorda disables global warning, logging and exception capture. Existing
application/project settings take precedence. Repeated use preserves the
selected configuration, hooks and existing application sink.

Keep the completed inspection view's nonemitting, count-only adapter. It already
registers and resolves without configuring the application or importing
ArgDigest. Provider absence/failure retains the structured findings. The
completed #21 slice does not need a new setup API.

The explicitly selected recovery adapter registers its catalog without choosing
application policy. **Registration and emission have different effects**:
real emission retains SMonitor's compatibility console fallback when there are
no handlers, including an application explicitly configured with `handlers=[]`.
Normal session creation first loads the argument baseline; even a future
nonbootstrap emission option would not undo that earlier setup. An existing
application sink and its selected policy remain in place. A restrictive scope
governs payload collection, not configuration or handler bootstrap.

Recovery retains fixed codes and notes, safe session/operation IDs and native
exception identity/cause. Filtering or failed diagnostics do not certify journal
completion or change the scientific failure. This decision changes no recording
schema, result, routing or retention contract.

## Optional capabilities

| Boundary | Disposition and revisit trigger |
| --- | --- |
| Registration-only argument setup and nonbootstrap recovery emission | **Deferred.** No named consumer requirement justifies a second setup route in this review. Revisit when a named embedding application needs a handlerless or application-only startup contract. Review argument first use and real recovery emission together, with explicit setup/refusal semantics and receiving evidence; changing ArgDigest alone is insufficient. |
| Explicit per-call inspection audience | **Deferred.** Current callers use SMonitor's selected audience. Revisit when a real consumer needs two audience presentations in one process without changing global policy. |
| SMonitor 0.21 safe audience maps | **Not applicable to the current slice.** Existing fixed recovery messages and count-only inspection templates/shared hints suffice. Revisit for a concrete audience-specific safe explanation. |
| Nonemitting identity export or live diagnostic/operation bridge | **Not applicable to this decision.** No new Recorda export/association boundary is selected. Existing Lab experiments and #15 retain their own scope; a new consumer question requires its own substantive review. |

Keep the admitted floors and ranges. SMonitor 0.19 supports current scopes and
registration; 0.20 adds optional nonbootstrap emission. ArgDigest 0.16 registers
without bootstrap on a capable SMonitor, but Recorda still explicitly chooses
its first-use baseline. Availability and compatibility do not select a new local
behavior. Public Recorda release work remains [#26](https://github.com/uibcdf/recorda/issues/26).

## Receiving evidence

`tests/test_diagnostic_setup.py` qualifies fresh unconfigured, application-owned
and project-configured first use, repeat use, opaque option rejection and native
path-error identity. Explicit recovery cases distinguish repeated registration,
direct adapter emission and actual session recovery with an existing sink or
empty handlers. They preserve application capture hooks, native failure/cause,
fixed notes and incomplete work. Recovery cases stay in the explicitly enabled
`RECORDA_TEST_SMONITOR=1` route.

Existing suites cover provider-free ordinary inspection, count-only rendering,
missing/inadequate provider refusal, inherited-payload exclusion, filtered and
failed emission, cancellation and concurrent recovery. The
[dated receipt](evidence/diagnostic_setup_29_20261022.json) records exact installed
public legacy/latest provider identities and executed results. No runtime
implementation or dependency change is selected by this review.
