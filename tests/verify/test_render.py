"""Behaviour tests for `render_views` (plan §7.1 wave 2, §9, §11).

Unit tests below monkeypatch `_run_polyfetch` so no real polyfetch/Chromium call ever
happens — they exercise `render_views`'s own control flow (SKIP/PASS/FAIL decisions,
PNG validation, naming) against a fake subprocess runner. The `browser`-marked tests at
the bottom are the real integration path (`pytest -m browser`, `CAXGAUGE_POLYFETCH_DIR`
set to a real polyfetch-scrape checkout with Chromium installed).

Strict TDD: written before `src/caxgauge/verify/render.py` exists.
"""

import struct
import subprocess
import zlib
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


def test_relative_out_dir_reaches_polyfetch_as_an_absolute_path(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    # polyfetch runs via `uv run --directory <polyfetch>`, which makes its cwd the polyfetch
    # checkout; a relative PNG path would then point inside that checkout (USING.md).
    _with_polyfetch_dir(monkeypatch, tmp_path)
    monkeypatch.chdir(tmp_path)
    seen: list[Path] = []

    def fake(cmd: list[str], timeout: float) -> subprocess.CompletedProcess[bytes]:
        seen.append(_screenshot_out(cmd))
        return _fake_success(cmd, timeout)

    monkeypatch.setattr(render_module, "_run_polyfetch", fake)

    result = render_views(FIXTURE, Path("reports/part"), views=("front",))

    assert result.status is Status.PASS
    assert seen == [tmp_path / "reports" / "part" / f"{FIXTURE.stem}-front.png"]
    assert seen[0].is_absolute()


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


def _decode_png(path: Path) -> tuple[int, int, int, bytes]:
    """Minimal stdlib PNG decoder (8-bit RGB/RGBA, non-interlaced) → (w, h, channels, raw)."""
    data = path.read_bytes()
    pos, idat, width, height, channels = 8, b"", 0, 0, 0
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos : pos + 4])
        kind, body = data[pos + 4 : pos + 8], data[pos + 8 : pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, color = struct.unpack(">IIBB", body[:10])
            assert (depth, body[12]) == (8, 0), "only 8-bit non-interlaced PNGs"
            channels = {2: 3, 6: 4}[color]
        elif kind == b"IDAT":
            idat += body
        pos += 12 + length
    raw, stride, out = zlib.decompress(idat), width * channels, bytearray()
    prev = bytearray(stride)
    for row in range(height):
        start = row * (stride + 1)
        line = bytearray(raw[start + 1 : start + 1 + stride])
        _unfilter(raw[start], line, prev, channels)
        out += line
        prev = line
    return width, height, channels, bytes(out)


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else (b if pb <= pc else c)


def _unfilter(kind: int, line: bytearray, prev: bytearray, channels: int) -> None:
    """Undo one PNG row filter in place (types 0-4: none/sub/up/average/paeth)."""
    for i in range(len(line)):
        a = line[i - channels] if i >= channels else 0
        c = prev[i - channels] if i >= channels else 0
        predictor = (0, a, prev[i], (a + prev[i]) // 2, _paeth(a, prev[i], c))[kind]
        line[i] = (line[i] + predictor) & 0xFF


def _part_aspect(path: Path) -> float:
    """Width/height of the bounding box of the part's (blue) pixels in a render."""
    width, height, channels, px = _decode_png(path)
    xs: list[int] = []
    ys: list[int] = []
    for y in range(height):
        for x in range(width):
            i = (y * width + x) * channels
            r, g, b = px[i], px[i + 1], px[i + 2]
            if b > r + 40 and b > g:  # the part's blue; background is grey, label is dark
                xs.append(x)
                ys.append(y)
    assert xs, f"no part pixels in {path}"
    return (max(xs) - min(xs) + 1) / (max(ys) - min(ys) + 1)


@pytest.mark.browser
def test_real_render_views_follow_cad_z_up(tmp_path: Path):
    # good.stl is a 20 (X) x 15 (Y) x 10 (Z) box. CAD exports are Z-up, so `top` looks
    # down -Z (20:15), `front` looks along +Y (20:10), `right` looks along -X (15:10).
    result = render_views(FIXTURE, tmp_path / "out", views=("top", "front", "right"))

    assert result.status is Status.PASS, result.detail
    aspects = {v.name: _part_aspect(v.path) for v in result.views}
    assert aspects["top"] == pytest.approx(20 / 15, rel=0.05)
    assert aspects["front"] == pytest.approx(20 / 10, rel=0.05)
    assert aspects["right"] == pytest.approx(15 / 10, rel=0.05)


@pytest.mark.browser
def test_real_top_view_shows_features_that_share_a_face_normal(tmp_path: Path):
    # The boss's top face and the plate's top face both point +Z, so flat shading alone
    # renders them as one colour and the boss vanishes from `top`. Feature edges must show it.
    boss = FIXTURE.parent / "feature_absorbed_intended.stl"  # 40x40x5 plate + d10 boss
    result = render_views(boss, tmp_path / "out", views=("top",))
    assert result.status is Status.PASS, result.detail

    width, height, channels, px = _decode_png(result.views[0].path)
    # Central quarter of the frame: inside the plate, away from its outer border and the label.
    dark = 0
    for y in range(height * 3 // 8, height * 5 // 8):
        for x in range(width * 3 // 8, width * 5 // 8):
            i = (y * width + x) * channels
            if max(px[i], px[i + 1], px[i + 2]) < 60:
                dark += 1
    assert dark > 50, f"no feature edges inside the plate ({dark} dark px)"


@pytest.mark.browser
def test_real_render_of_garbage_stl_fails_with_no_screenshot(tmp_path: Path):
    garbage = tmp_path / "garbage.stl"
    garbage.write_bytes(b"not an stl at all")
    out_dir = tmp_path / "out"

    result = render_views(garbage, out_dir, views=("front",), timeout=20.0)

    assert result.status is Status.FAIL
    assert list(out_dir.glob("*.png")) == []
