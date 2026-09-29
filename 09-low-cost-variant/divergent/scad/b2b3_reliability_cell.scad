// DND-107 InventorBeta -- reliability-first machine cell CAD evidence.
//
// Witnesses the two printed features that decide whether B2 (pressure blanket +
// mechanical hold) and B3 (rotary drum mask) pass the DND-103 reliability gate:
//
//   B2: the per-cell 2-state TOGGLE (living hinge + hard-stop lug). The hinge
//       thickness must be a robust 2-line feature (>= 0.88 mm), and the lug must
//       seat on a HARD STOP, not on a friction face.
//   B3: the per-column one-way PAWL in the 5-pocket rack (unchanged from the
//       promoted register) and the DRUM-TRACK follower finger that reads the
//       row track. B3 deletes the per-cell keeper, so the smallest repeated
//       feature is the pawl leaf and the follower finger.
//
// This is a pitch-budget + feature-size witness at the true 5.08 mm pitch.
// EVIDENCE CLASS: CAD (this file, read analytically). Not a print, not a
// measurement. Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle.

PITCH = 5.08;

// B2 toggle
TOGGLE_T = 0.90;        // living-hinge thickness: 2 lines (DND-103 robust)
TOGGLE_W = 4.00;        // hinge width (well above the pitch, into the row)
TOGGLE_L = 6.00;        // hinge length
TOGGLE_LUG = 1.20;      // hard-stop lug engagement depth (generous, positive)
TOGGLE_SHOULDER = 0.90; // printed hard-stop shoulder thickness
COLUMN_BODY = 4.72;     // square column, owned lane = (PITCH-BODY)/2 = 0.18

// B3 pawl + drum follower
PAWL_T = 0.90;          // pawl leaf thickness (2 lines)
PAWL_W = 0.70;          // pawl width in the row direction
GATE_BAR_T = 1.20;      // drum follower finger (generous, 2+ lines)
POCKET_DEPTH = 1.00;    // rack pocket depth
WALL = 0.90;            // printed frame wall

// drum track bit as printed on the drum surface
TRACK_RIDGE_T = 1.20;   // printed ridge width (generous)
DRUM_D = 40.0;          // sourced/printed drum diameter allowance

MIN_FDM_WALL = 0.44;    // 1 extrusion line @ 0.4 mm nozzle
