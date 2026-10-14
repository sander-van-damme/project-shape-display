// E-277 manufacturing discriminator; not a qualified owner print.
include <BOSL2/std.scad>
use <slicing.scad>
$fn=64;
$slop=0;
part="channel";
// World axis +Z. One side open; square convex hull retained at each section.
module channel() {
    difference() {
        translate([-5.15,-5.15,10]) cube([10.3,10.3,126]);
        translate([-5.16,-4.35,9.99]) cube([9.51,8.7,124.01]);
    }
}
if(part=="channel") translate([-10,5.15,5.15]) rotate([0,90,0]) channel();
if(part=="nut") translate([5.15,5.15,0]) intersection() {
    body(false);
    translate([-6,-6,0]) cube([12,12,10]);
}
