$fn=48;
// Base plate X40 Y30 Z5; upright at Y0..5 up to Z30.
// Holes: centre line Y=15, offset +5 away from upright -> Y=20; X=20+-12.
difference(){
  union(){
    cube([40,30,5]);
    cube([40,5,30]);
  }
  for(x=[8,32]) translate([x,20,-1]) cylinder(d=5,h=7);
}
