#!/usr/bin/env bash
# One-machine proof (plan §5 BENCH-2): does each tool run headless here, and does the gauge
# score its output? No agent and no model — every part below is written by us. Output goes to
# the Machine's log (`fly logs`).
set -uo pipefail
cd "$(dirname "$0")/../.."
work="$(mktemp -d)"

check() {  # check NAME STL ENVELOPE BAND
	echo "== $1"
	uv run caxgauge check "$2" --envelope "$3" --volume-band "$4" --no-render --out "$work/$1-report"
	echo "exit=$?"
}

echo "== solidcraft-cli"
solidcraft-cli --version
# A 40 x 30 x 20 box: sketch on XY, rectangle, extrude.
cat > "$work/box.json" <<'EOF'
{"commands": [
  {"command": "sketch.create", "params": {"plane": "XY"}},
  {"command": "sketch.rectangle.two_point", "params": {"p0": [0, 0], "p1": [40, 30]}},
  {"command": "solid.extrude", "params": {"distance": 20}}
]}
EOF
solidcraft-cli run "$work/box.json" --out "$work/box-sc.stl" && check solidcraft "$work/box-sc.stl" 41,31,21 23760,24240

echo "== openscad"
echo 'cube([40, 30, 20]);' > "$work/box.scad"
openscad -o "$work/box-os.stl" "$work/box.scad" && check openscad "$work/box-os.stl" 41,31,21 23760,24240

echo "== build123d"
cat > "$work/box.py" <<EOF
from build123d import Box, Align, export_stl
export_stl(Box(40, 30, 20, align=Align.MIN), "$work/box-b3d.stl")
EOF
uv run --no-project --with build123d python "$work/box.py" && check build123d "$work/box-b3d.stl" 41,31,21 23760,24240

echo "== claude"
claude --version
echo "probe: done"
