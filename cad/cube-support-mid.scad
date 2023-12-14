/*
* Import the The Belfry OpenScad Library v2.
* documentation:
* - https://github.com/BelfrySCAD/BOSL2/wiki/
*/
include <BOSL2/std.scad>


/*
* Rendering parameters
*/
$fn=100;


/*
* Drawing parameters
*/
support_length = 300;
support_width = 5;
support_depth = 3;

support_edge_length = 1;
support_edge_depth = 1;

hole_diameter = 2.5;
hole_count = 60;
hole_spacing = support_length / hole_count;


/*
* Drawing
*/
xdistribute(
    sizes=[
        support_edge_length,
        support_length,
        support_edge_length
    ],
    spacing=-0.001) {
        
    // Draw upper support edge.
    cube(
        [support_edge_length, support_width, support_edge_depth],
        anchor=BOTTOM
    );
    
    // Draw support with holes.
    difference() {
        // Draw support.
        cube(
            [support_length,support_width,support_depth],
            anchor=BOTTOM
        );
        // Draw holes.
        xcopies(hole_spacing, n=hole_count) {
            fwd(support_width/2) down(0.001)
                cylinder(d=hole_diameter, h=support_width+0.002, $fn=20, anchor=BOTTOM);
            fwd(-support_width/2) down(0.001)
                cylinder(d=hole_diameter, h=support_width+0.002, $fn=20, anchor=BOTTOM);
            }
    }
  
    // Draw lower support edge.
    cube(
        [support_edge_length, support_width, support_edge_depth],
        anchor=BOTTOM
    );
}


