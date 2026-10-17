// Dimensions mm. Two identical frame halves meet at Y=0. No threaded redesign.
// Reproduce with BOSL2 136e6367e65d52196a3ea51d03156f8b622c60fc.
include <../2026-10-15-compact-screw-fit/thread-kernel.scad>
part="half";

module frame_half() {
    difference() {
        union() {
            translate([-18,0,0]) cube([36,10,2]);
            for(x=[-15,12]) translate([x,0,2]) cube([3,6.5,42]);
            translate([-7,0,2]) cube([14,6.5,8.2]); // motor cradle
            translate([-15,0,20.2]) cube([30,3.5,3.5]); // thrust deck
            intersection() { translate([0,0,20.2]) cylinder(d=9,h=3.5);
                translate([-5,0,20]) cube([10,5,4]); }
            translate([-15,0,28.9]) cube([30,3.5,2.1]); // screw foot keeper
            translate([-5,0,36]) cube([10,4.5,8]); // square antirotation guide
            translate([-15,3.5,41]) cube([30,3,3]); // guide to uprights
        }
        translate([0,0,2]) cylinder(d=8.5,h=10);
        // Photo shows a front flange/ears but does not dimension their OD.
        // Clamp the cylindrical body, leave its upper 1 mm generously relieved.
        translate([0,0,9.2]) cylinder(d=11.5,h=1.1);
        // Radial clearance for terminals; wires leave through open side window.
        translate([-7,0,3]) cube([4,3.5,7.3]);
        translate([0,0,19.9]) cylinder(d=3.5,h=4.1);
        translate([0,0,28.8]) cylinder(d=4.2,h=2.4);
        translate([-2.4,-2.4,35.9]) cube([4.8,4.8,8.3]);
        // Shallow exterior tie channels: 2.5 mm-wide reusable cable ties.
        for(z=[6,21,38]) translate([-16,5.9,z]) cube([32,2,2.8]);
    }
}

// Operating pose: stem bottom Z15.2; journal 20.2..24.2;
// thrust face Z24.2; screw square foot Z26.2..28.6.
module drive_cup() {
    difference() {
        union() {
            translate([-6.5,-6.5,24.2]) cube([13,13,4.6]);
            translate([0,0,20.2]) cylinder(d=3,h=4.01);
            translate([0,0,15.2]) cylinder(d=2.4,h=5.01);
        }
        translate([-5.2,-5.2,26.2]) cube([10.4,10.4,3]);
    }
}

if(part=="half") {
    // Broad split face on bed. No hidden supports in bearing or guide.
    rotate([90,0,0]) frame_half();
}
if(part=="cup") {
    // Socket open toward bed; 10.4 mm roof bridge, stem upwards.
    translate([0,0,28.8]) rotate([180,0,0]) drive_cup();
}
if(part=="screw") {
    // Exact functional coupon geometry including its existing 10 mm square foot.
    union() {
        translate([-5,-5,0]) cube([10,10,2.4]);
        translate([0,0,2.39]) cylinder(d=1.4,h=.02);
        translate([0,0,2.4]) intersection() {
            compact_thread();
            union() { cylinder(d=3.3,h=15.4);
                translate([0,0,15.4]) cylinder(d1=3.3,d2=1.4,h=.6); }
        }
    }
}
if(part=="pin") {
    // Same .175 relief / 6 mm working thread as physically successful coupon.
    // Its external .24 mm print foot remains below the guide throughout travel.
    union() {
        compact_pin_body(relief=.175);
        difference() {
            translate([-6,-6,0]) cube([12,12,.24]);
            translate([0,0,-3]) compact_thread(d=3.55,l=6);
        }
    }
}
