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


/*
* Set drawing parameters
*/

// general
length = 50;
width = 10;
thread_diameter = 4;
thread_pitch = 2;

// cube
cube_wall_thickness = 1;
cube_thread_length = 10;

// bolt
bolt_thread_length = 10;
bolt_bracket_length = 1;
bolt_bracket_diameter = 4.5;

/*
* Calculate drawing parameters
*/

top_wall_width = width;
nut_outer_diameter = width;
rectangular_tube_length = length - cube_wall_thickness - cube_thread_length;


/*
* Draw
*/

// half nut
difference(){
    trapezoidal_threaded_nut(
    shape="square",
    nutwidth=nut_outer_diameter,
    id=thread_diameter, 
    h=cube_thread_length, 
    pitch=thread_pitch,
    $fa=1,
    $fs=1,
    anchor=CENTER);
    // Cube to cut half of the nut
    translate([width/2, -0.1, -0.1])
    cube([width, width+1, cube_thread_length+1], anchor = CENTER);
    
} 

// nut
translate([10,0,0])
trapezoidal_threaded_nut(
    shape="square",
    nutwidth=nut_outer_diameter,
    id=thread_diameter, 
    h=cube_thread_length, 
    pitch=thread_pitch,
    $fa=1,
    $fs=1,
    anchor=CENTER);

// bolt
translate([20,0,0])
zdistribute(
    sizes=[
        bolt_thread_length, 
        bolt_bracket_length
    ],
    spacing=-0.001) {
    
    // Draw thread.
    trapezoidal_threaded_rod(
        d=thread_diameter,
        height=bolt_thread_length,
        pitch=thread_pitch,
        bevel1=true);
    
    // Draw top bracket.
    zcyl(l=bolt_bracket_length, r=bolt_bracket_diameter/2);
}
