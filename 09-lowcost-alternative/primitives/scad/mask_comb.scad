// DND-76 — P2 mask medium: printed 4-plane louvre comb bar (one bar shown).
//
// EVIDENCE CLASS: CAD geometry. NOT a print, NOT a measurement ([DND-27]).
//
// A single comb bar carries one unary threshold plane for one bank: an open
// slot over every ARMED cell and a 2-line land over every DISARMED cell. The
// bar is stroked in a 1.60 mm guide channel (bar 1.20 mm -> 0.40 mm free,
// 0.20 mm after worst-case tolerance). Four such bars form the stack; they are
// indexed by one camshaft per bank driven off the platen stroke.
//
// The bar is drawn with the ACTIVE slot pattern as a parameter (armed = true)
// so a reader can see the medium; a real map sets the pattern per bank.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

PITCH = 5.08;
N_COLS = 80;
LOUVRE_BAR_T = 1.20;               // 3 lines, load-bearing
LOUVRE_SLOT_WEB = 1.32;            // 3-line land between slots
LOUVRE_GUIDE_SLOT = 1.60;
BAR_LEN = N_COLS * PITCH;          // 406.4 mm (split into printable segments)
SLOT_T = 0.80;                     // vertical slot height (Z), through the bar

// For a printable, bed-fitting render show a 16-cell segment of the bar.
SEG_CELLS = 16;

module comb_bar_segment(armed_mask) {
    // armed_mask: a vector of 0/1, one per cell in the segment.
    w = LOUVRE_BAR_T;
    len = SEG_CELLS * PITCH;
    difference() {
        color([0.4, 0.4, 0.8])
            cube([w, len, 4.0], center = true);
        for (i = [0 : SEG_CELLS - 1]) {
            if (armed_mask[i] == 1) {
                // an open slot over an armed cell
                translate([0, (i - (SEG_CELLS - 1) / 2) * PITCH, 0])
                    cube([w + 2, LOUVRE_SLOT_WEB, SLOT_T], center = true);
            }
        }
    }
}

// Example pattern for viewing (arbitrary).
example = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1];
comb_bar_segment(example);
