---
summary: Complete support-library adoption at the current Recorda-owned boundaries.
issue: uibcdf/recorda#2
status: partial
opened: 2026-10-06
closed:
verification: reproduced
area: [engineering, arguments, diagnostics]
blocked_by: []
supersedes: []
---

# Current ecosystem boundary review

## What

Assess ArgDigest, DepDigest, SMonitor and PyUnitWizard against the current
standalone prototype. Keep the maintained classification and adoption criteria
in [../SUPPORT_LIBRARIES.md](../SUPPORT_LIBRARIES.md).

## How / evidence

The audit inspects Recorda `c695b39f655f55ca1928f7fd5f7735ba8ab21a8d` under MOLI's
support-library policy and verifies current core regressions with published
pytest-receptor on Python 3.14. The source/import/test receipt is
[../evidence/ecosystem_boundaries_local.json](../evidence/ecosystem_boundaries_local.json).

`CapturePolicy` now canonicalizes profiles; reference checking has public option
constraints. ArgDigest applicability is no longer covered by a blanket claim
that every guard is basic. Operation/session completion fault handlers already
append recovery advice to native exceptions, making SMonitor applicable now.
The recovery adapter in `uibcdf/recorda#16` now exercises the resolved SMonitor
source APIs through explicit selection; published-provider qualification follows
in `uibcdf/recorda#18` with SMonitor 0.19.0 and ArgDigest 0.15.0.
That published-provider qualification is complete: all 15 jobs pass at
`2b8b3deecc43dc65e6c34e440dfeb0cbe3d29891`, including eight Linux
Python 3.11–3.14 provider lanes. See [../archive/published_support.md](../archive/published_support.md).
See [../RECOVERY_DIAGNOSTICS.md](../RECOVERY_DIAGNOSTICS.md) and its executed receipt.
The resolved explicit ArgDigest capture experiment in `uibcdf/recorda#17` exercises
both contract axes against pinned development sources with mandatory core guards;
all 15 jobs pass at its code/test commit, including Python 3.11–3.14 provider lanes.
Default configuration now uses ArgDigest under `uibcdf/recorda#19`, with required
metadata, aligned Conda routes and a local recipe/preflight. Reference-check
contracts remain in #20. The original optional integration route's
receipt is [../evidence/published_support_local.json](../evidence/published_support_local.json);
default-adoption evidence is [../evidence/default_arguments_local.json](../evidence/default_arguments_local.json).
See [../ARGUMENT_CONFIGURATION.md](../ARGUMENT_CONFIGURATION.md).
DepDigest has no current core backend loader, and
PyUnitWizard has no quantity parsing/conversion/validation boundary.

Published SMonitor 0.18.0, ArgDigest 0.14.0 and DepDigest 0.13.0 Conda archive
hashes and required metadata match the solver index. The candidate closure admits
Python 3.11–3.14 without a required scientific package or reverse dependency
cycle. This is inspected metadata, not installed integration qualification.

## Why

The original review predates selection and persistence-recovery work. A
stdlib-only implementation is not itself an exemption from the current policy.
Explicit boundaries prevent both unjustified dependencies and missed adoption.

## Alternatives

Adding all four packages mechanically would introduce unused core dependencies.
Wrapping arbitrary scientific calls would expose producer-owned arguments and
errors and change the inactive path. Claiming an exception or adoption without
qualification is also rejected. Implement one bounded Recorda-owned boundary
at a time, with published-provider and compatibility evidence.

## Acceptance criteria

- Keep current applicability and reassessment triggers explicit for all four providers.
- Adopt SMonitor for safe recovery diagnostics without replacing native exceptions,
  losing incomplete outcomes or exposing scientific content.
- Adopt ArgDigest for Recorda-owned configuration contracts while retaining
  mandatory capture, filesystem and lifecycle invariants.
- Qualify the chosen published versions, supported-minor behavior and dependency
  closure; synchronize metadata, Conda provisioning and the distribution review.
- Synchronize MOLI's registry only after adoption evidence or a governed exception
  exists, and preserve this resolved analysis in the archive when the theme closes.

## Resolution

Partial. Current-runtime classification, regressions and the bounded source-provider
recovery/configuration integrations are recorded. Default CapturePolicy adoption
is tracked in #19; reference-check contracts and complete release qualification
remain open in
`uibcdf/recorda#2`; MOLI's registry
remains `partial`. No public Recorda release, registry promotion or policy exception is claimed.
