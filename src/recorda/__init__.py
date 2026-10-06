"""Provisional explicit recording API; see devguide/FIRST_SLICE.md."""

from .capture import Omitted, Reference
from .reader import ScientificRecord, inspect
from .runtime import RecordingSession, record, session, start, stop

__all__ = [
    "Omitted",
    "RecordingSession",
    "Reference",
    "ScientificRecord",
    "inspect",
    "record",
    "session",
    "start",
    "stop",
]
__version__ = "0.2.0"
