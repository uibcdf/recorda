# Standalone acceptance assessment — 2026-10-06

Coordinated in `uibcdf/recorda#1` and `uibcdf/recorda-lab#1`. Start with
[CHECKPOINT.md](CHECKPOINT.md) for the previously published qualified pair.
This assessment adds a local scientific workflow trial in `uibcdf/recorda-lab#10`;
the core implementation and immutable 0.2.0 tag are unchanged.

## What the completed mechanisms let a consumer answer

| Consumer question | Evidence and remaining limit |
| --- | --- |
| Which declared scientific operations were attempted, and what happened? | Activation and interruption trials retain identities, implementation and outcomes; undeclared calls remain outside coverage. |
| Which native results or exception traces belong to an operation? | Exact-type adapters preserve producer ownership and exception identity; unknown objects and adapter faults remain omissions. |
| Can a session select less detail honestly? | Capture selection records policy omissions and excluded invocation limits; minimal capture loses scientific dependencies. |
| Are the referenced files still available and unchanged? | Explicit local indices and bounded byte checks expose missing/altered files; receipts do not authenticate scientific identity or correctness. |
| Which intermediate observations and fit actually fed evaluation? | The new multi-step trial links prepared arrays and the native fit by full references; its expansion rules are trial-specific. |
| Does the retained result agree with an independent scientific calculation? | The new scalar OLS oracle checks selected rows, parameters, covariance and residuals; the qualification is a fictional dimensionless affine fit. |

Parent nesting alone cannot establish data dependencies. A byte match alone cannot
establish scientific correctness. The trial preserves both distinctions without
adding a core graph API, changing the provisional schema or instrumenting providers.

## New local trial

The Lab consumer prepares finite observations, calls unmodified SciPy curve_fit and
evaluates residuals. Direct, dormant and recorded executions agree with closed-form
OLS: slope 87/35, intercept -23/35 and residual sum of squares 1/14. Four recorded
dependency occurrences connect prepared data to fitting and evaluation, and the fit
to evaluation. The independent reader requires Recorda and stdlib only.

Acceptance retains actual optimizer failure/retry, hard process exit after
preparation, minimal-capture omissions and intermediate-file removal/alteration/
restoration. Missing files never rewrite the execution outcome. A negative case
updates a scientifically wrong evaluation together with its receipts and journal
references: all byte checks match while the scientific oracle reports inconsistency.

Local Linux Python 3.14.7, published pytest-receptor 1.1.0, Ruff 0.16.5:
**112 passed, four explicit Sabueso skips**. Six selected notebooks execute 45 cells,
including the new seventh notebook; the fourth/Sabueso notebook is skipped. This
differs from the earlier 112-test/six-notebook pair even though totals coincide.
IPykernel here is 7.4.0; previous qualification used 7.3.0. Exact sources, tooling,
commands, checks and artifact fingerprints are retained in
[evidence/multi_step_workflow_local.json](evidence/multi_step_workflow_local.json),
byte-identical to the Lab receipt. These local results do not requalify Sabueso's
frozen provider stack. Hosted evidence is recorded separately below.

## Executed hosted checks

Published gh-run-receptor 1.2.0 inspected the actual implementation runs; native
GitHub conclusions agree. [Core CI](https://github.com/uibcdf/recorda/actions/runs/37440493804)
passed seven jobs. [Lab PR CI](https://github.com/uibcdf/recorda-lab/actions/runs/37440479013)
passed four routine dummy/minor jobs and skipped two manual-only jobs.
[Manual Jupyter/SciPy integration](https://github.com/uibcdf/recorda-lab/actions/runs/37440827173)
passed all seven jobs at Lab `77e7c36a34a2ae0d140c3ad51b461e046ee0b7d5`, pinned to
Recorda `565a68c5103a587b06c2411bba2064d1572b4c56`. The scientific log reports
112 passed and four explicit Sabueso skips. These runs qualify the named source
heads; later documentation commits do not change their tested file fingerprints.
See [the paired hosted receipt](evidence/multi_step_workflow_hosted.json).

Implementation and owner review are tracked in
[uibcdf/recorda-lab#10](https://github.com/uibcdf/recorda-lab/issues/10).
The laboratory's `devguide/MULTI_STEP_WORKFLOW.md` defines the scientific
contract, consumer adapters, limited native reader and scenario coverage.

## Remaining decisions

The core API is sufficient for this controlled workflow; no new core limitation
was required to implement it. Broader standalone usefulness remains open: choose
the next consumer question from a concrete scientific need, rather than adding
all capabilities from DESIGN.md. Physical quantities require a concrete scenario
and the PyUnitWizard codec; they are not introduced by dimensionless fixtures.

Complete the support-library applicability decisions in `uibcdf/recorda#2`.
Packaging/distribution, installed-candidate OS qualification and coverage remain
`uibcdf/recorda#3`, `uibcdf/recorda#4` and `uibcdf/recorda#6`. Shared context/routing,
reliability policy, distributed propagation and replay stay separate future work
under the relevant MOLI contracts. Broader coordination issues remain open.
