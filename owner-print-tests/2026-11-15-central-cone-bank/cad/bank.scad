// DES-010. mm. Physical fits unknown. z coordinates are assembly datums.
// key_open and guide_open are fit parameters. Structural coordinates are explicit:
// changing pitch/stack requires revising dependent mounts and rerunning all checks.
part="bank";
$fn=64;
pitch=5.08;
row=0;
key_open=2.3;
guide_open=4.7;

module hole(d,h=100){
translate([0,0,-.01])cylinder(d=d,h=h+.02);
}

module gridholes(d,h=100){
for(x=[0,pitch])for(y=[0,pitch])translate([x,y,0])hole(d,h);
}

module bolts(h=100){
for(x=[-8,13.08])for(y=[-5,10.08])translate([x,y,0])hole(3.4,h);
}

module plate(z,h,bore){
difference(){
translate([-12,-9,z])cube([29.08,23.08,h]);
translate([0,0,z])gridholes(bore,h);
translate([0,0,z])bolts(h);
}
}

module wideplate(){
difference(){
translate([-48,-9,31.35])cube([101,23.08,2.6]);
translate([0,0,31.35])gridholes(2.3,2.6);
translate([0,0,31.35])bolts(2.6);
for(x=[-42,47])for(y=[-5,10.08])translate([x,y,31.35])hole(3.4,2.6);
}
}

module lower(i){
intersection(){
wideplate();
translate([-55,i==0?-12:(i==1?0:5.08),28])cube([120,i==0?12:(i==1?5.08:12),8]);
}
}

module upper(){
plate(35.05,1.6,3.5);
}

module guide(open=guide_open){
difference(){
translate([-12,-9,0])cube([29.08,23.08,2]);
for(x=[0,pitch])for(y=[0,pitch])translate([x-open/2,y-open/2,-.01])cube([open,open,2.02]);
bolts(2);
}
}

module spacer(h=1.1){
difference(){
cylinder(d=6,h=h);
hole(3.4,h);
}
}

module cupbase(){
difference(){
union(){
cylinder(d=4.6,h=2);
translate([0,0,2])cylinder(d=2,h=3);
translate([0,0,5])cylinder(d=4.4,h=1);
translate([0,0,6])cylinder(d=3.2,h=2.2);
}
translate([0,0,-.01])cylinder(r1=1.906,r2=1.1,h=1.396);
}
}

module male(){
union(){
translate([-1,-1,-18])cube([2,2,18.1]);
translate([0,0,-2.6])cylinder(d=4.2,h=.8);
cylinder(r1=1.9,r2=1.1,h=1.386);
}
}

module rotor(){
difference(){
union(){
translate([0,0,12])cylinder(d=4,h=8);
translate([0,0,14])cylinder(d=4.6,h=4);
translate([0,0,14])cylinder(d=4.9,h=.5);
translate([0,0,17.5])cylinder(d=4.9,h=.5);
}
translate([-key_open/2,-key_open/2,11.9])cube([key_open,key_open,8.2]);
}
}

module motorpulley(){
difference(){
union(){
cylinder(d=11.6,h=.6);
cylinder(d=10.6,h=4);
translate([0,0,3.4])cylinder(d=11.6,h=.6);
translate([0,0,-4])cylinder(d=10,h=4.1);
}
translate([0,0,-4.1])cylinder(d=5.15,h=8.2);
translate([0,-6,-2])rotate([-90,0,0])cylinder(d=2.5,h=12);
}
}

module bank(){
difference(){
union(){
translate([-33,-60,3])cube([71,81,6]);
translate([38,17,6])cube([7,4,3]);
translate([.08,20,3])cube([10,9,6]);
for(z=[11.8])translate([-4,-4,z])cube([13.08,8,2]);
for(x=[-6.8,8.88])translate([x,-4,9])cube([3,8,9.2]);
for(s=[-1,1])translate([s<0?1.58:-3.5,s<0?22:15,9])cube([7,6,5]);
}
for(mx=[-23.46,28.54])for(my=[-52,-18])translate([mx,my,3.9])cylinder(d=2.5,h=5.2);
for(x=[-5.3,10.38])translate([x,0,13])cylinder(d=1.6,h=5.3);
translate([41.5,19,5.9])cylinder(d=3.2,h=3.2);
for(x=[-28,33])translate([x,-61,6])rotate([-90,0,0])cylinder(d=3.4,h=83);
translate([-19.2,-60.7,2.9])cube([43.4,47.4,6.2]);
hull(){
for(my=[-35,-39])translate([2.54,my,8.9])cylinder(d=23,h=3.2);
}
;
for(x=[-15.5,15.5])for(y=[-15.5,15.5])hull(){
for(dy=[-4,0])translate([2.54+x,-35+y+dy,8.9])cylinder(d=3.5,h=3.2);
}
for(x=[0,5.08])translate([x,0,2.9])cylinder(d=3.3,h=6.2);
for(x=[0,5.08])for(z=[11.7,18.1])translate([x,0,z])cylinder(d=4.3,h=2.2);
for(s=[-1,1])translate([s<0?5.08:0,s<0?25:18,2.9])cylinder(d=6.4,h=6.2);
for(s=[-1,1])translate([s<0?5.08:0,s<0?25:18,8.9])cylinder(d=3.4,h=5.3);
for(s=[-1,1])translate([s<0?5.08:0,s<0?25:18,11.5])cylinder(d=6.6,h=2.6,$fn=6);
}
}

// yoke fork: collar captured for positive manual pull-down. Print on its side.
module yoke(reach=18){
difference(){
union(){
translate([-2.45,-2.45,-4.7])cube([4.9,reach+4.9,2]);
translate([-2.45,-2.45,-1.7])cube([4.9,7.4,.8]);
translate([-2.45,3,-4.7])cube([4.9,1.9,3.8]);
translate([-2.45,5,-4.7])cube([4.9,reach-2.55,3]);
}
translate([0,0,-5])cylinder(d=3.2,h=5);
translate([-1.6,-3,-5])cube([3.2,3,5]);
translate([0,reach,-4.8])cylinder(d=3.5,h=3.2);
}
}

module long_yoke(){
difference(){
yoke(25);
translate([-5.08,18,-5])cylinder(d=8,h=6);
}
}

module endblock(){
difference(){
cube([78,8,14]);
for(x=[8,69])translate([x,-.1,6])rotate([-90,0,0])cylinder(d=3.2,h=8.2);
for(x=[4,74])translate([x,4,-.1])cylinder(d=3.5,h=14.2);
}
}

module framefoot(){
difference(){
cube([12,12,29.35]);
translate([6,6,-.1])cylinder(d=3.4,h=29.6);
}
}

module springseat(){
difference(){
cylinder(d=5,h=1.2);
translate([0,0,.6])cylinder(d=3.8,h=.7);
hole(3.4,1.2);
}
}

if(part=="bank")bank();

if(part=="lower0")translate([0,0,-31.35])lower(0);

if(part=="lower1")translate([0,0,-31.35])lower(1);

if(part=="lower2")translate([0,0,-31.35])lower(2);

if(part=="upper")translate([0,0,-35.05])upper();

if(part=="guide")guide();

if(part=="cupbase")cupbase();

if(part=="male")translate([0,0,18])male();

if(part=="rotor")translate([0,0,-12])rotor();

if(part=="motorpulley")translate([0,0,4])motorpulley();

if(part=="yoke")translate([0,0,2.45])rotate([0,90,0])yoke();

if(part=="spacer")spacer();

if(part=="endblock")endblock();

if(part=="foot")framefoot();

if(part=="springseat")springseat();

if(part=="assembly"){

color("silver")bank();
color("silver")motorplate();
color("silver")translate([0,0,18.2])import("../components/cap.stl");
for(x=[0,pitch]){
translate([x,0,0])rotor();
translate([x,0,29])male();
translate([x,0,29])if(x>0)long_yoke();
else yoke(18);
}

color("gray")translate([2.54,-35,14])motorpulley();
for(i=[0:2])lower(i);
upper();
for(z=[50,66])translate([0,0,z])guide();
for(x=[0,pitch])for(y=[0,pitch])translate([x,y,29])import("../components/screw.stl");
for(x=[0,pitch])for(y=[0,pitch])color("orange")translate([x,y,40.2])import("../components/pin.stl");

for(cx=[-42,47]){
for(cy=[-5,10.08])color("slategray")translate([cx-6,cy-6,0])framefoot();
for(sz=[29.35,33.95])color("slategray")translate([cx,0,sz])import("../components/strap.stl");
}

for(ey=[-70,35])color("slategray")translate([-36,ey,0])endblock();

for(rx=[-28,33])color("gray")translate([rx,-72,6])rotate([-90,0,0])cylinder(d=3,h=120);

color("slategray")translate([41.5,19,14])import("../components/index.stl");

for(x=[-8,13.08])for(y=[-5,10.08])color("gray")translate([x,y,28.5])cylinder(d=3,h=55);

color("dimgray")translate([-18.61,-56.15,-33])cube([42.3,42.3,40]);


}

module brace(side){
mirror([side<0?1:0,0,0]){

translate([5.5,-2,0])cube([3,4,.48]);
translate([6,-1,0])cube([2,2,35.4]);

for(i=[0:1]){
z=(side>0?17.2:15.76)+12*i;

hull(){
translate([6.2,-.4,z-4.5])cube([.8,.8,.6]);
translate([2.1,-.4,z-.48])cube([.3,.8,.6]);
}

translate([1.35,-.225,z-.12])cube([.95,.45,.24]);
}
}
}

if(part=="screw-supported"){
import("../components/screw.stl");
brace(1);
brace(-1);
}


if(part=="guide-coupon")difference(){
translate([-4,-4,0])cube([13.08,8,2]);
for(x=[0,5.08])translate([x-guide_open/2,-guide_open/2,-.01])cube([guide_open,guide_open,2.02]);
}


if(part=="strap")difference(){
translate([-4,-9,0])cube([8,23.08,2]);
for(y=[-5,10.08])translate([0,y,0])hole(3.4,2);
}


if(part=="index")difference(){
translate([-6.5,-2,0])cube([10,26,2]);
for(y=[0,5.08])translate([0,y,0])hole(3.2,2);
translate([-3.5,20,0])hole(3.4,2);
}


if(part=="cap")difference(){
translate([-6.8,-4,0])cube([18.68,8,2]);
for(x=[0,5.08])translate([x,0,0])hole(4.3,2);
for(mx=[-23.46,28.54])for(my=[-52,-18])translate([mx,my,3.9])cylinder(d=2.5,h=5.2);
for(x=[-5.3,10.38])translate([x,0,0])hole(2.2,2);
}


if(part=="torque-arm")difference(){
union(){
cylinder(d=7,h=3);
translate([0,-1.5,0])cube([21.5,3,3]);
}
translate([-1.15,-1.15,-.01])cube([2.3,2.3,3.02]);
translate([20,0,0])hole(1.8,3);
}




if(part=="yoke-long")translate([0,0,2.45])rotate([0,90,0])long_yoke();


module motorplate(){
difference(){
translate([-27.46,-57,9])cube([60,45,3]);
hull(){
for(my=[-35,-39])translate([2.54,my,8.9])cylinder(d=23,h=3.2);
}
for(x=[-15.5,15.5])for(y=[-15.5,15.5])hull(){
for(dy=[-4,0])translate([2.54+x,-35+y+dy,8.9])cylinder(d=3.5,h=3.2);
}
for(mx=[-23.46,28.54])for(my=[-52,-18])translate([mx,my,8.9])cylinder(d=3.4,h=3.2);
}
}

if(part=="motorplate")translate([0,0,-9])motorplate();
