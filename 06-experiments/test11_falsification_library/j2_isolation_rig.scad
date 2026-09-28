// J2 shared isolation-rig coupon geometry. Units: mm. OpenSCAD, no libraries.
//
// This file is a *fixture* for the J2 isolation protocol, not a display cell.
// It is deliberately architecture-agnostic: the tile holder accepts an
// interchangeable drive fixture with the same four M3 bolt pattern.
//
// Exported geometry is not a printer or material qualification. Print on the
// X1C/PLA process, inspect sliced walls, and record slicer settings per the
// project fabrication baseline in 02-design-criteria.
//
// PRINT BASELINE (Bambu X1C, PLA, 0.4 mm nozzle) -- proposed, not yet verified:
//   layer 0.20 mm; walls 3 perimeters; top/bottom 5 layers; 15% gyroid infill.
//   holder + miniature_tray + indicator_bracket: print as laid out below, no
//     supports (all overhangs <= 45 deg by construction).
//   base_rail: prints flat; 12 mm thick, split if the slicer bed allows.
//   Do NOT scale tile/cell_pitch_mm: the whole point is full-scale pitch.
//
// Print the parts on ONE plate with `part = "plate"`. Individual STL export:
//   openscad -o holder_10x10.stl -D tile=10 j2_isolation_rig.scad
//   openscad -o base_rail.stl     -D part=\"base_rail\" j2_isolation_rig.scad
//   openscad -o plate.stl         -D part=\"plate\" j2_isolation_rig.scad
//
// See `print_plan.md` for the bite-by-bite build/measurement plan and
// `isolation_rig_runner.py` for the pass/fail gate engine fed by the results.

// ------------------------- user parameters -----------------------------------
// tile cells per side: 5, 10 or 20 (the three protocol sweep points)
tile = 10;
// full-scale cell pitch. Do not scale this down.
cell_pitch_mm = 5.08;
// nominal seam between the two tile holders
seam_gap_mm = 0.40;
// holder border wall around the active cell field
border_mm = 6.0;
// holder base thickness
base_thickness_mm = 3.0;
// holder side wall height (keeps the tile registered; not a load surface)
wall_height_mm = 8.0;
// M3 clearance hole diameter and bolt pattern inset from each corner
m3_clearance_mm = 3.4;
bolt_inset_mm = 4.0;
// print clearance for self-tapping M3 into the rail (tap pilot)
m3_pilot_mm = 2.7;
// edge chamfer to fight first-layer elephant-foot (bowtie) at the seam face
chamfer_mm = 0.6;

part = "holder";        // holder | base_rail | indicator_bracket | miniature_tray | plate
$fn = 64;

active_mm = tile * cell_pitch_mm;
outer_mm = active_mm + 2 * border_mm;

// ------------------------- holders -------------------------------------------
module m3_holes() {
    for (dx = [bolt_inset_mm, outer_mm - bolt_inset_mm])
        for (dy = [bolt_inset_mm, outer_mm - bolt_inset_mm])
            translate([dx, dy, -1]) cylinder(d = m3_clearance_mm, h = base_thickness_mm + 2);
}

module holder() {
    // Outer registration frame with a recessed active field and M3 bolt pattern.
    difference() {
        cube([outer_mm, outer_mm, wall_height_mm]);
        // active field recess: square hole through, offset by border
        translate([border_mm, border_mm, base_thickness_mm])
            cube([active_mm, active_mm, wall_height_mm]);
        m3_holes();
    }
    // thin floor under the active field with the interchangeable-fixture socket
    // (a rectangular pocket, so each survivor's drive fixture drops in flush)
    difference() {
        translate([border_mm, border_mm, 0]) cube([active_mm, active_mm, base_thickness_mm]);
        translate([border_mm + 2, border_mm + 2, -1])
            cube([active_mm - 4, active_mm - 4, base_thickness_mm + 2]);
    }
}

// ------------------------- shared base rail ----------------------------------
rail_length_mm = 2 * outer_mm + seam_gap_mm + 20;
rail_width_mm = outer_mm + 8;
rail_thickness_mm = 12;

module base_rail() {
    difference() {
        cube([rail_length_mm, rail_width_mm, rail_thickness_mm]);
        // two sets of holder bolt slots, separated by seam_gap_mm
        for (i = [0:1]) {
            x0 = 10 + i * (outer_mm + seam_gap_mm);
            for (dx = [bolt_inset_mm, outer_mm - bolt_inset_mm])
                for (dy = [4 + bolt_inset_mm, 4 + outer_mm - bolt_inset_mm])
                    translate([x0 + dx, dy, -1]) cylinder(d = m3_clearance_mm, h = rail_thickness_mm + 2);
        }
    }
}

// ------------------------- dial indicator bracket ----------------------------
// Clamps a 0.01 mm dial indicator so its probe can sit on the neighbour tile.
bracket_stem_d_mm = 8.0;   // typical indicator stem
module indicator_bracket() {
    difference() {
        union() {
            cube([24, 24, 4]);
            translate([4, 4, 4]) cube([16, 16, 14]);
        }
        translate([12, 12, 8]) rotate([90, 0, 0])
            cylinder(d = bracket_stem_d_mm + 0.2, h = 20, center = true);
        translate([12, 12, -1]) cylinder(d = m3_clearance_mm, h = 6);
    }
}

// ------------------------- miniature tray ------------------------------------
// A shallow tray so a real miniature base can be centred on the neighbour tile
// and its movement/tipping scored against a fixed datum.
min_base_mm = 25.4;   // one battle-map square
module miniature_tray() {
    difference() {
        cube([min_base_mm + 4, min_base_mm + 4, 3]);
        translate([2, 2, 1]) cube([min_base_mm, min_base_mm, 3]);
    }
}

// ------------------------- print plate layout --------------------------------
// Lays the whole J2 set on one X1C bed (256 x 256) with 6 mm part gaps and no
// supports. Big tiles (20x20) exceed the bed in one piece: print those halves
// separately and bolt on the printed splice per the protocol.
module print_plate() {
    gap = 6.0;
    // two holders side by side (the pair under test)
    translate([0, 0, 0]) holder();
    translate([outer_mm + gap, 0, 0]) holder();
    // miniature trays below the holders
    translate([0, outer_mm + gap, 0]) miniature_tray();
    translate([min_base_mm + 4 + gap, outer_mm + gap, 0]) miniature_tray();
    // two indicator brackets
    translate([0, outer_mm + gap + min_base_mm + 4 + gap, 0])
        indicator_bracket();
    translate([24 + gap, outer_mm + gap + min_base_mm + 4 + gap, 0])
        indicator_bracket();
}

// ------------------------- dispatch ------------------------------------------
if (part == "holder") holder();
else if (part == "base_rail") base_rail();
else if (part == "indicator_bracket") indicator_bracket();
else if (part == "miniature_tray") miniature_tray();
else if (part == "plate") print_plate();
else holder();
