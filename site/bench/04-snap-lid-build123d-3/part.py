from build123d import *

# Assumptions (mm): box outer 50x30, wall 1.5 -> inner 47x27. PETG, FDM 0.4 nozzle.
# Lid top face at z=2, plate underside at z=0, rim and hooks extend to -z.
# Box is assumed to have a small outer bead/ledge just below its top edge
# that the hook barbs snap under.
PL, PW, PT = 52, 32, 2.0          # plate: 1 mm overhang per side
CL = 0.2                          # rim clearance per side to inner wall face
RIM_T, RIM_D = 1.2, 3.0           # rim wall thickness (3 perimeters), depth
ARM_T, ARM_W, ARM_L = 1.0, 10.0, 6.0  # hook arm (long enough to flex, 1 mm thick)
ARM_GAP = 0.3                     # gap between arm and outer wall face
BARB = 0.6                        # barb engagement depth

plate = Pos(0, 0, PT / 2) * Box(PL, PW, PT)

ro_x, ro_y = 47 - 2 * CL, 27 - 2 * CL
outer = Pos(0, 0, -RIM_D / 2) * Box(ro_x, ro_y, RIM_D)
inner = Pos(0, 0, -RIM_D / 2) * Box(ro_x - 2 * RIM_T, ro_y - 2 * RIM_T, RIM_D + 1)
lid = plate + (outer - inner)

y_in = 15 + ARM_GAP               # arm inner face
y_out = y_in + ARM_T              # 16.3 (within plate edge at 16)
for sx in (-10, 10):
    arm = Pos(sx, (y_in + y_out) / 2, -ARM_L / 2) * Box(ARM_W, ARM_T, ARM_L)
    # barb profile in (y,z): flat catch face on top, lead-in chamfer below
    with BuildSketch(Plane.YZ) as sk:
        Polygon((y_in, -ARM_L + 1.4), (y_in - BARB, -ARM_L + 1.4),
                (y_in, -ARM_L - 0.0), align=None)
    barb = Pos(sx - ARM_W / 2, 0, 0) * extrude(sk.sketch, ARM_W)
    hook = arm + barb
    lid = lid + hook + mirror(hook, Plane.XZ)

export_stl(lid, "part.stl")
