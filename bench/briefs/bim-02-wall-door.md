---
envelope: 5001,201,3001
volume_band: 2595780000,2648220000
---

# Brief: wall with a door opening

A straight wall, modelled as one IFC wall element: 5000 mm long (along X), 200 mm thick
(along Y) and 3000 mm tall (Z up), standing on the ground at Z = 0.
It has one door opening 900 mm wide and 2100 mm high, starting at the floor and centred
along the wall's length, cut through the full thickness as an IFC opening that voids the wall.

Bounds: 5000·200·3000 − 900·200·2100 = 2.622e9 mm³ (band ±1 %, no curved faces); envelope = the element's
extents with 1 mm margin. Scored on the STL that `bench/ifc_to_stl.py` tessellates from the
agent's IFC; a reference built with the IfcOpenShell API lands exactly on the volume.
