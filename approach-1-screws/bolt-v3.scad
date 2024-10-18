/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
* - https://github.com/BelfrySCAD/BOSL2/wiki/threading.scad
* - https://github.com/BelfrySCAD/BOSL2/wiki/gears.scad
*/

include <BOSL2/std.scad>
include <BOSL2/threading.scad>
include <BOSL2/gears.scad>


/*
* Set rendering parameters
*/

$fn = $preview ? 32 : 128;
$slop = 0.15;

/*
* Set drawing parameters
*/

thread_length = 50;
thread_diameter = 4;
thread_pitch = 2;
slop = 1;

top_bracket_length = 1;
top_bracket_diameter = 4.5;


/*
* Calculate drawing parameters
*/



/*
* Drawing
*/

zdistribute(
    sizes=[
        thread_length, 
        top_bracket_length
    ],
    spacing=-0.001) {
    
    // Draw thread.
    trapezoidal_threaded_rod(
        d=thread_diameter,
        height=thread_length,
        pitch=thread_pitch,
        bevel1=true    );
    
    // Draw top bracket.
    zcyl(l=top_bracket_length, r=top_bracket_diameter/2);
}
