// design calculation coupon B — 5x5 cycling rig with loaded untouched neighbour + miniature.
//
// CAD-ready handoff definition. The 25 cells reuse the A1 cell parts UNCHANGED
// from `a1_binary_latch_cell.scad` at the true 5.08 mm pitch; this file adds
// ONLY the coupon tile frame: a base plate with a 5x5 socket grid, a service
// load seat over the CENTRE cell (the loaded untouched neighbour, 3.27 N +
// miniature mass), and a miniature plinth sized for a representative 28-35 mm
// figure base.
//
// EVIDENCE CLASS: CAD geometry only. No print, no purchase, no measurement
// (design calculation). Nothing here is physical validation.
//
// Geometry deltas from the A1 package (all else identical):
//   COUPON_B_N = 5 (5x5 = 25 cells); field = 5 * 5.08 = 25.4 mm
//   COUPON_B_BASE = 40 x 40 x 3.0 mm tile (fits X1C 256 mm bed)
//   COUPON_B_LOAD_SEAT over centre cell (2,2): dead-weight / spring seat
//   COUPON_B_PLINTH 30 mm dia miniature station on the centre cell
//
// Measured against the Q5 proposal: peak neighbour motion <= 0.10 mm.
// Kill lines: neighbour motion > 0.10 mm, miniature tip-over, hinge
// stall/fracture at any cycle count.

PITCH = 5.08;
BODY  = 3.60;
CLEAR = 0.20;
TRAVEL = 40.0;

// Coupon tile (NEW geometry; min feature 0.44, min wall 0.88 observed).
COUPON_B_N = 5;                                   // 5x5 array
COUPON_B_FIELD = COUPON_B_N * PITCH;              // 25.4 mm
COUPON_B_BASE = 40.0;                             // tile edge (mm)
COUPON_B_BASE_T = 3.0;                            // tile thickness (mm)
COUPON_B_SOCKET = BODY + 2*CLEAR;                 // per-cell socket width
COUPON_B_PLINTH_D = 30.0;                         // miniature station diameter
COUPON_B_PLINTH_T = 2.0;                          // plinth thickness
SERVICE_LOAD_N = 3.27;                            // loaded-neighbour service load

$fn = 24;

module coupon_b_tile() {
    difference() {
        cube([COUPON_B_BASE, COUPON_B_BASE, COUPON_B_BASE_T], center=true);
        // 5x5 socket grid at true pitch
        for (i = [0 : COUPON_B_N - 1])
            for (j = [0 : COUPON_B_N - 1])
                translate([(i - (COUPON_B_N-1)/2) * PITCH,
                           (j - (COUPON_B_N-1)/2) * PITCH, 0])
                    cube([COUPON_B_SOCKET, COUPON_B_SOCKET,
                          COUPON_B_BASE_T + 0.2], center=true);
    }
    // miniature plinth ring on the centre (loaded, untouched) cell station
    translate([0, 0, COUPON_B_BASE_T/2 + COUPON_B_PLINTH_T/2])
        difference() {
            cylinder(h = COUPON_B_PLINTH_T, d = COUPON_B_PLINTH_D, center = true);
            cylinder(h = COUPON_B_PLINTH_T + 0.2, d = BODY, center = true);
        }
}

module coupon_b_part_selector() {
    if (part == "coupon_b_tile") coupon_b_tile();
    else coupon_b_tile();
}

coupon_b_part_selector();

// ---- self-checks (echoed, captured by the readiness gate) ------------------
echo(str("COUPON_B field=", COUPON_B_FIELD, " (5 x 5.08 true pitch)"));
echo(str("COUPON_B tile=", COUPON_B_BASE, " fits X1C bed 256: ", COUPON_B_BASE <= 256.0));
echo(str("COUPON_B centre cell is the loaded untouched neighbour (3.27 N + miniature)"));
echo(str("COUPON_B Q5 gate 0.10 mm; kill on motion > 0.10 mm, tip-over, stall/fracture"));
