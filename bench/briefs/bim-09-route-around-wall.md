---
envelope: 3001,2601,3001
elements: IfcWall=1; IfcPipeSegment=2..8; IfcPipeFitting=1..7
systems: IfcPipeSegment=DOMESTICCOLDWATER; IfcPipeFitting=DOMESTICCOLDWATER
open_ports: 2
networks: 1
joints: 1
ends: 0,0,1000; 3000,0,1000
ends_tol: 5
path_length: 3000,6000
no_clash: yes
---

# Brief: route a cold-water pipe around a wall

A straight wall, one IFC wall element with no openings, 2000 mm long along Y (from Y = -1000
to Y = 1000), 200 mm thick (X from 1400 to 1600) and 3000 mm tall (Z up), standing on the
floor at Z = 0.

Route a domestic cold-water pipe, 32 mm outside diameter, from (0, 0, 1000) on one side of the
wall to (3000, 0, 1000) on the other. You choose the path, within these constraints: the
centreline stays horizontal, 1000 mm above the floor; the pipe leaves its start and reaches
its end running along X; it does not pass through or touch the wall; every part of it stays
between X = 0 and X = 3000 and between Y = -1600 and Y = 1600; and it is built from straight
pipe segments joined by elbow pipe fittings, at most 8 segments.

Give every segment and fitting a distribution port at each of its two ends, placed on the
centreline, and connect the two ports wherever two elements meet. The ends at (0, 0, 1000)
and (3000, 0, 1000) stay unconnected. Assign every segment and fitting to one distribution
system whose type is DOMESTICCOLDWATER.

Bounds: element counts (2–8 segments, 1–7 fittings, one wall); system membership; 2 open
ports within 5 mm of the declared ends; one connected network; connected ports within 1 mm
of each other; no clash with the wall, paired with the ends; a path length, summed port to
port along the run, between 3000 mm (the straight line, which the wall rules out) and
6000 mm (twice it). Blind spot: the wall's own position is not checked; the envelope and the
render cover it. Envelope = 3000 × 2600 × 3000 mm (the wall from Y = -1000 to the route's
limit at 1600) with 1 mm margin. No volume band (volume reports `SKIP`). The IFC-level bounds
are decided by `bench/ifc_checks.py` (plan §5 BENCH-MEP); until the extractor is wired (PR B),
only the envelope is scored.
