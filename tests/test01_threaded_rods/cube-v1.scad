/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
* - https://github.com/BelfrySCAD/BOSL2/wiki/threading.scad
*/

include <BOSL2/std.scad>
include <BOSL2/threading.scad>


/*
* Set rendering parameters
*/

$fn = $preview ? 32 : 128;


/*
* Set drawing parameters
*/

length = 50;
width = 4.9;
side_walls_thickness = 1;
top_wall_thickness = 1;
nut_length = 10;
nut_inner_diameter = 4;
nut_pitch = 2;
nut_slop = 0.1;


/*
* Calculate drawing parameters
*/

top_wall_width = width;
nut_outer_diameter = width;
rectangular_tube_length = length - top_wall_thickness - nut_length;


/*
* Draw
*/

zdistribute(
    sizes=[top_wall_thickness, rectangular_tube_length, nut_length],
    spacing=-0.001) {
        
    // Draw top wall
    cube(
        [top_wall_width, top_wall_width, top_wall_thickness],
        anchor=CENTER
    );
    
    // Draw tube
    rect_tube(
        size=width, 
        wall=side_walls_thickness, 
        h=rectangular_tube_length,
        anchor=CENTER
    );
        
    // Draw nut
    threaded_nut(
        shape="square",
        nutwidth=nut_outer_diameter,
        id=nut_inner_diameter, 
        h=nut_length, 
        pitch=nut_pitch,
        $slop=nut_slop,
        $fa=1,
        $fs=1,
        anchor=CENTER);

}