"""Explicit recovery adapter for the qualified SMonitor 0.19 public API.

Import this module explicitly with the qualified SMonitor provider installed.
No provider import or diagnostic activation occurs through `import recorda`.
"""

from pathlib import Path

from smonitor import diagnostic_scope, emit
from smonitor.integrations import register_provider

from recorda._recovery import CODES


class SMonitorRecoveryDiagnostics:
    """Register Recorda's catalog without changing the application's policy.

    Pass an instance as `recovery_diagnostics` to `session` or `start`.
    Only failed persistence during a native failure emits a diagnostic.
    """

    def __init__(self):
        register_provider(Path(__file__).resolve().parents[1], provider="recorda")

    def __call__(self, code, *, session_id, operation_id=None):
        """Emit a catalog diagnostic with only deliberately supplied safe IDs."""
        entry = CODES[code]
        facts = {"recorda_session_id": session_id}
        if operation_id is not None:
            facts["recorda_operation_id"] = operation_id
        with diagnostic_scope(safe_extra=facts):
            emit(
                entry["level"],
                "",
                code=code,
                source="recorda.recovery",
                category=entry["category"],
            )
