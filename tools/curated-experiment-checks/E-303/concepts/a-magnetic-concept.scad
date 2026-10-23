// E-303 candidate A: dimensioned force-path concept, NOT printable release.
// mm. Render: openscad -o work/a.csg this-file.scad
// show_section=true exposes pole gaps; explode separates assemblies.
// Thread envelope deliberately labelled: actual E-295 profile stays authoritative.
$fn=72;
show_section=true;
explode=0;
washer_od=9; washer_id=3.2; washer_t=.8;
pole_spacing=5.6; pole_tip_z=12.3; face_z=12.4;
input_od=10; input_id=8; housing_od=12.4;
beam_t=.24; beam_w=.6; shaft_d=2.6;
assert(face_z-pole_tip_z>=.1-1e-9);
assert(pole_spacing>3.8); // separated coil envelopes
assert(pole_spacing/2+1 < input_id/2); // poles clear rotating annulus
assert(housing_od>10.16); // expressly NOT four-height grid compatible
module annulus(od,id,h){difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
module ring_at(z,od,id,h){translate([0,0,z])annulus(od,id,h);}
module section(){if(show_section)difference(){children();translate([-20,-20,-2])cube([40,20,60]);}else children();}
module steel_parts(){
  // Standard 9x3.2x0.8 yoke, unmodified. Inverted M2 heads touch its top.
  color("slategray")ring_at(1.5,washer_od,washer_id,washer_t);
  for(x=[-pole_spacing/2,pole_spacing/2])translate([x,0,0]){
    color("gray")translate([0,0,2.3])difference(){cylinder(d=3.8,h=2);translate([0,0,-.01])cylinder(d=1.7,h=.8,$fn=6);}
    color("gray")translate([0,0,4.3])cylinder(d=2,h=8); // thread envelope; magnetic model uses root area
    color("tan")translate([0,0,4.5])annulus(2.4,2.1,4);
    color("peru")translate([0,0,4.5])annulus(3.8,2.4,4); // 80 turns, wire0.10; not solid copper
  }
}
module input(){color("sienna")union(){ring_at(11.4,input_od,input_id,1);ring_at(11.4,11,input_id,.3);}}
module output(){
  color("silver")ring_at(face_z,washer_od,washer_id,washer_t);
  color("royalblue")union(){
    translate([0,0,13.35])cylinder(d=shaft_d,h=5.95);
    translate([0,0,13.35])cylinder(d=3.2,h=beam_t);
    ring_at(13.2,9,8.2,.15+beam_t); // outer stand-off leaves .15 below free beams
    for(a=[0:90:270])rotate([0,0,a])translate([1.5,-beam_w/2,13.35])cube([2.8,beam_w,beam_t]);
    translate([0,0,16.4])cylinder(d=4.4,h=1.2);
    // Screw envelope only. See reused E-295 thread-kernel.scad for functional90deg thread.
    translate([0,0,19.3])cylinder(d=3.2,h=16);
  }
}
module fixed_support(){
 // Sectional envelope for TWO mating support/keeper halves. Not release CAD.
 // Main two radial lands, lower/upper output collar thrust lands, input bearing,
 // lower yoke seat and pole-head keeper are shown explicitly.
 color([.3,.65,.55,.5])difference(){ union(){
  ring_at(.5,housing_od,3.2,1);
  ring_at(1.5,housing_od,11.5,18.6);
  ring_at(10.4,housing_od,10.4,1); // input thrust land top11.4
  ring_at(11.85,housing_od,10.4,.5); // input flange upper capture clearance.15
  ring_at(15.4,housing_od,2.9,.99); // output collar lowerface16.4, .01gap
  ring_at(17.61,housing_od,2.9,1.49); // upperface17.6,.01gap
  for(x=[-pole_spacing/2,pole_spacing/2])translate([x,0,4.3])annulus(4.4,2.2,.19); // head keeper
  for(a=[0,180])rotate([0,0,a])translate([4.8,-.5,4.3])cube([1.1,1,.19]); // keeper-to-shell webs
 }
 translate([-1,4.8,11.75])cube([2,2.2,.8]); // radial access to OD10 input rim, outside section plane
 }
}
section(){steel_parts();translate([0,0,explode])input();translate([0,0,2*explode])output();fixed_support();}
// A terrain pin is not included in this clutch concept render. Its 4.4mm square
// body, 6mm internal thread and fixed antirotation guides remain E-295 geometry.
// Closure shimming, carrier creep, actual contact pressure, shaft fit and magnetic
// leakage have not been verified. Do not export these envelopes for owner printing.
