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
* Rendering parameters
*/
$fn=100;


/*
* Drawing parameters
*/
thread_length = 70;
thread_diameter = 2;
thread_pitch = 1;

top_bracket_length = 1;
top_bracket_diameter = 4.5;

bracket_traverse_length = 3 + 0.5;
bracket_traverse_diameter = thread_diameter;

bottom_bracket_length = top_bracket_length;
bottom_bracket_diameter = top_bracket_diameter;

gear_length = 3;
gear_width = 2.2;
gear_teeth_count = 9;
gear_module = gear_width / gear_teeth_count;


/*
* Drawing
*/
zdistribute(
    sizes=[
        thread_length, 
        top_bracket_length, 
        bracket_traverse_length, 
        bottom_bracket_length,
        gear_length
    ],
    spacing=-0.001) {
    
    // Draw thread.
    threaded_rod(
        d=thread_diameter,
        height=thread_length,
        pitch=thread_pitch, 
        $fa=1, 
        $fs=1
    );
    
    // Draw top bracket.
    zcyl(
        l=top_bracket_length, 
        r=top_bracket_diameter/2
    );
    
    // Draw traverse.
    zcyl(
        l=bracket_traverse_length, 
        r=bracket_traverse_diameter/2
    );
    
    // Draw bottom bracket.
    zcyl(
        l=bottom_bracket_length, 
        r=bottom_bracket_diameter/2
    );
    
    // Draw gear.
    spur_gear(
        thickness=gear_length,
        teeth=gear_teeth_count, 
        mod=gear_module
    );
}

