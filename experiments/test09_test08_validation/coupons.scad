// Test09 independent process/detent coupons. Units mm; no external libraries.
// Exported geometry is not a printer or material qualification.
include <results/coupon_parameters.scad>
part="fit_tile";
clearance=0.10; // PER SIDE, change with -D after comparing process copies
body=4.68;
levels=cam_levels;
thickness=detent_thickness_mm;
length=detent_length_mm;
angle=0;
$fn=80;

module fit_tile() {
    difference() {
        translate([-5,-5,0]) cube([2*cell_pitch_mm+10,cell_pitch_mm+10,4]);
        for(x=[0:2],y=[0:1]) translate([x*cell_pitch_mm-body/2-clearance,y*cell_pitch_mm-body/2-clearance,-0.01])
            cube([body+2*clearance,body+2*clearance,4.02]);
    }
}
module fit_slider() { cube([body,body,80.2]); }
module walls() {
    cube([42,18,2]);
    for(i=[0:4]) translate([3+i*8,2,2]) cube([[.2,.3,.4,.6,.8][i],14,10]);
}
module bushings() {
    difference() {
        cube([60,12,5]);
        for(i=[0:4]) {
            translate([6+12*i,4,-.01]) cylinder(d=1.1+2*[.05,.1,.15,.2,.25][i],h=5.02);
            translate([6+12*i,9,-.01]) cube([.7+2*[.05,.1,.15,.2,.25][i],1.8+2*[.05,.1,.15,.2,.25][i],5.02],center=false);
        }
    }
}
module gauge_shaft() { cylinder(d=1.1,h=20); }
module bearing_half() {
    // One half of a THREE-journal row. Mirror in Y for the other half;
    // two rows tile at true pitch. Split permits captive rotor assembly.
    difference() {
        translate([-5,0,0]) cube([2*cell_pitch_mm+10,cell_pitch_mm/2,2]);
        for(x=[0:2]) translate([x*cell_pitch_mm-.3,0,-.01])
            cylinder(d=1.1+2*clearance,h=2.02);
    }
}
function radius(a)=detent_outer_radius_mm-detent_depth_mm/2*(1+cos(levels*a));
module wheel() {
    difference() {
        linear_extrude(1.5) polygon([for(a=[0:1:359]) [radius(a)*cos(a),radius(a)*sin(a)]]);
        translate([0,0,-.01]) cylinder(d=1.3,h=1.52);
    }
}
module home_wheel() {
    wheel();
    // Lug ABOVE the leaf running plane. Bench stop position sets zero datum.
    translate([-2.2,-.3,1.4]) cube([1,.6,.9]);
}
module motor_cradle() {
    // Bench sleeve for an 8mm body; clamp with a strap through the two slots.
    difference() {
        translate([-9,-7,0]) cube([18,14,6]);
        translate([0,0,-.01]) cylinder(d=8.4,h=6.02);
        for(x=[-6,6]) translate([x,-5,-.01]) cube([1.5,10,6.02]);
    }
}
module home_stop() {
    difference() {
        cube([10,6,4]);
        translate([3,3,-.01]) cylinder(d=3.3,h=4.02);
    }
    translate([9,2,3.9]) cube([1,2,3]);
}
// Flat bench leaf: free end at y=0, clamp at y=length. Same cross-section
// as proposed vertical packed leaf, but this bench assembly DOES NOT tile.
// Finite nib profile and friction must be measured, not inferred from r(theta).
module leaf() {
    translate([1.8,0,0]) cube([thickness,length+1,detent_width_mm]);
    hull() {
        translate([detent_outer_radius_mm-detent_depth_mm-detent_preload_mm+.2,.2,0]) cylinder(r=.2,h=detent_width_mm);
        translate([1.8,0,0]) cube([thickness,.4,detent_width_mm]);
    }
    translate([.5,length,0]) difference() {
        cube([5,5,2]);
        translate([2.5,2.5,-.01]) cylinder(d=2.3,h=2.02);
    }
}
module bench_base() {
    difference() {
        translate([-8,-7,0]) cube([20,28,3]);
        translate([0,0,-.01]) cylinder(d=1.3,h=3.02);
        translate([3,12.5,-.01]) cylinder(d=2.3,h=3.02);
        for(x=[-5,9]) translate([x,-4,-.01]) cylinder(d=3.3,h=3.02);
    }
}
// Split journal block, two halves clamp externally; bench-only M3 ears.
module journal_half() {
    difference() {
        translate([0,-5,0]) cube([5,10,4]);
        translate([0,0,-.01]) cylinder(d=1.1+2*clearance,h=4.02);
        for(y=[-3,3]) translate([2.5,y,-.01]) cylinder(d=1.8,h=4.02);
    }
}
module collar_half() {
    difference() {
        intersection() {cylinder(d=3,h=1.5);translate([0,-2,-.01])cube([2,4,1.52]);}
        translate([0,0,-.01]) cylinder(d=1.1,h=1.52);
    }
}
// Face pad holder bore is deliberately a parameter, default gauge shaft only.
shaft_d=1.1;
module coupler() {
    difference() {
        cylinder(d=4,h=5);
        translate([0,0,-.01]) cylinder(d=shaft_d+2*clearance,h=4);
        translate([0,0,4.6]) cylinder(d=2.4,h=.41);
    }
}
module beam_half() {
    // 203.2 mm sample, assembled pair tests a midspan bolted splice.
    difference() {
        cube([203.2,beam_width_mm,beam_height_mm]);
        translate([-.01,beam_wall_mm,beam_wall_mm]) cube([203.22,beam_width_mm-2*beam_wall_mm,beam_height_mm-2*beam_wall_mm]);
        for(x=[10,25,178.2,193.2]) translate([x,beam_width_mm/2,-.01]) cylinder(d=3.3,h=beam_height_mm+.02);
    }
}
module splice() {
    difference() {
        cube([60,20,3]);
        for(x=[5,20,40,55]) translate([x,10,-.01]) cylinder(d=3.3,h=3.02);
    }
}
if(part=="fit_tile") fit_tile();
else if(part=="slider") fit_slider();
else if(part=="walls") walls();
else if(part=="bushings") bushings();
else if(part=="shaft") gauge_shaft();
else if(part=="bearing_half") bearing_half();
else if(part=="wheel") wheel();
else if(part=="home_wheel") home_wheel();
else if(part=="motor_cradle") motor_cradle();
else if(part=="home_stop") home_stop();
else if(part=="leaf") leaf();
else if(part=="bench_base") bench_base();
else if(part=="journal_half") journal_half();
else if(part=="collar_half") collar_half();
else if(part=="coupler") coupler();
else if(part=="beam_half") beam_half();
else if(part=="splice") splice();
else if(part=="detent_scene") {
    bench_base();
    translate([0,0,3.2]) rotate([0,0,angle]) wheel();
    translate([0,0,3.45]) leaf();
}
else assert(false,"unknown part");
