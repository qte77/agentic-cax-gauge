// Plate 40x40x5 centred in XY, sitting on Z=0; boss d10, 8 mm tall on top.
$fn=64;
union(){
  translate([-20,-20,0]) cube([40,40,5]);
  translate([0,0,4.99]) cylinder(d=10,h=8.01); // slight overlap, top at Z=13
}
