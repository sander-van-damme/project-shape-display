// DND-71 S6-LC ultra-low-cost shape display -- real OpenSCAD geometry.
//
// EVIDENCE CLASS: CAD (geometry only). No print, no measurement (DND-27).
// All dimensions are mirrored from ../analysis/s6lc.py.
//
// Machine: 8 banks of 10 rows (80x80 = 6,400 cells) at 5.08 mm pitch.
//   * square printed columns with a 5-pocket vertical rack (10 mm pockets);
//   * printed cantilever pawls (0.90 x 1.20 x 8.00 mm) holding a column;
//   * per-bank threshold mask gate (printed sliding comb) read from a medium;
//   * 8 banked release combs on a travelling reset carriage;
//   * one 4-screw belt-synced platen (printed frame, excluded from the BOM).
//
// Render (real OpenSCAD):
//   openscad -o s6lc_cell.stl       -D 'PART="cell"'    s6lc_machine.scad
//   openscad -o s6lc_bank.stl       -D 'PART="bank"'    s6lc_machine.scad
//   openscad -o s6lc_platen.stl     -D 'PART="platen"'  s6lc_machine.scad

PART = "cell";

// ---- product / geometry constants (analysis/s6lc.py) ----------------------
PITCH       = 5.08;
BODY        = 3.60;      // square column body (S1 lane budget: 3.60 + 1.48 = 5.08)
COL_H       = 44.0;      // column height (40 mm travel + 4 mm base)
TRAVEL      = 40.0;
LEVEL       = 10.0;
POCKET_H    = 3.0;       // rack pocket depth in Z
POCKET_D    = 0.8;       // rack pocket depth in X (S1 coupon)
PAWL_T      = 0.90;      // 2 extrusion lines
PAWL_W      = 1.20;
PAWL_L      = 8.00;
ROWS_BANK   = 10;
COLS        = 80;
BANKS       = 8;

$fn = 48;

module column_with_rack() {
    // Square column body with 5 rack pockets on the +X face.
    difference() {
        translate([-BODY/2, -BODY/2, 0]) cube([BODY, BODY, COL_H]);
        // rack pockets at 0,10,20,30,40 mm above the base
        for (k = [0:4]) {
            translate([BODY/2 - POCKET_D, -BODY/2 + 0.4, 4 + k*LEVEL])
                cube([POCKET_D + 1, BODY - 0.8, POCKET_H]);
        }
    }
}

module pawl() {
    // Rooted cantilever: base block + thin leaf with a wedge toe.
    // Root is attached to the frame (not floating).
    translate([0, 0, 0]) cube([PAWL_T, PAWL_W, 1.5]);          // root block
    translate([0, 0, 1.5]) cube([PAWL_T/2, PAWL_W, PAWL_L]);   // thin leaf
    // toe wedge at the free end (points into the rack)
    translate([0, 0, 1.5 + PAWL_L - 1.2])
        multmatrix([[1,0,0,0],[0,1,0,0],[0.5,0,1,0],[0,0,0,1]])
            cube([PAWL_T/2, PAWL_W, 1.2]);
}

module mask_gate() {
    // Printed sliding comb: body bar + bosses over cells that must be BLOCKED.
    // One per bank (COLS = 80 cells wide); boss pitch = PITCH.
    bar_w = COLS * PITCH;
    translate([0, 0, 0]) cube([bar_w, 1.2, 1.0]);
    for (i = [0 : COLS-1]) {
        // alternating boss pattern is illustrative geometry; the real pattern
        // comes from the map. This renders the printable comb envelope.
        if (i % 2 == 0)
            translate([i*PITCH + PITCH/2 - 0.44, -0.4, 1.0])
                cube([0.88, 2.0, 1.2]);
    }
}

module release_comb() {
    // One bank release comb: a bar with a toe under every cell, lifted by the
    // travelling carriage to trip all pawls of the bank at reset.
    bar_w = COLS * PITCH;
    translate([0, 0, 0]) cube([bar_w, 1.2, 1.0]);
    for (i = [0 : COLS-1]) {
        translate([i*PITCH + PITCH/2 - 0.44, 0.8, 1.0])
            cube([0.88, 1.6, 1.0]);
    }
}

module bank_row() {
    // One row of a bank: 80 cells at true pitch, with pawl + gate lanes.
    for (i = [0 : COLS-1]) {
        translate([i*PITCH, 0, 0]) {
            column_with_rack();
        }
    }
    // pawl lane sits in the Y gap between rows (not rendered per cell here for
    // clarity of the row envelope; the cell module includes the pawl).
}

module cell_assembly() {
    // The unit-cell mechanism: column + pawl (side-by-side lane) + gate lane.
    column_with_rack();
    translate([BODY/2 + 0.10, 0, 4]) pawl();
}

module bank_assembly() {
    // A bank: the full 80-column width at true pitch, rendered as 3
    // representative rows to keep the mesh tractable (the envelope width
    // 80 * PITCH = 406.4 mm is the printability-relevant dimension; the row
    // count does not change any gate). The real bank is 10 rows, sub-tiled.
    for (r = [0 : 2]) {
        translate([0, r*PITCH, 0]) bank_row();
    }
}

if (PART == "cell")     cell_assembly();
if (PART == "bank")     bank_assembly();
if (PART == "gate")     mask_gate();
if (PART == "comb")     release_comb();
if (PART == "platen")   cube([COLS*PITCH, ROWS_BANK*PITCH, 2.0]);
