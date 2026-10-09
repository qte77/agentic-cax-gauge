"""Command-line entry point (`caxgauge`). Checks arrive in M2 (docs/plans/001-v0.md §7)."""

import sys


def main() -> int:
    """Report that no checks exist yet and fail, so the stub can never read as a pass.

    Returns:
        Non-zero exit status.
    """
    print(
        "caxgauge: no checks implemented yet — preflight and render arrive in M2. "
        "Nothing was checked.",
        file=sys.stderr,
    )
    return 2
