---
envelope: 51,51,21
volume_band: 42287,43361
---

# Brief: block with a hemispherical pocket

A square block 50 × 50 mm and 20 mm tall (Z up). Centred in its top face is a
hemispherical pocket 30 mm in diameter (15 mm deep), as if a ball of that size were
pressed halfway into the top face.

Bounds: 50·50·20 − ⅔·π·15³ = 42931.4 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`14-combine-cut`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/14-combine-cut), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
