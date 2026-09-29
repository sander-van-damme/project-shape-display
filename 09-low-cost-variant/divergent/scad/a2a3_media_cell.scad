// DND-75 A2 / A3 divergent machines -- punched-media true-pitch cell CAD.
//
// A2 (hand-crank + punched-tape reader) and A3 (S1-B banked broadcast ratchet +
// punched-film threshold planes) share ONE new geometric claim that must be
// witnessed at the real 5.08 mm pitch: a punched MEDIA bit (a hole in a thin
// film/tape) must be able to open or block a printed gate beside a 4.72 mm
// column, with printable walls, and a follower must pass the hole.
//
// This file models that media cell: the column + 5-pocket rack, the printed
// gate bar, and the punched film with its hole and its boss (the A2 read-comb
// follower or the A3 threshold-plane boss). It is the pitch-budget witness for
// the whole punched-media family, deliberately kept to the S5 column so the
// only NEW parts are the film plane and the gate.
//
// EVIDENCE CLASS: CAD (this file + its STL render). Not a print, not a
// measurement. See 07-evidence-and-decisions/dnd75-divergent-low-cost.md.
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle.

PITCH = 5.08;
LEVELS = 5;
TRAVEL = 40.0;

// unchanged visible column (test11 S1 coupon conventions)
COLUMN_CAP = 4.72;
COLUMN_BODY = 3.60;
RACK_PITCH = 10.0;
RACK_POCKETS = 5;
POCKET_DEPTH = 1.20;
POCKET_WIDTH = 2.40;

// printed gate bar (S1 coupon geometry: stacked ABOVE the pawl in Z).
// DND-75 hostile fix: the test11 S1 coupon used 0.80 mm leaves, which sit
// between the 1-line floor (0.44) and the 2-line robustness target (0.88).
// A2/A3 re-profile both to 0.90 mm (2 lines) so the printed leaves PASS.
PAWL_T = 0.90;
PAWL_W = 7.00;
PAWL_L = 1.60;
GATE_BAR_T = 0.90;
GATE_TRAVEL = 1.40;

// punched media
FILM_T = 0.30;                  // punched film/tape thickness (1 line = 0.44;
                                // declared 0.30 is BELOW the floor -> the
                                // validator must flag it RISK, which is the
                                // honest A2/A3 media risk to record)
HOLE_D = 1.60;                  // media hole diameter
BOSS_D = 1.00;                  // film boss over an armed cell
MEDIA_W = PITCH;

// printed guide sleeves / housing
WALL = 0.90;
BASE = 3.00;
MIN_FDM_WALL = 0.44;

$fn = 48;
EPS = 0.01;

module column() {
    // necked body + square visible cap
    translate([0, 0, 0]) cube([COLUMN_BODY, COLUMN_BODY, TRAVEL + 4.0], center = false);
    translate([0, 0, TRAVEL + 4.0])
        cube([COLUMN_CAP, COLUMN_CAP, 1.2], center = false);
    // 5-pocket rack on one face
    for (k = [0:RACK_POCKETS - 1])
        translate([COLUMN_BODY / 2 - POCKET_DEPTH, -PITCH / 2 - EPS,
                   k * RACK_PITCH + 2.0])
            cube([POCKET_DEPTH, PITCH + 2 * EPS, 1.2]);
}

module pawl() {
    // flat cantilever rooted on the frame, wedge toe into a rack pocket
    translate([-PAWL_T, -PAWL_W / 2, 0]) cube([PAWL_T, PAWL_W, PAWL_L]);
}

module gate_bar() {
    // vertical gate bar, stacked above the pawl in the same X/Y lane
    translate([-PAWL_T - GATE_BAR_T, -GATE_BAR_T / 2, PAWL_L + 0.2])
        cube([GATE_BAR_T, GATE_BAR_T, 2.0]);
}

module punched_film() {
    // the media plane with one hole and one boss (armed cell)
    difference() {
        translate([-MEDIA_W / 2, -MEDIA_W / 2, -FILM_T])
            cube([MEDIA_W, MEDIA_W, FILM_T]);
        translate([0, 0, -FILM_T - EPS]) cylinder(r = HOLE_D / 2, h = FILM_T + 2 * EPS);
    }
    translate([0, 0, -FILM_T - BOSS_D / 2])
        cylinder(r = BOSS_D / 2, h = BOSS_D, center = true);
}

module frame() {
    difference() {
        translate([-PITCH / 2, -PITCH / 2, -BASE - 2.0])
            cube([PITCH, PITCH, BASE + 2.0]);
        translate([-COLUMN_BODY / 2 - 0.15, -COLUMN_BODY / 2 - 0.15, 0])
            cube([COLUMN_BODY + 0.30, COLUMN_BODY + 0.30, TRAVEL + 6.0], center = false);
    }
}

module media_cell_assembly() {
    frame();
    column();
    pawl();
    gate_bar();
    translate([0, 0, PAWL_L + 2.6]) punched_film();
}

// The 5x3 true-pitch coupon witness: 5 columns x 3 rows at 5.08 mm.
module coupon_witness() {
    for (i = [0:4]) for (j = [0:2])
        translate([i * PITCH, j * PITCH, 0]) media_cell_assembly();
}

part = "assembly";

if (part == "assembly") {
    media_cell_assembly();
} else if (part == "coupon") {
    coupon_witness();
} else if (part == "column") {
    column();
} else if (part == "pawl") {
    pawl();
} else if (part == "gate") {
    gate_bar();
} else if (part == "film") {
    punched_film();
}
