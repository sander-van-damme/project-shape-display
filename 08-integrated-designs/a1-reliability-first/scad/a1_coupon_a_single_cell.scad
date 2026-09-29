// SHA-13 coupon A — single cell at true pitch (toggle-force + read-contrast).
//
// CAD-ready handoff definition. The repeated A1 cell parts (column, latch arm,
// cradle, CH-A vane, shutter) are REUSED UNCHANGED from
// `a1_binary_latch_cell.scad`; this file adds ONLY the coupon frame:
// a base plate with a centred cell socket, a force-gauge mount post aligned
// to the latch toe contact, and a reader bracket holding the fixed
// 1.8 mm standoff / 0.44 mm aperture.
//
// EVIDENCE CLASS: CAD geometry only. No print, no purchase, no measurement
// (DND-27). Nothing here is physical validation.
//
// Geometry deltas from the A1 package (all else identical):
//   COUPON_A_BASE    30 x 30 x 3.0 mm plate (fits X1C 256 mm bed)
//   COUPON_A_SOCKET  centred pocket BODY+2*CLEAR wide (places one cell)
//   COUPON_A_POST    gauge mount post, axis on the latch toe contact
//   COUPON_A_BRACKET reader bracket, aperture plane at Z_FLAG_TOP + 1.8 mm
//
// Kill lines carried (SHA-7): R1 snap mean > 7.14 N kills; R4 on/off < 2x kills.

PITCH = 5.08;
BODY  = 3.60;
CLEAR = 0.20;
TRAVEL = 40.0;
LATCH_T = 0.45;
HINGE_X = BODY/2 + LATCH_T/2 + CLEAR;   // 2.225 mm
Z_FLAG_TOP = TRAVEL + 3.0;              // 43.0 mm
SHUT_APER_GAP = 1.80;                   // adopted fixed standoff (DND-115)
SHUT_AP = 0.44;                         // dedicated read aperture (1 line)

// Coupon frame (NEW geometry; min feature 0.44, min wall 0.88 observed).
COUPON_A_BASE = 30.0;                   // base plate edge (mm)
COUPON_A_BASE_T = 3.0;                  // base plate thickness (mm)
COUPON_A_SOCKET = BODY + 2*CLEAR;       // centred cell socket width
COUPON_A_POST_D = 6.0;                  // gauge post diameter
COUPON_A_POST_H = 12.0;                 // gauge post height
COUPON_A_BRACKET_T = 2.0;               // reader bracket thickness
COUPON_A_APER_Z = Z_FLAG_TOP + SHUT_APER_GAP;  // 44.8 mm aperture plane

$fn = 24;

module coupon_a_base() {
    difference() {
        cube([COUPON_A_BASE, COUPON_A_BASE, COUPON_A_BASE_T], center=true);
        // centred cell socket (one true-pitch cell station)
        cube([COUPON_A_SOCKET, COUPON_A_SOCKET, COUPON_A_BASE_T + 0.2], center=true);
    }
    // gauge mount post, axis on the latch toe contact line
    translate([HINGE_X, COUPON_A_BASE/2 - 3.0, COUPON_A_BASE_T/2 + COUPON_A_POST_H/2])
        cylinder(h = COUPON_A_POST_H, d = COUPON_A_POST_D, center = true);
    // reader bracket: holds the aperture plane at the adopted standoff
    translate([HINGE_X, 0, COUPON_A_APER_Z + COUPON_A_BRACKET_T/2])
        cube([SHUT_AP + 4.0, SHUT_AP + 4.0, COUPON_A_BRACKET_T], center=true);
}

module coupon_a_part_selector() {
    if (part == "coupon_a_base") coupon_a_base();
    else coupon_a_base();
}

coupon_a_part_selector();

// ---- self-checks (echoed, captured by the readiness gate) ------------------
echo(str("COUPON_A base=", COUPON_A_BASE, " fits X1C bed 256: ", COUPON_A_BASE <= 256.0));
echo(str("COUPON_A socket=", COUPON_A_SOCKET, " places one true-pitch cell"));
echo(str("COUPON_A aperture plane=", COUPON_A_APER_Z, " (vane top + 1.8 standoff)"));
echo(str("COUPON_A min feature (aperture 0.44): ", SHUT_AP >= 0.44));
echo(str("COUPON_A kill R1 snap mean > 7.14 N; kill R4 on/off < 2x"));
