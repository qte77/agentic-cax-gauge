---
envelope: 1101,51,101
elements: IfcJunctionBox=1; IfcCableCarrierSegment=2; IfcOutlet=2
systems: IfcJunctionBox=ELECTRICAL; IfcCableCarrierSegment=ELECTRICAL; IfcOutlet=ELECTRICAL
ports: 8
open_ports: 0
networks: 1
joints: 1
height: IfcOutlet=290,310
---

# Brief: junction box feeding two outlets by conduit

Three boxes in a row along X, each 100 mm wide (X), 50 mm deep (Y) and 100 mm tall (Z, up),
centred at Y = 0 and 300 mm above the floor: a junction box centred at X = 1000, and two
power outlets centred at X = 500 and X = 1500. Two straight conduits, 20 mm outside diameter,
run along X at that height from the junction box's sides to the outlets' facing sides: one from
X = 950 to X = 550, the other from X = 1050 to X = 1450. Model them as five IFC elements: a
junction box, two cable-carrier segments of type conduit, and two outlets of type power outlet.

Give the junction box a distribution port on each side where a conduit meets it, each conduit a
port at each end, and each outlet one port on its side facing the junction box, all on the
conduit centreline. Connect the two ports wherever two elements meet. Assign all five
elements to one distribution system whose type is ELECTRICAL.

Bounds: element counts; system membership; 8 ports, none open; one connected network;
connected ports within 1 mm of each other; each outlet's centre (of its geometry) between
290 and 310 mm above the floor around the stated 300 mm. Envelope = the row's extents
(1100 × 50 × 100 mm) with 1 mm margin. No volume band (volume reports `SKIP`). The IFC-level
bounds are decided by `bench/ifc_checks.py` from the facts `bench/ifc_facts.py` measures on
the agent's IFC (plan §5 BENCH-MEP).
