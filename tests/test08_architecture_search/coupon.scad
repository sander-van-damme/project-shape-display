// Generated dimensions come from params.json via analysis.py. Units mm.
// Purpose: inspect/print the hard-stop contact and guide coupon, NOT a complete product.
include <results/parameters.scad>
part = "section"; // section, assembly, rotor, follower, follower_guide, body_guide, lift_plate, collision
level = 2;
raised = false;
rotation = 0; // rotor rotation during raised interference checks
nx = 3; ny = 2;
$fn=60;
eps=0.01;
h = raised ? travel_mm+1 : level*travel_mm/(levels-1);
angle = raised ? rotation : -level*360/levels;

module sector(r, start, end, height) {
    if(height>0) linear_extrude(height)
        polygon(concat([[0,0]], [for(a=[start:1:end]) [r*cos(a),r*sin(a)]], [[r*cos(end),r*sin(end)]]));
}

module rotor() {
    translate([center_x_mm,0,0]) {
        cylinder(r=radius_mm,h=base_mm);
        translate([0,0,base_mm]) cylinder(r=core_radius_mm,h=travel_mm);
        for(k=[0:levels-1]) translate([0,0,base_mm])
            sector(radius_mm,k*360/levels-180/levels,k*360/levels+180/levels,k*travel_mm/(levels-1));
        // Bearing shaft and face-drive surface: no keyed angular engagement.
        translate([0,0,-14]) cylinder(r=0.55,h=14+eps);
        translate([0,0,-14]) cylinder(r=1.15,h=1);
        // Five detent valleys on wheel; compliant leaf is a separate experiment.
        translate([0,0,-10]) difference() {
            cylinder(r=1.65,h=1.5);
            for(a=[0:360/levels:359]) rotate([0,0,a])
                translate([1.65,0,-eps]) cylinder(r=0.25,h=1.5+2*eps);
        }
    }
}

module rotor_at() {
    translate([center_x_mm,0,0]) rotate([0,0,angle]) translate([-center_x_mm,0,0]) rotor();
}

module follower() {
    // Default solid improves gravity return; hollow variant quantifies the tradeoff.
    difference() {
        translate([-body_width_mm/2,-body_width_mm/2,body_bottom_mm])
            cube([body_width_mm,body_width_mm,body_length_mm]);
        if(body_hollow) translate([-body_width_mm/2+body_wall_mm,-body_width_mm/2+body_wall_mm,body_bottom_mm+body_floor_mm])
            cube([body_width_mm-2*body_wall_mm,body_width_mm-2*body_wall_mm,body_length_mm-body_floor_mm-body_roof_mm]);
        translate([body_relief_x_mm,-body_relief_half_width_mm,body_bottom_mm-eps])
            cube([3-body_relief_x_mm,2*body_relief_half_width_mm,body_relief_height_mm+eps]);
    }
    translate([stem_x_mm,-stem_width_mm/2,base_mm])
        cube([stem_thickness_mm,stem_width_mm,follower_length_mm+eps]);
    translate([toe_x_mm,-toe_width_mm/2,base_mm])
        cube([stem_x_mm+stem_thickness_mm-toe_x_mm,toe_width_mm,toe_thickness_mm]);
    translate([toe_x_mm,-bridge_width_mm/2,body_bottom_mm])
        cube([stem_x_mm+stem_thickness_mm-toe_x_mm,bridge_width_mm,bridge_thickness_mm]);
}

module follower_guide() {
    // Open inward slot passes the toe; lips capture wider stem at either side.
    // It must be tied to a rigid frame in a real cartridge.
    difference() {
        translate([guide_inner_x_mm,-1.3,4]) cube([2.50-guide_inner_x_mm,2.6,follower_guide_top_mm-4]);
        translate([stem_x_mm-guide_clearance_mm,-stem_width_mm/2-guide_clearance_mm,3])
            cube([stem_thickness_mm+2*guide_clearance_mm,stem_width_mm+2*guide_clearance_mm,follower_guide_top_mm-2]);
        translate([guide_inner_x_mm-eps,-guide_slot_half_width_mm,3])
            cube([stem_x_mm-guide_inner_x_mm+guide_clearance_mm+eps,2*guide_slot_half_width_mm,follower_guide_top_mm-2]);
    }
}

module body_guide() {
    for(z=[body_bottom_mm+body_length_mm-14,body_bottom_mm+body_length_mm-6]) difference() {
        translate([-pitch_mm/2,-pitch_mm/2,z]) cube([nx*pitch_mm,ny*pitch_mm,4]);
        for(x=[0:nx-1],y=[0:ny-1])
            translate([x*pitch_mm-body_width_mm/2-body_guide_clearance_mm,
                       y*pitch_mm-body_width_mm/2-body_guide_clearance_mm,z-eps])
            cube([body_width_mm+2*body_guide_clearance_mm,body_width_mm+2*body_guide_clearance_mm,4+2*eps]);
    }
}

module lift_plate() {
    difference() {
        translate([-pitch_mm/2,-pitch_mm/2,42+(raised?travel_mm+1:0)]) cube([nx*pitch_mm,ny*pitch_mm,2]);
        for(x=[0:nx-1],y=[0:ny-1])
            translate([x*pitch_mm+toe_x_mm-guide_clearance_mm,
                       y*pitch_mm-body_relief_half_width_mm,41])
            cube([2.65-toe_x_mm+guide_clearance_mm,2*body_relief_half_width_mm,45]);
    }
}

module scene() {
    color("#a9bdcb",0.5) body_guide();
    color("#67899a",0.7) lift_plate();
    for(x=[0:nx-1],y=[0:ny-1]) translate([x*pitch_mm,y*pitch_mm,0]) {
        color("#dda44b") rotor_at();
        color("#449d82") translate([0,0,h]) follower();
        color("#a3a7b0") follower_guide();
    }
}

// Intended horizontal support contacts are separated by eps for intersection testing.
module collision() {
    intersection() { rotor_at(); translate([0,0,h+eps]) follower(); }
    intersection() { rotor_at(); follower_guide(); }
    intersection() { translate([0,0,h]) follower(); follower_guide(); }
    intersection() { lift_plate(); follower_guide(); }
    intersection() { lift_plate(); translate([0,0,h+eps]) follower(); }
    intersection() { body_guide(); translate([0,0,h]) follower(); }
}

if(part=="rotor") rotor();
else if(part=="follower") follower();
else if(part=="follower_guide") follower_guide();
else if(part=="body_guide") body_guide();
else if(part=="lift_plate") lift_plate();
else if(part=="collision") collision();
else if(part=="assembly") scene();
else if(part=="section") intersection() {
    scene(); translate([-20,-0.05,-20]) cube([80,40,190]);
}
