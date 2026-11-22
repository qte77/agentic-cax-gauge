---
envelope: 13.4,21,13.4
volume_band: 2063.8,2116.3
volume: 12.4*12.4*20 - pi*3.2**2*20 - 20*(5*6.2 - (2.5*(3.2**2 - 2.5**2)**0.5 + 3.2**2*asin(2.5/3.2)))
---

# Brief: cable clip for a 6 mm cable

A clip that holds a 6 mm round cable. It is a square block, 12.4 mm wide (X) by 12.4 mm tall
(Z), and 20 mm long (Y). A round channel 6.4 mm in diameter (the cable plus 0.4 mm of room)
runs the full length, centred in the square cross-section. From the top face, a slot 5 mm
wide runs the full length down into the channel, so the cable can be pushed in from above.

Bounds: 12.4²·20 − π·3.2²·20 − 20·(5·6.2 − (2.5·√(3.2² − 2.5²) + 3.2²·asin(2.5/3.2))) =
2095.3 mm³ (block, minus the channel, minus the part of the slot above the channel; band
−1.5 % / +1 %, the low side allowing for default curve tessellation); envelope = the part's
extents with 1 mm margin. Part from The Stack Underflow's lab
[`freecad-beginner-lab`](https://github.com/thestackunderflow/freecad-beginner-lab/tree/978ab52a690cbbe11df2a4257f406d1fd06bee4f) (Apache-2.0), whose FreeCAD run measured 2095.31 mm³ and
12.4 × 20 × 12.4 mm at 6 mm; described and recomputed here in our own words. The lab's point
carries over: "valid" from a CAD kernel means one solid, not the size asked for.
