"""Receiving of retained first-use setup versus registration-only adapters (#29)."""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import recorda


def fresh(tmp_path, code, *arguments):
    completed = subprocess.run(
        [sys.executable, "-B", "-c", textwrap.dedent(code), *arguments],
        cwd=tmp_path,
        env={
            **os.environ,
            "PYTHONPATH": str(Path(recorda.__file__).resolve().parents[1]),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


@pytest.mark.parametrize("setup", ["unconfigured", "application", "project"])
@pytest.mark.parametrize("boundary", ["capture", "references"])
def test_first_use_and_errors_retain_selected_application_setup(tmp_path, setup, boundary):
    fresh(
        tmp_path,
        """
        import logging, sys, warnings
        from pathlib import Path
        import recorda
        assert not {"smonitor", "argdigest", "depdigest"} & sys.modules.keys()
        import smonitor
        manager = smonitor.get_manager()
        setup, boundary = sys.argv[1:]
        if setup == "application":
            class Sink:
                name = "application"
                def handle(self, event, **kwargs):
                    pass
            smonitor.configure(handlers=[Sink()], profile="qa", level="CRITICAL",
                capture_logging=True, capture_warnings=True, capture_exceptions=True,
                run_id="application-run", session_id="application-session",
                routes=[], filters=[])
        elif setup == "project":
            Path("_smonitor.py").write_text(
                'SMONITOR = {"profile": "qa", "level": "CRITICAL", '
                '"capture_logging": False, "capture_warnings": False, '
                '"capture_exceptions": False}\\n')
        before = manager.config, manager._policy, tuple(manager._handlers)
        hooks = warnings.showwarning, sys.excepthook, tuple(logging.root.handlers)
        class Opaque:
            def __repr__(self):
                raise AssertionError("opaque repr collected")
            def __str__(self):
                raise AssertionError("opaque text collected")
        for _ in range(2):
            if boundary == "capture":
                assert recorda.CapturePolicy(profiles=["b", "a", "b"]).profiles == ("a", "b")
                try:
                    recorda.CapturePolicy(inputs=Opaque())
                except TypeError:
                    pass
                else:
                    raise AssertionError("native capture validation bypassed")
            else:
                assert recorda.LocalFileResolver('.', {}).references == ()
                native = OSError("synthetic path failure")
                class BrokenPath:
                    def __fspath__(self):
                        raise native
                try:
                    recorda.LocalFileResolver(BrokenPath(), {})
                except OSError as error:
                    assert error is native
                else:
                    raise AssertionError("native path exception replaced")
        assert manager._policy_configured
        if setup == "application":
            assert manager.config is before[0] and manager._policy is before[1]
            assert tuple(manager._handlers) == before[2]
            assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
            assert manager.config.capture_logging and manager.config.capture_warnings
            assert manager.config.capture_exceptions
            assert manager._run_id == "application-run"
            assert manager._session_id == "application-session"
        else:
            assert not manager.config.capture_logging and not manager.config.capture_warnings
            assert not manager.config.capture_exceptions
            assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        if setup != "unconfigured":
            assert manager.config.level == "CRITICAL" and manager.config.profile == "qa"
        assert smonitor.get_capture_policy() == smonitor.CapturePolicy()
        """,
        setup,
        boundary,
    )


@pytest.mark.skipif(
    os.environ.get("RECORDA_TEST_SMONITOR") != "1",
    reason="explicit SMonitor integration lane",
)
@pytest.mark.parametrize("setup", ["unconfigured", "application_sink", "application_empty"])
@pytest.mark.parametrize("boundary", ["adapter", "recovery"])
def test_registration_and_real_emission_have_distinct_setup_effects(tmp_path, setup, boundary):
    fresh(
        tmp_path,
        """
        import logging, sys, warnings
        import recorda, smonitor
        from recorda.integrations.smonitor import SMonitorRecoveryDiagnostics
        manager = smonitor.get_manager()
        setup, boundary = sys.argv[1:]
        class Sink:
            name = "application"
            def __init__(self):
                self.events = []
            def handle(self, event, **kwargs):
                self.events.append(event)
        handler = Sink()
        if setup != "unconfigured":
            smonitor.configure(handlers=[handler] if setup == "application_sink" else [],
                level="DEBUG", profile="qa", capture_logging=False,
                capture_warnings=False, capture_exceptions=False, routes=[], filters=[])
        hooks = warnings.showwarning, sys.excepthook, tuple(logging.root.handlers)
        before = manager.config, manager._policy, tuple(manager._handlers)
        sink = SMonitorRecoveryDiagnostics()
        SMonitorRecoveryDiagnostics()
        assert manager.config is before[0] and manager._policy is before[1]
        assert tuple(manager._handlers) == before[2]
        assert "argdigest" not in sys.modules
        assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        if boundary == "adapter":
            sink("RECORDA-RECOVERY-SESSION-001", session_id="safe-session")
            assert "argdigest" not in sys.modules
            assert manager.config is before[0] and manager._policy is before[1]
            assert manager._policy_configured == (setup != "unconfigured")
        else:
            class NativeFailure(ValueError):
                def __str__(self):
                    raise AssertionError("native text collected")
                def __repr__(self):
                    raise AssertionError("native repr collected")
            native = NativeFailure()
            cause = RuntimeError("synthetic scientific cause")
            session = recorda.session("synthetic private label", path="journal.jsonl",
                                     recovery_diagnostics=sink)
            with session:
                pass
            assert session.record.status == "succeeded"
            session = recorda.session("synthetic private label", path="failed.jsonl",
                                     recovery_diagnostics=sink)
            def broken(event, **data):
                raise OSError("synthetic private disk path")
            try:
                with session:
                    session._append = broken
                    raise native from cause
            except NativeFailure as error:
                assert error is native and error.__cause__ is cause
            else:
                raise AssertionError("native failure replaced")
            assert session.record.status == "incomplete" and session._file is None
            assert any("persist session completion" in note for note in native.__notes__)
            assert manager._policy_configured
            if setup != "unconfigured":
                assert manager.config is before[0] and manager._policy is before[1]
            else:
                assert not manager.config.capture_logging and not manager.config.capture_warnings
                assert not manager.config.capture_exceptions
        if setup == "application_sink":
            assert tuple(manager._handlers) == before[2]
            assert len(handler.events) == 1
            event = handler.events[0]
            assert event["context"] is None and event["tags"] is None
            assert "recorda_session_id" in event["extra"]
            assert "synthetic private" not in str(event)
        else:
            # Compatibility emit adds a console even to explicitly configured handlers=[].
            assert not before[2] and manager._handlers
        assert hooks == (warnings.showwarning, sys.excepthook, tuple(logging.root.handlers))
        assert smonitor.get_capture_policy() == smonitor.CapturePolicy()
        """,
        setup,
        boundary,
    )
