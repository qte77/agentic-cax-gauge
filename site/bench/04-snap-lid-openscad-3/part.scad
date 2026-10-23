// Snap-fit lid for 50x30 box, 1.5 mm walls, PETG. Z up, lid top faces up.
// Assumptions: box inner = 47x27; box has a small matching groove/undercut
// 2.5 mm below its top edge on the long inner walls for the hooks to catch.
plate_t   = 2;      // top plate thickness
overhang  = 1;      // plate overhang per side -> 52x32
clr       = 0.2;    // clearance per side between rim and box inner wall
rim_t     = 1.2;    // rim wall thickness
rim_h     = 4;      // rim depth below plate
hook_w    = 12;     // hook tab width
slot      = 0.8;    // relief slot each side of hook tab
barb      = 0.6;    // barb protrusion
hook_x    = 12;     // hook centres at x = +-12
ox = 47 - 2*clr;  oy = 27 - 2*clr;   // rim outer 46.6 x 26.6
z0 = 1;             // rim bottom; plate underside at z = z0+rim_h = 5

module rim() {
  difference() {
    translate([-ox/2,-oy/2,z0]) cube([ox,oy,rim_h+0.01]);
    translate([-ox/2+rim_t,-oy/2+rim_t,z0-1]) cube([ox-2*rim_t,oy-2*rim_t,rim_h+2]);
    // relief slots around hook tabs
    for (sx=[-1,1], sy=[-1,1], d=[-1,1])
      translate([sx*hook_x + d*(hook_w/2+slot/2) - slot/2, sy*(oy/2-rim_t/2) - 1.5, z0-1])
        cube([slot,3,rim_h+1]);
  }
}
module hook(sy) {
  translate([0,sy*(oy/2),0]) mirror([0,sy<0?1:0,0]) {
    // tab, extends down below the rim
    translate([-hook_w/2,-rim_t,0]) cube([hook_w,rim_t,z0+rim_h]);
    // barb: flat catch face at z=2.5 (2.5 below box top), ramp for lead-in
    rotate([90,0,90]) translate([0,0,-hook_w/2])
      linear_extrude(hook_w) polygon([[-0.01,2.5],[barb,2.5],[-0.01,0.2]]);
  }
}
union() {
  translate([-(50+2*overhang)/2+0,-(30+2*overhang)/2,z0+rim_h])
    cube([50+2*overhang,30+2*overhang,plate_t]);
  rim();
  for (sx=[-1,1], sy=[-1,1]) translate([sx*hook_x,0,0]) hook(sy);
}
