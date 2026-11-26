"""Decide the IFC-level bounds of the plumbing and wiring briefs (plan §5 BENCH-MEP).

Usage: python3 -I bench/ifc_checks.py BRIEF.md FACTS.json

Pure Python, standard library only, so CI tests every rule with hand-written facts. It never
opens an IFC file: `bench/ifc_facts.py` (IfcOpenShell) measures the model and writes the facts;
this module only decides. It prints one result per check as JSON and exits 0 when no
check failed, which is necessary, not sufficient: the render and the human decide. Exit 1
when a check failed, including when the facts are missing or unreadable. Exit 2 when the
brief declares a bound this module cannot read, so nothing was checked.

**Bounds** are flat `key: value` lines in the brief's front matter (`bench/run.sh` hides
them from the agent). `;` separates entries, `,` separates numbers, `lo..hi` is a count range.
An absent bound reports `skip`; an unknown key or a malformed value is an error, never a
`skip`. `envelope`, `volume_band` and `volume` belong to `caxgauge check` and are ignored here.

- `elements: IfcPipeSegment=2; IfcPipeFitting=1..3`: element count per IFC class.
- `systems: IfcPipeSegment=DOMESTICCOLDWATER`: every element of the class belongs to a
  distribution system of that predefined type; a class with no elements fails.
- `ports: 6`, `open_ports: 2`, `networks: 1`: total ports, ports in no connection, and
  connected groups among the elements that own ports.
- `joints: 1`: every connection's two ports lie within this many mm of each other.
- `ends: x,y,z; x,y,z` with `ends_tol: 5`: the open ports sit at these points, one each,
  within the tolerance in mm.
- `fall: IfcPipeSegment=0.015,0.025`: each element of the class has a slope between its two
  ports (height difference over horizontal run) within the window. The magnitude only: the
  direction of fall is left to the `ends` bound.
- `height: IfcOutlet=290,310`: the Z of each element's geometric centre, in mm.
- `path_length: 3000,6000`: the run's length in mm, summed port to port over every element
  of a class that owns ports anywhere in the model (each must own exactly two), plus the gaps
  at its connections.
- `no_clash: yes`: no distribution element intersects, touches or lies inside a wall, and at
  least one pair was tested.

Every window is two-sided and inclusive. An empty model, or facts that are missing or broken,
fail every declared bound. Broken includes ids that are empty or repeated, a port naming an
unknown element, and a connection that joins a port to itself or to its own element, or reuses
a port.

**Facts** (JSON, millimetres, written by `bench/ifc_facts.py`):

    {"elements": [{"id": str, "ifc_class": str, "systems": [str],
                   "centre": [x, y, z] | null}],
     "ports": [{"id": str, "element": str, "position": [x, y, z] | null}],
     "connections": [[port_id, port_id]],
     "clash_pairs_tested": int,
     "clashes": [[element_id, element_id]]}

`systems` holds the predefined types of the systems the element belongs to. A coordinate that
is missing, not a finite number or not three long counts as unmeasured: the checks that need
it fail, the others still run.

Blind spots: the fall, ends, joints and path length are read from the ports, so a segment
whose body disagrees with its ports is caught only by the clash check, the envelope and the
render. Classes the `elements` bound does not name are not counted.
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import cast

PASS = "pass"  # noqa: S105 — a check outcome, not a credential
FAIL = "fail"
SKIP = "skip"

PREFLIGHT_KEYS = frozenset({"envelope", "volume_band", "volume"})

type Point = tuple[float, float, float]
type Window = tuple[float, float]


class BoundError(ValueError):
    """The brief declares a bound this module cannot read."""


@dataclass(frozen=True)
class Result:
    """One check's outcome; `detail` says what was measured, or why nothing was."""

    name: str
    status: str
    detail: str


@dataclass(frozen=True)
class Ends:
    """Where the open ports must sit, and how close in mm."""

    points: tuple[Point, ...]
    tol: float


@dataclass(frozen=True)
class Element:
    """One IFC element as measured."""

    id: str
    ifc_class: str
    systems: frozenset[str]
    centre: Point | None


@dataclass(frozen=True)
class Port:
    """One distribution port as measured."""

    id: str
    element: str
    position: Point | None


@dataclass(frozen=True)
class Facts:
    """A whole model as measured, after validation."""

    elements: tuple[Element, ...]
    ports: tuple[Port, ...]
    connections: tuple[tuple[str, str], ...]
    clash_pairs_tested: int
    clashes: tuple[tuple[str, str], ...]


# --- reading bounds -------------------------------------------------------------------


def read_front_matter(brief: Path) -> dict[str, str]:
    """Return the brief's front-matter fields, parsed like `bench/run.sh` does."""
    parts = brief.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        msg = f"{brief}: no front matter"
        raise BoundError(msg)
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if not line.strip():
            continue
        if not sep or key.strip() in fields:  # run.sh's field() would read these differently
            msg = f"{brief}: a front-matter line is key: value, each key once: {line!r}"
            raise BoundError(msg)
        fields[key.strip()] = value.strip()
    return fields


def _number(text: str) -> float:
    try:
        value = float(text)
    except ValueError:
        msg = f"not a number: {text!r}"
        raise BoundError(msg) from None
    if not math.isfinite(value):
        msg = f"not a finite number: {text!r}"
        raise BoundError(msg)
    return value


def _window(text: str) -> Window:
    parts = text.split(",")
    if len(parts) != 2:
        msg = f"a window is low,high: {text!r}"
        raise BoundError(msg)
    low, high = _number(parts[0]), _number(parts[1])
    if not 0 <= low < high:
        msg = f"a window needs 0 <= low < high: {text!r}"
        raise BoundError(msg)
    return low, high


def _count(text: str) -> tuple[int, int]:
    low, dots, high = text.partition("..")
    if not re.fullmatch(r"\d+", low) or (dots and not re.fullmatch(r"\d+", high)):
        msg = f"a count is n or lo..hi, non-negative: {text!r}"
        raise BoundError(msg)
    lo, hi = int(low), int(high or low)
    if lo > hi:
        msg = f"a count range needs lo <= hi: {text!r}"
        raise BoundError(msg)
    return lo, hi


def _tolerance(text: str) -> float:
    value = _number(text)
    if value <= 0:
        msg = f"a tolerance is positive: {text!r}"
        raise BoundError(msg)
    return value


def _system(text: str) -> str:
    if not re.fullmatch(r"[A-Z]+", text):
        msg = f"a system type is an IFC enum name: {text!r}"
        raise BoundError(msg)
    return text


def _per_class[T](parse: Callable[[str], T]) -> Callable[[str], dict[str, T]]:
    def parse_map(text: str) -> dict[str, T]:
        out: dict[str, T] = {}
        for entry in text.split(";"):
            cls, sep, value = entry.strip().partition("=")
            if not sep or not re.fullmatch(r"Ifc[A-Za-z]+", cls) or cls in out:
                msg = f"an entry is IfcClass=value, each class once: {entry!r}"
                raise BoundError(msg)
            out[cls] = parse(value.strip())
        return out

    return parse_map


def _point(text: str) -> Point:
    parts = text.split(",")
    if len(parts) != 3:
        msg = f"a point is x,y,z: {text!r}"
        raise BoundError(msg)
    return (_number(parts[0]), _number(parts[1]), _number(parts[2]))


def _yes(text: str) -> bool:
    if text != "yes":
        msg = f"no_clash takes only 'yes': {text!r}"
        raise BoundError(msg)
    return True


_PARSERS: dict[str, Callable[[str], object]] = {
    "elements": _per_class(_count),
    "systems": _per_class(_system),
    "ports": _count,
    "open_ports": _count,
    "networks": _count,
    "joints": _tolerance,
    "fall": _per_class(_window),
    "height": _per_class(_window),
    "path_length": _window,
    "no_clash": _yes,
}


def parse_bounds(fields: Mapping[str, str]) -> dict[str, object]:
    """Parse a brief's IFC-level bounds; raise `BoundError` on anything unreadable."""
    unknown = set(fields) - set(_PARSERS) - PREFLIGHT_KEYS - {"ends", "ends_tol"}
    if unknown:
        msg = f"unknown bound(s): {sorted(unknown)}"
        raise BoundError(msg)
    bounds = {key: parse(fields[key]) for key, parse in _PARSERS.items() if key in fields}
    if ("ends" in fields) != ("ends_tol" in fields):
        msg = "ends and ends_tol go together"
        raise BoundError(msg)
    if "ends" in fields:
        points = tuple(_point(p.strip()) for p in fields["ends"].split(";"))
        bounds["ends"] = Ends(points, _tolerance(fields["ends_tol"]))
    return bounds


# --- reading facts --------------------------------------------------------------------


def _coords(value: object) -> Point | None:
    if not isinstance(value, list | tuple):
        return None
    items = list(cast("list[object] | tuple[object, ...]", value))
    nums = [v for v in items if isinstance(v, int | float) and not isinstance(v, bool)]
    if len(items) != 3 or len(nums) != 3 or not all(math.isfinite(n) for n in nums):
        return None
    return (float(nums[0]), float(nums[1]), float(nums[2]))


def _records(raw: Mapping[str, object], key: str) -> list[Mapping[str, object]]:
    value = raw.get(key)
    if not isinstance(value, list):
        msg = f"facts: {key} is not a list"
        raise TypeError(msg)
    items = cast("list[object]", value)
    if not all(isinstance(i, dict) for i in items):
        msg = f"facts: every {key} entry is an object"
        raise TypeError(msg)
    return cast("list[Mapping[str, object]]", items)


def _ids(values: list[str], what: str) -> set[str]:
    if not all(values) or len(set(values)) != len(values):
        msg = f"facts: {what} ids must be non-empty and unique"
        raise TypeError(msg)
    return set(values)


def _text(r: Mapping[str, object], key: str) -> str:
    value = r.get(key)
    return value if isinstance(value, str) else ""


def _pairs(raw: Mapping[str, object], key: str, known: set[str]) -> tuple[tuple[str, str], ...]:
    value = raw.get(key)
    items = cast("list[object]", value) if isinstance(value, list) else None
    if items is None:
        msg = f"facts: {key} is not a list"
        raise TypeError(msg)
    out: list[tuple[str, str]] = []
    for item in items:
        pair = cast("list[object]", item) if isinstance(item, list) else []
        if len(pair) != 2 or not all(isinstance(p, str) and p in known for p in pair):
            msg = f"facts: {key} entry {item!r} names an unknown id"
            raise TypeError(msg)
        out.append((str(pair[0]), str(pair[1])))
    return tuple(out)


def _element(r: Mapping[str, object]) -> Element:
    systems = r.get("systems")
    names = cast("list[object]", systems) if isinstance(systems, list) else []
    return Element(
        id=_text(r, "id"),
        ifc_class=_text(r, "ifc_class"),
        systems=frozenset(s for s in names if isinstance(s, str)),
        centre=_coords(r.get("centre")),
    )


def load_facts(raw: object) -> Facts:
    """Validate raw facts; raise `TypeError` when they can't be trusted at all."""
    if not isinstance(raw, dict):
        msg = "facts: not an object"
        raise TypeError(msg)
    data = cast("dict[str, object]", raw)
    elements = tuple(_element(r) for r in _records(data, "elements"))
    if not elements:
        msg = "facts: the model has no elements"
        raise TypeError(msg)
    element_ids = _ids([e.id for e in elements], "element")
    ports = tuple(
        Port(_text(r, "id"), _text(r, "element"), _coords(r.get("position")))
        for r in _records(data, "ports")
    )
    _ids([p.id for p in ports], "port")
    if any(p.element not in element_ids for p in ports):
        msg = "facts: a port names an unknown element"
        raise TypeError(msg)
    tested = data.get("clash_pairs_tested")
    if not isinstance(tested, int) or isinstance(tested, bool) or tested < 0:
        msg = "facts: clash_pairs_tested is not a count"
        raise TypeError(msg)
    connections = _pairs(data, "connections", {p.id for p in ports})
    _joints_are_sound(connections, {p.id: p.element for p in ports})
    return Facts(
        elements=elements,
        ports=ports,
        connections=connections,
        clash_pairs_tested=tested,
        clashes=_pairs(data, "clashes", element_ids),
    )


def _joints_are_sound(connections: tuple[tuple[str, str], ...], owner: dict[str, str]) -> None:
    """Each connection joins two different elements, and each port joins at most once."""
    used = [pid for pair in connections for pid in pair]
    if len(set(used)) != len(used) or any(owner[a] == owner[b] for a, b in connections):
        msg = "facts: a port is connected twice, to itself, or within its own element"
        raise TypeError(msg)


# --- checks ---------------------------------------------------------------------------


def _within(value: float, window: Window | tuple[int, int]) -> bool:
    return window[0] <= value <= window[1]  # positive containment, so NaN never passes


def _of(facts: Facts, cls: str) -> list[Element]:
    return [e for e in facts.elements if e.ifc_class == cls]


def _ports_of(facts: Facts, element: str) -> list[Port]:
    return [p for p in facts.ports if p.element == element]


def _connected(facts: Facts) -> set[str]:
    return {pid for pair in facts.connections for pid in pair}


def _check_elements(facts: Facts, bound: dict[str, tuple[int, int]]) -> tuple[bool, str]:
    counts = {cls: len(_of(facts, cls)) for cls in bound}
    ok = all(_within(n, bound[cls]) for cls, n in counts.items())
    return ok, f"counted {counts}"


def _check_systems(facts: Facts, bound: dict[str, str]) -> tuple[bool, str]:
    wrong: list[str] = []
    for cls, system in bound.items():
        members = _of(facts, cls)
        if not members:
            wrong.append(f"no {cls}")
        wrong += [f"{e.id} ({cls}) not in {system}" for e in members if system not in e.systems]
    return not wrong, "; ".join(wrong) or "every element is in its system"


def _check_ports(facts: Facts, bound: tuple[int, int]) -> tuple[bool, str]:
    return _within(len(facts.ports), bound), f"{len(facts.ports)} ports"


def _check_open_ports(facts: Facts, bound: tuple[int, int]) -> tuple[bool, str]:
    n = len([p for p in facts.ports if p.id not in _connected(facts)])
    return _within(n, bound), f"{n} open ports"


def _check_networks(facts: Facts, bound: tuple[int, int]) -> tuple[bool, str]:
    if not facts.ports:
        return False, "no ports, so no network to count"
    owner = {p.id: p.element for p in facts.ports}
    group = {e: e for e in owner.values()}

    def root(e: str) -> str:
        while group[e] != e:
            e = group[e]
        return e

    for a, b in facts.connections:
        group[root(owner[a])] = root(owner[b])
    n = len({root(e) for e in group})
    return _within(n, bound), f"{n} connected network(s)"


def _check_joints(facts: Facts, bound: float) -> tuple[bool, str]:
    if not facts.connections:
        return False, "no connections to measure"
    where = {p.id: p.position for p in facts.ports}
    gaps = [_gap(where[a], where[b]) for a, b in facts.connections]
    worst = max(gaps)
    return _within(worst, (0.0, bound)), f"widest joint {worst:g} mm"


def _gap(a: Point | None, b: Point | None) -> float:
    return math.dist(a, b) if a is not None and b is not None else math.inf


def _check_ends(facts: Facts, bound: Ends) -> tuple[bool, str]:
    open_ports = [p.position for p in facts.ports if p.id not in _connected(facts)]
    if len(open_ports) != len(bound.points) or None in open_ports:
        return False, f"{len(open_ports)} open port(s), some unplaced or not {len(bound.points)}"
    left = [p for p in open_ports if p is not None]
    for end in bound.points:
        hit = next((p for p in left if math.dist(p, end) <= bound.tol), None)
        if hit is None:
            return False, f"no open port within {bound.tol:g} mm of {end}"
        left.remove(hit)
    return True, "every open port is at a declared end"


def _two_ends(facts: Facts, element: str) -> tuple[Point, Point] | None:
    placed = [p.position for p in _ports_of(facts, element)]
    if len(placed) != 2 or placed[0] is None or placed[1] is None:
        return None
    return placed[0], placed[1]


def _check_fall(facts: Facts, bound: dict[str, Window]) -> tuple[bool, str]:
    falls: list[str] = []
    ok = True
    for cls, window in bound.items():
        members = _of(facts, cls)
        ok = ok and bool(members)
        for e in members:
            ends = _two_ends(facts, e.id)
            run = math.dist(ends[0][:2], ends[1][:2]) if ends else 0.0
            fall = abs(ends[0][2] - ends[1][2]) / run if ends and run > 0 else math.nan
            ok = ok and _within(fall, window)
            falls.append(f"{e.id} {fall:.4f}")
    return ok, "fall " + (", ".join(falls) or "of no element")


def _check_height(facts: Facts, bound: dict[str, Window]) -> tuple[bool, str]:
    heights: list[str] = []
    ok = True
    for cls, window in bound.items():
        members = _of(facts, cls)
        ok = ok and bool(members)
        for e in members:
            z = e.centre[2] if e.centre is not None else math.nan
            ok = ok and _within(z, window)
            heights.append(f"{e.id} {z:g}")
    return ok, "centre height " + (", ".join(heights) or "of no element") + " mm"


def _check_path_length(facts: Facts, bound: Window) -> tuple[bool, str]:
    ported = {e.ifc_class for e in facts.elements if _ports_of(facts, e.id)}
    on_run = sorted(e.id for e in facts.elements if e.ifc_class in ported)
    spans = [_two_ends(facts, e) for e in on_run]
    if not spans or None in spans:
        return False, "every element on the run needs exactly two placed ports"
    where = {p.id: p.position for p in facts.ports}
    length = sum(math.dist(a, b) for a, b in (s for s in spans if s is not None))
    length += sum(_gap(where[a], where[b]) for a, b in facts.connections)
    return _within(length, bound), f"path length {length:.1f} mm"


def _check_no_clash(facts: Facts, _bound: bool) -> tuple[bool, str]:
    if facts.clash_pairs_tested == 0:
        return False, "no element pair was tested for a clash"
    detail = f"{len(facts.clashes)} clash(es) in {facts.clash_pairs_tested} pair(s) tested"
    return not facts.clashes, detail


type Check = Callable[[Facts, object], tuple[bool, str]]

CHECKS: dict[str, Check] = {
    "elements": cast("Check", _check_elements),
    "systems": cast("Check", _check_systems),
    "ports": cast("Check", _check_ports),
    "open_ports": cast("Check", _check_open_ports),
    "networks": cast("Check", _check_networks),
    "joints": cast("Check", _check_joints),
    "ends": cast("Check", _check_ends),
    "fall": cast("Check", _check_fall),
    "height": cast("Check", _check_height),
    "path_length": cast("Check", _check_path_length),
    "no_clash": cast("Check", _check_no_clash),
}


def classify(bounds: Mapping[str, object], raw_facts: object) -> list[Result]:
    """Decide every check: `skip` when undeclared, `fail` on every declared one without facts."""
    try:
        facts = load_facts(raw_facts)
    except TypeError as broken:
        facts, reason = None, str(broken)
    else:
        reason = ""
    results: list[Result] = []
    for name, check in CHECKS.items():
        if name not in bounds:
            results.append(Result(name, SKIP, "no bound declared"))
        elif facts is None:
            results.append(Result(name, FAIL, reason))
        else:
            ok, detail = check(facts, bounds[name])
            results.append(Result(name, PASS if ok else FAIL, detail))
    return results


def main(argv: list[str]) -> int:
    """Print the results for one brief and one facts file; return the exit code."""
    if len(argv) != 2:
        print("usage: ifc_checks.py BRIEF.md FACTS.json", file=sys.stderr)
        return 2
    try:
        bounds = parse_bounds(read_front_matter(Path(argv[0])))
    except (BoundError, OSError) as bad:
        print(f"ifc_checks: {bad}", file=sys.stderr)
        return 2
    try:
        raw: object = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as missing:
        print(
            f"ifc_checks: facts unreadable, every declared bound fails: {missing}", file=sys.stderr
        )
        raw = None
    results = classify(bounds, raw)
    print(json.dumps([asdict(r) for r in results], indent=2))
    return 1 if any(r.status == FAIL for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
