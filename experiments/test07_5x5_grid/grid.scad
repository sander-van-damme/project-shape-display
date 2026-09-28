/*
 * Shape display — trial 7: sliding-release grid (5x5), capped pins
 * For Sander Van Damme's "3D grid map" project.
 *
 * Carries over trial 6's three-layer "sandwich":
 *   1. floor plate       - down-stop for pins + rod access holes
 *   2. bottom guide grid - pins slide in square channels (+ strip tray on top)
 *   3. release strips     - one printed "wire comb" PER ROW, slides 1 mm
 *   4. top cover grid      - protects the strips, extra pin guidance
 *
 * Changes vs. trial 6:
 *   - real N_cols x N_rows grid (default 5x5) instead of a 1x5 test strip
 *   - pins are CAPPED: the rack groove stops below the top, leaving a clean
 *     solid square cap as the visible display surface
 *   - one independent release comb per row (so camming a pin in one row
 *     cannot momentarily unlock its neighbours), tiled at the row pitch
 *
 * The under-display caddy / actuation (push-rod lift + lock release) is
 * developed separately once the actuation approach is chosen; this file is
 * the passive "display stack" that the caddy drives from below.
 *
 * Vanilla OpenSCAD, no libraries required.
 */

part = "assembly"; // [assembly, assembly_released, pin, pins_print, grid_bottom, release_strip, release_strips, grid_top, floor_plate, push_rod, release_dowel]

/* =====================  parameters (mm)  ===================== */

// layout
n_cols        = 5;     // pins per row (east-west, x)
n_rows        = 5;     // rows (north-south, y)
pitch         = 8.5;   // pin pitch (3 per 1-inch D&D square)
pin_w         = 6.0;   // square pin width
pin_clear     = 0.3;   // pin-to-channel clearance, per side

// vertical motion
travel        = 30;    // pin travel
levels        = 6;     // number of elevation levels
tooth_pitch   = travel / levels;   // 5 mm = one level

// detent geometry
release_travel = 1.0;  // strip slide to release
engagement     = 0.7;  // blade overlap over tooth tips (horizontal)
tip_recess     = 0.4;  // tooth tips recessed below the pin face
groove_w       = 2.4;  // rack groove width  (also the orientation key)
groove_d       = 1.8;  // rack groove depth
tooth_land     = 2.0;  // vertical land at full tooth protrusion
seat_gap       = 0.1;  // blade-to-flat gap at each detent level
cap_gap        = 3.0;  // solid pin material kept above the top rack tooth

// release strip (sized to fit one row band at the grid pitch)
row_gap       = 0.30;  // plan gap between adjacent row combs
blade_w       = 1.8;   // blade tongue width (rides inside the groove)
blade_t       = 1.2;   // blade tongue thickness (top layer of the strip)
bridge_t      = 1.0;   // column bars between pins (take the cam load)
strip_clear   = 0.25;  // strip-to-pin / strip-to-tray clearance
strip_h       = 3.7;   // strip thickness
stem_hole_d   = 4.5;   // rubber-band hole in the pull stem

// stack heights
floor_t       = 3;     // floor plate
guide_h       = 34;    // bottom guide grid (below the tray)
pocket_d      = 4.0;   // strip tray depth
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

// caddy release interface: a dowel hangs from each row comb down to the
// caddy plane, so a finger on the caddy can trip the spring lock from below.
caddy_release = true;  // add the from-below release dowels + their slots
dowel_d       = 2.2;   // release dowel diameter (or use 2 mm rod / filament)
dowel_drop    = 3;     // dowel protrudes this far below the floor underside
dowel_clr     = 0.3;   // dowel-to-slot clearance per side
dowel_seat    = 2.4;   // dowel press-fit depth into the comb crossbar

$fn = $preview ? 32 : 64;
eps = 0.01;

/* =====================  derived values  ===================== */

channel    = pin_w + 2 * pin_clear;            // guide channel width
wall       = pitch - channel;                  // guide wall thickness
tooth_prot = groove_d - tip_recess;            // tooth protrusion from groove floor
ramp_h     = tooth_pitch - tooth_land;         // ramp height per tooth

z_guide_top  = floor_t + guide_h;              // tray floor (absolute)
z_pocket_top = z_guide_top + pocket_d;         // cover bottom (absolute)
z_top        = z_pocket_top + cover_h;         // cover top (absolute)
blade_top    = z_guide_top + strip_h;          // detent seat plane (absolute)

first_flat = blade_top - floor_t + seat_gap - travel;  // lowest flat on the pin
n_teeth    = levels + 1;
pin_len    = z_top - floor_t + pin_proud;
rack_top   = first_flat + n_teeth * tooth_pitch;       // pin-local top of rack
groove_top = rack_top + cap_gap;                       // groove ends here -> cap above
cap_h      = pin_len - groove_top;                     // resulting solid cap height

// release comb extents, sized to the row band ---------------------
rail_out  = pitch/2 - row_gap;                 // comb half-width (y) tiles at pitch
rail_t    = rail_out - channel/2;              // row-rail thickness (auto from pitch)
sx0       = -pin_w/2 - release_travel - strip_clear - bridge_t;             // west crossbar west face
sx1       = (n_cols - 1) * pitch + pin_w/2 + strip_clear + 2 * bridge_t;    // east crossbar east face

// frame outline (cell 0,0 centred at origin)
cx0 = -channel/2;  cx1 = (n_cols - 1)*pitch + channel/2;
cy0 = -channel/2;  cy1 = (n_rows - 1)*pitch + channel/2;
fx0 = cx0 - frame_w;  fx1 = cx1 + frame_w;
fy0 = cy0 - frame_w;  fy1 = cy1 + frame_w;

stem_len  = fx1 - sx1 + 9;              // stem reaches past the east wall

// release dowel: hangs from the west crossbar down past the floor
dowel_x   = sx0 + bridge_t/2;                       // centre of the west crossbar
dowel_len = (z_guide_top + dowel_seat) + dowel_drop;  // comb seat -> below floor

bolt_xy = [[fx0 + 3, fy0 + 3], [fx0 + 3, fy1 - 3],
           [fx1 - 3, fy0 + 3], [fx1 - 3, fy1 - 3]];

echo(str("grid=", n_cols, "x", n_rows, "  channel=", channel, "  wall=", wall,
         "  rail_t=", rail_t, "  pin_len=", pin_len, "  cap_h=", cap_h,
         "  stack_top=", z_top));
if (rail_t < 0.6) echo("WARNING: rail_t very thin - consider a larger pitch");

/* =====================  modules  ===================== */

function rack_pts() = concat(
    [[-0.5, first_flat]],
    [for (k = [0 : n_teeth - 1]) each [
        [tooth_prot, first_flat + k * tooth_pitch],
        [tooth_prot, first_flat + k * tooth_pitch + tooth_land],
        [0,          first_flat + (k + 1) * tooth_pitch]
    ]],
    [[-0.5, first_flat + n_teeth * tooth_pitch]]);

// ---- pin: square shaft, recessed rack in a groove, SOLID CAP on top ----
module pin() {
    difference() {
        union() {
            difference() {
                translate([-pin_w/2, -pin_w/2, 0])
                    cube([pin_w, pin_w, pin_len]);
                // groove on the +X face - stops below the top to leave a cap
                translate([pin_w/2 - groove_d, -groove_w/2, -eps])
                    cube([groove_d + 1, groove_w, groove_top + eps]);
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
        // top edge chamfers on the cap
        for (a = [0, 90, 180, 270])
            rotate([0, 0, a])
                translate([pin_w/2, 0, pin_len])
                    rotate([0, 45, 0])
                        cube([1.4, pin_w + 2, 1.4], center = true);
    }
}

// ---- bottom guide grid with the strip tray on top ----
module grid_bottom() {
    h = guide_h + pocket_d;
    difference() {
        union() {
            translate([fx0, fy0, 0]) cube([fx1 - fx0, fy1 - fy0, h]);
            // one rubber-band peg per row on the east exterior wall
            for (j = [0 : n_rows - 1])
                translate([fx1 - eps, j*pitch, 12]) rotate([0, 90, 0]) {
                    cylinder(d = peg_d, h = 8);
                    translate([0, 0, 8]) cylinder(d = peg_d + 3, h = 2);
                }
        }
        // pin channels (full grid)
        for (j = [0 : n_rows - 1], i = [0 : n_cols - 1])
            translate([i*pitch - channel/2, j*pitch - channel/2, -eps])
                cube([channel, channel, h + 2*eps]);
        // strip tray (single recess across all rows; combs tile it)
        translate([sx0, fy0 + frame_w - rail_out - strip_clear, guide_h])
            cube([sx1 + release_travel - sx0,
                  (cy1 - cy0) + 2*(rail_out + strip_clear), pocket_d + eps]);
        // stem slot through the east wall, one per row
        for (j = [0 : n_rows - 1])
            translate([sx1 + release_travel - 0.5, j*pitch - 2 - strip_clear - 0.3, guide_h])
                cube([fx1 - (sx1 + release_travel) + 2,
                      2*(2 + strip_clear + 0.3), pocket_d + eps]);
        // release-dowel slots through the guide (allow the 1 mm release slide)
        if (caddy_release)
            for (j = [0 : n_rows - 1])
                translate([dowel_x - dowel_d/2 - dowel_clr,
                           j*pitch - dowel_d/2 - dowel_clr, -eps])
                    cube([dowel_d + release_travel + 2*dowel_clr,
                          dowel_d + 2*dowel_clr, guide_h + 2*eps]);
        // stack bolt holes
        for (p = bolt_xy)
            translate([p[0], p[1], -eps]) cylinder(d = bolt_d, h = h + 2*eps);
    }
}

// ---- release comb for ONE row ("printed wire comb"), modelled ENGAGED ----
module release_strip() {
    difference() {
        union() {
            // row rails (full thickness)
            for (s = [1, -1])
                translate([sx0, s > 0 ? channel/2 : -channel/2 - rail_t, 0])
                    cube([sx1 - sx0, rail_t, strip_h]);
            // west + east crossbars
            translate([sx0, -rail_out, 0]) cube([bridge_t, 2*rail_out, strip_h]);
            translate([sx1 - bridge_t, -rail_out, 0]) cube([bridge_t, 2*rail_out, strip_h]);
            // column bridges (one east of each pin) - carry the cam load
            for (i = [0 : n_cols - 1])
                translate([i*pitch + pin_w/2 + strip_clear, -rail_out, 0])
                    cube([bridge_t, 2*rail_out, strip_h]);
            // blade tongues: thin top-layer fingers into each groove
            for (i = [0 : n_cols - 1])
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
        for (i = [0 : n_cols - 1])
            translate([i*pitch + pin_w/2 - engagement - tip_recess, 0,
                       strip_h - blade_t])
                rotate([0, 45, 0])
                    cube([0.9, blade_w + 1, 0.9], center = true);
        // rubber-band hole in the paddle
        translate([sx1 - 1 + stem_len + 3.5, 0, -eps])
            cylinder(d = stem_hole_d, h = strip_h + 2*eps);
        // socket for the release dowel in the west crossbar (press fit)
        if (caddy_release)
            translate([dowel_x, 0, strip_h - dowel_seat])
                cylinder(d = dowel_d, h = dowel_seat + eps);
    }
}

// ---- release dowel: separate rod, hangs from a comb to the caddy plane ----
module release_dowel() {
    cylinder(d = dowel_d, h = dowel_len);
    // small collar marks the rest depth at the floor underside
    translate([0, 0, dowel_drop]) cylinder(d = dowel_d + 1.2, h = 0.8);
}

// all row combs in place (engaged), for a print plate / inspection
module release_strips(released = false) {
    for (j = [0 : n_rows - 1])
        translate([released ? release_travel : 0, j*pitch, 0]) release_strip();
}

// ---- top cover grid ----
module grid_top() {
    difference() {
        translate([fx0, fy0, 0]) cube([fx1 - fx0, fy1 - fy0, cover_h]);
        for (j = [0 : n_rows - 1], i = [0 : n_cols - 1]) {
            translate([i*pitch - channel/2, j*pitch - channel/2, -eps])
                cube([channel, channel, cover_h + 2*eps]);
            // flared mouth for easy pin insertion
            translate([i*pitch, j*pitch, cover_h - 1.4])
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
        translate([fx0, fy0, 0]) cube([fx1 - fx0, fy1 - fy0, floor_t]);
        for (j = [0 : n_rows - 1], i = [0 : n_cols - 1])
            translate([i*pitch, j*pitch, -eps])
                cylinder(d = rod_hole_d, h = floor_t + 2*eps);
        // release-dowel slots through the floor (allow the 1 mm release slide)
        if (caddy_release)
            for (j = [0 : n_rows - 1])
                translate([dowel_x - dowel_d/2 - dowel_clr,
                           j*pitch - dowel_d/2 - dowel_clr, -eps])
                    cube([dowel_d + release_travel + 2*dowel_clr,
                          dowel_d + 2*dowel_clr, floor_t + 2*eps]);
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
module pins_print(cols = n_cols, rows = 2) {
    for (j = [0 : rows - 1], i = [0 : cols - 1])
        translate([pin_len/2 + i*(pin_len + 4), j*(pin_w + 4), pin_w/2])
            rotate([0, -90, 0]) pin();
}

// demo height field (levels), centred pyramid
demo = [[0,1,2,1,0],
        [1,2,3,2,1],
        [2,3,5,3,2],
        [1,2,3,2,1],
        [0,1,2,1,0]];

function lift_of(i, j) =
    (j < len(demo) && i < len(demo[0])) ? demo[j][i] : 0;

// ---- assembly view ----
module assembly(released = false) {
    color("#9a9a92") floor_plate();
    color("#c8c4b8") translate([0, 0, floor_t]) grid_bottom();
    color("#ef9f27")
        translate([0, 0, z_guide_top]) release_strips(released = released);
    // release dowels hanging from each comb down to the caddy plane
    if (caddy_release)
        for (j = [0 : n_rows - 1])
            color("#b5651d")
                translate([dowel_x + (released ? release_travel : 0),
                           j*pitch, -dowel_drop]) release_dowel();
    color("#7a9bb5", 0.30) translate([0, 0, z_pocket_top]) grid_top();
    for (j = [0 : n_rows - 1], i = [0 : n_cols - 1])
        color("#1d9e75")
            translate([i*pitch, j*pitch,
                       floor_t + tooth_pitch * (released ? 0 : lift_of(i, j))])
                pin();
}

/* =====================  render  ===================== */
// Skipped when this file is included as a library (LIBRARY_MODE = true).
if (is_undef(LIBRARY_MODE) || !LIBRARY_MODE) {
if      (part == "pin")               pin();
else if (part == "pins_print")        pins_print();
else if (part == "grid_bottom")       grid_bottom();
else if (part == "release_strip")     release_strip();
else if (part == "release_strips")    release_strips();
else if (part == "grid_top")          grid_top();
else if (part == "floor_plate")       floor_plate();
else if (part == "push_rod")          push_rod();
else if (part == "release_dowel")     release_dowel();
else if (part == "assembly_released") assembly(released = true);
else if (part == "assembly")          assembly();
}
