// DES-003 / Q-009 critical-fit calibration coupon.
// Evidence class: CAD-derived/calculated only; no print or physical validation.
// Render: openscad -o a1_coupon_calibration.stl a1_coupon_calibration.scad
PITCH=5.08; BODY=3.60; CLEAR=0.20; LATCH_T=0.45; LATCH_W=1.20;
TRAVEL=40.0; FLAG_T=0.44; FLAG_W=1.60; FLAG_GAP=1.80;
SLIDE_W=8.0; SLIDE_L=42.0; SLIDE_H=6.0; SLIDE_RAIL=1.20; $fn=32;
OWNED_LANE=PITCH/2-BODY/2; HINGE_X=BODY/2+LATCH_T/2+CLEAR; FLAG_Z=TRAVEL+3.0;

// A: three actual binary-latch stations spanning the nominal clearance band.
module latch_station(c=CLEAR) {
  socket=BODY+2*c;
  difference(){ cube([14,14,3],center=true); translate([0,0,1.55]) cube([socket,socket,.4],center=true); }
  translate([0,0,23]) cube([BODY,BODY,46],center=true);
  translate([HINGE_X,0,1.5]) cube([LATCH_T,LATCH_W,3],center=true);
  for(z=[-TRAVEL/2,TRAVEL/2]) translate([HINGE_X,0,z]) cube([LATCH_T+2*c,LATCH_W+2*c,2],center=true);
  translate([HINGE_X,0,FLAG_Z-.4]) color("Gold") cube([FLAG_T,FLAG_W,.8],center=true);
  translate([HINGE_X,0,FLAG_Z+FLAG_GAP]) color("Orange",.35) cylinder(h=.2,d=FLAG_T+2*FLAG_GAP*tan(15),center=true);
}
module latch_band(){ for(i=[0:2]) translate([i*18-18,0,0]) latch_station(CLEAR+(i-1)*.1); }

// B: five true-pitch registration stations and half-pitch marks.
module registration_span(){
  translate([0,24,1.5]) cube([5*PITCH,8,3],center=true);
  for(i=[0:4]) { x=(i-2)*PITCH; translate([x,24,3.5]) cube([BODY,BODY,4],center=true); translate([x+PITCH/2,24,3.5]) cube([.44,BODY,4],center=true); }
}

// C: two-rail repeated-fit interface; clearance is intentionally adjustable.
module sliding_pair(c=CLEAR){
  difference(){ cube([SLIDE_L,SLIDE_W,SLIDE_H],center=true); for(y=[-SLIDE_W/2+SLIDE_RAIL/2,SLIDE_W/2-SLIDE_RAIL/2]) translate([0,y,0]) cube([SLIDE_L-4,SLIDE_RAIL+2*c,SLIDE_H+.2],center=true); }
  translate([0,0,SLIDE_H/2+1.5]) cube([SLIDE_L-8,SLIDE_W-2*SLIDE_RAIL-2*c,3],center=true);
}
module coupon(){ latch_band(); registration_span(); translate([0,-24,0]) sliding_pair(CLEAR); }
coupon();
echo(str("EVIDENCE=CAD-derived; physical_validation=unresolved"));
echo(str("PITCH=",PITCH," BODY=",BODY," CLEAR=",CLEAR," OWNED_LANE=",OWNED_LANE));
echo(str("LATCH_CLEAR_BAND=",CLEAR-.1,":",CLEAR+.1," FLAG_T=",FLAG_T));
echo(str("READER_FLAG_GAP=",FLAG_GAP," HALF_PITCH=",PITCH/2));
echo(str("SLIDE_CLEAR_BAND=",CLEAR-.1,":",CLEAR+.1," SLIDE_LENGTH=",SLIDE_L));
