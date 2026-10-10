"""Behaviour tests for `browser_load_check` (plan §7.1 wave 2, §9, §9.2).

Unit tests inject canned probe output by monkeypatching `browser._run_probe`, so they
never spawn a real subprocess or Chromium. Real-browser coverage lives in
`test_browser_load_check_against_real_chromium` below, marked `browser` and excluded by
default (`pytest -m browser` to run it).

Strict TDD: these tests are written before `src/caxgauge/verify/browser.py` exists.
"""

import subprocess
from pathlib import Path

import pytest

from caxgauge.verify import browser
from caxgauge.verify.substrate import POLYFETCH_ENV
from caxgauge.verify.types import Status

FIXTURE = Path(__file__).parent.parent / "fixtures" / "good.stl"


def _completed(
    stdout: str, *, returncode: int = 0, stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["probe"], returncode=returncode, stdout=stdout, stderr=stderr
    )


def test_skip_when_polyfetch_dir_unset(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(POLYFETCH_ENV, raising=False)
    calls = []
    monkeypatch.setattr(browser, "_run_probe", lambda *a, **k: calls.append(1))

    result = browser.browser_load_check(FIXTURE)

    assert result.status is Status.SKIP
    assert POLYFETCH_ENV in result.detail
    assert not calls


def test_skip_when_uv_not_on_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(browser.shutil, "which", lambda _name: None)
    calls = []
    monkeypatch.setattr(browser, "_run_probe", lambda *a, **k: calls.append(1))

    result = browser.browser_load_check(FIXTURE)

    assert result.status is Status.SKIP
    assert "uv" in result.detail
    assert not calls


def test_builds_an_in_clone_probe_command(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(browser.shutil, "which", lambda _name: "/usr/bin/uv")
    captured = {}

    def fake_run_probe(cmd, *, timeout) -> subprocess.CompletedProcess[str]:
        captured["cmd"] = cmd
        captured["timeout"] = timeout
        return _completed(
            '{"state": "rendered", "console_errors": [], "page_errors": [], "network_failures": []}'
        )

    monkeypatch.setattr(browser, "_run_probe", fake_run_probe)

    result = browser.browser_load_check(FIXTURE, timeout=12.0)

    assert result.status is Status.PASS
    cmd = captured["cmd"]
    assert cmd[0] == "/usr/bin/uv"
    assert cmd[1:4] == ["run", "--directory", str(tmp_path)]
    assert cmd[4] == "python"
    assert Path(cmd[5]).is_file()
    assert cmd[5].endswith("probes/load_probe.py")
    assert cmd[6].startswith("http://127.0.0.1:")
    assert cmd[7] == "12.0"
    assert captured["timeout"] == 12.0


def _run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    stdout: str,
    *,
    returncode: int = 0,
    stderr: str = "",
) -> browser.BrowserResult:
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(browser.shutil, "which", lambda _name: "/usr/bin/uv")
    monkeypatch.setattr(
        browser,
        "_run_probe",
        lambda *a, **k: _completed(stdout, returncode=returncode, stderr=stderr),
    )
    return browser.browser_load_check(FIXTURE)


def test_rendered_with_no_captured_errors_is_pass(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": "rendered", "console_errors": [], "page_errors": [], "network_failures": []}',
    )
    assert result.status is Status.PASS
    assert "verified" not in result.detail.lower()
    assert not result.console_errors
    assert not result.page_errors
    assert not result.network_failures


def test_state_error_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": "error", "console_errors": [], "page_errors": [], "network_failures": []}',
    )
    assert result.status is Status.FAIL
    assert "error" in result.detail.lower()
    assert "verified" not in result.detail.lower()


def test_null_state_is_fail_not_skip(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": null, "console_errors": [], "page_errors": [], "network_failures": []}',
    )
    assert result.status is Status.FAIL
    assert "verified" not in result.detail.lower()


def test_rendered_with_network_failure_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": "rendered", "console_errors": [], "page_errors": [], '
        '"network_failures": [{"url": "http://x/vendor.js", "status": 404}]}',
    )
    assert result.status is Status.FAIL
    assert result.network_failures
    assert "verified" not in result.detail.lower()


def test_rendered_with_console_error_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": "rendered", "console_errors": ["TypeError: boom"], '
        '"page_errors": [], "network_failures": []}',
    )
    assert result.status is Status.FAIL
    assert result.console_errors == ("TypeError: boom",)


def test_rendered_with_page_error_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(
        monkeypatch,
        tmp_path,
        '{"state": "rendered", "console_errors": [], '
        '"page_errors": ["SyntaxError: nope"], "network_failures": []}',
    )
    assert result.status is Status.FAIL
    assert result.page_errors == ("SyntaxError: nope",)


def test_nonzero_exit_is_fail_with_stderr_excerpt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(monkeypatch, tmp_path, "", returncode=1, stderr="Traceback: boom")
    assert result.status is Status.FAIL
    assert "boom" in result.detail


def test_garbage_stdout_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    result = _run(monkeypatch, tmp_path, "not json at all")
    assert result.status is Status.FAIL
    assert "verified" not in result.detail.lower()


def test_subprocess_timeout_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(browser.shutil, "which", lambda _name: "/usr/bin/uv")

    def raise_timeout(*_a: object, **_k: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(cmd=["probe"], timeout=30.0)

    monkeypatch.setattr(browser, "_run_probe", raise_timeout)

    result = browser.browser_load_check(FIXTURE)

    assert result.status is Status.FAIL
    assert "timed out" in result.detail.lower()
    assert "verified" not in result.detail.lower()


def test_build_env_drops_uv_project_environment_and_virtual_env(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    fake_venv = str(tmp_path / "venv-wave2-browser")
    fake_cache = str(tmp_path / "uv-cache")
    monkeypatch.setenv("UV_PROJECT_ENVIRONMENT", fake_venv)
    monkeypatch.setenv("VIRTUAL_ENV", fake_venv)
    monkeypatch.setenv("UV_CACHE_DIR", fake_cache)

    env = browser._build_env()

    assert "UV_PROJECT_ENVIRONMENT" not in env
    assert "VIRTUAL_ENV" not in env
    assert env.get("UV_CACHE_DIR") == fake_cache


@pytest.mark.browser
def test_browser_load_check_against_real_chromium(tmp_path: Path):
    """Golden-path + forced-failure integration (plan §7.3 item 5, §9.2 rule 3).

    Needs `CAXGAUGE_POLYFETCH_DIR` pointing at a real polyfetch checkout with Chromium
    installed. Run with `pytest -m browser`.
    """
    good_result = browser.browser_load_check(FIXTURE)
    assert good_result.status is Status.PASS
    assert not good_result.console_errors
    assert not good_result.page_errors
    assert not good_result.network_failures

    garbage = tmp_path / "garbage.stl"
    garbage.write_bytes(b"not an stl file at all, just some short garbage bytes")

    bad_result = browser.browser_load_check(garbage)
    assert bad_result.status is Status.FAIL
    # The literal state, not just "error" appearing anywhere — a wait-timeout
    # (state=null) detail can also contain the word "error" inside a captured
    # page_error, which would make a loose substring check pass for the wrong
    # reason (plan §9.2 rule 3: the forced failure must actually be observed).
    assert "body[data-state]=error" in bad_result.detail
    assert "verified" not in bad_result.detail.lower()
