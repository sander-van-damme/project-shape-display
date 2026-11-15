// External print-only braces. mm. Not an assembly component or physical validation.
// Four bed feet/towers with diagonal arms; only .46 x .60 x .24 necks touch flats.
// Clip each neck at the part and trim flush. Never twist the towers off.
part="pin-supported";
$fn=48;
module braces(face,post,levels,top){
 for(a=[0,90,180,270])rotate([0,0,a]){
  translate([post-1.5,-1.5,0])cube([3,3,.48]);
  translate([post-1,-1,0])cube([2,2,top]);
  for(z=levels){
   hull(){
    translate([post-.8,-.5,z-3])cube([.8,1,.6]);
    translate([face+.32,-.5,z-.24])cube([.30,1,.24]);
   }
   translate([face-.06,-.30,z-.12])cube([.46,.60,.24]);
  }
 }
}
if(part=="pin-supported"){
 import("../components/pin.stl");
 braces(2.25,5.5,[8,17,26,35],35.5);
}
if(part=="male-supported"){
 import("../components/male.stl");
 braces(1,4.25,[6,10.2,14.4],14.8);
}
