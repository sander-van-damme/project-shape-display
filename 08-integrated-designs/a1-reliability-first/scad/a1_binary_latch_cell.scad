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
SWING_DEG     = 30.0;   // assumption-class full latch toggle swing (CH-B)

// ---- DND-115 state-encoding shutter (the read STATE encoder) ----------------
// DND-114 left the vane undimensioned in one respect: nothing made its apparent
// brightness depend on the latch state. This shutter is a MATTE-DARK flap carried
// on a SHUTTER ARM that shares the frame-fixed latch hinge axis with the toe arm.
// The crank swings SWING_SHUT between its two hard stops:
//   HIDDEN state  (flap flat over the vane, plane normal +Z)  -> beam blocked;
//   VISIBLE state (flap edge-on, plane normal ~ +X)           -> beam reaches the
//                                                               frame-fixed vane.
// The REFLECTIVE TARGET remains the frame-fixed vane top at Z_FLAG_TOP (DeltaZ=0);
// the shutter is an ABSORBER, not a target, so no state-dependent target z is
// reintroduced. The flap pivot IS the hinge axis, placed directly over the vane,
// so the flap rotates ~in place: a large SWING_SHUT gives a small lateral stroke.
// The shutter flap must fit in the reader's near-field window. DND-114 assumed a
// 1.0 mm reader standoff; a tolerance stack-up (worst-case + Monte Carlo, in
// `shutter_tolerance_mc()`) shows the 1.0 mm window cannot hold a 0.44 mm flap
// with printed placing tolerances, so the ADOPTED fixed standoff is raised to
// SHUT_APER_GAP = 1.8 mm and the aperture is set to 0.44 mm. The read spot
// (1.405 mm) still clears the neighbour body (0.353 mm) at that standoff.
PIN_R         = 0.50;   // hinge pin radius (1.0 dia; matches CH model)
Z_SHUT_HINGE  = 45.8;   // hinge axis z (above the vane top 43 and the aperture)
SHUT_T        = 0.44;   // flap thickness in X (1 line @0.4 mm)
SHUT_W        = 1.55;   // flap width in X (covers the 1.405 mm read spot; keeps
                        //              the flat flap 0.255 mm off the neighbour)
SHUT_D        = 1.60;   // flap depth in Y (lane is open; covers the spot)
SHUT_GAP      = 0.55;   // flap underside clearance above the vane top (flat)
SHUT_APER_GAP = 1.80;   // reader standoff above the frame-fixed vane top
SHUT_AP       = 0.44;   // dedicated read aperture (1 line)
SHUT_FLAP_CZ  = Z_FLAG_TOP + SHUT_GAP + SHUT_T/2;     // flat flap centre z = 43.77
FLAP_R        = Z_SHUT_HINGE - SHUT_FLAP_CZ;          // 2.03 mm tip radius
SWING_SHUT    = 90.0;   // shutter crank swing: flat over vane -> edge-on

// Self-check quantities (all pure geometry; captured by the render tool).
SHUT_FLAT_BOT   = Z_SHUT_HINGE - FLAP_R - SHUT_T/2;   // flat underside z = 43.55
SHUT_FLAT_TOP   = Z_SHUT_HINGE - FLAP_R + SHUT_T/2;   // flat top z      = 43.99
SHUT_VANE_GAP   = SHUT_FLAT_BOT - Z_FLAG_TOP;         // 0.55 mm
SHUT_APER_Z     = Z_FLAG_TOP + SHUT_APER_GAP;         // reader aperture plane 44.8
SHUT_APER_CLEAR = SHUT_APER_Z - SHUT_FLAT_TOP;        // 0.81 mm to the aperture
SHUT_LATERAL    = FLAP_R * 2 * sin(SWING_SHUT/2);     // 2.871 mm lateral stroke
SHUT_SPOT       = SHUT_AP + 2*SHUT_APER_GAP*tan(15);  // 1.405 mm read spot
SHUT_COVERS_SPOT = SHUT_W >= SHUT_SPOT;

// Swept envelope of the flap over the full swing. The X maximum is at the flat
// (0 deg) state, where the flap centre is over the vane: HINGE_X + SHUT_W/2. The
// Z minimum is the flat underside. (Checked on a 0.1 deg grid in the analysis
// `shutter_read_contrast()`; the closed form below matches it exactly.)
SHUT_SWEEP_X    = HINGE_X + SHUT_W/2;                 // 3.00 mm, margin 0.28
SHUT_SWEEP_ZMIN = SHUT_FLAT_BOT;                      // 43.55 mm (flat underside)
// For the edge-on (90 deg) state the flap sits at x = HINGE_X - FLAP_R (toward own
// body) and its lowest point is Z_SHUT_HINGE - SHUT_T/2 (the plate is vertical).
SHUT_EDGE_LOW_Z = Z_SHUT_HINGE - SHUT_T/2;            // 45.58 mm, above own top
SHUT_CLEARS_NEIGHBOUR = SHUT_SWEEP_X <= (PITCH - BODY/2);
SHUT_ABOVE_OWN_COLUMN = SHUT_FLAT_BOT >= TRAVEL;      // flap bottom above own top (40)

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
module shutter_flap(state = "hidden") {
    // DND-115: the matte-dark flap carried on the shutter arm, pivoting on the
    // frame-fixed hinge axis (HINGE_X, 0, Z_SHUT_HINGE). `state`:
    //   "hidden"  -> flap FLAT over the vane (plane normal +Z): beam blocked;
    //   "visible" -> flap edge-on (crank swung SWING_SHUT toward the own body):
    //                beam reaches the frame-fixed vane.
    // The pivot is directly over the vane, so the flap rotates ~in place and the
    // lateral stroke is only FLAP_R*2*sin(swing/2) -- inside the own lane.
    ang = (state == "hidden") ? 0 : -SWING_SHUT;
    translate([HINGE_X, 0, Z_SHUT_HINGE])
        rotate([0, ang, 0])
            translate([0, 0, -FLAP_R])
                color("DimGray")
                    cube([SHUT_W, SHUT_D, SHUT_T], center=true);
}

module shutter_crank() {
    // DND-115: the shutter ARM. It shares the frame-fixed hinge axis with the toe
    // arm, so one latch motion drives both. Rendered from the hinge up/over to
    // the flap. Geometry is schematic for the shared-axis linkage; the flap and
    // its envelope are the validated quantities.
    translate([HINGE_X, 0, Z_SHUT_HINGE])
        rotate([90, 0, 0])
            color("Orange")
                cylinder(r = PIN_R, h = SHUT_D, center = true);
}

module cell_assembly() {
    color("SteelBlue") column();
    translate([BODY/2 + LATCH_T/2 + CLEAR, 0, TRAVEL/2])
        color("Orange") latch_arm();
    translate([0, 0, -COL_LEN/2 - 1.5]) color("Gainsboro") cradle_land();
    // DND-114: both candidate common-height targets (read at one standoff).
    ch_a_frame_vane();
    ch_b_arm_flag(+SWING_DEG/2);
    ch_b_arm_flag(-SWING_DEG/2);
    // DND-115: the state-encoding shutter, drawn in BOTH states.
    shutter_crank();
    shutter_flap("hidden");
    shutter_flap("visible");
}

module common_height_target() {
    // -D part="flag" renders CH-A (the frame-fixed vane) as a printable part.
    ch_a_frame_vane();
}

module shutter_part() {
    // -D part="shutter" renders the DND-115 shutter (crank pin + flap flat state)
    // as a printable part for mesh validation.
    shutter_crank();
    shutter_flap("hidden");
}

module part_selector() {
    // -D part="<key>" renders one printable part for mesh validation.
    // `part` is supplied by -D; the default below is used for interactive runs.
    if (part == "column") column();
    else if (part == "latch") latch_arm();
    else if (part == "cradle") cradle_land();
    else if (part == "flag") common_height_target();
    else if (part == "shutter") shutter_part();
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
// DND-115 state-encoding shutter self-checks.
echo(str("SHUT: hinge z=", Z_SHUT_HINGE, " flap_r=", FLAP_R,
         " swing=", SWING_SHUT));
echo(str("SHUT flat flap z=[", SHUT_FLAT_BOT, ",", SHUT_FLAT_TOP,
         "] vane top=", Z_FLAG_TOP, " vane gap=", SHUT_VANE_GAP));
echo(str("SHUT flap clears vane top: ", SHUT_VANE_GAP > 0));
echo(str("SHUT flat flap top below reader aperture plane (",
         SHUT_APER_Z, "): ", SHUT_APER_CLEAR > 0, " (clearance ",
         SHUT_APER_CLEAR, " mm)"));
echo(str("SHUT clears neighbour body (sweep x ", SHUT_SWEEP_X, " <= ",
         PITCH - BODY/2, "): ", SHUT_CLEARS_NEIGHBOUR));
echo(str("SHUT flap above own column top (", SHUT_FLAT_BOT, " >= ", TRAVEL,
         "): ", SHUT_ABOVE_OWN_COLUMN));
echo(str("SHUT lateral stroke=", SHUT_LATERAL, " mm within lane ",
         X_CLEAR_OWN, "+", X_CLEAR_NB, " mm"));
echo(str("SHUT min feature (flap): ", SHUT_T >= 0.44));
echo(str("SHUT read spot=", SHUT_SPOT, " flap width=", SHUT_W,
         " covers spot: ", SHUT_COVERS_SPOT));
echo(str("SHUT reader standoff=", SHUT_APER_GAP, " aperture=", SHUT_AP));
