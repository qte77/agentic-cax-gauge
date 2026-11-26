---
envelope: 3003,111,171
elements: IfcPipeSegment=1
systems: IfcPipeSegment=DRAINAGE
ports: 2
open_ports: 2
networks: 1
ends: 0,0,500; 3000,0,440
ends_tol: 5
fall: IfcPipeSegment=0.015,0.025
---

# Brief: drain pipe laid to a fall

A straight drain pipe, 110 mm outside diameter, modelled as one IFC pipe segment. Its
centreline runs along X from (0, 0, 500) to (3000, 0, 440), Z up: it falls 60 mm over its
3000 mm run, a 2 % fall toward the outlet end at X = 3000.

Give the segment a distribution port at each end, placed on the centreline, and leave both
unconnected. Assign it to a distribution system whose type is DRAINAGE.

Bounds: one segment in a DRAINAGE system; 2 ports, both open, within 5 mm of the declared
ends; a fall between 1.5 % and 2.5 % (two-sided around the stated 2 %: too flat and too steep
both fail). Envelope = the pipe's extents (about 3002.2 × 110 × 170.0 mm: the slope tilts the
end faces by 1.1 mm along X) with about 1 mm margin. No volume band (volume reports `SKIP`).
The IFC-level bounds are decided by `bench/ifc_checks.py` from the facts `bench/ifc_facts.py`
measures on the agent's IFC (plan §5 BENCH-MEP).
