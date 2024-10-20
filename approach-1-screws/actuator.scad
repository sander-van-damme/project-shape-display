/*
* Import the The Belfry OpenScad Library v2.
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
$slop = 0.65;

    
/*
* Set drawing parameters
*/

cube_width = 6;
cube_wall_thickness = 0.9;
cube_length = 50;
cube_thread_length = 10;

bolt_thread_length = 50;
bolt_topfoot_length = 1;
bolt_topfoot_diameter = 4.5;
bolt_midfoot_length = 2;
bolt_midfoot_diameter = 3;
bolt_lowfoot_length = 2;
bolt_lowfoot_diameter = 4.5;

thread_outer_diameter = 4;
thread_inner_diameter = 3.2;
thread_pitch = 2;

/*
* Draw cube
*/


cube_tube_length = cube_length - cube_wall_thickness;
zdistribute(
    sizes=[
        cube_wall_thickness, 
        cube_tube_length, 
        -cube_thread_length
        ],
    spacing=-0.001) {
    cube(
        [cube_width, cube_width, cube_wall_thickness],
        anchor=CENTER
    );
        rect_tube(
        size=cube_width, 
        wall=cube_wall_thickness, 
        h=cube_tube_length,
        anchor=CENTER
    );
    trapezoidal_threaded_nut(
        shape="square",
        nutwidth=cube_width,
        id=thread_inner_diameter, 
        h=cube_thread_length, 
        pitch=thread_pitch,
        anchor=CENTER);
}


/*
* Draw bolt
*/

translate([cube_width*2,0,0])
zdistribute(
    sizes=[
        bolt_thread_length, 
        bolt_topfoot_length,
        bolt_midfoot_length,
        bolt_lowfoot_length
    ],
    spacing=-0.001) {
    
    // Draw thread.
    trapezoidal_threaded_rod(
        d=thread_outer_diameter,
        height=bolt_thread_length,
        pitch=thread_pitch,
        bevel1=true);
        
    // Draw top bracket.
    zcyl(l=bolt_topfoot_length, r=bolt_topfoot_diameter/2);
    
    // Draw traverse.
    zcyl(l=bolt_midfoot_length, r=bolt_midfoot_diameter/2);
    
    // Draw bottom bracket.
    zcyl(l=bolt_lowfoot_length, r=bolt_lowfoot_diameter/2);
}
