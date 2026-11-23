"""Pre-release smoke check of the GitHub Pages site across a device matrix.

Run before a minor or major tag (`make release_smoke`; CONTRIBUTING.md). It serves `site/`
on 127.0.0.1 and loads each page in `PAGES` on each preset in `MATRIX` through polyfetch's
Chromium (`release_smoke_probe.py`, run under polyfetch's own interpreter like
`caxgauge.verify.probes`). The probe only measures; `classify` alone decides.

A finding is any of: the page did not load; a console error, page error or failed request;
horizontal overflow; an image that did not load, or a report without its four view images;
on a touch preset, a target under 44x44 CSS px that is not inside text (WCAG 2.2 SC 2.5.5,
whose "Inline" exception covers a target "in a sentence or block of text"); a screenshot
that was not written. No model looks at anything: the screenshots are for a human.

Blind spot: Patchright disables the Console API, so a page script's own `console.error` and
uncaught exceptions are not seen; only browser-made messages such as a failed load are
(`AGENT_LEARNINGS.md`, "polyfetch's `pageerror`/`console_errors` did not fire").

Exit 0: no findings, which is necessary, not sufficient. Exit 1: findings, or the probe
broke. Exit 2: polyfetch or uv is missing, so nothing was checked.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from collections.abc import Generator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, cast

from caxgauge.verify.substrate import POLYFETCH_ENV, polyfetch_dir

ROOT = Path(__file__).resolve().parent.parent
PROBE = Path(__file__).resolve().parent / "release_smoke_probe.py"
TOUCH_MIN_PX = 44
LOAD_TIMEOUT_S = 30.0
_STARTUP_BUDGET_S = 60.0


@dataclass(frozen=True)
class Cell:
    """One device preset (a polyfetch `--device` name) or a plain desktop viewport."""

    name: str
    device: str | None
    viewport: tuple[int, int] | None
    touch: bool


MATRIX: tuple[Cell, ...] = (
    Cell("desktop 1280x800", device=None, viewport=(1280, 800), touch=False),
    Cell("iPhone 13", device="iPhone 13", viewport=None, touch=True),
    Cell("iPhone 13 landscape", device="iPhone 13 landscape", viewport=None, touch=True),
    Cell("Pixel 7", device="Pixel 7", viewport=None, touch=True),
    Cell("Pixel 7 landscape", device="Pixel 7 landscape", viewport=None, touch=True),
    Cell("iPad Mini", device="iPad Mini", viewport=None, touch=True),
    Cell("iPad Mini landscape", device="iPad Mini landscape", viewport=None, touch=True),
)

# Page path under site/ -> how many images it must show (a report shows four views).
PAGES: dict[str, int] = {
    "index.html": 0,
    "so101-pipette-mount/report.html": 4,
}


def slug(text: str) -> str:
    """A file-name-safe form of a cell or page name."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _check_cell(cell: Cell, expected_images: int, result: Mapping[str, Any]) -> list[str]:
    """Every finding for one loaded page on one preset."""
    if result.get("error"):
        return [f"did not load: {result['error']}"]
    found = [f"console error: {e}" for e in result.get("console_errors") or ()]
    found += [f"page error: {e}" for e in result.get("page_errors") or ()]
    found += [f"network failure: {f}" for f in result.get("network_failures") or ()]
    scroll, client = int(result.get("scroll_width", 0)), int(result.get("client_width", 0))
    if scroll > client:
        found.append(f"horizontal overflow: page is {scroll}px wide in a {client}px viewport")
    found += _check_images(expected_images, result.get("images") or [])
    if cell.touch:
        found += _check_targets(result.get("targets") or [])
    shot = result.get("screenshot")
    if not shot or not Path(shot).is_file() or Path(shot).stat().st_size == 0:
        found.append("screenshot not written")
    return found


def _check_images(expected: int, images: Sequence[Mapping[str, Any]]) -> list[str]:
    found = [f"image did not load: {i.get('src')}" for i in images if not i.get("loaded")]
    if len(images) != expected:
        found.append(f"{len(images)} images, expected {expected}")
    return found


def _check_targets(targets: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        f"touch target under {TOUCH_MIN_PX}x{TOUCH_MIN_PX} CSS px: "
        f"{t.get('text')!r} is {t.get('w')}x{t.get('h')}"
        for t in targets
        if not t.get("in_text") and min(int(t.get("w", 0)), int(t.get("h", 0))) < TOUCH_MIN_PX
    ]


def classify(
    payload: Mapping[str, Any], *, matrix: Sequence[Cell], pages: Mapping[str, int]
) -> list[str]:
    """Turn the probe's JSON into findings, one line each, naming preset and page.

    Every (preset, page) pair in the matrix must have a result: a missing one is a finding,
    so an empty output fails every pair instead of reading as clean.
    """
    results = {(r.get("cell"), r.get("page")): r for r in payload.get("cells") or ()}
    findings: list[str] = []
    for cell in matrix:
        for page, expected in pages.items():
            result = results.get((cell.name, page))
            if result is None:
                findings.append(f"{cell.name} · {page}: no result from the probe")
                continue
            findings += [f"{cell.name} · {page}: {f}" for f in _check_cell(cell, expected, result)]
    return findings


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        """Silence per-request logging."""


@contextmanager
def _serve(site: Path) -> Generator[str]:
    """Serve `site` on 127.0.0.1 (ephemeral port) for the block's duration; yield the base URL."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(_QuietHandler, directory=str(site)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def _tools() -> tuple[str, Path] | None:
    uv, polyfetch = shutil.which("uv"), polyfetch_dir()
    return (uv, polyfetch) if uv and polyfetch else None


def _run_probe(cmd: list[str], *, timeout: float) -> subprocess.CompletedProcess[str]:
    """Run the probe; the seam tests monkeypatch. Drops vars that would pick this venv."""
    env = {
        k: v for k, v in os.environ.items() if k not in ("UV_PROJECT_ENVIRONMENT", "VIRTUAL_ENV")
    }
    return subprocess.run(  # noqa: S603 - absolute uv path, list args, no shell
        cmd, capture_output=True, text=True, timeout=timeout, check=False, env=env
    )


def _parse(proc: subprocess.CompletedProcess[str]) -> dict[str, Any] | str:
    """The probe's payload, or why there is none."""
    if proc.returncode != 0:
        return f"probe exited {proc.returncode}; stderr: {proc.stderr[-2000:]}"
    try:
        payload: Any = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return f"probe printed no JSON; output: {(proc.stdout + proc.stderr)[-2000:]}"
    if not isinstance(payload, dict) or not isinstance(payload.get("cells"), list):  # pyright: ignore[reportUnknownMemberType]
        return f"probe JSON has no cells list: {proc.stdout[:200]}"
    return cast("dict[str, Any]", payload)


def run(site: Path, out: Path, *, matrix: Sequence[Cell], pages: Mapping[str, int]) -> list[str]:
    """Load every page on every preset and return the findings (empty: none found).

    Raises:
        RuntimeError: polyfetch or uv is missing (`main` checks first and exits 2).
    """
    tools = _tools()
    if tools is None:
        raise RuntimeError(f"needs uv and {POLYFETCH_ENV}")
    uv, polyfetch = tools
    out.mkdir(parents=True, exist_ok=True)
    # Only the names this run writes (`release_smoke_probe._load`): `--out` may hold other PNGs.
    for cell in matrix:
        for page in pages:
            (out / f"{slug(cell.name)}--{slug(page)}.png").unlink(missing_ok=True)
    budget = len(matrix) * len(pages) * LOAD_TIMEOUT_S + _STARTUP_BUDGET_S
    with _serve(site) as base:
        config = {
            "base": base,
            "out": str(out.resolve()),
            "timeout": LOAD_TIMEOUT_S,
            "pages": list(pages),
            "matrix": [asdict(c) for c in matrix],
        }
        cmd = [uv, "run", "--directory", str(polyfetch), "python", str(PROBE), json.dumps(config)]
        try:
            proc = _run_probe(cmd, timeout=budget)
        except subprocess.TimeoutExpired:
            return [f"probe timed out after {budget}s"]
    payload = _parse(proc)
    if isinstance(payload, str):
        return [payload]
    return classify(payload, matrix=matrix, pages=pages)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry: print findings and a labelled summary; return the exit code."""
    parser = argparse.ArgumentParser(description="Pre-release smoke check of site/.")
    parser.add_argument("--site", type=Path, default=ROOT / "site")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "release-smoke")
    args = parser.parse_args(argv)
    if _tools() is None:
        print(f"release_smoke: SKIP — not checked: needs uv and {POLYFETCH_ENV} (with Chromium)")
        return 2
    findings = run(args.site, args.out, matrix=MATRIX, pages=PAGES)
    for finding in findings:
        print(f"release_smoke: {finding}")
    cells = len(MATRIX) * len(PAGES)
    if findings:
        print(f"release_smoke: {len(findings)} finding(s) across {cells} page loads")
        return 1
    print(
        f"release_smoke: no findings on {cells} page loads — necessary, not sufficient: "
        f"look at the screenshots in {args.out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
