// Integrated 60 mm rotor (12 mm body + 48 mm thread), upright.
// Two sacrificial towers, four small breakaway necks per side.
// Neck: 0.45 wide x 0.24 high; clip individually, do not pull towers.
module tower(side){
 mirror([side<0?1:0,0,0]){
  translate([5.5,-4,0])cube([4,8,.48]);
  translate([6,-1.5,.47])cube([3,3,56.65]);
  for(i=[0:3]){
   z=(side>0?21:19.56)+12*i;
   hull(){
    translate([6.2,-.4,z-4.7])cube([.8,.8,.6]);
    translate([2.1,-.4,z-.48])cube([.3,.8,.6]);
   }
   translate([1.4,-.225,z-.12])cube([.85,.45,.24]);
  }
 }
}
union(){import("../components/rotor-long.stl");tower(1);tower(-1);}
