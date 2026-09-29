// DND-60 S5-R fabrication package -- shared part constants (single source of truth).
//
// This file carries the geometric constants for EVERY printed part of the S5-R
// machine. It is `include`d by `s5r_parts.scad` (the part-set library) and read
// by `tools/gen_manifests.py` / `tools/fab_package_checks.py` so the printable
// geometry, the print manifest and the CI coherence gate all track ONE source.
//
// COHERENCE. The values here are the same ones carried by the promoted model
// (`06-experiments/test12_winner_convergence/s5r_register.py`,
// `s5r_register.scad`, `s5r_bank.py`, `s5r_bank.scad`). The CI gate
// `tools/verify_fab_constants.py` asserts they match; if a model constant moves,
// the gate fails until this package is re-generated.
//
// EVIDENCE CLASS: CAD geometry (this file + its real-OpenSCAD STL renders).
// It is NOT a print and NOT a measurement ([DND-27]).
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

// ---------------------------------------------------------------------------
// Field / cell (DND-54; from test08 results/parameters.scad).
// ---------------------------------------------------------------------------
PITCH = 5.08;
ROW_PITCH = 5.08;
ROTOR_RADIUS = 1.5;
ROTOR_CORE_RADIUS = 1.0;
LEVELS = 5;
LEVEL_ANGLE = 360 / LEVELS;      // 72 deg per level
COLUMN_LEN = 80.2;               // S5 column body (leaves 0.40 mm top gap)
COLUMN_SQ = 4.68;                // S5 column square body

// ---------------------------------------------------------------------------
// Printed drive pawl (load-bearing vertical cantilever; DND-54/DND-59).
// ---------------------------------------------------------------------------
PAWL_T = 0.90;                   // thickness in X (pitch direction); 2 lines
PAWL_W = 0.70;                   // width in Y (row direction)
PAWL_LEN = 8.00;                 // Z cantilever length
PAWL_DEFLECT = 0.10;

// ---------------------------------------------------------------------------
// Keeper latch (DND-59 re-profile: 0.90 mm = 2 lines, hard compression shoulder,
// placed in the ROW (Y) direction beside the pawl).
// ---------------------------------------------------------------------------
KEEPER_T = 0.90;
KEEPER_W = 0.70;
KEEPER_LEN = 4.00;
KEEPER_OVER_CENTRE = 0.06;
KEEPER_GATE_STEP = 0.35;
KEEPER_SHOULDER_X = 0.50;

// ---------------------------------------------------------------------------
// Drive rack + sourced bar (DND-58 corrected rack; sourced steel rod).
// ---------------------------------------------------------------------------
RACK_TOOTH_PITCH = 1.00;
RACK_TOOTH_HEIGHT = 0.50;
BAR_D = 6.0;                     // sourced steel rod diameter (not printed)
RACK_STRIP_W = 3.0;              // printed rack strip width (Y) per row

// ---------------------------------------------------------------------------
// Cell housing / bank geometry.
// ---------------------------------------------------------------------------
CELL_H = 7.0;
WALL = 0.90;                     // robust infill-free wall (>= 2 lines)
SLOT_CLEAR = 0.15;
ROTOR_BORE_CLEAR = 0.40;
EPS = 0.01;

// ---------------------------------------------------------------------------
// Machine layout (S5-R R=4).
// ---------------------------------------------------------------------------
COLS = 80;
ROWS_FULL = 80;
BANK_ROWS = 4;                   // R = 4 rows per bank pass
BANK_SPAN = COLS * PITCH;        // 406.4 mm in-row span
FIELD_SPAN = ROWS_FULL * ROW_PITCH;  // 406.4 mm cross-row span

// ---------------------------------------------------------------------------
// Modular cartridge (X1C 256 mm bed; DND-43 <= ~150 mm support spacing).
// The 406.4 mm field splits into 3 cartridges per axis (~135.5 mm).
// ---------------------------------------------------------------------------
CARTRIDGE_COLS = 27;             // 27 * 5.08 = 137.16 mm <= 150 mm
CARTRIDGE_ROWS = 27;
CARTRIDGE_W = CARTRIDGE_COLS * PITCH;   // 137.16
CARTRIDGE_D = CARTRIDGE_ROWS * ROW_PITCH;
CARTRIDGE_H = CELL_H + BAR_D + 1.0;     // housing floor to rotor top
FRAME_RAIL = 8.0;                // module frame rail width (X/Y)
FRAME_RAIL_H = 4.0;

// ---------------------------------------------------------------------------
// Bank / drive housing (DND-55/DND-58).
// ---------------------------------------------------------------------------
BAR_H = 12.0;                    // printed on-edge inspection section (bar body)
BANK_MOTOR_PINION_R = 6.0;
WRITER_FORCE_N = 1.2;

// ---------------------------------------------------------------------------
// Reset comber (DND-55/DND-59).
// ---------------------------------------------------------------------------
COMBER_TINE_T = 0.90;
COMBER_TINE_L = 14.0;
COMBER_BODY_L = 4.0;
COMBER_BODY_W = (BANK_ROWS - 1) * ROW_PITCH + RACK_STRIP_W;   // 12.24
COMBER_BODY_H = 8.0;
COMBER_Z_LOW = -2.0;
COMBER_Z_HIGH = 6.0;

// ---------------------------------------------------------------------------
// Writer carriage (40 stations; DND-55).
// ---------------------------------------------------------------------------
CARRIAGE_X = 44.0;
CARRIAGE_Y = 24.0;
CARRIAGE_Z = 26.0;
CARRIAGE_WALL = 1.20;
CARRIAGE_NOSE_L = 2.0;
CARRIAGE_CLEAR = 0.60;
COLUMN_TOP = RACK_TOOTH_HEIGHT + EPS + PAWL_LEN + CELL_H;
CARRIAGE_NOSE_Z0 = COLUMN_TOP + CARRIAGE_CLEAR;

// ---------------------------------------------------------------------------
// Platen / lift frame and brackets (S5 common lift; DND-43).
// ---------------------------------------------------------------------------
PLATEN_T = 4.0;
PLATEN_RIB = 3.0;                // printed stiffening rib width
LIFT_SCREW_R = 4.0;              // T8 lead-screw clearance radius
LIFT_SCREW_BORE = 2 * LIFT_SCREW_R + 0.4;
BRACKET_T = 3.0;
BRACKET_W = 16.0;
BRACKET_H = 20.0;
GUIDE_ROD_R = 4.0;               // 8 mm guide rod radius
GUIDE_BORE = 2 * GUIDE_ROD_R + 0.4;

$fn = 48;
