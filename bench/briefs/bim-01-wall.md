---
envelope: 5001,201,3001
volume_band: 2970000000,3030000000
---

# Brief: straight wall

A straight wall, modelled as one IFC wall element: 5000 mm long (along X), 200 mm thick
(along Y) and 3000 mm tall (Z up), standing on the ground at Z = 0.

Bounds: 5000·200·3000 = 3.000e9 mm³ (band ±1 %, no curved faces); envelope = the element's
extents with 1 mm margin. Scored on the STL that `bench/ifc_to_stl.py` tessellates from the
agent's IFC; a reference built with the IfcOpenShell API lands exactly on the volume.
