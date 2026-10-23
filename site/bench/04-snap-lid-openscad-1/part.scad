// Snap-fit lid for 50x30 box, 1.5 mm walls (inner 47x27), PETG, FDM.
// Assumptions: box has a small internal catch groove/ledge ~3 mm below top edge
// (box top edge = lid underside, z=0). Lid prints top-down-flat (plate on bed, z up).
plate_x = 52; plate_y = 32; plate_t = 2;   // 1 mm overhang per side
clr = 0.3;                                 // clearance per side to inner wall
rim_x = 47 - 2*clr; rim_y = 27 - 2*clr;    // 46.4 x 26.4
rim_w = 1.2; rim_d = 3;                    // rim wall (3 perimeters @0.4) & depth
arm_len = 5;                               // hook arm length below plate underside
barb = 0.6;                                // barb protrusion (interference w/ clearance)
hook_w = 8; hook_x = 10;                   // hook width, offset from center
slot = 0.8;

module barb2d() { // profile in (y,z), y outward from rim outer face
    polygon([[0,-3],[barb,-3],[barb,-3.4],[0,-4.4]]);
}
union() {
    translate([-plate_x/2,-plate_y/2,0]) cube([plate_x,plate_y,plate_t]);
    difference() {
        union() {
            // rim
            translate([0,0,-rim_d/2+0.01]) difference() {
                cube([rim_x,rim_y,rim_d+0.02],center=true);
                cube([rim_x-2*rim_w,rim_y-2*rim_w,rim_d+1],center=true);
            }
            // hook arms + barbs on both long sides
            for (sx=[-1,1]) for (sy=[-1,1])
                translate([sx*hook_x,sy*rim_y/2,0]) mirror([0,sy<0?1:0,0]) {
                    translate([-hook_w/2,-rim_w,-arm_len]) cube([hook_w,rim_w,arm_len]);
                    translate([hook_w/2,0,0]) rotate([90,0,-90]) linear_extrude(hook_w) translate([0,0]) barb2d();
                }
        }
        // flex slots either side of each arm
        for (sx=[-1,1]) for (sy=[-1,1]) for (e=[-1,1])
            translate([sx*hook_x+e*(hook_w/2+slot/2)-slot/2, sy*rim_y/2-rim_w-0.2, -arm_len-0.01])
                cube([slot,rim_w+0.4,arm_len-1.0]);
    }
}
