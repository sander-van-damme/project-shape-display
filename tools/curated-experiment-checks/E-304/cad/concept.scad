// E-304 dimensioned PRINCIPLE ENVELOPES, mm. Not a printable clutch release.
// Actual force-test manufacturing CAD is in owner-print-tests/.../cad/rig.py.
// Gear and E-295 thread are envelopes; no claim of working tooth/thread geometry.
$fn=96;
stroke=0.6; engaged=true; exploded=false; section=true;
q=engaged?0:-stroke; ex=exploded?4:0;
alpha=35; ri=4; ro=5; cone_h=(ro-ri)/tan(alpha);
module ring(od,id,h){difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
module dd(d=3.2,af=2.7,h=10){intersection(){cylinder(d=d,h=h);translate([-af/2,-d/2,0])cube([af,d,h]);}}
module assembly(){
 // Stationary winding and two-piece nonmagnetic bobbin.
 color("orange")translate([0,0,-3.6-ex])ring(7.32,4.8,3.6);
 color("gray")translate([0,0,-4.4-ex])ring(8.4,4,.8);
 color("gray")translate([0,0,-3.6-ex])ring(4.8,4,4.4);
 color("gray")translate([0,0,-ex])ring(8.4,4.9,.8);
 // PM N up; magnet on screw-side sliding carrier, not on terrain load path.
 color("crimson")translate([0,0,-.4+q+ex])cylinder(d=3,h=1);
 color("royalblue")translate([0,0,.6+q+ex])cylinder(d=3,h=1);
 color("gold")translate([0,0,q+ex])difference(){
  union(){translate([0,0,1.6])cylinder(d=3.6,h=2.4);
   translate([0,0,3.4])cylinder(r=5,h=.6);
   translate([0,0,4])cylinder(r1=5,r2=4,h=cone_h);
   translate([0,0,4])cylinder(d=3.8,h=5);}
  translate([0,0,2.4])dd(3.4,2.9,10);
 }
 // Resident output shaft and thrust collar. Thread above z22 is ENVELOPE.
 color("steelblue")translate([0,0,2*ex])union(){
  translate([0,0,3.2])dd(h=12.8);
  translate([0,0,16])cylinder(d=3.2,h=6.1);
  translate([0,0,19])cylinder(d=6,h=1);
  translate([0,0,22])cylinder(d=3.2,h=16);
 }
 // Input socket and 24T module0.5 spur gear envelope (OD13 / PD12).
 color("seagreen")translate([0,0,ex/2])difference(){
  union(){translate([0,0,3.8])cylinder(d=10.8,h=2.2);
   translate([0,0,6])cylinder(d=10,h=6);
   translate([0,0,8])cylinder(d=13,h=2);}
  translate([0,0,3.79])cylinder(r1=5.147,r2=4,h=cone_h+.21);
  translate([0,0,4])cylinder(d=6,h=9);
 }
 // Fixed lower OFF stop, integrated into frame. Collar underside at z2.8 OFF.
 color([.5,.5,.5,.35])translate([0,0,2.5])ring(14,3.8,.3);
 // Four corner webs connect the split frame plates; gear engages through side window.
 for(x=[-6,6])for(y=[-6,6])color([.5,.5,.5,.2])translate([x-1,y-1,2.5])cube([2,2,43.5]);
 for(z=[32,42])color([.5,.5,.5,.35])translate([-7,-7,z])difference(){cube([14,14,2]);translate([4.6,4.6,-.1])cube([4.8,4.8,2.2]);}
 // Four counted thrust washers and frame journal/support plates.
 for(z=[7.7,10])color("silver")translate([0,0,z])ring(13,10.2,.3);
 for(z=[18.5,20.1])color("silver")translate([0,0,z+2*ex])ring(6.5,3.4,.5);
 for(z=[6,10.3])color([.5,.5,.5,.35])translate([0,0,z])ring(14,10.3,1.7);
 for(z=[17,20.6])color([.5,.5,.5,.35])translate([0,0,z+2*ex])ring(14,3.4,1.5);
 // Square pin/guide envelopes, NOT full E-295 screw/pin meshes.
 color([.7,.7,.85,.35])translate([-2.2,-2.2,28+2*ex])difference(){cube([4.4,4.4,18]);translate([2.2,2.2,-.1])cylinder(d=3.55,h=19);}
}
if(section)difference(){assembly();translate([0,-30,-20])cube([30,60,100]);}else assembly();
