"""Recorda-owned, count-only technical presentation templates."""

_REFERENCE_MESSAGES = {
    "missing": ("WARNING", "retained reference occurrences are missing now"),
    "mismatched": ("WARNING", "reference occurrences have different current bytes"),
    "unresolved": ("INFO", "reference occurrences have no supplied local binding"),
    "available_unverified": (
        "INFO",
        "reference occurrences are available without byte verification",
    ),
    "unsupported_digest": ("INFO", "reference occurrences have an unsupported digest declaration"),
    "too_large": ("INFO", "reference occurrences exceed the explicit byte-check bound"),
    "not_a_file": ("WARNING", "reference occurrences resolve to non-file objects"),
    "outside_root": ("WARNING", "reference occurrences resolve outside the supplied root"),
    "invalid_reference": ("WARNING", "reference occurrences have invalid declarations"),
    "unreadable": ("WARNING", "reference occurrences could not be read"),
    "unstable": ("WARNING", "reference occurrences changed during checking"),
}


def reference_code(state):
    return "RECORDA-INSPECT-REFERENCE-" + state.upper().replace("_", "-")


def _entry(level, message, hint):
    # A metadata_message would override the application's audience selection.
    return {
        "level": level,
        "category": "inspection",
        "user_message": "{count} " + message + ".",
        "dev_message": "Inspection observation ({count} occurrences): " + message + ".",
        "metadata_hint": hint,
    }


CODES = {
    reference_code(state): _entry(
        level,
        message,
        "Review the declared reference and trusted local index; recorded execution is unchanged.",
    )
    for state, (level, message) in _REFERENCE_MESSAGES.items()
}
CODES.update(
    {
        "RECORDA-INSPECT-INCOMPLETE": _entry(
            "WARNING",
            "operations lack recorded completion; the session remains incomplete",
            "Inspect recorded work without inferring why completion is absent.",
        ),
        "RECORDA-INSPECT-JOURNAL-TAIL": _entry(
            "WARNING",
            "truncated journal tails were observed",
            "Only the readable prefix is available; do not infer a specific interruption cause.",
        ),
        "RECORDA-INSPECT-UNCLASSIFIED": _entry(
            "WARNING",
            "observations have no classified presentation",
            "Review the original structured observations before drawing conclusions.",
        ),
    }
)
