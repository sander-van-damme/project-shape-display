// DND-76 — S6-LC-with-primitives unit cell (P1 bistable latch + P3 pocket/guide).
//
// EVIDENCE CLASS: CAD geometry (this file + its real-OpenSCAD render). It is
// NOT a print and NOT a measurement ([DND-27]).
//
// Rendered by ../tools/render_primitives_cad.py with `-D part="<key>"`.
// Single-manifold parts ("column", "pawl", "latch") are mesh-gated; the
// "cell"/"strip" bodies are multi-solid VIEWING assemblies and are excluded
// from the watertight gate (they overlap by design).
//
// The feature-vs-process checks for this cell live in `../primitives.py`
// (bistable_snap / lane_budget / pocket_throat / guide_budget /
// pocket_load_path), asserted by `../primitives_checks.py`, against the
// published FDM limits in tools/fdm-limits/fdm_process_limits.py.
//
// Units: mm. Target process: Bambu X1C, PLA, 0.4 mm nozzle, 0.20 mm layers.

PITCH = 5.08;
COLUMN_BODY = 3.60;
LANE = PITCH - COLUMN_BODY;        // 1.48 mm
LEVELS = 5;
STEP = 10.0;
COLUMN_H = 44.0;

// P3: rack pocket + guide
POCKET_DEPTH = 1.20;
POCKET_WIDTH = 2.40;
POCKET_RELIEF_DEG = 30.0;
POCKET_FLOOR = 0.88;
V_GUIDE_RAIL_T = 0.88;

// P1/P3: pawl
PAWL_T = 0.80;
PAWL_TOE = 0.60;
PAWL_LEN = 5.00;
PAWL_DEFLECT = 0.35;

// P1: bistable over-centre link
LATCH_T = 0.90;
LATCH_W = 0.70;
LATCH_L = 5.00;
LATCH_OVER_CENTRE = 0.40;

module column_body() {
    difference() {
        cube([COLUMN_BODY, COLUMN_BODY, COLUMN_H], center = true);
        for (lvl = [0 : LEVELS - 1]) rack_pocket_cut(lvl);
    }
}

module rack_pocket_cut(level) {
    z = -22.0 + level * STEP;
    translate([COLUMN_BODY / 2, 0, z])
        rotate([0, 90, 0])
            cylinder(h = POCKET_DEPTH + 0.01, d = POCKET_WIDTH, $fn = 32);
}

module v_guide_rails() {
    for (s = [1, -1])
        translate([s * (COLUMN_BODY + LANE - V_GUIDE_RAIL_T) / 2, 0, 20.0])
            cube([V_GUIDE_RAIL_T, COLUMN_BODY, 6.0], center = true);
}

module pawl() {
    // Z cantilever in the lane, toe toward the column.
    translate([(COLUMN_BODY + PAWL_T) / 2, 0, -18.0])
        cube([PAWL_T, PAWL_TOE, PAWL_LEN], center = true);
}

module latch() {
    // Over-centre link above the pawl in Z, same lane.
    translate([(COLUMN_BODY + LATCH_T) / 2, 0, 12.0])
        cube([LATCH_T, LATCH_W, LATCH_L], center = true);
}

module cell() {
    column_body();
    v_guide_rails();
    pawl();
    latch();
}

module strip() {
    for (i = [0 : 2]) translate([i * PITCH, 0, 0]) cell();
}

part = "column";
if (part == "column") column_body();
else if (part == "pawl") pawl();
else if (part == "latch") latch();
else if (part == "cell") cell();
else if (part == "strip") strip();
else echo("unknown part");
