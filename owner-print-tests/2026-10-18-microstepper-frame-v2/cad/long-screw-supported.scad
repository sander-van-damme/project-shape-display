// Revision 4: upright screw, two sacrificial side towers, eight small contacts.
// All dimensions mm. Functional screw is unchanged; supports are removed.
// Neck is 0.45 mm wide x 0.24 mm high, two 0.12-mm layers, at thread crests.
// Sloping arms rise approximately 45 degrees and join the neck from outside.
module tower(side) {
 mirror([side < 0 ? 1 : 0,0,0]) {
  translate([5.5,-4,0])cube([4,8,.48]);
  translate([6,-1.5,.47])cube([3,3,47.05]);
  for(i=[0:3]) {
   z=(side>0 ? 11.4 : 9.96)+12*i;
   hull() {
    translate([6.2,-.4,z-4.7])cube([.8,.8,.6]);
    translate([2.1,-.4,z-.48])cube([.3,.8,.6]);
   }
   translate([1.4,-.225,z-.12])cube([.85,.45,.24]);
  }
 }
}
union(){
 import("../components/screw-long.stl");
 tower(1);
 tower(-1);
}
