// E-277 changed manufacturing topology, not owner-ready hardware.
// Preserve the integral body and helical phase; add no fitting/latching features.
include <BOSL2/std.scad>
use <slicing.scad>
use <../E-263/article.scad>
$fn=64;
$slop=0;
part="positive";
module half(side) {
    intersection() {
        body();
        translate([side>0 ? 0 : -6,-6,-1]) cube([6,12,138]);
    }
}
if(part=="positive") translate([0,5.15,5.15]) rotate([0,90,0]) half(1);
if(part=="negative") translate([0,5.15,5.15]) rotate([0,90,0]) rotate([0,0,180]) half(-1);
if(part=="world_positive") half(1);
if(part=="world_negative") half(-1);
if(part=="male") thread(3.2);
