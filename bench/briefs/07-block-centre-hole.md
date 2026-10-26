---
envelope: 61,41,21
volume_band: 45051,46196
---

# Brief: block with a centred through hole

A rectangular block 60 mm long (X), 40 mm wide (Y) and 20 mm tall (Z). A round hole
12 mm in diameter goes vertically through the full height, centred on the top face.

Bounds: 60·40·20 − π·6²·20 = 45738.1 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`03-box-through-hole`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/03-box-through-hole), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
