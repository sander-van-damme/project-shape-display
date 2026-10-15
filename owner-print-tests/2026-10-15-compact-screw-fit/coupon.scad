// E-295 compact hand-fit coupons. Not a production-length pin qualification.
include <thread-kernel.scad>
part="screw";
relief=.175;
label=1;
foot_height=2.4;

module dots(z,y) {
    for(i=[0:label-1]) translate([-2.6+i*1.3,y,z-.01])
        cylinder(d=.8,h=.49);
}

if(part=="screw") union() {
    translate([-5,-5,0]) cube([10,10,foot_height]);
    translate([0,0,foot_height-.01]) cylinder(d=1.4,h=.02);
    translate([0,0,foot_height]) intersection() {
        compact_thread();
        union() {
            cylinder(d=3.3,h=15.4);
            translate([0,0,15.4]) cylinder(d1=3.3,d2=1.4,h=.6);
        }
    }
    dots(foot_height,3.6);
}

if(part=="pin") union() {
    compact_pin_body(relief=relief);
    // Deliberately modelled OUTSIDE foot, two 0.12 mm layers. No material
    // enters the bore. Leave this hand-test print aid attached during fitting;
    // optional exterior trimming afterwards is a separate handling observation.
    difference() {
        translate([-6,-6,0]) cube([12,12,.24]);
        translate([0,0,-3]) compact_thread(d=3.2+2*relief,l=6);
    }
    dots(.24,4.5);
}
