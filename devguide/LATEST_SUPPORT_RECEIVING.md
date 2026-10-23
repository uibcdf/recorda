# Latest public support-provider receiving

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
