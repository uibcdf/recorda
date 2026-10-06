# Recorda environment routes

All Conda routes use `uibcdf` with `conda-forge`. Create the selected environment,
then install this unpublished Recorda checkout with
`python -m pip install --no-deps --editable .`. Ordinary core requirements are
stdlib-only; pytest-receptor and Ruff are development tools.

| Specification | Runtime scope |
| --- | --- |
| `development_env.yaml` | Core development, Python 3.14, no optional providers |
| `test_env.yaml` | Provider-independent core tests, Python 3.11–3.14 |
| `recovery_test_env.yaml` | Explicit recovery integration, published SMonitor 0.19.0 build 1 |
| `support_test_env.yaml` | Explicit recovery/configuration integrations, published SMonitor 0.19.0 build 1, ArgDigest 0.15.0 build 0, DepDigest 0.13.0 build 0 |

For example, create the support environment for local Python 3.14 development:

```bash
mamba env create -f devtools/conda-envs/support_test_env.yaml
mamba activate recorda-support
python -m pip install --no-deps --editable .
python devtools/verify_support_environment.py argdigest
python -m pip check
RECORDA_TEST_ARGDIGEST=1 RECORDA_TEST_SMONITOR=1 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
python -m pytest -p pytest_receptor.plugin --receptor=llm
```

The shared specifications admit the complete supported range; for routine local
development select Python 3.14 when creating the environment. CI passes an exact
minor override for each matrix cell. The package extras declare feature bounds;
Conda supplies these providers before the `--no-deps` Recorda installation.
No public `recorda` Conda package or complete pip dependency route is claimed.

The early optional-feature check verifies project bounds, exact provider Conda
coordinates/digests and installed Python-file hashes, and rejects source imports.
`pip check` checks the installed dependency closure. These checks cover these
feature lanes; release recipe/preflight and public Recorda artifact qualification
remain tracked in `uibcdf/recorda#3`. Recorda has no Conda release recipe or retained
sibling-source CI installation route at this checkpoint.
