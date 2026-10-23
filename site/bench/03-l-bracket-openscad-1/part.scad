$fn=48;
difference(){
  union(){
    cube([40,30,5]);        // base
    cube([40,5,30]);        // upright at Y=0 edge, 30 tall overall
  }
  for(x=[8,32]) translate([x,20,-1]) cylinder(d=5,h=7);
}
