---
envelope: 51,41,31
volume_band: 13427,13769
---

# Brief: open-top box

An open-top box, 50 mm long (X), 40 mm wide (Y) and 30 mm tall (Z) outside, with 2 mm
thick walls and a 2 mm thick floor. The top is open; the inside is a single empty pocket.

Bounds: 50·40·30 − 46·36·28 = 13632.0 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`09-shell`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/09-shell), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
