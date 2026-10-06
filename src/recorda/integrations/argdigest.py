"""Compatibility factory; ordinary CapturePolicy construction now uses ArgDigest."""

from recorda.policy import CapturePolicy


def capture_policy(
    profiles=None, *, inputs=True, parameters=True, outputs=True, exception_references=True
):
    """Return the same frozen policy as the default constructor, with no bypass."""
    return CapturePolicy(profiles, inputs, parameters, outputs, exception_references)
