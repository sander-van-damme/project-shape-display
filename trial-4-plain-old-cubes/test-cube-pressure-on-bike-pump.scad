/*
* Import the The Belfry OpenScad Library v2.
* - https://github.com/BelfrySCAD/BOSL2/wiki/
* - https://github.com/BelfrySCAD/BOSL2/wiki/threading.scad
* - https://github.com/BelfrySCAD/BOSL2/wiki/constants.scad#constant-slop
*/

include <BOSL2/std.scad>
include <BOSL2/threading.scad>
include <BOSL2/screws.scad>

/*
* Set rendering parameters
*/

$fn = $preview ? 32 : 128;
    
/*
* Draw.
*/
module test_valve(offset=0) {
    translate([0,0,50])
    rect_tube(size=6, wall=0.44 + offset, h=50);
    translate([0,0,50])
    rect_tube(size=6, wall=2, h=5);
    translate([0,0,30])
    tube(h=50, or=3, wall=0.44);
   
}

tolerances = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3];
for (i = [0 : len(tolerances) - 1]) {
    translate([i * 15, 0, 0])
    test_valve(tolerances[i]);    
}


