"""Blind labelling for the benchmark pilot (plan §5 BENCH).

`make`: copy each run's four renders under an anonymous ID into `site/bench-blind/`, with the
brief's prompt and nothing else — no tool name, no script, no check results — plus a sheet
`bench/labels-blind.csv` for the human to fill (`accept` yes/no, `reject_reason`). The
ID -> run key goes to `bench/blind-key.csv`; don't open it until the sheet is filled.

`unblind`: copy the filled sheet's answers into `bench/labels.csv` (accept, note).

Usage: python3 bench/blind.py make [--seed N]  |  python3 bench/blind.py unblind
Renders are copied, never re-made, so tessellation (OpenSCAD's faceted curves) can still
hint at the tool; that residual tell is noted on the page.
"""

import argparse
import csv
import html
import random
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RUNS = REPO / "site" / "bench"
OUT = REPO / "site" / "bench-blind"
SHEET = REPO / "bench" / "labels-blind.csv"
KEY = REPO / "bench" / "blind-key.csv"
LABELS = REPO / "bench" / "labels.csv"
VIEWS = ("iso", "front", "right", "top")


def _prompt(brief: Path) -> str:
    """The brief as the agent saw it: no front matter, no `# heading`, nothing from `Bounds:`."""
    parts = brief.read_text().split("---", 2)
    body = parts[2] if len(parts) == 3 else parts[0]
    lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("Bounds:"):
            break
        if not line.startswith("# "):
            lines.append(line)
    return "\n".join(lines).strip()


def _pilot_runs() -> list[tuple[str, str, str]]:
    with LABELS.open() as f:
        return [(r["brief"], r["tool"], r["run"]) for r in csv.DictReader(f)]


def make(seed: int) -> None:
    """Write the blind page, the empty sheet and the key, shuffled by `seed`."""
    runs = _pilot_runs()
    random.Random(seed).shuffle(runs)  # noqa: S311 — order only, not a secret
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    items: list[str] = []
    key: list[dict[str, str]] = []
    for i, (brief, tool, n) in enumerate(runs, 1):
        rid = f"B{i:02d}"
        src = RUNS / f"{brief}-{tool}-{n}"
        for view in VIEWS:
            png = src / f"part-{view}.png"
            if png.is_file():
                shutil.copy(png, OUT / f"{rid}-{view}.png")
        prompt = html.escape(_prompt(REPO / "bench" / "briefs" / f"{brief}.md"))
        imgs = "".join(
            f'<img src="{rid}-{v}.png" alt="{rid} {v} view">'
            for v in VIEWS
            if (OUT / f"{rid}-{v}.png").is_file()
        )
        items.append(f'<section id="{rid}"><h2>{rid}</h2><p>{prompt}</p>{imgs}</section>')
        key.append({"id": rid, "brief": brief, "tool": tool, "run": n})
    (OUT / "index.html").write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        "<title>Pilot: blind labelling</title><style>"
        "body{font:14px/1.5 system-ui,sans-serif;margin:16px;max-width:1100px}"
        "img{max-width:260px;width:48%;border:1px solid #ccc;margin:2px}"
        "section{border-top:1px solid #ddd;padding:8px 0}</style></head><body>"
        "<h1>Benchmark pilot: blind labelling</h1>"
        "<p>Each ID is one run, in random order, with the brief the agent was given and its "
        "four views. Tool names, scripts and check results are hidden. Record accept "
        "(yes/no) and, for a no, the reason, in <code>bench/labels-blind.csv</code>. "
        "Curves drawn as visible facets can hint at the tool; judge the part, not the "
        "mesh.</p>" + "".join(items) + "</body></html>\n"
    )
    with SHEET.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "accept", "reject_reason"])
        w.writerows([k["id"], "", ""] for k in key)
    with KEY.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "brief", "tool", "run"])
        w.writeheader()
        w.writerows(key)
    print(f"blind.py: {len(key)} runs -> {OUT.relative_to(REPO)}/index.html; fill {SHEET.name}")


def unblind() -> None:
    """Copy the filled sheet into `bench/labels.csv` via the key."""
    with KEY.open() as f:
        key = {r["id"]: r for r in csv.DictReader(f)}
    with SHEET.open() as f:
        answers = list(csv.DictReader(f))
    missing = [a["id"] for a in answers if a["accept"].strip().lower() not in ("yes", "no")]
    if missing:
        raise SystemExit(f"blind.py: accept must be yes/no; unfilled: {', '.join(missing)}")
    by_run = {
        (key[a["id"]]["brief"], key[a["id"]]["tool"], key[a["id"]]["run"]): a for a in answers
    }
    with LABELS.open() as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        a = by_run[(row["brief"], row["tool"], row["run"])]
        row["accept"] = a["accept"].strip().lower()
        row["note"] = a["reject_reason"].strip()
    with LABELS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["brief", "tool", "run", "accept", "note"])
        w.writeheader()
        w.writerows(rows)
    print(f"blind.py: wrote {len(rows)} labels to {LABELS.relative_to(REPO)}")


def main() -> None:
    """Parse the subcommand and run it."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    mk = sub.add_parser("make")
    mk.add_argument("--seed", type=int, default=20261113)
    sub.add_parser("unblind")
    args = parser.parse_args()
    make(args.seed) if args.cmd == "make" else unblind()


if __name__ == "__main__":
    main()
