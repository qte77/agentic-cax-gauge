---
envelope: 4001,1201,3001
elements: IfcWall=1; IfcOpeningElement=2; IfcPipeSegment=1; IfcCableCarrierSegment=1
systems: IfcPipeSegment=DOMESTICCOLDWATER; IfcCableCarrierSegment=ELECTRICAL
ports: 4
open_ports: 4
networks: 2
ends: 1000,-500,1000; 1000,700,1000; 3000,-500,500; 3000,700,500
ends_tol: 5
no_clash: yes
---

# Brief: wall with a pipe and a conduit passing through

A straight wall, one IFC wall element, 4000 mm long (X from 0 to 4000), 200 mm thick (Y from
0 to 200) and 3000 mm tall (Z up), standing on the floor at Z = 0. Two square openings pass
through its full thickness, each an IFC opening that voids the wall: one 100 × 100 mm centred
at X = 1000, Z = 1000, and one 50 × 50 mm centred at X = 3000, Z = 500.

A cold-water pipe, 32 mm outside diameter, modelled as one straight pipe segment, runs along Y
through the first opening from (1000, -500, 1000) to (1000, 700, 1000). A conduit, 20 mm
outside diameter, modelled as one straight cable-carrier segment of type conduit, runs along Y
through the second opening from (3000, -500, 500) to (3000, 700, 500). Neither touches the wall.

Give the pipe and the conduit a distribution port at each end, placed on the centreline, and
leave all four unconnected. Assign the pipe to a distribution system whose type is
DOMESTICCOLDWATER and the conduit to one whose type is ELECTRICAL.

Bounds: element counts; system membership; 4 ports, all open, in two separate networks; no
clash between the pipe or the conduit and the voided wall, paired with the 4 open ports within
5 mm of the declared ends (a pipe moved clear of the wall avoids the clash but misses its
ends). Blind spot: the openings' sizes and positions are not checked as bounds; an opening
the pipe or conduit touches or misses shows as a clash, and the render shows the rest. Envelope = 4000 × 1200 × 3000 mm with 1 mm margin. No volume band (volume reports
`SKIP`). The IFC-level bounds are decided by `bench/ifc_checks.py` from the facts
`bench/ifc_facts.py` measures on the agent's IFC (plan §5 BENCH-MEP); touching the wall counts
as a clash.
