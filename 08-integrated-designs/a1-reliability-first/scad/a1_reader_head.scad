// DND-111 + DND-113 — A1 reader-head optical geometry at the 5.08 mm pitch
// (real OpenSCAD)
//
// Bounds the SINGLE-CELL READ RESOLUTION question from CAD + geometry:
// can one wrong cell among 6,400 be distinguished from its neighbours?
//
// DND-113 CORRECTION (from the DND-112 audit). The reader head sits above the
// column tops at a working gap g. A single interrogation aperture of diameter
// d emits at half-angle theta. DND-111 computed ONE spot at ONE 2 mm gap and
// called it "the single-cell read". That is the UP-state spot only: the A1
// state is the column-top HEIGHT, so over a DOWN cell the reflective target is
// TRAVEL = 40 mm lower and the interrogated gap is ~42 mm, giving a ~24.5 mm
// spot (4.82 pitches). At that standoff the four up neighbours dominate the
// pocket return by ~441x, so a down cell reads UP — a silent wrong-cell
// failure. The read is NOT single-cell for the down half of the states, and
// the binding limit is the STATE-DEPENDENT STANDOFF, not a gantry registration
// tolerance.
//
// This file renders the worst case (aperture centred on a CELL CORNER) and
// echoes both states so the defect is visible in the render record. It also
// models the DND-113 PROPOSED fix: a reflective flag on the frame-anchored
// latch hinge, read at ONE standoff for both states (a common-height target).
//
// EVIDENCE CLASS: CAD geometry only. No print, no measurement (DND-27).
//
// Geometry from the placed cell CAD (a1_binary_latch_cell.scad):
//   PITCH = 5.08, BODY (column top face) = 3.60, lane = 0.74 each side.

PITCH      = 5.08;
BODY       = 3.60;         // column top face (square)
TRAVEL     = 40.0;         // column top at full up = 40 mm
OWNED_LANE = PITCH/2 - BODY/2;   // 0.74 mm

WORK_GAP   = 2.0;          // reader-to-UP-top working gap (assumption-class)
APERTURE   = 2.0;          // single-cell interrogation aperture (assumption-class)
HALF_ANGLE = 15.0;         // emission half-angle (deg)
$fn = 48;

// Spot diameter where the center ray meets the target plane:
//   spot = aperture + 2 * gap * tan(half_angle)
function spot_d(gap, d, ha) = d + 2*gap*tan(ha);
SPOT_UP   = spot_d(WORK_GAP, APERTURE, HALF_ANGLE);
SPOT_DOWN = spot_d(WORK_GAP + TRAVEL, APERTURE, HALF_ANGLE);

// DND-113: the true worst-case reach is with the aperture genuinely at the CELL
// CORNER. The farthest spot point from the cell centre is the corner radius
// sqrt((BODY/2)^2 + (BODY/2)^2) plus the spot radius. DND-111's
// `spot/2*sqrt(2)` was a CENTRED aperture with a diagonal spot and understated
// the reach by ~1.9 mm.
CORNER_HYP   = sqrt((BODY/2)*(BODY/2) + (BODY/2)*(BODY/2));   // 2.546 mm
CORNER_REACH = CORNER_HYP + SPOT_UP/2;                         // 4.081 mm

// DND-113: the physical crosstalk threshold is the NEIGHBOUR's near edge, not
// the own top-face edge (DND-112 R3).
NEIGHBOUR_NEAR_EDGE = PITCH - BODY/2;                          // 3.28 mm
SPOT_CONTAMINATES = SPOT_UP/2 > NEIGHBOUR_NEAR_EDGE;

module column_up() {
    color("SteelBlue")
        translate([0, 0, TRAVEL/2 - 20])
            cube([BODY, BODY, TRAVEL], center=true);
}

module column_down() {
    color("DimGray")
        translate([0, 0, -10 - 20])
            cube([BODY, BODY, TRAVEL], center=true);
}

module reader_head() {
    // the reader head body (orange) with the interrogation aperture (yellow)
    translate([0, 0, TRAVEL + WORK_GAP + 6])
        color("Orange") cube([APERTURE + 4, APERTURE + 4, 12], center=true);
    // the cone from the aperture to the UP target top face (green: fits)
    translate([0, 0, TRAVEL + WORK_GAP/2])
        color("Gold", 0.35)
            cylinder(h = WORK_GAP, d1 = SPOT_UP, d2 = APERTURE, center=true);
}

module down_state_cone() {
    // DND-113: the same aperture aimed 40 mm lower over a DOWN cell. The
    // resulting cone is a ~24.5 mm spot that covers the whole 3x3 patch — the
    // silent-crosstalk failure the audit found.
    translate([0, 0, WORK_GAP/2])
        color("Red", 0.22)
            cylinder(h = WORK_GAP + TRAVEL, d1 = SPOT_DOWN, d2 = APERTURE,
                     center=true);
}

module neighbour_patch() {
    // a 3x3 patch with the CENTRE cell DOWN (the wrong cell) and neighbours UP
    for (i = [-1, 0, 1])
        for (j = [-1, 0, 1]) {
            x = i*PITCH; y = j*PITCH;
            if (i == 0 && j == 0) translate([x, y, 0]) column_down();
            else translate([x, y, 0]) column_up();
        }
}

module common_height_flag() {
    // DND-113 PROPOSED fix: a reflective flag on the frame-anchored latch hinge,
    // read at ONE standoff for both states.
    // ---------------------------------------------------------------------
    // DND-114 STATUS: this is now a VALIDATED-ARTIFACT read target, not a
    // schematic. The flag is the CH-A frame-fixed vane from
    // `a1_binary_latch_cell.scad`: a post in the latch lane with its top face
    // at a single fixed z for both column states (DeltaZ = 0 by construction).
    // The reader rides at a FIXED standoff above the flag plane; the neighbour
    // columns sit at x >= PITCH - BODY/2, so only the X half-width of the spot
    // can reach them. See the self-checks below.
    translate([FLAG_X, 0, FLAG_Z_TOP - FLAG_H/2])
        color("Gold") cube([FLAG_T, FLAG_W, FLAG_H], center=true);
    translate([FLAG_X, 0, FLAG_Z_TOP + 0.01])
        color("Khaki") cube([FLAG_T, FLAG_W, 0.02], center=true);
}

module flag_reader_head() {
    // DND-114: the reader head fixed above the flag plane at ONE standoff.
    // A dedicated SMALL aperture (FLAG_AP=0.60 mm) and tight standoff
    // (FLAG_GAP=1.0 mm) keep the spot off the neighbour body; the spot may
    // spread in Y because the lane is open across the full pitch.
    translate([FLAG_X, 0, FLAG_Z_TOP + FLAG_GAP + 6])
        color("Orange") cube([FLAG_AP + 4, FLAG_AP + 4, 12], center=true);
    // cone from the aperture to the frame-fixed flag top face (green: fits)
    translate([FLAG_X, 0, FLAG_Z_TOP + FLAG_GAP/2])
        color("LimeGreen", 0.30)
            cylinder(h = FLAG_GAP,
                     d1 = FLAG_AP + 2*FLAG_GAP*tan(HALF_ANGLE),
                     d2 = FLAG_AP, center=true);
}

module assembly() {
    neighbour_patch();
    // aperture centred over the CENTRE cell corner (worst-case straddle)
    translate([BODY/2, BODY/2, 0]) {
        reader_head();
        down_state_cone();
    }
    // DND-114: the common-height flag target read at its own fixed standoff.
    common_height_flag();
    translate([0, 0, 0]) flag_reader_head();
}

assembly();

// ---- self-checks (echoed, captured by the render tool) ---------------------
echo(str("PITCH=", PITCH, " BODY=", BODY, " OWNED_LANE=", OWNED_LANE));
echo(str("WORK_GAP=", WORK_GAP, " APERTURE=", APERTURE, " HALF_ANGLE=", HALF_ANGLE));
echo(str("SPOT_UP_diameter=", SPOT_UP));
echo(str("SPOT_DOWN_diameter=", SPOT_DOWN, " = ", SPOT_DOWN/PITCH, " pitches"));
echo(str("CORNER_HYP=", CORNER_HYP, " CORNER_REACH_corrected=", CORNER_REACH));
echo(str("NEIGHBOUR_NEAR_EDGE=", NEIGHBOUR_NEAR_EDGE, " SPOT_CONTAMINATES=", SPOT_CONTAMINATES));
echo(str("spot fits top face at centre: ", (SPOT_UP/2) <= BODY/2));
echo(str("down-state single-cell read resolvable: ", SPOT_DOWN <= BODY));
echo(str("gap for centre fit: ", (BODY - APERTURE)/(2*tan(HALF_ANGLE))));

// ---- DND-114 common-height target read self-checks -------------------------
FLAG_X       = BODY/2 + 0.45/2 + 0.20;     // HINGE_X, frame-fixed lane
FLAG_T       = 0.44;                       // flag width in X
FLAG_W       = 1.60;                       // flag width in Y
FLAG_H       = 0.80;
FLAG_Z_TOP   = TRAVEL + 3.0;               // fixed target top face z
FLAG_GAP     = 1.0;                        // fixed reader-to-flag standoff
FLAG_AP      = 0.60;                       // dedicated small flag-read aperture
FLAG_SPOT_X  = FLAG_AP + 2*FLAG_GAP*tan(HALF_ANGLE);  // spot width in X
FLAG_SPOT_Y  = FLAG_SPOT_X;                // same formula, Y is open
X_CLEAR_NB   = PITCH - BODY/2 - FLAG_X;    // to the neighbour body
FLAG_SPOT_CLEARS_NB = (FLAG_SPOT_X/2) <= X_CLEAR_NB;
FLAG_SPOT_FITS_Y    = FLAG_SPOT_X <= FLAG_W;
echo(str("FLAG_X=", FLAG_X, " Z_FLAG_TOP=", FLAG_Z_TOP,
         " (frame-fixed; DeltaZ=0 for both states)"));
echo(str("FLAG_GAP=", FLAG_GAP, " FLAG_AP=", FLAG_AP,
         " FLAG_SPOT_X=", FLAG_SPOT_X, " X_CLEAR_NB=", X_CLEAR_NB));
echo(str("flag spot clears neighbour body: ", FLAG_SPOT_CLEARS_NB));
echo(str("flag spot fits flag Y width: ", FLAG_SPOT_FITS_Y));
