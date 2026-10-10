"""Behaviour tests for `preflight` (plan §7.1 wave 1, §7.2, §7.3).

Fixtures live in `tests/fixtures/` (see `make_fixtures.py` for how they were made).
Strict TDD: these tests are written before `src/caxgauge/verify/preflight.py` exists.
"""

from pathlib import Path

import trimesh
from hypothesis import given, settings
from hypothesis import strategies as st

from caxgauge.verify.preflight import preflight
from caxgauge.verify.types import Status

FIXTURES = Path(__file__).parent.parent / "fixtures"

GOOD = FIXTURES / "good.stl"
OVERSIZE = FIXTURES / "oversize.stl"
NON_MANIFOLD = FIXTURES / "non_manifold.stl"
HEADLINE_INTENDED = FIXTURES / "feature_absorbed_intended.stl"
HEADLINE_BUGGY = FIXTURES / "feature_absorbed_buggy.stl"

# Matches make_fixtures.py's GOOD_EXTENTS = (20.0, 15.0, 10.0); volume = 20*15*10.
GOOD_ENVELOPE = (20.001, 15.001, 10.001)
GOOD_VOLUME_BAND = (2999.9, 3000.1)


def _by_name(result, name: str):
    return next(c for c in result.checks if c.name == name)


def test_good_part_passes_all_checks_with_bounds_supplied():
    result = preflight(GOOD, envelope=GOOD_ENVELOPE, volume_band=GOOD_VOLUME_BAND)
    assert result.green
    assert not result.hard_fail
    assert [c.name for c in result.checks] == ["file_integrity", "watertight", "bbox", "volume"]
    for check in result.checks:
        assert check.status is Status.PASS


def test_non_manifold_fixture_fails_watertight():
    result = preflight(NON_MANIFOLD, envelope=GOOD_ENVELOPE, volume_band=GOOD_VOLUME_BAND)
    assert result.hard_fail
    assert not result.green
    watertight = _by_name(result, "watertight")
    assert watertight.status is Status.FAIL


def test_oversize_fixture_fails_bbox():
    result = preflight(OVERSIZE, envelope=GOOD_ENVELOPE)
    bbox = _by_name(result, "bbox")
    assert bbox.status is Status.FAIL
    assert not result.green


def test_headline_feature_absorbed_fails_volume_band():
    """If this ever passes green, the preflight is worthless (plan §7.3)."""
    intended_mesh = trimesh.load(HEADLINE_INTENDED)
    intended_volume = float(intended_mesh.volume)
    band = (intended_volume * 0.99, intended_volume * 1.01)

    result = preflight(HEADLINE_BUGGY, volume_band=band)

    watertight = _by_name(result, "watertight")
    assert watertight.status is Status.PASS, "the fused part must stay watertight"

    volume = _by_name(result, "volume")
    assert volume.status is Status.FAIL
    assert not result.green


def test_unbounded_run_skips_bbox_and_volume_and_is_not_green():
    result = preflight(GOOD)
    bbox = _by_name(result, "bbox")
    volume = _by_name(result, "volume")
    assert bbox.status is Status.SKIP
    assert "--envelope" in bbox.detail
    assert volume.status is Status.SKIP
    assert "--volume-band" in volume.detail
    assert not result.green
    assert {c.name for c in result.skipped} == {"bbox", "volume"}


def test_ascii_stl_file_integrity_is_skip_but_other_checks_still_run(tmp_path):
    ascii_stl = tmp_path / "ascii.stl"
    ascii_stl.write_text(
        "solid single_triangle\n"
        "  facet normal 0 0 1\n"
        "    outer loop\n"
        "      vertex 0 0 0\n"
        "      vertex 1 0 0\n"
        "      vertex 0 1 0\n"
        "    endloop\n"
        "  endfacet\n"
        "endsolid single_triangle\n"
    )

    result = preflight(ascii_stl)

    integrity = _by_name(result, "file_integrity")
    assert integrity.status is Status.SKIP
    assert "ascii" in integrity.detail.lower()
    # The other checks still ran (no exception) — they just don't gate on an
    # unbounded run.
    assert [c.name for c in result.checks] == ["file_integrity", "watertight", "bbox", "volume"]


def test_unparseable_file_produces_fail_checks_not_exception(tmp_path):
    garbage = tmp_path / "garbage.stl"
    garbage.write_bytes(b"not an stl file at all, just some short garbage bytes")

    result = preflight(garbage, envelope=GOOD_ENVELOPE, volume_band=GOOD_VOLUME_BAND)

    assert [c.name for c in result.checks] == ["file_integrity", "watertight", "bbox", "volume"]
    for check in result.checks:
        assert check.status is Status.FAIL
    assert result.hard_fail
    assert not result.green


def test_details_never_say_verified():
    result = preflight(GOOD, envelope=GOOD_ENVELOPE, volume_band=GOOD_VOLUME_BAND)
    for check in result.checks:
        assert "verified" not in check.detail.lower()


@settings(deadline=None, max_examples=20)
@given(
    x=st.floats(min_value=1.0, max_value=50.0),
    y=st.floats(min_value=1.0, max_value=50.0),
    z=st.floats(min_value=1.0, max_value=50.0),
)
def test_bbox_passes_its_own_envelope_and_fails_a_perturbed_one(x, y, z, tmp_path_factory):
    box = trimesh.creation.box(extents=(x, y, z))

    mesh_path = tmp_path_factory.mktemp("bbox-prop") / "box.stl"
    box.export(mesh_path, file_type="stl")

    # Binary STL stores coordinates as float32, so re-derive the envelope from the
    # reloaded mesh (what `preflight` will actually see), not the pre-export float64
    # extents — otherwise the round-trip's float32 precision loss can make a
    # same-size envelope FAIL by an epsilon.
    reloaded = trimesh.load(mesh_path, file_type="stl", process=True, validate=False)
    extents = tuple(float(e) for e in reloaded.extents)

    fits = preflight(mesh_path, envelope=extents)
    assert _by_name(fits, "bbox").status is Status.PASS

    perturbed = (extents[0] / 2, extents[1], extents[2])
    shrunk = preflight(mesh_path, envelope=perturbed)
    assert _by_name(shrunk, "bbox").status is Status.FAIL
