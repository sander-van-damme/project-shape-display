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

cube_width = 4.64;
cube_width_tolerances = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3];
cube_height = 30;
cube_count = 5;

for (i = [0 : len(cube_width_tolerances) - 1]) {
    tolerance = cube_width_tolerances[i];
    width = cube_width + tolerance;
    translate([0, i * cube_width * 2, 0])
    rect_tube(size=width, wall=0.44, h=cube_height);
}


