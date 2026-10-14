// Computational discriminator only: no owner print handoff or qualified fit.
// E-263 cutter preserved verbatim via use; pinned BOSL2 revision in slicing.py.
include <BOSL2/std.scad>
use <../E-263/article.scad>
$fn=64;
$slop=0;
part="integral";
module body(cap=true) {
    difference() {
        translate([-5.15,-5.15,0]) cube([10.3,10.3,cap ? 136 : 134]);
        intersection() {
            thread(3.5,true);
            translate([-6,-6,-.1]) cube([12,12,10.11]);
        }
        translate([-4.35,-4.35,10]) cube([8.7,8.7,cap ? 124 : 125]);
    }
}
// Horizontal longitudinal axis +X, bed face is original +X face.
if(part=="integral") translate([0,5.15,5.15]) rotate([0,90,0]) body();
if(part=="open") translate([0,5.15,5.15]) rotate([0,90,0]) body(false);
if(part=="tube") difference() {
    cube([124,10.3,10.3]);
    translate([-.1,.8,.8]) cube([124.2,8.7,8.7]);
}
// Short nut upright: both mouths accessible; no horizontal-bore overhang.
if(part=="nut") translate([5.15,5.15,0]) intersection() {
    body(false);
    translate([-6,-6,0]) cube([12,12,10]);
}
if(part=="cap") cube([10.3,10.3,2]);
