---
summary: Receive the published test-tool stream cleanup with native verdict and artifact checks.
issue: uibcdf/recorda#31
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [testing, tooling]
blocked_by: []
supersedes: []
---

# Published pytest-receptor receiving

The old 1.1.0 pin retained a post-verdict discard-stream ResourceWarning despite
the source fix in `uibcdf/pytest-receptor#4`. Receive published **1.2.1**, PyPI
wheel SHA256 `683200648785f3894357891b238cdc0780c1e874dcf067882dbba2aaa2c527c3`;
six installed Python files independently match it. All four applicable Conda
specifications, explicit CI installs and maintained guidance select that pin.

Guard: `tests/test_receptor_receiving.py`. Eight fresh-process cases cross llm/ci,
success/failure and statistics. ResourceWarning is explicitly visible; no warning
or late writer failure is suppressed. Native exits, terminal verdicts, JUnit
counts and complete integrity-checked JSONL agree. Controlled nested failures
are fixtures, not failed release gates. Sixteen local receiving artifacts verify.

Source and installed-wheel suites each pass 376 tests without warnings. Exact
source 40003836709 passes all 14 jobs; candidate 40004306942 all 10, with 376 tests
per Linux x86_64/macOS arm64 Python 3.11–3.14 cell. The regression runs in those
actual installed lanes; closure is based on usable receiving, not the provider's
earlier source-only issue closure. Historical warnings remain in old receipts.

Delivered in 0.3.2 under `uibcdf/recorda#33`; see
[release_0_3_2.json](../evidence/release_0_3_2.json) and
[current contract](../TEST_TOOL_RECEIVING.md). The tool is a development/CI
dependency, not a runtime requirement, and this does not qualify scientific
consumer adoption or change recording behavior.
