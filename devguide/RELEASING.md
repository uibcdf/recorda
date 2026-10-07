# Stabilization release qualification

The maintainer has authorized a stabilization tag and official package, followed
by a pause for consumer adoption. The selected public version is **0.3.0**.
This remains a pre-1.0 experimental API and journal schema. Consumer adoption
belongs to receiving MOLI components and MolSysMT; it does not introduce a MOLI
runtime dependency or imply arbitrary-call capture, complete workflows or replay.

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
after public evidence succeeds. The official route is Conda `uibcdf` with
`conda-forge`; no PyPI or DOI/archive availability is claimed.

Record the actual source/run IDs, artifact hashes, coverage acceptance and public
installation results in issues and a release receipt. Update the status and
adoption guidance in a subsequent documentation commit; the immutable tag remains
on its qualified candidate. If candidate source or build inputs change, qualify
the replacement explicitly rather than borrowing earlier results.
