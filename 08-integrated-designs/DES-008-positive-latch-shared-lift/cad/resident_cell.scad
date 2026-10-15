// DES-008 resident C-guide integration STUDY; mm. Not fabrication CAD.
// Represents pin / captured A+B T-feet / C-guide / grounded pawl ramp.
// Row lift transmission, wide upper guide plates, upper/lower channel guidance,
// ground root frame and bank drive remain unreleased; see study.md.
// part: assembly | channel | dog | dog_guide | pin | rail | b_dog | b_rail
//       pawl | ground_seat | pockets | channel_top
part="assembly";
pitch=6.35;
bit=1;                 // 1 admitted, 0 farther withdrawn
A=0.85;                // 0 writing; .85 engaged
lift=-30.4;            // acquisition; loaded pulse extrema approximately -50..-10
height=0;              // terrain range 0 .. 50
row_lift=0;            // 0 retained; 2 acquisition; only with A=0, dogs clear
B=0;                   // 0 B raised; 1 B down 1.2 mm / pawl retracted .85
nx=2; ny=2;
$fn=24;
function cy(b,a)=-3.05-1.6*(1-b)+a;

module pin(h=0){
 translate([0,0,h]) difference(){
  union(){
   translate([-1.4,-1.2,-85]) cube([2.8,2.4,130]);
   translate([-2.4,-2.4,45]) cube([4.8,4.8,90]);
   translate([-2.4,-2.4,135]) cube([4.8,4.8,1.2]);
  }
  // One face serves spatially separated grounded and moving dogs.
  // Ground phases [-50,0]; A acquisition phases [-80,-30].
  for(z=[-80:5:0]) translate([.3,-1.21,z-2.0]) cube([1.0,.66,3.2]);
 }
}
module channel(b=1,a=.85,r=0){
 translate([0,cy(b,a),r]) union(){
 difference(){
  translate([2.2,-1.2,-104]) cube([1.6,2.4,136]);
  // Captive T-slot: .25 mm retention overlap / side, .10 Y clearance.
  translate([2.5,-.85,-104.1]) cube([1,1.7,136.2]);
  translate([2.1,-.5,-104.1]) cube([.5,1,136.2]);
 }
  // Bottom and top positive-register feet. Both release after 1.2 mm lift.
  // Joined end bridges are REAL required parts/processes: T-feet must be
  // inserted before final bridge attachment. The joining process is unquoted.
  translate([2.2,-1.2,-104]) cube([1.6,2.4,.5]);
  translate([2.2,-1.2,31.5]) cube([1.6,2.4,.5]);
  translate([2.65,-.4,-105.2]) cube([.7,.8,1.3]);
  translate([3.8,-.4,30]) cube([.65,.8,.8]);
  translate([3.95,-.4,28.8]) cube([.5,.8,1.3]);
  // Cassette shoulder and OLD-aligned programming lug.
  translate([1.9,-1.2,-101]) cube([2.2,2.4,.6]);
  translate([2.8,.1,31.9]) cube([.4,.4,2.1]);
  // Bottom second-lug makes endpoint programming bilateral during row unlock.
  translate([3.8,.1,-101]) cube([.8,.4,.6]);
  translate([4.2,.1,-100.4]) cube([.4,.4,2]);
 }
}
module dog(b=1,a=.85,z=-30.4){
 translate([0,cy(b,a),z]) union(){
  // Sliding long key body at rail; .35 X wide precision metal reference.
  translate([1.65,-.4,-1.3]) cube([.35,4.0,2.6]);
  // L beam from key to rack and T-foot.
  translate([.4,-.2,-1.3]) cube([1,.4,2.6]);
  translate([1.4,-.4,-1.3]) cube([1.25,.8,2.6]);
  translate([.4,-.2,-1.3]) cube([.8,1.7,2.6]);
  translate([2.75,-.75,-1.3]) cube([.5,1.5,2.6]);
  translate([2.6,-.4,-1.3]) cube([.2,.8,2.6]);
 }
}
module dog_guide(z=-30.4){
 // Fixed Y location; long key body remains in this guide at all bit/A poses.
 translate([0,0,z]) difference(){
  translate([1.5,-1.65,-1.55]) cube([.65,.5,3.1]);
  translate([1.6,-1.75,-1.4]) cube([.45,.7,2.8]);
 }
}
module rail(z=-30.4,rows=2){
 // Thin steel Y rail. It cannot be replaced by a solid X-crosslinked platen.
 translate([1.65,-6,z-22]) cube([.4,(rows-1)*pitch+12,20.45]);
}
module b_dog(b=1,a=.85,down=0){
 z=5-1.2*down;
 translate([0,cy(b,a),z]) union(){
  translate([1.65,-.4,-1.3]) cube([.35,4.0,2.6]);
  translate([.4,-.2,-.5]) cube([2.25,.4,1]);
  translate([2.75,-.75,-1.3]) cube([.5,1.5,2.6]);
  translate([2.6,-.4,-1.3]) cube([.2,.8,2.6]);
  // Rounded fixed nose: not a 4,096-bearing proposal. Friction is included.
  // Initial centre3.682843, tangent to slope after .35 approach.
  translate([.4,0,-1.317157]) rotate([0,90,0]) cylinder(r=.2,h=.8);
  translate([.4,-.15,-1.317157]) cube([.8,.3,.817157]);
 }
}
module b_rail(down=0,rows=2){
 translate([1.65,-6,5-1.2*down+1.55]) cube([.4,(rows-1)*pitch+12,20]);
}
module wedge(){
 // 45 degree top is cut back at Y=-1.3 to clear the pin faceY=-1.2.
 translate([.4,0,0]) rotate([0,90,0])
  linear_extrude(height=.8) polygon([[-2,-2.45],[-3.3,-2.45],[-2.15,-1.3],[-2,-1.3]]);
}
module pawl(release=0){
 translate([0,-release,0]){
  translate([-1.4,-2.1,0]) cube([2.6,.4,1.2]);
  translate([.4,-2.45,0]) cube([.8,1.75,1.2]);
  translate([.4,-2.35,1.2]) cube([.8,1.05,.8]);
  wedge();
 }
 // Cubic end-force elastic-deflection envelope; does not solve contact/stress.
 for(k=[0:19]) hull() for(q=[k,k+1]){
  s=1-q/20;
  d=release*s*s*(3-s)/2;
  translate([-1.4,-2.1-d,2*q]) cube([1.2,.4,.05]);
 }
}
module ground_seat(){
 // Supports the pawl immediately outside the pin; no fixed material in rack.
 translate([.35,-1.9,-.8]) cube([.9,.5,.8]);
}
module channel_top(a=.85){
 // Top positive Y register + X slide guide on common A subframe.
 difference(){
  translate([1.9,-6.3+a,28.5]) cube([2.85,4.9,1.5]);
  translate([2.1,-6.0+a,28.4]) cube([1.8,4.3,1.7]);
  for(b=[0,1]) translate([3.85,cy(b,a)-.5,28.7]) cube([.7,1,1.4]);
 }
}
module cassette(a=.85,r=0,cols=2){
 translate([0,0,r]) difference(){
  translate([1.7,-6.2+a,-102]) cube([(cols-1)*pitch+2.6,5.7,1]);
  for(i=[0:cols-1]) translate([i*pitch+2.1,-6+a,-102.1]) cube([1.8,4.3,1.2]);
 }
}
module codebar(b=1,a=0,rows=2){
 yc=cy(b,a)+.3;
 difference(){
  translate([2.5,yc-10,34.4]) cube([1,(rows-1)*pitch+20,3]);
  for(j=[0:rows-1]) translate([2.7,j*pitch+yc-.3,34.3]) cube([.6,.6,2.2]);
 }
}
module lower_codebar(b=1,a=0,rows=2){
 yc=cy(b,a)+.3;
 difference(){
  translate([4.0,yc-10,-98]) cube([.8,(rows-1)*pitch+20,3]);
  for(j=[0:rows-1]) translate([4.1,j*pitch+yc-.3,-98.1]) cube([.6,.6,2.2]);
 }
}
module writer_pair(b=1,a=0,rows=2){
 // External paired-links are stiffness envelopes, not released bearing joints.
 yc=cy(b,a)+.3;
 union(){
  codebar(b,a,rows);lower_codebar(b,a,rows);
  for(y=[yc-8,(rows-1)*pitch+yc+8])
   translate([2.5,y-1.75,-96]) cube([2.5,3.5,133.4]);
 }
}
module pockets(a=.85){
 // Retention cells on the common A subframe. No row lift/codebar is faked.
 difference(){
  translate([1.7,-6.2+a,-107]) cube([2.6,5.7,3]);
  for(b=[0,1]) translate([2.55,cy(b,a)-.5,-105.2]) cube([.9,1,1.3]);
 }
}
module assembly(){
 for(i=[0:nx-1]){
  color("slategray") translate([i*pitch,0,0]) rail(lift,ny);
  color("navy") translate([i*pitch,0,0]) b_rail(B,ny);
  color("teal") translate([i*pitch,0,0]) writer_pair(i%2,A,ny);
  for(j=[0:ny-1]){
   b=(i+j)%2;
   translate([i*pitch,j*pitch,0]){
    color([.6,.7,.8,.7]) pin(height);
    color("orange") channel(b,A,j==0?row_lift:0);
    color("crimson") dog(b,A,lift);
    color("purple") b_dog(b,A,B);
    color("steelblue") dog_guide(lift);
    color("royalblue") dog_guide(5-1.2*B);
    color("green") pawl(b*max(0,1.2*B-.35));
    color("darkgreen") ground_seat();
    color([.5,.5,.5,.4]) channel_top(A);
    color("gray") pockets(A);
   }
  }
 }
 for(j=[0:ny-1]) color("silver") translate([0,j*pitch,0]) cassette(A,j==0?row_lift:0,nx);
}
if(part=="assembly") assembly();
else if(part=="channel") channel(bit,A,row_lift);
else if(part=="dog") dog(bit,A,lift);
else if(part=="dog_guide") dog_guide(lift);
else if(part=="pin") pin(height);
else if(part=="rail") rail(lift,ny);
else if(part=="b_dog") b_dog(bit,A,B);
else if(part=="b_rail") b_rail(B,ny);
else if(part=="pawl") pawl(bit*max(0,1.2*B-.35));
else if(part=="ground_seat") ground_seat();
else if(part=="channel_top") channel_top(A);
else if(part=="cassette") cassette(A,row_lift,nx);
else if(part=="codebar") codebar(bit,A,ny);
else if(part=="lower_codebar") lower_codebar(bit,A,ny);
else if(part=="writer_pair") writer_pair(bit,A,ny);
else if(part=="pockets") pockets(A);
