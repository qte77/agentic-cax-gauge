from build123d import *

# Assumptions (PETG, 0.4 mm nozzle FDM):
# - Box outer 50x30, wall 1.5 -> inner cavity 47x27.
# - Box walls have small notches/ledge ~4 mm below the top edge (inside face)
#   so the hook barbs can catch; hook barb catch face is at 4 mm below wall top.
# - Lid plate 52x32x2 (1 mm overhang), underside at z=3 (plate z 3..5).
# - Locating rim: 1.2 mm thick, 3 mm tall, 0.2 mm clearance to the inner wall.
# - Snap arms: 1.2 thick x 8 wide, 7 mm long below plate, barb 0.6 mm
#   with 45-degree lead-in ramp; 2 per long side (4 total).
PL_X, PL_Y, PL_T = 52, 32, 2
RIM_H = 3
CLR = 0.2
RO_X, RO_Y = 47 / 2 - CLR, 27 / 2 - CLR   # 23.3, 13.3
T = 1.2
ARM_W = 8
ARM_BOT = -4
BARB = 0.6

lid = Pos(0, 0, RIM_H + PL_T / 2) * Box(PL_X, PL_Y, PL_T)
ring = Pos(0, 0, RIM_H / 2) * Box(2 * RO_X, 2 * RO_Y, RIM_H) \
    - Pos(0, 0, RIM_H / 2) * Box(2 * (RO_X - T), 2 * (RO_Y - T), RIM_H + 1)
lid = lid + ring

for sx in (-1, 1):
    for sy in (-1, 1):
        xc = sx * 12
        # slots in ring either side of arm (flex relief), up to plate
        for dx in (-4.5, 4.5):
            lid = lid - Pos(xc + dx, sy * (RO_Y - T / 2), RIM_H / 2) * Box(1, T + 0.4, RIM_H)
        # arm
        arm = Pos(xc, sy * (RO_Y - T / 2), (ARM_BOT + RIM_H) / 2) * Box(ARM_W, T, RIM_H - ARM_BOT)
        # barb profile in (y,z), outward pointing, extruded along x
        pts = [(RO_Y, ARM_BOT), (RO_Y + BARB, ARM_BOT + BARB), (RO_Y + BARB, -1), (RO_Y, -1)]
        with BuildSketch(Plane.YZ) as sk:
            with BuildLine():
                Polyline(*pts, close=True)
            make_face()
        barb = extrude(sk.sketch, amount=ARM_W / 2, both=True)
        barb = Pos(xc, 0, 0) * barb
        if sy < 0:
            barb = mirror(barb, Plane.XZ)
        lid = lid + arm + barb

part = lid.solids().sort_by(Axis.Z)[0] if len(lid.solids()) > 1 else lid
export_stl(part, "part.stl")
