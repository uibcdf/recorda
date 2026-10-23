---
summary: Qualify and publish the original 0.3.2 maintenance artifact after tool and description fixes.
issue: uibcdf/recorda#33
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [release, distribution, maintenance]
blocked_by: []
supersedes: []
---

# Recorda 0.3.2 maintenance delivery

Diego authorizes fixing #31/#32 and publishing 0.3.2 when qualification succeeds
and no release blocker remains. Both fixes close with actual receiving evidence;
the final pre-publication open-issue inventory contains only this release issue.
Keep old tags/bytes intact and choose a fresh immutable coordinate.

Qualified source: `e97ec6055e7110b37aac87a7c810c2da3f732c92`. Annotated tag object:
`1dead4ec102cdb584b756eb3f2e7cee225773c6b`. Original archive:
`recorda-0.3.2-py_0.tar.bz2`, SHA256
`d6293cfb48110baada88653beaa52250554558e858311fe409245eeac5372ede`.

Source 40003836709 passes 14 jobs; exact-Conda 40004306942 passes 10, including
376 tests per Linux x86_64/macOS arm64 Python 3.11–3.14 cell. All eight receipts
bind identical source/file/runtime/description data. Source ordinary lanes retain
18 explicit recovery exclusions; explicit recovery and candidate lanes run all
376 tests. Both llm/ci receiving modes run on every minor through their regression.
No skipped gate is relabeled. The extra tag source CI also passes all 14 jobs.

Trusted canonical-credential presence-only readiness 40003902707 succeeds without
token disclosure or candidate-build access to a publication secret. Publication
40005577937 uploads the original file once and passes both public-channel OS
checks, all three jobs successful. Registry labels/digest, anonymous download,
actual METADATA and all three GitHub Release assets independently verify.
Release title, tag and package version are exactly 0.3.2. The file was not rebuilt
or overwritten at upload; a later documentation commit is not the tagged source.

The [release receipt](../evidence/release_0_3_2.json) preserves full input/gate
identities, 24 complete verified capture members, original artifact and public
observations. [Tool](pytest_receptor_1_2_1_receiving.md) and
[description](stable_packaged_description.md) analyses retain their separate
acceptance. Local source/installed suites each pass 376 tests with complete
artifact/JUnit/native agreement and zero warnings.

Only the runtime version identifier changes among the 15 delivered Python files;
provider ranges and scientific recording behavior remain unchanged. Native
scientific acceptance/adoption, replay and MOLI routing are separately owned.
No PyPI/DOI claim is made. MolSysSuite #130 is updated to current 0.3.2 availability
while preserving 0.3.1 history; related coordinations receive the same public proof.

Owned environments/scratch retire after proof extraction. Original artifacts and
complete audit proof retain owner/review triggers in
[resource closeout](../evidence/release_0_3_2_resources.json). Shared active work
and older independently scoped evidence are preserved.
