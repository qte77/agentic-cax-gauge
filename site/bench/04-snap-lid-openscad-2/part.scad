// Snap-fit lid for 50x30 box, 1.5 mm walls, PETG, FDM (0.4 nozzle).
// Assumptions: box inner cavity 47x27; box has a matching shallow 0.5 mm groove
// in the inner wall ~3 mm below the top edge for the hooks to catch.
plate_x = 52; plate_y = 32; plate_t = 2;   // 1 mm overhang each side
clr = 0.2;                                  // clearance per side to inner wall
rim_wall = 1.2; rim_h = 5;                  // locating rim depth below plate
rim_x = 47 - 2*clr; rim_y = 27 - 2*clr;     // 46.6 x 26.6
hook_w = 10; hook_out = 0.6;                // hook width and protrusion
hook_top = 3;                               // catch face 3 mm below plate underside

// plate, top at z=plate_t, underside at z=0
translate([-plate_x/2, -plate_y/2, 0]) cube([plate_x, plate_y, plate_t]);

// rim
translate([0,0,-rim_h])
difference() {
  translate([-rim_x/2, -rim_y/2, 0]) cube([rim_x, rim_y, rim_h + 0.01]);
  translate([-rim_x/2+rim_wall, -rim_y/2+rim_wall, -1])
    cube([rim_x-2*rim_wall, rim_y-2*rim_wall, rim_h+1]);
}

// hooks on both long sides: flat catch face on top, ramp below for lead-in
module hook() {
  translate([0, rim_y/2, 0])
    rotate([90,0,90]) linear_extrude(hook_w, center=true)
      polygon([[-0.3,-hook_top],[hook_out,-hook_top],[0,-rim_h+0.2],[-0.3,-rim_h+0.2]]);
}
hook();
mirror([0,1,0]) hook();
