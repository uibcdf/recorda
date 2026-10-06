"""Lazy default configuration digestion; native scientific calls remain untouched."""

from pathlib import Path

from smonitor import diagnostic_scope
from smonitor.integrations import ensure_configured

from recorda.policy import _detail_switch, _profiles

# Provider imports and rule registration also inherit the restrictive scope.
with diagnostic_scope():
    ensure_configured(Path(__file__).resolve().parent)
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
    def capture_profiles(profiles, inputs, parameters, outputs, exception_references):
        # Keep checks in the function body too: private unwrapping/bypass cannot
        # turn an unvalidated collection or switch into a trusted policy.
        profiles = _profiles(profiles)
        for value in (inputs, parameters, outputs, exception_references):
            _detail_switch(value)
        return profiles
