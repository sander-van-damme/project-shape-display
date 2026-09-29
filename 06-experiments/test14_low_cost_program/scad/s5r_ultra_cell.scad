// DND-72 ultra-low-cost S5-R variant -- CAD evidence for the unit cell and the
// R=6 / 20-writer low-cost bank geometry.
//
// This is a SINGLE-COLUMN unit cell of the unchanged S5-R register mechanism,
// re-rendered for the low-cost variant's design point, plus the R=6 deep bank
// cross-section that the exhaustive cost scan selects as the cheapest
// requirement-preserving configuration (R6-W20-M2, $345.90 delivered,
// 29.987 s). Its job is to let the sourced analytic printability gate read the
// declared feature sizes and to let a real OpenSCAD render + mesh-validate that
// the cell + bank geometry is a closed solid at the 5.08 mm pitch.
//
// IMPORTANT: this variant does NOT change the mechanism. The DND-72 finding is
// that the S5-R FIXED BASE alone ($218.70 parts -> $253.69 delivered) exceeds
// the $250 purchased target, so no mechanism cost-engineering can reach the
// target under the unchanged mission requirements. The CAD here is the cell of
// the cheapest requirement-preserving point, kept identical to the promoted
// geometry because that geometry is already the minimum for the gates.
//
// The constants below are parsed by tools/validate/analytic_printability.py
// (via tools/lowcost_analytic_printability.py) and recomputed by s5r_ultra.py.
// Keep them in sync.
//
// EVIDENCE CLASS: CAD (this file + its STL render). Not a print, not a
// measurement. See 07-evidence-and-decisions/dnd72-low-cost-variant.md.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle (tools/fdm-limits).

// ==== cell geometry (unchanged S5-R; the DND-59 re-profile) ================
PITCH = 5.08;
ROTOR_RADIUS = 1.5;
ROTOR_CORE_RADIUS = 1.0;
BASE = 2.0;
LEVELS = 5;
LEVEL_ANGLE = 360 / LEVELS;     // 72 deg

// printed drive pawl (vertical cantilever, load-bearing = 2 lines)
PAWL_T = 0.90;                  // thickness in X (pitch direction); 2 lines
PAWL_W = 0.70;                  // width in Y (row direction)
PAWL_LEN = 8.00;                // Z extent of the cantilever
PAWL_DEFLECT = 0.10;            // working deflection off the rack tooth

// keeper latch (DND-59 re-profile: 2 lines + hard compression shoulder)
KEEPER_T = 0.90;               // thickness in Y (2 lines; PASS)
KEEPER_W = 0.70;
KEEPER_LEN = 4.00;
KEEPER_OVER_CENTRE = 0.06;
KEEPER_GATE_STEP = 0.35;
KEEPER_SHOULDER_X = 0.50;

// shared drive bar with rack (DND-58: pitch 1.00 / tooth 0.50, sourced rod d=6)
RACK_TOOTH_PITCH = 1.00;
RACK_TOOTH_HEIGHT = 0.50;
BAR_D = 6.0;                    // sourced steel drive rod d=6
BAR_H = BAR_D;
BAR_W = PITCH;                  // one column of the real 80-wide bar

// housing
CELL_H = 7.0;
WALL = 0.90;
SLOT_CLEAR = 0.15;
ROTOR_BORE_CLEAR = 0.40;

// ---- DND-72 low-cost design point (the cheapest <30 s configuration) ------
ROWS_IN_BANK = 6;               // R=6 bank depth (no pitch penalty)
WRITERS = 20;                   // 20 writer solenoids over 480 cells/group
BANK_MOTORS = 2;                // 2 bank motors drive the shared rod

$fn = 48;
EPS = 0.01;

module rotor() {
    cylinder(r = ROTOR_RADIUS, h = BASE);
    translate([0, 0, BASE]) cylinder(r = ROTOR_CORE_RADIUS, h = CELL_H - BASE);
}

module pawl() {
    translate([0, -PAWL_W / 2, 0]) cube([PAWL_T, PAWL_W, PAWL_LEN]);
}

module keeper() {
    // keeper re-profiled into the ROW (Y) direction, beside the pawl (DND-59).
    // Gate noses and the shoulder are given a small overlap into the leaf so the
    // union is a single manifold on every OpenSCAD/CGAL version (coincident faces
    // are version-sensitive and can leave a non-manifold shell).
    KEEP_OVERLAP = 0.05;
    translate([0, PAWL_W + KEEPER_OVER_CENTRE, 0])
        cube([KEEPER_T, KEEPER_T, KEEPER_LEN]);
    for (k = [0:LEVELS - 1])
        translate([0, PAWL_W + KEEPER_OVER_CENTRE + KEEPER_T - KEEP_OVERLAP,
                   k * KEEPER_GATE_STEP])
            cube([KEEPER_T, 0.20 + KEEP_OVERLAP, 0.15]);
    // hard printed shoulder: pawl push-out taken in COMPRESSION
    translate([0, PAWL_W + KEEPER_OVER_CENTRE, -KEEPER_SHOULDER_X])
        cube([KEEPER_T, KEEPER_SHOULDER_X, KEEPER_SHOULDER_X + KEEP_OVERLAP]);
}

module drive_bar() {
    // sourced steel rod d=6, modelled round; rack teeth 1.00/0.50
    translate([0, 0, -BAR_H / 2]) rotate([90, 0, 0])
        cylinder(r = BAR_D / 2, h = BAR_W, center = true);
    for (t = [0:3])
        translate([-BAR_W / 2 + t * RACK_TOOTH_PITCH, -BAR_W / 2, 0])
            cube([RACK_TOOTH_HEIGHT, BAR_W, RACK_TOOTH_HEIGHT]);
}

module cell() {
    difference() {
        translate([-PITCH / 2, -PITCH / 2, -BAR_H - 1])
            cube([PITCH, PITCH, CELL_H + BAR_H + 1]);
        translate([0, 0, -BAR_H - 1 - EPS]) cylinder(r = ROTOR_RADIUS + 0.10,
                                                     h = CELL_H + 2 * EPS);
        translate([PAWL_T / 2, -PITCH / 2 - EPS, -BAR_H - 1 - EPS])
            cube([PITCH / 2, PITCH + 2 * EPS, CELL_H + 2 * EPS]);
        translate([-PITCH / 2 - EPS, PAWL_W / 2, -BAR_H - 1 - EPS])
            cube([PITCH + 2 * EPS, PITCH / 2, CELL_H + 2 * EPS]);
    }
}

module unit_cell_assembly() {
    cell();
    rotor();
    translate([0, 0, BASE + 1]) pawl();
    translate([0, 0, BASE + 1]) keeper();
    drive_bar();
}

// The R=6 bank cross-section: 6 rows of the cell share ONE racked drive rod.
// This is the geometry that lets 6 rows be written per bank pass with no pitch
// penalty (row pitch == column pitch == 5.08 mm). Rendered as a small 6-row
// witness to keep the CAD render bounded; the real bank is 80 columns wide.
module bank_cross_section() {
    for (r = [0:ROWS_IN_BANK - 1])
        translate([0, r * PITCH, 0]) unit_cell_assembly();
}

part = "assembly";

if (part == "assembly") {
    unit_cell_assembly();
} else if (part == "bank") {
    bank_cross_section();
} else if (part == "cell") {
    cell();
} else if (part == "pawl") {
    pawl();
} else if (part == "keeper") {
    keeper();
}
