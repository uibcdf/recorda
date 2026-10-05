# Recorda contributor instructions

Read `MOLI_GUIDE.md` and `devguide/README.md` first. Recorda is governed directly
by MOLI, not by MolSysSuite. Preserve the byte-identical canonical MOLI guide;
changes to it belong in `uibcdf/moli`.

The first slice is experimental. Use `recorda-lab` for controlled dummy scenarios,
keep its scientific library independent, and instrument declared semantic boundaries.
Never imply that a session captures arbitrary calls. Preserve native object ownership,
exceptions, incomplete work and safe references; never capture arbitrary repr or secrets.

Record local work in Recorda issues, laboratory scenarios in Recorda Lab issues, and
shared platform contracts in MOLI issues. Follow `devguide/reporting_protocol.md`:
issues precede queued reports; preserve resolved analysis in `devguide/archive/`.
Cross-repository identities use `uibcdf/<repository>#<number>`.

Use Ruff and published pytest-receptor (`--receptor=llm` locally, `--receptor=ci` in CI).
Develop with Python 3.14 and retain tests for Python 3.11–3.14. Read
`devguide/PYTHON_SUPPORT.md` for the tracked MOLI transition. The existing shared
work environment is `/home/diego/Myopt/miniconda3/envs/molsyssuite@uibcdf_3.14`;
verify `sys.executable` and select its interpreter explicitly if the shell activates
another environment. Use a published receptor rather than its development checkout.
Run `python devtools/validate_governance.py`, `ruff check .`,
`ruff format --check .`, and relevant pytest checks. The sibling MOLI component checker
may additionally verify the canonical guide. Declared CI is not executed evidence.
Do not claim platform support, public packages, DOI verification or replay without evidence.

Read MOLI's `devguide/RECORDA.md` before changing shared context, routing, reliability
or project integration. Keep standalone code free of a MOLI runtime dependency.
