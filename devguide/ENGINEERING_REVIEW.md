# Initial engineering review

Recorda is a directly governed MOLI component. Registry admission and review states
must be reconciled in MOLI; the laboratory is associated test infrastructure.

## Runtime boundaries

The first slice uses the Python standard library. Public inputs currently have ordinary
type, size and lifecycle guards. No argument normalization engine or optional scientific
backend is introduced; ArgDigest and DepDigest have no selected runtime use yet.
Scientific failures and capture omissions are structured record data, not diagnostic logs.
Storage faults propagate as Python I/O exceptions. A richer user-facing diagnostic boundary
must be reviewed for SMonitor before adding warnings, recovery advice or a logging framework.
No physical quantities are encoded by this first laboratory; future quantity adapters
must consume PyUnitWizard's codec without altering application unit configuration.
This bounded inspection is not a suite-wide non-applicability decision.

## Development and distribution

Use published pytest-receptor 1.1.0 and Ruff 0.16.5. The initial 25-test prototype
passed from source on Python 3.11 and against both built wheels on Python 3.13 outside
the source checkout, using the published receptor 1.1.0. Other checkouts may contain
development tool versions and are not substituted as release evidence. The local
versions and artifact fingerprints are in `evidence/first_slice_local.json`.
The subsequent source and installed-wheel qualification on Python 3.14.7 also
passes all 25 tests and the five laboratory scenarios; its independent evidence
is in `evidence/python314_local.json`.
The manual activation experiment now passes 43 tests from source on Python 3.14
and against the same built wheels on Linux Python 3.11, 3.12, 3.13 and 3.14. Native
adapters are explicit trusted integration callbacks, with faults exposed as omissions;
semantic profile labels do not implement the planned policy engine. Qualification and
artifact fingerprints are in `evidence/manual_activation_local.json`.
The laboratory additionally keeps runnable notebooks, real IPykernel cross-cell and
fault qualification, and repeated direct/dormant/active measurements. Notebook
dependencies are laboratory development/test tools, not runtime dependencies of
Recorda or the dummy package. Evidence and source identities are indexed in
`evidence/notebook_performance_local.json`. Timing remains specific to the local
dummy workload and filesystem, with the production synchronous writer unchanged.
The declared target is Python 3.11–3.14, with Python 3.14 for local development under
the baseline and admission history in `PYTHON_SUPPORT.md`. CI retains the 3.13
regression gate and includes the current MOLI routine version, 3.14, on Linux and macOS;
configured lanes do not establish current OS support. No public support claim is made yet.

Create the Conda environment in `devtools/conda-envs/`, then install this checkout with
`python -m pip install --no-deps --editable .`. Test tooling can alternatively run in a
virtual environment with the declared development packages, since the current runtime
closure is empty. Version `0.1.0` identifies the first experimental source checkpoint,
tracked in `uibcdf/recorda#5`. Earlier `0.0.0` artifacts and their evidence remain
historical; they do not qualify the new checkpoint. No PyPI, Conda, DOI or archival
availability is claimed.

Before publication, finish the distribution review: Conda recipe, metadata/environment
contract preflight and negative fixtures, exact candidate build and installed-platform
matrix, immutable artifact identity and independently verified public registry state.
There are no generated runtime resources in this slice. Public versions follow `X.Y.Z`.

## Evidence and remaining scope

Local tests and source inspection qualify only the exercised prototype. Record exact
tool versions and commands with the first-slice issue. Broader research-workflow usability,
full supported-minor/OS evidence, real-workload resource measurements, multi-process
context, crash power-loss recovery, routing, integrity certification, export and replay
remain separate work. Do not close admission/review issues based only on configured CI.

The workspace-wide guide checker also detects pre-existing drift in Nextia, Praxis
and Sabueso, and missing guide delivery in MOLI Agent. The new Recorda and Recorda
Lab copies match the canonical guide exactly. Component-local validators and the
ten relevant registry/guide policy tests pass; the workspace-wide checker does not.

## Owning review issues

The controlled SciPy trial (`uibcdf/recorda-lab#4`) now checks a real external
scientific API, native results/references and useful failure/configuration inspection.
Its scientific dependencies are laboratory-only. `evidence/scipy_local.json` indexes
the local source/kernel qualification. Broader research workflows and release/OS
qualification remain open; the trial does not add generic verification or replay.

- [uibcdf/recorda#2](https://github.com/uibcdf/recorda/issues/2)
- [uibcdf/recorda#3](https://github.com/uibcdf/recorda/issues/3)
- [uibcdf/recorda#4](https://github.com/uibcdf/recorda/issues/4)
- [uibcdf/moli#50](https://github.com/uibcdf/moli/issues/50)
- [uibcdf/recorda-lab#1](https://github.com/uibcdf/recorda-lab/issues/1)
