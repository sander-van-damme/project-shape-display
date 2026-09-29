// DND-76 — P4 single-actuator banked reset bar.
//
// EVIDENCE CLASS: CAD geometry. NOT a print, NOT a measurement ([DND-27]).
//
// The reset bar rides on the underside of the COMMON platen (an existing moving
// part). A Z-offset engagement dog contacts only the currently-indexed bank's
// four comb tails at the down limit; a printed one-way pawl clutch on each comb
// free-wheels on the up-stroke so the reset cannot corrupt the just-written
// mask. NO extra motor and NO bought clutch are added.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

BANKS = 8;
ROWS_PER_BANK = 10;
PITCH = 5.08;
RESET_BAR_T = 2.0;                 // printed reset bar thickness (Z)
RESET_ENGAGE = 1.20;               // engagement depth into a comb tail
CLUTCH_T = 0.90;                   // one-way pawl clutch leaf: 2 lines
CLUTCH_W = 0.70;
CLUTCH_L = 4.0;
BANK_SPAN = ROWS_PER_BANK * PITCH; // 50.8 mm depth per bank

module reset_bar() {
    // A single bar across the field (drawn as a 5-bank segment for the bed).
    color([0.8, 0.5, 0.2])
        cube([5 * BANK_SPAN, RESET_BAR_T, 8.0], center = true);
}

module engagement_dog() {
    // One Z-offset dog: engages the indexed bank's comb tails only.
    color([0.9, 0.2, 0.2])
        translate([0, 0, -RESET_BAR_T / 2 - RESET_ENGAGE / 2])
            cube([10.0, RESET_ENGAGE, RESET_ENGAGE], center = true);
}

module one_way_clutch() {
    // A printed pawl leaf that blocks on the down-stroke, free-wheels on up.
    color([0.2, 0.8, 0.4])
        cube([CLUTCH_T, CLUTCH_W, CLUTCH_L]);
}

reset_bar();
translate([0, 0, -RESET_BAR_T]) engagement_dog();
translate([BANK_SPAN / 2, 0, RESET_BAR_T])
    one_way_clutch();
