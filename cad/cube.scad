/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
* - https://github.com/BelfrySCAD/BOSL2/wiki/threading.scad
*/
include <BOSL2/std.scad>
include <BOSL2/threading.scad>


/*
* Rendering parameters
*/
$fn=100;


/*
* Drawing parameters
*/
cube_hat_length = 1;
cube_hat_width = 4.9;

cube_width = cube_hat_width;

nut_length = 4;
nut_outer_diameter = cube_width;
nut_inner_diameter = 2;
nut_pitch = 1;
nut_slop = 0.1;

cube_length = 70 + 1 - cube_hat_length - nut_length;
cube_wall_thickness = 1;


/*
* Drawing
*/
zdistribute(
    sizes=[cube_hat_length, cube_length, nut_length],
    spacing=-0.001) {
        
    // Draw cube hat.
    cube(
        [cube_hat_width, cube_hat_width, cube_hat_length],
        anchor=CENTER
    );
    
    // Draw cube.
    rect_tube(
        size=cube_width, 
        wall=cube_wall_thickness, 
        h=cube_length,
        anchor=CENTER
    );
        
    // Draw nut.
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