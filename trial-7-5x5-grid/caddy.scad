/*
 * Shape display — trial 7: under-display CADDY (per-row pusher bank)
 * For Sander Van Damme's "3D grid map" project.
 *
 * Architecture chosen for trial 7:
 *   - one bank of flexible push-rods (1.75-3 mm filament) acts on a whole ROW at
 *     once; the caddy steps in Y through the rows.
 *   - each rod is STORED HORIZONTAL in the low caddy and FED VERTICAL up a guide
 *     tube, through the floor-plate hole, into the pin's bottom dimple. Because
 *     the pin's own detent holds every click, the feeder only nudges the rod a
 *     bit at a time ("pump") and the rod follows the pin up - so the caddy body
 *     stays low (no 30 mm rigid stroke living under the plate).
 *   - the 5 feed servos are far too fat for the 8.5 mm pitch, so they stand in
 *     2 ranks (front/back), each only 12.6 mm wide so alternate columns clear;
 *     the tubes fan in Y from the ranks to the row centre line.
 *   - a release finger on a micro-servo nudges the parked row's release dowel
 *     ~1 mm to disengage the spring lock from below.
 *
 * This is the first printable iteration of the caddy: chassis, tube block,
 * servo layout, rod routing and release finger are real; the feeder internals
 * (hobbed wheel + sprung idler) are schematic and expect physical tuning.
 *
 * Pick the view with the `show` variable (or -D 'show="..."'). grid.scad is
 * pulled in as a library, so its own render is skipped automatically.
 */

LIBRARY_MODE = true;    // pull in grid.scad as a library (skip its own render)
include <grid.scad>

show    = "assembly";   // [assembly, section, exploded, caddy, tube_block, feeder, feeder_print, release, base, base_print]
at_row  = 2;            // which row the caddy is parked under (0..n_rows-1)
ghost   = true;         // show the display stack (ghosted) in the assembly view
explode = 0;            // drop the caddy this far below the display (exploded view)

/* =====================  caddy parameters (mm)  ===================== */

flex_d     = 2.5;       // flexible push-rod (filament) diameter
tube_od    = flex_d + 2.6;
tube_id    = flex_d + 0.6;

tube_top_z = -1;        // rod exits the rigid guide just below the floor
wheel_z    = -9;        // feeder drive height (rod leaves the feeder here)
servo_top  = -7;        // top face of the standing feed servos
rank_dy    = 13;        // front/back rank offset from the row centre line

// SG90 / FS90R class micro-servo (standing: W along X, L along Y, H along Z)
servo_w = 12.6; servo_l = 23.0; servo_h = 22.5;
tab_l   = 32.0; tab_t = 2.5; tab_z = 15.8;

servo_bot = servo_top - servo_h;        // -29.5
base_t    = 3;
base_z    = servo_bot - 0.5 - base_t;   // base underside
rail_d    = 5;
rail_x    = [-12, (n_cols - 1)*pitch + 12];

cy = at_row * pitch;    // parked-row centre line (y)
$fn = $preview ? 28 : 48;

/* even columns -> front rank (-y), odd columns -> back rank (+y) */
function rank_y(i) = cy + (i % 2 == 0 ? -rank_dy : rank_dy);

/* =====================  generic bits  ===================== */

// standing SG90: origin at centre of the bottom face
module servo() {
    color("#34435c") translate([-servo_w/2, -servo_l/2, 0])
        cube([servo_w, servo_l, servo_h]);
    color("#34435c") translate([-servo_w/2, -tab_l/2, tab_z])
        cube([servo_w, tab_l, tab_t]);
    color("#e8e8e8") translate([0, servo_l/2 - 5.9, servo_h]) cylinder(d = 5, h = 3.2);
}

// hobbed drive wheel, axis along Y (feeds filament vertically)
module hob_wheel() {
    color("#9a9a9a") rotate([90, 0, 0]) difference() {
        cylinder(d = 9, h = 5, center = true);
        rotate_extrude() translate([4.7, 0]) circle(d = flex_d + 0.4);
    }
}

/* =====================  tube block  ===================== */
// rigid guide tubes: angle from each feeder rank up to the row centre line
module tube_block() {
    difference() {
        union() {
            for (i = [0 : n_cols - 1]) hull() {
                translate([i*pitch, rank_y(i), wheel_z]) sphere(d = tube_od);
                translate([i*pitch, cy,        tube_top_z]) sphere(d = tube_od);
            }
            // spine tying the tube tops together at the row line
            translate([-tube_od/2, cy - tube_od/2, tube_top_z - 4])
                cube([(n_cols - 1)*pitch + tube_od, tube_od, 4]);
        }
        for (i = [0 : n_cols - 1]) hull() {
            translate([i*pitch, rank_y(i), wheel_z - eps]) sphere(d = tube_id);
            translate([i*pitch, cy,        tube_top_z + eps]) sphere(d = tube_id);
        }
    }
}

/* =====================  feeder  ===================== */
// printable feeder block straddling the hobbed wheel, rod outlet up
module feeder_body() {
    color("#7c8794") difference() {
        translate([-7, -8, wheel_z - 6]) cube([14, 16, 12]);
        rotate([90, 0, 0]) cylinder(d = 10.6, h = 30, center = true);   // wheel pocket
        translate([0, 0, wheel_z - 6 - eps]) cylinder(d = tube_id, h = 14); // outlet up
    }
}

// feeder block + its (bought) wheel and standing servo, as a unit
module feeder_unit() {
    feeder_body();
    hob_wheel();
    translate([0, 0, servo_bot]) servo();
}

// place a feeder for column i at its rank position
module feeder_at(i) { translate([i*pitch, rank_y(i), 0]) feeder_unit(); }

/* =====================  release finger  ===================== */
// micro-servo at the west edge swings a finger that nudges the dowel east (~1 mm)
module release_finger(engaged = false) {
    // the finger, at the dowel hang height
    translate([dowel_x - 8, cy, -1.6])
        color("#cf5b2a") rotate([0, 0, engaged ? 2 : -14])
            translate([0, -1.5, -1.5]) cube([8.5, 3, 3]);
    // its micro-servo lying flat on the base, west of the grid
    translate([dowel_x - 20, cy, base_z + base_t]) rotate([0, 0, 90]) servo();
}

/* =====================  flexible push-rods  ===================== */
// column i rod: stored horizontal at the rank, fed up to the pin bottom
module flex_rod(i) {
    lvl   = lift_of(i, at_row);
    top_z = floor_t + tooth_pitch * lvl + 1.5;     // just into the pin dimple
    ry    = rank_y(i);
    color("#d8a64a") {
        // fed/vertical part: wheel -> row line -> up into the pin
        hull() { translate([i*pitch, ry, wheel_z]) sphere(d = flex_d);
                 translate([i*pitch, cy, tube_top_z]) sphere(d = flex_d); }
        translate([i*pitch, cy, tube_top_z]) cylinder(d = flex_d, h = top_z - tube_top_z);
        // stored/horizontal part: a curl lying flat in the caddy (low storage)
        dir = (i % 2 == 0) ? -1 : 1;
        translate([i*pitch, ry, wheel_z - 2]) rotate([dir*90, 0, 0])
            cylinder(d = flex_d, h = 14);
    }
}

/* =====================  base + Y rails  ===================== */
// printable base plate with the linear-bearing bushings
module caddy_base_print() {
    y0 = cy - rank_dy - servo_l + 2;
    y1 = cy + rank_dy + servo_l - 2;
    color("#6f7a86") difference() {
        union() {
            translate([rail_x[0] - 5, y0, base_z])
                cube([rail_x[1] - rail_x[0] + 10, y1 - y0, base_t]);
            for (rx = rail_x) translate([rx, y0 + 4, base_z + base_t])
                cube([8, y1 - y0 - 8, 7]);
        }
        for (rx = rail_x) translate([rx + 4, y0 - 1, base_z + base_t + 3.5])
            rotate([-90, 0, 0]) cylinder(d = rail_d + 0.6, h = y1 - y0 + 2);
    }
}

// the bought steel Y rods the caddy slides along
module caddy_rails() {
    for (rx = rail_x) color("#cfcfcf")
        translate([rx + 4, cy - 48, base_z + base_t + 3.5]) rotate([-90, 0, 0])
            cylinder(d = rail_d, h = 96);
}

module caddy_base() { caddy_base_print(); caddy_rails(); }

/* =====================  caddy + combined  ===================== */
module caddy(show_rods = true) {
    tube_block();
    for (i = [0 : n_cols - 1]) feeder_at(i);
    if (show_rods) for (i = [0 : n_cols - 1]) flex_rod(i);
    release_finger();
    caddy_base();
}

module combined(drop = 0) {
    if (ghost) %assembly();              // display: floor underside at z = 0
    translate([0, 0, -drop]) caddy(show_rods = drop == 0);  // caddy below z = 0
}

// cut a thin slab through the parked row to show rod-into-pin + release
module combined_section() {
    intersection() {
        union() { assembly(); caddy(); }
        translate([fx0 - 10, cy - 1.4, base_z - 6])
            cube([(fx1 - fx0) + 60, 2.8, 130]);
    }
}

/* =====================  render  ===================== */
if      (show == "tube_block")   tube_block();        // printable
else if (show == "feeder")       feeder_unit();        // block + servo + wheel
else if (show == "feeder_print") feeder_body();        // printable
else if (show == "base")         caddy_base();         // base + steel rails
else if (show == "base_print")   caddy_base_print();   // printable
else if (show == "release")      release_finger(engaged = true);
else if (show == "caddy")        caddy();
else if (show == "section")      combined_section();
else if (show == "exploded")     combined(drop = 26);
else                              combined();
