// E-281 short hand-fit coupon; NOT a full-travel display component.
// E-277 paired profile, pinned BOSL2; all dimensions millimetres.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64;
$slop=0;
part="screw";
relief=.15; // radial difference, not a measured printer compensation
label=1;
module thread(d,l) {
    trapezoidal_threaded_rod(d=d,l=l,pitch=3,thread_depth=.9,
        thread_angle=90,starts=1,left_handed=false,bevel=false,
        blunt_start=false,anchor=BOT);
}
module dots(z) {
    for(i=[0:label-1]) translate([-3+i*1.5,4,z-.01]) cylinder(d=.9,h=.41);
}
if(part=="screw") union() {
    // Permanent broad hand grip and bed anchor, no removable supports.
    translate([-7,-7,0]) cube([14,14,3]);
    translate([0,0,2.8]) cylinder(d=1.4,h=.3);
    translate([0,0,3]) intersection() {
        thread(3.2,16);
        union() {
            cylinder(d=3.3,h=15.4);
            translate([0,0,15.4]) cylinder(d1=3.3,d2=1.4,h=.6);
        }
    }
    dots(3);
}
if(part=="nut") union() {
    difference() {
        translate([-5.15,-5.15,0]) cube([10.3,10.3,10]);
        translate([0,0,-3]) thread(3.2+2*relief,16);
    }
    dots(10);
}
