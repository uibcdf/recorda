---
summary: Qualify and publish 0.3.3 with permissive runtime provider requirements.
issue: uibcdf/recorda#37
status: resolved
opened: 2026-10-24
closed: 2026-10-24
verification: measured
area: [distribution, engineering, release]
guard: tests/test_publication_route.py::test_candidate_and_publication_routes_use_the_current_package_coordinate
blocked_by: []
supersedes: []
---

# Release 0.3.3

## Authorization and scope

Diego requests 0.3.3 after #34/#35 receiving. Starting source is
`5f11e250079df26145f160e76763353641ca285b`. Deliver minimum-only runtime
provider requirements in the public package, retaining the qualified cohort,
latest-public monitoring and experimental API/schema. Runtime changes only
the canonical version. Preserve previous tags/files and historical evidence.

## Acceptance

- Package/runtime/recipe/version routes agree; stable description and actual
  wheel/Conda runtime/dependency metadata match the candidate source.
- Fresh local source/installed checks, 14 exact-source jobs, two latest-public
  jobs and ten original-Conda qualification jobs pass with published tools.
- Trusted canonical credential readiness executes without exposing values;
  actual same-file publication follows all gates and a blocker review.
- Verify original artifact bytes, registry and clean public Linux/macOS installs;
  create the Release titled exactly 0.3.3 with matching tag/package and assets.
- Deliver availability through owning domain/consumer issues, archive receipts
  and retire owned disposable resources while retaining useful evidence with
  an owner and review trigger.

## Resolution

0.3.3 is publicly delivered. Source/tag target:
`99f6ca12295ef675abebfe8c42cbd3ad7881bb07`; annotated object:
`d84688ce83ff27a5927b8934553b77b953380c27`. Original file:
`recorda-0.3.3-py_0.tar.bz2`, 23642 bytes, SHA256
`fcee216130bca444e92e195fc38f8ef24fb501439cd123638bc11fa8e5df76ea`.

Local source and private installed wheel pass 408 tests each. Exact-source
40141263674 passes 14 jobs, latest-public 40141291843 two (408 each), original
Conda 40141291792 ten (408 in each of eight Linux x86_64/macOS arm64 Python
3.11–3.14 cells), and publication 40142058462 three on attempt 1. Trusted
presence-only readiness passes; upload receipt verifies all-labels absence and
one original-file upload without rebuilding. The additional tag source CI also
passes 14 jobs. Thirty full capture members and 53 local tested-input hashes
are independently verified.

Actual archive requirements are minimum-only, with all 15 runtime files and
stable description matching the manifest. Public registry/main label, anonymous
Conda download, hosted public Linux/macOS installs and a separate fresh public-only
Linux installation verify the original file and recording/CLI behavior with clean
dependency closure. [Release 0.3.3](https://github.com/uibcdf/recorda/releases/tag/0.3.3)
has canonical title/tag/package version, is public/non-prerelease, and all three
assets anonymously download byte-identical to the original archive, manifest
and checksums, agreeing with API digests and sizes.

The guard rejects stale candidate/publisher coordinates when versions change;
`tests/test_release_candidate.py` additionally protects source/artifact identity,
descriptions and installed metadata. Runtime changes only the canonical version.
Actual [release evidence](../evidence/release_0_3_3.json) and
[candidate proof](../evidence/candidate_0_3_3_hosted.json) preserve every original
identity; no historical result is substituted for new qualification.

Availability is delivered through release-specific MolI #78 / MolSysSuite #142,
with wider policy evaluation in #76/#137 and consumer receiving independently
owned. No automatic adoption, future-version certification or scientific replay
is implied. Actions runtime maintenance remains separate in Recorda #36; its
annotations have caused no native gate failure. Owned disposable resources are
retired after evidence extraction; useful original-artifact proof has an owner
and review trigger in [resource closeout](../evidence/release_0_3_3_resources.json).
