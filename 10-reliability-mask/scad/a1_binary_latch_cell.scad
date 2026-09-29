// DND-104 A1 — binary over-centre latch cell at 5.08 mm pitch (real OpenSCAD)
//
// Reliability-first cell: the visible column has exactly TWO states (down =
// 0 mm, up = 40 mm). The state is held by a large over-centre toggle arm that
// travels between TWO printed hard stops; it holds in COMPRESSION against the
// stop land, not by a printed spring preload. A shared external writer head
// toggles the arm; a reader head confirms the state.
//
// This file renders the DENSE-LEVEL PARTS ONLY (column, latch arm, frame cradle
// land, latch pocket). The gantry/writer is modelled in a separate file because
// it is a shared subsystem, not a repeated part.
//
// EVIDENCE CLASS: CAD geometry. No print. Printable features are checked against
// the repo's provisional FDM rules (MIN_FEATURE 0.44 mm = 1 line at 0.4 mm;
// MIN_WALL 0.88 mm = 2 lines). No tolerance is claimed as measured (DND-27).

PITCH = 5.08;
BODY  = 3.60;          // column body (S1 coupon budget: 3.60 + 1.48 lane)
TRAVEL = 40.0;         // usable up-travel
COL_LEN = 46.0;        // column length incl. lead-in

// owned lane = half the inter-body gap
OWNED_LANE = PITCH/2 - BODY/2;      // 0.74 mm

// Latch arm is a two-position toggle. Its thickness in X must fit the OWNED
// lane with running clearance (DND-91 A1 lesson: check PLACEMENT, not budget).
LATCH_T = 0.45;        // leaf thickness in X (1 line, enters own lane)
LATCH_W = 1.20;        // width in Y
LATCH_L = 6.00;        // arm length in Z

CLEAR = 0.20;          // running clearance (assumption-class)
STOP_LAND = 0.88;      // hard-stop land width (2 lines, compression)
STOP_DEPTH = 1.20;     // land depth in Z

$fn = 24;

module column() {
    // square column with a tall pocket that the latch toe enters
    difference() {
        cube([BODY, BODY, COL_LEN], center=true);
        // latch pockets at two heights (down-stop and up-stop engagement)
        for (z = [-TRAVEL/2, TRAVEL/2])
            translate([BODY/2, 0, z])
                cube([LATCH_T + 2*CLEAR, LATCH_W + 2*CLEAR, 2.0], center=true);
    }
}

module latch_arm() {
    // one printed over-centre toggle arm (repeated 6,400x)
    // it pivots on a printed hinge pin and its toe engages the pocket land
    translate([0, 0, 0]) {
        // hinge barrel at the anchored end (outboard, does not enter the lane)
        cylinder(h = LATCH_W, d = 1.0, center = true);
        // arm leaf: the ONLY part entering the owned lane
        translate([0, 0, LATCH_L/2])
            cube([LATCH_T, LATCH_W, LATCH_L], center=true);
        // toe that engages the column pocket land (compression hold)
        translate([0, 0, LATCH_L - STOP_DEPTH/2])
            cube([LATCH_T, STOP_LAND, STOP_DEPTH], center=true);
    }
}

module cradle_land() {
    // frame cradle: two hard stops bound the arm's two states
    difference() {
        cube([BODY + 2*OWNED_LANE, BODY, 3.0], center=true);
        cube([BODY + 2*CLEAR, BODY + 2*CLEAR, 3.2], center=true);
        // relief for the latch arm on one side
        translate([BODY/2 + LATCH_T/2 + CLEAR, 0, 0])
            cube([LATCH_T + 2*CLEAR, LATCH_W + 2*CLEAR, 3.2], center=true);
    }
}

// ---- assembly (viewing) ----------------------------------------------------
module cell_assembly() {
    color("SteelBlue") column();
    translate([BODY/2 + LATCH_T/2 + CLEAR, 0, TRAVEL/2])
        color("Orange") latch_arm();
    translate([0, 0, -COL_LEN/2 - 1.5]) color("Gainsboro") cradle_land();
}

module part_selector() {
    // -D part="<key>" renders one printable part for mesh validation.
    // `part` is supplied by -D; the default below is used for interactive runs.
    if (part == "column") column();
    else if (part == "latch") latch_arm();
    else if (part == "cradle") cradle_land();
    else cell_assembly();
}

part_selector();

// ---- self-checks (echoed, captured by the render tool) ---------------------
echo(str("PITCH=", PITCH, " BODY=", BODY, " OWNED_LANE=", OWNED_LANE));
echo(str("LATCH_T+CLEAR=", LATCH_T + CLEAR, " <= OWNED_LANE=", OWNED_LANE));
echo(str("latch fits owned lane: ", (LATCH_T + CLEAR) <= OWNED_LANE));
echo(str("min feature check (latch): ", LATCH_T >= 0.44));
echo(str("stop land (2 lines): ", STOP_LAND >= 0.88));
