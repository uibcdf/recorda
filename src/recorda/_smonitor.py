"""Provider declarations and safe first-use defaults; application policy wins."""

from recorda._recovery import CODES as CODES

SIGNALS = {}

# Default argument validation must not activate process-wide scientific capture.
# register_provider only records these recommendations. ensure_configured applies
# them on first use only, when no application/project policy has been selected.
SMONITOR = {
    "capture_logging": False,
    "capture_warnings": False,
    "capture_exceptions": False,
}
