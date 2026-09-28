// test11 - S3 selector fan-out coupon, parametric.
//
// This is the cheapest geometric gate for S3. It asks one question:
//   Can FOUR independently rockable selector fingers plus one shared 4-plane
//   cam bank be packed inside ONE 5.08 mm cell band, and can a 2x4 section be
//   printed on the X1C with a 0.4 mm nozzle?
//
// It is a *fit coupon*, not a mechanism. It has no springs, no drive and no
// tooth engagement; those are Stage-C questions after this geometry is printed
// and measured.
//
// Render:
//   openscad -o selector_fanout_coupon.stl selector_fanout_coupon.scad
//   openscad -D 'part="bank"' ...
//   openscad -D 'part="finger"' ...
//   openscad -D 'part="assembled_2x4"' ...

PITCH = 5.08;          // project pitch
ROWS_PER_STATION = 4;  // one station services 4 rows
BAND = PITCH / ROWS_PER_STATION;   // 1.27 mm axial land per row on the cam bank

// --- printed finger geometry -------------------------------------------------
FINGER_T = 0.80;       // finger thickness along the row axis (band is 1.27)
FINGER_H = 3.20;       // finger height (rocker)
FINGER_L = 4.40;       // finger length along travel
PIVOT_D = 0.80;        // printed pivot boss diameter
NOTCH_D = 0.55;        // selector notch diameter (state write feature)
MIN_WEB = 0.24;        // target minimum printed web at 0.4 mm nozzle

// --- cam bank geometry -------------------------------------------------------
BANK_R = 2.20;         // bank radius (fits under 5.08 column)
LAND_H = 0.90;         // cam land height
HUB_D = 1.20;
SHAFT_D = 1.00;        // printed shaft, D-shape flat optional

part = "assembled_2x4";

module finger(engaged = true) {
    difference() {
        union() {
            // rocker body
            translate([0, 0, FINGER_T / 2])
                cube([FINGER_L, FINGER_H, FINGER_T], center = true);
            // pivot boss
            rotate([90, 0, 0]) cylinder(d = PIVOT_D, h = FINGER_T, center = true);
            // toe that meets the cam land
            translate([FINGER_L / 2 - 0.3, -FINGER_H / 2 + 0.35, 0])
                cube([0.6, 0.7, FINGER_T], center = true);
        }
        // selector notch - present = this finger writes when the cam is at
        // its plane; absent = finger rides the land
        if (engaged)
            translate([FINGER_L / 2 - 0.3, -FINGER_H / 2 + 0.35, 0])
                cylinder(d = NOTCH_D, h = FINGER_T * 2, center = true);
    }
}

module cam_bank() {
    difference() {
        union() {
            cylinder(d = BANK_R * 2, h = LAND_H, center = true);
            // four raised lands, one per row, 90 deg apart
            for (i = [0:ROWS_PER_STATION - 1])
                rotate([0, 0, i * 360 / ROWS_PER_STATION])
                    translate([BANK_R * 0.55, 0, LAND_H / 2])
                        cube([BAND * 0.7, BANK_R * 0.9, 0.5], center = true);
        }
        // shaft bore
        cylinder(d = SHAFT_D, h = LAND_H * 3, center = true);
    }
}

module coupon_base() {
    // 2 cells x 4 rows footprint, open frame so fingers can be inspected
    difference() {
        cube([PITCH * 2, PITCH * 4, 1.20], center = true);
        for (x = [0, 1], y = [0:3])
            translate([(x - 0.5) * PITCH, (y - 1.5) * PITCH, 0.2])
                cube([FINGER_L + 0.3, BAND + 0.15, 1.2], center = true);
    }
}

module assembled_2x4() {
    coupon_base();
    // cam banks under each column
    for (x = [0, 1])
        translate([(x - 0.5) * PITCH, 0, -1.8]) rotate([90, 0, 0]) cam_bank();
    // four fingers per column, one per row
    for (x = [0, 1], y = [0:3])
        translate([(x - 0.5) * PITCH, (y - 1.5) * PITCH, 0.9])
            rotate([0, 0, 0]) finger((x + y) % 2 == 0);   // checkerboard
}

if (part == "finger") finger(true);
else if (part == "finger_blank") finger(false);
else if (part == "bank") cam_bank();
else if (part == "base") coupon_base();
else assembled_2x4();
