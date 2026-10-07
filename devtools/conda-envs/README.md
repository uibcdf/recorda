# Recorda environment routes

All Conda routes use `uibcdf` with `conda-forge`. Create the selected environment,
then install this unpublished Recorda checkout with
`python -m pip install --no-deps --editable .`. Ordinary core requirements are
ArgDigest `>=0.15,<0.16` and SMonitor `>=0.19,<0.20`; ArgDigest owns its DepDigest
dependency. No scientific producer package is required. Pytest-receptor, Ruff,
PyYAML and packaging are development tools. Plain import/journal reading stay
free of provider imports; configuration/recording and reference-checking calls
use the required providers.

| Specification | Runtime scope |
| --- | --- |
| `development_env.yaml` | Core development, Python 3.14 and required published closure |
| `test_env.yaml` | Default configuration/core tests, Python 3.11–3.14 |
| `recovery_test_env.yaml` | Required closure plus opt-in recovery diagnostic tests |
| `support_test_env.yaml` | Compatibility specification for the same required published closure |
| `build_env.yaml` | Python 3.14 Conda build and exact-file publication tooling |

For example, create the support environment for local Python 3.14 development:

```bash
mamba env create -f devtools/conda-envs/support_test_env.yaml
mamba activate recorda-support
python -m pip install --no-deps --editable .
python devtools/verify_support_environment.py argdigest
python -m pip check
RECORDA_TEST_SMONITOR=1 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest -p pytest_receptor.plugin --receptor=llm
```

The shared specifications admit the complete supported range; for routine local
development select Python 3.14 when creating the environment. CI passes an exact
minor override for each matrix cell. All five specifications pin ArgDigest 0.15.0
build 0, SMonitor 0.19.0 build 1 and DepDigest 0.13.0 build 0. The old extra names
are empty compatibility aliases; package metadata now declares these providers
as required. Conda supplies the closure before `--no-deps` installation.
No public `recorda` Conda package or complete pip dependency route is claimed.

The static `check_dependencies.py` gate compares required metadata with the local
noarch recipe, every inventoried environment and CI/source routes. It rejects
missing dependencies, weaker bounds, incompatible Python constraints, unclassified
routes and source candidates below the declared floor. The installed provider
check verifies project bounds, exact Conda coordinates/digests and Python-file
hashes, and rejects source imports.
For Python noarch providers, archive-relative `site-packages/` paths are mapped
to the running interpreter's `sysconfig` purelib directory. Already installed
paths are retained. Both forms must match Conda's installed `files` inventory;
resolved paths must stay inside the environment, and provider Python files must
stay inside the imported package. Archive coordinates and managed Python-byte
checks remain mandatory. This corrects `uibcdf/recorda#23`; historical Lab #15
receipts still describe the older checker's failure and their explicit workaround.
`pip check` checks the installed dependency closure. These checks cover these
development lanes; a local-source recipe and negative preflight fixtures are now
present. The recipe is maintained at `devtools/conda-build/meta.yaml`.
[Release qualification](../../devguide/RELEASING.md) builds once with the published
UIBCDF action, tests that same file and uploads it without rebuilding. Public
publication and OS evidence remain tracked in `uibcdf/recorda#3` / #4. No sibling
source CI installation route is retained.
