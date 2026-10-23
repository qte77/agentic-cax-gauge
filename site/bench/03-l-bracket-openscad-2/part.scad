// L-bracket. Assumption: upright at the Y=0 edge; base spans Y 0..30.
// Holes at Y = 15 + 5 = 20 (away from upright), X = 20 +/- 12.
$fn = 48;
difference() {
    union() {
        cube([40, 30, 5]);   // base
        cube([40, 5, 30]);   // upright
    }
    for (x = [8, 32])
        translate([x, 20, -1]) cylinder(d = 5, h = 7);
}
