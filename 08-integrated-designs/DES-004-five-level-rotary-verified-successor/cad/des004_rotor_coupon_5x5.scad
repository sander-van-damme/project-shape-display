// DES-004 5x5 rotor coupon, geometry gate only.
// Render printable parts with: openscad -D 'part="frame"' ...
// No physical fit, load, cycle-life, or reader validation is implied.

$fn = 48;

PITCH = 5.08;
N = 5;
FIELD = N * PITCH;                 // 25.40 mm, centre-to-centre span
FRAME = 40.0;
FRAME_T = 3.0;
ROTOR_R = 1.50;
ROTOR_T = 3.0;
POCKET_R = 1.70;                   // 0.40 mm diametral running allowance
AXLE_D = 1.00;                     // proposed coupon pin, not a procurement choice
BORE_D = 1.40;                     // 0.40 mm diametral bore allowance
VANE_T = 0.45;
VANE_W = 1.20;
VANE_OFFSET = 1.70;
READER_APERTURE_W = 0.70;
READER_APERTURE_H = 1.00;
READER_STANDOFF = 1.80;
READER_HEAD_X = 2.00;
READER_HEAD_Y = 2.00;
READER_HEAD_Z = 4.00;
WRITER_TONGUE_T = 0.80;
WRITER_TONGUE_W = 1.00;
WRITER_ENGAGEMENT = 1.00;
WRITER_POCKET_T = 1.20;
WRITER_POCKET_W = 1.40;
RETAINER_T = 1.0;
part = "frame";

function cell(i) = (i - (N - 1) / 2) * PITCH;

module frame() {
    difference() {
        cube([FRAME, FRAME, FRAME_T], center = true);
        for (i = [0:N-1]) for (j = [0:N-1])
            translate([cell(i), cell(j), 0])
                cylinder(r = POCKET_R, h = FRAME_T + 0.4, center = true);
    }
}

module rotor() {
    difference() {
        cylinder(r = ROTOR_R, h = ROTOR_T, center = true);
        cylinder(d = BORE_D, h = ROTOR_T + 0.4, center = true);
    }
    // Frame-fixed/readback vane envelope. It is deliberately simple: this
    // coupon checks pitch, neighbour clearance, and axle/bore fit only.
    translate([VANE_OFFSET, 0, 0])
        cube([VANE_T, VANE_W, ROTOR_T], center = true);
}

module rotors() {
    for (i = [0:N-1]) for (j = [0:N-1])
        translate([cell(i), cell(j), ROTOR_T / 2 + 0.2]) rotor();
}

module axle_sample() {
    cylinder(d = AXLE_D, h = 10.0, center = true);
}

module writer_sample() {
    cube([WRITER_TONGUE_T, WRITER_TONGUE_W, WRITER_ENGAGEMENT], center = true);
}

module reader_sample() {
    difference() {
        cube([READER_HEAD_X, READER_HEAD_Y, READER_HEAD_Z], center = true);
        translate([0, 0, READER_HEAD_Z/2 - READER_STANDOFF])
            cube([READER_APERTURE_W, READER_APERTURE_H, 0.4], center = true);
    }
}

module assembly() {
    color("lightgray") frame();
    color("orange") rotors();
}

if (part == "frame") frame();
else if (part == "rotors") rotors();
else if (part == "axle") axle_sample();
else if (part == "writer") writer_sample();
else if (part == "reader") reader_sample();
else assembly();

echo(str("DES004 5x5 field span = ", FIELD, " mm"));
echo(str("frame margin per side = ", (FRAME - FIELD) / 2, " mm"));
echo(str("rotor-pocket radial clearance = ", POCKET_R - ROTOR_R, " mm"));
echo(str("axle-bore diametral clearance = ", BORE_D - AXLE_D, " mm"));
echo(str("nearest rotor edge gap = ", PITCH - 2 * ROTOR_R, " mm"));
echo(str("writer tongue = ", WRITER_TONGUE_T, " x ", WRITER_TONGUE_W,
         " x ", WRITER_ENGAGEMENT, " mm"));
echo(str("reader aperture = ", READER_APERTURE_W, " x ", READER_APERTURE_H,
         " mm at ", READER_STANDOFF, " mm standoff"));
