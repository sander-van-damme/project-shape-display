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
// Rendered with `-D part="<key>"` by ../tools/render_primitives_cad.py.
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

RESET_BAR_T = 2.0;                 // printed reset bar thickness (Z)
RESET_ENGAGE = 1.20;               // engagement dog depth
CLUTCH_T = 0.90;                   // one-way pawl clutch leaf: 2 lines
CLUTCH_W = 0.70;
CLUTCH_L = 4.0;
SEG_BANKS = 4;                     // drawn segment for the bed (203.2 mm)
BANK_SPAN = 10 * 5.08;             // 50.8 mm per bank

module reset_bar() {
    cube([SEG_BANKS * BANK_SPAN, RESET_BAR_T, 8.0], center = true);
}

module engagement_dog() {
    translate([0, 0, -RESET_BAR_T / 2 - RESET_ENGAGE / 2])
        cube([10.0, RESET_ENGAGE, RESET_ENGAGE], center = true);
}

module clutch() {
    // A printed pawl leaf: blocks on the down-stroke, free-wheels on the up.
    cube([CLUTCH_T, CLUTCH_W, CLUTCH_L]);
}

part = "bar";
if (part == "bar") reset_bar();
else if (part == "dog") engagement_dog();
else if (part == "clutch") clutch();
else echo("unknown part");
