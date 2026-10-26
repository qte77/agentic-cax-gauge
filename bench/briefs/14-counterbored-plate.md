---
envelope: 81,51,11
volume_band: 36215,37135
---

# Brief: plate with counterbored holes

A flat plate 80 mm long (X), 50 mm wide (Y) and 10 mm thick (Z). Six counterbored
through holes, opening on the top face: each is a 5.5 mm diameter through hole with a
10 mm diameter counterbore 5.5 mm deep. Hole centres at X = 15, 40, 65 mm and
Y = 15, 35 mm, measured from one corner.

Bounds: 80·50·10 − 6(π·5²·5.5 + π·2.75²·4.5) = 36766.7 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`57-hole-pattern-sketch-points`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/57-hole-pattern-sketch-points), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
