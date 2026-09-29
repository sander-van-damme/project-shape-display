// DND-76 — S6-LC-with-primitives unit cell (P1 bistable latch + P3 pocket/guide).
//
// EVIDENCE CLASS: CAD geometry (this file + its real-OpenSCAD render). It is
// NOT a print and NOT a measurement ([DND-27]).
//
// This file draws ONE 5.08 mm cell of the ultra-low-cost broadcast-ratchet
// machine with the DND-76 primitives applied:
//   * a 3.60 mm square column body (P3) in a 1.48 mm lane;
//   * a 5-pocket vertical rack with a RELIEVED THROAT (P3);
//   * a 0.80 mm printed release pawl in the lane;
//   * a 0.90 mm over-centre bistable link (P1) above the pawl in Z;
//   * two 0.88 mm V-guide rails (P3).
//
// The feature-vs-process checks for this cell live in `../primitives.py`
// (bistable_snap / lane_budget / pocket_throat / guide_budget /
// pocket_load_path) and are asserted by `../primitives_checks.py`. They use the
// published FDM limits in tools/fdm-limits/fdm_process_limits.py. They are NOT
// the S3 fan-out coupon checker, whose BAND/journal semantics do not apply to
// this single-pitch cell.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

// --- field / cell ----------------------------------------------------------
PITCH = 5.08;
COLUMN_BODY = 3.60;
LANE = PITCH - COLUMN_BODY;        // 1.48 mm
LEVELS = 5;
STEP = 10.0;

// --- P3: rack pocket + guide ----------------------------------------------
POCKET_DEPTH = 1.20;
POCKET_WIDTH = 2.40;
POCKET_RELIEF_DEG = 30.0;
POCKET_FLOOR = 0.88;               // 2-line compression land
V_GUIDE_RAIL_T = 0.88;             // 2-line rail

// --- P1/P3: pawl ----------------------------------------------------------
PAWL_T = 0.80;                     // across the lane
PAWL_TOE = 0.60;
PAWL_LEN = 5.00;                   // Z free length
PAWL_DEFLECT = 0.35;

// --- P1: bistable over-centre link ----------------------------------------
LATCH_T = 0.90;                    // over-centre link: 2 lines
LATCH_W = 0.70;
LATCH_L = 5.00;
LATCH_OVER_CENTRE = 0.40;

// ---------------------------------------------------------------------------
module column_body() {
    color([0.3, 0.6, 0.9])
        translate([0, 0, 0])
            cube([COLUMN_BODY, COLUMN_BODY, 44.0], center = true);
}

module v_guide_rails() {
    color([0.5, 0.5, 0.5]) {
        translate([ (COLUMN_BODY + LANE - V_GUIDE_RAIL_T) / 2, 0, 20.0])
            cube([V_GUIDE_RAIL_T, COLUMN_BODY, 6.0], center = true);
        translate([-(COLUMN_BODY + LANE - V_GUIDE_RAIL_T) / 2, 0, 20.0])
            cube([V_GUIDE_RAIL_T, COLUMN_BODY, 6.0], center = true);
    }
}

module rack_pocket(level) {
    // A relieved pocket at the given level. The mouth is countersunk by
    // POCKET_RELIEF_DEG so the toe cannot wedge on a fused sharp edge.
    z = -22.0 + level * STEP;
    translate([COLUMN_BODY / 2, 0, z]) {
        rotate([0, 90, 0])
            cylinder(h = POCKET_DEPTH, d = POCKET_WIDTH, $fn = 32);
        // countersink cone on the mouth
        translate([-POCKET_DEPTH, 0, 0])
            rotate([0, -90, 0])
                cylinder(h = POCKET_DEPTH * 0.5,
                         d1 = POCKET_WIDTH, d2 = POCKET_WIDTH + 2 * POCKET_DEPTH
                              * tan(POCKET_RELIEF_DEG), $fn = 32);
    }
}

module pawl_and_latch() {
    // Pawl: a Z cantilever in the lane, toe toward the column.
    color([0.9, 0.3, 0.2])
        translate([(COLUMN_BODY + PAWL_T) / 2, 0, -18.0])
            cube([PAWL_T, PAWL_TOE, PAWL_LEN], center = true);
    // Bistable over-centre link: above the pawl in Z, same lane.
    color([0.2, 0.8, 0.3])
        translate([(COLUMN_BODY + LATCH_T) / 2, 0, 12.0])
            cube([LATCH_T, LATCH_W, LATCH_L], center = true);
}

module cell() {
    column_body();
    v_guide_rails();
    for (lvl = [0 : LEVELS - 1]) rack_pocket(lvl);
    pawl_and_latch();
}

// Assembly for viewing: a 1 x 3 strip at true pitch (the coupon test unit).
module cell_strip() {
    for (i = [0 : 2])
        translate([i * PITCH, 0, 0]) cell();
}

cell_strip();
