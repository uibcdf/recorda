---
summary: Qualify an explicit SMonitor adapter for native-failure recovery advice.
issue: uibcdf/recorda#16
status: resolved
opened: 2026-10-06
closed: 2026-10-06
verification: reproduced
area: [diagnostics, recovery, confidentiality]
blocked_by: []
supersedes: []
---

# Explicit source-provider recovery experiment

## What and ownership

Use SMonitor's resolved registration and scoped capture APIs at the two existing
Recorda recovery-advice sites. This is a development integration, with public
provider selection left to the umbrella ecosystem/distribution issues #2/#3.
Inspection presentation (#14) and linking provider diagnostics (#15) are separate.

## Implementation and evidence

The fixed messages now belong to a Recorda catalog. `recovery_diagnostics=None`
keeps its notes without importing SMonitor; an explicit synchronous sink receives
only the known code and Recorda-owned IDs. The SMonitor adapter registers this
catalog without reconfiguring the application and enters a metadata-only scope
before emission. It receives no native/storage error, value or journal path.
Fault-isolated notes preserve native failure propagation when diagnostics fail
or are filtered. The context-local live guard prevents feedback while allowing
tasks created by a sink to emit after its delivery has ended.

[../RECOVERY_DIAGNOSTICS.md](../RECOVERY_DIAGNOSTICS.md) documents activation and
limits. [The local receipt](../evidence/recovery_diagnostics_local.json) records
Python 3.14.7, published pytest-receptor 1.1.0, the source manifest and built
development wheel digest. Core checks pass 104 tests with 12 declared provider
skips; both source-provider and installed-Recorda/source-provider suites pass
116 tests. Governance, Ruff and whitespace checks pass. The provider is SMonitor
source `6feac9728cc35d57cbc92f284d7040d7f04cb35b`, never attributed to its old
published 0.18.0 artifact.

## Alternatives and remaining scope

Global configuration changes, automatic scientific `@signal` wrapping and
forwarding exception/message/path payloads do not satisfy this boundary. The
selected callback remains a caller-owned explicit integration; there is no
automatic backend discovery or capability registry in Recorda. A dependency
extra/floor remains unselected until a new provider is published and qualified.
This is partial ecosystem adoption rather than a policy exception.

## Acceptance criteria

- Preserve existing recording behavior, native identity/cause/traceback and notes.
- Demonstrate both recovery sites and diagnostic failures without unsafe payloads.
- Verify application configuration and independent core import/inspection.
- Verify interleaved contexts, threads, filtered events and recursive delivery.
- Execute the pinned-source installed-Recorda CI lane on Python 3.11–3.14.
- Retain publication/adoption limits and cross-links when closing this experiment.

## Resolution

Local source/installed qualification and hosted source-provider acceptance are complete.
[CI 37498367934](https://github.com/uibcdf/recorda/actions/runs/37498367934) passes
all 11 jobs at code commit `70a98587d9d2f8dce0626fa2bca1bd4a6a932c47`, including
the four installed-Recorda/source-SMonitor Linux Python 3.11–3.14 lanes. Published
gh-run-receptor 1.2.0 inspected the completed run. The closing documentation
checkpoint changes no runtime/test/metadata/workflow byte in the receipt.
Public provider and ArgDigest adoption remain tracked in `uibcdf/recorda#2`.
