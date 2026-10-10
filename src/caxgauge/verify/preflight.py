"""Cheap deterministic preflight checks on an exported mesh (plan §7.1, §7.2).

Necessary, not sufficient (`caxgauge.verify.types.NECESSARY_NOT_SUFFICIENT`): these
checks cannot see local defects a render would show a human. Four independent checks,
always reported in this order:

- `file_integrity` — binary STL structural check only (header/triangle-count/file-length
  via `struct`), ported from `../so101-biolab-automation/src/hardware/slicer/validate.py`
  (plan §11). It is **not** a manifold check. ASCII STL files `SKIP` this check (the
  binary layout does not apply); the other three checks still run against them.
- `watertight` — `trimesh.is_watertight` + `is_winding_consistent`; the Euler number is
  reported, never asserted on (plan §7.2: it only catches through-holes, not blind
  feature loss — that is what `volume` is for).
- `bbox` — mesh extents at or below an optional per-axis `envelope` (max extents, not a
  two-sided band); `SKIP` with none given.
- `volume` — mesh volume within an optional two-sided `volume_band`; `SKIP` with none
  given. A non-watertight mesh's volume is not a meaningful measurement, so a *supplied*
  band still reports `FAIL` rather than `SKIP` (`SKIP` is reserved for an absent bound,
  `.claude/rules/verification-honesty.md`) and never `PASS`.

Loading uses `trimesh.load(..., process=True, validate=False)`, never
`trimesh.repair.*`/`fill_holes` (plan §11 — a gauge must never repair what it reports).
`process=False` leaves every triangle's three vertices unmerged (a binary STL stores
vertices by value, not by shared index), so `is_watertight` is `False` for *every* STL,
including a perfect cube — that is a loader artifact, not a defect. `process=True` drops
non-finite values and merges vertices within `trimesh.tol.merge` (1e-8, far below STL's
float32 precision); confirmed empirically that a mesh with one face removed is still
reported non-watertight after merging (merging vertices never re-adds a face).
`validate=False` skips degenerate/duplicate-face removal and normal fixing.

Pure: no network, no agent, no CAD/browser imports.
"""

import struct
from pathlib import Path

import trimesh

from caxgauge.verify.types import CheckResult, PreflightResult, Status

_STL_HEADER_SIZE = 80
_TRIANGLE_RECORD_SIZE = 50
_MIN_BINARY_STL_SIZE = _STL_HEADER_SIZE + 4  # header + uint32 triangle count

_CHECK_ORDER = ("file_integrity", "watertight", "bbox", "volume")


def preflight(
    mesh: Path,
    *,
    envelope: tuple[float, float, float] | None = None,
    volume_band: tuple[float, float] | None = None,
) -> PreflightResult:
    """Run the four deterministic preflight checks on an exported mesh.

    Args:
        mesh: Path to the exported STL file.
        envelope: Optional (x, y, z) max extents the mesh must fit within.
        volume_band: Optional two-sided (min, max) the mesh volume must fall within.

    Returns:
        A `PreflightResult` with one `CheckResult` per check, always in the order
        `file_integrity`, `watertight`, `bbox`, `volume`. An unreadable or
        unparseable mesh produces `FAIL` for every check it could not run — never
        an exception escaping to the caller.
    """
    try:
        data = mesh.read_bytes()
    except OSError as exc:
        return _all_fail(f"could not read {mesh}: {exc}")

    integrity = _file_integrity(data)

    tm_mesh, load_error = _load_mesh(mesh)
    if tm_mesh is None:
        result = _all_fail(f"mesh failed to parse: {load_error}")
        return PreflightResult(checks=(integrity, *result.checks[1:]))

    return PreflightResult(
        checks=(
            integrity,
            _watertight(tm_mesh),
            _bbox(tm_mesh, envelope),
            _volume(tm_mesh, volume_band),
        )
    )


def _all_fail(detail: str) -> PreflightResult:
    """Build a result where every check in `_CHECK_ORDER` is `FAIL` with `detail`."""
    return PreflightResult(
        checks=tuple(
            CheckResult(name=name, status=Status.FAIL, detail=detail) for name in _CHECK_ORDER
        )
    )


def _load_mesh(mesh: Path) -> tuple[trimesh.Trimesh | None, str | None]:
    """Load `mesh` without repairing it; return `(None, reason)` on any failure.

    `process=True` merges vertices within `trimesh.tol.merge` (required: a binary STL
    stores three independent vertices per triangle, so an unprocessed mesh can never
    be watertight); `validate=False` skips degenerate/duplicate-face removal. See the
    module docstring for the empirical check behind this choice. A malformed file may
    either raise or load as an empty/multi-body `Scene` rather than a single
    `Trimesh` — both are treated as a parse failure here, never left to propagate.
    """
    try:
        # trimesh's own type stubs leave `load`'s return partially unknown (it
        # returns the `Geometry` union); narrowed below via `isinstance`.
        loaded = trimesh.load(  # pyright: ignore[reportUnknownMemberType]
            mesh, file_type="stl", process=True, validate=False
        )
    except Exception as exc:
        return None, str(exc)
    if not isinstance(loaded, trimesh.Trimesh):
        return None, "did not parse as a single solid mesh"
    return loaded, None


def _file_integrity(data: bytes) -> CheckResult:
    """Binary-STL structural check only: header size, triangle count, file length.

    Ported from `../so101-biolab-automation/src/hardware/slicer/validate.py:141-183`
    (plan §11, §7.2). This is a **file-integrity** check, not a manifold check: it
    cannot detect non-manifold geometry in an otherwise well-formed file. ASCII STL
    files (no binary header/triangle-count layout) report `SKIP`.
    """
    name = "file_integrity"
    if len(data) < _MIN_BINARY_STL_SIZE:
        detail = (
            f"file too small ({len(data)} bytes, need >= {_MIN_BINARY_STL_SIZE} "
            "for a binary STL header + triangle count)"
        )
        return CheckResult(name=name, status=Status.FAIL, detail=detail)

    (num_triangles,) = struct.unpack_from("<I", data, _STL_HEADER_SIZE)
    expected_size = _MIN_BINARY_STL_SIZE + _TRIANGLE_RECORD_SIZE * num_triangles

    if num_triangles > 0 and len(data) == expected_size:
        detail = (
            f"binary STL: header present, {num_triangles} triangles, file length matches 84 + 50*n"
        )
        return CheckResult(name=name, status=Status.PASS, detail=detail)

    if data[:5].lower() == b"solid":
        detail = (
            "ASCII STL (starts with 'solid'): the binary header/triangle-count/"
            "file-length structure this check validates does not apply"
        )
        return CheckResult(name=name, status=Status.SKIP, detail=detail)

    if num_triangles == 0:
        return CheckResult(
            name=name, status=Status.FAIL, detail="zero triangles in binary STL header"
        )

    detail = (
        f"file length mismatch: expected {expected_size} bytes "
        f"(84 + 50*{num_triangles}), got {len(data)}"
    )
    return CheckResult(name=name, status=Status.FAIL, detail=detail)


def _watertight(tm_mesh: trimesh.Trimesh) -> CheckResult:
    """Watertight + consistent winding; the Euler number is reported, never asserted on."""
    watertight = bool(tm_mesh.is_watertight)
    winding_ok = bool(tm_mesh.is_winding_consistent)
    status = Status.PASS if (watertight and winding_ok) else Status.FAIL
    detail = (
        f"watertight={watertight}, winding_consistent={winding_ok}, "
        f"euler_number={tm_mesh.euler_number} (reported only, not asserted — plan §7.2)"
    )
    return CheckResult(name="watertight", status=status, detail=detail)


def _bbox(tm_mesh: trimesh.Trimesh, envelope: tuple[float, float, float] | None) -> CheckResult:
    """Mesh extents at or below a per-axis `envelope` (max extents); `SKIP` with none given."""
    if envelope is None:
        return CheckResult(name="bbox", status=Status.SKIP, detail="no --envelope given")
    extents = tuple(float(e) for e in tm_mesh.extents)
    fits = all(e <= bound for e, bound in zip(extents, envelope, strict=True))
    status = Status.PASS if fits else Status.FAIL
    detail = f"extents={extents}, envelope={tuple(envelope)}"
    return CheckResult(name="bbox", status=status, detail=detail)


def _volume(tm_mesh: trimesh.Trimesh, volume_band: tuple[float, float] | None) -> CheckResult:
    """Mesh volume within a two-sided `volume_band`; `SKIP` with none given.

    A non-watertight mesh's volume is not a meaningful measurement, so a *supplied*
    band still reports `FAIL` (never `SKIP` — the bound was given; never `PASS` — the
    measurement is not trustworthy).
    """
    if volume_band is None:
        return CheckResult(name="volume", status=Status.SKIP, detail="no --volume-band given")
    if not tm_mesh.is_watertight:
        detail = "mesh is not watertight: volume is not a meaningful measurement"
        return CheckResult(name="volume", status=Status.FAIL, detail=detail)
    volume = float(tm_mesh.volume)
    low, high = volume_band
    status = Status.PASS if low <= volume <= high else Status.FAIL
    detail = f"volume={volume}, band=[{low}, {high}]"
    return CheckResult(name="volume", status=status, detail=detail)
