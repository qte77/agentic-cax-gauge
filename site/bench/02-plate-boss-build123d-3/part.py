from build123d import *

# Plate 40x40x5 with base at Z=0; boss D10 x 8 centred on top face.
with BuildPart() as p:
    Box(40, 40, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
    with Locations((0, 0, 5)):
        Cylinder(5, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))

export_stl(p.part, "part.stl")
