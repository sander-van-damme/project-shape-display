// E-295 conditional 2x2 screw demo. Millimetres. Not a physically proven rig.
// Reuse exactly the compact coupon thread; see ../2026-10-15-compact-screw-fit/thread-kernel.scad.
include <../2026-10-15-compact-screw-fit/thread-kernel.scad>
part="plate";
relief=.175;
pitch=5.08;
guide_width=4.60;
$fn=64;
module centers() { for(x=[-pitch/2,pitch/2]) for(y=[-pitch/2,pitch/2]) translate([x,y,0]) children(); }
module hexagon(af,h) { cylinder(d=af/cos(30),h=h,$fn=6); }
module screw() {
    difference() {
        union() {
            cylinder(d=4.4,h=3.6);
            translate([0,0,3.59]) cylinder(d=3.2,h=1.92);
            translate([0,0,5.5]) intersection() {
                compact_thread(d=3.2,l=16);
                union() {
                    cylinder(d=3.3,h=15.4);
                    translate([0,0,15.4]) cylinder(d1=3.3,d2=1.4,h=.6);
                }
            }
        }
        translate([0,0,-.01]) hexagon(2.2,2.41);
        translate([0,0,-.01]) cylinder(d1=3.0/cos(30),d2=2.2/cos(30),h=.41,$fn=6);
    }
}
module pin() {
    // Short 6 mm female thread, hollow 11.2 mm, flat square 0.8 mm cap.
    union() {
        compact_pin_body(relief=relief,height=17.2,engagement=6);
        translate([-2.2,-2.2,17.19]) cube([4.4,4.4,.81]);
    }
}
module base() {
    difference() {
        translate([-12,-12,0]) cube([24,24,5.1]);
        // Common cavity: no thin walls replicated between the four rotors.
        translate([-7,-7,1.2]) cube([14,14,4]);
        centers() translate([0,0,-.1]) cylinder(d=3.6,h=1.4);
    }
    for(x=[-9.5,9.5]) for(y=[-9.5,9.5]) translate([x,y,5.09]) cylinder(d=2.6,h=1.41);
}
module guide_plate(z) {
    difference() {
        translate([-12,-12,z]) cube([24,24,1.2]);
        centers() translate([-guide_width/2,-guide_width/2,z-.1]) cube([guide_width,guide_width,1.4]);
    }
}
module cage() {
    union() {
        difference() {
            translate([-12,-12,5.1]) cube([24,24,1.6]);
            centers() translate([0,0,5]) cylinder(d=3.5,h=1.8);
            for(x=[-9.5,9.5]) for(y=[-9.5,9.5]) translate([x,y,5]) cylinder(d=2.95,h=1.8);
        }
        for(x=[-12,10.4]) translate([x,-12,6.69]) cube([1.6,24,18.71]);
        guide_plate(14);
        guide_plate(24.2);
    }
}
module print_cage() {
    // Old X becomes print Z; one whole sidewall is the bed anchor.
    translate([0,0,12]) rotate([0,-90,0]) translate([0,0,-5.1]) cage();
}
module driver() {
    // Only the long 2 AF tip enters the grid; the broad grip stays 6 mm below it.
    difference() {
        cylinder(d=12,h=2);
        translate([3,-.5,1.3]) cube([4,1,1]); // visible turn-count notch
    }
    translate([0,0,1.99]) cylinder(d1=6,d2=3,h=2.01);
    translate([0,0,3.99]) cylinder(d=3,h=4.01);
    translate([0,0,7.99]) hexagon(2.0,5.61);
    translate([0,0,13.59]) cylinder(d1=2/cos(30),d2=1.6/cos(30),h=.41,$fn=6);
}
module neutral_gauge() { cube([24,4,3.3]); }
module plate() {
    translate([13,13,0]) base();
    translate([51,13,0]) print_cage();
    for(i=[0:3]) translate([8+i*10,39,0]) screw();
    for(i=[0:3]) translate([8+i*10,52,0]) pin();
    translate([55,48,0]) driver();
    translate([2,62,0]) neutral_gauge();
}
module assembly() {
    color("silver") base();
    color("lightblue",.6) cage();
    centers() {
        color("orange") translate([0,0,1.2]) rotate([0,0,240]) screw();
        color("ivory") translate([0,0,10.7]) rotate([0,0,0]) pin();
    }
}
if(part=="plate") plate();
if(part=="base") base();
if(part=="cage") print_cage();
if(part=="cage-assembled") cage();
if(part=="screw") screw();
if(part=="pin") pin();
if(part=="driver") driver();
if(part=="assembly") assembly();
if(part=="gauge") neutral_gauge();
