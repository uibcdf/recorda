# Development checkpoint — 2026-10-06

Start here when resuming, then read [NEXT_STEPS.md](NEXT_STEPS.md) and the
maintained guide for the behavior being changed. Recorda remains an experimental
standalone component governed directly by MOLI. This checkpoint records completed
work and proposed next work; it does not authorize a new release or integration.

## Published and qualified source pair

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
2. **Adopt the identified ecosystem boundaries** in
   [uibcdf/recorda#2](https://github.com/uibcdf/recorda/issues/2).
   [SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md) classifies all four providers for
   the current runtime. SMonitor applies to existing persistence-recovery advice;
   ArgDigest applies to Recorda-owned argument contracts. Explicit source-provider
   experiments now cover recovery (`uibcdf/recorda#16`) and capture configuration
   (`uibcdf/recorda#17`); read [RECOVERY_DIAGNOSTICS.md](RECOVERY_DIAGNOSTICS.md)
   and [ARGUMENT_CONFIGURATION.md](ARGUMENT_CONFIGURATION.md) for their separate
   evidence. Published-provider qualification is now tracked against SMonitor 0.19.0 /
   ArgDigest 0.15.0 in `uibcdf/recorda#18`. Default adoption and reference-check
   contracts remain pending. DepDigest and PyUnitWizard
   have no current core boundary, with explicit reassessment triggers.
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
