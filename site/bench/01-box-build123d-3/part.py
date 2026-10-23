from build123d import *

# Assumption: block with one corner at the origin (extends +X, +Y, +Z).
with BuildPart() as p:
    Box(20, 15, 10, align=(Align.MIN, Align.MIN, Align.MIN))

export_stl(p.part, "part.stl")
