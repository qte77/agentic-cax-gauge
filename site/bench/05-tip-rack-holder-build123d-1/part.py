from build123d import *

# Outer 127x85, base 3 mm, wall 10 mm on top of base (total 13); inner pocket 123x81 open at top.
with BuildPart() as p:
    Box(127, 85, 13, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, 0, 3)):
        Box(123, 81, 10, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

export_stl(p.part, "part.stl")
