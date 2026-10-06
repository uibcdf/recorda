"""Explicit CapturePolicy factory requiring the qualified ArgDigest/SMonitor APIs."""

from smonitor import diagnostic_scope

from recorda.policy import CapturePolicy, _detail_switch, _profiles

# Provider imports and rule registration also inherit the restrictive scope.
with diagnostic_scope():
    from argdigest import DigestConfig, arg_digest, register_pipeline

    @register_pipeline(kind="recorda.capture", name="profiles")
    def _profile_rule(value, ctx):
        return _profiles(value)

    @register_pipeline(kind="recorda.capture", name="detail_switch")
    def _switch_rule(value, ctx):
        return _detail_switch(value)

    @arg_digest.map(
        config=DigestConfig(
            capture_policy="metadata_only",
            argument_digestion=False,
            strictness="error",
            unknown_argument="error",
        ),
        profiles={"kind": "recorda.capture", "rules": [_profile_rule]},
        inputs={"kind": "recorda.capture", "rules": [_switch_rule]},
        parameters={"kind": "recorda.capture", "rules": [_switch_rule]},
        outputs={"kind": "recorda.capture", "rules": [_switch_rule]},
        exception_references={"kind": "recorda.capture", "rules": [_switch_rule]},
    )
    def _build_policy(profiles, inputs, parameters, outputs, exception_references):
        # These core invariants remain mandatory even if a private caller bypasses
        # digestion. The public factory has no bypass parameter.
        return CapturePolicy(profiles, inputs, parameters, outputs, exception_references)


def capture_policy(
    profiles=None, *, inputs=True, parameters=True, outputs=True, exception_references=True
):
    """Validate Recorda configuration with ArgDigest and return a frozen policy.

    Accepted values, bounds and canonical form match recorda.CapturePolicy.
    No scientific target argument is digested and no global policy is selected.
    """
    return _build_policy(profiles, inputs, parameters, outputs, exception_references)
