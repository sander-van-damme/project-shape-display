// E-302, mm. Existing E-301 screw/pin STLs reused without modification.
// Source photo dimensions are NOT physical measurements of owner motors.
part="half";
tip_r=1.00; // A .95, nominal N 1.00, C 1.05; three broad rounded lobes
$fn=96;
body_d=8.30;
pcb_half_width=3.0; // open side envelope, unmeasured PCB: check before closing
socket_bottom=11.2;
socket_top=19.5;
module frame_half(){
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
  // Full-height, outward-open PCB/wire windows on both sides.
  for(x=[-7.1,3])translate([x,-.01,2])cube([4.1,pcb_half_width+.01,8.3]);
  // Clearance behind transverse flexure; rigid cradle stops frame closure.
  translate([-5,3.5,3])cube([10,2.7,6.3]);
  translate([0,0,19.9])cylinder(d=3.5,h=4.1);
  translate([0,0,28.8])cylinder(d=4.2,h=2.4);
  translate([-2.4,-2.4,35.9])cube([4.8,4.8,8.3]);
  // Keep elastic away from the motor spring and open PCB windows.
  for(z=[21,38])translate([-16,5.9,z])cube([32,2,2.8]);
 }
 // Transverse two-ended flexure: 10 mm bridge, .6 thick, 2.4 axial width.
 // Flat first bridging layer has anchors at both ends; nominal preload .10.
 translate([-5.2,3.9,6])cube([10.4,.6,2.4]);
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
if(part=="half")rotate([90,0,0])frame_half();
if(part=="cup")translate([0,0,28.8])rotate([180,0,0])cup();
if(part=="assembly") {frame_half();rotate([0,0,180])frame_half();cup();}
