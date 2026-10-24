# Latest public support-provider receiving

## Current source receiving — 2026-10-24

Owner: [uibcdf/recorda#34](https://github.com/uibcdf/recorda/issues/34).
Coordination: uibcdf/molsyssuite#135 and uibcdf/praxis#14.

Review ArgDigest **0.17.0 py_0** and SMonitor **0.22.0 py_0**, retaining
DepDigest **0.15.1 py_0**. Source metadata and the recipe admit
`argdigest>=0.15.0,<0.18` and `smonitor>=0.19.0,<0.23`; all five build/test/
development/recovery environments and the exact-provider checker select the
reviewed public cohort. Existing floors and the next-minor bounds are retained.

ArgDigest 0.17 adds opt-in `contract_owner` and repairs alias presence and
staticmethod handling. Recorda's free-function pipelines keep the default owner,
explicit restrictive capture and disabled value digestion; no new owner or
normalization contract is selected. SMonitor 0.22 adds an opt-in pytest policy
CLI/module, leaving the consumed scope, registration, resolution and recovery
APIs unchanged. Recorda does not enable that policy or change diagnostic startup.
The [diagnostic setup decision](DIAGNOSTIC_SETUP.md) remains applicable.

| Provider | File | SHA-256 |
| --- | --- | --- |
| ArgDigest | `argdigest-0.17.0-py_0.tar.bz2` | `9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1` |
| SMonitor | `smonitor-0.22.0-py_0.tar.bz2` | `bbf5890bed4ea657044b904f07d3cef137d474f0862ef5f35b063db9c8f0c949` |
| DepDigest | `depdigest-0.15.1-py_0.tar.bz2` | `2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850` |

Fresh Linux/Python 3.14.9 provisioning from `uibcdf` / `conda-forge` verifies the
three public archives and **97 managed Python files** (39 ArgDigest, 41 SMonitor,
17 DepDigest). With published pytest-receptor 1.2.1, **378 source and 378
installed-wheel tests pass**, recovery enabled, without failures, skips or
warnings. Native exits, JUnit and complete integrity-valid receptor artifacts
agree; `pip check` and route/governance/Ruff checks pass.
[Local receipt](evidence/support_cohort_34_local.json).

A separate clean venv, without inherited site-packages, installs actual editable
snapshots of the three provider commits from #34's corrected source audit. All
**378 tests** and `pip check` pass. Runtime roots are checked in normal Python
and `python -I`; installed metadata alone is not proof. The initial inherited
venv attempt reproduced the already reported provider-shadowing trap and was
rejected before testing. Provider tracked files remain unchanged after builds.
[Editable receipt](evidence/support_cohort_34_editable.json).

Applicable exact-commit hosted gates remain pending. This source change does not
publish a new Recorda version. Public **0.3.2** retains its original metadata
(`argdigest<0.17`, `smonitor<0.22`), bytes, tag and qualified provider closure.
The shared workspace must refresh Recorda from the receiving source commit;
an all-public install of the new cohort requires a separately qualified release.
No scientific consumer adoption is implied. Earlier #24 evidence below keeps
its original cohort and scope.

## Historical owner

Owner: uibcdf/recorda#24. Coordination: uibcdf/molsyssuite#82 and uibcdf/moli#40.

## Public delivery — 0.3.1, 2026-10-23

The separately qualified [0.3.1 release](https://github.com/uibcdf/recorda/releases/tag/0.3.1)
now delivers this compatibility publicly. Its [receipt](evidence/release_0_3_1.json)
binds the original Conda file to source `a432cc38fe675ae16eff4f6a0f2f43522b50994b`,
14 successful source jobs, 10 candidate jobs (364 tests per eight OS/minor cells),
and three successful publication/public-install jobs. Anaconda and GitHub assets
match SHA256 `8d040ae189d0f47ea0191a142c7e9cc0b57cd9e890303a354d8f463fe34242d9`.
Receiving notice is `uibcdf/molsyssuite#130`; consumer adoption remains separately
owned. The historical source-only limitations below describe the original #24
checkpoint, not today's 0.3.1 package.

## Historical source receiving — 2026-10-20

On 2026-10-20 Liliana requested compatibility with the latest published support
providers: ArgDigest 0.16.0, SMonitor 0.21.0 and DepDigest 0.15.1. Preserve the
previous runtime floors and admit these qualified minors through bounded upper
limits. Current receiving must execute existing contracts against public provider
files and verify their identities; widened metadata alone is not evidence.

The public Recorda 0.3.0 archive retains its original provider ceilings. Source
compatibility does not rewrite that archive or claim a new public release. A
future separately authorized Recorda release is required before a public-only
joint install can select the new cohort. Praxis's old-cohort recording tests and
the latest mandatory-provider tests therefore have distinct scopes.

No provider scientific implementation, component version, existing release plan,
tag or public file is changed. Joint editable-source receiving does not claim
an installed consumer Conda release or broader scientific qualification.

The qualified current cohort uses original public files:

| Provider | File | SHA-256 |
| --- | --- | --- |
| ArgDigest | `argdigest-0.16.0-py_0.tar.bz2` | `e82d82680d79ae3d5df9917b1662d2855ed8485128943b72ddec87a5769a467d` |
| SMonitor | `smonitor-0.21.0-py_2.tar.bz2` | `62b6cbae37f7fa06374af87923792f00253020955d000294b1a7d37eb9d04e56` |
| DepDigest | `depdigest-0.15.1-py_0.tar.bz2` | `2765c692de4e6aacff4197c4226ebb42ec1f0df9edb27e92f196ef1390cb1850` |

Joint editable receiving on Linux/Python 3.14.8 passed 345 Recorda tests
(including explicitly enabled SMonitor recovery) and 154 Praxis tests. Praxis
skipped its optional real-MolSysMT scenario because that provider is absent; this
is not scientific receiving of MolSysMT. All optional Recorda/Ackredit scenarios
ran in that joint editable receipt. `pip check` passed without exceptions.
Recorda's exact installed-provider checker verified 39 ArgDigest, 40 SMonitor
and 17 DepDigest Python files, all managed by their original public Conda
records; provider imports came from that disposable environment.

Provider selection is a dated, reviewed cohort, not a claim about unreleased
future minors. Preserve receiving evidence when reviewing a later public provider.
