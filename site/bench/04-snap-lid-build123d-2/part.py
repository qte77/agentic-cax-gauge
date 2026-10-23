from build123d import *

# Assumptions (mm): box outer 50x30, wall 1.5 -> inner 47x27. PETG FDM, 0.4 nozzle.
# Box is assumed to have a small internal groove/ledge just under its top edge
# for the hook barbs to catch on.
PLATE_X, PLATE_Y, PLATE_T = 52.0, 32.0, 2.0   # 1 mm overhang per side
CLEAR = 0.2                                    # per-side clearance for rim
RIM_X, RIM_Y = 47.0 - 2*CLEAR, 27.0 - 2*CLEAR  # 46.6 x 26.6
RIM_W, RIM_H = 1.2, 3.0                        # 3 perimeters of 0.4
HOOK_W = 8.0                                   # hook width along X
HOOK_L = 7.0                                   # hook length below plate underside
BARB = 0.7                                     # barb protrusion
HOOK_XS = (-10.0, 10.0)                        # two hooks per long side -> 4 hooks

# Plate occupies z 0..2 (top faces up); rim and hooks hang below z=0
with BuildPart() as lid:
    with Locations((0, 0, PLATE_T/2)):
        Box(PLATE_X, PLATE_Y, PLATE_T)
    # locating rim
    with BuildSketch(Plane.XY.offset(-RIM_H)):
        Rectangle(RIM_X, RIM_Y)
        Rectangle(RIM_X - 2*RIM_W, RIM_Y - 2*RIM_W, mode=Mode.SUBTRACT)
    extrude(amount=RIM_H + 0.01)

    yo = RIM_Y/2          # rim outer face
    yi = yo - RIM_W
    for sgn in (1, -1):
        for hx in HOOK_XS:
            # profile in (Y, Z): arm + barb with catch face on top, lead-in ramp below
            pts = [(yi, 0.5), (yo, 0.5), (yo, -HOOK_L + 2.2),
                   (yo + BARB, -HOOK_L + 2.2),      # flat catch face (upper)
                   (yo + BARB, -HOOK_L + 1.2),
                   (yo - 0.3, -HOOK_L),             # ramp to tip
                   (yi, -HOOK_L)]
            pts = [(sgn*p[0], p[1]) for p in pts]
            with BuildSketch(Plane.YZ.offset(hx)):
                Polygon(*pts, align=None)
            extrude(amount=HOOK_W/2, both=True)

part = lid.part
export_stl(part, "part.stl")
