---
envelope: 6001,4001,251
volume_band: 5940000000,6060000000
---

# Brief: floor slab

A rectangular floor slab, modelled as one IFC slab element: 6000 mm long (X), 4000 mm
wide (Y) and 250 mm thick, its underside at Z = 0.

Bounds: 6000·4000·250 = 6.000e9 mm³ (band ±1 %, no curved faces); envelope = the element's
extents with 1 mm margin. Scored on the STL that `bench/ifc_to_stl.py` tessellates from the
agent's IFC. (The wall briefs' references were built and measured; this slab's was not.)
