// Integral manufacture comparison, not an owner print or qualified hardware.
include <BOSL2/std.scad>
use <thread_profile.scad>
$fn=64;
$slop=0;
angle=90;
open_side=false;
difference() {
    translate([-5.15,-5.15,0]) cube([10.3,10.3,136]);
    intersection() {
        paired_thread(3.5,true);
        translate([-6,-6,-.1]) cube([12,12,10.1]);
    }
    translate([open_side ? -5.16 : -4.35,-4.35,10])
        cube([open_side ? 9.51 : 8.7,8.7,124]);
}
