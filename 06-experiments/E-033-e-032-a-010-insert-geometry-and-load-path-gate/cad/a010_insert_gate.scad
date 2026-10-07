// E-033 A-010 analytical envelope CAD.
// Units: mm.  This is geometry evidence, not a fabrication-ready process file.

pitch = 5.08;
active = 25.40;
cartridge = 30.48;
aperture = 3.00;
slider_t = 0.40;
guide_t = 0.40;
stop_t = 0.80;
state_step = 0.80;
follower_d = 1.20;

module cell_aperture(x, y, z, shift=0) {
    translate([x + shift, y, z]) cube([aperture, aperture, 0.01], center=true);
}

module gate_slider(x, y, z, state=2) {
    // Representative 4.20 x 4.60 slider; state apertures are indexed in X.
    difference() {
        translate([x, y, z + slider_t/2]) cube([4.20, 4.60, slider_t], center=true);
        cell_aperture(x + (state - 2) * state_step, y, z + slider_t/2);
    }
}

module guide_plate(z) {
    difference() {
        translate([0, 0, z + guide_t/2]) cube([cartridge, cartridge, guide_t], center=true);
        for (row=[-2:2]) for (col=[-2:2])
            translate([col*pitch, row*pitch, z + guide_t/2])
                cube([4.50, 4.90, guide_t + 0.02], center=true);
    }
}

module stop_plate(z) {
    // Five shelves, 0.80 mm pitch.  The plate is shown as an envelope;
    // shelf stiffness and contact stress are intentionally not simulated.
    difference() {
        translate([0, 0, z + stop_t/2]) cube([cartridge, cartridge, stop_t], center=true);
        for (row=[-2:2]) for (col=[-2:2])
            translate([col*pitch, row*pitch, z + stop_t/2])
                cube([3.40, 3.40, stop_t + 0.02], center=true);
    }
}

// Exploded section-friendly assembly at the declared frame datum z=0.
guide_plate(0.00);                    // lower guide, z 0.00..0.40
for (row=[-2:2]) for (col=[-2:2])
    gate_slider(col*pitch, row*pitch, 0.40, 2);
guide_plate(0.80);                    // upper guide, z 0.80..1.20
stop_plate(1.20);                     // five-stop plate, z 1.20..1.80

// Representative follower at the reader target; load shoulder is above the
// stop plate and is not part of the gate.  It makes the bypass path visible.
translate([0, 0, 1.80]) cylinder(h=2.00, d=follower_d, $fn=32);
translate([0, 0, 1.80]) cylinder(h=0.35, d=3.00, $fn=32);
