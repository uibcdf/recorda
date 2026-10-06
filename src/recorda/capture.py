"""Bounded declared capture. Never inspect opaque objects or call their repr."""

import math
import re
from dataclasses import asdict, dataclass

_SENSITIVE = re.compile(r"password|passwd|secret|token|credential|api[_-]?key|authorization", re.I)


@dataclass(frozen=True)
class Reference:
    """Caller-declared safe identity; neither stores bytes nor promises resolution."""

    owner: str
    identifier: str
    revision: str | None = None
    digest: str | None = None

    def __post_init__(self):
        for key, value in asdict(self).items():
            if value is None and key in {"revision", "digest"}:
                continue
            if not isinstance(value, str) or not value or len(value) > 1024:
                raise ValueError("reference fields must be nonempty bounded strings")


@dataclass(frozen=True)
class Omitted:
    """Explicit caller request to omit a value for a non-sensitive reason label."""

    reason: str = "caller_omitted"


def _omit(reason):
    return {"kind": "omitted", "reason": reason}


def _adapt(value, adapter):
    try:
        reference = adapter(value)
    except Exception:
        return _omit("reference_adapter_failed")
    if not isinstance(reference, (Reference, Omitted)):
        return _omit("invalid_reference_adapter_result")
    return capture(reference)


def exception_reference(error, *, reference_adapters=None):
    """Reference an exact registered exception type without replacing its propagation."""
    adapter = (reference_adapters or {}).get(type(error))
    if adapter is None:
        return _omit("unsupported_type")
    try:
        return _adapt(error, adapter)
    except BaseException:
        # An interrupt inside trusted capture must not replace the already failing
        # scientific operation's exception (including its cancellation/interrupt).
        return _omit("reference_adapter_failed")


def capture(value, name="", *, reference_adapters=None):
    if _SENSITIVE.search(name):
        return _omit("sensitive_name")
    if isinstance(value, Omitted):
        # A supplied explanation is also a value that may accidentally hold a secret.
        return _omit("caller_omitted")
    if isinstance(value, Reference):
        return {"kind": "reference", **asdict(value)}
    if value is None or type(value) is bool:
        return value
    if type(value) is int:
        return value if value.bit_length() <= 256 else _omit("oversized_value")
    if type(value) is float:
        return value if math.isfinite(value) else _omit("nonfinite_value")
    if type(value) is str:
        return value if len(value) <= 1024 else _omit("oversized_value")
    adapter = (reference_adapters or {}).get(type(value))
    if adapter is not None:
        return _adapt(value, adapter)
    return _omit("unsupported_type")


def fields(values, *, reference_adapters=None):
    if values is None:
        return {}
    if type(values) is not dict:
        raise TypeError("declared fields must be a dict")
    if len(values) > 64:
        raise ValueError("at most 64 fields may be declared at one boundary")
    result = {}
    for name, value in values.items():
        if type(name) is not str or not name or len(name) > 256:
            raise ValueError("field names must be nonempty bounded strings")
        result[name] = capture(value, name, reference_adapters=reference_adapters)
    return result


def label(value):
    if type(value) is not str or not value or len(value) > 256:
        raise ValueError("names must be nonempty strings of at most 256 characters")
    return value
