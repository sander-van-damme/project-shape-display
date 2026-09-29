// DND-60 S5-R COMPLETE PRINTABLE PART SET -- real OpenSCAD, one selector.
//
// Printable-part geometry for the promoted S5-R machine (shared-drive
// programmable rotary register, R=4). Every DISTINCT printed part is a module;
// `part=` selects which renders to STL. Constants come from
// `s5r_parts_common.scad` so the printable set cannot drift from the model.
//
// CAD EVIDENCE. Not a print, not a measurement ([DND-27]).
// Units: mm. Process: Bambu X1C, PLA, 0.4 nozzle, 0.20 layers.
// Parts longer than the 256 mm bed are split at the cartridge boundary.

include <s5r_parts_common.scad>

module inner_cell() {
    // one open cell tube (bore + pawl chamber +X + keeper chamber +Y) at origin
    translate([0, 0, -BAR_D - 1 - EPS])
        cylinder(r = ROTOR_RADIUS + 0.10, h = CELL_H + 2 * EPS);
    translate([PAWL_T / 2, -PITCH / 2 - EPS, -BAR_D - 1 - EPS])
        cube([PITCH / 2, PITCH + 2 * EPS, CELL_H + 2 * EPS]);
    translate([-PITCH / 2 - EPS, PAWL_W / 2, -BAR_D - 1 - EPS])
        cube([PITCH + 2 * EPS, PITCH / 2, CELL_H + 2 * EPS]);
}

// MODEL SIZE. A full 27x27 cartridge (729 cell bores) is ~30x over the
// reasonable CGAL render budget for one part. The cartridge geometry is a
// periodic cell array, so this module renders a REPRESENTATIVE_CART_BLOCK x
// REPRESENTATIVE_CART_BLOCK witness block: it exercises the real 5.08 mm pitch,
// the bore, both side chambers, the rack channel and the frame lip. The FULL
// 27x27 footprint, cell count and mass are computed analytically in
// tools/gen_manifests.py and stated on the manifest; the uniform-pitch argument
// (identical to s5r_bank.scad's reduced-model note) carries the witness to the
// full part. The STL is a CAD witness of the cell, not a print file.
REPRESENTATIVE_CART_BLOCK = 8;   // 8x8 = 64 cells

module cell_cartridge(cols = REPRESENTATIVE_CART_BLOCK,
                      rows = REPRESENTATIVE_CART_BLOCK) {
    w = cols * PITCH;
    d = rows * PITCH;
    h = CELL_H;
    difference() {
        translate([-w / 2, -d / 2, -BAR_D - 1]) cube([w, d, h + BAR_D + 1]);
        for (cx = [0 : cols - 1])
            for (cy = [0 : rows - 1])
                translate([(cx - (cols - 1) / 2) * PITCH,
                           (cy - (rows - 1) / 2) * PITCH, 0])
                    inner_cell();
        // rack channel under each row (rod + rack strip pass through)
        for (cy = [0 : rows - 1])
            translate([-w / 2 - EPS,
                       (cy - (rows - 1) / 2) * PITCH - RACK_STRIP_W / 2,
                       -BAR_D - 1])
                cube([w + 2 * EPS, RACK_STRIP_W, BAR_D + EPS]);
    }
    // module frame lip on two edges (bolt-to-neighbour datum)
    translate([-w / 2, d / 2 - FRAME_RAIL, 0]) cube([w, FRAME_RAIL, FRAME_RAIL_H]);
    translate([w / 2 - FRAME_RAIL, -d / 2, 0]) cube([FRAME_RAIL, d, FRAME_RAIL_H]);
}

module rotor() {
    cylinder(r = ROTOR_RADIUS, h = 2.0);
    translate([0, 0, 2.0]) cylinder(r = ROTOR_CORE_RADIUS, h = CELL_H - 2.0);
}

module drive_pawl() {
    translate([-PAWL_T / 2, -PAWL_W / 2, 0]) cube([PAWL_T, PAWL_W, PAWL_LEN]);
    translate([-PAWL_T / 2 - 0.25, -PAWL_W / 2 - 0.25, PAWL_LEN])
        cube([PAWL_T + 0.5, PAWL_W + 0.5, 1.60]);
}

module keeper() {
    union() {
        cube([KEEPER_T, KEEPER_T, KEEPER_LEN]);
        // hard printed shoulder: rooted at the leaf base, projecting -Y and -Z
        // (overlaps the leaf so the union is a single closed solid)
        translate([0, -KEEPER_SHOULDER_X, 0])
            cube([KEEPER_T, KEEPER_SHOULDER_X + EPS, KEEPER_LEN]);
        for (k = [0 : LEVELS - 1])
            translate([KEEPER_T - EPS, 0, k * KEEPER_GATE_STEP])
                cube([0.20 + EPS, KEEPER_T, 0.15]);
    }
}

module detent_leaf() {
    union() {
        cube([WALL, 0.70, 6.00]);
        // scallop nose, embedded into the front face so the union is closed
        translate([WALL / 2, 0.70 / 2, 0.80]) rotate([0, 90, 0])
            cylinder(r = 0.40, h = WALL, center = true);
    }
}

module rack_strip(len = CARTRIDGE_COLS * PITCH) {
    cube([len, RACK_STRIP_W, 2.0]);
    for (t = [0 : floor(len / RACK_TOOTH_PITCH) - 1])
        translate([t * RACK_TOOTH_PITCH, 0, 2.0])
            cube([RACK_TOOTH_HEIGHT, RACK_STRIP_W, RACK_TOOTH_HEIGHT]);
    for (e = [0, len - 3.0])
        translate([e, 0, -BAR_D / 2])
            difference() {
                cube([3.0, RACK_STRIP_W, BAR_D / 2 + 2.0]);
                translate([-EPS, RACK_STRIP_W / 2, 0]) rotate([0, 90, 0])
                    cylinder(r = BAR_D / 2 + 0.2, h = 3.0 + 2 * EPS);
            }
}

module bank_drive_housing(l = 60.0, w = 40.0, h = 30.0) {
    difference() {
        cube([l, w, h]);
        for (s = [-1, 1])
            translate([l / 2 + s * 18, w / 2, 0]) cylinder(r = 11.0, h = h + 2 * EPS);
        translate([-EPS, w / 2, h / 2]) rotate([0, 90, 0])
            cylinder(r = BAR_D / 2 + 0.25, h = l + 2 * EPS);
        translate([l / 2, w / 2, h / 2]) rotate([0, 90, 0])
            cylinder(r = BANK_MOTOR_PINION_R + 1.0, h = 12.0, center = true);
    }
}

module reset_comber() {
    translate([0, -COMBER_BODY_W / 2, -COMBER_BODY_H / 2])
        cube([COMBER_BODY_L, COMBER_BODY_W, COMBER_BODY_H]);
    for (r = [0 : BANK_ROWS - 2])
        translate([COMBER_BODY_L / 2 - COMBER_TINE_T / 2,
                   r * ROW_PITCH + ROW_PITCH / 2 - 0.30, -COMBER_TINE_L / 2])
            cube([COMBER_TINE_T, 0.60, COMBER_TINE_L]);
}

module writer_carriage() {
    difference() {
        translate([-CARRIAGE_X / 2, -CARRIAGE_Y / 2, 0])
            cube([CARRIAGE_X, CARRIAGE_Y, CARRIAGE_Z]);
        for (sx = [0 : 7])
            for (sy = [0 : 4])
                translate([-CARRIAGE_X / 2 + 4.0 + sx * 4.5,
                           -CARRIAGE_Y / 2 + 3.0 + sy * 4.5, -EPS])
                    cylinder(r = 2.2, h = CARRIAGE_Z + 2 * EPS);
    }
    for (sx = [0 : 7])
        translate([-CARRIAGE_X / 2 + 4.0 + sx * 4.5 - 1.0,
                   -CARRIAGE_Y / 2 + 3.0, -CARRIAGE_NOSE_L])
            cube([2.0, 4 * 4.5 + 4.0, CARRIAGE_NOSE_L]);
}

module platen_module(cols = CARTRIDGE_COLS, rows = CARTRIDGE_ROWS) {
    w = cols * PITCH;
    d = rows * ROW_PITCH;
    difference() {
        translate([-w / 2, -d / 2, 0]) cube([w, d, PLATEN_T]);
        for (sx = [-1, 1], sy = [-1, 1])
            translate([sx * (w / 2 - 8), sy * (d / 2 - 8), -EPS])
                cylinder(r = LIFT_SCREW_R + 0.2, h = PLATEN_T + 2 * EPS);
    }
    for (i = [-2 : 2])
        translate([i * (w / 5), -d / 2, PLATEN_T]) cube([PLATEN_RIB, d, 3.0]);
}

module lift_frame_rail(len = CARTRIDGE_W + FRAME_RAIL) {
    difference() {
        cube([len, FRAME_RAIL, FRAME_RAIL_H + 6.0]);
        for (i = [0 : floor(len / 20.0) - 1])
            translate([6.0 + i * 20.0, -EPS, 3.0])
                cube([10.0, FRAME_RAIL + 2 * EPS, FRAME_RAIL_H]);
    }
}

module guide_bracket() {
    difference() {
        cube([BRACKET_W, BRACKET_T, BRACKET_H]);
        translate([BRACKET_W / 2, -EPS, 6.0]) rotate([-90, 0, 0])
            cylinder(r = GUIDE_ROD_R + 0.2, h = BRACKET_T + 2 * EPS);
        translate([BRACKET_W / 2, -EPS, BRACKET_H - 6.0]) rotate([-90, 0, 0])
            cylinder(r = LIFT_SCREW_R + 0.2, h = BRACKET_T + 2 * EPS);
        for (sx = [-1, 1])
            translate([BRACKET_W / 2 + sx * 5.5, -EPS, BRACKET_H / 2])
                rotate([-90, 0, 0]) cylinder(r = 1.7, h = BRACKET_T + 2 * EPS);
    }
}

module solenoid_mount() {
    difference() {
        cube([CARRIAGE_X - 2 * CARRIAGE_WALL, 6.0, 4.0]);
        for (sx = [0 : 7])
            translate([CARRIAGE_WALL + sx * 4.5, -EPS, -EPS])
                cylinder(r = 2.3, h = 4.0 + 2 * EPS);
    }
}

module comber_cam() {
    difference() {
        cylinder(r = 8.0, h = 4.0);
        translate([0, 0, -EPS]) cylinder(r = 2.2, h = 4.0 + 2 * EPS);
        translate([-9, -1.2, -EPS]) cube([18.0, 2.4, 4.0 + 2 * EPS]);
    }
}

part = "cell_cartridge";

if (part == "cell_cartridge")           cell_cartridge();
else if (part == "rotor")               rotor();
else if (part == "drive_pawl")          drive_pawl();
else if (part == "keeper")              keeper();
else if (part == "detent_leaf")         detent_leaf();
else if (part == "rack_strip")          rack_strip();
else if (part == "bank_drive_housing")  bank_drive_housing();
else if (part == "reset_comber")        reset_comber();
else if (part == "writer_carriage")     writer_carriage();
else if (part == "platen_module")       platen_module();
else if (part == "lift_frame_rail")     lift_frame_rail();
else if (part == "guide_bracket")       guide_bracket();
else if (part == "solenoid_mount")      solenoid_mount();
else if (part == "comber_cam")          comber_cam();
