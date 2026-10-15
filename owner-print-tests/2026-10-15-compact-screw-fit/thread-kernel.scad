// Shared E-295 thread geometry, dimensions in millimetres.
// BOSL2 pinned to 136e6367e65d52196a3ea51d03156f8b622c60fc.
// Same paired 90-degree profile as the physically tried E-281 / short-thread-fit.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64;
$slop=0;

module compact_thread(d=3.2,l=16) {
    trapezoidal_threaded_rod(d=d,l=l,pitch=3,thread_depth=.9,
        thread_angle=90,starts=1,left_handed=false,bevel=false,
        blunt_start=false,anchor=BOT);
}

// Phase at Z=0 is the same for screw and female cutter. Passing a diameter
// increased by 2*relief gives CAD radial relief; no BOSL2 internal/slop mode.
module compact_pin_body(relief=.175,height=18,engagement=6) {
    difference() {
        translate([-2.2,-2.2,0]) cube([4.4,4.4,height]);
        translate([0,0,-3]) compact_thread(d=3.2+2*relief,l=engagement+3.01);
        // The 0.01 mm overlap avoids a coincident CSG plane. The actual
        // supported threaded length is 6 mm; cavity fits the 3.2 mm screw.
        translate([-1.76,-1.76,engagement]) cube([3.52,3.52,height]);
    }
}
