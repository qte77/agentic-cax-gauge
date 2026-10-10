"""In-clone probe: load one viewer page via polyfetch and print a JSON verdict.

Runs with polyfetch's own interpreter (`uv run --directory <polyfetch> python
<this file> <url> <timeout>`, plan §9) so it can import `polyfetch_scrape`, which is
never a caxgauge dependency and is not installed in caxgauge's own venv (that is
also why pyright excludes this directory — see `pyproject.toml`). This script
therefore imports only the standard library plus `polyfetch_scrape`; it cannot
import `caxgauge` itself.

Prints exactly one JSON object to stdout:
`{"state": "rendered"|"error"|null, "console_errors": [...], "page_errors": [...],
"network_failures": [...]}`. `state` is `null` when `body[data-state]` never
appeared before the wait timeout — a hard failure, not "still loading"
(`viewer/README.md` -> "Consuming this page headlessly"; plan §11's "exit 0 but no
output = FAIL" rule applied to this page).

`src/caxgauge/verify/browser.py` is the only intended caller, and it alone decides
pass/fail — this script never emits a verdict word itself
(`.claude/rules/verification-honesty.md`).
"""

import json
import sys
from typing import Any

from polyfetch_scrape import render_session

_VIEWPORT = (800, 600)


def _wait_for_state(
    session: Any,  # noqa: ANN401 - no stubs for polyfetch_scrape's RenderSession here
    timeout_s: float,
) -> tuple[str | None, str | None]:
    """Wait for `body[data-state]` and read it structurally.

    Uses `get_attribute`, never `page.evaluate` of page globals (plan §9.2.1 —
    Patchright's isolated world reads page-script globals back as `undefined` even
    on success).

    Args:
        session: The active `polyfetch_scrape` `RenderSession`.
        timeout_s: Wait budget in seconds (Playwright/Patchright waits are in ms).

    Returns:
        `(state, None)` on success, or `(None, error_message)` if the selector
        never appeared within the timeout.
    """
    try:
        session.page.wait_for_selector("body[data-state]", timeout=timeout_s * 1000)
    except Exception as exc:  # any wait failure (incl. timeout) means no verdict
        return None, str(exc)
    return session.page.get_attribute("body[data-state]", "data-state"), None


def _probe(url: str, timeout_s: float) -> dict[str, object]:
    """Load `url` in a managed polyfetch session and collect the verdict + evidence.

    Args:
        url: The viewer page URL to load (`viewer/README.md`'s URL contract).
        timeout_s: Wait/session budget in seconds.

    Returns:
        A JSON-serialisable mapping matching this module's stdout contract.
    """
    page_errors: list[str] = []
    try:
        with render_session(url, timeout=timeout_s, viewport=_VIEWPORT) as session:
            session.page.on("pageerror", lambda exc: page_errors.append(str(exc)))
            state, wait_error = _wait_for_state(session, timeout_s)
            if wait_error is not None:
                page_errors.append(wait_error)
            console_errors = [str(e) for e in session.console_errors]
            network_failures = [str(f) for f in session.network_failures]
    except Exception as exc:  # a session/navigation failure (e.g. FetchError) is state=None
        return {
            "state": None,
            "console_errors": [],
            "page_errors": [*page_errors, str(exc)],
            "network_failures": [],
        }
    return {
        "state": state,
        "console_errors": console_errors,
        "page_errors": page_errors,
        "network_failures": network_failures,
    }


def main() -> None:
    """Parse `argv` (`<url> <timeout>`), run the probe, print one JSON object."""
    url = sys.argv[1]
    timeout_s = float(sys.argv[2])
    print(json.dumps(_probe(url, timeout_s)))


if __name__ == "__main__":
    main()
