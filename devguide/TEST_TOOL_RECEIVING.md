# Published pytest-receptor receiving

Owner: `uibcdf/recorda#31`. Release: `uibcdf/recorda#33` (0.3.2).

Current development/CI selection is published **pytest-receptor 1.2.1**, admitting
Python 3.11–3.14. The PyPI wheel has SHA256
`683200648785f3894357891b238cdc0780c1e874dcf067882dbba2aaa2c527c3`.
It contains the terminal-stream cleanup absent from Recorda's earlier 1.1.0 pin;
provider `uibcdf/pytest-receptor#4` retains the original fix and released-source
history. This is a developer tool, not a Recorda runtime dependency.

`tests/test_receptor_receiving.py` runs fresh processes with both `llm` and `ci`,
with/without statistics and controlled success/failure. Explicit plugin loading
and disabled autoload prevent accidental substitution by another checkout.
ResourceWarning is made visible rather than suppressed. Native exit, terminal
verdict, JUnit totals and the public integrity-checked JSONL reader must agree;
the stream must finish and no late closed-writer/discard warning may follow.
An intentional nested failure is a receiving fixture, not a failed Recorda gate.

All four applicable Conda environments and explicit CI installs use the same
published pin. Existing source and exact-Conda matrices execute the regression
on each supported Python minor; qualification belongs to its actual source/run.
Older receipts retain their original tool versions and warning observations.
The source/installed full suite and release candidate still need their own
complete evidence; the targeted probe does not certify publication.
