"""Tessellate every element of an IFC file into one STL, in millimetres (bench BIM track).

Usage: uv run --no-project --with ifcopenshell --with trimesh python bench/ifc_to_stl.py IN OUT

Bench tooling, not part of the gauge: `caxgauge check` scores the STL like any other part.
IfcOpenShell outputs metres; the briefs' bounds are in millimetres, so the mesh is scaled.
"""

import sys

import ifcopenshell
import ifcopenshell.geom
import numpy as np
import trimesh


def main(src: str, dst: str) -> int:
    """Write all product geometry in `src` to the STL `dst`; return a process exit code."""
    model = ifcopenshell.open(src)
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)
    meshes = []
    for product in model.by_type("IfcProduct"):
        if product.Representation is None or product.is_a("IfcOpeningElement"):
            continue
        shape = ifcopenshell.geom.create_shape(settings, product)
        verts = np.array(shape.geometry.verts).reshape(-1, 3) * 1000.0
        faces = np.array(shape.geometry.faces).reshape(-1, 3)
        meshes.append(trimesh.Trimesh(vertices=verts, faces=faces, process=False))
    if not meshes:
        print(f"ifc_to_stl: no product geometry in {src}", file=sys.stderr)
        return 1
    trimesh.util.concatenate(meshes).export(dst)
    print(f"ifc_to_stl: {len(meshes)} element(s) -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
