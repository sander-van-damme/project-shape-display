/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
* - https://github.com/BelfrySCAD/BOSL2/wiki/threading.scad
* - https://github.com/BelfrySCAD/BOSL2/wiki/constants.scad#constant-slop
*/

include <BOSL2/std.scad>
include <BOSL2/threading.scad>


/*
* Set rendering parameters
*/

$fn = $preview ? 32 : 128;
$slop = 0.15;

/*
* Set drawing parameters
*/

length = 50;
width = 8;
side_walls_thickness = 1;
top_wall_thickness = 1;
nut_length = 10;
nut_inner_diameter = 4;
nut_pitch = 2;


/*
* Calculate drawing parameters
*/

top_wall_width = width;
nut_outer_diameter = width;
rectangular_tube_length = length - top_wall_thickness - nut_length;


/*
* Draw
*/


  
trapezoidal_threaded_nut(
    shape="square",
    nutwidth=nut_outer_diameter,
    id=nut_inner_diameter, 
    h=nut_length, 
    pitch=nut_pitch,
    $fa=1,
    $fs=1,
    anchor=CENTER);

