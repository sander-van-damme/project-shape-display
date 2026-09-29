// DND-54 S5-R register unit cell -- CAD evidence for the dropout latch.
//
// This is a SINGLE-COLUMN unit cell of the shared-drive programmable rotary
// register (the S5-R pivot). It is NOT a full machine and NOT a print. Its job
// is to let the analytic printability gate read the declared feature sizes and
// to let a real OpenSCAD render + mesh-validate that the latch + rotor bank
// geometry is a closed solid at the 5.08 mm pitch.
//
// The constants below are the source of truth parsed by
// tools/validate/analytic_printability.py and recomputed by s5r_register.py.
// Keep the two in sync.
//
// EVIDENCE CLASS: CAD (this file + its STL render). Not a print, not a
// measurement. See 07-evidence-and-decisions/dnd54-s5r-register-latch.md.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle (tools/fdm-limits).

// ---- cell / rotor (unchanged S5 geometry, test08 parameters.scad) ----
PITCH = 5.08;
ROTOR_RADIUS = 1.5;
ROTOR_CORE_RADIUS = 1.0;
BASE = 2.0;
LEVELS = 5;
LEVEL_ANGLE = 360 / LEVELS;     // 72 deg

// ---- printed drive pawl (vertical cantilever, load-bearing = 2 lines) ----
PAWL_T = 0.90;                  // thickness in X (pitch direction); 2 lines
PAWL_W = 0.70;                  // width in Y (row direction)
PAWL_LEN = 8.00;                // Z extent of the cantilever
PAWL_DEFLECT = 0.10;            // working deflection off the rack tooth

// ---- keeper latch (bistable over-centre leaf, 5-position gate) ----
KEEPER_T = 0.45;                // thickness in X (light latch; 1 line)
KEEPER_W = 0.70;                // width in Y
KEEPER_LEN = 3.00;              // Z cantilever
KEEPER_OVER_CENTRE = 0.06;      // bistability offset
KEEPER_GATE_STEP = 0.35;        // spacing of the 5 gate positions

// ---- shared drive bar with rack ----
// DND-58 (from DND-55 bank close-out): DND-54's rack (pitch 0.60, tooth 0.45)
// left a 0.15 mm inter-tooth gap that FUSES at a 0.4 mm nozzle (< 0.44 mm line).
// Re-dimensioned to pitch 1.00 / tooth 0.50 -> 0.50 mm gap. The per-stroke
// advance is therefore 1.00 mm (one tooth) instead of 0.60 mm.
RACK_TOOTH_PITCH = 1.00;
RACK_TOOTH_HEIGHT = 0.50;
BAR_D = 6.0;                    // sourced steel drive rod d=6 (DND-58); a round bar
BAR_H = BAR_D;                  // (round steel; replaces the 3x2 printed placeholder)
BAR_W = PITCH;                  // bar spans one column here; real bar is 80xR

// ---- housing ----
CELL_H = 7.0;
WALL = 0.90;                    // robust infill-free wall (>= 2 lines)
SLOT_CLEAR = 0.15;              // guide clearance (worst case >= 0.20 after print)
ROTOR_BORE_CLEAR = 0.40;        // total diametral rotor-to-bore free play

$fn = 48;
EPS = 0.01;

module rotor() {
    cylinder(r = ROTOR_RADIUS, h = BASE);
    translate([0, 0, BASE]) cylinder(r = ROTOR_CORE_RADIUS, h = CELL_H - BASE);
}

module pawl() {
    // a thin vertical leaf, attached to the hub at its top, tip down at the rack
    translate([0, -PAWL_W / 2, 0]) cube([PAWL_T, PAWL_W, PAWL_LEN]);
}

module keeper() {
    // a leaf offset outboard of the pawl in +X, with an over-centre nose
    translate([PAWL_T + KEEPER_OVER_CENTRE, -KEEPER_W / 2, 0])
        cube([KEEPER_T, KEEPER_W, KEEPER_LEN]);
    // gate nose: 5 stacked positions (the writer moves the keeper index)
    for (k = [0:LEVELS - 1])
        translate([PAWL_T + KEEPER_OVER_CENTRE + KEEPER_T, -KEEPER_W / 2,
                   k * KEEPER_GATE_STEP])
            cube([0.20, KEEPER_W, 0.15]);
}

module drive_bar() {
    // the toothed rack under the pawl tip. DND-58: the bar is a SOURCED STEEL
    // ROD (d=6 mm), modelled here as the round bar body; the rack teeth are the
    // corrected 1.00/0.50 pitch/height.
    translate([0, 0, -BAR_H / 2]) rotate([90, 0, 0])
        cylinder(r = BAR_D / 2, h = BAR_W, center = true);
    for (t = [0:3])
        translate([-BAR_W / 2 + t * RACK_TOOTH_PITCH, -BAR_W / 2, 0])
            cube([RACK_TOOTH_HEIGHT, BAR_W, RACK_TOOTH_HEIGHT]);
}

module cell() {
    // housing: a square tube with a floor, open toward +Z for the rotor
    difference() {
        translate([-PITCH / 2, -PITCH / 2, -BAR_H - 1])
            cube([PITCH, PITCH, CELL_H + BAR_H + 1]);
        // rotor bore
        translate([0, 0, -BAR_H - 1 - EPS]) cylinder(r = ROTOR_RADIUS + 0.10,
                                                     h = CELL_H + 2 * EPS);
        // pawl + keeper side chamber (open slot)
        translate([PAWL_T / 2, -PITCH / 2 - EPS, -BAR_H - 1 - EPS])
            cube([PITCH / 2, PITCH + 2 * EPS, CELL_H + 2 * EPS]);
    }
}

module unit_cell_assembly() {
    cell();
    rotor();
    translate([0, 0, BASE + 1]) pawl();
    translate([0, 0, BASE + 1]) keeper();
    drive_bar();
}

// part = "cell" | "assembly" | "pawl" | "keeper";
part = "assembly";

if (part == "assembly") {
    unit_cell_assembly();
} else if (part == "cell") {
    cell();
} else if (part == "pawl") {
    pawl();
} else if (part == "keeper") {
    keeper();
}
