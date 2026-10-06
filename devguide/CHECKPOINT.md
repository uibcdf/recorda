# Development checkpoint — 2026-10-06

Start here when resuming, then read [NEXT_STEPS.md](NEXT_STEPS.md) and the
maintained guide for the behavior being changed. Recorda remains an experimental
standalone component governed directly by MOLI. This checkpoint records completed
work and proposed next work; it does not authorize a new release or integration.

## Current inspection-view receiving qualification

Lab #13 receives Recorda `48a6c9a0630027f0f2c3d8d82215de8e27764913` (core #21 plus supplied-check wording #22)
at Lab implementation `b2b44d18f726bae975c7d21af3bf13bcda594980` and default promotion `181f706c09cef42ec104a8edc7b3c413601307d9`. Both
[candidate](https://github.com/uibcdf/recorda-lab/actions/runs/37544421813) and
[default](https://github.com/uibcdf/recorda-lab/actions/runs/37544670429) runs pass
all nine jobs with published receptors; the default run has no Recorda SHA override.
Local installed checks pass **333 tests/four explicit Sabueso skips** (305 core +
28 Lab), six selected notebooks/**49 code cells** and **14 real-kernel fault cells**.

The [Lab receiving contract](https://github.com/uibcdf/recorda-lab/blob/main/devguide/INSPECTION_VIEW.md)
and its local/hosted receipts preserve source/wheel/provider hashes, actual
verdicts and fixed user-question comparisons. Native dummy/scientific code and
oracles remain independent. Saved reference messages identify the supplied check;
they do not assert freshness. This is a controlled technical presentation trial,
not a human usability study, new scientific scenario or release/replay certificate.
Core #15 producer-operation correlation analysis is complete; its controlled Lab
comparison is queued separately below.

## Producer diagnostic association decision

[DIAGNOSTIC_CORRELATION.md](DIAGNOSTIC_CORRELATION.md) completes the architectural
analysis in `uibcdf/recorda#15`. Compare application-retained native bundles with
a bounded consumer-owned association sidecar using public explicit operations,
references, SMonitor scopes and handlers in `uibcdf/recorda-lab#14`. Keep native
science unchanged; existing SciPy trials establish attempt/retry context, not
native SMonitor emission. No reusable core bridge or shared MOLI rewrite is selected.

The [receipt](evidence/diagnostic_correlation_analysis.json) and public reproducer
retain **20 passing research cases** and **15 unchanged recovery/import/view guards**
on Linux Python 3.14.7 with published SMonitor 0.19.0 py_1 and pytest-receptor 1.1.0.
This is analysis evidence, not a working scientific diagnostic bridge or new CI.
Provider proposals/defects belong to `uibcdf/smonitor#40` (strict nonemitting export),
`uibcdf/smonitor#41` (buffer resizing), `uibcdf/smonitor#42` (degradation failure
precedence), with direct-consumer notice in `uibcdf/moli#62`. The resolved report
is [archive/diagnostic_correlation.md](archive/diagnostic_correlation.md).

## Previous published-provider receiving qualification

Recorda `b3a53770e3b9917e5ff399dbfc00a9c53f2a37ac` is now paired with Lab
receiving implementation `11b1465f9b8558a2ac4c7c172ab2377251820af3` and default
promotion `4256184d185cbae469b90de36f6f0fb260b7e4d4`, under
[uibcdf/recorda-lab#12](https://github.com/uibcdf/recorda-lab/issues/12).
All four Recorda-bearing Lab environments provision published SMonitor 0.19.0
py_1, ArgDigest 0.15.0 py_0 and transitive DepDigest 0.13.0 py_0. Dummy native
code, metadata and routine CI remain independent.

Local installed-wheel qualification on Linux Python 3.14.7 passes **242 tests
with four explicit Sabueso skips** (221 core + 21 Lab), six selected notebooks/45
cells and the real-kernel fault scenario. Provider provenance, pip check,
preflight rejection scenarios, governance and Ruff pass. The current pair runs
the seventh/multi-step notebook and excludes the fourth/Sabueso notebook.

[Explicit-candidate CI](https://github.com/uibcdf/recorda-lab/actions/runs/37536928526)
passes all nine jobs before default promotion;
[default CI](https://github.com/uibcdf/recorda-lab/actions/runs/37537236289) passes
the same nine afterward without a Recorda SHA override. Hosted kernels and dummy
checks cover Linux Python 3.11–3.14; the scientific/recovery lane uses 3.14 and
reports 242 passing tests/four skips. Published pytest-receptor 1.1.0 and
gh-run-receptor 1.2.0 were used. Exact source selection, manifests and verdicts
are retained in Lab's `devguide/evidence/published_providers_linux_py314.json`
and `published_providers_hosted.json`; read its maintained checkpoint.

This receiving pair does not requalify the historical Sabueso stack or establish
a public release, general OS support or replay. Earlier receipts below preserve
their original sources and limits. Subsequent documentation commits retain the
tested runtime, tools, environments, metadata, README and promoted workflow bytes.

## Historical reference-check source pair

| Repository | Implementation/experiment commit |
| --- | --- |
| Recorda | `565a68c5103a587b06c2411bba2064d1572b4c56` |
| Recorda Lab | `bac97e6e53c842846b5d21b3905df79cee9b3342` |

Subsequent checkpoint-only documentation commits do not replace those tested
source identities. Lab's manual integration default pins the full Recorda SHA.
The paired local receipts are `evidence/reference_checks_local.json` and Lab's
`devguide/evidence/reference_checks_linux_py314.json`, byte-identical with SHA256
`c9f575747ad0f498cbca7ea3da474beeabb46291ad2f080a870256bdedb45cce`.
All 13 core runtime/test files and 35 Lab runtime/test/experiment/fixture/notebook
files selected from their manifests match the published commits. Documentation
and the final workflow pin were published after local qualification, as stated
in the receipt's `manifest_scope`.

Completed behavior:

- Manual start/stop across ordinary decorated semantic calls; optional context
  managers use the same lifecycle. Unwrapped calls are outside declared coverage.
- Safe native input/result/exception references and explicit omissions, retaining
  native objects, scientific decisions and exception identity.
- Nested lineage, inspectable interrupted work and manual finalization after
  terminal persistence failure, with active-operation/context guards preserved.
- Session capture selection and minimal/detailed payload policies with explicit
  coverage limits.
- Explicit local reference resolution and bounded byte checks. Missing or altered
  retained files do not rewrite the original execution outcome.
- Six Lab notebooks, controlled SciPy fitting and offline Sabueso resolution.
  The independent dummy and scientific providers were not instrumented internally.

These are issue-backed slices, not frozen API/schema or full platform acceptance.
Their owning analyses remain in `archive/`; current behavior is in `ACTIVATION.md`,
`CAPTURE_SELECTION.md`, `REFERENCE_CHECKS.md` and the laboratory guides.

## Executed evidence and limits

- Local Linux Python **3.14.7**, published pytest-receptor **1.1.0**: **112 passed**
  (91 core + 21 Lab); six real-kernel notebooks, **45 code cells**. Ruff check,
  format, local governance and component MOLI guide checks passed.
- [Core CI](https://github.com/uibcdf/recorda/actions/runs/37432740933): seven
  successful jobs at the exact core commit, including Linux Python 3.11–3.14
  and the declared macOS lanes.
- [Lab routine CI](https://github.com/uibcdf/recorda-lab/actions/runs/37433553465):
  four successful dummy Python 3.11–3.14 jobs; manual-only jobs skipped.
- [Exact-pair manual integration](https://github.com/uibcdf/recorda-lab/actions/runs/37433724195):
  seven successful jobs, including real kernels on 3.13/3.14 and the SciPy lane.
  The scientific job passed 108 tests with four explicit Sabueso skips.
  Hosted CI does not execute Sabueso.

Local Sabueso evidence uses frozen copies of development packages and attributed
public fixtures. Their hashes and provenance are in the receipt; this does not
qualify published provider packages. Temporary directories under `/tmp` are not
durable dependencies: reconstruct matching sources and verify hashes before
repeating that lane. A different provider tree requires a new receipt.

The immutable **0.2.0** source tag still identifies
`4e3d422fef1b0927fe63422323dc6d941c061bfb`; it does not contain later recovery,
selection or reference-check work. Runtime metadata remains 0.2.0, so identify
current source by commit as well as version. Lab's dummy remains 0.0.0.
No new installed release candidate, public registry state, public OS support,
authenticated integrity, full dependency closure or replay is qualified here.

## Resumption checklist

1. Read both repositories' `AGENTS.md`, this checkpoint, `NEXT_STEPS.md` and
   Lab's `RECORDA_BASELINE.md`. Recheck Git status, HEAD, remote changes and owning
   issue states; do not overwrite concurrent work or interpret historical
   reports as current policy.
2. Select `/home/diego/Myopt/miniconda3/envs/molsyssuite@uibcdf_3.14/bin/python`
   explicitly and verify `sys.executable`/`sys.version`. The shell may activate
   another environment. Read `PYTHON_SUPPORT.md` before changing the target.
3. Verify published pytest-receptor 1.1.0 comes from a published distribution,
   rather than the shared development checkout. `/tmp/recorda-tools` was used
   for this receipt; recreate an isolated tool installation if it is gone.
4. Run `python devtools/validate_governance.py`, `ruff check .`,
   `ruff format --check .` and relevant pytest checks in each changed repository.
   Locally use `--receptor=llm`; CI uses `--receptor=ci`. For the qualified paired
   source command and optional-lane flags, consult the receipt. Enable Jupyter,
   SciPy and Sabueso only after checking their respective prerequisites.
5. Confirm the next independently closable theme and create its owning issue
   before an active report or implementation. Core implementation belongs here,
   laboratory scenarios in Lab, shared platform contracts in MOLI.

## Next work, in order

1. **Consolidate standalone acceptance** in
   [uibcdf/recorda#1](https://github.com/uibcdf/recorda/issues/1) and
   [uibcdf/recorda-lab#1](https://github.com/uibcdf/recorda-lab/issues/1).
   The individual trials above and the multi-step native-reference workflow in
   `uibcdf/recorda-lab#10` are complete. The consumer-question assessment is in
   [STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md). Choose another experiment
   only for a concrete remaining scientific question and specify its oracle,
   omissions and interruption cases in a new Lab issue first.
   The next selected comparison is `uibcdf/recorda-lab#14`, following the completed
   core #15 analysis above. Qualify explicit diagnostic references/associations
   before choosing a reusable automatic core adapter.
2. **Reconcile the completed current-core ecosystem review** in
   [uibcdf/recorda#2](https://github.com/uibcdf/recorda/issues/2).
   [SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md) classifies all four providers for
   the current runtime. SMonitor applies to existing persistence-recovery advice;
   ArgDigest applies to Recorda-owned argument contracts. Explicit source-provider
   experiments now cover recovery (`uibcdf/recorda#16`) and capture configuration
   (`uibcdf/recorda#17`); read [RECOVERY_DIAGNOSTICS.md](RECOVERY_DIAGNOSTICS.md)
   and [ARGUMENT_CONFIGURATION.md](ARGUMENT_CONFIGURATION.md) for their separate
   evidence. Published-provider qualification is complete for SMonitor 0.19.0 /
   ArgDigest 0.15.0 in `uibcdf/recorda#18`. Default configuration adoption is
   complete in `uibcdf/recorda#19`; reference-check contracts are qualified in #20.
   DepDigest and PyUnitWizard
   have no current core boundary, with explicit reassessment triggers.
   The local review is resolved; the concrete ecosystem-state change is proposed
   to MOLI in `uibcdf/moli#62`, with its observed registry still `partial`.
   Before advancing Lab's candidate, qualify the required provider environments
   and exact Recorda/Lab pair under `uibcdf/recorda-lab#12`.
3. **Before a distributable release**, complete packaging/distribution
   [uibcdf/recorda#3](https://github.com/uibcdf/recorda/issues/3), installed-candidate
   OS evidence [uibcdf/recorda#4](https://github.com/uibcdf/recorda/issues/4), and
   coverage/badge review [uibcdf/recorda#6](https://github.com/uibcdf/recorda/issues/6).
   A new tag needs its own exact candidate qualification; keep 0.2.0 immutable.
4. **After a concrete integration need**, read MOLI's `devguide/RECORDA.md` and
   open shared-contract work there. ProjectContext/EventLedger/ProjectRecord,
   cross-process routing and replay remain future work. Standalone Recorda
   retains no MOLI runtime dependency.

## Subsequent local acceptance assessment

`uibcdf/recorda-lab#10` completed the preparation/fitting/evaluation workflow and
was closed after direct integration into main. Read
[STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md) for the scientific questions,
local receipt and separate hosted Jupyter/SciPy qualification. Core runtime and
the previously published source pair above are unchanged; the new Lab evidence
does not replace their historical hosted results.

## Subsequent ecosystem boundary audit

[SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md) and
`evidence/ecosystem_boundaries_local.json` record the current-runtime audit in
`uibcdf/recorda#2`, with 91 core regressions passing locally under published
pytest-receptor on Python 3.14.7. The initial basic-guard/future-diagnostic rationale
is superseded by explicit ArgDigest/SMonitor applicability. Adoption remains
partial; no runtime dependency, accepted exception or registry promotion follows
from the classification alone.

The broad acceptance and engineering issues remain open. A completed local
scenario or configured CI lane does not close their wider obligations.

## Subsequent recovery-diagnostic source integration

`uibcdf/recorda#16` adds an explicitly selected SMonitor adapter at the two native
failure recovery sites. Read [RECOVERY_DIAGNOSTICS.md](RECOVERY_DIAGNOSTICS.md) for
activation, catalog codes, fallback and confidentiality limits. Local Linux
Python 3.14.7 tests with published pytest-receptor 1.1.0 pass: 104 core tests
(12 integration tests explicitly skipped), and 116 with pinned SMonitor source,
including the built/installed Recorda development wheel. The receipt is
`evidence/recovery_diagnostics_local.json`.
[CI 37498367934](https://github.com/uibcdf/recorda/actions/runs/37498367934) passes
all 11 jobs at implementation commit `70a98587d9d2f8dce0626fa2bca1bd4a6a932c47`,
including installed-Recorda/source-SMonitor checks on Linux Python 3.11–3.14.
Published gh-run-receptor 1.2.0 inspected the completed run. The experiment's
resolved analysis is in [archive/recovery_diagnostics_source.md](archive/recovery_diagnostics_source.md).

The subsequent closing documentation checkpoint changes no receipt-selected
runtime, test, metadata or workflow byte; it does not create a new CI certificate.

SMonitor `6feac9728cc35d57cbc92f284d7040d7f04cb35b` supplies the new scoped and
registration APIs; published 0.18.0 does not. No dependency/extra, version/tag,
public provider qualification or completed ecosystem adoption is inferred from
this development experiment. ArgDigest configuration work and #14/#15 remain
separate; MOLI's wider ecosystem state remains partial.

## Subsequent published-provider qualification

`uibcdf/recorda#18` replaces the provider-source routes with published SMonitor
0.19.0 build 1, ArgDigest 0.15.0 build 0 and DepDigest 0.13.0 build 0. The explicit
integrations remain caller-selected; optional extras and dedicated Conda environment
specifications declared their bounds. The core remained provider-independent at
that checkpoint, before the default-adoption work in `uibcdf/recorda#19`.

That checkpoint's [receipt](evidence/published_support_local.json) records public-index
and downloaded-archive hashes, byte-identical installed provider files, a tested
development Recorda wheel and 158 passing source/installed tests on Python 3.14.7
with published pytest-receptor 1.1.0. [CI 37529525379](https://github.com/uibcdf/recorda/actions/runs/37529525379)
passes all 15 jobs at `2b8b3deecc43dc65e6c34e440dfeb0cbe3d29891`, including
eight installed-provider lanes on Linux Python 3.11–3.14, inspected with published
gh-run-receptor 1.2.0. Earlier receipts keep their original source/publication limits.

Continue with default ArgDigest adoption and the reference-check argument contract;
inspection presentation and provider-operation correlation remain independent.
No public Recorda release, generic dependency loader, quantity schema, full OS
qualification or MOLI registry promotion follows from this provider checkpoint.

## Subsequent default argument adoption

`uibcdf/recorda#19` adopts published ArgDigest for ordinary CapturePolicy
construction, preserving the closed constructor signature and mandatory native
guards. Providers load lazily at configuration use. Plain import, journal reading
and existing reference checks retain provider-free imports. Recorda's first-use
SMonitor baseline disables global logging/warning/exception capture while an
existing application/project policy wins. Scientific calls remain native.

Required metadata, all four Conda environments and the local noarch development
recipe agree; a read-only preflight has negative route/constraint regressions.
The [receipt](evidence/default_arguments_local.json) records 171 passing source
and installed-wheel tests on Python 3.14.7 with published pytest-receptor 1.1.0;
the default lane passes 159 with 12 explicit recovery skips.
[CI 37532171347](https://github.com/uibcdf/recorda/actions/runs/37532171347)
passes all 11 jobs at `87ec6526fbd17e6d849efdc14773e3596cfa7bd8`, including
default installed-package Linux Python 3.11–3.14/macOS 3.13–3.14 and four Linux
recovery lanes, inspected with published gh-run-receptor 1.2.0.
The resolved report is [archive/default_arguments.md](archive/default_arguments.md).

Continue with reference-check contracts in `uibcdf/recorda#20`; the ecosystem
umbrella remains partial. Lab's next candidate requires receiving environments
and exact-pair qualification in `uibcdf/recorda-lab#12`. No Lab default SHA was
advanced. The recipe has not been built or published; public release, broader
OS acceptance and MOLI registry promotion remain separate. Closing documentation
changes no receipt-selected runtime/test/tool/metadata/Conda/workflow/README byte.

## Subsequent reference-option adoption and core review closure

`uibcdf/recorda#20` now uses published ArgDigest for resolver construction and
reference-check options. Closed signatures, exact identities, positive non-boolean
byte limits and declared algorithms remain explicit. Index shape and relative
confinement are checked before root processing. Invalid individual references
retain structured observations; the guarded native byte-check body is unchanged.
Each report validates configuration once and caches distinct reference checks.
Plain import and journal reading stay provider-free; checking calls now load the
already-required providers. Earlier receipts retain their historical import scope.

The [new receipt](evidence/reference_arguments_local.json) records 50 new receiving
regressions, 221 passing source/installed tests on Python 3.14.7 with published
pytest-receptor 1.1.0, or 209 with 12 recovery skips in the default lane.
[CI 37534456487](https://github.com/uibcdf/recorda/actions/runs/37534456487)
passes all 11 jobs at `c6248686815bd405a08955565e4fdc232bcef906`, inspected
with published gh-run-receptor 1.2.0. Closing documentation preserves every
receipt-selected implementation/test/tool/metadata/Conda/workflow/README byte.
The resolved slice is [archive/reference_arguments.md](archive/reference_arguments.md).

The current-core four-library review (#2) is locally complete, preserved in
[archive/ecosystem_boundaries.md](archive/ecosystem_boundaries.md): both applicable
providers have receiving evidence; DepDigest/PyUnitWizard retain explicit present
non-applicability and reassessment triggers. A concrete `partial` to `adopted`
registry proposal belongs to `uibcdf/moli#62`; the observed central state is still
`partial`, with no registry change made here. Lab receiving/exact-pair work is
complete in `uibcdf/recorda-lab#12`, as recorded above. Public release/OS/coverage
remain independent, and
SMonitor presentation/correlation remain separate from this core adoption.

## Subsequent inspection-presentation evaluation

`uibcdf/recorda#14` completes its architectural analysis, not a renderer
implementation. [INSPECTION_PRESENTATION.md](INSPECTION_PRESENTATION.md)
recommends explicitly requested Recorda-owned findings with a lazy, nonemitting
SMonitor resolve-only adapter. Execution, current reference observations,
expected coverage omissions and presentation availability remain separate.
Current package dependencies and plain import/inspection behavior are unchanged.

The [analysis receipt](evidence/inspection_presentation_analysis.json) records
13 passing published-SMonitor 0.19.0 research probes on Python 3.14.7 with
published pytest-receptor 1.1.0, five passing unchanged recovery/import guards,
and real example facts from the unchanged Lab #9 scenario. The reproducer is
retained with the evidence. Analysis does not qualify a working user view or
claim a new CI certificate. The resolved report is
[archive/inspection_presentation_analysis.md](archive/inspection_presentation_analysis.md).

At that analysis checkpoint, implementation was queued in `uibcdf/recorda#21`
and a separate Lab receiving issue was required before consumer/notebook changes.
Both later slices are complete as recorded above and below. Safe audience
templates, especially hints, are proposed in `uibcdf/smonitor#39`; shared safe
hints suffice for the first slice, so no provider or MOLI restructuring blocks it.
At that checkpoint, live producer-event correlation remained `uibcdf/recorda#15`;
the subsequent completed analysis and Lab #14 gate are recorded above.


## Explicit inspection-view core prototype

`uibcdf/recorda#21` implements `inspection_view(record, *, reference_report=None)`:
independent bounded JSON facts, execution/reference/coverage summaries, grouped
technical findings and lazy nonemitting SMonitor messages. No local audience
option bootstraps the application; native fact guards retain a closed signature.
Read [INSPECTION_PRESENTATION.md](INSPECTION_PRESENTATION.md) for the bounds,
source pointers, report-binding limits and presentation fault reasons.

The [local receipt](evidence/inspection_view_local.json) records 83 new regressions,
304 passing source/installed recovery tests on Linux Python 3.14.7 and 292 installed
default passes/12 explicit recovery skips with published pytest-receptor 1.1.0.
All 15 runtime files match source, wheel and ordinary installation. Published
provider verification, pip check, dependency preflight, governance/shared MOLI
core and Ruff pass. [Exact-head CI](https://github.com/uibcdf/recorda/actions/runs/37541857485) passes
all 11 jobs at `80ef3dd337cd7db901132007c390ced8b7980b9c`, inspected with published
gh-run-receptor 1.2.0. Actual installed-test logs report 292 passes/12 recovery
skips in six default lanes and 304 passes in four recovery lanes. The resolved
report is [archive/inspection_view.md](archive/inspection_view.md). Closing
documentation preserves all receipt-selected implementation and qualification
bytes; this is a core prototype, not a new Lab default or release.

The receiving experiment `uibcdf/recorda-lab#13` is complete, including notebook
comparisons and qualified default promotion as recorded above. Safe hints remain the
SMonitor #39 opportunity; nonbootstrapping ArgDigest registration is proposed in
`uibcdf/argdigest#32` and coordinated with `uibcdf/moli#62`. Live producer-operation
correlation was independently scoped in Recorda #15; its completed architectural
decision and queued Lab #14 comparison are recorded above.
