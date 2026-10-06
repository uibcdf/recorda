"""Recorda-owned recovery catalog and fault-isolated diagnostic handoff."""

from contextvars import ContextVar
from threading import Event

CODES = {
    "RECORDA-RECOVERY-OPERATION-001": {
        "level": "ERROR",
        "category": "recording",
        "user_message": "Recorda could not persist operation completion; inspect for gaps.",
        "metadata_message": "Recorda could not persist operation completion; inspect for gaps.",
        "user_hint": "Inspect the journal before relying on recorded completion.",
    },
    "RECORDA-RECOVERY-SESSION-001": {
        "level": "ERROR",
        "category": "recording",
        "user_message": "Recorda could not persist session completion; inspect for gaps.",
        "metadata_message": "Recorda could not persist session completion; inspect for gaps.",
        "user_hint": "Inspect the journal before relying on recorded completion.",
    },
}

_EMITTING = ContextVar("recorda_recovery_emitting", default=None)


def advise(error, code, sink, *, session_id, operation_id=None):
    """Keep the native failure and a fixed note even if a trusted sink fails."""
    try:
        # Recovery must not dispatch to an exception's arbitrary add_note override.
        BaseException.add_note(error, CODES[code]["user_message"])
    except BaseException:
        # An unusable native notes attribute cannot replace its original failure.
        pass
    active = _EMITTING.get()
    if sink is None or (active is not None and active.is_set()):
        return
    # A task created during delivery inherits this live guard. Once delivery ends,
    # its later independent work must not inherit a permanently suppressed sink.
    delivery = Event()
    delivery.set()
    token = _EMITTING.set(delivery)
    try:
        facts = {"session_id": session_id}
        if operation_id is not None:
            facts["operation_id"] = operation_id
        sink(code, **facts)
    except BaseException:
        # Diagnostic cancellation/interrupts also yield to the active native error.
        # Never stringify a diagnostic fault or send it back to the same sink.
        pass
    finally:
        delivery.clear()
        _EMITTING.reset(token)
