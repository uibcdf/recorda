# Stable packaged description

Owner: `uibcdf/recorda#32`. Release: `uibcdf/recorda#33` (0.3.2).

Delivered in [0.3.2](evidence/release_0_3_2.json): actual wheel, original Conda,
all eight installed candidates and both public OS installations agree on the
description digest. Public download inspection and all three Release assets
verify; #32 is resolved without changing the historical 0.3.1 archive.

`pyproject.toml` selects **PACKAGE_README.md** for installed METADATA. It contains
stable purpose, usage, scope and absolute documentation/release links. The live
README carries release status independently. A public promotion therefore keeps
the tested package bytes without embedding a temporary unpublished/candidate
assertion. The immutable 0.3.1 archive retains its original build-time description.

The candidate inspector reads the actual archive METADATA and checks its Markdown
content type and full description against the declared file. The manifest binds
the exact source file and normalized description SHA256. Normalization decodes
UTF-8, maps CRLF to LF and removes terminal newline characters; it preserves
other spaces, content and scientific wording. Installed/public checks verify the
same description digest from installed distribution metadata.

`tests/test_release_candidate.py` rejects stale descriptions and wrong content
types, exercises UTF-8, guards the independent source choice and shows that
changing live release-status prose does not change the packaged description.
The actual wheel and original Conda archive require inspection as well as unit
fixtures; no source declaration alone qualifies the delivered metadata.

Keep release state in maintained guidance and receipts. Version, tag, runtime,
dependency and original-file checks remain mandatory. This changes packaging
description and developer verification, not the experimental recording API or
journal schema, and does not rewrite earlier releases.
