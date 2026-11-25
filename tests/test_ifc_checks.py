"""The IFC-level classifier for the plumbing and wiring briefs (plan §5 BENCH-MEP, PR A).

`bench/ifc_checks.py` decides from facts that PR B's extractor will measure. These tests
hand-write those facts: one reference model per brief that meets every declared bound, a
known-bad model per bound, and broken or empty facts. Hand-written facts are not measured
from any IFC, so they test the decision rules only, never the extractor.
"""

import copy
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from ifc_checks import (
    CHECKS,
    FAIL,
    PASS,
    SKIP,
    BoundError,
    classify,
    parse_bounds,
    read_front_matter,
)

BENCH = Path(__file__).resolve().parent.parent / "bench"
BRIEFS = BENCH / "briefs"
MEP = sorted(BRIEFS.glob("bim-0[5-9]-*.md"))

# Read from the IFC4 schema in IfcOpenShell 0.9.0.post1 on 2026-11-25
# (IfcDistributionSystemEnum). CI has no IfcOpenShell; PR B's marked test reads it live.
VERIFIED_SYSTEMS = {"DOMESTICCOLDWATER", "DRAINAGE", "ELECTRICAL"}


def _el(
    eid: str, cls: str, systems: list[str] | None = None, centre: list[float] | None = None
) -> dict:
    return {"id": eid, "ifc_class": cls, "systems": systems or [], "centre": centre}


def _chain(pts: list[tuple[float, float, float]], classes: list[str], system: str) -> dict:
    """Elements in a row, each with a port at both ends, connected end to end."""
    elements, ports, connections = [], [], []
    for i, cls in enumerate(classes):
        elements.append(_el(f"e{i}", cls, [system]))
        ports.append({"id": f"e{i}a", "element": f"e{i}", "position": list(pts[2 * i])})
        ports.append({"id": f"e{i}b", "element": f"e{i}", "position": list(pts[2 * i + 1])})
        if i:
            connections.append([f"e{i - 1}b", f"e{i}a"])
    return {
        "elements": elements,
        "ports": ports,
        "connections": connections,
        "clash_pairs_tested": 0,
        "clashes": [],
    }


def _bim05() -> dict:
    pts = [(0, 0, 1000), (1950, 0, 1000), (1950, 0, 1000), (2000, 50, 1000)]
    pts += [(2000, 50, 1000), (2000, 1500, 1000)]
    classes = ["IfcPipeSegment", "IfcPipeFitting", "IfcPipeSegment"]
    return _chain(pts, classes, "DOMESTICCOLDWATER")


def _bim06() -> dict:
    return _chain([(0, 0, 500), (3000, 0, 440)], ["IfcPipeSegment"], "DRAINAGE")


def _bim07() -> dict:
    sys_ = ["ELECTRICAL"]
    elements = [
        _el("jb", "IfcJunctionBox", sys_, [1000, 0, 300]),
        _el("c1", "IfcCableCarrierSegment", sys_),
        _el("c2", "IfcCableCarrierSegment", sys_),
        _el("o1", "IfcOutlet", sys_, [500, 0, 300]),
        _el("o2", "IfcOutlet", sys_, [1500, 0, 300]),
    ]
    at = {
        "jb1": ("jb", (950, 0, 300)),
        "jb2": ("jb", (1050, 0, 300)),
        "c1a": ("c1", (950, 0, 300)),
        "c1b": ("c1", (550, 0, 300)),
        "c2a": ("c2", (1050, 0, 300)),
        "c2b": ("c2", (1450, 0, 300)),
        "o1": ("o1", (550, 0, 300)),
        "o2": ("o2", (1450, 0, 300)),
    }
    ports = [{"id": k, "element": e, "position": list(p)} for k, (e, p) in at.items()]
    connections = [["jb1", "c1a"], ["c1b", "o1"], ["jb2", "c2a"], ["c2b", "o2"]]
    return {
        "elements": elements,
        "ports": ports,
        "connections": connections,
        "clash_pairs_tested": 0,
        "clashes": [],
    }


def _bim08() -> dict:
    pipe = _chain([(1000, -500, 1000), (1000, 700, 1000)], ["IfcPipeSegment"], "DOMESTICCOLDWATER")
    cond = _chain([(3000, -500, 500), (3000, 700, 500)], ["IfcCableCarrierSegment"], "ELECTRICAL")
    for p in cond["ports"]:  # distinct ids for the second run
        p["id"] = "k" + p["id"]
        p["element"] = "k" + p["element"]
    cond["elements"][0]["id"] = "ke0"
    walls = [_el("w", "IfcWall"), _el("op1", "IfcOpeningElement"), _el("op2", "IfcOpeningElement")]
    return {
        "elements": walls + pipe["elements"] + cond["elements"],
        "ports": pipe["ports"] + cond["ports"],
        "connections": [],
        "clash_pairs_tested": 2,
        "clashes": [],
    }


def _bim09() -> dict:
    corners = [(950, 0), (1000, 50), (1000, 1150), (1050, 1200), (1950, 1200), (2000, 1150)]
    corners += [(2000, 50), (2050, 0)]
    xy = [(0, 0), *[c for c in corners for _ in (0, 1)], (3000, 0)]
    pts = [(x, y, 1000) for x, y in xy]
    classes = ["IfcPipeSegment", "IfcPipeFitting"] * 4 + ["IfcPipeSegment"]
    facts = _chain(pts, classes, "DOMESTICCOLDWATER")
    facts["elements"].insert(0, _el("w", "IfcWall"))
    facts["clash_pairs_tested"] = 9
    return facts


REFERENCE = {
    "bim-05-water-pipe": _bim05,
    "bim-06-drain": _bim06,
    "bim-07-outlets": _bim07,
    "bim-08-wall-penetrations": _bim08,
    "bim-09-route-around-wall": _bim09,
}


def _bounds(stem: str) -> dict[str, Any]:
    return parse_bounds(read_front_matter(BRIEFS / f"{stem}.md"))


def _statuses(stem: str, facts: object) -> dict[str, str]:
    return {r.name: r.status for r in classify(_bounds(stem), facts)}


def _port(facts: dict, pid: str) -> dict:
    return next(p for p in facts["ports"] if p["id"] == pid)


# --- the briefs ---------------------------------------------------------------------


def test_there_are_five_mep_briefs_each_with_a_reference_model():
    assert [p.stem for p in MEP] == sorted(REFERENCE)


@pytest.mark.parametrize("path", MEP, ids=lambda p: p.stem)
def test_every_brief_bound_parses_and_has_no_volume_band(path: Path):
    fields = read_front_matter(path)
    assert "volume_band" not in fields  # thin pipes: volume reports SKIP, no tuned band
    assert "envelope" in fields
    assert parse_bounds(fields)  # raises on an unknown or malformed bound
    assert "\nBounds:" in path.read_text()  # the prompt stops there (bench/run.sh)


def test_every_check_is_declared_by_some_brief():
    used = {key for p in MEP for key in parse_bounds(read_front_matter(p))}
    assert used == set(CHECKS)


@pytest.mark.parametrize("path", MEP, ids=lambda p: p.stem)
def test_declared_systems_are_ifc4_names(path: Path):
    systems = parse_bounds(read_front_matter(path)).get("systems", {})
    assert set(systems.values()) <= VERIFIED_SYSTEMS


@pytest.mark.parametrize("path", MEP, ids=lambda p: p.stem)
def test_declared_ends_are_stated_in_the_prompt(path: Path):
    body = path.read_text().split("---", 2)[2].split("\nBounds:")[0]
    ends = parse_bounds(read_front_matter(path)).get("ends")
    for x, y, z in ends.points if ends else ():
        assert f"({x:g}, {y:g}, {z:g})" in body


@pytest.mark.parametrize("path", MEP, ids=lambda p: p.stem)
def test_a_clash_bound_is_paired_with_declared_ends(path: Path):
    bounds = parse_bounds(read_front_matter(path))
    if "no_clash" in bounds:  # moving the pipe away avoids a clash; the ends catch that
        assert len(bounds["ends"].points) >= 2


def test_the_path_length_window_starts_at_the_straight_line():
    bounds = _bounds("bim-09-route-around-wall")
    a, b = bounds["ends"].points
    assert bounds["path_length"][0] == pytest.approx(math.dist(a, b))


def test_the_fall_window_contains_the_stated_fall():
    bounds = _bounds("bim-06-drain")
    a, b = bounds["ends"].points
    stated = abs(a[2] - b[2]) / math.dist(a[:2], b[:2])
    low, high = bounds["fall"]["IfcPipeSegment"]
    assert low < stated < high
    assert stated == pytest.approx(0.02)


def test_the_height_window_contains_the_stated_height():
    text = (BRIEFS / "bim-07-outlets.md").read_text()
    stated = float(re.search(r"(\d+) mm above the floor", text).group(1))
    low, high = _bounds("bim-07-outlets")["height"]["IfcOutlet"]
    assert low < stated < high


# --- reference models pass; absent bounds skip ---------------------------------------


@pytest.mark.parametrize("stem", sorted(REFERENCE))
def test_the_reference_model_passes_every_declared_bound(stem: str):
    bounds = _bounds(stem)
    statuses = _statuses(stem, REFERENCE[stem]())
    assert {k for k, s in statuses.items() if s == PASS} == set(bounds)
    assert {k for k, s in statuses.items() if s == SKIP} == set(CHECKS) - set(bounds)


# --- broken or empty facts fail every declared bound ---------------------------------


@pytest.mark.parametrize("stem", sorted(REFERENCE))
@pytest.mark.parametrize(
    "facts",
    [None, {}, "crashed", {"elements": [], "ports": [], "connections": []}],
    ids=["none", "empty-dict", "not-a-dict", "no-elements"],
)
def test_missing_or_empty_facts_fail_every_declared_bound(stem: str, facts: object):
    statuses = _statuses(stem, facts)
    assert {k for k, s in statuses.items() if s == FAIL} == set(_bounds(stem))


def test_a_port_naming_an_unknown_element_fails_every_declared_bound():
    facts = _bim05()
    facts["ports"][0]["element"] = "ghost"
    assert set(_statuses("bim-05-water-pipe", facts).values()) == {FAIL, SKIP}


@pytest.mark.parametrize("bad", [math.nan, math.inf, None, True, "1", [0, 0]])
def test_a_bad_coordinate_fails_the_checks_that_need_it(bad: object):
    facts = _bim05()
    _port(facts, "e0a")["position"] = [bad, 0, 1000] if bad != [0, 0] else bad
    statuses = _statuses("bim-05-water-pipe", facts)
    assert statuses["ends"] == FAIL
    assert statuses["elements"] == PASS  # counts don't need positions


# --- a known-bad model per bound ------------------------------------------------------


def test_a_missing_element_fails_the_counts():
    facts = _bim05()
    facts["elements"] = [e for e in facts["elements"] if e["id"] != "e1"]
    facts["ports"] = [p for p in facts["ports"] if p["element"] != "e1"]
    facts["connections"] = []
    assert _statuses("bim-05-water-pipe", facts)["elements"] == FAIL


def test_counts_outside_a_range_fail_on_both_sides():
    facts = _bim09()
    facts["elements"] = [e for e in facts["elements"] if e["ifc_class"] != "IfcPipeFitting"]
    assert _statuses("bim-09-route-around-wall", facts)["elements"] == FAIL
    facts = _bim09()
    facts["elements"] += [_el(f"x{i}", "IfcPipeFitting", ["DOMESTICCOLDWATER"]) for i in range(4)]
    assert _statuses("bim-09-route-around-wall", facts)["elements"] == FAIL


@pytest.mark.parametrize("systems", [[], ["DOMESTICHOTWATER"]], ids=["none", "wrong"])
def test_an_element_outside_its_system_fails(systems: list[str]):
    facts = _bim07()
    facts["elements"][3]["systems"] = systems
    assert _statuses("bim-07-outlets", facts)["systems"] == FAIL


def test_a_system_bound_on_a_class_with_no_elements_fails():
    facts = _bim08()
    facts["elements"] = [e for e in facts["elements"] if e["ifc_class"] != "IfcCableCarrierSegment"]
    facts["ports"] = [p for p in facts["ports"] if not p["id"].startswith("k")]
    assert _statuses("bim-08-wall-penetrations", facts)["systems"] == FAIL


def test_a_missing_port_fails_the_port_count():
    facts = _bim05()
    facts["ports"] = [p for p in facts["ports"] if p["id"] != "e0a"]
    assert _statuses("bim-05-water-pipe", facts)["ports"] == FAIL


def test_a_missing_connection_leaves_ports_open_and_splits_the_network():
    facts = _bim07()
    facts["connections"].pop()
    statuses = _statuses("bim-07-outlets", facts)
    assert statuses["open_ports"] == FAIL
    assert statuses["networks"] == FAIL


def test_a_model_without_ports_fails_the_network_bound():
    facts = _bim06()
    facts["ports"] = []
    assert _statuses("bim-06-drain", facts)["networks"] == FAIL


def test_connected_ports_apart_fail_the_joint_bound():
    facts = _bim05()
    _port(facts, "e1a")["position"] = [1940, 0, 1000]
    assert _statuses("bim-05-water-pipe", facts)["joints"] == FAIL


def test_a_joint_bound_with_no_connections_fails():
    facts = _bim05()
    facts["connections"] = []
    assert _statuses("bim-05-water-pipe", facts)["joints"] == FAIL


def test_a_misplaced_end_fails():
    facts = _bim05()
    _port(facts, "e2b")["position"] = [2000, 1490, 1000]
    assert _statuses("bim-05-water-pipe", facts)["ends"] == FAIL


@pytest.mark.parametrize("z_out", [500, 470, 300], ids=["flat", "too-shallow", "too-steep"])
def test_a_fall_outside_its_window_fails(z_out: float):
    facts = _bim06()
    _port(facts, "e0b")["position"] = [3000, 0, z_out]
    assert _statuses("bim-06-drain", facts)["fall"] == FAIL


def test_a_vertical_segment_fails_the_fall_bound():
    facts = _bim06()
    _port(facts, "e0b")["position"] = [0, 0, 440]
    assert _statuses("bim-06-drain", facts)["fall"] == FAIL


@pytest.mark.parametrize("z", [450, 150, None], ids=["high", "low", "unmeasured"])
def test_an_outlet_outside_its_height_window_fails(z: float | None):
    facts = _bim07()
    facts["elements"][4]["centre"] = None if z is None else [1500, 0, z]
    assert _statuses("bim-07-outlets", facts)["height"] == FAIL


def test_a_detour_longer_than_the_window_fails_the_path_length():
    facts = _bim09()
    for p in facts["ports"]:
        if p["position"][1] == 1200:
            p["position"][1] = 4000
    assert _statuses("bim-09-route-around-wall", facts)["path_length"] == FAIL


def test_a_straight_run_through_the_wall_passes_length_but_fails_the_clash():
    facts = _chain([(0, 0, 1000), (3000, 0, 1000)], ["IfcPipeSegment"], "DOMESTICCOLDWATER")
    facts["elements"].insert(0, _el("w", "IfcWall"))
    facts["clash_pairs_tested"] = 1
    facts["clashes"] = [["e0", "w"]]
    statuses = _statuses("bim-09-route-around-wall", facts)
    assert statuses["path_length"] == PASS  # the low edge is the straight line itself
    assert statuses["no_clash"] == FAIL


def test_a_clash_check_that_tested_nothing_fails():
    facts = _bim08()
    facts["clash_pairs_tested"] = 0
    assert _statuses("bim-08-wall-penetrations", facts)["no_clash"] == FAIL


def test_a_pipe_moved_out_of_the_wall_avoids_the_clash_but_misses_its_ends():
    facts = _bim08()
    for p in facts["ports"]:
        p["position"][0] += 5000  # clear of the wall, so nothing clashes
    statuses = _statuses("bim-08-wall-penetrations", facts)
    assert statuses["no_clash"] == PASS
    assert statuses["ends"] == FAIL


# --- malformed bounds are errors, never a SKIP -----------------------------------------


@pytest.mark.parametrize(
    "fields",
    [
        {"open_port": "2"},  # unknown key (typo)
        {"ports": "two"},
        {"ports": "-1"},
        {"elements": "IfcWall=2..1"},
        {"elements": "Wall=1"},
        {"fall": "IfcPipeSegment=0.03,0.01"},
        {"fall": "IfcPipeSegment=nan,0.01"},
        {"path_length": "100"},
        {"ends": "0,0,0"},  # ends without ends_tol
        {"ends_tol": "5"},  # ends_tol without ends
        {"ends": "0,0", "ends_tol": "5"},
        {"no_clash": "no"},
        {"systems": "IfcPipeSegment=cold water"},
        {"joints": "-1"},
    ],
)
def test_a_malformed_bound_is_an_error(fields: dict[str, str]):
    with pytest.raises(BoundError):
        parse_bounds(fields)


def test_preflight_keys_are_left_to_caxgauge():
    assert parse_bounds({"envelope": "1,2,3", "volume_band": "1,2", "volume": "2"}) == {}


# --- the command line that PR B's run.sh wiring calls ----------------------------------


def _cli(brief: Path, facts: Path) -> subprocess.CompletedProcess[str]:
    script = BENCH / "ifc_checks.py"
    return subprocess.run(
        [sys.executable, "-I", str(script), str(brief), str(facts)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_exits_0_on_the_reference_model(tmp_path: Path):
    facts = tmp_path / "facts.json"
    facts.write_text(json.dumps(_bim05()))
    done = _cli(BRIEFS / "bim-05-water-pipe.md", facts)
    assert done.returncode == 0, done.stderr
    results = json.loads(done.stdout)
    assert {r["status"] for r in results} == {PASS, SKIP}


def test_cli_exits_1_when_the_facts_file_is_missing_or_broken(tmp_path: Path):
    assert _cli(BRIEFS / "bim-05-water-pipe.md", tmp_path / "absent.json").returncode == 1
    broken = tmp_path / "facts.json"
    broken.write_text("{not json")
    assert _cli(BRIEFS / "bim-05-water-pipe.md", broken).returncode == 1


def test_cli_exits_2_on_a_malformed_brief(tmp_path: Path):
    brief = tmp_path / "brief.md"
    brief.write_text("---\nopen_port: 2\n---\n\nBounds: none\n")
    facts = tmp_path / "facts.json"
    facts.write_text(json.dumps(_bim05()))
    assert _cli(brief, facts).returncode == 2


def test_a_deep_copy_of_the_reference_is_unchanged_by_classify():
    facts = _bim05()
    before = copy.deepcopy(facts)
    classify(_bounds("bim-05-water-pipe"), facts)
    assert facts == before
