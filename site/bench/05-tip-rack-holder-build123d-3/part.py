from build123d import *

# Assumption: base spans the full outer footprint 127 x 85, 3 mm thick;
# wall 2 mm thick, 10 mm tall on top of base (13 mm total); inside pocket 123 x 81.
with BuildPart() as p:
    Box(127, 85, 13, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, 0, 3)):
        Box(123, 81, 10, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)

export_stl(p.part, "part.stl")
