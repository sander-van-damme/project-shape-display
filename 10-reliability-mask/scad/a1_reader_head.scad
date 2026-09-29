// DND-111 — A1 reader-head optical geometry at the 5.08 mm pitch (real OpenSCAD)
//
// Bounds the SINGLE-CELL READ RESOLUTION question from CAD + geometry:
// can one wrong cell among 6,400 be distinguished from its neighbours?
//
// The reader head sits above the column tops at a working gap g. A single
// interrogation aperture of diameter d emits at half-angle theta. The
// returned spot must land ENTIRELY on the target column top face so a
// neighbour's light does not contaminate the reading. This file renders the
// worst case: the aperture centred on a CELL CORNER (max straddle), so the
// spot's reach past the top face into the 0.74 mm owned lane is visible.
//
// EVIDENCE CLASS: CAD geometry only. No print, no measurement (DND-27).
//
// Geometry taken from the placed cell CAD (a1_binary_latch_cell.scad):
//   PITCH = 5.08, BODY (column top face) = 3.60, lane = 0.74 each side.

PITCH      = 5.08;
BODY       = 3.60;         // column top face (square)
TRAVEL     = 40.0;         // column top at full up = 40 mm
OWNED_LANE = PITCH/2 - BODY/2;   // 0.74 mm

WORK_GAP   = 2.0;          // reader-to-column-top working gap (assumption-class)
APERTURE   = 2.0;          // single-cell interrogation aperture (assumption-class)
HALF_ANGLE = 15.0;         // emission half-angle (deg)
$fn = 48;

// Spot diameter where the center ray meets the target plane:
//   spot = aperture + 2 * gap * tan(half_angle)
function spot_d(gap, d, ha) = d + 2*gap*tan(ha);
SPOT = spot_d(WORK_GAP, APERTURE, HALF_ANGLE);

// Worst-case aperture position: at a cell corner -> spot reaches sqrt(2) times
// further diagonally. Required: the diagonal reach must stay on the top face.
CORNER_REACH = SPOT/2 * sqrt(2);

module column_up() {
    // a raised column: top face at z = TRAVEL
    color("SteelBlue")
        translate([0, 0, TRAVEL/2 - 20])
            cube([BODY, BODY, TRAVEL], center=true);
}

module column_down() {
    // a retracted column: top face near the base (z = 0)
    color("DimGray")
        translate([0, 0, -10 - 20])
            cube([BODY, BODY, TRAVEL], center=true);
}

module reader_head() {
    // the reader head body (orange) with the interrogation aperture (yellow)
    translate([0, 0, TRAVEL + WORK_GAP + 6])
        color("Orange") cube([APERTURE + 4, APERTURE + 4, 12], center=true);
    // the cone from the aperture to the target top face
    translate([0, 0, TRAVEL + WORK_GAP/2])
        color("Gold", 0.35)
            cylinder(h = WORK_GAP, d1 = SPOT, d2 = APERTURE, center=true);
}

module neighbour_patch() {
    // a 3x3 patch with the CENTRE cell DOWN (the wrong cell) and neighbours UP,
    // to show that a single-cell read only sees the centre column's top face.
    for (i = [-1, 0, 1])
        for (j = [-1, 0, 1]) {
            x = i*PITCH; y = j*PITCH;
            if (i == 0 && j == 0) translate([x, y, 0]) column_down();
            else translate([x, y, 0]) column_up();
        }
}

module assembly() {
    neighbour_patch();
    // aperture centred over the CENTRE cell corner (worst-case straddle)
    translate([BODY/2, BODY/2, 0]) reader_head();
}

assembly();

// ---- self-checks (echoed, captured by the render tool) ---------------------
echo(str("PITCH=", PITCH, " BODY=", BODY, " OWNED_LANE=", OWNED_LANE));
echo(str("WORK_GAP=", WORK_GAP, " APERTURE=", APERTURE, " HALF_ANGLE=", HALF_ANGLE));
echo(str("SPOT_diameter=", SPOT));
echo(str("CORNER_REACH=", CORNER_REACH, " vs BODY/2=", BODY/2));
echo(str("spot fits top face at centre: ", (SPOT/2) <= BODY/2));
echo(str("spot fits top face at corner: ", CORNER_REACH <= BODY/2));
echo(str("gap for centre fit: ", (BODY - APERTURE)/(2*tan(HALF_ANGLE))));
