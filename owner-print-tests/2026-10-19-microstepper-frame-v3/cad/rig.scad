// E-302 v3: dimensions mm; assembly Z measured from frame bottom.
// scripts/generate.py unions the exact E-301 thread mesh with rotor-base.
// assembly imports that final generated mesh, including its thread.
part="front";
shim=.60;
$fn=96;
module bore(){difference(){circle(d=2.5);for(a=[0,120,240])rotate(a)translate([1.55,0])circle(r=.5);}}
module rotor(){
 difference(){
  union(){
   translate([0,0,12.2])cylinder(d=7,h=12);

  }
  translate([0,0,12.19])linear_extrude(6.01)bore();
  translate([0,0,12.19])cylinder(d1=2.9,d2=1.9,h=.51);
 }
}
module peg(){rotate([90,0,0]){cylinder(d=3,h=2.3);translate([0,0,2.3])cylinder(d1=3,d2=2.5,h=.5);}}
module half(front=true){
 difference(){
  union(){
   translate([-16,0,0])cube([32,6.5,2]);
   for(x=[-13,10])translate([x,0,2])cube([3,6.5,38]);
   translate([-7,0,2])cube([14,6.5,8.5]);
   translate([-13,0,10.5])cube([26,6.5,1.45]);
   translate([-13,0,20.5])cube([26,6.5,3.7]);
   translate([-13,0,24.5])cube([26,6.5,2]);
   translate([-5,0,32])cube([10,6.5,8]);
   translate([-13,0,38])cube([26,6.5,2]);
   for(p=[[-11.5,6],[11.5,29]])translate([p[0]-3,0,p[1]-3])cube([6,6.5,6]);
  }
  translate([0,0,2])cylinder(d=8.2,h=8.5);
  translate([0,0,9.2])cylinder(d=11.5,h=1.1);
  // Open PCB/4-wire side; unchanged known envelope, still unmeasured.
  translate([-8,-.01,2])cube([5.5,3.51,8.5]);
  // Gear/boss clearance through thin thrust deck; ring ID3.2 bridges this hole.
  translate([0,0,10.49])cylinder(d=4,h=1.47);
  translate([0,0,11.7])cylinder(d=7.3,h=.3);
  translate([0,0,20.49])cylinder(d=7.4,h=3.72);
  translate([0,0,24.49])cylinder(d=4.2,h=2.02);
  translate([-2.4,-.01,31.99])cube([4.8,2.41,8.02]);
  // Shim recess with broad removable tab, away from PCB and split stops.
  translate([3.5,-.01,3])cube([1.2,1.2,5]);
  translate([3.5,-.01,7])cube([3.3,2.2,1.25]);
  for(z=[15,35])translate([-14,5.9,z])cube([28,1,2.4]);
  if(!front)for(p=[[-11.5,6],[11.5,29]])
   translate([p[0],-.01,p[1]])rotate([-90,0,0])
    hull(){for(dx=(p[1]>20?[-.35,.35]:[0]))translate([dx,0,0])cylinder(d=3.5,h=3.2);}
 }
 if(front)for(p=[[-11.5,6],[11.5,29]])translate([p[0],0,p[1]])peg();
}
// Shim flat face against pocket at X4.7; thickness .60/.72/.84.
module spacer(t){union(){cube([t,2,5]);translate([0,-1,4])cube([t+1.2,4,1]);}}
if(part=="front"||part=="back")translate([0,0,6.5])rotate([-90,0,0])half(part=="front");
if(part=="rotor-base")translate([0,0,-12.2])rotor();
if(part=="pin")import("../../2026-10-18-microstepper-frame-v2/components/pin-18.stl");
if(part=="spacer")rotate([0,-90,0])translate([-shim-1.2,0,0])spacer(shim);
if(part=="assembly"){half(true);mirror([0,1,0])half(false);translate([0,0,12.2])import("../components/rotor.stl");}
