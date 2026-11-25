---
envelope: 2017,1517,33
elements: IfcPipeSegment=2; IfcPipeFitting=1
systems: IfcPipeSegment=DOMESTICCOLDWATER; IfcPipeFitting=DOMESTICCOLDWATER
ports: 6
open_ports: 2
networks: 1
joints: 1
ends: 0,0,1000; 2000,1500,1000
ends_tol: 5
---

# Brief: cold-water pipe with an elbow

A domestic cold-water pipe, 32 mm outside diameter, whose centreline runs 1000 mm above the
floor (Z up). It starts at (0, 0, 1000), runs along X to a 90° corner at (2000, 0, 1000), and
turns to run along Y to its end at (2000, 1500, 1000). Model it as three IFC elements: two
straight pipe segments and one elbow pipe fitting at the corner, which both segments meet.

Give each of the three elements a distribution port at each of its two ends, placed on the
centreline, and connect the two ports wherever two elements meet. The free ends at
(0, 0, 1000) and (2000, 1500, 1000) stay unconnected. Assign all three elements to one
distribution system whose type is DOMESTICCOLDWATER.

Bounds: element counts; system membership; 6 ports, 2 of them open; one connected network;
connected ports within 1 mm of each other; the 2 open ports within 5 mm of the declared ends.
Envelope = the run's extents (2016 × 1516 × 32 mm: the centreline's extents plus the 16 mm
radius where the pipe sticks out past them) with 1 mm margin. No volume band: a thin pipe's
volume depends on the mesh more than on the model, so volume reports `SKIP`. The IFC-level
bounds are decided by `bench/ifc_checks.py` from facts measured on the agent's IFC (plan §5
BENCH-MEP); until the extractor is wired (PR B), only the envelope is scored.
