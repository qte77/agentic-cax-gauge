"""Headless browser load check: did the mesh parse and render at all (plan §7.1, §9).

`browser_load_check(mesh)` serves the viewer + mesh locally (`substrate.serve_viewer`)
and drives it through polyfetch's own interpreter — an **in-clone probe script**
(`verify/probes/load_probe.py`) run via `uv run --directory <polyfetch> python
<probe> <url> <timeout>` (env-borrow, plan §9; `../polyfetch-scrape/USING.md` "Why
env-borrow" / "Scripting substrate"). The probe prints one JSON verdict to stdout;
this module never asserts anything from `page.evaluate` of page globals itself —
`body[data-state]` is the signal (plan §9.2.1, §9.2 rule 3; `viewer/README.md` →
"Success / failure signals").

`pageerror` is captured as a bonus signal only (upstream polyfetch#253: it did not
fire for this page's own script errors on Patchright during wave 1's smoke test,
`AGENT_LEARNINGS.md`) — it is never required to fire, and its absence never turns a
real failure into a pass.

Polyfetch/Chromium absent, or `uv` missing from `PATH`, is `SKIP`, never `PASS`
(`.claude/rules/verification-honesty.md`): nothing ran, so nothing was checked.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from caxgauge.verify.substrate import polyfetch_dir, serve_viewer
from caxgauge.verify.types import BrowserResult, Status

_PROBE_SCRIPT = Path(__file__).resolve().parent / "probes" / "load_probe.py"
_DEFAULT_VIEW = "iso"
_UV_STARTUP_BUDGET_S = 30.0
_ENV_VARS_TO_DROP = ("UV_PROJECT_ENVIRONMENT", "VIRTUAL_ENV")


def browser_load_check(mesh: Path, *, timeout: float = 30.0) -> BrowserResult:
    """Run the headless load check against `mesh`.

    Args:
        mesh: Path to the exported STL to load in the viewer.
        timeout: Seconds budgeted for the viewer to reach a verdict. Also used
            (plus a startup budget) as the subprocess timeout.

    Returns:
        `SKIP` when `CAXGAUGE_POLYFETCH_DIR` is unset/missing or `uv` is not on
        `PATH` — nothing ran. Otherwise `PASS` only when the viewer reported
        `state="rendered"` with no captured console/page/network errors; every
        other outcome (`state="error"`, no verdict at all, any captured error,
        or a probe that crashed/timed out) is `FAIL`.
    """
    polyfetch = polyfetch_dir()
    if polyfetch is None:
        return BrowserResult(
            status=Status.SKIP,
            detail="browser-load check skipped: CAXGAUGE_POLYFETCH_DIR is unset or not a directory",
        )

    uv = shutil.which("uv")
    if uv is None:
        return BrowserResult(
            status=Status.SKIP, detail="browser-load check skipped: uv not found on PATH"
        )

    with serve_viewer(mesh) as viewer:
        url = viewer.page_url(_DEFAULT_VIEW)
        cmd = [
            uv,
            "run",
            "--directory",
            str(polyfetch),
            "python",
            str(_PROBE_SCRIPT),
            url,
            str(timeout),
        ]
        return _run_and_classify(cmd, timeout)


def _build_env() -> dict[str, str]:
    """`os.environ`, minus vars that would redirect the probe into this venv.

    `UV_PROJECT_ENVIRONMENT`/`UV_CACHE_DIR` are a global `uv` override, not scoped
    to this repo's `uv run` call (plan Handoff's `/tmp` prefix). Left in place, the
    probe's `uv run --directory <polyfetch>` would target *this* package's venv —
    where `polyfetch_scrape` is not installed — instead of polyfetch's own.
    """
    return {k: v for k, v in os.environ.items() if k not in _ENV_VARS_TO_DROP}


def _run_probe(cmd: list[str], *, timeout: float) -> subprocess.CompletedProcess[str]:
    """Run the probe subprocess; the sole seam tests monkeypatch to inject canned output.

    `cmd` is an absolute-path list with no shell; `timeout` bounds the whole
    subprocess, not just the in-page wait, so a Chromium cold start does not get
    killed before it can print its JSON verdict.
    """
    return subprocess.run(  # noqa: S603 - absolute `uv` path, list args, no shell
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout + _UV_STARTUP_BUDGET_S,
        check=False,
        env=_build_env(),
    )


def _run_and_classify(cmd: list[str], timeout: float) -> BrowserResult:
    """Invoke the probe and map its outcome to a `BrowserResult` (never raises)."""
    try:
        proc = _run_probe(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        budget = timeout + _UV_STARTUP_BUDGET_S
        return BrowserResult(
            status=Status.FAIL,
            detail=f"browser-load probe subprocess timed out after {budget}s",
        )

    if proc.returncode != 0:
        excerpt = proc.stderr[-2000:]
        return BrowserResult(
            status=Status.FAIL,
            detail=f"browser-load probe exited {proc.returncode}; stderr: {excerpt}",
        )

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        excerpt = (proc.stdout + proc.stderr)[-2000:]
        return BrowserResult(
            status=Status.FAIL,
            detail=f"browser-load probe produced non-JSON stdout; output: {excerpt}",
        )

    return _classify(payload)


def _classify(payload: dict[str, Any]) -> BrowserResult:
    """Map one probe JSON payload to a `BrowserResult` per the browser.py contract.

    `state="rendered"` with no captured error is the only `PASS`. `state="error"`,
    `state=None` (no verdict — "exit 0 but no output = FAIL", plan §11), and any
    captured console/page/network error are all `FAIL`.
    """
    state = payload.get("state")
    console_errors = tuple(str(e) for e in payload.get("console_errors") or ())
    page_errors = tuple(str(e) for e in payload.get("page_errors") or ())
    network_failures = tuple(str(f) for f in payload.get("network_failures") or ())
    has_errors = bool(console_errors or page_errors or network_failures)

    if state == "rendered" and not has_errors:
        return BrowserResult(status=Status.PASS, detail="viewer reported body[data-state]=rendered")

    if state is None:
        detail = "no verdict: body[data-state] never appeared before the wait timeout"
    elif state == "error":
        detail = "viewer reported body[data-state]=error"
    else:
        detail = f"viewer reported an unexpected body[data-state]={state!r}"

    if has_errors:
        detail += (
            f"; console_errors={console_errors}, page_errors={page_errors}, "
            f"network_failures={network_failures}"
        )

    return BrowserResult(
        status=Status.FAIL,
        detail=detail,
        console_errors=console_errors,
        page_errors=page_errors,
        network_failures=network_failures,
    )
