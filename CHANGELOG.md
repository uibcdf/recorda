# Source checkpoints

## 0.2.0

Experimental checkpoint tracked by `uibcdf/recorda#9`.

- Reuse session-local exact-type reference adapters for native exceptions at declared
  operation boundaries; record a safe reference or explicit omission under
  `exception.reference`.
- Preserve native exception identity, cause and traceback propagation, including
  cancellation. Faulty capture callbacks cannot replace the original exception.
- Read historical type-only failures with the additive provisional journal field.
- Qualify the controlled Sabueso consumer and fourth laboratory notebook without
  manual caller trace retention (`uibcdf/recorda#7`, `uibcdf/recorda-lab#6`).

The manual finalization limitation after a failed terminal write remains tracked in
`uibcdf/recorda#8`. The independent Lab package remains version `0.0.0`.
Artifact identities, installed checks and exact paired CI conclusions belong to
the checkpoint's issue receipt. This tag establishes source tracking; package-channel
publication, public OS support, archival, MOLI routing and replay remain separate work.

## 0.1.0

First experimental source checkpoint (`uibcdf/recorda#5`), retaining standalone
start/stop, optional context managers, declared operations, dormant decorators,
native input/output references, correlation and incremental local journals.
Its tag and historical receipts remain unchanged.
