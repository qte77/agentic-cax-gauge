// Pipette rack tray. Assumption: wall's 10 mm stands on top of the 3 mm base (13 mm total).
base_t = 3;
wall_t = 2;
wall_h = 10;
in_x = 123;  // 122 + 0.5 clearance each side
in_y = 81;   // 80 + 0.5 clearance each side
out_x = in_x + 2*wall_t; // 127
out_y = in_y + 2*wall_t; // 85

difference() {
    translate([-out_x/2, -out_y/2, 0]) cube([out_x, out_y, base_t + wall_h]);
    translate([-in_x/2, -in_y/2, base_t]) cube([in_x, in_y, wall_h + 1]);
}
