"""Measure an IFC model into the facts `bench/ifc_checks.py` decides (plan §5 BENCH-MEP).

Usage: uv run --no-project --with ifcopenshell==0.9.0.post1 python -I bench/ifc_facts.py IN OUT

Bench tooling, not part of the gauge, and IfcOpenShell is not a package dependency. This module
measures and never decides: it writes the facts JSON whose schema is in `bench/ifc_checks.py`,
in millimetres whatever the file's length unit. Exit 0 when the facts are written; 1 when the
IFC cannot be read, and then nothing is written, so every declared bound fails; 2 on a usage
error.

- `elements`: every `IfcElement`, openings included, with its STEP id (`#12`) as its id, so ids
  are unique even when the model repeats a GlobalId. `systems` holds the `PredefinedType` of
  each distribution system the element is assigned to. `centre` is the middle of the bounding
  box of its tessellated body, in world coordinates; `null` when it has no body or the body
  fails to tessellate.
- `ports`: every `IfcDistributionPort` except those nested in a type object, which describe
  the type's occurrences rather than a port in the model, with the element it is nested in
  (`""` when none, which the classifier rejects) and the origin of its placement (`null` when
  it has none).
- `connections`: one pair per pair of connected ports. IfcOpenShell records a connection in
  both directions, so a pair and its reverse count once; a port connected to two different
  ports appears in two pairs, which the classifier rejects.
- `clashes`: each pair of a distribution element and a wall whose bodies intersect or touch,
  or where a vertex of either body lies inside the other, which catches an element, or one
  item of it, buried in the wall, and an element enclosing a wall. Walls are voided by their
  openings first. `clash_pairs_tested` counts the pairs; it is 0 when the model has no such
  pair, when any of those elements has no body, or when the clash test fails, because a clash
  test that left an element out has not tested the model.

Blind spots: clashes are found on tessellated meshes, so a curved body that only grazes a wall
can read as a gap as wide as the mesher's deflection; only walls are tested, not slabs or other
elements; the inside test casts one ray from each vertex, so it assumes both meshes are
closed.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.placement
import ifcopenshell.util.system
import ifcopenshell.util.unit
import numpy as np

type Entity = Any  # ifcopenshell.entity_instance: attributes come from the schema at runtime
type Mesh = tuple[np.ndarray, np.ndarray]  # vertices in metres (n x 3), triangles (m x 3)

DIGITS = 6  # mm, so a file in metres and one in millimetres give identical facts
RAY = np.array([0.5773, 0.5774, 0.5776])  # skewed off every axis, so it misses grid edges


def _id(entity: Entity) -> str:
    return f"#{entity.id()}"


def _mm(values: np.ndarray, scale: float) -> list[float] | None:
    """Scale a point to millimetres; `None` when any coordinate is not finite."""
    point = [round(float(v) * scale * 1000.0, DIGITS) for v in values]
    return point if len(point) == 3 and all(math.isfinite(v) for v in point) else None


def _settings() -> ifcopenshell.geom.settings:
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)
    return settings


def _meshes(model: ifcopenshell.file) -> dict[int, Mesh]:
    """Each element's tessellated body in world coordinates, keyed by STEP id."""
    settings = _settings()
    meshes: dict[int, Mesh] = {}
    for element in model.by_type("IfcElement"):
        if element.Representation is None:
            continue
        try:
            shape: Any = ifcopenshell.geom.create_shape(settings, element)
        except RuntimeError as failed:
            print(f"ifc_facts: no body for {_id(element)}: {failed}", file=sys.stderr)
            continue
        verts = np.asarray(shape.geometry.verts, dtype=float).reshape(-1, 3)
        faces = np.asarray(shape.geometry.faces, dtype=int).reshape(-1, 3)
        if len(verts) and len(faces):
            meshes[element.id()] = (verts, faces)
    return meshes


def _element(element: Entity, meshes: dict[int, Mesh]) -> dict[str, object]:
    systems = ifcopenshell.util.system.get_element_systems(element)
    mesh = meshes.get(element.id())
    centre = (mesh[0].min(axis=0) + mesh[0].max(axis=0)) / 2 if mesh else None
    return {
        "id": _id(element),
        "ifc_class": element.is_a(),
        "systems": sorted(
            {s.PredefinedType for s in systems if getattr(s, "PredefinedType", None)}
        ),
        "centre": _mm(centre, 1.0) if centre is not None else None,
    }


def _port(port: Entity, scale: float) -> dict[str, object]:
    owner = ifcopenshell.util.system.get_port_element(port)
    position = None
    if port.ObjectPlacement is not None:
        matrix = ifcopenshell.util.placement.get_local_placement(port.ObjectPlacement)
        position = _mm(matrix[:3, 3], scale)
    return {"id": _id(port), "element": _id(owner) if owner else "", "position": position}


def _inside(points: np.ndarray, mesh: Mesh) -> bool:
    """Whether any of `points` is inside the closed mesh: an odd count of ray crossings."""
    verts, faces = mesh
    near = np.all((points >= verts.min(axis=0)) & (points <= verts.max(axis=0)), axis=1)
    v0, v1, v2 = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    e1, e2 = v1 - v0, v2 - v0
    p = np.cross(RAY, e2)
    det = np.einsum("ij,ij->i", e1, p)
    hit = np.abs(det) > 1e-12
    inv = np.divide(1.0, det, out=np.zeros_like(det), where=hit)
    for point in points[near]:  # only points within the mesh's bounding box can be inside
        s = point - v0
        u = np.einsum("ij,ij->i", s, p) * inv
        q = np.cross(s, e1)
        v = (q @ RAY) * inv
        t = np.einsum("ij,ij->i", e2, q) * inv
        crossings = hit & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-9)
        if int(crossings.sum()) % 2 == 1:
            return True
    return False


def _clashes(model: ifcopenshell.file, meshes: dict[int, Mesh]) -> tuple[int, list[list[str]]]:
    """Distribution element and wall pairs that touch, intersect or nest; and how many pairs."""
    flows = model.by_type("IfcDistributionElement")
    walls = model.by_type("IfcWall")
    unbodied = [_id(e) for e in [*flows, *walls] if e.id() not in meshes]
    if unbodied:
        print(f"ifc_facts: no body, so no clash tested: {unbodied}", file=sys.stderr)
        return 0, []
    if not flows or not walls:
        return 0, []
    try:
        tree = ifcopenshell.geom.tree(backend="opencascade.trianglebvh")
        tree.add_file(model, _settings())
        found = tree.clash_collision_many(flows, walls, allow_touching=True)
    except RuntimeError as failed:
        print(f"ifc_facts: clash test failed, so none tested: {failed}", file=sys.stderr)
        return 0, []
    wall_ids = {w.id() for w in walls}
    pairs = set()
    for clash in found:
        a, b = clash.a, clash.b
        flow, wall = (b, a) if a.id() in wall_ids else (a, b)
        pairs.add((_id(flow), _id(wall)))
    for flow in flows:  # nesting leaves no surfaces crossing, so the collision test misses it
        f = meshes[flow.id()]
        for wall in walls:
            w = meshes[wall.id()]
            if _inside(f[0], w) or _inside(w[0], f):
                pairs.add((_id(flow), _id(wall)))
    return len(flows) * len(walls), [list(p) for p in sorted(pairs)]


def _on_type(port: Entity) -> bool:
    owner = ifcopenshell.util.system.get_port_element(port)
    return owner is not None and owner.is_a("IfcTypeObject")


def extract(model: ifcopenshell.file) -> dict[str, object]:
    """Measure `model` into the facts schema of `bench/ifc_checks.py`."""
    scale = ifcopenshell.util.unit.calculate_unit_scale(model)  # file unit -> metres
    meshes = _meshes(model)
    tested, clashes = _clashes(model, meshes)
    pairs = [
        (_id(r.RelatingPort), _id(r.RelatedPort)) for r in model.by_type("IfcRelConnectsPorts")
    ]
    connections = [list(p) for p in dict.fromkeys(tuple(sorted(p)) for p in pairs)]
    return {
        "elements": [_element(e, meshes) for e in model.by_type("IfcElement")],
        "ports": [_port(p, scale) for p in model.by_type("IfcDistributionPort") if not _on_type(p)],
        "connections": connections,
        "clash_pairs_tested": tested,
        "clashes": clashes,
    }


def main(argv: list[str]) -> int:
    """Measure one IFC file into one facts file; return the exit code."""
    if len(argv) != 2:
        print("usage: ifc_facts.py IN.ifc OUT.json", file=sys.stderr)
        return 2
    try:
        model = ifcopenshell.open(argv[0])
    except (OSError, RuntimeError, ifcopenshell.Error) as unreadable:
        print(f"ifc_facts: cannot read {argv[0]}: {unreadable}", file=sys.stderr)
        return 1
    facts = extract(model)
    Path(argv[1]).write_text(json.dumps(facts, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
