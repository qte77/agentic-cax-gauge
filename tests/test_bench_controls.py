"""Control parts for the benchmark briefs: test the gauge's bounds, not the contestants.

Every part here is made from `trimesh` primitives, never by a contestant tool (OpenSCAD,
build123d), so a brief's bounds are checked against parts its scorer did not shape (plan §5
BENCH-3 item 2). Three controls per brief with bounds:

- a null part (empty file) must fail;
- a box filling the whole envelope must fail its volume band, unless the brief's part *is* a
  cuboid of that size, so the bounds genuinely cannot tell them apart;
- a box with the band's volume that fits the envelope passes preflight: bounds cannot see
  shape. That is the documented blind spot the render and the human cover. Green is
  necessary, not sufficient.

Plus known-good parts, made independently, for the briefs whose part is a primitive.
"""

from pathlib import Path

import pytest
import trimesh

from caxgauge.verify.preflight import preflight
from caxgauge.verify.types import PreflightResult, Status

BRIEFS = Path(__file__).resolve().parent.parent / "bench" / "briefs"
FIXTURES = Path(__file__).parent / "fixtures"

# Briefs whose part is a plain cuboid filling its envelope less the margin: an envelope box
# lands in their band by construction, so for them the bounds cannot reject it.
CUBOID_BRIEFS = {"bim-01-wall", "bim-04-slab"}


def _front_matter(brief: Path) -> dict[str, str]:
    parts = brief.read_text().split("---", 2)
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def _bounds(brief: Path) -> tuple[tuple[float, float, float], tuple[float, float]] | None:
    fm = _front_matter(brief)
    if "envelope" not in fm or "volume_band" not in fm:
        return None
    x, y, z = (float(v) for v in fm["envelope"].split(","))
    low, high = (float(v) for v in fm["volume_band"].split(","))
    return (x, y, z), (low, high)


BOUNDED = [b for b in sorted(BRIEFS.glob("*.md")) if _bounds(b) is not None]


def _failed(result: PreflightResult) -> set[str]:
    return {c.name for c in result.checks if c.status is Status.FAIL}


def _check(part: trimesh.Trimesh, brief: Path, tmp_path: Path) -> PreflightResult:
    bounds = _bounds(brief)
    assert bounds is not None
    envelope, band = bounds
    stl = tmp_path / "part.stl"
    part.export(stl)
    return preflight(stl, envelope=envelope, volume_band=band)


def _at_origin(part: trimesh.Trimesh) -> trimesh.Trimesh:
    part.apply_translation(-part.bounds[0])
    return part


def test_every_bounded_brief_is_covered():
    # 15 CAD briefs, minus the open-design snap lid (envelope only), plus 4 BIM briefs.
    assert len(BOUNDED) == 18


def test_a_null_part_fails(tmp_path: Path):
    empty = tmp_path / "part.stl"
    empty.write_bytes(b"")
    assert "file_integrity" in _failed(preflight(empty, envelope=(1, 1, 1), volume_band=(1, 2)))


@pytest.mark.parametrize("brief", BOUNDED, ids=lambda b: b.stem)
def test_an_envelope_filling_box_fails_the_volume_band(brief: Path, tmp_path: Path):
    bounds = _bounds(brief)
    assert bounds is not None
    envelope, _ = bounds
    box = _at_origin(trimesh.creation.box(extents=[e - 0.01 for e in envelope]))
    failed = _failed(_check(box, brief, tmp_path))
    if brief.stem in CUBOID_BRIEFS:
        assert failed == set(), "cuboid brief: an envelope box is a correct answer"
    else:
        assert failed == {"volume"}


@pytest.mark.parametrize("brief", BOUNDED, ids=lambda b: b.stem)
def test_right_volume_wrong_shape_passes_preflight_the_render_must_catch_it(
    brief: Path, tmp_path: Path
):
    bounds = _bounds(brief)
    assert bounds is not None
    (x, y, _), (low, high) = bounds
    # A plain slab: the envelope's footprint less the margin, as tall as the band's middle
    # volume needs. It has none of the brief's features (holes, bosses, pockets, walls).
    wx, wy = x - 1, y - 1
    slab = _at_origin(trimesh.creation.box(extents=[wx, wy, (low + high) / 2 / (wx * wy)]))
    assert _failed(_check(slab, brief, tmp_path)) == set()


def test_known_good_box_is_inside_its_bounds(tmp_path: Path):
    box = _at_origin(trimesh.creation.box(extents=[20, 15, 10]))
    assert _failed(_check(box, BRIEFS / "01-box.md", tmp_path)) == set()


def test_known_good_cylinder_is_inside_its_bounds(tmp_path: Path):
    cylinder = _at_origin(trimesh.creation.cylinder(radius=15, height=50, sections=256))
    assert _failed(_check(cylinder, BRIEFS / "06-cylinder.md", tmp_path)) == set()


def test_known_good_plate_with_boss_is_inside_its_bounds(tmp_path: Path):
    # The headline fixture's intended part (tests/fixtures/make_fixtures.py), made once with
    # build123d as a test fixture, not a benchmark run.
    part = trimesh.load(FIXTURES / "feature_absorbed_intended.stl", file_type="stl")
    assert isinstance(part, trimesh.Trimesh)
    assert _failed(_check(part, BRIEFS / "02-plate-boss.md", tmp_path)) == set()
