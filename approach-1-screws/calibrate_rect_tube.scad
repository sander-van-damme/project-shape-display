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
* Draw tube
*/


rect_tube(size=4, wall=1, h=10);

translate([10,0,0])
rect_tube(size=4, wall=0.84, h=10);

translate([20,0,0])
rect_tube(size=4, wall=0.43, h=10);