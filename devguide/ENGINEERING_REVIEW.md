# Initial engineering review

For current source identities, executed checks and resumption priorities, read
[CHECKPOINT.md](CHECKPOINT.md). The initial evidence below is historical; it does
not qualify later source or close the outstanding engineering issues.

Recorda is a directly governed MOLI component. Registry admission and review states
must be reconciled in MOLI; the laboratory is associated test infrastructure.

## Runtime boundaries

The current runtime requires ArgDigest and SMonitor; the initial stdlib-only
description below is historical. [SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md) records
the current assessment and evidence in `uibcdf/recorda#2`. Default profile
configuration uses ArgDigest (#19), and reference options have their own adoption
(#20). Recovery advice attached to native exceptions has an explicitly selected
SMonitor adapter (#16/#18). Scientific failures, omissions and reference observations remain
structured Recorda data, while native objects and errors retain provider ownership.

The current core ecosystem review (#2) is resolved with published-provider,
installed-wheel and supported-minor CI evidence. MOLI's observed registry remains
`partial`; the concrete `adopted` state proposal is recorded in `uibcdf/moli#62`.
Distribution, OS and coverage qualification are independent reviews.

DepDigest has no current core optional/heavy/backend loader. PyUnitWizard has no
current core quantity parsing, conversion or dimensional-validation boundary.
Their non-applicability decisions have explicit reassessment triggers in the maintained
review. A stdlib-only runtime is not itself a policy exception. Future quantity adapters
must consume PyUnitWizard's codec without altering application unit configuration.

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
virtual environment with the declared development packages after provisioning the
required published provider closure. Version `0.1.0` identifies the first experimental source checkpoint,
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

At the initial review, the workspace-wide guide checker detected pre-existing
drift in Nextia, Praxis and Sabueso, and missing guide delivery in MOLI Agent.
Both new guide copies matched MOLI; component-local validators and ten relevant
registry/guide policy tests passed. That historical workspace diagnosis is not a
current audit of sibling repositories. The current checkpoint records executed
Recorda and Lab component checks separately.

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
