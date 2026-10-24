# Development checkpoint — 2026-10-24

## Current public release and pause checkpoint — 0.3.3

**0.3.3 is delivered**, owned by `uibcdf/recorda#37`:
[canonical Release](https://github.com/uibcdf/recorda/releases/tag/0.3.3),
official `uibcdf/main` noarch package and matching tag/package version.
Source: `99f6ca12295ef675abebfe8c42cbd3ad7881bb07`; annotated tag object:
`d84688ce83ff27a5927b8934553b77b953380c27`. Original file:
`recorda-0.3.3-py_0.tar.bz2`, SHA256
`fcee216130bca444e92e195fc38f8ef24fb501439cd123638bc11fa8e5df76ea`.

Fresh [source](https://github.com/uibcdf/recorda/actions/runs/40141263674),
[latest-public](https://github.com/uibcdf/recorda/actions/runs/40141291843),
[same-file Conda](https://github.com/uibcdf/recorda/actions/runs/40141291792) and
[publication](https://github.com/uibcdf/recorda/actions/runs/40142058462) gates
pass **14/2/10/3 jobs**. All eight Linux x86_64/macOS arm64 Python 3.11–3.14
Conda cells pass **408 tests each**. Trusted presence-only readiness passes;
the upload receipt verifies one original-file upload after an all-labels absent
preflight. The extra tag source CI also passes 14 jobs. Thirty full capture
members and 53 locally tested input hashes are independently verified.

Public API/main-label metadata, anonymous Conda download, two hosted public
installs, an independent fresh public-only Linux install and all three anonymous
GitHub Release asset downloads match original bytes, actual runtime/dependency
metadata and stable description. Canonical title/name/tag are exactly 0.3.3.
The [release receipt](evidence/release_0_3_3.json) and
[resolved analysis](archive/release_0_3_3.md) preserve the measured scope.

Public 0.3.3 now permits `argdigest>=0.15.0` / `smonitor>=0.19.0`; required floors,
five exact qualification environments, scientific recording behavior and
experimental API/schema remain unchanged. A separate weekly/manual latest-public
lane remains maintained; permitted resolution does not certify future versions.
Earlier files/tags and receipts remain immutable.

Release-specific notices: [MolI #78](https://github.com/uibcdf/moli/issues/78) and
[MolSysSuite #142](https://github.com/uibcdf/molsyssuite/issues/142), with actual
availability and evidence. Policy evaluations #76/#137 and consumer receiving
remain independently owned. Next: pause or select concrete receiving work;
Recorda #36 is a nonblocking Actions runtime maintenance review. A later checked
documentation-only closeout is not a new producer/gate. Owned disposable resources
are retired; useful proof has an owner/review trigger in
[resource closeout](evidence/release_0_3_3_resources.json).

## Historical dependency-policy receiving checkpoint — #35

Diego accepts minimum-only requirements (`argdigest>=0.15.0`,
`smonitor>=0.19.0`), retaining the five exact qualification environments and
adding a sixth, separate latest-public lane. Read [DEPENDENCY_POLICY.md](DEPENDENCY_POLICY.md).
The recipe expresses the same public intervals; static guards reject weakened
floors and hidden recipe ceilings. Runtime recording files remain unchanged.

Local Python 3.14.9 checks pass 68 targeted tests and **408 source + 408 installed
wheel tests**, with recovery enabled, clean `pip check`, complete integrity-valid
receptor/JUnit/native agreement and no failures/skips/warnings. The actual latest
selection and 97 installed public provider Python files are verified.
[Source CI 40133093885](https://github.com/uibcdf/recorda/actions/runs/40133093885)
passes all **14 jobs**, preserving the eight installed Linux/macOS arm64 Python
3.11–3.14 cells (390 passes / 18 explicit recovery skips) and four recovery plus
coverage cells (408 passes each).
[Latest-public CI 40133098600](https://github.com/uibcdf/recorda/actions/runs/40133098600)
passes both Linux/macOS arm64 Python 3.14 cells, **408 tests each**. Their actual
selection/installation identities and complete JSONL/JUnit agree with native
conclusions; twelve full-capture members and 50 locally tested input hashes are
verified. Source: `3c2dbc462fda451459e6b8f0af7d5d354ec50cd7`.
Read the [hosted receipt](evidence/dependency_policy_35_hosted.json) and
[resolved analysis](archive/permissive_provider_versions.md).

Requested independent evaluations are uibcdf/moli#76 and
uibcdf/molsyssuite#137. Their issues do not adopt this decision for other owners.
The domain issues remain evaluation requests, with no automatic wider adoption.
Next: select/qualify a 0.3.3 release separately if requested. Nonblocking
Actions runtime maintenance is tracked in `uibcdf/recorda#36`. Public 0.3.2 and
all historical evidence below remain immutable. Owned disposable resources are
retired; retained proof has an owner/review trigger in
[resource closeout](evidence/dependency_policy_35_resources.json). A later checked
documentation-only closeout is not a new producer or a new hosted gate.

## Completed source cohort receiving — #34 (historical bounds)

Admit ArgDigest 0.17.0 and SMonitor 0.22.0 for the editable refresh requested
in uibcdf/molsyssuite#135; related Praxis receiving is uibcdf/praxis#14.
The recipe and runtime source metadata preserve existing floors and widen only
the reviewed ceilings to `<0.18` / `<0.23`. Five environment routes and exact
provider verification select the public cohort with DepDigest 0.15.1.
Read [LATEST_SUPPORT_RECEIVING.md](LATEST_SUPPORT_RECEIVING.md).
Fresh public Conda source/installed-wheel checks each pass **378 tests** on
Linux/Python 3.14.9, with recovery enabled, clean `pip check`, verified public
provider bytes and complete receptor/JUnit/native agreement. A separate clean
editable-provider venv also passes 378 tests with normal/isolated runtime
origins asserted. Local [public](evidence/support_cohort_34_local.json) and
[editable](evidence/support_cohort_34_editable.json) receipts preserve the scope.
Exact-source [CI 40130538386](https://github.com/uibcdf/recorda/actions/runs/40130538386)
passes **14/14 jobs** at `28fe4912be30873cfc1bd6400c4a7f2c6783288c`:
eight installed Linux/macOS arm64 Python 3.11–3.14 cells pass 360 tests / 18
explicit recovery skips; four Linux recovery cells and coverage pass all 378.
The [hosted receipt](evidence/support_cohort_34_hosted.json) verifies native
conclusions, executed steps, full receptor capture and 45 local input hashes
against the commit. All 15 runtime files are unchanged from the starting source.

The [resolved analysis](archive/support_cohort_34.md) and existing dependency
route/provider-provenance regressions preserve this decision. Return receiving
to uibcdf/molsyssuite#135 and uibcdf/praxis#14; their shared refresh and Praxis
work remain independently owned. The named shared environment and primary
provider checkouts were preserved. A documentation-only closeout is not a new
tested producer commit; use the source above and its receipts.

No new release is selected. Public 0.3.2 and its immutable evidence below retain
their original ArgDigest `<0.17` / SMonitor `<0.22` limits; source/editable
receiving does not make that archive admit newer providers.

Next: consumers may refresh from the receiving source commit. Recheck live
issues before further work; a public-only cohort needs a separately selected
release. Owned disposable environments/copies are retired; retained evidence has
an owner and review trigger in [resource closeout](evidence/support_cohort_34_resources.json).

## Historical public release and pause checkpoint — 0.3.2

**0.3.2 is delivered**, with [Release 0.3.2](https://github.com/uibcdf/recorda/releases/tag/0.3.2),
official `uibcdf` Conda and matching tag/package version. Qualified source:
`e97ec6055e7110b37aac87a7c810c2da3f732c92`. Original file:
`recorda-0.3.2-py_0.tar.bz2`, SHA256
`d6293cfb48110baada88653beaa52250554558e858311fe409245eeac5372ede`.

Source [40003836709](https://github.com/uibcdf/recorda/actions/runs/40003836709)
passes 14 jobs; candidate [40004306942](https://github.com/uibcdf/recorda/actions/runs/40004306942)
passes 10, with **376 tests in every Linux x86_64/macOS arm64 Python 3.11–3.14
cell**. Publication [40005577937](https://github.com/uibcdf/recorda/actions/runs/40005577937)
passes all three jobs, including public-channel installs on both OSes. The extra
automatic tag source CI also passes all 14 jobs. Independent public Anaconda and
GitHub asset downloads match the original file; all 15 runtime files and actual
installed/public descriptions match the manifest.

Fixes #31/#32 are delivered: published pytest-receptor 1.2.1 has fresh llm/ci
success/failure/statistics receiving, intact JSONL/JUnit/native agreement and no
late warning; stable PACKAGE_README.md prevents live release status entering
installed metadata. The [release receipt](evidence/release_0_3_2.json) binds the
actual inputs, gates, public state and title/version checks. Resolved analyses:
[tool receiving](archive/pytest_receptor_1_2_1_receiving.md),
[description](archive/stable_packaged_description.md) and
[release](archive/release_0_3_2.md). Older receipts retain their original scope.

The [MolSysSuite #130](https://github.com/uibcdf/molsyssuite/issues/130) notice
now identifies 0.3.2 and preserves 0.3.1 history. Consumer receiving is separately
owned. No new runtime/scientific integration, API freeze or replay work is queued.
At closeout #31/#32 and release #33 are resolved; recheck live issues before
beginning new work after the pause.

Owned temporary environments/scratch are retired after evidence extraction;
the original artifact and complete proof have a release-audit owner and review
trigger in [resource closeout](evidence/release_0_3_2_resources.json). Preserve
shared active work and all published tags/files. A later documentation commit is
not a new qualified candidate; the tag remains on the exact source above.

## Historical maintenance preparation — 0.3.2

Diego authorizes fixing `uibcdf/recorda#31` and `uibcdf/recorda#32`, then publishing
0.3.2 if receiving and release gates pass and no release blocker remains. Owner:
`uibcdf/recorda#33`. Source baseline is
`006b92f4e015872406454a691cef66c9f8eda401`. Existing public tags/files remain intact.

Published pytest-receptor **1.2.1** is selected consistently across development
and CI. Its six installed Python files match the verified public wheel. The
eight fresh-process llm/ci success/failure/statistics cases and description
fixtures pass 26 targeted tests. Full source and installed-wheel checks each
pass **376 tests**, with complete, integrity-valid JSONL, matching JUnit/native
exits and no warnings. Actual wheel and installed METADATA match the stable
description. [Local receipt](evidence/candidate_0_3_2_local.json) binds these
inputs. Hosted same-source/same-artifact gates remain pending.

The package now reads stable `PACKAGE_README.md`, independent of live release
status. Candidate and installed/public verification bind the actual METADATA
description to its source and manifest digest. Read
[TEST_TOOL_RECEIVING.md](TEST_TOOL_RECEIVING.md) and
[PACKAGED_DESCRIPTION.md](PACKAGED_DESCRIPTION.md).

Next: full source and installed-wheel tests, fresh exact-source and same-file
Conda qualification across Linux x86_64/macOS arm64 Python 3.11–3.14, then
authorized exact-file publication and public/Release checks. The existing
canonical credential route and presence-only readiness apply. Notify the current
MolSysSuite receiving issue after verified delivery. Do not infer adoption or
reuse the 0.3.1 gates for new source/artifact inputs.

The completed 0.3.1 state and earlier history below retain their own identities.

## Historical release and receiving handoff — 0.3.1

**0.3.1 is publicly delivered**, with the canonical
[GitHub Release](https://github.com/uibcdf/recorda/releases/tag/0.3.1) title/tag
and package version. Source: `a432cc38fe675ae16eff4f6a0f2f43522b50994b`.
Original file: `recorda-0.3.1-py_0.tar.bz2`, SHA256
`8d040ae189d0f47ea0191a142c7e9cc0b57cd9e890303a354d8f463fe34242d9`.

[Source CI](https://github.com/uibcdf/recorda/actions/runs/39989246726) passes
all 14 jobs; [candidate qualification](https://github.com/uibcdf/recorda/actions/runs/39989597891)
all 10, with 364 tests in every Linux x86_64/macOS arm64 Python 3.11–3.14 cell.
[Exact-file publication](https://github.com/uibcdf/recorda/actions/runs/39991293202)
passes all three jobs, including independent public-channel installs on Linux
and macOS arm64. All receipts agree on the original source/digest and 15 runtime
files. Public Anaconda metadata and anonymous downloads from both Anaconda and
GitHub Release match; all three Release assets were independently verified.

The [release receipt](evidence/release_0_3_1.json) binds qualification, upload,
public installs, tag and Release. [Resolved analysis](archive/release_0_3_1.md)
preserves the decision and limits. Preparation receipts below remain historical;
their pre-publication pending states are not the current delivery state.

Requested availability handoff:
[uibcdf/molsyssuite#130](https://github.com/uibcdf/molsyssuite/issues/130), linked
to suite #82, MOLI #40 and Praxis #10 receiving. Delivery does not establish
consumer adoption. The original standalone/Lab acceptance and MOLI #62 are
complete; new scientific integration requires its own consumer question.

Next: receiving owners triage the new public package; Recorda's independently
scoped developer-tool follow-up is [#31](https://github.com/uibcdf/recorda/issues/31).
Future package-description stability is [#32](https://github.com/uibcdf/recorda/issues/32):
the immutable package long description retains build-time candidate prose;
version, runtime, dependency and digest evidence remain valid. Live guidance is updated.
Keep all public tags/files immutable. Original package and complete proof are
retained in `/tmp/recorda-031-candidate-nkrd225g` under Recorda #26 for release
audit, reviewed at the next audit/consumer handoff or by 2026-11-22. The owned
test environments and disposable scratch were retired; shared work was preserved.

## Historical preparation and qualification — 2026-10-23

Owner: [uibcdf/recorda#26](https://github.com/uibcdf/recorda/issues/26).
Checkpoint reconciliation: [uibcdf/recorda#30](https://github.com/uibcdf/recorda/issues/30).

**Qualified candidate, publication pending.** Exact source:
`a432cc38fe675ae16eff4f6a0f2f43522b50994b`. Original file:
`recorda-0.3.1-py_0.tar.bz2`, SHA256
`8d040ae189d0f47ea0191a142c7e9cc0b57cd9e890303a354d8f463fe34242d9`.
The [source gate](https://github.com/uibcdf/recorda/actions/runs/39989246726)
passes all **14 jobs**; the
[Conda candidate](https://github.com/uibcdf/recorda/actions/runs/39989597891)
passes all **10**, with **364 passing tests in each of eight installed
Linux x86_64/macOS arm64 Python 3.11–3.14 cells**. Independent archive inspection
and all eight receipts confirm the same source/digest and all 15 runtime files.

The [hosted receipt](evidence/candidate_0_3_1_hosted.json) preserves the full
manifest, platform receipts, native executed steps and 18 verified capture-member
digests. The [local receipt](evidence/candidate_0_3_1_local.json) records 364 source
and 364 installed-wheel passes, exact provider files and checked inputs.
[Credential presence](https://github.com/uibcdf/recorda/actions/runs/39989268650)
passes; read-only metadata identifies the organization secret and no repository
shadow. This does not prove credential validity, write access or delivery.

The original candidate and complete gate evidence are retained under
`/tmp/recorda-031-candidate-nkrd225g`, owned by Recorda #26 with review at the next
publication/retirement decision. Use the original file and successful candidate
run **39989597891**; do not rebuild or tag a later documentation commit. No
0.3.1 tag, upload or public Release was created during preparation. #30 is closed;
#26 remains open for the publication decision and public-only receiving.

The following preparation rationale retains its original pre-gate scope.

The active task is to prepare **0.3.1**, carrying the latest-support-provider
compatibility accepted in #24 and the retained diagnostic setup qualified in
[#29](DIAGNOSTIC_SETUP.md). Receiving source baseline:
`ebe95dcc8528cfa4760951a87c818b812c4ebbba`. The new candidate needs its own exact
committed source, successful source gates, original Conda artifact and full
installed Linux x86_64/macOS arm64 Python 3.11–3.14 gates. Preparation does not
tag, publish or qualify that artifact in advance.

Current source admits ArgDigest `>=0.15.0,<0.17` and SMonitor `>=0.19.0,<0.22`.
The selected public receiving cohort is ArgDigest **0.16.0 py_0**, SMonitor
**0.21.0 py_2** and transitive DepDigest **0.15.1 py_0**. Read
[LATEST_SUPPORT_RECEIVING.md](LATEST_SUPPORT_RECEIVING.md) for original file
identities. Version **0.3.0 remains the latest public release**, with its original
narrower dependency ceilings and immutable artifact. Source/editable receiving
does not make the new cohort installable with the historical public package.

Completed work must not be reopened as a blocker:

- Original standalone and Lab acceptance (#1 in both repositories) is complete.
- Recorda #24 accepted latest-provider compatibility in source. Recorda #29
  retained the safe first-use baseline, nonemitting inspection and explicit
  recovery behavior, with scoped receiving evidence; optional capabilities
  have named reassessment triggers rather than assumed adoption.
- [MOLI #62](https://github.com/uibcdf/moli/issues/62) is **closed** with archived
  direct-owner decisions. Future integration needs a separately owned question;
  MOLI routing is not a pending prerequisite for this compatibility release.

Next: qualify the new candidate under [RELEASING.md](RELEASING.md), preserve its
original file and digest, and record the actual gate/credential-readiness results
in #26. Publication is a separate final decision. After public-only receiving,
return the immutable delivery receipt to MolSysSuite #82, MOLI #40 and Praxis #10.
Each receiving consumer owns its adoption; publication alone does not establish it.

Nonblocking tool follow-up: [Recorda #31](https://github.com/uibcdf/recorda/issues/31)
tracks receiving the published pytest-receptor discard-stream fix. The retained
1.1.0 local tool reports a post-verdict `/dev/null` ResourceWarning; native exits
and JUnit totals still agree. Preserve that warning rather than suppressing it.

All older sections below retain their original dates, source identities and
evidence scope. Their historical next-step statements do not override this summary.

## Historical stabilization release and adoption checkpoint — 2026-10-07

The maintainer-authorized **0.3.0** tag identifies qualified source
`101b8ba82f3b3dba7f434a074b3637d072056a18`. The official public Conda artifact is
`recorda-0.3.0-py_0.tar.bz2`, SHA256
`3f86072ed1449ea4d600312fb539caa2d807b611d18ac8faab10374f7b330e33`.
Source [CI 37595326267](https://github.com/uibcdf/recorda/actions/runs/37595326267)
passes all **14 jobs** and exact-Conda
[candidate 37595337965](https://github.com/uibcdf/recorda/actions/runs/37595337965)
all **10**, including **345 passes per Linux x86_64/macOS arm64 Python 3.11–3.14
cell**. Every installed receipt confirms the same source/digest and all 15 runtime
files. [Publication](https://github.com/uibcdf/recorda/actions/runs/37598242844)
uploads that retained file without rebuilding; independent public-registry and
anonymous-download checks match its SHA256 and main label.

The [release receipt](evidence/release_0_3_0.json) retains source/run identities,
artifact/closure metadata, published receptor captures, coverage acceptance and
public channel installation evidence. Codecov accepts the exact main commit with
91.96% service coverage; coverage.py reports 94% combined statement/branch coverage.
The separately scoped [scientific receipt](evidence/release_0_3_0_scientific.json)
records the exact Conda with unchanged Lab/SciPy/native Sabueso participants:
**420 passes/four historical skips**, seven notebooks/55 code cells and 14 kernel
fault cells on Linux Python 3.14. Earlier receipts keep their original identities.

The API/schema remain experimental before 1.0. Distribution, installed-platform
and coverage evidence belong to `uibcdf/recorda#3`, `uibcdf/recorda#4` and
`uibcdf/recorda#6`. Shared registry reconciliation is separately owned in
`uibcdf/moli#62`. Follow [RELEASING.md](RELEASING.md) for future candidates.
The current direction is to **wait for consumer-owned adoption by MOLI components
and MolSysMT**, then respond to concrete receiving feedback.

Start here when resuming, then read [NEXT_STEPS.md](NEXT_STEPS.md) and the
maintained guide for the behavior being changed. Recorda remains an experimental
standalone component governed directly by MOLI. This checkpoint records completed
work and proposed next work; it does not authorize a new release or integration.

## Original standalone acceptance completed

`uibcdf/recorda#1` and `uibcdf/recorda-lab#1` are resolved against their original
criteria. [STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md) maps each criterion
to installed/fault/producer-free checks and the bounded real SciPy/Sabueso trials.
The [consolidation receipt](evidence/standalone_acceptance_consolidation.json)
retains **101 fresh targeted passes**, two fresh five-scenario artifact sets and
ten journals read with Recorda/stdlib alone. All 15 runtime and 67 Lab source
files match the previously qualified native scientific manifest. Existing
scientific and current-core hosted runs were reinspected with published
gh-run-receptor 1.2.0; their separate source scopes and counts remain unchanged.

This completes the minimal experimental substrate/laboratory, with provisional
API/schema. At that acceptance checkpoint, packaging, installed-candidate OS evidence, coverage, new scientific
questions and shared integration retain their separate gates. The original
coordination analyses are archived; at that point the next engineering work was
`uibcdf/recorda#3`, now qualified by the release above.

## Native Conda provider preflight correction

`uibcdf/recorda#23` is resolved by the development checker correction at Recorda
`9228c84f78221442a4ceb0cfbc45887a919d8367`. It accepts both native Conda's
archive-relative noarch paths and micromamba's installation-relative paths,
matching the actual installed `files` inventory. Exact published coordinates,
import ownership and Python-byte checks remain mandatory; escaping paths and
duplicate mapped entries are rejected.

Linux Python 3.14.7 with published pytest-receptor 1.1.0 passes **331 source tests**
and **331 installed-wheel tests**, including **26 new verifier regressions**.
Both real prefixes pass both feature checks, each verifying **94 provider Python
files**. Governance, dependency routes, Ruff and pip checks pass. All 15 runtime
files match the previous qualified source bytes. The
[local receipt](evidence/conda_noarch_local.json) retains provider-record, source,
runtime, wheel and log hashes. [Exact-source CI](https://github.com/uibcdf/recorda/actions/runs/37587276559)
passes all **11 jobs**, inspected with published gh-run-receptor 1.2.0. Actual
installed logs report 319 passes/12 opt-in recovery skips in six default lanes
(Linux Python 3.11–3.14, macOS 3.13/3.14), and 331 passes in each of four Linux
recovery lanes. The [hosted receipt](evidence/conda_noarch_hosted.json) retains
the full capture hashes and ten successful provider preflights. Hosted
provisioning uses micromamba; actual native Conda evidence is local.

The historical Lab #15 receipts retain their original checker failure and explicit
mapping workaround. This correction does not promote a new Lab default, change
scientific code or requalify those earlier experiment receipts.

## Native Sabueso diagnostic receiving trial

`uibcdf/recorda-lab#15` executes the real producer question: a Card was returned,
but which requested source was partial or failed, which native diagnostic was
delivered, and to which attempt does it belong? Clean Sabueso
`68dac8f8bfc35944f5b6dd59aca8cb2a2819388d` is an ordinary source-built installed
wheel with published support providers. Its source and Recorda's runtime remain
unchanged. The fixture transport uses attributed public UniProt data and explicitly
fictional RCSB-shaped responses; source connections are forbidden.

The corrected installed pair passes **380 tests/four historical Sabueso skips**
(305 core + 75 Lab), including **16 new native receiving cases**, seven notebooks/
**55 cells** and **14 kernel-fault cells**. Native source status, execution and
conditional diagnostic observation have independent acceptance checks. [Exact-pair CI](https://github.com/uibcdf/recorda-lab/actions/runs/37584430143)
passes all **13 jobs** at Lab `a0376799c25c6b650ffa79aa6e4012601892d24c`;
actual native lanes report 47 passes each on Python 3.11–3.14. Published
pytest-receptor 1.1.0 and gh-run-receptor 1.2.0 were used.

Read [Lab's native trial](https://github.com/uibcdf/recorda-lab/blob/main/devguide/SABUESO_DIAGNOSTICS.md)
and its frozen source/wheel/provider evidence. Existing explicit references answer
this bounded question. Any automatic ordinary-call integration needs a separately
scoped public context/attachment decision; MOLI routing is unchanged.
The historical trial encountered the native Conda noarch-metadata preflight
limitation owned by `uibcdf/recorda#23`; the subsequent correction is described
above. Local Lab evidence explicitly mapped and byte-verified its closure;
it does not claim the older core checker passed. Historical Sabueso tests
remain distinct from this new native diagnostic scenario.

## Previous controlled producer diagnostic comparison qualification

Lab #14 qualifies both existing-reference alternatives at Lab implementation
`214a68d93a878bfe2b0d70a3aa90f81e00620db1`, paired with existing Recorda
`48a6c9a0630027f0f2c3d8d82215de8e27764913`. Native science, core runtime,
dependencies and the workflow Recorda default remain unchanged. Local installed
checks pass **364 tests/four explicit Sabueso skips** (305 core + 59 Lab), including
**31 new cases**, seven notebooks/**55 cells**, and **14 kernel fault cells**.

[Exact-pair CI](https://github.com/uibcdf/recorda-lab/actions/runs/37581680564)
passes all nine jobs. Actual logs report 364 scientific/recovery passes/four skips,
50 passes/13 optional skips per Python 3.11–3.14 kernel lane and six dummy passes
per minor. Published pytest-receptor 1.1.0 and gh-run-receptor 1.2.0 were used.
Lab's [maintained decision](https://github.com/uibcdf/recorda-lab/blob/main/devguide/DIAGNOSTIC_ASSOCIATION.md)
and local/hosted receipts retain source/wheel/provider/capture hashes. Closing
documentation preserves every qualified source byte.

Selected associations answer the controlled attempt question with bounded codes,
identities and explicit gaps; reviewed native bundles retain more diagnostic detail.
The producer is a synthetic consumer, not native dummy/SciPy SMonitor emission.
These results do not justify an automatic core bridge or complete capture. A real
producer/user question and a separately owned public context/attachment decision
are required for a further integration slice.

## Previous inspection-view receiving qualification

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
Core #15 producer-operation correlation analysis and the controlled Lab #14
comparison are complete, as recorded below.

## Producer diagnostic association decision

The original architectural decision below retains its own pre-Lab evidence scope.

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
selection or reference-check work. At that pre-release checkpoint runtime metadata
remained 0.2.0; source was identified by commit as well as version. Lab's dummy
remains 0.0.0. That historical checkpoint did not qualify a new installed release
candidate, public registry state, OS support, authenticated integrity, full
dependency closure or replay. The 0.3.0 release evidence is recorded above.

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

## Historical next-work order — 2026-10-07

1. **Wait for receiving adoption** by MOLI components and MolSysMT. Each consumer
   owns its semantic boundary, native records and exact installed receiving gate.
   Use the public 0.3.0 artifact; do not infer adoption from publication alone.
2. **Respond to concrete feedback** in the owning repository. The 0.3.0 release
   resolves local packaging/OS/coverage qualification (#3/#4/#6); a future source
   or build change needs a new candidate. Keep 0.1.0, 0.2.0 and 0.3.0 immutable.
3. **Track shared ecosystem reconciliation** in
   [uibcdf/moli#62](https://github.com/uibcdf/moli/issues/62). The local review
   `uibcdf/recorda#2`, published-provider adoption and receiving trials are complete;
   the central registry decision is separately owned. [SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md)
   preserves all four applicability decisions and reassessment triggers.
4. **Choose a new scientific scenario only for a concrete question**, with an
   independent oracle, omissions and interruption cases in its own Lab issue.
   Existing references answer the qualified source/attempt question. Core automatic
   attachment requires a separately scoped public contract decision.
5. **After a concrete integration need**, read MOLI's `devguide/RECORDA.md` and
   open shared-contract work there. ProjectContext/EventLedger/ProjectRecord,
   cross-process routing and replay remain future work. Standalone Recorda
   retains no MOLI runtime dependency. Original standalone acceptance #1 in both
   repositories is complete; these gates do not reopen that experimental slice.

## Subsequent local acceptance assessment

`uibcdf/recorda-lab#10` completed the preparation/fitting/evaluation workflow and
was closed after direct integration into main. Read
[STANDALONE_ACCEPTANCE.md](STANDALONE_ACCEPTANCE.md) for the scientific questions,
local receipt and separate hosted Jupyter/SciPy qualification. Core runtime and
the previously published source pair above are unchanged; the new Lab evidence
does not replace their historical hosted results.

## Historical ecosystem boundary audit

[SUPPORT_LIBRARIES.md](SUPPORT_LIBRARIES.md) and
`evidence/ecosystem_boundaries_local.json` record the current-runtime audit in
`uibcdf/recorda#2`, with 91 core regressions passing locally under published
pytest-receptor on Python 3.14.7. The initial basic-guard/future-diagnostic rationale
is superseded by explicit ArgDigest/SMonitor applicability. Adoption remains
partial; no runtime dependency, accepted exception or registry promotion follows
from the classification alone.

At that audit, standalone acceptance and engineering reviews remained open.
Original acceptance is now resolved by the separate consolidation above;
distribution, OS and coverage retain their independently owned obligations.

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
decision and completed Lab #14 comparison are recorded above.
