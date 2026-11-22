---
envelope: 81,61,51
volume_band: 33256,34101
volume: 80*60*4 + 80*4*46 - 2*pi*2.5**2*4
---

# Brief: L-shaped wall bracket

An L-shaped wall bracket, 80 mm wide (X). The base plate lies flat: 60 mm deep (Y) and 4 mm
thick (Z). The back plate stands at the back edge of the base: 4 mm thick (Y) and 50 mm tall
overall (Z), so it rises 46 mm above the base. Two 5 mm holes go through the back plate,
40 mm apart, centred across the width, with their centres 35 mm above the bottom.

Bounds: 80·60·4 + 80·4·46 − 2·π·2.5²·4 = 33762.9 mm³ (band −1.5 % / +1 %, the low side allowing for
default curve tessellation); envelope = the part's extents with 1 mm margin. Part and dimensions
from The Stack Underflow's lab [`freecad-mcp-lab`](https://github.com/thestackunderflow/freecad-mcp-lab/tree/e0bd5d9cfe607d372d679b539d73e16c91562c99) (Apache-2.0), which tests the same
bracket at 80 mm and then 100 mm; described and recomputed here in our own words.
