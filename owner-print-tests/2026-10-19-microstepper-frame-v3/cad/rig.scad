// E-302 v3 measured-interface correction, 20 October. Units mm.
// L motor only. Handed halves and 18–50 mm pin guide. See verification.md.
part="front";
shim=.60;
$fn=96;
motor_base=2;
motor_h=9.2;
motor_top=motor_base+motor_h;
motor_seat_d=8.4; // 8.2 drawing maximum + 0.2 diametral print allowance
flange_clear_d=11.5; // space allowance, NOT a measured flange diameter
flange_bottom=motor_top-1.2;
deck_bottom=motor_top+.2;
ring_bottom=deck_bottom+1.0; // explicit minimum 1 mm load-bearing deck
ring_t=.50;
rotor_z=ring_bottom+ring_t; // 12.9; NOT motor_h correction blindly added
upper_shift=rotor_z-12.2;
lead_in=.25; // was .50: extend straight engagement, keep proven radial C profile
max_pin_length=50;
guide_extension=max_pin_length-18;
guide_top=40+upper_shift+guide_extension;
assert(max_pin_length>=18 && max_pin_length<=50);
pcb_half_width=4.25; // measured <=7 plus 1.5 mm total allowance
module bore(){difference(){circle(d=2.5);for(a=[0,120,240])rotate(a)translate([1.55,0])circle(r=.5);}}
module rotor(){
 difference(){
  translate([0,0,rotor_z])cylinder(d=7,h=12);
  translate([0,0,rotor_z-.01])linear_extrude(6.01)bore();
  translate([0,0,rotor_z-.01])cylinder(d1=2.9,d2=1.9,h=lead_in+.01);
 }
}
module peg(){rotate([90,0,0]){cylinder(d=3,h=2.3);translate([0,0,2.3])cylinder(d1=3,d2=2.5,h=.5);}}
module half(front=true){
 difference(){
  union(){
   translate([-16,0,0])cube([32,6.5,2]);
   for(x=[-13,10])translate([x,0,2])cube([3,6.5,38+upper_shift]);
   translate([-7,0,2])cube([14,6.5,deck_bottom-2]);
   translate([-13,0,deck_bottom])cube([26,6.5,ring_bottom+.25-deck_bottom]);
   translate([-13,0,20.5+upper_shift])cube([26,6.5,3.7]);
   translate([-13,0,24.5+upper_shift])cube([26,6.5,2]);
   translate([-5,0,32+upper_shift])cube([10,6.5,8+guide_extension]);
   translate([-13,0,38+upper_shift])cube([26,6.5,2]);
   for(p=[[-11.5,6],[11.5,29+upper_shift]])translate([p[0]-3,0,p[1]-3])cube([6,6.5,6]);
  }
  translate([0,0,motor_base])cylinder(d=motor_seat_d,h=deck_bottom-motor_base+.01);
  // Envelope clears both top lip orientations; no invented exact lip contour.
  translate([0,0,flange_bottom])cylinder(d=flange_clear_d,h=deck_bottom-flange_bottom+.01);
  // Open left channel for PCB, glue below it and upward cables, full frame height.
  translate([-9,-.01,motor_base])cube([6.5,pcb_half_width+.01,flange_bottom-motor_base+.01]);
  // Above PCB, route cables outside X=-4.2: clear of ring and rotor.
  translate([-9,-.01,motor_base])cube([4.8,pcb_half_width+.01,guide_top+2]);
  translate([0,0,deck_bottom-.01])cylinder(d=4,h=ring_bottom+.3-deck_bottom);
  translate([0,0,ring_bottom])cylinder(d=7.3,h=.3);
  translate([0,0,20.49+upper_shift])cylinder(d=7.4,h=3.72);
  translate([0,0,24.49+upper_shift])cylinder(d=4.2,h=2.02);
  translate([-2.4,-.01,31.99+upper_shift])cube([4.8,2.41,8.02+guide_extension]);
  translate([3.5,-.01,3])cube([1.2,1.2,5]);
  translate([3.5,-.01,7])cube([3.3,2.2,1.25]);
  for(z=[15+upper_shift,35+upper_shift,guide_top-5])translate([-14,5.9,z])cube([28,1,2.4]);
  if(!front)for(p=[[-11.5,6],[11.5,29+upper_shift]])
   translate([p[0],-.01,p[1]])rotate([-90,0,0])
    hull(){for(dx=(p[1]>20?[-.35,.35]:[0]))translate([dx,0,0])cylinder(d=3.5,h=3.2);}
 }
 if(front)for(p=[[-11.5,6],[11.5,29+upper_shift]])translate([p[0],0,p[1]])peg();
}
module spacer(t){union(){cube([t,2,5]);translate([0,-1,4])cube([t+1.2,4,1]);}}
// The back print must have opposite X handedness. Assembly uses rotations only.
module printable_half(front=true){
 if(front)half(true);else mirror([1,0,0])half(false);
}
if(part=="front"||part=="back")translate([0,0,6.5])rotate([-90,0,0])printable_half(part=="front");
if(part=="rotor-base")translate([0,0,-rotor_z])rotor();
if(part=="pin-50")import("../../2026-10-18-microstepper-frame-v2/components/pin-50.stl");
if(part=="pin")import("../../2026-10-18-microstepper-frame-v2/components/pin-18.stl");
if(part=="spacer")rotate([0,-90,0])translate([-shim-1.2,0,0])spacer(shim);
if(part=="assembly"){printable_half(true);rotate([0,0,180])printable_half(false);translate([0,0,rotor_z])import("../components/rotor.stl");}
