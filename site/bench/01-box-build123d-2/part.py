# Assumption: block centred on the origin in X and Y, sitting on Z=0 (corner option ambiguous);
# here we choose a corner at the origin (spans 0..20, 0..15, 0..10).
from build123d import *

with BuildPart() as p:
    Box(20, 15, 10, align=(Align.MIN, Align.MIN, Align.MIN))

export_stl(p.part, "part.stl")
