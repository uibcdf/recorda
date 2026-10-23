# Stabilization release qualification

## Current preparation — 0.3.1

Owner: `uibcdf/recorda#26`. The selected compatibility patch is **0.3.1**;
the public 0.3.0 release, tag and original artifact remain immutable. Source,
recipe and runtime version must agree, and current published-provider identities
remain pinned in the environment specifications. No schema or public API change
is selected. Historical 0.3.0 evidence below does not certify this candidate.

Commit the reviewed candidate, pass the 14-job exact-source workflow, then run
`release_candidate.yml` with its full `candidate_sha`. Its 10 required jobs must
build once and test the same `recorda-0.3.1-py_0.tar.bz2` on Linux x86_64 and
macOS arm64 for Python 3.11–3.14, with recovery enabled. Retain the manifest,
source/run identities, original file and SHA256 before a publication decision.

Credential owner/contract: [MOLI #8](https://github.com/uibcdf/moli/issues/8) and
MOLI's distribution policy. Diego Prada administers the selected-repository
organization secret `ANACONDA_UIBCDF_TOKEN`. The publisher explicitly adopts
that canonical name, removing the reviewed legacy `ANACONDA_TOKEN` fallback.
Ordinary source/candidate tests receive no publication credential.
`publication_readiness.yml` is a trusted **manual main-branch** presence-only
check with no checkout, package input, upload or token output. The selected
publisher checks presence again before work. Record the actual readiness run
and administrator disposition in #26; presence alone does not establish a grant,
validity or a successful upload. Request missing access from Diego in that issue.

Only after authorization, create the new annotated `0.3.1` tag on the qualified
source and use `build_and_upload_conda_packages.yaml` with the successful
candidate run and retained digest. Upload the exact original file; never rebuild,
overwrite an occupied coordinate or retag. Independently verify public registry
and clean channel installs. A GitHub Release title must be exactly `0.3.1`,
matching its tag and package version. No tag or upload is part of preparation.

At closeout, retire owned environments/build scratch after final evidence
extraction. Retain original candidate bytes and proof with an owner and a next
review trigger through the publication decision. Provider/adoption feedback goes
to MolSysSuite #82, MOLI #40 and Praxis #10 after actual delivery.

## Historical procedure and evidence — 0.3.0

For any future public GitHub Release, verify before creating or editing it
that the visible title (`name`) is exactly the canonical `X.Y.Z` version,
equal to the tag and package version. Use `gh release create X.Y.Z --title X.Y.Z`
or set the API `name` and `tag_name` identically. Put descriptive text in
the release notes and verify the resulting metadata. This instruction does
not retroactively change the 0.3.0 release receipt below.

The maintainer has authorized a stabilization tag and official package, followed
by a pause for consumer adoption. The selected public version is **0.3.0**.
This remains a pre-1.0 experimental API and journal schema. Consumer adoption
belongs to receiving MOLI components and MolSysMT; it does not introduce a MOLI
runtime dependency or imply arbitrary-call capture, complete workflows or replay.

The executed 0.3.0 qualification and publication are recorded in the
[release receipt](evidence/release_0_3_0.json),
[scientific receipt](evidence/release_0_3_0_scientific.json) and
[GitHub release/finalization receipt](evidence/release_0_3_0_github.json).
The original publication route finishes with three successful jobs on attempt 2;
only the previously unstarted macOS installation was rerun. The upload executed
once. A temporary alternative CI route was withdrawn after the original route
succeeded, and the qualified configuration was restored without changing the tag
or artifact. Cancelled alternatives are not qualification evidence.
The procedure below describes those gates; a future version must select and qualify its own exact identities.

Ownership: distribution `uibcdf/recorda#3`, installed-platform qualification
`uibcdf/recorda#4`, coverage `uibcdf/recorda#6`. The original standalone acceptance
is complete in `uibcdf/recorda#1` and `uibcdf/recorda-lab#1`. Existing scientific
receipts keep their original participant identities; they are not certificates
for a newly built package.

## Candidate before tag

Commit the candidate on main and retain its full SHA. Metadata, runtime version
and `devtools/conda-build/meta.yaml` must agree. Run governance, Ruff, dependency
preflight and published pytest-receptor. Exact-source `Tests and governance`
includes quality, eight installed-wheel Linux/macOS arm64 Python 3.11–3.14 cells,
four recovery-provider cells and an installed-runtime coverage producer.

Manually dispatch `Conda release candidate` with that SHA. The reviewed published
UIBCDF action v2.3.0 builds once without upload. Preserve the tarball, manifest and
build receipt. The manifest binds version, immutable coordinate, SHA256,
dependency metadata and every delivered runtime Python file to that source.
Recorda has no generated or vendored runtime resources.

Eight jobs install that **same Conda file** on Linux and macOS arm64, Python
3.11–3.14, verify installed bytes and Conda metadata, exercise recording and CLI,
and run the full suite with published pytest-receptor and recovery enabled.
Linux 3.14 additionally measures branch and statement coverage; a separate job
uploads its XML through Codecov OIDC. Path normalization maps only byte-identical
installed files to repository sources and leaves measured counts unchanged.
Do not show a coverage badge until the service accepts a recent main report.

Inspect both runs with published gh-run-receptor and preserve native GitHub job
conclusions. All 14 source jobs and all 10 Conda-candidate jobs must succeed;
configured jobs and historical green runs do not qualify the new candidate.
Check that an Anaconda upload credential is available to Actions. Missing access
must be configured without recording token values in issues, logs or chat.

## Tag, exact-file publication and independent verification

After the prerequisite gates, create annotated tag `0.3.0` on the qualified SHA
and push that tag explicitly. Never move an existing public tag. Dispatch
`Publish qualified Conda package` with the source SHA, successful candidate run ID
and expected file SHA256. Its guard checks the tag and both exact-source runs.

The official UIBCDF exact-file upload action checks all labels before uploading
`uibcdf/recorda/0.3.0/noarch/recorda-0.3.0-py_0.tar.bz2` to `main`. An occupied
coordinate blocks upload, even when its bytes match. No force overwrite or build
during publication is permitted. If upload has an uncertain outcome, inspect the
registry read-only before any retry; never re-upload to an occupied coordinate.

Independent public-registry observation must match the retained file SHA256 and
main label. Fresh Linux and macOS arm64 environments then solve the public channel
package and verify installed provenance and representative recording/inspection.
Create GitHub Release `0.3.0` with that exact artifact, manifest and checksums only
after public evidence succeeds. Verify the existing tag object and peeled source
independently; when creating the release for that existing tag, omit `--target`.
The GitHub API ignores `target_commitish` for existing tags, so its default `main`
metadata does not replace the tag's source identity. The official route is Conda `uibcdf` with
`conda-forge`; no PyPI or DOI/archive availability is claimed.

Record the actual source/run IDs, artifact hashes, coverage acceptance and public
installation results in issues and a release receipt. Update the status and
adoption guidance in a subsequent documentation commit; the immutable tag remains
on its qualified candidate. If candidate source or build inputs change, qualify
the replacement explicitly rather than borrowing earlier results.
