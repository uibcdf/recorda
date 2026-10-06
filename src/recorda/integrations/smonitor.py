"""Explicit recovery adapter for the qualified SMonitor 0.19 public API.

Import this module explicitly with the qualified SMonitor provider installed.
No provider import or diagnostic activation occurs through `import recorda`.
"""

from pathlib import Path

from smonitor import diagnostic_scope, emit, get_manager, resolve
from smonitor.integrations import register_provider

from recorda._inspection_catalog import CODES as INSPECTION_CODES
from recorda._recovery import CODES


class SMonitorInspectionPresentation:
    """Resolve count-only templates without emitting or configuring capture."""

    def __init__(self):
        register_provider(Path(__file__).resolve().parents[1], provider="recorda")

    def __call__(self, code, *, count):
        entry = INSPECTION_CODES[code]
        if get_manager().get_codes().get(code) != entry:
            return None
        with diagnostic_scope(safe_extra={"count": count}):
            result = resolve(code=code)
        if type(result) is not tuple or len(result) != 2:
            return None
        message, hint = result
        if type(message) is not str or type(hint) is not str:
            return None
        if not message or len(message) > 4096 or len(hint) > 4096:
            return None
        # Generic provider fallbacks are not qualified Recorda explanations.
        if message not in {
            entry[key].format(count=count) for key in ("user_message", "dev_message")
        }:
            return None
        if hint != entry["metadata_hint"]:
            return None
        return message, hint


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
