// Repaired A-010: x/y are the shared indexing datum; z is load axis.
// Geometry evidence only; all dimensions are mm.
$fn = 48;
include <a010_carriage_params.scad>;
field = cartridge;
travel = state_y[len(state_y)-1] - state_y[0];

module frame_plate(z,t,c="lightgray") {
  color(c) translate([-field/2,-field/2,z]) cube([field,field,t]);
}
module guide_channel() {
  color("silver") {
    translate([-guide_x/2-0.40,-2.45,guide_z0]) cube([0.40,guide_y,guide_z1-guide_z0]);
    translate([ guide_x/2,  -2.45,guide_z0]) cube([0.40,guide_y,guide_z1-guide_z0]);
  }
}
module gate_slider(y) {
  difference() {
    color("orange") translate([-slider_x/2,-field/2,gate_z]) cube([slider_x,field,gate_t]);
    translate([0,y,gate_z-0.01]) cube([gate_window,gate_window,gate_t+0.02],center=true);
  }
}
module indexed_stop_plate() {
  difference() {
    frame_plate(stop_z,stop_t,"lightblue");
    for (y=state_y) translate([0,y,stop_z-0.01]) cube([stop_bore,stop_bore,stop_t+0.02],center=true);
  }
}
module carriage_and_load_path(y, alpha=1.0) {
  color([0,1,0,alpha]) translate([-carriage_x/2,y-carriage_y/2,gate_z+gate_t])
    cube([carriage_x,carriage_y,stop_z-(gate_z+gate_t)]);
  color([0.55,0,0.75,alpha]) translate([0,y,gate_z+gate_t])
    cylinder(d=follower_d,h=stop_z-(gate_z+gate_t)+0.02);
  color([0.55,0,0.75,alpha]) translate([0,y,stop_z+stop_t])
    cylinder(d=shoulder_d,h=shoulder_t);
}
module writer_path() {
  color("red") translate([-0.30,state_y[0]-writer_approach,gate_z+gate_t])
    cube([0.60,travel+2*writer_approach,0.20]);
  color("red") translate([-0.30,state_y[0]-writer_approach,gate_z])
    cube([0.60,tab_engagement,gate_t]);
}
guide_channel();
frame_plate(0,0.20,"gray");
indexed_stop_plate();
gate_slider(state_y[2]);
carriage_and_load_path(state_y[2]);
for (i=[0:state_count-1]) if (i != 2) carriage_and_load_path(state_y[i],0.18);
writer_path();
for (y=state_y) color("black") translate([-3.0,y,0.02]) cube([0.20,0.08,0.08]);
