// E-280 release witness, NOT selected hardware or print handoff.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64;
$slop=0;
angle=90;
part="finished";
module shank() {
    trapezoidal_threaded_rod(d=3.2,l=64,pitch=3,thread_depth=.9,
        thread_angle=angle,starts=1,left_handed=false,bevel=false,
        blunt_start=false,anchor=BOT);
}
module outer() {
    union() {
        shank();
        translate([0,0,-4]) cylinder(d=2.8,h=4.01);
        translate([0,0,-10]) cylinder(d=4.4,h=6); // collar -6..-4, driver -10..-6
        translate([0,0,63.99]) cylinder(d=1.4,h=4.01);
    }
}
module socket() {translate([0,0,-10.01]) cylinder(d=2/cos(30),h=2.01,$fn=6);}
if(part=="finished") difference(){outer();socket();}
if(part=="outer") outer();
if(part=="shank") shank();
