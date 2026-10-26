---
envelope: 31,31,51
volume_band: 34812,35697
---

# Brief: plain cylinder

A solid cylinder 30 mm in diameter and 50 mm tall, standing on its base (Z up).

Bounds: π·15²·50 = 35342.9 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`02-cylinder`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/02-cylinder), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
