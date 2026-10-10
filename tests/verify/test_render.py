"""Behaviour tests for `render_views` (plan §7.1 wave 2, §9, §11).

Unit tests below monkeypatch `_run_polyfetch` so no real polyfetch/Chromium call ever
happens — they exercise `render_views`'s own control flow (SKIP/PASS/FAIL decisions,
PNG validation, naming) against a fake subprocess runner. The `browser`-marked tests at
the bottom are the real integration path (`pytest -m browser`, `CAXGAUGE_POLYFETCH_DIR`
set to a real polyfetch-scrape checkout with Chromium installed).

Strict TDD: written before `src/caxgauge/verify/render.py` exists.
"""

import subprocess
from pathlib import Path

import pytest

from caxgauge.verify import render as render_module
from caxgauge.verify.render import render_views
from caxgauge.verify.substrate import POLYFETCH_ENV
from caxgauge.verify.types import Status

FIXTURE = Path(__file__).parent.parent / "fixtures" / "good.stl"
_VIEWS = ("front", "iso", "top", "right")
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _screenshot_out(cmd: list[str]) -> Path:
    """Pull the `--screenshot-out` value back out of a built `polyfetch fetch` command."""
    return Path(cmd[cmd.index("--screenshot-out") + 1])


def _fake_success(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
    """A fake `_run_polyfetch` that writes a tiny valid PNG and reports exit 0."""
    del timeout
    _screenshot_out(cmd).write_bytes(_PNG_MAGIC + b"fake-png-body")
    return subprocess.CompletedProcess(cmd, 0, stdout=b"", stderr=b"")


def _with_polyfetch_dir(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    """Point `CAXGAUGE_POLYFETCH_DIR` at a real (empty) directory so the SKIP leg differs."""
    pf_dir = tmp_path / "polyfetch"
    pf_dir.mkdir()
    monkeypatch.setenv(POLYFETCH_ENV, str(pf_dir))
    return pf_dir


def test_env_unset_is_skip_naming_the_env_var(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.delenv(POLYFETCH_ENV, raising=False)
    result = render_views(FIXTURE, tmp_path / "out")
    assert result.status is Status.SKIP
    assert POLYFETCH_ENV in result.detail
    assert "verified" not in result.detail.lower()
    assert result.views == ()


def test_uv_missing_is_skip(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)
    monkeypatch.setattr(render_module.shutil, "which", lambda _name: None)
    result = render_views(FIXTURE, tmp_path / "out")
    assert result.status is Status.SKIP
    assert "verified" not in result.detail.lower()


def test_all_views_succeed_is_pass_with_four_views(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)
    monkeypatch.setattr(render_module, "_run_polyfetch", _fake_success)
    out_dir = tmp_path / "out"

    result = render_views(FIXTURE, out_dir, views=_VIEWS)

    assert result.status is Status.PASS
    assert [v.name for v in result.views] == list(_VIEWS)
    for view in result.views:
        assert view.path.is_file()
        assert view.path.read_bytes().startswith(_PNG_MAGIC)
    assert "verified" not in result.detail.lower()


def test_default_views_are_the_four_camera_presets(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)
    monkeypatch.setattr(render_module, "_run_polyfetch", _fake_success)

    result = render_views(FIXTURE, tmp_path / "out")

    assert [v.name for v in result.views] == ["front", "iso", "top", "right"]


def test_png_named_mesh_stem_dash_view(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)
    monkeypatch.setattr(render_module, "_run_polyfetch", _fake_success)
    out_dir = tmp_path / "out"

    result = render_views(FIXTURE, out_dir, views=("front",))

    expected = out_dir / f"{FIXTURE.stem}-front.png"
    assert expected.is_file()
    assert result.views[0].path == expected


def test_one_view_nonzero_exit_is_fail_naming_it(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        if any("view=top" in part for part in cmd):
            return subprocess.CompletedProcess(cmd, 1, stdout=b"", stderr=b"boom: selector wait")
        return _fake_success(cmd, timeout)

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, tmp_path / "out", views=_VIEWS)

    assert result.status is Status.FAIL
    assert "top" in result.detail
    assert "boom" in result.detail
    assert "verified" not in result.detail.lower()


def test_exit_zero_with_no_file_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        del timeout
        # Exit 0 but never write the PNG — the "exit 0 but no output = FAIL" rule.
        return subprocess.CompletedProcess(cmd, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, tmp_path / "out", views=("front",))

    assert result.status is Status.FAIL
    assert "front" in result.detail
    assert result.views == ()


def test_exit_zero_with_non_png_file_is_fail(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        del timeout
        _screenshot_out(cmd).write_bytes(b"not a png")
        return subprocess.CompletedProcess(cmd, 0, stdout=b"", stderr=b"")

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, tmp_path / "out", views=("front",))

    assert result.status is Status.FAIL
    assert result.views == ()


def test_timeout_is_fail_naming_the_view(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    _with_polyfetch_dir(monkeypatch, tmp_path)

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=timeout)

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, tmp_path / "out", views=("iso",), timeout=5.0)

    assert result.status is Status.FAIL
    assert "iso" in result.detail
    assert "timed out" in result.detail.lower()


def test_partial_failure_still_reports_the_views_that_succeeded(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    _with_polyfetch_dir(monkeypatch, tmp_path)

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        if any("view=iso" in part for part in cmd):
            return subprocess.CompletedProcess(cmd, 1, stdout=b"", stderr=b"fail")
        return _fake_success(cmd, timeout)

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, tmp_path / "out", views=("front", "iso"))

    assert result.status is Status.FAIL
    assert [v.name for v in result.views] == ["front"]


# -- Integration: real polyfetch + Chromium (pytest -m browser) --


@pytest.mark.browser
def test_real_render_of_good_part_produces_four_pngs(tmp_path: Path):
    out_dir = tmp_path / "out"

    result = render_views(FIXTURE, out_dir)

    assert result.status is Status.PASS, result.detail
    assert len(result.views) == 4
    for view in result.views:
        assert view.path.is_file()
        assert view.path.stat().st_size > 0


@pytest.mark.browser
def test_real_render_of_garbage_stl_fails_with_no_screenshot(tmp_path: Path):
    garbage = tmp_path / "garbage.stl"
    garbage.write_bytes(b"not an stl at all")
    out_dir = tmp_path / "out"

    result = render_views(garbage, out_dir, views=("front",), timeout=20.0)

    assert result.status is Status.FAIL
    assert list(out_dir.glob("*.png")) == []
