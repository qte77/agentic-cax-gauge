"""`caxgauge check MESH` — the documented command consumers adopt (plan §7.1 wave 4, §8).

Wiring only, no check logic. Writes `report.json` + `report.html` and exits `0` for
`review` (nothing obviously broken — a human decides), `1` for `fail`, `2` for a usage
error. There is no "pass" exit: green is necessary, not sufficient.
"""

import argparse
import sys
from pathlib import Path

from caxgauge.report import build_report, write_report
from caxgauge.verify.browser import browser_load_check
from caxgauge.verify.preflight import preflight
from caxgauge.verify.render import render_views
from caxgauge.verify.types import NECESSARY_NOT_SUFFICIENT, BrowserResult, RenderResult, Status

_NO_RENDER = "skipped: --no-render given"


def _floats(text: str, count: int, name: str) -> tuple[float, ...]:
    parts = text.split(",")
    try:
        values = tuple(float(p) for p in parts)
    except ValueError:
        values = ()
    if len(values) != count:
        msg = f"{name} needs {count} comma-separated numbers, got {text!r}"
        raise argparse.ArgumentTypeError(msg)
    return values


def _envelope(text: str) -> tuple[float, float, float]:
    x, y, z = _floats(text, 3, "--envelope")
    return x, y, z


def _band(text: str) -> tuple[float, float]:
    low, high = _floats(text, 2, "--volume-band")
    if low > high:
        msg = f"--volume-band min {low} is greater than max {high}"
        raise argparse.ArgumentTypeError(msg)
    return low, high


def _existing_file(text: str) -> Path:
    path = Path(text)
    if not path.is_file():
        msg = f"mesh file not found: {text}"
        raise argparse.ArgumentTypeError(msg)
    return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="caxgauge", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Check one exported mesh and write a review report.")
    check.add_argument("mesh", type=_existing_file, help="Exported STL to check.")
    check.add_argument("--envelope", type=_envelope, metavar="X,Y,Z", help="Max extents (mm).")
    check.add_argument("--volume-band", type=_band, metavar="MIN,MAX", help="Volume (mm³).")
    check.add_argument("--out", type=Path, help="Report directory (default: reports/<stem>).")
    check.add_argument("--no-render", action="store_true", help="Skip browser + render.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run `caxgauge check`; return the exit status.

    Args:
        argv: Arguments without the program name (default: `sys.argv[1:]`).

    Returns:
        0 for a `review` verdict, 1 for `fail` (usage errors exit 2 via argparse).
    """
    args = _parser().parse_args(argv)
    mesh: Path = args.mesh
    out: Path = args.out or Path("reports") / mesh.stem

    checked = preflight(mesh, envelope=args.envelope, volume_band=args.volume_band)
    if args.no_render:
        browser = BrowserResult(status=Status.SKIP, detail=_NO_RENDER)
        render = RenderResult(status=Status.SKIP, detail=_NO_RENDER, requested_views=())
    else:
        browser = browser_load_check(mesh)
        render = render_views(mesh, out)

    report = build_report(mesh, checked, browser, render)
    _, html_path = write_report(report, out)

    print(f"verdict: {report.verdict}")
    print(NECESSARY_NOT_SUFFICIENT)
    for check in report.skipped:
        print(f"  SKIP {check.name}: {check.detail}")
    print(f"report: {html_path}")
    return 1 if report.verdict == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
