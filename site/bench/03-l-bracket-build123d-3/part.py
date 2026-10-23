from build123d import *

# Base plate: X -20..20, Y -15..15, Z 0..5. Upright at Y -15..-10 (open edge at +Y).
# Holes at Y=+5 (5 mm from centre line toward open edge), X=+-12.
with BuildPart() as p:
    with Locations((0, 0, 2.5)):
        Box(40, 30, 5)
    with Locations((0, -12.5, 15)):
        Box(40, 5, 30)
    with Locations((12, 5, 0), (-12, 5, 0)):
        Cylinder(2.5, 5, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

export_stl(p.part, "part.stl")
