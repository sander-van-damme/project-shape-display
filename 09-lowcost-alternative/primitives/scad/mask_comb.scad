// DND-76 — P2 mask medium: printed 4-plane louvre comb bar (one bar shown).
//
// EVIDENCE CLASS: CAD geometry. NOT a print, NOT a measurement ([DND-27]).
//
// One comb bar carries one unary threshold plane for one bank: an open slot
// over every ARMED cell and a 3-line land over every DISARMED cell. The bar is
// stroked in a 1.60 mm guide channel (bar 1.20 mm -> 0.40 mm free, 0.20 mm
// after worst-case tolerance). Four such bars form the stack, indexed by one
// camshaft per bank driven off the platen stroke.
//
// Rendered with `-D part="bar"` by ../tools/render_primitives_cad.py.
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

PITCH = 5.08;
N_COLS = 80;
LOUVRE_BAR_T = 1.20;               // 3 lines, load-bearing
LOUVRE_SLOT_WEB = 1.32;            // 3-line land between slots
LOUVRE_GUIDE_SLOT = 1.60;
BAR_H = 4.0;                       // Z height of the bar
SLOT_T = 0.80;                     // vertical slot height (Z)
SEG_CELLS = 16;                    // printable segment for the render

module comb_bar(armed_mask) {
    difference() {
        cube([LOUVRE_BAR_T, SEG_CELLS * PITCH, BAR_H], center = true);
        for (i = [0 : SEG_CELLS - 1]) {
            if (armed_mask[i] == 1) {
                translate([0, (i - (SEG_CELLS - 1) / 2) * PITCH, 0])
                    cube([LOUVRE_BAR_T + 2, LOUVRE_SLOT_WEB, SLOT_T], center = true);
            }
        }
    }
}

// Example pattern for viewing (arbitrary).
example = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1];

part = "bar";
if (part == "bar") comb_bar(example);
else echo("unknown part");
