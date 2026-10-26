---
envelope: 51,41,31
volume_band: 15803,16205
---

# Brief: box open at the top and the front

A box 50 mm long (X), 40 mm deep (Y) and 30 mm tall (Z) outside, open at the top and at
the front (the face at the lowest Y). The floor, back wall and two side walls are each
3 mm thick.

Bounds: 50·40·30 − 44·37·27 = 16044.0 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`46-shell-two-open-faces`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/46-shell-two-open-faces), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
