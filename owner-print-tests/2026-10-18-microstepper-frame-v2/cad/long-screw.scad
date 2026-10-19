// E-302 revision 3. Same E-301 thread kernel and square drive foot, longer shaft.
// BOSL2 136e6367e65d52196a3ea51d03156f8b622c60fc; millimetres.
include <../../2026-10-15-compact-screw-fit/thread-kernel.scad>
thread_length=48;
module long_screw(){
 union(){
  translate([-5,-5,0])cube([10,10,2.4]);
  translate([0,0,2.39])cylinder(d=1.4,h=.02);
  translate([0,0,2.4])intersection(){
   compact_thread(l=thread_length);
   union(){
    cylinder(d=3.3,h=thread_length-.6);
    translate([0,0,thread_length-.6])cylinder(d1=3.3,d2=1.4,h=.6);
   }
  }
 }
}
long_screw();
