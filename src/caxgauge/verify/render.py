"""Multi-view PNG capture via polyfetch + the static viewer (plan §7.1, §9, §11).

**The primary gate.** A human looks at these views beside the preflight verdict and
decides (`.claude/rules/verification-honesty.md`) — this module never emits a
"verified" detail string, and a `PASS` requires every requested view to have produced
a real PNG: "exit 0 but no output" is a hard fail here, not a pass, mirroring
i3mega's slicer validator (plan §11).

`polyfetch` is env-borrowed (`caxgauge.verify.substrate.polyfetch_dir`), never a
dependency: an unset/missing `CAXGAUGE_POLYFETCH_DIR`, or no `uv` on `PATH`, means this
leg reports `SKIP` — never `PASS` (an unsupplied bound is `SKIP`, never a pass).

Per view, this shells out to polyfetch's stable CLI (`../polyfetch-scrape/USING.md` →
"Commands"), pinned to the patchright tier and waiting for the viewer's own success
signal — `body[data-state="rendered"]`, never `pageerror` (plan §9.2: an error page
never reaches that state, so the wait times out into a failure instead of silently
producing a screenshot of a blank/error page).

Two deliberate deviations from the sketch in the task brief, both confirmed against
`USING.md` and `polyfetch fetch --help` directly rather than assumed:

- **No `--json`.** USING.md "Errors & exit codes": with `--json`, a failure's message
  moves to the JSON error schema on **stdout**; without it, `<ErrorType>: <message>`
  goes to **stderr**, which is where a FAIL's detail excerpt reads from. The screenshot
  is already verified on disk via `--screenshot-out`, so the `--json` response body
  (and its base64 `screenshot_b64` duplicate of the same PNG) is not needed.
- **Strip `UV_PROJECT_ENVIRONMENT`/`VIRTUAL_ENV` before the child `uv run`.** Both are
  commonly set by the caller to redirect *this* repo's own venv under `/tmp` (disk
  pressure under `/workspaces`); inherited unchanged, they would redirect polyfetch's
  `uv run --directory <polyfetch>` at the wrong project environment too, syncing
  polyfetch's (heavy, unrelated) lockfile into it. `USING.md`'s env-borrow contract is
  "runs in the clone's own `.venv`" — these two vars exist only to point `uv` elsewhere
  and must not leak into the child.
"""

import os
import shutil
import subprocess
from pathlib import Path

from caxgauge.verify.substrate import POLYFETCH_ENV, polyfetch_dir, serve_viewer
from caxgauge.verify.types import RenderedView, RenderResult, Status

DEFAULT_VIEWS = ("front", "iso", "top", "right")

_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
_STDERR_EXCERPT_LIMIT = 200
_SUBPROCESS_TIMEOUT_BUFFER_S = 10.0
_SKIP_DETAIL = (
    f"no render: polyfetch unavailable — set {POLYFETCH_ENV} to a checkout and have 'uv' on PATH"
)


def render_views(
    mesh: Path,
    out_dir: Path,
    *,
    views: tuple[str, ...] = DEFAULT_VIEWS,
    size: tuple[int, int] = (800, 600),
    timeout: float = 60.0,
) -> RenderResult:
    """Capture one PNG per named camera preset through polyfetch's patchright tier.

    Args:
        mesh: Path to the exported STL to render.
        out_dir: Directory the PNGs are written to, as `<mesh-stem>-<view>.png`.
        views: Camera presets to capture (`viewer/README.md` → "Camera presets").
        size: `(width, height)` in px — passed to the viewer's `w`/`h` query params and
            matched to polyfetch's `--viewport`, so the screenshot is the render and not
            the render plus surrounding page background.
        timeout: Per-view seconds given to polyfetch's own `--timeout`. This function's
            own subprocess guard adds a further buffer on top so polyfetch's own
            timeout failure surfaces first, as a normal non-zero exit.

    Returns:
        `SKIP` when polyfetch is unavailable (no `CAXGAUGE_POLYFETCH_DIR` checkout, or
        no `uv` on `PATH`) — never `PASS`. Otherwise `PASS` only when every requested
        view produced a real PNG; else `FAIL`, naming which views failed and why.
    """
    pf_dir = polyfetch_dir()
    uv = shutil.which("uv")
    if pf_dir is None or uv is None:
        return RenderResult(status=Status.SKIP, detail=_SKIP_DETAIL, requested_views=views)

    out_dir.mkdir(parents=True, exist_ok=True)
    produced: list[RenderedView] = []
    failures: list[str] = []

    width, height = size
    with serve_viewer(mesh) as viewer:
        for view in views:
            page_url = viewer.page_url(view, width=width, height=height)
            png = out_dir / f"{mesh.stem}-{view}.png"
            outcome = _capture_view(uv, pf_dir, page_url, view, png, size, timeout)
            if isinstance(outcome, RenderedView):
                produced.append(outcome)
            else:
                failures.append(outcome)

    if failures:
        detail = "render failed: " + "; ".join(failures)
        return RenderResult(
            status=Status.FAIL, detail=detail, requested_views=views, views=tuple(produced)
        )

    return RenderResult(
        status=Status.PASS,
        detail=f"{len(produced)} view(s) captured at {width}x{height}",
        requested_views=views,
        views=tuple(produced),
    )


def _capture_view(
    uv: str,
    pf_dir: Path,
    page_url: str,
    view: str,
    png: Path,
    size: tuple[int, int],
    timeout: float,
) -> RenderedView | str:
    """Capture one view; returns the `RenderedView` on success, a failure reason on FAIL."""
    cmd = _build_command(uv, pf_dir, page_url, png, size, timeout)
    try:
        result = _run_polyfetch(cmd, timeout + _SUBPROCESS_TIMEOUT_BUFFER_S)
    except subprocess.TimeoutExpired:
        return f"{view}: timed out after {timeout}s"
    if result.returncode != 0:
        return f"{view}: exit {result.returncode}: {_excerpt(result.stderr)}"
    if not _is_valid_png(png):
        return f"{view}: exit 0 but no valid PNG at {png}"
    return RenderedView(name=view, path=png)


def _build_command(
    uv: str, pf_dir: Path, page_url: str, png: Path, size: tuple[int, int], timeout: float
) -> list[str]:
    """Build one `polyfetch fetch` invocation for one view (`USING.md` → "Commands").

    No `--json` — see the module docstring: with `--json`, a failure's message moves
    to stdout instead of stderr. `--viewport` matches `page_url`'s own `w`/`h` query
    params (`viewer/README.md` → "Consuming this page headlessly").
    """
    width, height = size
    viewport = f"{width}x{height}"
    return [
        uv,
        "run",
        "--directory",
        str(pf_dir),
        "polyfetch",
        "fetch",
        page_url,
        "--tier",
        "patchright",
        "--viewport",
        viewport,
        "--wait-for-selector",
        'body[data-state="rendered"]',
        "--screenshot",
        "viewport",
        "--screenshot-out",
        str(png),
        "--timeout",
        str(timeout),
    ]


def _run_polyfetch(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
    """Run one polyfetch CLI invocation; raises `subprocess.TimeoutExpired` on timeout.

    Absolute, list-form, no shell — `cmd[0]` is `shutil.which("uv")`'s absolute result,
    not a bare name (`# noqa: S603`: this is a fixed, non-shell argv list built entirely
    from this module's own values, not untrusted input passed through to a shell).

    `UV_PROJECT_ENVIRONMENT`/`VIRTUAL_ENV` are stripped from the child's environment —
    see the module docstring's second deviation note for why leaving them set would be
    wrong, not merely redundant.
    """
    env = {
        k: v for k, v in os.environ.items() if k not in ("UV_PROJECT_ENVIRONMENT", "VIRTUAL_ENV")
    }
    return subprocess.run(  # noqa: S603
        cmd, capture_output=True, timeout=timeout, check=False, env=env
    )


def _is_valid_png(path: Path) -> bool:
    """Whether `path` exists, is non-empty, and starts with the PNG magic bytes."""
    try:
        if not path.is_file() or path.stat().st_size == 0:
            return False
        with path.open("rb") as handle:
            return handle.read(len(_PNG_MAGIC)) == _PNG_MAGIC
    except OSError:
        return False


def _excerpt(data: bytes, limit: int = _STDERR_EXCERPT_LIMIT) -> str:
    """A short, decode-safe **tail** excerpt of subprocess stderr for a failure detail.

    The tail, not the head: a `uv run` startup/sync notice (e.g. the harmless "does not
    match the project environment … will be ignored" warning) prints first, and the
    actual `<ErrorType>: <message>` line polyfetch itself writes comes last.
    """
    text = data.decode("utf-8", errors="replace").strip()
    return text if len(text) <= limit else "…" + text[-limit:]
