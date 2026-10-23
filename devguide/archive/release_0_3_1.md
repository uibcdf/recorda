---
summary: Deliver accepted latest-provider compatibility in immutable Recorda 0.3.1.
issue: uibcdf/recorda#26
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [release, distribution, compatibility]
blocked_by: []
supersedes: []
---

# Recorda 0.3.1 compatibility delivery

## What and why

Source receiving #24 admitted current public ArgDigest/SMonitor releases while
the immutable Recorda 0.3.0 package retained older ceilings. A new public file
was needed for consumers to select the accepted public cohort. The patch keeps
the existing runtime behavior, experimental API/schema and dependency floors.
Diagnostic setup #29 and original standalone/Lab acceptance are complete;
closed MOLI #62 is not a release blocker. Checkpoint drift is separately fixed
in Recorda #30.

## Decision and evidence

Select 0.3.1 at exact source `a432cc38fe675ae16eff4f6a0f2f43522b50994b`.
Use original `recorda-0.3.1-py_0.tar.bz2`, SHA256
`8d040ae189d0f47ea0191a142c7e9cc0b57cd9e890303a354d8f463fe34242d9`.
Do not move older tags, overwrite an occupied coordinate or rebuild at upload.

Published provider pins: ArgDigest 0.16.0 py_0, SMonitor 0.21.0 py_2 and transitive
DepDigest 0.15.1 py_0. The new metadata ranges retain prior floors. Fresh local
source and installed-wheel checks each pass 364 tests, using published
pytest-receptor 1.1.0 with explicit recovery and plugin selection. The old tool's
post-verdict discard warning remains visible and is owned in Recorda #31.

Exact-source CI 39989246726 passes all 14 jobs. Candidate run 39989597891 builds
once and passes all 10 jobs, including 364 tests in every Linux x86_64/macOS arm64
Python 3.11–3.14 cell. Eight receipts and independent archive inspection bind all
15 runtime files and the same original source/digest. Ordinary source lanes
retain their explicit 18 recovery exclusions; full recovery/candidate lanes run
all 364 tests. No skipped gate is relabeled as a pass.

Adopt the canonical organization secret under MOLI #8, explicitly removing the
legacy alias. Keep credentials out of candidate build/tests; a trusted manual
main-branch presence-only workflow has no checkout/upload. Availability,
organization metadata/no local shadow, credential validity and actual delivery
are separate observations. Publication run 39991293202 completes its exact-file
upload once and both public-channel Linux/macOS arm64 installations. Independent
registry and anonymous downloads agree. The existing annotated 0.3.1 tag points
to the qualified source; the GitHub Release title/tag/package version are exactly
0.3.1, and all three public assets match the originals.

Machine-readable identities and complete-capture member digests are in
[release_0_3_1.json](../evidence/release_0_3_1.json), with separate local/candidate
and resource receipts. The extra automatic tag CI also succeeds; it does not
replace the original main-source qualification.

## Alternatives and limits

Reject a metadata-only claim of public availability, a replacement of the 0.3.0
file, a rebuild at upload, and any inference that provider availability selects
new optional diagnostic behavior. The original artifact remains the source of
truth. Publisher assertions and `tests/test_release_candidate.py` guard digest,
source, payload and occupied coordinates; `tests/test_publication_route.py`
guards version routing, credential separation and presence-only behavior.

This qualifies the declared package/platform scope. Native scientific meaning,
component records, production instrumentation and receiving adoption remain with
consumers. No automatic call capture, full dependency closure of a scientific
workflow, authenticated scientific identity, replay, PyPI or DOI archival follows.

Post-delivery description inspection finds build-time candidate prose in the
packaged README/METADATA. Its actual Version is 0.3.1; live README/Release
guidance is current. Recorda #32 tracks stable future descriptions without
altering this original artifact. This is separate from runtime correctness and
the successful digest-bound delivery; no failed test is hidden or reclassified.

## Resolution and handoff

Package and Release are public. The requested availability notice is
`uibcdf/molsyssuite#130`, linked to suite #82, MOLI #40 and Praxis #10. Consumers
triage their own receiving; original completed integration scopes are preserved.
Owned test environments and disposable scratch were retired. Original files,
complete proof and their owner/review trigger remain recorded for release audit.
