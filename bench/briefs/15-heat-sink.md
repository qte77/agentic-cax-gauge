---
envelope: 61,51,31
volume_band: 42478,43557
---

# Brief: finned heat sink

A heat sink: a base plate 60 mm long (X), 50 mm wide (Y) and 5 mm thick. On top, fifteen
straight fins run the full 50 mm along Y; each fin is 1.5 mm thick (X) and 25 mm tall,
so the part is 30 mm tall overall. The fins are 4 mm apart centre-to-centre, the first
one starting 2 mm in from the base's edge at X = 0. Base and fins are one solid.

Bounds: 60·50·5 + 15·1.5·50·25 = 43125.0 mm³ (band −1.5 % / +1 %, the low side allowing for default
curve tessellation); envelope = the part's extents with 1 mm margin. Idea from SolidCraft's
analytic reference case [`62-heat-sink`](https://github.com/tangency-labs/solidcraft/tree/4ced1d7bcfbb3bd40c557d4c68cf583ac22f2767/tests/oracle/62-heat-sink), MIT OR Apache-2.0; brief written and volume
recomputed here, confirmed against a fine OpenSCAD reference mesh (within 0.05 %).
