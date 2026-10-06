"""Lazy Recorda option digestion; native scientific calls remain untouched."""

from pathlib import Path

from smonitor import diagnostic_scope
from smonitor.integrations import ensure_configured

from recorda.policy import _detail_switch, _profiles
from recorda.references import (
    _digest_algorithm,
    _index_entries,
    _index_root,
    _inspected_record,
    _max_bytes,
    _resolver,
)

# Provider imports and rule registration also inherit the restrictive scope.
with diagnostic_scope():
    ensure_configured(Path(__file__).resolve().parent)
    from argdigest import DigestConfig, arg_digest, register_pipeline

    _CONFIG = DigestConfig(
        capture_policy="metadata_only",
        argument_digestion=False,
        strictness="error",
        unknown_argument="error",
    )

    @register_pipeline(kind="recorda.capture", name="profiles")
    def _profile_rule(value, ctx):
        return _profiles(value)

    @register_pipeline(kind="recorda.capture", name="detail_switch")
    def _switch_rule(value, ctx):
        return _detail_switch(value)

    @arg_digest.map(
        config=_CONFIG,
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

    @register_pipeline(kind="recorda.references", name="root")
    def _root_rule(value, ctx):
        return _index_root(value)

    @register_pipeline(kind="recorda.references", name="entries")
    def _entries_rule(value, ctx):
        return _index_entries(value)

    @register_pipeline(kind="recorda.references", name="digest_algorithm")
    def _algorithm_rule(value, ctx):
        return _digest_algorithm(value)

    @register_pipeline(kind="recorda.references", name="resolver")
    def _resolver_rule(value, ctx):
        return _resolver(value)

    @register_pipeline(kind="recorda.references", name="max_bytes")
    def _limit_rule(value, ctx):
        return _max_bytes(value)

    @register_pipeline(kind="recorda.references", name="record")
    def _record_rule(value, ctx):
        return _inspected_record(value)

    @arg_digest.map(
        config=_CONFIG,
        digest_algorithm={"kind": "recorda.references", "rules": [_algorithm_rule]},
        entries={"kind": "recorda.references", "rules": [_entries_rule]},
        root={"kind": "recorda.references", "rules": [_root_rule]},
    )
    def reference_index_options(digest_algorithm, entries, root):
        _digest_algorithm(digest_algorithm)
        _index_entries(entries)
        _index_root(root)
        return root, entries, digest_algorithm

    @arg_digest.map(
        config=_CONFIG,
        resolver={"kind": "recorda.references", "rules": [_resolver_rule]},
        max_bytes={"kind": "recorda.references", "rules": [_limit_rule]},
    )
    def reference_check_options(resolver, *, max_bytes):
        _resolver(resolver)
        _max_bytes(max_bytes)
        return resolver, max_bytes

    @arg_digest.map(
        config=_CONFIG,
        resolver={"kind": "recorda.references", "rules": [_resolver_rule]},
        max_bytes={"kind": "recorda.references", "rules": [_limit_rule]},
        record={"kind": "recorda.references", "rules": [_record_rule]},
    )
    def record_check_options(resolver, *, max_bytes, record):
        _resolver(resolver)
        _max_bytes(max_bytes)
        _inspected_record(record)
        return resolver, max_bytes, record
