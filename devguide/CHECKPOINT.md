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
   The individual trials above are complete. Assess their useful provenance
   links and remaining coverage before choosing another experiment. A candidate
   is a small multi-step workflow with retained native references between steps;
   specify its scientific oracle, consumer question, omissions and interruption
   cases in a new Lab issue first. Its scope is still a proposal.
2. **Finish the ecosystem boundary review** in
   [uibcdf/recorda#2](https://github.com/uibcdf/recorda/issues/2): explicit
   applicability of ArgDigest, DepDigest, SMonitor and PyUnitWizard. Revisit
   diagnostics before adding advice/logging, and quantity codecs only when a
   concrete scientific scenario needs them.
3. **Before a distributable release**, complete packaging/distribution
   [uibcdf/recorda#3](https://github.com/uibcdf/recorda/issues/3), installed-candidate
   OS evidence [uibcdf/recorda#4](https://github.com/uibcdf/recorda/issues/4), and
   coverage/badge review [uibcdf/recorda#6](https://github.com/uibcdf/recorda/issues/6).
   A new tag needs its own exact candidate qualification; keep 0.2.0 immutable.
4. **After a concrete integration need**, read MOLI's `devguide/RECORDA.md` and
   open shared-contract work there. ProjectContext/EventLedger/ProjectRecord,
   cross-process routing and replay remain future work. Standalone Recorda
   retains no MOLI runtime dependency.

The broad acceptance and engineering issues remain open. A completed local
scenario or configured CI lane does not close their wider obligations.
