# Recorda

**Scientific recording and provenance for computational work.**

Activate a recording session once, call instrumented scientific functions normally,
and stop recording. Library authors declare selected semantic boundaries with a
decorator; native return values, exceptions and component-owned records retain
their normal ownership.

```python
import recorda


@recorda.record("example.double", profile="scientific_analysis")
def double(value):
    return value * 2


session = recorda.start("analysis", path="analysis.jsonl")
result = double(3)
record = recorda.stop()
```

Without an active session, the decorated function executes directly. A session
observes declared instrumented boundaries; coverage gaps and omissions remain
explicit. Interrupted or unclosed work can remain inspectable as incomplete.
Native scientific results and provenance stay with their producing libraries.

The public API and journal schema are experimental before 1.0. References and
local byte checks do not establish scientific validity, authenticity or replay.

The official installation route uses the `uibcdf` and `conda-forge` Conda channels:

```bash
micromamba create -n recorda -c uibcdf -c conda-forge --strict-channel-priority python=3.14 recorda
```

For version-specific artifacts and qualification, see the
[Recorda releases](https://github.com/uibcdf/recorda/releases).
Installation and usage guidance is maintained in the
[repository README](https://github.com/uibcdf/recorda/blob/main/README.md).
Developer contracts, evidence and next work are in the
[development guide](https://github.com/uibcdf/recorda/tree/main/devguide).
