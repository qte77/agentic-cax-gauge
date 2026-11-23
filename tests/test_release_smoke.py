"""Behaviour tests for `scripts/release_smoke.py`, the pre-release check of `site/`.

The probe runs under polyfetch's interpreter and only measures; `release_smoke.classify`
alone turns its JSON into findings. Unit tests feed canned probe JSON, so they need no
Chromium. `test_real_site_and_forced_failures` drives real Chromium (marked `browser`).
"""

import json
import subprocess
from pathlib import Path

import pytest

import release_smoke as smoke
from caxgauge.verify.substrate import POLYFETCH_ENV

DESKTOP = smoke.Cell("desktop 1280x800", device=None, viewport=(1280, 800), touch=False)
PHONE = smoke.Cell("iPhone 13", device="iPhone 13", viewport=None, touch=True)
MATRIX = (DESKTOP, PHONE)
PAGES = {"index.html": 0, "report.html": 4}


def _cell(cell: smoke.Cell, page: str, tmp_path: Path, **over: object) -> dict[str, object]:
    shot = tmp_path / f"{smoke.slug(cell.name)}--{smoke.slug(page)}.png"
    shot.write_bytes(b"\x89PNG fake")
    images = [{"src": f"v{i}.png", "loaded": True} for i in range(PAGES[page])]
    base: dict[str, object] = {
        "cell": cell.name,
        "page": page,
        "error": None,
        "console_errors": [],
        "page_errors": [],
        "network_failures": [],
        "scroll_width": 390,
        "client_width": 390,
        "images": images,
        "targets": [],
        "screenshot": str(shot),
    }
    return {**base, **over}


def _clean(tmp_path: Path) -> list[dict[str, object]]:
    return [_cell(c, p, tmp_path) for c in MATRIX for p in PAGES]


def _findings(cells: list[dict[str, object]]) -> list[str]:
    return smoke.classify({"cells": cells}, matrix=MATRIX, pages=PAGES)


def _replace(cells: list[dict[str, object]], new: dict[str, object]) -> list[dict[str, object]]:
    key = (new["cell"], new["page"])
    return [new if (c["cell"], c["page"]) == key else c for c in cells]


def test_clean_run_has_no_findings(tmp_path: Path):
    assert _findings(_clean(tmp_path)) == []


@pytest.mark.parametrize(
    ("field", "value", "word"),
    [
        ("console_errors", ["TypeError: boom"], "console"),
        ("page_errors", ["SyntaxError: nope"], "page error"),
        ("network_failures", [{"url": "http://x/a.png", "status": 404}], "network"),
        ("error", "navigation timed out", "did not load"),
    ],
)
def test_each_captured_error_is_a_finding_naming_cell_and_page(
    tmp_path: Path, field: str, value: object, word: str
):
    cells = _replace(_clean(tmp_path), _cell(PHONE, "report.html", tmp_path, **{field: value}))

    findings = _findings(cells)

    assert len(findings) == 1
    assert "iPhone 13" in findings[0]
    assert "report.html" in findings[0]
    assert word in findings[0]


def test_horizontal_overflow_is_a_finding(tmp_path: Path):
    wide = _cell(PHONE, "index.html", tmp_path, scroll_width=520, client_width=390)

    findings = _findings(_replace(_clean(tmp_path), wide))

    assert len(findings) == 1
    assert "overflow" in findings[0]
    assert "520" in findings[0]


def test_an_image_that_did_not_load_is_a_finding(tmp_path: Path):
    images = [{"src": f"v{i}.png", "loaded": i != 2} for i in range(4)]
    broken = _cell(DESKTOP, "report.html", tmp_path, images=images)

    findings = _findings(_replace(_clean(tmp_path), broken))

    assert len(findings) == 1
    assert "v2.png" in findings[0]


@pytest.mark.parametrize("count", [0, 3, 5])
def test_wrong_view_image_count_is_a_finding_and_zero_never_passes(tmp_path: Path, count: int):
    images = [{"src": f"v{i}.png", "loaded": True} for i in range(count)]
    cell = _cell(DESKTOP, "report.html", tmp_path, images=images)

    findings = _findings(_replace(_clean(tmp_path), cell))

    assert len(findings) == 1
    assert f"{count} images" in findings[0]


def test_small_standalone_target_on_a_touch_preset_is_a_finding(tmp_path: Path):
    target = {"text": "tip_rack_holder", "w": 114, "h": 20, "in_text": False}
    cell = _cell(PHONE, "index.html", tmp_path, targets=[target])

    findings = _findings(_replace(_clean(tmp_path), cell))

    assert len(findings) == 1
    assert "tip_rack_holder" in findings[0]
    assert "114x20" in findings[0]


def test_small_target_is_not_a_finding_on_desktop_or_inside_text(tmp_path: Path):
    standalone = {"text": "a", "w": 114, "h": 20, "in_text": False}
    in_text = {"text": "b", "w": 114, "h": 20, "in_text": True}
    cells = _replace(
        _replace(_clean(tmp_path), _cell(DESKTOP, "index.html", tmp_path, targets=[standalone])),
        _cell(PHONE, "index.html", tmp_path, targets=[in_text]),
    )

    assert _findings(cells) == []


def test_a_matrix_cell_missing_from_the_output_is_a_finding(tmp_path: Path):
    cells = [c for c in _clean(tmp_path) if c["cell"] != PHONE.name or c["page"] != "index.html"]

    findings = _findings(cells)

    assert len(findings) == 1
    assert "iPhone 13" in findings[0]
    assert "no result" in findings[0]


def test_empty_output_fails_every_cell(tmp_path: Path):
    assert len(_findings([])) == len(MATRIX) * len(PAGES)


def test_a_missing_screenshot_is_a_finding(tmp_path: Path):
    cell = _cell(PHONE, "report.html", tmp_path, screenshot=str(tmp_path / "absent.png"))

    findings = _findings(_replace(_clean(tmp_path), cell))

    assert len(findings) == 1
    assert "screenshot" in findings[0]


def test_main_refuses_without_polyfetch(monkeypatch: pytest.MonkeyPatch, capsys, tmp_path: Path):
    monkeypatch.delenv(POLYFETCH_ENV, raising=False)
    calls = []
    monkeypatch.setattr(smoke, "_run_probe", lambda *a, **k: calls.append(1))

    rc = smoke.main(["--out", str(tmp_path)])

    assert rc == 2
    assert not calls
    out = capsys.readouterr().out
    assert "SKIP" in out
    assert "not checked" in out


def _main_with(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, proc: subprocess.CompletedProcess[str]
) -> int:
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(smoke.shutil, "which", lambda _name: "/usr/bin/uv")
    monkeypatch.setattr(smoke, "_run_probe", lambda *a, **k: proc)
    monkeypatch.setattr(smoke, "MATRIX", MATRIX)
    monkeypatch.setattr(smoke, "PAGES", PAGES)
    return smoke.main(["--out", str(tmp_path / "out")])


def test_main_clean_run_exits_0_with_the_honesty_label(
    monkeypatch: pytest.MonkeyPatch, capsys, tmp_path: Path
):
    stdout = json.dumps({"cells": _clean(tmp_path)})
    proc = subprocess.CompletedProcess(["probe"], 0, stdout=stdout, stderr="")

    rc = _main_with(monkeypatch, tmp_path, proc)

    out = capsys.readouterr().out
    assert rc == 0
    assert "necessary, not sufficient" in out
    assert "verified" not in out.lower()


def test_main_findings_exit_1(monkeypatch: pytest.MonkeyPatch, capsys, tmp_path: Path):
    cells = _replace(
        _clean(tmp_path), _cell(PHONE, "index.html", tmp_path, console_errors=["boom"])
    )
    proc = subprocess.CompletedProcess(["probe"], 0, stdout=json.dumps({"cells": cells}), stderr="")

    rc = _main_with(monkeypatch, tmp_path, proc)

    assert rc == 1
    assert "boom" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("returncode", "stdout"), [(1, ""), (0, "not json"), (0, "[]"), (0, '{"cells": 3}')]
)
def test_main_broken_probe_exits_1(
    monkeypatch: pytest.MonkeyPatch, capsys, tmp_path: Path, returncode: int, stdout: str
):
    proc = subprocess.CompletedProcess(["probe"], returncode, stdout=stdout, stderr="Traceback")

    rc = _main_with(monkeypatch, tmp_path, proc)

    assert rc == 1
    assert "verified" not in capsys.readouterr().out.lower()


def test_main_probe_timeout_exits_1(monkeypatch: pytest.MonkeyPatch, capsys, tmp_path: Path):
    def raise_timeout(*_a: object, **_k: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(cmd=["probe"], timeout=1.0)

    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    monkeypatch.setattr(smoke.shutil, "which", lambda _name: "/usr/bin/uv")
    monkeypatch.setattr(smoke, "_run_probe", raise_timeout)

    assert smoke.main(["--out", str(tmp_path)]) == 1
    assert "timed out" in capsys.readouterr().out


_BAD_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"></head><body>
<div style="width:2000px">wide</div>
<img src="missing.png" alt="front view">
<p><button style="width:30px;height:20px">x</button></p>
<p>A sentence with <a href="#">an inline link</a> in it.</p>
</body></html>"""


@pytest.mark.browser
def test_real_site_and_forced_failures(tmp_path: Path):
    """The committed `site/` has no findings; each detector fires on a forced-bad page.

    Needs `CAXGAUGE_POLYFETCH_DIR` with Chromium. Run with `pytest -m browser`.
    """
    site = Path(__file__).resolve().parent.parent / "site"
    assert smoke.run(site, tmp_path / "good", matrix=smoke.MATRIX, pages=smoke.PAGES) == []

    bad_site = tmp_path / "bad"
    bad_site.mkdir()
    (bad_site / "bad.html").write_text(_BAD_PAGE)
    phone = (smoke.MATRIX[1],)

    findings = smoke.run(bad_site, tmp_path / "shots", matrix=phone, pages={"bad.html": 1})

    text = "\n".join(findings)
    assert "overflow" in text
    assert "missing.png" in text
    assert "30x20" in text
    # Patchright disables the Console API, so a page script's own console.error is never
    # seen (AGENT_LEARNINGS.md); the browser's own failed-load message is.
    assert "console error: Failed to load resource" in text
    assert "inline link" not in text
