"""Shared wave-2 substrate: serve the viewer beside a mesh, and locate polyfetch (plan §9).

`browser.py` and `render.py` both drive `viewer/index.html` through polyfetch. The viewer
and the mesh are served from one temporary directory on one origin, so the page's `fetch()`
of the mesh never trips CORS (`viewer/README.md` → "Smoke-testing").

polyfetch is env-borrowed, never a dependency (plan §9): its checkout is named by
`CAXGAUGE_POLYFETCH_DIR`. Unset or missing means the browser legs report `SKIP`.
"""

import os
import tempfile
import threading
import urllib.parse
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

POLYFETCH_ENV = "CAXGAUGE_POLYFETCH_DIR"

# Repo-root `viewer/` (src/caxgauge/verify/substrate.py -> parents[3]). Works from a source
# checkout or editable install; packaging the viewer as package data is not done yet.
VIEWER_DIR = Path(__file__).resolve().parents[3] / "viewer"


@dataclass(frozen=True)
class ServedViewer:
    """A running local server with the viewer at `/viewer/` and the mesh at `/mesh.stl`."""

    base: str

    def page_url(self, view: str, *, width: int = 800, height: int = 600) -> str:
        """URL of the viewer page for one camera preset (contract: `viewer/README.md`)."""
        query = urllib.parse.urlencode(
            {"mesh": f"{self.base}/mesh.stl", "view": view, "w": width, "h": height}
        )
        return f"{self.base}/viewer/index.html?{query}"


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        """Silence per-request logging."""


@contextmanager
def serve_viewer(mesh: Path) -> Generator[ServedViewer]:
    """Serve `viewer/` and `mesh` on 127.0.0.1 (ephemeral port) for the block's duration.

    Args:
        mesh: Path to the STL to serve as `/mesh.stl`.

    Yields:
        The running server's base URL and a page-URL builder.
    """
    with tempfile.TemporaryDirectory(prefix="caxgauge-serve-") as root:
        (Path(root) / "viewer").symlink_to(VIEWER_DIR, target_is_directory=True)
        (Path(root) / "mesh.stl").symlink_to(mesh.resolve())
        handler = partial(_QuietHandler, directory=root)
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield ServedViewer(base=f"http://127.0.0.1:{server.server_address[1]}")
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


def polyfetch_dir() -> Path | None:
    """The polyfetch checkout named by `CAXGAUGE_POLYFETCH_DIR`, or None if unset/missing."""
    value = os.environ.get(POLYFETCH_ENV)
    if not value:
        return None
    path = Path(value)
    return path if path.is_dir() else None
