---
envelope: 41,31,21
volume_band: 23374,23968
---

# Brief: block with chamfered top edges

A rectangular block 40 mm long (X), 30 mm wide (Y) and 20 mm tall (Z). The four edges
of the top face have a 2 mm × 45° chamfer; the vertical edges and bottom edges stay sharp.

Bounds: 40·30·18 + ∫₀² (36+2u)(26+2u) du = 23730.7 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`08-chamfer`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/08-chamfer), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
