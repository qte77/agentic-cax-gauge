from build123d import *

# Assumptions: base centred on origin in XY, z 0..5; upright at the y=-15 edge
# (wall y -15..-10, z up to 30). Holes at y=+5 (towards open edge), x=+-12.
with BuildPart() as p:
    with Locations((0, 0, 2.5)):
        Box(40, 30, 5)
    with Locations((0, -12.5, 15)):
        Box(40, 5, 30)
    with Locations((-12, 5, 0), (12, 5, 0)):
        Cylinder(2.5, 5, mode=Mode.SUBTRACT, align=(Align.CENTER, Align.CENTER, Align.MIN))

export_stl(p.part, "part.stl")
