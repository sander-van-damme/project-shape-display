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
* Rendering
*/

$fn = $preview ? 32 : 128;
$slop=0.65;


/*
* Globals
*/

pitch = 3;


/*
* Cube
*/

od_cube = 4.4;
wall_cube = 0.44;
od_thread_cube = 3.4;
depth_thread_cube = (pitch / 2) * 0.9;
len_cube = 25.4 * 2;
len_cube_thread = 10;

union(){
    zdistribute(
        sizes=[len_cube, -len_cube_thread],
        spacing=-0.001) 
    {
     
        rect_tube(
            size=od_cube, 
            wall=wall_cube, 
            h=len_cube,
            anchor=CENTER
        );
        trapezoidal_threaded_nut(
            shape="square",
            nutwidth=od_cube,
            thread_angle=30,
            id=od_thread_cube, 
            h=len_cube_thread,
            thread_depth = depth_thread_cube,
            pitch=pitch,
            anchor=CENTER);
    }
}


/*
* Screw
*/

od_screw = 3.2;
depth_thread_screw = (pitch / 2) * 0.6;
len_screw = 50;

translate([od_cube*2,0,0])
zdistribute(
    sizes=[
        len_screw
    ],
    spacing=-0.001) {
    
    // Draw thread.
    trapezoidal_threaded_rod(
        d=od_screw,
        height=len_screw,
        pitch=pitch,
        thread_angle=30,
        thread_depth=depth_thread_screw,
        bevel1=true);

  
}
