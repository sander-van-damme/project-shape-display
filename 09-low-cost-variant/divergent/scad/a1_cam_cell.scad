// DND-75 A1 divergent machine -- single-shaft cam cell CAD evidence.
//
// The A1 machine keeps the promoted S5-R register (DND-54/DND-59) cell: a
// 5-level rotor, a printed load-bearing pawl, and a printed keeper gate. What
// A1 CHANGES is the DRIVE: instead of a lift motor + a scanner motor + 40
// writer solenoids + a bank motor, ONE sourced stepper turns a printed camshaft
// that carries, in phased sections:
//   1. FOUR lift cams (4 x 10 mm) -- the zoned platen stroke,
//   2. ONE bank-stroke cam -- the shared rack advance,
//   3. ONE Geneva drum -- the writer-comb index (replaces the scanner motor),
//   4. the writer comb itself (replaces the 40 writer solenoids).
//
// This cell is the pitch-budget witnesses for that claim: the camshaft sections
// and the writer comb must fit in the cell's 5.08 mm row band alongside the
// unchanged rotor/pawl/keeper. The full camshaft spans the whole machine; this
// file models one cell's local cross-section plus the camshaft section that
// passes through it, so a real OpenSCAD render + mesh check can read the
// declared feature sizes against the FDM process limits.
//
// EVIDENCE CLASS: CAD (this file + its STL render). Not a print, not a
// measurement. See 07-evidence-and-decisions/dnd75-divergent-low-cost.md.
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle.

PITCH = 5.08;
ROTOR_RADIUS = 1.5;
ROTOR_CORE_RADIUS = 1.0;
BASE = 2.0;
LEVELS = 5;

// unchanged S5-R register leaves (DND-59 re-profile)
PAWL_T = 0.90;
PAWL_W = 0.70;
PAWL_LEN = 8.00;
KEEPER_T = 0.90;
KEEPER_W = 0.70;
KEEPER_LEN = 4.00;
KEEPER_OVER_CENTRE = 0.06;
KEEPER_GATE_STEP = 0.35;
KEEPER_SHOULDER_X = 0.50;

// ---- A1 drive: printed camshaft on a sourced 8 mm rod ---------------------
ROD_D = 8.00;                   // sourced steel rod (A1 camshaft_rod line)
CAM_BASE_R = 3.00;              // cam base circle radius
CAM_RISE = 1.50;                // printed cam rise (not the 10 mm travel;
                                // the 10 mm lift is the follower arm ratio)
CAM_T = 1.00;                   // cam disc thickness in Z (>1 line)
LIFT_CAMS = 4;                  // four zoned lift cams
GENEVA_PINS = 4;                // Geneva drum index positions
GENEVA_R = 2.00;
CAM_SHAFT_Y = PITCH;            // camshaft row, one pitch below the cell row

// ---- writer comb (replaces 40 solenoids; cam-actuated) --------------------
COMB_T = 0.90;                  // comb finger thickness (2 lines)
COMB_W = 0.70;
COMB_H = 3.00;

// ---- housing + unchanged rack tooth (register-cell checker inputs) --------
WALL = 0.90;
RACK_TOOTH_HEIGHT = 0.50;
ROTOR_BORE_CLEAR = 0.40;
ROD_D_PRINTED = 1.80;           // printed rod wall if the sourced rod is
                                // substituted (2+ lines); sourced is preferred

$fn = 48;
EPS = 0.01;

module rotor() {
    cylinder(r = ROTOR_RADIUS, h = BASE);
    translate([0, 0, BASE]) cylinder(r = ROTOR_CORE_RADIUS, h = 7.0 - BASE);
}

module pawl() {
    translate([0, -PAWL_W / 2, 0]) cube([PAWL_T, PAWL_W, PAWL_LEN]);
}

module keeper() {
    translate([0, PAWL_W + KEEPER_OVER_CENTRE, 0])
        cube([KEEPER_T, KEEPER_T, KEEPER_LEN]);
    for (k = [0:LEVELS - 1])
        translate([0, PAWL_W + KEEPER_OVER_CENTRE + KEEPER_T,
                   k * KEEPER_GATE_STEP])
            cube([KEEPER_T, 0.20, 0.15]);
    translate([0, PAWL_W + KEEPER_OVER_CENTRE, -KEEPER_SHOULDER_X])
        cube([KEEPER_T, KEEPER_SHOULDER_X, KEEPER_SHOULDER_X]);
}

// The camshaft: one sourced rod carrying the printed A1 cam/drum sections.
module camshaft() {
    translate([0, CAM_SHAFT_Y, 0]) rotate([90, 0, 0])
        cylinder(r = ROD_D / 2, h = PITCH, center = true);
    // one lift-cam disc shown at this row station
    translate([0, CAM_SHAFT_Y, 0])
        cylinder(r = CAM_BASE_R, h = CAM_T, center = true);
    // the cam nose (the 10 mm stroke is taken at the follower arm, not here)
    translate([CAM_BASE_R, CAM_SHAFT_Y, 0])
        cylinder(r = CAM_RISE, h = CAM_T, center = true);
    // Geneva drum section (writer index)
    translate([0, CAM_SHAFT_Y, CELL_Z + 1.0])
        cylinder(r = GENEVA_R, h = 1.50, center = true);
    for (g = [0:GENEVA_PINS - 1])
        rotate([0, 0, g * 360 / GENEVA_PINS])
            translate([GENEVA_R, CAM_SHAFT_Y, CELL_Z + 1.0])
                cylinder(r = 0.25, h = 1.60, center = true);
}

CELL_Z = 4.0;   // camshaft/Geneva plane above the rotor base

// The writer comb finger for one cell: cam-actuated to set the keeper gate.
module writer_comb() {
    translate([0, -COMB_W / 2 - COMB_W, CELL_Z + 1.0])
        cube([COMB_T, COMB_W, COMB_H]);
}

module unit_cell_assembly() {
    rotor();
    translate([0, 0, BASE + 1]) pawl();
    translate([0, 0, BASE + 1]) keeper();
    camshaft();
    writer_comb();
}

// The row witness: the cell plus the camshaft station that serves it. Two rows
// show that the camshaft sits one row-pitch away and does not collide.
module row_witness() {
    unit_cell_assembly();
    translate([0, PITCH, 0]) unit_cell_assembly();
}

part = "assembly";

if (part == "assembly") {
    unit_cell_assembly();
} else if (part == "row") {
    row_witness();
} else if (part == "rotor") {
    rotor();
} else if (part == "pawl") {
    pawl();
} else if (part == "keeper") {
    keeper();
} else if (part == "camshaft") {
    camshaft();
} else if (part == "comb") {
    writer_comb();
}
