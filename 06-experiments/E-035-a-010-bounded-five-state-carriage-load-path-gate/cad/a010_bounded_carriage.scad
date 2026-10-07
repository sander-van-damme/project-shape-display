// Bounded A-010: gate selects a state; a guided vertical carriage follows it.
// Geometry evidence only; all dimensions are mm.
$fn = 48;
pitch=5.08; field=30.48; follower_d=1.20; gate_window=3.00;
stop_bore=1.60; shoulder_d=3.00;
states=[0,0.80,1.60,2.40,3.20];

module plate(z,t,c="lightgray") { color(c) translate([-field/2,-field/2,z]) cube([field,field,t]); }
module lower_guide() {
  difference() { plate(0,0.40,"silver");
    for (x=[-2:2]) for (y=[-2:2]) translate([x*pitch-2.25,y*pitch-2.45,-.01]) cube([4.50,4.90,.42]); }
}
module upper_guide() {
  difference() { plate(.80,.40,"silver");
    for (x=[-2:2]) for (y=[-2:2]) translate([x*pitch-2.25,y*pitch-2.45,.79]) cube([4.50,4.90,.42]); }
}
module gate_slider() {
  // S2 is shown; five apertures are vertically indexed at .80 pitch.
  difference() { color("orange") translate([-2.30,-field/2,.40]) cube([4.60,field,.40]);
    translate([0,0,1.99]) cube([gate_window,gate_window,.44],center=true); }
}
module indexed_stop_plate() {
  // Five dedicated vertical stop identities; the selected shoulder lands on one.
  difference() { plate(1.20,.80,"lightblue");
    for (z=states) translate([0,0,1.19+z]) cube([stop_bore,stop_bore,.82],center=true); }
}
module carriage_and_follower(z=1.60) {
  color("green") translate([-2,-2,.78+z]) cube([4,4,.42]);
  color("purple") translate([0,0,1.20+z]) cylinder(d=follower_d,h=2.00);
  color("purple") translate([0,0,2.00+z]) cylinder(d=shoulder_d,h=.35);
}
module actuator_path() {
  // Bidirectional writer tongue path: 3.20 indexed travel + .20 approach.
  color("red") translate([-.50,-2,.40]) cube([1,4,.80]);
  color("red") translate([-.70,-2,.30]) cube([1.40,.60,1.00]);
}
lower_guide(); gate_slider(); upper_guide(); indexed_stop_plate();
// Transparent overlays expose the follower/shoulder envelope for every state;
// the opaque S2 instance above is the nominal section used for the load path.
for (z=states) color([0,1,0,0.18]) carriage_and_follower(z);
carriage_and_follower(1.60); actuator_path();
for (z=states) color("black") translate([-5.8,0,2.0+z]) cube([.5,.08,.08]);
