from build123d import *

# Assumptions: wall is 10 mm tall on top of the 3 mm base (13 mm overall).
# Outside 127x85, inside pocket 123x81 (0.5 mm clearance around 122x80 rack).
with BuildPart() as p:
    Box(127, 85, 13, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, 0, 3)):
        Box(123, 81, 10, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

export_stl(p.part, "part.stl")
