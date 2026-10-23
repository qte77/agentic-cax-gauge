// Plate 40x40x5 centred in XY, base at z=0; boss d10, 8 mm tall on top (overlaps slightly for union)
$fn=96;
union(){
  translate([-20,-20,0]) cube([40,40,5]);
  cylinder(d=10,h=13);
}
