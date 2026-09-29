// DND-106 (child of DND-104) -- reliability-first cell / mechanism CAD witness.
//
// This file is the CAD witness for the InventorAlpha reliability primitives
// (see 06-experiments/test14_low_cost_program/divergent/reliability_primitives_alpha.py).  It
// models, at the true 5.08 mm surface pitch:
//
//   * R2 -- the DOUBLE-ACTING WEDGE-GATE CELL: a two-position sliding gate
//     between two printed hard stops, sitting in the 1.48 mm lane beside a
//     3.60 mm column body.  The high stop is a printed wall; the low stop is
//     reached by the platen pushing the gate down (a driven, positive reset,
//     replacing S6-LC's release-and-trust-gravity reset).
//   * R1 -- the TOGGLE-ROCKER ROW MODULE: one off-pitch rocker per row with a
//     4-step staircase that the passive column teeth rest on.  The module is
//     deliberately OFF the 5.08 mm cell pitch (02-design-criteria: internal
//     machinery may be larger / shared / external).
//   * R3 -- the READ COMB finger that seats against a gate (detectable state).
//
// EVIDENCE CLASS: CAD (this file + the analytic printability checker).  It is
// NOT a print and NOT a measurement.  See 02-design-criteria for the sourced
// FDM limits and DND-27 for the no-print/no-purchase/no-measure constraint.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.2 mm layers.

// --- shared surface scale ---------------------------------------------------
PITCH = 5.08;
LEVELS = 5;
TRAVEL = 40.0;

// --- unchanged visible column (S1 coupon conventions) -----------------------
COLUMN_CAP = 4.72;
COLUMN_BODY = 3.60;
RACK_PITCH = 10.0;
RACK_POCKETS = 5;
POCKET_DEPTH = 1.20;
POCKET_WIDTH = 2.40;

// --- R2: double-acting wedge gate -------------------------------------------
GATE_BODY_T = 0.90;             // 2-line sliding wedge (>= 0.88 mm robust)
GATE_THROW = 1.40;              // travel between the two hard stops
GATE_LANE = 1.48;               // lane beside the column body (pitch - body)
GATE_SHOULDER = 1.00;           // shoulder that blocks the column tooth
GATE_LOW_STOP = 0.90;           // printed low-stop wall
GATE_HIGH_STOP = 0.90;          // printed high-stop wall

// --- R1: row rocker + 4-step staircase (off-pitch module) -------------------
ROCKER_ARM_T = 1.32;            // 3-line load-bearing arm
ROCKER_STEPS = 4;               // 0/10/20/30/40 mm staircase
STEP_RISE = RACK_PITCH;         // 10 mm per step (level height)
STEP_TOOTH_W = 0.90;            // 2-line step/ledge tooth
STEP_TOOTH_L = 2.40;
ROTOR_R = 2.00;                 // printed rocker pivot boss radius
ROTOR_BORE_CLEAR = 0.25;        // printed boss-in-socket free play (total)

// --- R3: read-comb finger ---------------------------------------------------
FINGER_T = 0.90;                // 2-line compliant finger
FINGER_L = 4.00;
FINGER_W = 0.80;                // < 2-line in Y: it is a compliant sensor,
                                // reported by the checker as a sensing risk,
                                // not a load-bearing wall

// --- printed housing / base -------------------------------------------------
WALL = 0.90;
BASE = 3.00;
MIN_FDM_WALL = 0.44;

$fn = 48;
EPS = 0.01;

module column() {
    cube([COLUMN_BODY, COLUMN_BODY, TRAVEL + 4.0], center = false);
    translate([0, 0, TRAVEL + 4.0])
        cube([COLUMN_CAP, COLUMN_CAP, 1.2], center = false);
    // 5-pocket rack on one face (height is set by which pocket the pawl rests in)
    for (k = [0:RACK_POCKETS - 1])
        translate([COLUMN_BODY / 2 - POCKET_DEPTH, -PITCH / 2 - EPS,
                   k * RACK_PITCH + 2.0])
            cube([POCKET_DEPTH, PITCH + 2 * EPS, 1.2]);
}

module wedge_gate() {
    // R2: sliding wedge gate in the lane, between two printed hard stops.
    // high stop (raised state) at the top, low stop (lowered) at the bottom.
    translate([COLUMN_BODY / 2 + EPS, -GATE_BODY_T / 2, TRAVEL * 0.5])
        cube([GATE_BODY_T, GATE_BODY_T, GATE_THROW]);
    // the gate's shoulder that blocks the column lift tooth when raised
    translate([COLUMN_BODY / 2 - GATE_SHOULDER + EPS,
               -GATE_BODY_T / 2, TRAVEL * 0.5 + GATE_THROW - GATE_SHOULDER])
        cube([GATE_SHOULDER, GATE_BODY_T, GATE_SHOULDER]);
}

module gate_stops() {
    // printed hard stops: raised wall above, lowered wall below.
    translate([COLUMN_BODY / 2 + EPS, -GATE_BODY_T / 2 - EPS,
               TRAVEL * 0.5 + GATE_THROW])
        cube([GATE_BODY_T, GATE_BODY_T + 2 * EPS, GATE_HIGH_STOP]);
    translate([COLUMN_BODY / 2 + EPS, -GATE_BODY_T / 2 - EPS,
               TRAVEL * 0.5 - GATE_LOW_STOP])
        cube([GATE_BODY_T, GATE_BODY_T + 2 * EPS, GATE_LOW_STOP]);
}

module r2_cell() {
    column();
    wedge_gate();
    gate_stops();
}

// R1 row rocker module: OFF-PITCH (placed beside the row) with a 4-step
// staircase whose steps the passive column teeth rest on.
module row_rocker() {
    // rocker arm (load-bearing, 3-line)
    translate([-8.0, -ROCKER_ARM_T / 2, 0])
        cube([12.0, ROCKER_ARM_T, ROCKER_ARM_T]);
    // pivot boss
    translate([-8.0, 0, 0]) cylinder(r = ROTOR_R, h = ROCKER_ARM_T);
    // 4-step staircase carried by the rocker
    for (k = [0:ROCKER_STEPS - 1])
        translate([k * STEP_TOOTH_L, -STEP_TOOTH_W / 2, k * STEP_RISE])
            cube([STEP_TOOTH_L, STEP_TOOTH_W, STEP_TOOTH_W]);
}

module r3_read_finger() {
    // compliant read finger that seats against a gate to sense its state
    translate([0, 0, 0]) cube([FINGER_T, FINGER_W, FINGER_L]);
}

module frame() {
    difference() {
        translate([-PITCH / 2, -PITCH / 2, -BASE - 2.0])
            cube([PITCH, PITCH, BASE + 2.0]);
        translate([-COLUMN_BODY / 2 - 0.15, -COLUMN_BODY / 2 - 0.15, 0])
            cube([COLUMN_BODY + 0.30, COLUMN_BODY + 0.30, TRAVEL + 6.0],
                 center = false);
    }
}

module reliability_cell_assembly() {
    frame();
    r2_cell();
    translate([COLUMN_BODY / 2 + 1.6, 0, TRAVEL * 0.5]) r3_read_finger();
}

// The 5x3 true-pitch coupon witness: 5 columns x 3 rows at 5.08 mm pitch.
module coupon_witness() {
    for (i = [0:4]) for (j = [0:2])
        translate([i * PITCH, j * PITCH, 0]) reliability_cell_assembly();
}

part = "assembly";

if (part == "assembly") {
    reliability_cell_assembly();
} else if (part == "coupon") {
    coupon_witness();
} else if (part == "column") {
    column();
} else if (part == "gate") {
    wedge_gate();
} else if (part == "stops") {
    gate_stops();
} else if (part == "rocker") {
    row_rocker();
} else if (part == "finger") {
    r3_read_finger();
}
