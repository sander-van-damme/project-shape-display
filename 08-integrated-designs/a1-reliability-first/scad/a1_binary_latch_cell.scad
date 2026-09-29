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

// ---- DND-114 common-height read target (latch-hinge flag) ------------------
// The as-drawn reader targets the column TOP FACE, which moves TRAVEL=40 mm with
// the state: a down cell is read at ~42 mm with a ~24.5 mm spot (4.82 pitches),
// swamped ~441x by up neighbours (DND-113 ADR). The fix is a target at ONE z for
// both states. Two variants are modelled:
//
//   CH-A  frame-fixed reflective vane: a post on the frame cradle in the latch
//         lane, top face at Z_FLAG_TOP -- z does NOT move with the column, so
//         the target is common-height BY CONSTRUCTION (DeltaZ = 0).
//   CH-B  arm-carried reflective flag: a small vane on the latch arm at radius
//         FLAG_R from the hinge axis. Its mean z shifts by the hinge arc
//         DeltaZ = FLAG_R * (sin(max) - sin(min)); the bound is DeltaZ <= DOF.
//
// Both sit in the LATCH LANE at x = HINGE_X (frame-fixed), clear of the column
// body (own edge x=BODY/2=1.80) and the neighbour body (inner edge
// x=PITCH-BODY/2=3.28). The lane is open in Y across the full pitch, so the
// read spot may spread in Y; only the X half-width is bounded by the lane.
HINGE_X       = BODY/2 + LATCH_T/2 + CLEAR;   // 2.225 mm, matches assembly
FLAG_T        = 0.44;   // flag width in X (1 line @0.4 mm nozzle)
FLAG_W        = 1.60;   // flag width in Y (fits lane; >= spot_Y)
FLAG_H        = 0.80;   // flag post height in Z (frame-fixed vane)
FLAG_R        = 1.20;   // CH-B: radius of the arm flag from the hinge axis
Z_FLAG_TOP    = TRAVEL + 3.0;  // fixed target top face z (above the UP top)
DOF_BUDGET    = 1.0;    // DND-112 pass: target within +/-1 mm
SWING_DEG     = 30.0;   // assumption-class full latch toggle swing

X_CLEAR_NB    = PITCH - BODY/2 - HINGE_X;     // 1.055 mm to neighbour body
X_CLEAR_OWN   = HINGE_X - BODY/2;             // 0.425 mm to own body
FLAG_FITS_X   = FLAG_T/2 <= X_CLEAR_NB;
// CH-B hinge-arc DeltaZ: symmetric swing about the hinge axis.
FLAG_DELTA_Z  = FLAG_R * 2 * sin(SWING_DEG/2);
FLAG_IN_DOF   = FLAG_DELTA_Z <= DOF_BUDGET;
R_FLAG_MAX    = DOF_BUDGET / (2*sin(SWING_DEG/2));  // max arm radius in DoF

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

module ch_a_frame_vane() {
    // DND-114 CH-A: frame-fixed reflective vane.
    // A post on the frame cradle in the latch lane; its top face is the read
    // target and is at a single fixed z (Z_FLAG_TOP) for BOTH column states,
    // because the cradle is frame-anchored. DeltaZ = 0 by construction.
    // Rendered in Mirror/Gold to read as the reflective target face.
    translate([HINGE_X, 0, Z_FLAG_TOP - FLAG_H/2])
        color("Gold")
            cube([FLAG_T, FLAG_W, FLAG_H], center=true);
    // reflective top face highlighted
    translate([HINGE_X, 0, Z_FLAG_TOP + 0.01])
        color("Khaki")
            cube([FLAG_T, FLAG_W, 0.02], center=true);
}

module ch_b_arm_flag(swing = 0) {
    // DND-114 CH-B: arm-carried reflective flag.
    // A small vane on the latch arm at radius FLAG_R from the hinge axis; it
    // rotates with the arm so the target tilt encodes state. Its mean z shifts
    // by the hinge arc: DeltaZ = FLAG_R * (sin(max)-sin(min)). Modelled at the
    // two toggle extremes (+/-SWING_DEG/2 about the hinge).
    translate([HINGE_X, 0, TRAVEL/2])                 // hinge axis (frame-fixed)
        rotate([swing, 0, 0])                          // swing about the hinge
            translate([0, 0, FLAG_R])
                color("DarkOrange")
                    cube([FLAG_T, FLAG_W, FLAG_H], center=true);
}

// ---- assembly (viewing) ----------------------------------------------------
module cell_assembly() {
    color("SteelBlue") column();
    translate([BODY/2 + LATCH_T/2 + CLEAR, 0, TRAVEL/2])
        color("Orange") latch_arm();
    translate([0, 0, -COL_LEN/2 - 1.5]) color("Gainsboro") cradle_land();
    // DND-114: both candidate common-height targets (read at one standoff).
    ch_a_frame_vane();
    ch_b_arm_flag(+SWING_DEG/2);
    ch_b_arm_flag(-SWING_DEG/2);
}

module common_height_target() {
    // -D part="flag" renders CH-A (the frame-fixed vane) as a printable part.
    ch_a_frame_vane();
}

module part_selector() {
    // -D part="<key>" renders one printable part for mesh validation.
    // `part` is supplied by -D; the default below is used for interactive runs.
    if (part == "column") column();
    else if (part == "latch") latch_arm();
    else if (part == "cradle") cradle_land();
    else if (part == "flag") common_height_target();
    else cell_assembly();
}

part_selector();

// ---- self-checks (echoed, captured by the render tool) ---------------------
echo(str("PITCH=", PITCH, " BODY=", BODY, " OWNED_LANE=", OWNED_LANE));
echo(str("LATCH_T+CLEAR=", LATCH_T + CLEAR, " <= OWNED_LANE=", OWNED_LANE));
echo(str("latch fits owned lane: ", (LATCH_T + CLEAR) <= OWNED_LANE));
echo(str("min feature check (latch): ", LATCH_T >= 0.44));
echo(str("stop land (2 lines): ", STOP_LAND >= 0.88));
// DND-114 common-height read target self-checks.
echo(str("HINGE_X=", HINGE_X, " X_CLEAR_NB=", X_CLEAR_NB, " X_CLEAR_OWN=", X_CLEAR_OWN));
echo(str("CH flag fits lane in X: ", FLAG_FITS_X, " (FLAG_T/2=", FLAG_T/2,
         " <= X_CLEAR_NB=", X_CLEAR_NB, ")"));
echo(str("CH-A target is frame-fixed: DeltaZ=0 at Z_FLAG_TOP=", Z_FLAG_TOP));
echo(str("CH-B hinge-arc DeltaZ=", FLAG_DELTA_Z, " mm (DOF budget ",
         DOF_BUDGET, " mm); in DoF: ", FLAG_IN_DOF));
echo(str("CH-B max arm radius in DoF: R_FLAG_MAX=", R_FLAG_MAX, " mm"));
echo(str("min feature check (flag): ", FLAG_T >= 0.44));
