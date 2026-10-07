"""Provisional explicit recording API; see devguide/FIRST_SLICE.md."""

from .capture import Omitted, Reference
from .policy import CapturePolicy
from .presentation import inspection_view
from .reader import ScientificRecord, inspect
from .references import LocalFileResolver, check_reference, check_references
from .runtime import RecordingSession, record, session, start, stop

__all__ = [
    "CapturePolicy",
    "LocalFileResolver",
    "Omitted",
    "RecordingSession",
    "Reference",
    "ScientificRecord",
    "check_reference",
    "check_references",
    "inspect",
    "inspection_view",
    "record",
    "session",
    "start",
    "stop",
]
__version__ = "0.3.0"
