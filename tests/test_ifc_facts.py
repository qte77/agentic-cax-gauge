"""The IFC extractor for the plumbing and wiring briefs (plan §5 BENCH-MEP, PR B).

`bench/ifc_facts.py` measures an IFC model into the facts that `bench/ifc_checks.py` decides.
These tests build reference and known-bad models with the IfcOpenShell API, in millimetres
and in metres, measure them and decide them against each brief's bounds. The models are made
with the same library the extractor reads them with, so they are not independent controls:
a defect shared by the API and the reader would pass here (the ifc-lite cross-check of row
BENCH-BIM still applies).

Marked `ifc` and excluded by default: run with `make test_ifc` (IfcOpenShell is not a
package dependency).
"""

from __future__ import annotations

import json
import subprocess
import sys
from itertools import pairwise
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Sequence

pytestmark = pytest.mark.ifc
pytest.importorskip("ifcopenshell")  # the default run collects this module, then deselects it

import ifcopenshell  # noqa: E402
import ifcopenshell.api.context  # noqa: E402
import ifcopenshell.api.feature  # noqa: E402
import ifcopenshell.api.geometry  # noqa: E402
import ifcopenshell.api.root  # noqa: E402
import ifcopenshell.api.system  # noqa: E402
import ifcopenshell.api.unit  # noqa: E402
import ifcopenshell.guid  # noqa: E402
import ifcopenshell.util.unit  # noqa: E402
import numpy as np  # noqa: E402

import ifc_facts  # noqa: E402
from ifc_checks import FAIL, PASS, SKIP, classify, parse_bounds, read_front_matter  # noqa: E402
from test_ifc_checks import VERIFIED_SYSTEMS  # noqa: E402

BENCH = Path(__file__).resolve().parent.parent / "bench"
BRIEFS = BENCH / "briefs"
MEP = sorted(BRIEFS.glob("bim-0[5-9]-*.md"))
UNITS = {"millimetres": "MILLI", "metres": None}
MM = 0.001  # the API's placement and length arguments are in metres

type Point = tuple[float, float, float]
type Entity = Any  # ifcopenshell.entity_instance; its attributes are dynamic


class Model:
    """An IFC4 model built with the IfcOpenShell API; every coordinate given in mm."""

    def __init__(self, prefix: str | None) -> None:
        self.file = ifcopenshell.file(schema="IFC4")
        ifcopenshell.api.root.create_entity(self.file, ifc_class="IfcProject")
        length = ifcopenshell.api.unit.add_si_unit(self.file, unit_type="LENGTHUNIT", prefix=prefix)
        ifcopenshell.api.unit.assign_unit(self.file, units=[length])
        model = ifcopenshell.api.context.add_context(self.file, context_type="Model")
        self.body = ifcopenshell.api.context.add_context(
            self.file,
            context_type="Model",
            context_identifier="Body",
            target_view="MODEL_VIEW",
            parent=model,
        )
        self.scale = ifcopenshell.util.unit.calculate_unit_scale(self.file)

    def _place(self, product: Entity, origin: Point, z_axis: Sequence[float] = (0, 0, 1)) -> None:
        z = np.array(z_axis, dtype=float)  # a copy: the caller's direction stays intact
        z /= np.linalg.norm(z)
        x = np.array([1.0, 0, 0]) if abs(z[0]) < 0.9 else np.array([0, 1.0, 0])
        x -= z * (x @ z)
        x /= np.linalg.norm(x)
        matrix = np.eye(4)
        matrix[:3, 0], matrix[:3, 1], matrix[:3, 2] = x, np.cross(z, x), z
        matrix[:3, 3] = np.asarray(origin) * MM
        ifcopenshell.api.geometry.edit_object_placement(self.file, product=product, matrix=matrix)

    def _element(self, cls: str, predefined: str | None) -> Entity:
        return ifcopenshell.api.root.create_entity(
            self.file, ifc_class=cls, predefined_type=predefined
        )

    def port(self, element: Entity, at: Point) -> Entity:
        port = ifcopenshell.api.system.add_port(self.file, element=element)
        self._place(port, at)
        return port

    def segment(
        self, cls: str, a: Point, b: Point, radius: float, predefined: str | None = None
    ) -> tuple[Entity, Entity, Entity]:
        """A straight round segment from `a` to `b` with a port at each end."""
        element = self._element(cls, predefined)
        direction = np.subtract(b, a)
        self._place(element, a, direction)
        profile = self.file.create_entity(
            "IfcCircleProfileDef", ProfileType="AREA", Radius=radius * MM / self.scale
        )
        body = ifcopenshell.api.geometry.add_profile_representation(
            self.file,
            context=self.body,
            profile=profile,
            depth=float(np.linalg.norm(direction)) * MM,
        )
        ifcopenshell.api.geometry.assign_representation(
            self.file, product=element, representation=body
        )
        return element, self.port(element, a), self.port(element, b)

    def box(self, cls: str, lo: Point, hi: Point, predefined: str | None = None) -> Entity:
        """An axis-aligned box from corner `lo` to corner `hi`."""
        element = self._element(cls, predefined)
        self._place(element, lo)
        x, y, z = (float(v) * MM for v in np.subtract(hi, lo))
        body = ifcopenshell.api.geometry.add_wall_representation(
            self.file, context=self.body, length=x, thickness=y, height=z
        )
        ifcopenshell.api.geometry.assign_representation(
            self.file, product=element, representation=body
        )
        return element

    def wall(self, lo: Point, hi: Point, openings: Sequence[tuple[Point, Point]] = ()) -> Entity:
        wall = self.box("IfcWall", lo, hi)
        for o_lo, o_hi in openings:
            opening = self.box("IfcOpeningElement", o_lo, o_hi)
            ifcopenshell.api.feature.add_feature(self.file, feature=opening, element=wall)
        return wall

    def connect(self, a: Entity, b: Entity) -> None:
        ifcopenshell.api.system.connect_port(self.file, port1=a, port2=b)

    def system(self, elements: list[Entity], predefined: str) -> None:
        system = ifcopenshell.api.system.add_system(self.file, ifc_class="IfcDistributionSystem")
        system.PredefinedType = predefined
        ifcopenshell.api.system.assign_system(self.file, products=elements, system=system)

    def run(self, points: list[Point], classes: list[str], radius: float, system: str) -> list:
        """A connected run: element i spans points i to i+1; a fitting is a box round its ports."""
        made: list[tuple[Entity, Entity, Entity]] = []
        for cls, a, b in zip(classes, points, points[1:], strict=False):
            if cls == "IfcPipeFitting":
                lo = tuple(min(p, q) - radius for p, q in zip(a, b, strict=True))
                hi = tuple(max(p, q) + radius for p, q in zip(a, b, strict=True))
                fitting = self.box(cls, lo, hi, "BEND")
                made.append((fitting, self.port(fitting, a), self.port(fitting, b)))
            else:
                made.append(self.segment(cls, a, b, radius))
        for (_, _, end), (_, start, _) in pairwise(made):
            self.connect(end, start)
        self.system([m[0] for m in made], system)
        return made


SEG, FIT = "IfcPipeSegment", "IfcPipeFitting"
CONDUIT = "IfcCableCarrierSegment"


def bim05(prefix: str | None) -> Model:
    m = Model(prefix)
    corners = [(0, 0, 1000), (1950, 0, 1000), (2000, 50, 1000), (2000, 1500, 1000)]
    m.run(corners, [SEG, FIT, SEG], 16, "DOMESTICCOLDWATER")
    return m


def bim06(prefix: str | None) -> Model:
    m = Model(prefix)
    m.run([(0, 0, 500), (3000, 0, 440)], [SEG], 55, "DRAINAGE")
    return m


def bim07(prefix: str | None) -> Model:
    m = Model(prefix)
    box = m.box("IfcJunctionBox", (950, -25, 250), (1050, 25, 350), "POWER")
    made = [box]
    for side, end, lo in ((950, 550, 450), (1050, 1450, 1450)):
        conduit, a, b = m.segment(CONDUIT, (side, 0, 300), (end, 0, 300), 10, "CONDUITSEGMENT")
        outlet = m.box("IfcOutlet", (lo, -25, 250), (lo + 100, 25, 350), "POWEROUTLET")
        m.connect(m.port(box, (side, 0, 300)), a)
        m.connect(b, m.port(outlet, (end, 0, 300)))
        made += [conduit, outlet]
    m.system(made, "ELECTRICAL")
    return m


def bim08(
    prefix: str | None = "MILLI", *, pipe_x: float = 1000, openings: bool = True
) -> tuple[Model, Entity]:
    m = Model(prefix)
    voids = [((950, -100, 950), (1050, 300, 1050)), ((2975, -100, 475), (3025, 300, 525))]
    m.wall((0, 0, 0), (4000, 200, 3000), voids if openings else ())
    pipe, *_ = m.run([(pipe_x, -500, 1000), (pipe_x, 700, 1000)], [SEG], 16, "DOMESTICCOLDWATER")
    m.run([(3000, -500, 500), (3000, 700, 500)], [CONDUIT], 10, "ELECTRICAL")
    return m, pipe[0]


def bim09(prefix: str | None) -> Model:
    m = Model(prefix)
    m.wall((1400, -1000, 0), (1600, 1000, 3000))
    xy = [(0, 0), (1150, 0), (1200, 50), (1200, 1150), (1250, 1200), (1750, 1200)]
    xy += [(1800, 1150), (1800, 50), (1850, 0), (3000, 0)]
    m.run([(x, y, 1000) for x, y in xy], [SEG, FIT] * 4 + [SEG], 16, "DOMESTICCOLDWATER")
    return m


REFERENCE = {
    "bim-05": bim05,
    "bim-06": bim06,
    "bim-07": bim07,
    "bim-08": lambda prefix: bim08(prefix)[0],
    "bim-09": bim09,
}


def _brief(stem: str) -> dict[str, object]:
    (path,) = (p for p in MEP if p.stem.startswith(stem))
    return parse_bounds(read_front_matter(path))


def _measure(model: Model, tmp_path: Path) -> dict:
    """Write the model to disk and measure the file as the bench does."""
    path = tmp_path / "part.ifc"
    model.file.write(str(path))
    return ifc_facts.extract(ifcopenshell.open(str(path)))


def _status(stem: str, facts: dict) -> dict[str, str]:
    return {r.name: r.status for r in classify(_brief(stem), facts)}


# --- reference models -----------------------------------------------------------------


def test_every_mep_brief_has_a_reference_model():
    assert sorted(REFERENCE) == [p.stem[:6] for p in MEP]


@pytest.mark.parametrize("prefix", UNITS.values(), ids=UNITS.keys())
@pytest.mark.parametrize("stem", REFERENCE)
def test_the_measured_reference_model_meets_every_declared_bound(
    stem: str, prefix: str | None, tmp_path: Path
):
    results = classify(_brief(stem), _measure(REFERENCE[stem](prefix), tmp_path))
    declared = set(_brief(stem)) & {r.name for r in results}
    assert {r.name: r.status for r in results if r.name in declared} == dict.fromkeys(
        declared, PASS
    ), [r for r in results if r.status == FAIL]
    assert all(r.status == SKIP for r in results if r.name not in declared)


@pytest.mark.parametrize("stem", REFERENCE)
def test_millimetres_and_metres_give_identical_facts(stem: str, tmp_path: Path):
    mm = _measure(REFERENCE[stem]("MILLI"), tmp_path)
    m = _measure(REFERENCE[stem](None), tmp_path)
    assert mm == m  # the extractor rounds to 1e-6 mm, so float noise in the scale cancels


def test_ports_and_centres_are_in_millimetres(tmp_path: Path):
    facts = _measure(bim06(None), tmp_path)
    assert sorted(p["position"] for p in facts["ports"]) == [[0, 0, 500], [3000, 0, 440]]
    assert facts["elements"][0]["centre"] == pytest.approx([1500, 0, 470], abs=1)


# --- clashes against walls ------------------------------------------------------------


def _clash(model: Model, tmp_path: Path) -> tuple[str, dict]:
    facts = _measure(model, tmp_path)
    return _status("bim-08", facts)["no_clash"], facts


def test_a_pipe_through_a_solid_wall_clashes(tmp_path: Path):
    status, facts = _clash(bim08(openings=False)[0], tmp_path)
    assert status == FAIL
    assert len(facts["clashes"]) == 2  # the pipe and the conduit
    assert facts["clash_pairs_tested"] == 2


def test_a_pipe_through_an_opening_does_not_clash(tmp_path: Path):
    status, facts = _clash(bim08()[0], tmp_path)
    assert status == PASS
    assert facts["clashes"] == []
    assert facts["clash_pairs_tested"] == 2


@pytest.mark.parametrize(
    ("pipe_x", "expected"),
    [
        (965.5, FAIL),  # 0.5 mm into the opening's edge
        (966.0, FAIL),  # touching it: the briefs say the pipe must not touch the wall
        (966.5, PASS),  # 0.5 mm clear of it
    ],
)
def test_touching_the_wall_clashes_and_a_gap_does_not(pipe_x: float, expected: str, tmp_path: Path):
    assert _clash(bim08(pipe_x=pipe_x)[0], tmp_path)[0] == expected


def test_an_element_wholly_inside_a_wall_clashes(tmp_path: Path):
    model, _ = bim08()
    model.run([(2000, 50, 1500), (2000, 150, 1500)], [SEG], 16, "DOMESTICCOLDWATER")
    status, facts = _clash(model, tmp_path)
    assert status == FAIL
    assert len(facts["clashes"]) == 1


def test_a_pipe_without_a_body_leaves_the_clash_untested(tmp_path: Path):
    model, pipe = bim08(openings=False)
    pipe.Representation = None  # the pipe would cross the solid wall, if it had a body
    status, facts = _clash(model, tmp_path)
    assert facts["clash_pairs_tested"] == 0
    assert status == FAIL


def test_a_model_without_a_wall_tests_no_pair(tmp_path: Path):
    facts = _measure(bim05("MILLI"), tmp_path)
    assert facts["clash_pairs_tested"] == 0
    assert facts["clashes"] == []


# --- ports and connections ------------------------------------------------------------


def test_every_connection_is_reported_so_a_reused_port_fails(tmp_path: Path):
    model = bim05("MILLI")
    ports = model.file.by_type("IfcDistributionPort")
    for other in ports[1:3]:  # the first port joins two more, one on its own element
        model.file.create_entity(
            "IfcRelConnectsPorts",
            GlobalId=ifcopenshell.guid.new(),
            RelatingPort=ports[0],
            RelatedPort=other,
        )
    facts = _measure(model, tmp_path)
    assert len(facts["connections"]) == 4
    assert {s for k, s in _status("bim-05", facts).items() if k in _brief("bim-05")} == {FAIL}


def test_an_unplaced_port_has_no_position(tmp_path: Path):
    model = bim06("MILLI")
    model.file.by_type("IfcDistributionPort")[0].ObjectPlacement = None
    facts = _measure(model, tmp_path)
    assert None in [p["position"] for p in facts["ports"]]
    assert _status("bim-06", facts)["ends"] == FAIL


def test_a_port_on_no_element_fails_every_declared_bound(tmp_path: Path):
    model = bim06("MILLI")
    ifcopenshell.api.root.create_entity(model.file, ifc_class="IfcDistributionPort")
    facts = _measure(model, tmp_path)
    assert "" in [p["element"] for p in facts["ports"]]
    assert {s for k, s in _status("bim-06", facts).items() if k in _brief("bim-06")} == {FAIL}


def test_a_system_is_reported_by_its_predefined_type(tmp_path: Path):
    facts = _measure(bim07("MILLI"), tmp_path)
    assert {e["ifc_class"]: e["systems"] for e in facts["elements"]} == {
        "IfcJunctionBox": ["ELECTRICAL"],
        "IfcCableCarrierSegment": ["ELECTRICAL"],
        "IfcOutlet": ["ELECTRICAL"],
    }


# --- the installed IFC4 schema --------------------------------------------------------


def _schema() -> Entity:
    return ifcopenshell.ifcopenshell_wrapper.schema_by_name("IFC4")


def test_the_verified_systems_are_in_the_installed_ifc4_enum():
    enum = _schema().declaration_by_name("IfcDistributionSystemEnum").enumeration_items()
    assert set(enum) >= VERIFIED_SYSTEMS


@pytest.mark.parametrize("path", MEP, ids=lambda p: p.stem)
def test_declared_systems_and_classes_are_ifc4_names(path: Path):
    bounds = parse_bounds(read_front_matter(path))
    enum = set(_schema().declaration_by_name("IfcDistributionSystemEnum").enumeration_items())
    systems = bounds.get("systems", {})
    assert isinstance(systems, dict)
    assert set(systems.values()) <= enum
    elements = bounds.get("elements", {})
    assert isinstance(elements, dict)
    for cls in {*systems, *elements}:
        declaration = _schema().declaration_by_name(cls)
        while declaration.name() != "IfcElement":
            declaration = declaration.supertype()  # raises at the root if not an element


# --- the command line -----------------------------------------------------------------


def _cli(*args: Path) -> subprocess.CompletedProcess[str]:
    script = BENCH / "ifc_facts.py"
    return subprocess.run(
        [sys.executable, "-I", str(script), *map(str, args)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_writes_the_facts_and_exits_0(tmp_path: Path):
    ifc, out = tmp_path / "part.ifc", tmp_path / "facts.json"
    bim06("MILLI").file.write(str(ifc))
    assert _cli(ifc, out).returncode == 0
    assert json.loads(out.read_text()) == ifc_facts.extract(ifcopenshell.open(str(ifc)))


def test_cli_exits_1_and_writes_nothing_on_an_unreadable_ifc(tmp_path: Path):
    ifc, out = tmp_path / "part.ifc", tmp_path / "facts.json"
    ifc.write_text("not an IFC file")
    done = _cli(ifc, out)
    assert done.returncode == 1
    assert not out.exists()


def test_cli_exits_2_on_a_usage_error(tmp_path: Path):
    assert _cli(tmp_path).returncode == 2
