# Python support and working environment

Recorda and Recorda Lab admit Python 3.11–3.14 with
`requires-python = ">=3.11,<3.15"`. Their development environments use Python 3.14.
Ruff keeps `target-version = "py311"` to preserve the oldest supported syntax.

For the existing shared workspace, use the interpreter in
`/home/diego/Myopt/miniconda3/envs/molsyssuite@uibcdf_3.14`. Its name does not change
Recorda's direct MOLI governance. Check `sys.executable` and `sys.version`; an inherited
shell may still activate `molsyssuite@uibcdf_3.13`. Commands executed in a subprocess
do not change the parent shell's active environment.

## MOLI baseline and transition history

MOLI's current registry admits Python 3.11–3.14, uses Python 3.14 for development
and marks the common transition completed. Recorda's earlier component-specific
admission is retained in
`policies.python.transition.components` in MOLI's registry, with ownership in
[uibcdf/recorda#4](https://github.com/uibcdf/recorda/issues/4) and coordination in
[uibcdf/moli#50](https://github.com/uibcdf/moli/issues/50). Recorda Lab follows that
admission as associated test infrastructure, tracked by
[uibcdf/recorda-lab#1](https://github.com/uibcdf/recorda-lab/issues/1).

The earlier local 3.14 development default was a bounded deviation from MOLI's
routine 3.13 default, with review due by 2026-11-05 or the first public release.
Common-baseline adoption now satisfies that exit condition. Preserve historical
evidence and retain required Linux tests for every admitted minor, including 3.13.
This baseline alignment does not resolve the distribution or OS-support reviews.

## Qualification

The dependency-policy receiving in `uibcdf/recorda#35` qualifies source
`3c2dbc462fda451459e6b8f0af7d5d354ec50cd7` with 14 successful source jobs,
preserving the fixed-cohort Linux/macOS arm64 Python 3.11–3.14 matrix. Its
separate latest-public monitor passes Linux/macOS arm64 Python 3.14 with 408
tests each and complete installed-identity/JSONL/JUnit evidence. Local 3.14.9
targeted/source/installed checks pass 68/408/408.
[Policy receipt](evidence/dependency_policy_35_hosted.json). Runtime floors
permit later versions; only executed closures are qualified. No new public
Conda file or additional OS/architecture/Python support is claimed.

The later source-only provider receiving in `uibcdf/recorda#34` passes all 14
exact-source CI jobs at `28fe4912be30873cfc1bd6400c4a7f2c6783288c`, preserving
the Linux/macOS arm64 Python 3.11–3.14 installed-wheel matrix. Eight ordinary
cells pass 360 tests / 18 explicit recovery skips; four Linux recovery cells
and coverage pass all 378. Local Linux/Python 3.14.9 public-source,
installed-wheel and actual editable-provider lanes each pass 378 tests.
[Receiving receipt](evidence/support_cohort_34_hosted.json). This does not
requalify or change the immutable public 0.3.2 archive below.

The current **0.3.2** release qualifies the same original Conda file on Linux
x86_64 and macOS arm64 for Python 3.11–3.14, with **376 tests per installed cell**.
Its source/candidate/publication workflows pass 14/10/3 jobs, and public-channel
Linux/macOS installs and Release asset downloads match the original digest.
See [release_0_3_2.json](evidence/release_0_3_2.json). Earlier evidence below
retains its original source/tool/closure scope; Windows remains unclaimed.

Use published pytest-receptor 1.2.1, whose metadata admits Python 3.11–3.14, and
Ruff 0.16.5. The shared 3.14 environment contains a development receptor; select the
published tool separately for evidence. Do not change shared packages merely to run
the experiment. Preserve source and installed-wheel results with interpreter/tool
versions and artifact fingerprints in `evidence/`.

The 0.3.2 tool receiving is owned in `uibcdf/recorda#31`; read
[TEST_TOOL_RECEIVING.md](TEST_TOOL_RECEIVING.md). Older receipts retain their
original tool pins. The shared development checkout is never release evidence.

Required CI includes 3.14 without tolerated failures, while preserving older minors.
Version 0.3.0 qualifies the same Conda file on Linux x86_64 and macOS arm64 for
every admitted minor, with the full 345-test suite and published provider closure.
Source CI passes all 14 jobs and the exact-Conda candidate all 10. Independent
public-registry and clean channel installation evidence are preserved in
[`release_0_3_0.json`](evidence/release_0_3_0.json), owned by `uibcdf/recorda#3` / #4.
Recurring required source CI retains every OS/minor cell. Windows and other
architectures are not admitted by this receipt; shared MOLI registry reconciliation
remains separately owned.
