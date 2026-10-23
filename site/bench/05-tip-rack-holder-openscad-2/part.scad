// Pipette rack tray. Origin at the corner-centered footprint, base bottom at z=0.
// Assumption: wall stands on top of the 3 mm base (total height 13 mm).
base_t = 3;
wall_t = 2;
wall_h = 10;
in_x = 123;
in_y = 81;
out_x = in_x + 2*wall_t; // 127
out_y = in_y + 2*wall_t; // 85

union() {
    translate([-out_x/2, -out_y/2, 0]) cube([out_x, out_y, base_t]);
    translate([0, 0, base_t])
        difference() {
            translate([-out_x/2, -out_y/2, 0]) cube([out_x, out_y, wall_h]);
            translate([-in_x/2, -in_y/2, -0.01]) cube([in_x, in_y, wall_h + 0.02]);
        }
}
