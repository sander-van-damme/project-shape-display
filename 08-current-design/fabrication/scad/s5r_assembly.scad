// DND-69 S5-R ASSEMBLED-SCENE library for board-viewable renders.
//
// This file places the printed part modules from `s5r_parts.scad` at their real
// relative positions so a render (or an STL) shows the ASSEMBLED mechanism, not
// the loose part set. It adds NO new part geometry: every solid is the same
// module the printable STLs are rendered from, so an assembly image is true to
// the shipped geometry.
//
// Two scenes are exposed via `scene=`:
//   * "cell_cluster" -- a 3x3 cartridge tile with rotors, pawls, keepers and
//     detent leaves installed in every cell, a rack strip + sourced steel rod
//     in the centre row, i.e. the per-cell register as it sits in the field.
//   * "cell_exploded" -- the same cluster with the moving parts lifted +Z and
//     the rack/rod pulled +Y, so the cell, rotor, pawl, keeper, detent and rack
//     stack is readable.
//
// EVIDENCE CLASS: CAD assembly geometry. NOT a printed or measured assembly
// ([DND-27]). The sourced steel rod is shown as a bare cylinder for context; it
// is not a printed part.

include <s5r_parts.scad>

// --- placement (mm), mirrored from `s5r_parts_common.scad` ----------------
ASSY_COLS = 3;
ASSY_ROWS = 3;

// cell centre (x,y) of cell (cx,cy) in an ASSY_COLS x ASSY_ROWS tile
function cell_x(cx) = (cx - (ASSY_COLS - 1) / 2) * PITCH;
function cell_y(cy) = (cy - (ASSY_ROWS - 1) / 2) * PITCH;

// The cartridge part subtracts `inner_cell()` (rotor bore + pawl chamber +X +
// keeper chamber +Y) at each cell centre, all rooted at z = 0 = housing top.
// Rotor sits in the bore (z 0..CELL_H); pawl chamber is +X; keeper chamber +Y.

module rotor_at(cx, cy, dz = 0) {
    translate([cell_x(cx), cell_y(cy), dz]) rotor();
}

module pawl_at(cx, cy, dz = 0) {
    // pawl chamber is +X of the bore; leaf hangs down the chamber at z 0..LEN
    translate([cell_x(cx) + PAWL_T / 2, cell_y(cy), dz]) drive_pawl();
}

module keeper_at(cx, cy, dz = 0) {
    // keeper chamber is +Y of the bore
    translate([cell_x(cx), cell_y(cy) + KEEPER_T / 2, dz]) keeper();
}

module detent_at(cx, cy, dz = 0) {
    // detent leaf rides the -X wall of the bore, scallop toward the rotor
    translate([cell_x(cx) - WALL, cell_y(cy), dz]) detent_leaf();
}

// The cartridge tile itself: real printed geometry (true 27x27 module supports
// cols/rows), rendered here at the small ASSY tile size for a readable scene.
module cartridge_tile() {
    cell_cartridge(ASSY_COLS, ASSY_ROWS);
}

// One full populated cell (rotor + pawl + keeper + detent).
module populated_cell(cx, cy, dz = 0) {
    rotor_at(cx, cy, dz);
    pawl_at(cx, cy, dz);
    keeper_at(cx, cy, dz);
    detent_at(cx, cy, dz);
}

// Sourced steel rod (NOT printed): a plain Ø6 mm cylinder through the rack
// channel under the centre row, drawn short so it reads as a drive rod.
module sourced_rod(len = ASSY_ROWS * PITCH + 24) {
    // rack channel centre is at y = 0 for the centre row, just under the tile
    translate([-len / 2, 0, -BAR_D - 0.0])
        rotate([0, 90, 0]) cylinder(r = BAR_D / 2, h = len);
}

// A printed rack strip for the centre row, teeth up, clipped on the rod.
module centre_rack() {
    translate([-(ASSY_COLS * PITCH) / 2, -RACK_STRIP_W / 2, -BAR_D - 0.0]) rack_strip(ASSY_COLS * PITCH);
}

module cell_cluster() {
    cartridge_tile();
    for (cx = [0 : ASSY_COLS - 1], cy = [0 : ASSY_ROWS - 1])
        populated_cell(cx, cy);
    centre_rack();
    sourced_rod();
}

module cell_exploded() {
    cartridge_tile();
    // rotors + register lifted clear of their bores
    for (cx = [0 : ASSY_COLS - 1], cy = [0 : ASSY_ROWS - 1])
        populated_cell(cx, cy, dz = CELL_H + 6.0);
    // rack + rod pulled down/clear
    translate([0, 0, -10.0]) centre_rack();
    translate([0, 0, -18.0]) sourced_rod();
}

scene = "cell_cluster";

if (scene == "cell_cluster")        cell_cluster();
else if (scene == "cell_exploded")  cell_exploded();
