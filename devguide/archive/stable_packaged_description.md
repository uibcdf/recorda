---
summary: Keep delivered package descriptions independent of transient release status.
issue: uibcdf/recorda#32
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [packaging, metadata]
blocked_by: []
supersedes: []
---

# Stable packaged description

The immutable 0.3.1 METADATA correctly identified Version 0.3.1 but retained
build-time README candidate/publication prose. Updating a live README cannot
change an already sealed archive. Preserve that historical artifact and deliver
the fix in a new independently qualified coordinate.

PEP621 now selects `PACKAGE_README.md`, with stable purpose/usage and absolute
release/documentation links. Live release status remains in the repository
README/checkpoint. `devtools/release_candidate.py` checks actual archive Markdown
metadata against the source, binds source/payload hashes and checks the installed
payload. Normalization decodes UTF-8, maps CRLF to LF and removes terminal newline
characters without changing other content/spaces.

Guards: `tests/test_release_candidate.py` checks the independent source choice,
UTF-8, stale content, wrong media type and live-README status independence.
Actual wheel, original Conda, eight installed candidates and both public channel
installations all match normalized description SHA256
`958858344b752a4e359b9f53fd505137b5cf5e5011c0efbfcb339f7fc6ebafbe`.
The public archive contains the stable body, not old release/candidate claims.

Delivered as original 0.3.2 file SHA256
`d6293cfb48110baada88653beaa52250554558e858311fe409245eeac5372ede`, source
`e97ec6055e7110b37aac87a7c810c2da3f732c92`. See
[release receipt](../evidence/release_0_3_2.json) and
[maintained contract](../PACKAGED_DESCRIPTION.md). The runtime API/schema and
existing archives/tags are unchanged. This is metadata correctness and usable
artifact receiving, not a scientific-validity or replay certificate.
