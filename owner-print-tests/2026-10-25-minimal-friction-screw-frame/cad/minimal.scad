// Millimetres. L motor; the existing C radial profile and motor envelopes are preserved.
// Build script joins an unchanged historical thread mesh. No library download required.
part="front";
$fn=96;
rotor_z=12.9; body_h=3.6; flange_h=1.2; hub_d=4;
guide_open=4.8; guide_z=[36,56]; guide_h=2;
module c_bore(){difference(){circle(d=2.5);for(a=[0,120,240])rotate(a)translate([1.55,0])circle(r=.5);}}
module rotor_base(){difference(){
 union(){cylinder(d=7,h=flange_h);cylinder(d=hub_d,h=body_h);}
 translate([0,0,-.01])linear_extrude(2.41)c_bore();
 translate([0,0,-.01])cylinder(d1=2.9,d2=1.9,h=.26);
}}
module peg(){rotate([90,0,0]){cylinder(d=3,h=2.3);translate([0,0,2.3])cylinder(d1=3,d2=2.5,h=.5);}}
peg_pts=[[-11.5,6],[9.5,37],[9.5,57]];
module half(front=true){
 difference(){
  union(){
   translate([-16,0,0])cube([32,6.5,2]);
   for(x=[-13,10])translate([x,0,2])cube([3,6.5,14]);
   translate([-7,0,2])cube([14,6.5,9.4]);
   translate([-13,0,11.4])cube([26,6.5,1.25]);
   // One compact upper thrust stop; last 0.6 mm is a loose emergency radial land.
   translate([-13,0,14.4])cube([26,6.5,1.6]);
   // Rigid rails, relieved between two short guide stations; hard split faces.
   translate([8.5,0,16])cube([2.5,6.5,42]);
   for(z=guide_z)translate([-4.2,0,z])cube([16.5,6.5,guide_h]);
   for(p=peg_pts)translate([p[0]-2.8,0,p[1]-3])cube([5.6,6.5,6]);
  }
  // Exact successful v3 cavity, tab allowance, PCB/glue/wire and shim slots.
  translate([0,0,2])cylinder(d=8.4,h=9.41);
  translate([0,0,10])cylinder(d=11.5,h=1.41);
  translate([-9,-.01,2])cube([6.5,4.26,8.01]);
  translate([-9,-.01,2])cube([4.8,4.26,60]);
  translate([0,0,11.39])cylinder(d=4,h=1.31);
  translate([0,0,12.4])cylinder(d=7.3,h=.3);
  translate([0,0,14.39])cylinder(d=5,h=1.02);
  translate([0,0,15.4])cylinder(d=4.4,h=.61);
  for(z=guide_z)translate([-guide_open/2,-.01,z-.01])cube([guide_open,guide_open/2+.01,guide_h+.02]);
  translate([3.5,-.01,3])cube([1.2,1.2,5]);
  translate([3.5,-.01,7])cube([3.3,2.2,1.25]);
  for(z=[7,36,56])translate([-15,5.9,z])cube([30,1,1.2]);
  if(!front)for(p=peg_pts)translate([p[0],-.01,p[1]])rotate([-90,0,0])
   hull(){for(dx=p[1]>10?[-.2,.2]:[0])translate([dx,0,0])cylinder(d=3.5,h=3.2);}
 }
 if(front)for(p=peg_pts)translate([p[0],0,p[1]])peg();
}
module printable_half(front=true){if(front)half(true);else mirror([1,0,0])half(false);}
// Only two 0.24-mm contact necks per side. Clip at neck; don't twist the tower.
// They brace the 27-mm screw and do NOT touch the internal thread of a pin.
module screw_tower(side){mirror([side<0?1:0,0,0]){
 translate([5.5,-2,0])cube([3,4,.48]);
 translate([6,-1,0])cube([2,2,27.2]);
 for(i=[0:1]){
  z=(side>0?12.6:11.16)+12*i;
  hull(){translate([6.2,-.4,z-4.5])cube([.8,.8,.6]);translate([2.1,-.4,z-.48])cube([.3,.8,.6]);}
  translate([1.35,-.225,z-.12])cube([.95,.45,.24]);
 }
}}
if(part=="front"||part=="back")translate([0,0,6.5])rotate([-90,0,0])printable_half(part=="front");
if(part=="rotor-base")rotor_base();
if(part=="rotor-supported")union(){import("../components/A-screw.stl");screw_tower(1);screw_tower(-1);}
// A small guide coupon separates print-orientation effects from the motor assembly.
if(part=="guide-coupon")difference(){cube([10,12,4.5]);translate([2.6,-.01,2.1])cube([4.8,12.02,2.41]);}
