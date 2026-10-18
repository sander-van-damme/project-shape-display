// E-302 revision 3, mm. E-301 functional thread and foot retained.
// Source photo dimensions are NOT physical measurements of owner motors.
part="half-front";
pin_height=50;
tip_r=1.00; // A .95, nominal N 1.00, C 1.05; three broad rounded lobes
$fn=96;
body_d=8.30;
pcb_half_width=3.5; // open side envelope, unmeasured PCB: check before closing
socket_bottom=11.2;
socket_top=19.5;
module cradle_half(){
 difference(){
  union(){
   translate([-18,0,0])cube([36,10,2]);
   for(x=[-15,12])translate([x,0,2])cube([3,6.5,42]);
   translate([-7,0,2])cube([14,6.5,8.2]);
   translate([-15,0,20.2])cube([30,3.5,3.5]);
   intersection(){translate([0,0,20.2])cylinder(d=9,h=3.5);translate([-5,0,20])cube([10,5,4]);}
   translate([-15,0,28.9])cube([30,3.5,2.1]);
   translate([-5,0,36])cube([10,4.5,8]);
   translate([-15,3.5,41])cube([30,3,3]);
  }
  translate([0,0,2])cylinder(d=body_d,h=10);
  translate([0,0,9.2])cylinder(d=11.5,h=1.1);
  // Clearance behind transverse flexure; rigid cradle stops frame closure.
  translate([-5,3.5,4.5])cube([10,2.7,4]);
  translate([0,0,19.9])cylinder(d=3.5,h=4.1);
  translate([0,0,28.8])cylinder(d=4.2,h=2.4);
  translate([-2.4,-2.4,35.9])cube([4.8,4.8,8.3]);
  // Keep elastic away from the motor spring and open PCB windows.
  for(z=[21,38])translate([-16,5.9,z])cube([32,2,2.8]);
 }
 // Transverse two-ended flexure: 10 mm bridge, .6 thick, 2.4 axial width.
 // Flat first bridging layer has anchors at both ends; nominal preload .10.
 translate([-5.2,3.9,5])cube([10.4,.6,2.4]);
}
// Cut AFTER adding spring: no spring or wall may cross the PCB envelope.
module frame_half(){
 difference(){
  cradle_half();
  translate([-8,-.01,2])cube([5.5,pcb_half_width+.01,8.5]);
 }
}
module bore_profile(){
 difference(){
  circle(d=2.5);
  // Rounded wall-integrated lobes, not a miniature involute gear.
  for(a=[0,120,240])rotate(a)translate([tip_r+.5,0])circle(r=.5);
 }
}
module cup(){
 difference(){
  union(){
   translate([-6.5,-6.5,24.2])cube([13,13,4.6]);
   translate([0,0,19.7])cylinder(d=3,h=4.51);
   translate([0,0,socket_bottom])cylinder(d=5,h=19.71-socket_bottom);
  }
  translate([-5.2,-5.2,26.2])cube([10.4,10.4,3]);
  translate([0,0,socket_bottom-.01])linear_extrude(socket_top-socket_bottom+.01)bore_profile();
  // Lead-in removes the first .5 mm of full-depth engagement.
  translate([0,0,socket_bottom-.01])cylinder(d1=2.9,d2=1.9,h=.51);
  // 1/2/3 external notches identify A/N/C, away from bearing and square socket.
  for(i=[0:(tip_r<.98?0:tip_r>1.02?2:1)])
   translate([-3+i*3,6.1,27])cube([1,1,2]);
 }
}
if(part=="half-front")rotate([90,0,0])frame_half();
if(part=="half-back")rotate([90,0,0])mirror([1,0,0])frame_half();
if(part=="cup")translate([0,0,28.8])rotate([180,0,0])cup();
if(part=="assembly") {frame_half();mirror([0,1,0])frame_half();cup();}

// Exact supplied E-301 meshes are retained as functional source geometry.
if(part=="screw")import("../2026-10-17-microstepper-screw-pin/screw.stl");
if(part=="pin-18")import("../2026-10-17-microstepper-screw-pin/pin.stl");
if(part=="pin-50")union(){
 import("../2026-10-17-microstepper-screw-pin/pin.stl");
 // Overlap only the straight upper tube; threaded bottom and print foot unchanged.
 translate([0,0,17.9])difference(){
  translate([-2.2,-2.2,0])cube([4.4,4.4,pin_height-17.9]);
  translate([-1.76,-1.76,-.01])cube([3.52,3.52,pin_height-17.8]);
 }
}
