// Manufacturing comparison, not an owner print or qualified mating pair.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64;
$slop=0;
angle=30;
part="nut";
module paired_thread(d,cutting=false) {
    translate([0,0,cutting ? -3 : 0])
    trapezoidal_threaded_rod(d=d,l=cutting ? 69 : 64,pitch=3,
        thread_depth=.9,thread_angle=angle,starts=1,left_handed=false,
        bevel=false,blunt_start=false,anchor=BOT);
}
if(part=="nut") difference() {
    translate([-5.15,-5.15,0]) cube([10.3,10.3,10]);
    paired_thread(3.5,true);
}
if(part=="male") paired_thread(3.2);
