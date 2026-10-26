---
envelope: 91,71,6
volume_band: 29356,30102
---

# Brief: plate with a grid of holes

A flat plate 90 mm long (X), 70 mm wide (Y) and 5 mm thick (Z). Twelve round through
holes, each 6 mm in diameter, in a grid of 4 columns × 3 rows: column centres at
X = 15, 35, 55, 75 mm and row centres at Y = 15, 35, 55 mm, measured from one corner.

Bounds: 90·70·5 − 12·π·3²·5 = 29803.5 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`10-rect-pattern-holes`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/10-rect-pattern-holes), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
