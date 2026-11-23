"""In-clone probe for `release_smoke.py`: load each page on each preset, measure, print JSON.

Runs under polyfetch's own interpreter (`uv run --directory <polyfetch> python <this file>
<config-json>`), so it imports only the standard library plus `polyfetch_scrape`, never
`caxgauge`. It measures and never decides: `release_smoke.classify` does that.

The DOM is read with `page.evaluate` of DOM properties only (sizes, `img.complete`), which
Patchright's isolated world shares with the page; page-script globals are never read.

Prints one JSON object: `{"cells": [{"cell", "page", "error", "console_errors",
"page_errors", "network_failures", "scroll_width", "client_width", "images", "targets",
"screenshot"}, ...]}`.
"""

import json
import re
import sys
from typing import Any

from polyfetch_scrape import render_session

# Visible pointer targets, plus whether each sits inside text (a non-blank text node next
# to it), which WCAG 2.2 SC 2.5.5's "Inline" exception exempts.
_MEASURE = """() => {
  const de = document.documentElement;
  const besideText = (n) => n && n.nodeType === Node.TEXT_NODE && n.textContent.trim() !== "";
  const targets = [...document.querySelectorAll(
    "a[href], button, input, select, textarea, summary, [role=button]")]
    .map((e) => ({e, r: e.getBoundingClientRect()}))
    .filter(({r}) => r.width > 0 && r.height > 0)
    .map(({e, r}) => ({
      text: (e.textContent || e.getAttribute("aria-label") || e.tagName).trim().slice(0, 60),
      w: Math.round(r.width), h: Math.round(r.height),
      in_text: besideText(e.previousSibling) || besideText(e.nextSibling),
    }));
  const images = [...document.images].map((i) => ({
    src: i.getAttribute("src"), loaded: i.complete && i.naturalWidth > 0}));
  return {scroll_width: de.scrollWidth, client_width: de.clientWidth, images, targets};
}"""


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _load(cell: dict[str, Any], page: str, config: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {"cell": cell["name"], "page": page, "error": None}
    page_errors: list[str] = []
    shot = f"{config['out']}/{_slug(cell['name'])}--{_slug(page)}.png"
    viewport = tuple(cell["viewport"]) if cell["viewport"] else None
    try:
        with render_session(
            f"{config['base']}/{page}",
            wait_until="load",
            timeout=config["timeout"],
            device=cell["device"],
            viewport=viewport,
        ) as session:
            session.page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            result.update(session.page.evaluate(_MEASURE))
            session.page.screenshot(path=shot, full_page=True)
            result["console_errors"] = [str(e) for e in session.console_errors]
            result["network_failures"] = [str(f) for f in session.network_failures]
    except Exception as exc:  # a failed launch or navigation is a result, not a crash
        result["error"] = str(exc)
    result["page_errors"] = page_errors
    result["screenshot"] = shot
    return result


def main() -> None:
    """Parse the JSON config from `argv[1]`, load every cell, print one JSON object."""
    config = json.loads(sys.argv[1])
    cells = [_load(c, p, config) for c in config["matrix"] for p in config["pages"]]
    print(json.dumps({"cells": cells}))


if __name__ == "__main__":
    main()
