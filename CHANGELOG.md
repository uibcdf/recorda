# Release history

## 0.3.0 — stabilization candidate

The standalone experimental slice is complete. This release prepares adoption
by scientific consumers while the API and JSONL schema remain provisional.

- Adopt published ArgDigest 0.15.0 and SMonitor 0.19.0 for Recorda-owned
  configuration, reference-check contracts and explicit technical presentation.
  Recovery diagnostics remain explicitly selected.
- Add read-only inspection views beside structured native facts, preserving
  execution outcomes, ownership, safe omissions and supplied-check scope.
- Qualify independent dummy, real SciPy and offline native Sabueso consumers,
  including interruption, native failures/retries and conditional diagnostics.
- Verify native Conda and micromamba noarch provider metadata without weakening
  installed ownership or Python-byte checks.
- Add digest-bound Conda candidate qualification and publication gates.

- Add explicit local file resolution and bounded reference checks, distinguishing
  byte matches, availability, loss, alteration, unsupported digests, omissions
  and incomplete execution. Native scientific semantics remain owner-specific
  (`uibcdf/recorda#12`, `uibcdf/recorda-lab#9`).

- Add optional session `CapturePolicy` for declared profile selection and payload
  detail. Selected lifecycle facts remain mandatory; exclusions use bounded
  aggregate coverage and disabled adapters are bypassed (`uibcdf/recorda#11`,
  `uibcdf/recorda-lab#8`).

- Manual finalization can close an idle session as incomplete after an operation's
  terminal write fails. Native errors, persisted prefixes, context ownership and
  the stop barrier for running async work are preserved (`uibcdf/recorda#8`).

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
