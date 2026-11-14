"""Per-run provenance for the benchmark (plan §5 BENCH-3 item 5).

Prints one JSON object: which harness commit ran, a hash of the exact brief, and the versions
of the CAD tool (for build123d, also its OCCT binding) and of Claude Code. Without these a
run can't be re-run or compared later, and they can't be backfilled: the 30 pilot runs have
none. `bench/run.sh` writes it to each run's `provenance.json`; the ledger `runs.tsv` keeps its
columns. The Python tool versions come from the same unpinned `uv run --with` resolution the
run uses, seconds before it, not from inside the run itself.

Usage: python3 -I bench/provenance.py --brief BRIEF.md --tool TOOL --model MODEL
"""

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_PY_VERSION = "import {m}; print({m}.{attr})"
_BUILD123D_VERSION = """
from importlib import metadata
import build123d
ocp = "unknown"
for name in ("cadquery-ocp-novtk", "cadquery-ocp"):
    try:
        ocp = metadata.version(name)
        break
    except metadata.PackageNotFoundError:
        pass
print(f"build123d {build123d.__version__}, OCP {ocp}")
"""
_TOOL_VERSION: dict[str, list[str]] = {
    "build123d": [
        *("uv", "run", "--no-project", "--with", "build123d", "python", "-c"),
        _BUILD123D_VERSION,
    ],
    "ifcopenshell": [
        *("uv", "run", "--no-project", "--with", "ifcopenshell", "python", "-c"),
        _PY_VERSION.format(m="ifcopenshell", attr="version"),
    ],
    "openscad": ["openscad", "--version"],
    "solidcraft": ["solidcraft-cli", "--version"],
}


def _run(cmd: list[str]) -> str:
    """First non-empty output line of `cmd`, or why it couldn't be read."""
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=180, check=False)  # noqa: S603 — fixed argv, no shell
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"unavailable: {type(exc).__name__}"
    # stdout first: uv reports its installs on stderr; OpenSCAD prints its version there.
    out = done.stdout.strip() or done.stderr.strip()
    if done.returncode != 0 or not out:
        return f"unavailable: exit {done.returncode}"
    return out.splitlines()[0].strip()


def _dirty() -> str:
    """`yes` if tracked files differ from the harness commit (the commit is then incomplete)."""
    try:
        done = subprocess.run(  # noqa: S603 — fixed argv, no shell
            ["git", "-C", str(REPO), "status", "--porcelain", "--untracked-files=no"],  # noqa: S607
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unknown"
    if done.returncode != 0:
        return "unknown"
    return "yes" if done.stdout.strip() else "no"


def provenance(brief: Path, tool: str, model: str) -> dict[str, str]:
    """Collect the run's provenance; never raises for a missing tool."""
    commit = _run(["git", "-C", str(REPO), "rev-parse", "HEAD"])
    return {
        "recorded_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "harness_commit": commit,
        "harness_dirty": _dirty(),
        "brief": brief.name,
        "brief_sha256": hashlib.sha256(brief.read_bytes()).hexdigest(),
        "tool": tool,
        "tool_version": _run(_TOOL_VERSION[tool]) if tool in _TOOL_VERSION else "unknown tool",
        "claude_code_version": _run(["claude", "--version"]),
        "model": model,
    }


def main() -> None:
    """Print the provenance JSON for one run."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--tool", required=True)
    parser.add_argument("--model", required=True)
    args = parser.parse_args()
    print(json.dumps(provenance(args.brief, args.tool, args.model), indent=2))


if __name__ == "__main__":
    main()
