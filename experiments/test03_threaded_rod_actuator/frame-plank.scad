/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
*/
include <BOSL2/std.scad>


/*
* Rendering parameters
*/
$fn = $preview ? 32 : 128;


/*
* Drawing parameters
*/

length = 25.4;
width = 25.4 / 4;
depth = 1.9;

edge_length = 1;
edge_depth = 1;

hole_diameter = 3;
hole_count = 4;
hole_spacing = length / hole_count;


/*
* Drawing
*/
xdistribute(
    sizes=[
        edge_length,
        length,
        edge_length
    ],
    spacing=-0.001) {
        
    // Draw upper support edge.
    cube(
        [edge_length, width, edge_depth],
        anchor=BOTTOM
    );
    
    // Draw support with holes.
    difference() {
        // Draw support.
        cube(
            [length,width,depth],
            anchor=BOTTOM
        );
        // Draw holes.
        xcopies(hole_spacing, n=hole_count) {
            fwd(width/2) down(0.001)
                cylinder(d=hole_diameter, h=width+0.002, $fn=20, anchor=BOTTOM);
            fwd(-width/2) down(0.001)
                cylinder(d=hole_diameter, h=width+0.002, $fn=20, anchor=BOTTOM);
            }
    }
  
    // Draw lower support edge.
    cube(
        [edge_length, width, edge_depth],
        anchor=BOTTOM
    );
}


