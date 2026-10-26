---
envelope: 101,101,11
volume_band: 65757,67427
---

# Brief: round flange with a bolt circle

A round flange: a disc 100 mm in diameter and 10 mm thick (Z up) with a central bore
30 mm in diameter. Six through holes, each 10 mm in diameter, are equally spaced on a
circle 80 mm in diameter around the centre.

Bounds: π(50² − 15²)·10 − 6·π·5²·10 = 66758.8 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`11-circular-pattern-flange`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/11-circular-pattern-flange), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
