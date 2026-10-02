// design calculation coupon C — gantry registration over 406 mm (thermal/belt drift).
//
// CAD-ready handoff definition. The reader/writer head aperture geometry is
// REUSED UNCHANGED from `a1_reader_head.scad` (0.44 mm aperture, 1.8 mm
// standoff); this file adds ONLY the coupon reference hardware: a spliced
// 406.4 mm reference rail (two 210 mm segments + splice plate, each fitting
// the X1C 256 mm bed), 9 measurement stations (every 10 cells = 50.8 mm),
// and a head-carriage mock carrying the aperture bar.
//
// EVIDENCE CLASS: CAD geometry only. No print, no purchase, no measurement
// (design calculation). Nothing here is physical validation.
//
// Geometry deltas from the A1 package (all else identical):
//   COUPON_C_SPAN = 406.4 mm (80 x 5.08); two COUPON_C_SEG = 210 mm segments
//   COUPON_C_STATIONS = 9 (stations 0..8, every 50.8 mm)
//   COUPON_C_SPLICE 40 x 20 x 3.0 mm splice plate with M3 holes
//
// Measured against half-pitch: absolute drift < 2.54 mm (kill line);
// secondary read concern: repeatability within +/-0.264 mm.

PITCH = 5.08;
COLS = 80;
SPAN = COLS * PITCH;                  // 406.4 mm full traverse

// Coupon reference hardware (NEW geometry; min wall 0.88 observed).
COUPON_C_SPAN = 406.4;                // full traverse (mm)
COUPON_C_SEG = 210.0;                 // per-segment length (fits 256 bed)
COUPON_C_SEGMENTS = 2;                // spliced rail segment count
COUPON_C_STATIONS = 9;                // stations every 10 cells (50.8 mm)
COUPON_C_STATION_STEP = 10 * PITCH;   // 50.8 mm
COUPON_C_SPLICE_L = 40.0;             // splice plate length
COUPON_C_SPLICE_W = 20.0;             // splice plate width
COUPON_C_SPLICE_T = 3.0;              // splice plate thickness
HALF_PITCH = PITCH / 2;               // 2.54 mm kill-line drift bound
REGISTRATION_SECONDARY = 0.264;       // +/-0.264 mm secondary read concern

$fn = 24;

module coupon_c_rail_segment() {
    // one 210 mm reference rail segment with station sockets every 50.8 mm
    difference() {
        cube([COUPON_C_SEG, 12.0, 3.0], center=true);
        for (s = [0 : 4])
            translate([-COUPON_C_SEG/2 + 10.0 + s * COUPON_C_STATION_STEP, 0, 0])
                cylinder(h = 3.2, d = 3.2, center = true);
    }
}

module coupon_c_splice() {
    // splice plate joining the two segments at mid-span
    difference() {
        cube([COUPON_C_SPLICE_L, COUPON_C_SPLICE_W, COUPON_C_SPLICE_T], center=true);
        for (dx = [-12.0, 12.0])
            translate([dx, 0, 0])
                cylinder(h = COUPON_C_SPLICE_T + 0.2, d = 3.2, center = true);
    }
}

module coupon_c_part_selector() {
    if (part == "coupon_c_rail") coupon_c_rail_segment();
    else if (part == "coupon_c_splice") coupon_c_splice();
    else coupon_c_rail_segment();
}

coupon_c_part_selector();

// ---- self-checks (echoed, captured by the readiness gate) ------------------
echo(str("COUPON_C span=", COUPON_C_SPAN, " (80 x 5.08); segments=", COUPON_C_SEGMENTS, " x ", COUPON_C_SEG));
echo(str("COUPON_C segment fits X1C bed 256: ", COUPON_C_SEG <= 256.0));
echo(str("COUPON_C stations=", COUPON_C_STATIONS, " every ", COUPON_C_STATION_STEP, " mm"));
echo(str("COUPON_C kill drift >= half-pitch ", HALF_PITCH, "; secondary repeatability +/-", REGISTRATION_SECONDARY));
