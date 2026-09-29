// DND-55 S5-R R=4 multi-row BANK assembly -- CAD + interference evidence.
//
// This models the part of the S5-R machine that DND-54 left un-modelled: the
// multi-row (R=4) shared drive bar with its rack, the reset comber, and the
// writer-carriage sweep envelope. It is NOT a full 320-rotor machine and NOT a
// print. Its job is to let a real OpenSCAD (a) render the bank geometry and
// (b) run scoped interference queries between the moving sub-assemblies at the
// design positions, so the assembly-level envelope claims can be checked as CAD
// instead of asserted.
//
// WHY THE COLUMN COUNT IS REDUCED. The bank geometry in question (bar torsion /
// rack / comber / writer-carriage arcs) is invariant along a uniform,
// equally-spaced row of columns. The bank is modelled as BANK_COLS_MODEL
// evenly-spaced columns at the real 5.08 mm pitch, and the pitch/clearance
// arithmetic is done for the FULL 80-column row in s5r_bank.py (analytic) --
// the reduced model is the CAD witness for the geometry, not a stand-in for
// the arithmetic.
//
// DATUM. z = 0 is the TOP of the bar BODY; the rack teeth stand RACK_TOOTH_HEIGHT
// above it, so the engaged pawl tip bears on the tooth-top plane at
// z = RACK_TOOTH_HEIGHT. The bar body hangs below; the rotor hubs sit above.
// Intended contact is ONLY the engaged pawl tip on a rack tooth, separated here
// by EPS so any residual intersection is an unintended collision.
//
// EVIDENCE CLASS: CAD (this file + its STLs + interference queries). Not a
// print, not a measurement. See 07-evidence-and-decisions/dnd55-s5r-bank-assembly.md.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle (tools/fdm-limits).

// ---- field / bank layout -------------------------------------------------
PITCH = 5.08;                   // in-row (X) column pitch, from the S5 cell
ROW_PITCH = 5.08;               // cross-row (Y) pitch (independent of column pitch)
BANK_ROWS = 4;                  // R = 4 rows deep (the DND-54 design point)
BANK_COLS_MODEL = 8;            // modelled columns (real row has 80; see header)

// ---- shared drive bar (spans 80 columns in X, R rows in Y) ---------------
BAR_W = 3.0;                    // bar cross-section width (Y), = one row band
BAR_H = 12.0;                   // bar cross-section height (Z): the DND-55 torsion-driven section
BAR_UNDER = BAR_H;              // bar body depth below the tooth tips (Z)
// DND-55 CORRECTION: DND-54's rack (pitch 0.60, tooth 0.45) leaves a
// 0.15 mm inter-tooth gap that FUSES at a 0.4 mm nozzle (< 0.44 mm line).
// The rack is re-dimensioned to pitch 1.00 / tooth 0.50 -> 0.50 mm gap OK.
RACK_TOOTH_PITCH = 1.00;
RACK_TOOTH_HEIGHT = 0.50;       // tooth height above the bar body (Z)

// ---- the rotor/pawl column, mirrored from s5r_register.scad --------------
ROTOR_RADIUS = 1.5;
PAWL_T = 0.90;                  // pawl thickness in X (pitch direction)
PAWL_W = 0.70;                  // pawl width in Y (row direction)
PAWL_LEN = 8.00;                // cantilever length (Z)
PAWL_XY_CLEAR = 0.40;           // designed pawl-to-rack lateral free play
CELL_H = 7.0;                   // S5 cell height (rotor hub top above rack top)
KEEPER_T = 0.90;                // DND-59: re-profiled to 2 lines (was 0.45)
KEEPER_GATE_STEP = 0.35;        // height a dropped pawl is held clear

// ---- reset comber (one reverse pass trips every dropped pawl) -------------
// DND-59: the keeper moved to +Y (row direction), so the X-gap between column
// stacks now holds only the pawl (PAWL_T = 0.90 in 5.08), leaving >4.1 mm of
// free X. The comber tines ride that X-gap, and at Y = -0.30 they are also
// clear of the keeper (which occupies +Y 0.35..1.25). It swings in Z: parked
// low, then up to the pawl plane to trip a dropped pawl over-centre.
COMBER_TINE_T = 0.90;           // tine thickness (X): 2 lines, robust printed rake tine
COMBER_TINE_L = 14.0;           // tine length (Z)
COMBER_Z_LOW = -2.0;            // comber park position (below the pawl tips)
COMBER_Z_HIGH = 6.0;            // comber trip position (over-centre travel)
COMBER_BODY_CLEAR = 0.50;       // designed clearance body-to-column in X

// ---- writer carriage (40 solenoids, off the dense field) ------------------
CARRIAGE_X = 44.0;              // carriage body length in X (carries writers)
CARRIAGE_Y = 24.0;              // carriage body depth in Y (clears the R rows)
CARRIAGE_Z = 26.0;              // carriage body height in Z
CARRIAGE_WALL = 1.20;           // printed carriage wall (2 lines is 0.88; 1.2 robust)
CARRIAGE_LIFT = 2.0;            // writer stroke in Z (solenoid push)
CARRIAGE_CLEAR = 0.60;          // designed clearance to the column tops (Z)
// column top (hub top) = RACK_TOOTH_HEIGHT + PAWL_LEN + CELL_H (declared here
// so the carriage datum is derived, not hard-coded)
COLUMN_TOP = RACK_TOOTH_HEIGHT + 0.01 + PAWL_LEN + CELL_H;
CARRIAGE_NOSE_Z0 = COLUMN_TOP + CARRIAGE_CLEAR;   // nose bottom
CARRIAGE_NOSE_L = 2.0;          // nose length

$fn = 48;
EPS = 0.01;

// -------------------------------------------------------------------------
// A single column (X) at one row (Y): rotor hub + engaged pawl + keeper.
// Everything in the column lives ABOVE the tooth-top plane, because the rack
// spans the full X range below it; only the pawl TIP reaches down to
// base = RACK_TOOTH_HEIGHT + EPS, the intended contact plane.
// Engaged: tip at base. Dropped: the whole pawl is raised by KEEPER_GATE_STEP.
// -------------------------------------------------------------------------
module one_column(row_i = 0, dropped = false) {
    y = row_i * ROW_PITCH;
    base = RACK_TOOTH_HEIGHT + EPS;
    z0 = dropped ? base + KEEPER_GATE_STEP : base;
    translate([0, y, 0]) {
        // drive pawl leaf: hangs from the hub down toward the rack
        translate([-PAWL_T / 2, -PAWL_W / 2, z0])
            cube([PAWL_T, PAWL_W, PAWL_LEN]);
        // rotor hub sits on top of the pawl (cantilever root)
        translate([0, 0, base + PAWL_LEN]) cylinder(r = ROTOR_RADIUS, h = CELL_H);
        // keeper leaf outboard in +Y (ROW direction), BESIDE the pawl -- DND-59
        // moved the keeper out of the pitch (X) band so it does not consume it.
        translate([-PAWL_T / 2, PAWL_W / 2, base])
            cube([PAWL_T, KEEPER_T, PAWL_LEN + CELL_H]);
    }
}

module bank_columns(dropped_col = -1, dropped_row = -1) {
    for (c = [0:BANK_COLS_MODEL - 1])
        translate([c * PITCH - (BANK_COLS_MODEL - 1) * PITCH / 2, 0, 0])
            for (r = [0:BANK_ROWS - 1])
                one_column(r, dropped = (c == dropped_col && r == dropped_row));
}

// -------------------------------------------------------------------------
// Shared drive bar with R parallel rack strips (one per row). Tooth tops at
// z = 0, bar body from -BAR_UNDER to 0. Each rack strip is BAR_W wide in Y and
// centred on its row, so the engaged pawl (0.70 wide) is centred on it.
// -------------------------------------------------------------------------
module drive_bar() {
    x0 = -(BANK_COLS_MODEL - 1) * PITCH / 2 - PITCH;
    x1 = (BANK_COLS_MODEL - 1) * PITCH / 2 + PITCH;
    len = x1 - x0;
    translate([x0, -BAR_W / 2, -BAR_UNDER]) cube([len, BAR_W, BAR_UNDER]);
    for (r = [0:BANK_ROWS - 1])
        translate([x0, r * ROW_PITCH - BAR_W / 2, -BAR_UNDER])
            for (t = [0:floor(len / RACK_TOOTH_PITCH)])
                translate([t * RACK_TOOTH_PITCH, 0, 0])
                    cube([RACK_TOOTH_HEIGHT, BAR_W, BAR_UNDER + RACK_TOOTH_HEIGHT]);
}

// -------------------------------------------------------------------------
// Reset comber: a rake of tines that swings up through the pawl line to trip
// dropped pawls back over centre. The body is a rail OFF the dense field, to
// +X of the modelled span; its tines pass between columns (one per column).
// -------------------------------------------------------------------------
module reset_comber(z = COMBER_Z_LOW) {
    x_body = (BANK_COLS_MODEL - 1) * PITCH / 2 + 6 * PITCH;
    translate([x_body, -BAR_W / 2, -4]) cube([4.0, (BANK_ROWS - 1) * ROW_PITCH + BAR_W, 8.0]);
    // tines at the MIDPOINTS between column stacks (half-pitch offset), so they
    // are clear of every pawl/keeper in X
    for (c = [0:BANK_COLS_MODEL - 2], r = [0:BANK_ROWS - 1])
        translate([c * PITCH - (BANK_COLS_MODEL - 1) * PITCH / 2 + PITCH / 2 - COMBER_TINE_T / 2,
                   r * ROW_PITCH - 0.30, z])
            cube([COMBER_TINE_T, 0.60, COMBER_TINE_L]);
}

// -------------------------------------------------------------------------
// Writer carriage: a block that travels in X ABOVE the rows and carries the
// writer bank; its sweep envelope is the collision object.
// -------------------------------------------------------------------------
module writer_carriage(x = 0) {
    translate([x - CARRIAGE_X / 2, -CARRIAGE_Y / 2, CARRIAGE_NOSE_Z0 + CARRIAGE_NOSE_L])
        cube([CARRIAGE_X, CARRIAGE_Y, CARRIAGE_Z]);
}
module writer_sweep_envelope() {
    // The sweep is a translation in X, so its envelope is a single box spanning
    // the travel range; the Y/Z extent is the carriage cross-section.
    x_start = -(BANK_COLS_MODEL - 1) * PITCH / 2 - CARRIAGE_X / 2;
    x_end = (BANK_COLS_MODEL - 1) * PITCH / 2 + CARRIAGE_X / 2;
    translate([x_start, -CARRIAGE_Y / 2, CARRIAGE_NOSE_Z0 + CARRIAGE_NOSE_L])
        cube([x_end - x_start, CARRIAGE_Y, CARRIAGE_Z]);
    // writer noses that reach down toward the keepers, within the sweep
    translate([x_start, -CARRIAGE_Y / 2 + 2.0, CARRIAGE_NOSE_Z0])
        cube([x_end - x_start, CARRIAGE_Y - 4.0, CARRIAGE_NOSE_L]);
}

// -------------------------------------------------------------------------
// Assemblies
// -------------------------------------------------------------------------
module bank_assembly() {
    drive_bar();
    bank_columns();
}

// ---- interference queries -------------------------------------------------
// Intended contact is separated by EPS, so a non-empty result is a collision.
// "run": every pawl engaged (tip at z = EPS, just above the tooth top at 0).
module collision_run() {
    intersection() { bank_columns(); drive_bar(); }
}
// "selected": one dropped pawl must not touch the rack or its neighbour.
module collision_selected() {
    intersection() {
        bank_columns(dropped_col = 3, dropped_row = 1);
        drive_bar();
    }
}
// The comber at low/high extremes must not touch a raised (engaged) column.
module collision_comber_low() {
    intersection() { bank_columns(); reset_comber(COMBER_Z_LOW); }
}
module collision_comber_high() {
    intersection() { bank_columns(); reset_comber(COMBER_Z_HIGH); }
}
// The writer sweep must not touch the column tips.
module collision_carriage() {
    intersection() { bank_columns(); writer_sweep_envelope(); }
}

// part = "assembly" | "columns" | "bar" | "comber" | "carriage" | "envelope"
//      | "run" | "selected" | "comber_low" | "comber_high" | "carriage_sweep"
part = "assembly";

if (part == "assembly") bank_assembly();
else if (part == "columns") bank_columns();
else if (part == "bar") drive_bar();
else if (part == "comber") reset_comber();
else if (part == "carriage") writer_carriage();
else if (part == "envelope") writer_sweep_envelope();
else if (part == "run") collision_run();
else if (part == "selected") collision_selected();
else if (part == "comber_low") collision_comber_low();
else if (part == "comber_high") collision_comber_high();
else if (part == "carriage_sweep") collision_carriage();
