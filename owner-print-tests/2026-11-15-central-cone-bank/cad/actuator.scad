// DES owner-commissioned actuator coupon. Units mm; no physical qualification.
// CLI openscad -o part.stl -D 'part="base"' actuator.scad
part="assembly";
$fn=48;
travel=10; lift=3;
module hole(d,h){cylinder(d=d,h=h,center=true);}
module along_y(d,h){rotate([90,0,0])cylinder(d=d,h=h,center=true);}
module base(){
 difference(){
 union(){
 translate([6,0,1.5])cube([36,82,3],center=true);
 // external guide walls leave 0.3 mm per side
 for(x=[-7,19])translate([x,0,4.5])cube([1.4,36,3],center=true);
 for(y=[-17,17])translate([2,y,4.5])cube([16,1.2,3],center=true);
 // fixed coil seats; bobbins slide in from the outer end
 for(y=[-27,27])for(a=[-8,8])translate([14,y+a,7])difference(){cube([13,2,8],center=true);translate([0,0,1.5])along_y(10.95,4);}
 // spring wire anchor
 translate([-8,-15,4.5])cube([3,5,3],center=true);
 }
 for(x=[-6,18])for(y=[-38,38])translate([x,y,2])hole(3.4,8);
 for(x=[-10,22])translate([x,0,1.5])hole(1.8,5);
 // spring anchor hole accepts 0.35 mm wire, measured/reamed manually
 translate([-8,-15,4.5])along_y(.55,10);
 // wire free tip needs lateral clearance in guide wall
 translate([-7,0,4.7])cube([4,7,2],center=true);
 }
}
module slider(){
 difference(){
 union(){
 translate([6,0,1.5])cube([24,22,3],center=true);
 // cam: local low +y, high -y; 6mm ramp /3mm lift
 translate([4,0,3])rotate([0,-90,0])linear_extrude(8)polygon([[0,-7],[3,-7],[3,-3],[0,3],[0,7],[-.1,7],[-.1,-7]]);
 // rod clamps; removable M2 screws pinch steel plungers
 for(y=[-9,9])translate([14,y,5.2])difference(){cube([7,6,6],center=true);along_y(3.25,9);translate([0,0,2])hole(1.8,6);}
 // manual knob well outside spring path
 translate([14,0,6])cube([6,6,8],center=true);
 }
 // two side notches for bent wire detent; triangular lead-in either direction
 for(y=[-5,5])translate([-6,y,1.5])cylinder(r=.85,h=5,center=true,$fn=4);
 }
}
// Winding: bare Cu 0.20mm, ~0.22mm turn pitch, 63 turns/layer x9=567 (14mm clear length).
// Bore axis y in assembly; print bobbin vertical on its flange.
module bobbin(){difference(){union(){cylinder(d=4.8,h=16);for(z=[0,15])translate([0,0,z])cylinder(d=10.8,h=1); } translate([0,0,-1])cylinder(d=3.65,h=18);for(z=[.5,15.5])translate([4.4,0,z])hole(.9,3);}}
// spring-loaded follower measurement carriage; insert known weights or calibrated spring
module follower(){difference(){union(){translate([0,0,3])cube([7,7,6],center=true);translate([0,0,5.8])cylinder(d=9,h=2);}translate([0,0,4])hole(2.4,12);}}
module follower_bridge(){difference(){union(){for(x=[-10,22])translate([x,0,11])cube([3,10,22],center=true);translate([6,0,22])cube([36,10,3],center=true);}translate([0,0,22])hole(3,6);for(x=[-10,22])translate([x,0,11])hole(2.2,30);}}
module assembly(){
 color("silver")base();
 color("orange")translate([0,-5,3.3])slider();
 for(y=[-27,27]) color("sienna")translate([14,y-8,8.5])rotate([-90,0,0])bobbin();
 // metal plungers: 3 x24mm mild-steel rods clamped at y +/-9
 for(y=[-21,21])color("gray")translate([14,y-5,8.5])along_y(3,24);
 color("red")translate([0,0,10.3])follower();
 color("gray")translate([0,0,6.3])cylinder(d=2,h=25);
 // removable bridge is screw/clamp held to base externally during force testing
 color([.3,.5,.8,.5])translate([0,0,3])follower_bridge();
}
if(part=="base")base();
else if(part=="slider")slider();
else if(part=="bobbin")bobbin();
else if(part=="follower")follower();
else if(part=="bridge")translate([0,0,23.5])rotate([180,0,0])follower_bridge();
else assembly();
