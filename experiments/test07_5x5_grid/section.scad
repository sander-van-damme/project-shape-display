// Cut-open display row for inspecting the detent + cap. Renders one row.
LIBRARY_MODE = true;   // pull grid.scad in as a library (skip its own render)
include <grid.scad>
intersection() {
    assembly();
    // slab through row 2 (y = 2*pitch), showing pins, rack, blades, cap
    translate([fx0 - 5, 2*pitch - groove_w/2 - 0.2, -10])
        cube([(fx1 - fx0) + 30, groove_w + 0.4, z_top + travel + 20]);
}
