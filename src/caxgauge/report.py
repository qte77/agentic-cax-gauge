"""One human review artifact per part: render beside per-check verdicts (plan §7.1 wave 3).

The verdict is only ever `fail` (some check failed) or `review` (nothing obviously broken —
a human looks at the render and decides). There is no `pass` and never "verified"
(`.claude/rules/verification-honesty.md`). Writes `report.json` for machines and
`report.html` for the human.
"""

import html
import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from caxgauge.verify.types import (
    NECESSARY_NOT_SUFFICIENT,
    BrowserResult,
    CheckResult,
    PreflightResult,
    RenderedView,
    RenderResult,
    Status,
)

Verdict = Literal["fail", "review"]


class Report(BaseModel):
    """Everything a human needs to decide on one part."""

    model_config = ConfigDict(frozen=True)

    mesh: Path
    verdict: Verdict
    checks: tuple[CheckResult, ...]
    views: tuple[RenderedView, ...]
    render_skipped: bool
    source: Path | None = None

    @property
    def skipped(self) -> tuple[CheckResult, ...]:
        """Checks that checked nothing (no bound, or no tooling)."""
        return tuple(c for c in self.checks if c.status is Status.SKIP)


def build_report(
    mesh: Path,
    preflight: PreflightResult,
    browser: BrowserResult,
    render: RenderResult,
    *,
    source: Path | None = None,
) -> Report:
    """Combine all results; any `FAIL` makes the verdict `fail`, otherwise `review`.

    `source` is the part's design script, shown beside the renders so the human can compare
    intent with result. It informs the review only: it is never a check and never gates.
    """
    checks = (
        *preflight.checks,
        CheckResult(name="browser_load", status=browser.status, detail=browser.detail),
        CheckResult(name="render", status=render.status, detail=render.detail),
    )
    failed = any(c.status is Status.FAIL for c in checks)
    return Report(
        mesh=mesh,
        verdict="fail" if failed else "review",
        checks=checks,
        views=render.views,
        render_skipped=render.status is Status.SKIP,
        source=source,
    )


def write_report(report: Report, out_dir: Path) -> tuple[Path, Path]:
    """Write `report.json` and `report.html` into `out_dir`; return both paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "report.json"
    html_path = out_dir / "report.html"
    json_path.write_text(json.dumps(_as_json(report, out_dir), indent=2) + "\n")
    html_path.write_text(_as_html(report, out_dir))
    return json_path, html_path


def _rel(path: Path, out_dir: Path) -> str:
    return Path(os.path.relpath(path, out_dir)).as_posix()


def _as_json(report: Report, out_dir: Path) -> dict[str, object]:
    return {
        "mesh": report.mesh.as_posix(),
        "verdict": report.verdict,
        "label": NECESSARY_NOT_SUFFICIENT,
        "checks": [
            {"name": c.name, "status": c.status.value, "detail": c.detail} for c in report.checks
        ],
        "skipped": [c.name for c in report.skipped],
        "views": [{"name": v.name, "path": _rel(v.path, out_dir)} for v in report.views],
        "source": report.source.as_posix() if report.source else None,
    }


_STYLE = """
body { font: 14px/1.5 system-ui, sans-serif; margin: 16px; color: #1d1d1f; background: #fafafa; }
h1 { overflow-wrap: anywhere; }
.verdict { font-size: 20px; font-weight: 600; padding: 8px 12px; border-radius: 4px; }
.fail { background: #fde2e1; } .review { background: #fff4d6; }
.label, .norender { padding: 8px 12px; border-left: 4px solid #b26b00; background: #fff; }
.norender { border-color: #c0392b; font-weight: 600; }
.checks { overflow-x: auto; }
table { border-collapse: collapse; margin: 12px 0; }
td, th { border: 1px solid #ddd; padding: 4px 8px; text-align: left; vertical-align: top; }
.views { display: flex; flex-wrap: wrap; gap: 12px; }
.views figure { margin: 0; } .views img { max-width: 400px; width: 100%; border: 1px solid #ccc; }
.source pre { overflow-x: auto; padding: 8px 12px; background: #fff; border: 1px solid #ddd; }
"""


def _source_html(source: Path | None) -> str:
    """The design script as inert, escaped text — compare it with the renders by eye."""
    if source is None:
        return ""
    esc = html.escape
    text = source.read_text(errors="replace")
    return (
        f'<section class="source"><h2>Design source: {esc(source.name)}</h2>'
        "<p>The intent as written, for comparison with the renders. Not checked.</p>"
        f"<pre><code>{esc(text)}</code></pre></section>"
    )


def _as_html(report: Report, out_dir: Path) -> str:
    esc = html.escape
    rows = "".join(
        f"<tr><td>{esc(c.name)}</td><td>{esc(c.status.value.upper())}</td>"
        f"<td>{esc(c.detail)}</td></tr>"
        for c in report.checks
    )
    views = "".join(
        f'<figure><img src="{esc(_rel(v.path, out_dir))}" alt="{esc(v.name)} view">'
        f"<figcaption>{esc(v.name)}</figcaption></figure>"
        for v in report.views
    )
    norender = (
        '<p class="norender">No render: the primary gate did not run, so a human cannot '
        "judge this part from this report. Set CAXGAUGE_POLYFETCH_DIR and re-run.</p>"
        if report.render_skipped
        else ""
    )
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>caxgauge: {esc(report.mesh.name)}</title><style>{_STYLE}</style></head><body>"
        f"<h1>{esc(report.mesh.name)}</h1>"
        f'<p class="verdict {report.verdict}">Verdict: {report.verdict}</p>'
        f'<p class="label">{esc(NECESSARY_NOT_SUFFICIENT)}</p>{norender}'
        f'<div class="views">{views}</div>{_source_html(report.source)}'
        f'<div class="checks"><table><tr><th>Check</th><th>Status</th><th>Detail</th></tr>'
        f"{rows}</table></div>"
        "</body></html>\n"
    )
