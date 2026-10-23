// Assumption: plate centred on XY origin, bottom at Z=0.
$fn = 64;
union() {
    translate([-20, -20, 0]) cube([40, 40, 5]);
    translate([0, 0, 5]) cylinder(d = 10, h = 8);
}
