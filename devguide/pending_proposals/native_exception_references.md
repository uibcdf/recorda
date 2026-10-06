---
summary: Evaluate safe opt-in references to native exception provenance.
issue: uibcdf/recorda#7
status: open
opened: 2026-10-05
closed:
verification: reproduced
area: [recording, native-references, exception-provenance]
blocked_by: []
supersedes: []
---

## What

The Sabueso laboratory scenario preserves a native ConnectorError carrying its
acquisition_trace. Recorda records the safe exception type and failed operation,
but its input/return adapters do not provide a declared native exception reference.
The caller therefore retains the trace and links it in the Lab index explicitly.

## Evidence and impact

`uibcdf/recorda-lab#5`, the laboratory's `experiments/run_sabueso.py` and its fourth
usage notebook reproduce the extra caller step. The native return/exception identity
regression passes. This is a recording-layer capability proposal, not a Sabueso bug
or a new shared platform contract. The manual step is documented as a coverage gap.

## Alternatives and acceptance

Retaining sidecars manually is adequate for this controlled trial. Before adopting
in library consumers, evaluate a narrow opt-in mechanism at declared boundaries.
Keep hook names provisional. Preserve exact exception identity, traceback and
propagation, native ownership and inactive behavior. Make unsupported exceptions
and adapter failure visible as omissions; never capture arbitrary messages, repr,
exception dictionaries or secrets. Prove those properties with targeted regressions
before changing the core API. Keep standalone code free of MOLI runtime dependencies.
