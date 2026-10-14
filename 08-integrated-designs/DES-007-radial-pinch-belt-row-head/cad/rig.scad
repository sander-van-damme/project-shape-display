// DES-007, mm. Source for an unqualified 2x4 radial belt bench rig.
// BOSL2 pinned at 136e6367e65d52196a3ea51d03156f8b622c60fc.
include <BOSL2/std.scad>
include <BOSL2/threading.scad>
$fn=64; $slop=0;
part="assembly";
row=0;
q=3;
p=6.35;
body=5.0; guide=5.30;
frame_w=43.05; frame_d=32;
xs=[0,p,2*p,3*p]; ys=[0,p];
// Six common M3 tie bolts outside the pin/head travel.
posts=[[-9,-7],[-9,17],[-9,3.175],[28.05,-7],[28.05,17],[28.05,3.175]];
module thread(d,l) {
 trapezoidal_threaded_rod(d=d,l=l,pitch=3,thread_depth=.9,
 thread_angle=90,starts=1,left_handed=false,bevel=false,blunt_start=false,anchor=BOT);
}
module plate(t=3,kind="journal") {
 difference(){
  translate([-12,-11,0])cube([frame_w,frame_d,t]);
  for(a=posts)translate([a[0],a[1],-.1])cylinder(d=3.4,h=t+.2);
  for(x=xs,y=ys)translate([x,y,-.1])
   if(kind=="guide")translate([-guide/2,-guide/2,0])cube([guide,guide,t+.2]);
   else cylinder(d=kind=="keeper"?3.6:2.6,h=t+.2);
 }
}
module upper_piece(r=0){
 intersection(){plate(3);translate([-15,r==0?-12:(r==1?.10:p+.10),-.1])
 cube([50,r==0?11.9:(r==1?p-.2:16),3.2]);}
}
module spacer(h=10){difference(){cylinder(d=6,h=h);translate([0,0,-.1])cylinder(d=3.4,h=h+.2);}}
module screw(r=0){
 // Radial journal, drive rim and thrust collar are integral; no fitted coupler.
 union(){
  translate([0,0,r==0?-4:-10])cylinder(d=2.4,h=r==0?22.01:28.01);
  translate([0,0,r==0?-4:-10])cylinder(d=5,h=3);
  translate([0,0,18])cylinder(d=5,h=2);
  translate([0,0,20])thread(3.2,20);
 }
}
module pin(){
 difference(){
  translate([-body/2,-body/2,0])cube([body,body,25]);
  translate([0,0,-3])thread(3.5,16); // nut material only first 10 mm
  translate([0,0,10])cylinder(d=3.8,h=14); // closed 1 mm top
 }
}
module roof(){
 // Slots preserve visibility; two lips catch each pin's top edges at upper stop.
 difference(){
  plate(2,"guide");
  for(x=xs,y=ys)translate([x-1.8,y-1.8,-.1])cube([3.6,3.6,2.2]);
 }
 // bridge the larger guide aperture with two narrow positive stop lips
 for(x=xs,y=ys,s=[-1,1])translate([x-2.9,y+s*2.25-.25,0])cube([5.8,.5,2]);
}
module shoe_base(){
 difference(){union(){
 translate([-.65,-8,0])cube([5.3,8,3]);
 translate([1,-6.8,2.8])cube([2,1.6,7.2]); // manual return tab
 translate([3.175,0,2.8])cylinder(d=2,h=5.2);
 }
 translate([3.175,0,1])cylinder(d=1.0,h=7.2);
 }
}
module shoe_tip(){
 difference(){union(){
 translate([2.375,-.8,17.6])cube([1.6,1.6,2.2]);
 hull(){
  translate([1.0,.8,17.6])cube([.3,.5,2.2]);
  translate([2.375,.2,17.6])cube([.3,.6,2.2]);
 }
 translate([-1.2,.8,17.6])cube([2.4,.5,5.4]);
 }
 translate([3.175,0,17.5])cylinder(d=1.0,h=2.4);
 }
}
module shoe(){
 shoe_base();shoe_tip();
 translate([3.175,0,1])cylinder(d=.8,h=18.8); // STEEL stock, never print as PLA
}
module head(){
 // Fixed head mounted at Z=-25; shoe floor at Z=-24.
 difference(){
  translate([-5,-16,0])cube([31.05,15,4.2]);
  for(a=posts)translate([a[0],a[1],-.1])cylinder(d=6.6,h=5);
  for(x=xs)translate([x-.8,-14.5,1])cube([5.6,10.7,3.3]);
  for(x=xs)translate([x+2.675,-4.2,1.9])cube([1.0,.7,2.0]);
  for(x=xs)translate([x+2.0,-4.1,3.7])cube([2.4,1.3,1]);
  for(x=xs)translate([x+2,-16.1,2.5])rotate([-90,0,0])cylinder(d=2.5,h=3);
  for(x=[-p/2,p/2,1.5*p,2.5*p,3.5*p])translate([x,-2.3,-.1])cylinder(d=1.1,h=4.5);
 }
 // Five 1 mm steel guide wires; holes pass through the front wall.
 // Wires project above the print; no fragile printed upright separators.
 // Two mounting ears; bolted to independent base, not miniature-bearing guides.
 for(x=[-5,26.05])translate([x,-18,0])difference(){
  cylinder(d=8,h=4.2);translate([0,0,-.1])cylinder(d=3.4,h=5.2);
 }
}
module head_cover(){
 difference(){translate([-9,-22,0])cube([39.05,15.5,1.6]);
 for(a=posts)translate([a[0],a[1],-.1])cylinder(d=6.6,h=2);
 for(x=[-5,26.05])translate([x,-18,-.1])cylinder(d=3.4,h=1.8);
 for(x=xs)translate([x+1.8,-8,-.1])cube([2.8,2,1.8]);
 for(x=xs)translate([x+.8,-11.5,-.1])cube([2.4,2.6,1.8]);}
}
module foot(){
 difference(){translate([-15,-22,0])cube([49.05,45,3]);
 for(a=posts)translate([a[0],a[1],-.1])cylinder(d=3.4,h=3.2);
 for(x=[-5,26.05])translate([x,-18,-.1])cylinder(d=3.4,h=3.2);
 }
}
module belt_strip(){cube([180,.2,3]);}
module assembly(){
 color("silver")translate([0,0,-30])foot();
 for(a=posts)translate([a[0],a[1],-27])spacer(27);
 for(r=[0,1,2])color("lightgray")upper_piece(r);
 for(r=[0,1,2])color("lightgray")translate([0,0,15])upper_piece(r);
 color("gray")translate([0,0,20.2])plate(1.6,"keeper");
 color("lightgray")translate([0,0,34])plate(2,"guide");
 color("lightgray")translate([0,0,44])plate(2,"guide");
 color("lightgray")translate([0,0,53.2])roof();
 for(a=posts){
  translate([a[0],a[1],3])spacer(12);
  translate([a[0],a[1],18])spacer(2.2);
  translate([a[0],a[1],21.8])spacer(12.2);
  translate([a[0],a[1],36])spacer(8);
  translate([a[0],a[1],46])spacer(7.2);
 }
 for(x=xs,r=[0,1]){
  color("orange")translate([x,r*p,0])rotate([0,0,120*(1-q)])screw(r);
  color("lightblue")translate([x,r*p,22+q])pin();
 }
 color("green")translate([0,0,-25])head();
 color("green")translate([0,0,-20.8])head_cover();
 for(x=xs)color("purple")translate([x,-4.4,-24])shoe();
 for(x=[-p/2,p/2,1.5*p,2.5*p,3.5*p])
  color("silver")translate([x,-2.3,-24.8])cylinder(d=1,h=23.8);
 color("black")translate([-40,-3.0,-4])belt_strip();
}
if(part=="assembly")assembly();
if(part=="screw")screw(row);
if(part=="pin")pin();
if(part=="journal")plate(3);
if(part=="keeper")plate(1.6,"keeper");
if(part=="guide")plate(2,"guide");
if(part=="roof")roof();
if(part=="spacer")spacer(q);
if(part=="shoe")rotate([90,0,0])shoe();
if(part=="head")head();
if(part=="foot")foot();
if(part=="belt")rotate([90,0,0])belt_strip();

if(part=="head_cover")head_cover();

if(part=="upper_piece")upper_piece(row);

// Sacrificial stabilizers contact only outer collar, never thread or journal.
module supported_screw(r=0){
 screw(r);
 for(sign=[-1,1]){
  translate([sign*6-2,-3,r==0?-4:-10])cube([4,6,1]);
  translate([sign*6-1,-1,r==0?-4:-10])cube([2,2,r==0?23.2:29.2]);
  translate([sign==1?2.2:-6.8,-.3,18.8])cube([4.6,.6,.4]);
 }
}
if(part=="supported_screw")supported_screw(row);

if(part=="shoe_base")shoe_base();
if(part=="shoe_tip")rotate([90,0,0])shoe_tip();

// Optional load probe, printed disk-down; invert in use through the roof opening.
module load_probe(){cylinder(d=10,h=2);translate([0,0,2])cylinder(d=3,h=12);}
if(part=="load_probe")load_probe();
