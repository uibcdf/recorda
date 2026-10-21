# Recorda contributor instructions

During development, testing, scientific exploration and human conversations,
surface actionable suspected defects, inconsistencies, missing capabilities
and improvements, even uncertain or nonblocking ones. At a natural pause,
explicitly offer the owning issue or an update to an existing one; distinguish
observation from hypothesis. Use reporting authority already granted without
repeated permission. Respect declined or deferred human disclosure and protect
confidential material; otherwise authorized technical reporting remains due.
Deliver an accepted report through an observable issue/update or explain the
private route or maintainer handoff. Follow
`MOLI_GUIDE.md#reporting-bugs-and-proposals` and its linked human-facing policy.


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

Keep defect details in owning issues, code, tests and technical documentation.
Put only accepted, lasting contributor working instructions in the correctly scoped
`AGENTS.md`, following `MOLI_GUIDE.md#durable-instructions-for-development-agents`.
For developer-guide work, read `devguide/AGENTS.md`.

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

At task or release closeout, review temporary resources created by the work.
Remove only owned disposable paths after their last needed use; retain useful
evidence with an owner and review trigger. Protect active sessions, worktrees
and caller outputs, and report cleanup failures. Follow
`MOLI_GUIDE.md#temporary-development-resources`.

Before creating or editing a public GitHub Release, check that its visible
title is exactly the canonical `X.Y.Z` version and matches its tag and
package version. Put descriptions in the release notes. Follow
`MOLI_GUIDE.md#moli-engineering-baseline` and `devguide/RELEASING.md`.

Read MOLI's `devguide/RECORDA.md` before changing shared context, routing, reliability
or project integration. Keep standalone code free of a MOLI runtime dependency.
