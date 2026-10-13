// E-263, one S40 article. Millimetres. See canonical result for limits.
// BOSL2 commit 136e6367e65d52196a3ea51d03156f8b622c60fc; no implicit slop.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64;
$slop=0;
part="assembly";
q=22;
second_land=true;
phase_sign=-1;

module block(x0,x1,y0,y1,z0,z1) {
    translate([x0,y0,z0]) cube([x1-x0,y1-y0,z1-z0]);
}
module thread(d, cutting=false) {
    translate([0,0,cutting ? -3 : 0])
    trapezoidal_threaded_rod(d=d,l=cutting ? 60 : 54,pitch=3,thread_depth=.9,
        thread_angle=30,starts=1,left_handed=false,bevel=false,
        blunt_start=false,anchor=BOT);
}
module pin() {
    difference() {
        union() {
            block(-2.2,2.2,-2.2,2.2,0,86);
            // Laboratory stop shoulders; not an array cap design.
            block(-4,4,-4,4,0,2);
            block(-14,14,-14,14,84,86);
        }
        // Identical periodic helical phase to male, with explicit radial relief.
        intersection() { thread(3.5,true); block(-5,5,-5,5,-.1,10.01); }
        block(-1.76,1.76,-1.76,1.76,10,84);
    }
}
module screw() {
    union() {
        thread(3.2);
        translate([0,0,-22]) cylinder(d=3.2,h=22.02);
        translate([0,0,-26]) cylinder(d=24,h=4.02);
    }
}
module frame_stock() {
    union() {
        block(-35,35,-25,25,-30.2,-26.2);
        for(s=[-1,1]) translate([s*24,0,0])
            block(-4,4,-6,6,-26.21,86);
        block(-20.01,20.01,-6,6,-21.8,-19.8);
        block(-20.01,20.01,-6,6,-4,-2);
        block(-20.01,20.01,-6,6,44,46);
        block(-20.01,20.01,-6,6,84,86);
    }
}
module frame_cut() {
    difference() {
        frame_stock();
        translate([0,0,-22]) cylinder(d=5,h=3);
        translate([0,0,-4.1]) cylinder(d=3.6,h=2.2);
        for(z=[44,84]) block(-2.4,2.4,-2.4,2.4,z-.1,z+2.1);
        // Slots for the removable second root land, not an added thrust seat.
        block(-22.2,22.2,-10,10,-18.2,-15.8);
        // Two loose shared-fixture registration keys; no fine alignment screw.
        for(p=[[-24,10],[24,70]])
            translate([p[0],0,p[1]]) block(-1.8,1.8,-2.2,2.2,-1.8,1.8);
    }
}
module half_frame(side) {
    intersection() {
        frame_cut();
        if(side==1) block(-40,40,0,26,-31,87);
        else block(-40,40,-26,0,-31,87);
    }
}
module half_land(side) {
    difference() {
        if(side==1) block(-22,22,0,10,-18,-16);
        else block(-22,22,-10,0,-18,-16);
        translate([0,0,-18.1]) cylinder(d=3.6,h=2.2);
    }
}
module key() { cube([3.2,4,3.2],center=true); }
module assembly() {
    color("lightgray") frame_cut();
    color("gold") rotate([0,0,phase_sign*360*q/3]) screw();
    color("teal") translate([0,0,q]) pin();
    if(second_land) color("orange") { half_land(1);half_land(-1); }
}
if(part=="assembly") assembly();
if(part=="pin") translate([0,0,86]) rotate([180,0,0]) pin();
if(part=="screw") translate([0,0,26]) screw();
// Split faces on the bed. The small recesses bridge <=4.8 mm.
if(part=="frame_front") translate([35,86,0]) rotate([90,0,0]) half_frame(1);
if(part=="frame_back") translate([35,30.2,0]) rotate([-90,0,0]) half_frame(-1);
if(part=="land_front") translate([22,0,18]) half_land(1);
if(part=="land_back") translate([22,10,18]) half_land(-1);
if(part=="key") translate([1.6,2,1.6]) key();
// World-coordinate verification exports (not handed to owner).
if(part=="world_frame") frame_cut();
if(part=="world_pin") translate([0,0,q]) pin();
if(part=="world_screw") rotate([0,0,phase_sign*360*q/3]) screw();
if(part=="world_land") {half_land(1);half_land(-1);}
if(part=="thread_male") thread(3.2);
if(part=="thread_cutter") thread(3.5,true);
