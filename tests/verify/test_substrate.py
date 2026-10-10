"""Shared wave-2 substrate: serving the viewer + mesh, locating polyfetch (plan §7.1, §9)."""

import http.client
import urllib.parse
from pathlib import Path

import pytest

from caxgauge.verify.substrate import POLYFETCH_ENV, polyfetch_dir, serve_viewer

FIXTURE = Path(__file__).parent.parent / "fixtures" / "good.stl"


def _get(url: str) -> bytes:
    """GET over plain HTTP only (no `file:`/custom schemes, unlike `urlopen`)."""
    parts = urllib.parse.urlsplit(url)
    conn = http.client.HTTPConnection(parts.netloc, timeout=5)
    try:
        conn.request("GET", f"{parts.path}?{parts.query}" if parts.query else parts.path)
        return conn.getresponse().read()
    finally:
        conn.close()


def test_serves_viewer_and_mesh_same_origin():
    with serve_viewer(FIXTURE) as viewer:
        assert viewer.base.startswith("http://127.0.0.1:")
        assert b"STLLoader" in _get(f"{viewer.base}/viewer/index.html")
        assert _get(f"{viewer.base}/mesh.stl") == FIXTURE.read_bytes()


def test_page_url_carries_mesh_view_and_size():
    with serve_viewer(FIXTURE) as viewer:
        url = viewer.page_url("top", width=640, height=480)
    assert url.startswith(viewer.base)
    assert "mesh=" in url
    assert "view=top" in url
    assert "w=640" in url
    assert "h=480" in url


def test_server_stops_on_exit():
    with serve_viewer(FIXTURE) as viewer:
        base = viewer.base
    with pytest.raises(ConnectionRefusedError):
        _get(f"{base}/mesh.stl")


def test_polyfetch_dir_unset_is_none(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv(POLYFETCH_ENV, raising=False)
    assert polyfetch_dir() is None


def test_polyfetch_dir_missing_path_is_none(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path / "absent"))
    assert polyfetch_dir() is None


def test_polyfetch_dir_existing_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    monkeypatch.setenv(POLYFETCH_ENV, str(tmp_path))
    assert polyfetch_dir() == tmp_path
