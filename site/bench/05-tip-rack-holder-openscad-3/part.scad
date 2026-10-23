// Pipette rack tray. Origin at corner of outside; Z up.
// Assumption: wall pocket goes down to the top of the 3 mm base.
base = 3; wall = 2; wall_h = 10;
in_x = 123; in_y = 81;   // rack 122x80 + 0.5 clearance per side
difference() {
    cube([in_x + 2*wall, in_y + 2*wall, base + wall_h]);
    translate([wall, wall, base]) cube([in_x, in_y, wall_h + 1]);
}
