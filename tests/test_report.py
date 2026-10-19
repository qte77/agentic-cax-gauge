"""Report: one human review artifact per part (plan §7.1 wave 3). Green is never "verified"."""

import json
from pathlib import Path

from caxgauge.report import build_report, write_report
from caxgauge.verify.types import (
    NECESSARY_NOT_SUFFICIENT,
    BrowserResult,
    CheckResult,
    PreflightResult,
    RenderedView,
    RenderResult,
    Status,
)

MESH = Path("part.stl")


def _preflight(*checks: tuple[str, Status, str]) -> PreflightResult:
    return PreflightResult(
        checks=tuple(CheckResult(name=n, status=s, detail=d) for n, s, d in checks)
    )


def _render(tmp_path: Path) -> RenderResult:
    views = tuple(RenderedView(name=v, path=tmp_path / f"part-{v}.png") for v in ("front", "iso"))
    return RenderResult(
        status=Status.PASS, detail="2 view(s)", requested_views=("front", "iso"), views=views
    )


_BROWSER_OK = BrowserResult(status=Status.PASS, detail="rendered")
_ALL_PASS = _preflight(
    ("watertight", Status.PASS, "closed"),
    ("bbox", Status.PASS, "fits"),
)


def test_no_failure_means_human_review_never_pass(tmp_path: Path):
    report = build_report(MESH, _ALL_PASS, _BROWSER_OK, _render(tmp_path))
    assert report.verdict == "review"


def test_any_failed_check_makes_the_verdict_fail(tmp_path: Path):
    preflight = _preflight(("watertight", Status.FAIL, "open edges"))
    assert build_report(MESH, preflight, _BROWSER_OK, _render(tmp_path)).verdict == "fail"
    browser = BrowserResult(status=Status.FAIL, detail="data-state=error")
    assert build_report(MESH, _ALL_PASS, browser, _render(tmp_path)).verdict == "fail"
    render = RenderResult(status=Status.FAIL, detail="iso: exit 1", requested_views=("iso",))
    assert build_report(MESH, _ALL_PASS, _BROWSER_OK, render).verdict == "fail"


def test_written_report_carries_label_and_never_says_verified(tmp_path: Path):
    report = build_report(MESH, _ALL_PASS, _BROWSER_OK, _render(tmp_path))
    json_path, html_path = write_report(report, tmp_path)
    for path in (json_path, html_path):
        text = path.read_text()
        assert NECESSARY_NOT_SUFFICIENT in text
        assert "verified" not in text.lower()


def test_report_names_the_bounds_that_were_not_supplied(tmp_path: Path):
    preflight = _preflight(
        ("watertight", Status.PASS, "closed"),
        ("bbox", Status.SKIP, "no --envelope given"),
        ("volume", Status.SKIP, "no --volume-band given"),
    )
    report = build_report(MESH, preflight, _BROWSER_OK, _render(tmp_path))
    data = json.loads(write_report(report, tmp_path)[0].read_text())
    assert data["skipped"] == ["bbox", "volume"]
    html = (tmp_path / "report.html").read_text()
    assert "--envelope" in html
    assert "--volume-band" in html


def test_skipped_render_is_shown_loudly(tmp_path: Path):
    render = RenderResult(
        status=Status.SKIP, detail="no render: polyfetch unavailable", requested_views=("iso",)
    )
    browser = BrowserResult(status=Status.SKIP, detail="polyfetch unavailable")
    report = build_report(MESH, _ALL_PASS, browser, render)
    assert report.verdict == "review"
    html = write_report(report, tmp_path)[1].read_text()
    assert "No render" in html


def test_html_shows_each_view_by_relative_path(tmp_path: Path):
    report = build_report(MESH, _ALL_PASS, _BROWSER_OK, _render(tmp_path))
    html = write_report(report, tmp_path)[1].read_text()
    assert 'src="part-front.png"' in html
    assert 'src="part-iso.png"' in html


def test_html_is_readable_on_a_phone(tmp_path: Path):
    # Without a viewport meta tag, mobile browsers lay the page out at desktop width and shrink it.
    report = build_report(MESH, _ALL_PASS, _BROWSER_OK, _render(tmp_path))
    html = write_report(report, tmp_path)[1].read_text()
    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in html


def test_html_escapes_check_details(tmp_path: Path):
    preflight = _preflight(("watertight", Status.FAIL, "<script>alert(1)</script>"))
    report = build_report(MESH, preflight, _BROWSER_OK, _render(tmp_path))
    html = write_report(report, tmp_path)[1].read_text()
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_json_lists_every_check_with_its_status(tmp_path: Path):
    report = build_report(MESH, _ALL_PASS, _BROWSER_OK, _render(tmp_path))
    data = json.loads(write_report(report, tmp_path)[0].read_text())
    assert data["verdict"] == "review"
    assert data["mesh"] == "part.stl"
    assert [(c["name"], c["status"]) for c in data["checks"]] == [
        ("watertight", "pass"),
        ("bbox", "pass"),
        ("browser_load", "pass"),
        ("render", "pass"),
    ]
