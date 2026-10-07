# Standalone acceptance assessment — 2026-10-07

Coordinated in `uibcdf/recorda#1` and `uibcdf/recorda-lab#1`. Start with
[CHECKPOINT.md](CHECKPOINT.md) for the previously published qualified pair.
This assessment retains the historical scientific workflow trial in
`uibcdf/recorda-lab#10` and subsequent receiving evidence below. The immutable
0.2.0 source tag is unchanged; current prototype code is identified by exact SHA.

## Resolution of the original standalone slice

The original acceptance criteria in `uibcdf/recorda#1` and
`uibcdf/recorda-lab#1` are satisfied. Their coordination reports are resolved in
[archive/standalone_lab.md](archive/standalone_lab.md) and
[Lab's archive](https://github.com/uibcdf/recorda-lab/blob/main/devguide/archive/controlled_laboratory.md).
The accepted scope is a minimal experimental standalone substrate and its
independent controlled laboratory, with bounded real SciPy and native Sabueso
follow-ons. API/schema remain provisional. Wider usability, publication and
platform integration have separate acceptance gates.

| Original acceptance criterion | Executed evidence |
| --- | --- |
| Persist operation starts before calling scientific code | Core recording tests check ordered/fsynced writes and refuse execution when the start cannot persist. |
| Preserve original exceptions and expose incomplete work | Recording, activation, native exception-reference and recovery tests check exception identity, terminal storage faults, truncated tails and hard process exit. |
| Support caller boundaries, opt-in decorators, inactive calls and nested correlation | The explicit and manual activation runners check native behavior, parent identities and context ownership. |
| Retain native results through safe references | Dummy, SciPy fit and Sabueso Card/acquisition trials check native ownership and exact return/error objects. |
| State declared coverage, omissions and safe handling | Core capture tests and Lab reports check secret/opaque omissions, unwrapped-call gaps and minimal-capture losses. |
| Preserve fresh fixtures, native files, journals and checked reports | Both original runners write new destinations, verify native results and reject destination reuse. |
| Inspect without the scientific producer | Fresh isolated `-I -S` children read ten journals with only Recorda supplied; scientific packages and all support providers are unavailable. Semantic reference readers separately receive the required support closure. |
| Qualify installed artifacts and applicable checks | Installed core and scientific-pair receipts retain wheel/source/provider hashes, actual pytest verdicts, governance, Ruff and executed hosted gates. |
| Exercise a real external library and Sabueso follow-ons | SciPy fitting/multi-step OLS and native Sabueso source/diagnostic trials check independent scientific/source facts, failed attempts, retry, interruption and artifact loss. |

The final [consolidation receipt](evidence/standalone_acceptance_consolidation.json)
records **101 fresh targeted passes**: 75 installed core guards and 26 installed
Lab cases. Two original runners independently reproduce all five scenario outcomes
and their ten journals are inspected in a producer-free process. It verifies all
15 current core runtime files and 67 Lab source files against the native trial's
manifest, plus 394 installed Sabueso wheel members. These focused checks are
separate from the earlier complete qualifications; their totals are not merged.

The existing scientific pair is Recorda
`48a6c9a0630027f0f2c3d8d82215de8e27764913` / Lab
`a0376799c25c6b650ffa79aa6e4012601892d24c`, with clean source-built Sabueso
`68dac8f8bfc35944f5b6dd59aca8cb2a2819388d`: 380 local passes/four historical
Sabueso skips and [13 successful hosted jobs](https://github.com/uibcdf/recorda-lab/actions/runs/37584430143).
The native cases run separately on Python 3.11–3.14; this does not requalify the
older Sabueso #5/#6 stack. The latest development verifier correction is Recorda
`9228c84f78221442a4ceb0cfbc45887a919d8367`: 331 source and 331 installed passes,
and [11 successful hosted jobs](https://github.com/uibcdf/recorda/actions/runs/37587276559).
Its runtime bytes match that scientific pair. The Lab workflow default stays at
its previously qualified Recorda SHA. Published pytest-receptor 1.1.0 and
gh-run-receptor 1.2.0 were used; both existing runs were reinspected successfully.

## What the completed mechanisms let a consumer answer

| Consumer question | Evidence and remaining limit |
| --- | --- |
| Which declared scientific operations were attempted, and what happened? | Activation and interruption trials retain identities, implementation and outcomes; undeclared calls remain outside coverage. |
| Which native results or exception traces belong to an operation? | Exact-type adapters preserve producer ownership and exception identity; unknown objects and adapter faults remain omissions. |
| Which selected consumer diagnostics accompanied a declared attempt? | Lab #14 compares reviewed native bundle subsets with bounded selected associations using existing references; coverage is delivered observation, and the producer is synthetic. |
| Which requested Sabueso source was partial or failed despite a returned Card? | Lab #15 retains native Card/source/acquisition facts beside delivered native warning codes per attempt; filtering and absent artifacts remain explicit. Inputs are controlled offline fixtures. |
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
to evaluation. The independent reader requires Recorda, its required support
providers and stdlib.

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

The completed bounded implementation is tracked in
[uibcdf/recorda-lab#10](https://github.com/uibcdf/recorda-lab/issues/10).
The maintainer authorized direct integration into main; the two historical PRs
were closed without merging. The resolved laboratory analysis is preserved in
`recorda-lab/devguide/archive/multi_step_workflow.md`.
The laboratory's `devguide/MULTI_STEP_WORKFLOW.md` defines the scientific
contract, consumer adapters, limited native reader and scenario coverage.

## Remaining decisions

The core API is sufficient for this controlled workflow; no new core limitation
was required to implement it. The original standalone acceptance is complete.
Further consumer questions need a concrete scientific use case and a separately
scoped issue with an independent oracle. Physical quantities require a concrete scenario
and the PyUnitWizard codec; they are not introduced by dimensionless fixtures.

The current support-library applicability decisions are in
[SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md). Applicable ArgDigest/SMonitor
boundaries are implemented and qualified; `uibcdf/recorda#2` is locally complete.
Lab receiving adoption in `uibcdf/recorda-lab#12` qualifies the current installed
pair: 242 passing tests/four explicit Sabueso skips, six selected notebooks/45
cells, and two nine-job hosted runs before and after default promotion. Read
[CHECKPOINT.md](CHECKPOINT.md) for exact sources and receipt locations. These
regressions preserve the multi-step scientific oracle; they do not add a new
scientific scenario or replace Sabueso's historical provider qualification.
SMonitor inspection presentation analysis (`uibcdf/recorda#14`) and the core
prototype (#21) are complete. [INSPECTION_PRESENTATION.md](INSPECTION_PRESENTATION.md)
records explicit technical findings and nonemitting resolution. Lab #13 now
qualifies the supplied-check wording correction (#22), seven receiving regressions,
six notebooks/49 cells and the fixed JSON/view questions with 333 installed-pair
passes/four Sabueso skips and two nine-job hosted runs. Native scientific oracles
remain separate; this is controlled technical utility, not a human usability study.
The producer-operation correlation analysis in `uibcdf/recorda#15` is now complete
in [DIAGNOSTIC_CORRELATION.md](DIAGNOSTIC_CORRELATION.md). Twenty published-provider
research cases and 15 unchanged core guards pass; no scientific diagnostic bridge
is qualified by that analysis. The subsequent comparison in `uibcdf/recorda-lab#14`
is now complete: 364 installed-pair passes/four Sabueso skips, 31 new receiving
cases, seven notebooks/55 cells and all nine exact-pair hosted jobs. Existing
explicit references answer this synthetic consumer question without a core bridge.
Read [Lab's trial](https://github.com/uibcdf/recorda-lab/blob/main/devguide/DIAGNOSTIC_ASSOCIATION.md)
for native-bundle review, ownership, gaps and separate scientific/diagnostic oracles.
Real producer usefulness requires a new question/experiment; native SciPy SMonitor
emission is not established. Provider improvements remain SMonitor #40–#42.
The subsequent native producer trial in `uibcdf/recorda-lab#15` answers a concrete
Sabueso Card/source question. The unchanged public API emits its native partial
and failed-source diagnostics while returning a Card; a direct failed source query
remains a failed attempt, even after retry. Local installed qualification passes
380 tests/four historical Sabueso skips, including 16 native receiving cases.
Missing/changed artifacts, filtered delivery, producer-free reading and native
failure/interruption precedence remain explicit. Read
[Lab's maintained native trial](https://github.com/uibcdf/recorda-lab/blob/main/devguide/SABUESO_DIAGNOSTICS.md).
[Exact-pair CI](https://github.com/uibcdf/recorda-lab/actions/runs/37584430143)
passes all 13 jobs, including 47 passes per native Python 3.11–3.14 lane. This offline real-library scenario
uses fictional RCSB-shaped responses and attributed public UniProt fixtures; it
establishes neither live source completeness nor human usability. Existing explicit
references suffice; no automatic core context/attachment contract is selected.

Packaging/distribution, installed-candidate OS qualification and coverage remain
`uibcdf/recorda#3`, `uibcdf/recorda#4` and `uibcdf/recorda#6`. Shared context/routing,
reliability policy, distributed propagation and replay stay separate future work
under the relevant MOLI contracts. The original standalone coordination issues
are resolved; this conclusion does not close those independent gates.
