/*
 * Test11 — selector-fan-out coupon at FINAL 5.08 mm pitch (S3/S4 family).
 *
 * The S3/S4 shared-drive family needs 320-400 printable per-column selectors
 * that a common short stroke can program without a bought actuator per column.
 * Test07 already produced a functionally relevant one: a sliding-gate latch
 * ("release strip") that clicks one 5 mm tooth per push and holds the load
 * passively via a spring return band.
 *
 * This file does NOT clone Test07's 8.5 mm geometry.  It re-derives the SAME
 * mechanism at r = 2.54 mm pitch (4 cells per 1" D&D square) so the two
 * decisive questions can be answered by one print:
 *
 *   1. Does a sliding-gate latch survive at final pitch, where the inter-cell
 *      wall band is only (5.08 - 4.88) = 0.20 mm and the gate slot cannot be a
 *      1.0 mm linear slide?
 *   2. What is the actual engaged overlap, tooth land and retaining-face shear
 *      area, so the 5 N abuse gate is a measured number rather than a guess?
 *
 * The band is 0.20 mm because it holds Test09's 4.68 mm body and 0.10 mm/side
 * clearance unchanged.  A wider 4.78 mm body at 0.05 mm/side gives a 0.40 mm
 * band but lowers Test09's surface fill and must be re-run there; this coupon
 * only demonstrates that one specific thin-wall remedy *exists*, not that it is
 * qualified.
 *
 * This is NOT a full dynamic selector.  The command gate (rotary solenoid or
 * micro-motor) and the moving drive bar are out of scope for this coupon; the
 * analytical model in coupon_geometry.py bounds them.  What is printed here is
 * the passive load-bearing latch at final pitch plus its gate slot.
 *
 * Vanilla OpenSCAD, no external libraries.  Geometry only; not a printer or
 * material qualification.
 *
 * Print:  part = "grid"       the latch-cluster block
 *         part = "plate"      the 2x4 retention-abuse tile (separate coupon)
 *         part = "carriers"   the interchangeable carriers
 *         part = "gate"       the sliding gate coupon piece
 *         part = "assembly"   carriers + gates in the cluster (engaged)
 */

part = "assembly"; // [assembly, grid, plate, carriers, gate, paddles]

/* =====================  parameters (mm)  ===================== */
pitch      = 5.08;   // FINAL pitch (2.54 radius = 4 cells per 1" square)
n_cols     = 4;
n_rows     = 2;

body       = 4.68;   // Test09 column body
clear      = 0.10;   // per-side body-to-channel clearance
channel    = body + 2*clear;          // 4.88
wall       = pitch - channel;         // 0.20 total inter-cell wall
wall_half  = wall/2;                  // 0.10 nominal half-band

// tooth / latch geometry
levels     = 5;
level_pitch = 10.0;   // 40 mm / (5-1)
tooth_pitch = level_pitch;
tooth_prot = 1.20;    // tooth protrusion from the rack face
tooth_land = 2.50;    // vertical land at full protrusion
tip_recess = 0.40;    // tooth tips recessed below the carrier face

// sliding gate (Test07 "blade") re-derived for the thin band
gate_w     = 0.50;    // finger width across the drive-bar channel (Y)
gate_t     = 1.20;    // finger thickness (thin dimension, X)
engagement = 0.90;    // intended finger overlap into the tooth envelope
gate_travel= 1.00;    // linear slide to release (Test07)
gate_slot  = gate_w + 0.30;   // slot opening for the finger
slot_wall  = 0.40;    // minimum printable wall each side of the slot

// stack
carrier_h  = 10.0;    // one removable carrier = one row segment
floor_h    = 3.0;
tier_gap   = 12.0;    // clearance between tallest tooth and the tier above

// retention plate coupon
plate_t    = 4.0;
plate_bore = 5.0;     // latch tooth bores, one per level
plate_hole_d = 1.2;   // Test09 gauge shaft diameter

// print/assembly
latch_dowel_d = 2.2;  // release dowel (Test07 interface)
paddle_w   = 8.0;

$fn = 64;
eps = 0.01;

/* =====================  derived  ===================== */
cx0 = 0; cx1 = (n_cols-1)*pitch;
cy0 = 0; cy1 = (n_rows-1)*pitch;

fx0 = -channel/2 - 1.5;  fx1 = cx1 + channel/2 + 1.5;
fy0 = -channel/2 - 1.5;  fy1 = cy1 + channel/2 + 1.5;

n_teeth = levels + 1;
rack_top = carrier_h - tip_recess;
first_flat = rack_top - n_teeth*tooth_pitch;  // may be negative -> clipped by carrier_h

gate_z = carrier_h/2 - gate_t/2;   // gate rides mid-carrier (a stand-in seat)

echo(str("TEST11 pitch=", pitch, " wall=", wall, " channel=", channel,
         " gate_slot=", gate_slot, " finger+gaps=", gate_slot+2*slot_wall));
if (wall < 0.18)
    echo("WARNING: inter-cell wall below 0.18 mm; gate slot wall cannot be printed");

/* =====================  modules  ===================== */

// rack on the -Y face of a carrier, teeth running in Z
function rack_pts() = concat(
    [[-0.5, first_flat]],
    [for (k = [0 : n_teeth-1]) each [
        [tooth_prot, first_flat + k*tooth_pitch],
        [tooth_prot, first_flat + k*tooth_pitch + tooth_land],
        [0,          first_flat + (k+1)*tooth_pitch]
    ]],
    [[-0.5, first_flat + n_teeth*tooth_pitch]]);

// One interchangeable carrier: square block, capped top, rack in a groove on
// the -Y face facing the gate channel.  The visible cap must stay solid.
module carrier() {
    difference() {
        union() {
            difference() {
                translate([-body/2, -body/2, 0]) cube([body, body, carrier_h]);
                // rack groove on the -Y face
                translate([-tooth_prot-0.2, -body/2 - eps, first_flat])
                    cube([tooth_prot+0.4, 1.8+eps, rack_top-first_flat+0.2]);
            }
            // teeth
            translate([-body/2, -body/2 + 1.8, 0])
                rotate([-90, 0, 0])
                    linear_extrude(body/2 - 1.8)
                        polygon(rack_pts());
        }
        // bottom cone/pocket facing the drive bar (not modelled in detail)
        translate([0, 0, -eps]) cylinder(d1=2.4, d2=0, h=1.2);
    }
}

// The sliding gate that engages one carrier's rack: a finger in the -Y groove
// slot.  Modelled in its seated (engaged) position; slides +Y by gate_travel.
// The slot through the 0.20 mm inter-cell band is the geometry under test.
module gate() {
    // finger reaches from the channel wall into the tooth envelope by engagement
    translate([-gate_t/2, -gate_w/2, gate_z])
        cube([gate_t, gate_w, carrier_h - 2.0]);
    // camming ramp on the finger's top edge (Test07 tipping action)
    translate([-gate_t/2, -gate_w/2, gate_z])
        rotate([0, 45, 0])
            cube([0.6, gate_w+0.2, 0.6], center=true);
    // pull stem out to the +Y edge of the cluster
    translate([-gate_t/2, gate_w/2, gate_z])
        cube([gate_t, fy1 - gate_w/2, gate_w]);
    translate([-gate_t/2, fy1 - 1, gate_z])
        cube([gate_t, paddle_w, gate_w]);
}

// Cluster block: the lattice holding carriers + one gate slot per column.
module grid() {
    difference() {
        translate([fx0, fy0, 0]) cube([fx1-fx0, fy1-fy0, carrier_h]);
        // carrier channels
        for (j=[0:n_rows-1], i=[0:n_cols-1])
            translate([i*pitch - channel/2, j*pitch - channel/2, -eps])
                cube([channel, channel, carrier_h+2*eps]);
        // gate slots through the inter-column bands (-Y face of each carrier)
        for (j=[0:n_rows-1], i=[0:n_cols-1])
            translate([i*pitch - gate_t/2 - 0.05,
                       j*pitch - channel/2 - gate_slot,
                       gate_z - 1.0])
                cube([gate_t + 0.10, gate_slot, carrier_h - 4.0 + 2.0]);
        // release dowel holes
        for (j=[0:n_rows-1], i=[0:n_cols-1])
            translate([i*pitch, fy1 - 1.5, -eps])
                cylinder(d=latch_dowel_d, h=carrier_h+2*eps);
    }
}

// Retention-abuse coupon: one latch tooth pattern per level as a strong,
// separately-orientable tile.  Push a calibrated rod through each bore against
// a printed tooth and measure force to slip / break / permanent set.
module plate() {
    difference() {
        translate([0, 0, 0]) cube([(levels-1)*pitch + 6, 10, plate_t]);
        for (k=[0:levels-2])
            translate([(k+0.5)*pitch + 3, 5, -eps])
                cylinder(d=plate_bore, h=plate_t+2*eps);
        // tooth under each bore edge, standing proud by tooth_prot in -Y
        for (k=[0:levels-2])
            translate([(k+0.5)*pitch + 3, 3.0, -eps])
                cube([tooth_prot, tooth_land, plate_t+eps]);
        translate([1.5, 5, -eps]) cylinder(d=plate_hole_d, h=plate_t+2*eps);
        translate([(levels-1)*pitch + 4.5, 5, -eps])
            cylinder(d=plate_hole_d, h=plate_t+2*eps);
    }
}

module carriers() {
    for (j=[0:n_rows-1], i=[0:n_cols-1])
        translate([i*pitch, j*pitch, 0]) carrier();
}

module paddles() {
    for (j=[0:n_rows-1]) translate([0, j*pitch, 0]) gate();
}

module assembly() {
    color("#c8c4b8") grid();
    color("#1d9e75") carriers();
    color("#ef9f27") paddles();
}

if (part == "carrier" || part == "carriers")      carriers();
else if (part == "gate")                           gate();
else if (part == "paddles")                        paddles();
else if (part == "grid")                           grid();
else if (part == "plate")                          plate();
else if (part == "assembly")                       assembly();
else assert(false, "unknown part");
