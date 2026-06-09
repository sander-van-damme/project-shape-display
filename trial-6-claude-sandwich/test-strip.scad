/*
 * Shape display — trial 6: sliding release grid (1x5 test strip)
 * For Sander Van Damme's "3D grid map" project.
 *
 * Architecture (Sander's three-layer sandwich):
 *   1. floor plate      - down-stop for pins + rod access holes
 *   2. bottom guide grid - pins slide in square channels (+ pocket on top)
 *   3. release strip     - printed "wire comb": slides 1 mm to release all pins
 *   4. top cover grid    - protects the release strip, extra pin guidance
 *
 * Pins carry a RECESSED sawtooth rack inside a groove on one face.
 * Blade tongues on the release strip reach into the groove:
 *   - pin pushed up  -> ramps cam the whole strip sideways against the
 *                       return band, then it snaps back (click)
 *   - load pushed down -> flat tooth face presses on blade top: locked
 *   - strip pulled 1 mm -> blades clear all teeth, every pin drops
 *
 * Vanilla OpenSCAD, no libraries required. Tested with OpenSCAD 2021.01.
 *
 * Select the part to render/export below.
 */

part = "assembly"; // [assembly, assembly_released, pin, pins_print, grid_bottom, release_strip, grid_top, floor_plate, push_rod]

/* =====================  parameters (mm)  ===================== */

// layout
n_pins        = 5;     // pins in the test row
pitch         = 8.5;   // pin pitch (3 per 1-inch D&D square)
pin_w         = 6.0;   // square pin width
pin_clear     = 0.3;   // pin-to-channel clearance, per side

// vertical motion
travel        = 30;    // pin travel
levels        = 6;     // number of elevation levels
tooth_pitch   = travel / levels;   // 5 mm = one level

// detent geometry
release_travel = 1.0;  // strip slide to release (fits the inter-pin budget)
engagement     = 0.7;  // blade overlap over tooth tips (horizontal)
tip_recess     = 0.4;  // tooth tips recessed below the pin face
groove_w       = 2.4;  // rack groove width  (also the orientation key)
groove_d       = 1.8;  // rack groove depth
tooth_land     = 2.0;  // vertical land at full tooth protrusion
seat_gap       = 0.1;  // blade-to-flat gap at each detent level

// release strip
blade_w       = 1.8;   // blade tongue width (rides inside the groove)
blade_t       = 1.2;   // blade tongue thickness (top layer of the strip)
bridge_t      = 1.0;   // column bars ("a bit thinner", per design)
rail_t        = 1.5;   // row rails ("equally thick")
strip_clear   = 0.25;  // strip-to-pin / strip-to-pocket plan clearance
strip_h       = 3.7;   // strip thickness
stem_hole_d   = 4.5;   // rubber-band hole in the pull stem

// stack heights
floor_t       = 3;     // floor plate
guide_h       = 34;    // bottom guide grid (below the pocket)
pocket_d      = 4.0;   // pocket depth that the strip slides in
cover_h       = 20;    // top cover grid
pin_proud     = 2;     // pin sticks out this much above the cover when down

// frame
frame_w       = 6;     // border width around the cells
bolt_d        = 3.2;   // M3 stack bolts
peg_d         = 5;     // rubber-band peg on the east wall

// push rod (hand-test tool)
rod_d         = 3.4;
rod_len       = 80;
rod_hole_d    = 3.8;   // rod hole in the floor plate
dimple_d      = 3.6;   // self-centering cone in the pin bottom
dimple_depth  = 2.0;

$fn = $preview ? 32 : 64;
eps = 0.01;

/* =====================  derived values  ===================== */

channel    = pin_w + 2 * pin_clear;            // guide channel width
wall       = pitch - channel;                  // guide wall thickness
tooth_prot = groove_d - tip_recess;            // tooth protrusion from groove floor
ramp_h     = tooth_pitch - tooth_land;         // ramp height per tooth

z_guide_top  = floor_t + guide_h;              // pocket floor (absolute)
z_pocket_top = z_guide_top + pocket_d;         // cover bottom (absolute)
z_top        = z_pocket_top + cover_h;         // cover top (absolute)
blade_top    = z_guide_top + strip_h;          // detent seat plane (absolute)

first_flat = blade_top - floor_t + seat_gap - travel;  // lowest flat on the pin
n_teeth    = levels + 1;
pin_len    = z_top - floor_t + pin_proud;

// frame outline (pin 0 centered at x = 0)
x_cells0 = -channel / 2;
x_cells1 = (n_pins - 1) * pitch + channel / 2;
fx0 = x_cells0 - frame_w;
fx1 = x_cells1 + frame_w;
fy  = channel / 2 + frame_w;

// release strip extents (modeled in the ENGAGED position)
sx0       = -pin_w / 2 - release_travel - strip_clear - bridge_t;  // west crossbar west face
sx1       = (n_pins - 1) * pitch + pin_w / 2 + strip_clear + 2 * bridge_t; // east crossbar east face
rail_out  = channel / 2 + rail_t;
pocket_x0 = sx0;                          // west hard stop = engaged position
pocket_x1 = sx1 + release_travel;         // east hard stop = released position
pocket_hw = rail_out + strip_clear;
stem_len  = fx1 - sx1 + 9;                // stem reaches past the east wall

bolt_xy = [[fx0 + 3,  fy - 2], [fx0 + 3, -(fy - 2)],
           [fx1 - 3,  fy - 2], [fx1 - 3, -(fy - 2)]];

echo(str("channel=", channel, "  wall=", wall, "  pin_len=", pin_len,
         "  first_flat=", first_flat, "  stack_top=", z_top));

/* =====================  modules  ===================== */

function rack_pts() = concat(
    [[-0.5, first_flat]],
    [for (k = [0 : n_teeth - 1]) each [
        [tooth_prot, first_flat + k * tooth_pitch],
        [tooth_prot, first_flat + k * tooth_pitch + tooth_land],
        [0,          first_flat + (k + 1) * tooth_pitch]
    ]],
    [[-0.5, first_flat + n_teeth * tooth_pitch]]);

// ---- pin: square shaft, recessed rack in a groove on the +X face ----
module pin() {
    difference() {
        union() {
            difference() {
                translate([-pin_w/2, -pin_w/2, 0])
                    cube([pin_w, pin_w, pin_len]);
                // groove on the +X face (full length: doubles as the key)
                translate([pin_w/2 - groove_d, -groove_w/2, -eps])
                    cube([groove_d + 1, groove_w, pin_len + 2*eps]);
            }
            // rack teeth inside the groove
            translate([pin_w/2 - groove_d, groove_w/2 + 0.01, 0])
                rotate([90, 0, 0])
                    linear_extrude(groove_w + 0.02)
                        polygon(rack_pts());
        }
        // self-centering cone for the push rod
        translate([0, 0, -eps])
            cylinder(d1 = dimple_d, d2 = 0, h = dimple_depth);
        // top edge chamfers
        for (a = [0, 90, 180, 270])
            rotate([0, 0, a])
                translate([pin_w/2, 0, pin_len])
                    rotate([0, 45, 0])
                        cube([1.4, pin_w + 2, 1.4], center = true);
    }
}

// ---- bottom guide grid with the strip pocket on top ----
module grid_bottom() {
    h = guide_h + pocket_d;
    difference() {
        union() {
            translate([fx0, -fy, 0]) cube([fx1 - fx0, 2*fy, h]);
            // rubber-band peg on the east exterior wall
            translate([fx1 - eps, 0, 12]) rotate([0, 90, 0]) {
                cylinder(d = peg_d, h = 8);
                translate([0, 0, 8]) cylinder(d = peg_d + 3, h = 2);
            }
        }
        // pin channels
        for (i = [0 : n_pins - 1])
            translate([i*pitch - channel/2, -channel/2, -eps])
                cube([channel, channel, h + 2*eps]);
        // sliding pocket for the release strip
        translate([pocket_x0, -pocket_hw, guide_h])
            cube([pocket_x1 - pocket_x0, 2*pocket_hw, pocket_d + eps]);
        // stem slot through the east wall
        translate([pocket_x1 - 0.5, -2 - strip_clear - 0.3, guide_h])
            cube([fx1 - pocket_x1 + 2, 2*(2 + strip_clear + 0.3), pocket_d + eps]);
        // stack bolt holes
        for (p = bolt_xy)
            translate([p[0], p[1], -eps]) cylinder(d = bolt_d, h = h + 2*eps);
    }
}

// ---- release strip ("printed wire comb"), modeled ENGAGED ----
module release_strip() {
    difference() {
        union() {
            // row rails (full thickness)
            for (s = [1, -1])
                translate([sx0, s*channel/2 + (s > 0 ? 0 : -rail_t), 0])
                    cube([sx1 - sx0, rail_t, strip_h]);
            // west + east crossbars
            translate([sx0, -rail_out, 0]) cube([bridge_t, 2*rail_out, strip_h]);
            translate([sx1 - bridge_t, -rail_out, 0]) cube([bridge_t, 2*rail_out, strip_h]);
            // column bridges (the "a bit thinner" bars), one east of each pin
            for (i = [0 : n_pins - 1])
                translate([i*pitch + pin_w/2 + strip_clear, -rail_out, 0])
                    cube([bridge_t, 2*rail_out, strip_h]);
            // blade tongues: thin top-layer fingers reaching into each groove
            for (i = [0 : n_pins - 1])
                translate([i*pitch + pin_w/2 - engagement - tip_recess, -blade_w/2,
                           strip_h - blade_t])
                    cube([engagement + tip_recess + strip_clear + bridge_t,
                          blade_w, blade_t]);
            // pull stem with a band paddle on the end
            translate([sx1 - 1, -2, 0]) cube([stem_len, 4, strip_h]);
            translate([sx1 - 1 + stem_len - eps, -4.5, 0])
                cube([7, 9, strip_h]);
        }
        // blade tip underside chamfers (smooth camming on the ramps)
        for (i = [0 : n_pins - 1])
            translate([i*pitch + pin_w/2 - engagement - tip_recess, 0,
                       strip_h - blade_t])
                rotate([0, 45, 0])
                    cube([0.9, blade_w + 1, 0.9], center = true);
        // rubber-band hole in the paddle
        translate([sx1 - 1 + stem_len + 3.5, 0, -eps])
            cylinder(d = stem_hole_d, h = strip_h + 2*eps);
    }
}

// ---- top cover grid ----
module grid_top() {
    difference() {
        translate([fx0, -fy, 0]) cube([fx1 - fx0, 2*fy, cover_h]);
        for (i = [0 : n_pins - 1]) {
            translate([i*pitch - channel/2, -channel/2, -eps])
                cube([channel, channel, cover_h + 2*eps]);
            // flared mouth for easy pin insertion
            translate([i*pitch, 0, cover_h - 1.4])
                linear_extrude(1.4 + eps, scale = (channel + 2.4) / channel)
                    square(channel, center = true);
        }
        for (p = bolt_xy)
            translate([p[0], p[1], -eps]) cylinder(d = bolt_d, h = cover_h + 2*eps);
    }
}

// ---- floor plate ----
module floor_plate() {
    difference() {
        translate([fx0, -fy, 0]) cube([fx1 - fx0, 2*fy, floor_t]);
        for (i = [0 : n_pins - 1])
            translate([i*pitch, 0, -eps]) cylinder(d = rod_hole_d, h = floor_t + 2*eps);
        for (p = bolt_xy)
            translate([p[0], p[1], -eps]) cylinder(d = bolt_d, h = floor_t + 2*eps);
    }
}

// ---- hand-test push rod ----
module push_rod() {
    cylinder(d = rod_d, h = rod_len - rod_d/2);
    translate([0, 0, rod_len - rod_d/2]) sphere(d = rod_d);
}

// ---- printable pin batch: lying down, groove facing up ----
module pins_print() {
    for (i = [0 : n_pins - 1])
        translate([pin_len/2, i * (pin_w + 4), pin_w/2])
            rotate([0, -90, 0]) pin();
}

// ---- assembly view ----
module assembly(lifts = [0, 2, 5, 6, 3], released = false) {
    color("#9a9a92") floor_plate();
    color("#c8c4b8") translate([0, 0, floor_t]) grid_bottom();
    color("#ef9f27")
        translate([released ? release_travel : 0, 0, z_guide_top])
            release_strip();
    color("#7a9bb5", 0.35) translate([0, 0, z_pocket_top]) grid_top();
    for (i = [0 : n_pins - 1])
        color("#1d9e75")
            translate([i*pitch, 0, floor_t + tooth_pitch * lifts[i]])
                pin();
    // a push rod parked under pin 3
    color("#854f0b")
        translate([3*pitch, 0, floor_t + tooth_pitch*lifts[3] - rod_len])
            push_rod();
}

/* =====================  render  ===================== */

if      (part == "pin")              pin();
else if (part == "pins_print")       pins_print();
else if (part == "grid_bottom")      grid_bottom();
else if (part == "release_strip")    release_strip();
else if (part == "grid_top")         grid_top();
else if (part == "floor_plate")      floor_plate();
else if (part == "push_rod")         push_rod();
else if (part == "assembly_released") assembly(lifts = [0,0,0,0,0], released = true);
else if (part == "assembly")          assembly();
