// Exact 5.08-mm pitch. Round stems allow all nine columns to rotate and lift.
part="stand"; $fn=64; pitch=5.08; hole=3.6;
module ring(od,id,h){difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}
// Printed inverted: flat deck on bed, four legs upward. Assembly deck Z20..22.
module stand(){difference(){union(){translate([-13,-13,0])cube([26,26,2]);
 for(x=[-11,9])for(y=[-11,9])translate([x,y,2])cube([2,2,20]);}
 for(x=[-1:1])for(y=[-1:1])translate([x*pitch,y*pitch,-.01])cylinder(d=(x==0&&y==0)?4.8:hole,h=2.02);
}}
module pin(){union(){
 cylinder(d=2.4,h=23);
 translate([0,0,22])cylinder(d1=2.4,d2=4.4,h=3);
 difference(){translate([-2.2,-2.2,25])cube([4.4,4.4,30]);translate([-1.5,-1.5,26.2])cube([3,3,29]);}
}}
// Optional peripheral restraint: sits on the stand; assembly ring Z32..34.
module boundary(){difference(){translate([-13,-13,0])cube([26,26,2]);translate([-7.5,-7.5,-.01])cube([15,15,2.02]);}
 for(x=[-11,9])for(y=[-11,9])translate([x,y,2])cube([2,2,10]);
}
// Removable close-play plate; raises deck 1.2 mm, all height spacers remain comparable.
module liner(){difference(){translate([-8,-8,0])cube([16,16,1.2]);
 for(x=[-1:1])for(y=[-1:1])translate([x*pitch,y*pitch,-.01])cylinder(d=(x==0&&y==0)?4.8:3,h=1.22);
}}
if(part=="stand")stand();
if(part=="pin")pin();
if(part=="boundary")boundary();
if(part=="liner")liner();
// Height risers reach the underside of the body cone at z~24; nominal 3/18 heights.
if(part=="spacer-3")ring(4.4,2.9,3);
if(part=="spacer-15")ring(4.4,2.9,15);
