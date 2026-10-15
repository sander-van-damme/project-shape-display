// DES-008 minimum positive load-transfer experiment, B workstream.
// Units mm. No machine-level speed/lifetime qualification.
// Export: openscad -o part.stl -D 'part="..."' rack_handoff.scad
// Render: part="assembly". Export individual print poses; arrange plate externally.
// Four active columns + four mechanically identical untouched witnesses.
// Cap offset +0.20 X gives a flat pin print face; inspect short pocket bridges.
$fn=32;
part="assembly";
component="pin";
index=0;
phase="park"; // park, capture, unloaded, move, restored
pulse=5;
selected=[1,0,1,0];
active_h=[0,5,10,5];
witness_h=[5,10,0,5];
pitch=6.35;
N=4;
stroke=10;
stem_x=4.6;
stem_y=2.8;
groove_depth=.85;
groove_width=3.4; // continuous 0.6-mm edge lands retain guide datum
working_tooth_width=2.4;
groove_h=3.2;
groove_pitch=5;
ground_tip_h=1.2;
drive_tip_h=2.6;
key_slot_play=.25;
cavity_half=(drive_tip_h+key_slot_play)/2;
frame_half=cavity_half+1.2;
unload=.3;
dog_initial_gap=.3;
release=.85; // drive-key travel
ground_release=1.05; // includes keeper pin/slot clearance allowance
leaf_t=.6;
leaf_y=-3.45;
ground_bottom=52.0;
ground_top=ground_bottom+ground_tip_h;
dog_home_top=7.9;
dog_center=dog_home_top-drive_tip_h/2+key_slot_play/2;
cx0=-22;
cx1=42.05;
cy=-6;
corner_x=[cx0,cx1];
stand_x=[-22,42.05];
root_x=[-15,35.05];
corner_y=[-6.0,11.0];
plate_x0=-25;
plate_y0=-8.5;
plate_w=70.05;
plate_d=22;

function is_moving()=phase=="unloaded" || phase=="move";
function is_captured()=phase!="park";
function is_shifted()=phase=="move" || phase=="restored";
function z_preload()=phase=="unloaded" || phase=="move" || phase=="restored" ? dog_initial_gap+unload : 0;
function pin_preload()=phase=="unloaded" || phase=="move" || phase=="restored" ? unload : 0;
function z_head()=dog_center+z_preload()+(is_shifted()?pulse:0);

module pin(){
  difference(){
    union(){
      translate([-stem_x/2,-stem_y/2,-25]) cube([stem_x,stem_y,95]);
      // Whole stem and cap share X=-2.3 face. Print that side on bed.
      translate([-stem_x/2,-2.5,70]) cube([5,5,2]);
    }
    for(k=[-5:12]){
      translate([-groove_width/2,-stem_y/2-.1,k*groove_pitch])
        cube([groove_width,groove_depth+.1,groove_h]);
      translate([-groove_width/2,stem_y/2-groove_depth,k*groove_pitch])
        cube([groove_width,groove_depth+.1,groove_h]);
    }
  }
}

module pin_print(){
  // Original minimum X=-2.3 becomes print Z=0. Original Z becomes X.
  translate([72,3,stem_x/2]) rotate([0,-90,0]) pin();
}

module ground_comb(){
  // A flexible spring comb. Grounded seat is an independent rigid part.
  union(){
    translate([-2.55,leaf_y,30]) cube([3*pitch+5.1,leaf_t,2]);
    for(i=[0:N-1]) translate([i*pitch,0,0]){
      translate([-2.2,leaf_y,32]) cube([4.4,leaf_t,ground_bottom-32]);
      // Head sits ON rigid seat. Its flexure is not the terrain load path.
      translate([-2.2,leaf_y,ground_bottom])
        cube([4.4,-1.65-leaf_y,ground_tip_h]);
      translate([-working_tooth_width/2,-1.65,ground_bottom])
        cube([working_tooth_width,.70,ground_tip_h]);
      // Accessible pull tab; same plane as leaf, no overhang in print pose.
      translate([-.8,leaf_y,ground_top]) cube([1.6,leaf_t,5.0]);
    }
  }
}

module ground_comb_print(){
  // Back of every leaf is on bed. XZ becomes XY; Y is print height.
  translate([3,58.2,-leaf_y]) rotate([90,0,0]) ground_comb();
}

module comb_deformed(mask=[0,0,0,0]){
  // Assembly visualization of flexible leaf. Actual printable comb stays flat.
  translate([-2.55,leaf_y,30]) cube([3*pitch+5.1,leaf_t,2]);
  for(i=[0:N-1]) translate([i*pitch,0,0]){
    d=mask[i]?ground_release:0;
    for(k=[0:19])hull(){
      t=k/20;u=(k+1)/20;
      translate([-2.2,leaf_y-d*(3*t*t-t*t*t)/2,32+20*t])cube([4.4,leaf_t,.01]);
      translate([-2.2,leaf_y-d*(3*u*u-u*u*u)/2,32+20*u-.01])cube([4.4,leaf_t,.01]);
    }
    translate([-2.2,leaf_y-d,ground_bottom]) cube([4.4,-1.65-leaf_y,ground_tip_h]);
    translate([-working_tooth_width/2,-1.65-d,ground_bottom]) cube([working_tooth_width,.70,ground_tip_h]);
    translate([-.8,leaf_y-d,ground_top]) cube([1.6,leaf_t,5.0]);
  }
}

module pin_apertures(z,h){
  for(j=[0:1],i=[0:N-1])
    translate([i*pitch-2.5,j*pitch-1.5,z]) cube([5.0,3.0,h]);
}
module corner_holes(z,h){
  for(x=stand_x,y=corner_y) translate([x,y,z]) cylinder(d=3.2,h=h);
}

module lower_guide(){
  difference(){
    translate([plate_x0,plate_y0,29]) cube([plate_w,plate_d,3]);
    pin_apertures(28.9,3.2);
    corner_holes(28.9,3.2);
    // Comb roots drop into pockets; bottom is a hard Z datum.
    for(j=[0:1]) translate([-2.75,j*pitch-4.65,30])
      cube([3*pitch+5.5,1.95,2.1]);
    for(j=[0:1],x=root_x)translate([x,j*pitch-3.15,28.9])cylinder(d=3.2,h=3.2);

  }
}

module root_clamp(row=0){
  // Install over a FREE comb before comb/seat assembly. Defined pads bear
  // on root at Z32; other undersides have 0.30 relief so bolt load reaches
  // the root before rigid frame faces. Check actual preload after printing.
  difference(){
    union(){
      translate([-2.75,-4.5,30.3])cube([24.55,1.05,1.70]);
      translate([-15,-4.45,32.3])cube([50.05,.85,3.7]);
      for(i=[-1:3]){
        translate([i*pitch+2.35,-4.45,32.3])cube([1.65,1.75,3.7]);
        intersection(){
          translate([i*pitch+2.35,-4.45,31.99])cube([1.65,1.0,.32]);
          translate([-2.75,-4.45,31.99])cube([24.55,1.0,.32]);
        }
        intersection(){
          translate([i*pitch+2.35,-3.45,32])cube([1.65,.6,.31]);
          translate([-2.55,-3.45,32])cube([24.15,.6,.31]);
        }
      }
      for(x=root_x)translate([x-2.3,-5.4,32.3])cube([4.6,4.5,3.7]);
    }
    for(x=root_x)translate([x,-3.15,31.9])cylinder(d=3.2,h=4.2);
  }
}

module upper_guide(){
  difference(){
    translate([plate_x0,plate_y0,59]) cube([plate_w,plate_d,3]);
    pin_apertures(58.9,3.2);
    // Front access to pull buttons and independent keeper insertion.
    translate([-3,-9,58.9])cube([25.05,6.5,3.2]);
    corner_holes(58.9,3.2);
    for(j=[0:1],x=root_x)translate([x,j*pitch-3.15,58.9])cylinder(d=3.5,h=3.2);
  }
}

module ground_seat(){
  difference(){
    union(){
      translate([plate_x0,plate_y0,48]) cube([plate_w,plate_d,4]);
      // Fixed positive Y reaction for four independent released-pawl keepers.
      translate([-2.3,-8.5,52])cube([23.65,2.0,4]);
    }
    pin_apertures(47.9,4.2);
    corner_holes(47.9,4.2);
    for(j=[0:1],x=root_x)translate([x,j*pitch-3.15,47.9])cylinder(d=3.5,h=4.2);
    for(i=[0:N-1])translate([i*pitch,-7.5,53.5])cylinder(d=2.0,h=2.6);
    // Leaves clear plate during outward deflection. Keep positive rear ledge.
    for(j=[0:1],i=[0:N-1]) translate([i*pitch-2.45,j*pitch-6.0,47.9])
      cube([4.9,3.30,4.2]);
  }
}

module spacer(h=16){
  difference(){
    cylinder(d=5.5,h=h);
    translate([0,0,-.1]) cylinder(d=3.2,h=h+.2);
  }
}

module frame_foot(){
  // Separate gravity support cup. Plate bears on annular top; nut/tip clear.
  // Hold frame down during manual travel. These are not tension fasteners.
  difference(){
    cylinder(d=9,h=17);
    translate([0,0,14])cylinder(d=6.8,h=3.1);
    translate([0,0,11])cylinder(d=3.4,h=6.1);
  }
}

module bottom_guide(){
  // Five-mm bearing region; 2-mm peripheral web reduces coupon material.
  difference(){
    union(){
      translate([plate_x0,plate_y0,-14])cube([plate_w,plate_d,2]);
      translate([-3,-2,-14])cube([25.05,10.35,5]);
      for(x=stand_x,y=corner_y)translate([x,y,-14])cylinder(d=5.5,h=5);
    }
    pin_apertures(-14.1,5.2);
    corner_holes(-14.1,5.2);
    // Relieve empty wings while retaining 3-mm webs to the stand-off feet.
    for(x=[-17,25])translate([x,-2,-14.1])cube([12,10,2.2]);
  }
}

module drive_key(){
  union(){
    translate([-2.1,1.85,-drive_tip_h/2])cube([4.2,1.65,drive_tip_h]);
    translate([-working_tooth_width/2,.95,-drive_tip_h/2])cube([working_tooth_width,.90,drive_tip_h]);
    translate([2.85,-8,-drive_tip_h/2])cube([.6,11.5,drive_tip_h]);
    translate([2.05,2.9,-drive_tip_h/2])cube([1.4,.6,drive_tip_h]);
    translate([1.2,-8,-drive_tip_h/2])cube([3.9,2.4,drive_tip_h]);
  }
}

module carriage_base(){
  difference(){
    union(){
      // Stiff continuous floor; pin clearance admits combined guide play.
      difference(){
        translate([cx0-4.5,-12,-frame_half-2.4])cube([cx1-cx0+9,17.675,3.6]);
        for(i=[0:N-1])translate([i*pitch-2.8,-1.8,-frame_half-2.5])cube([5.6,3.6,3.8]);
        translate([-3,4.35,-frame_half-2.5])cube([25.05,1.5,3.8]);
      }
      translate([cx0-2.5,1.9,-frame_half])cube([cx1-cx0+5,2.45,1.2]);
      for(x=corner_x){
        translate([x-4.5,-9.5,-frame_half])cube([9,15.175,frame_half+cavity_half]);
        translate([x,cy,-frame_half])cylinder(d=9,h=16);
      }
      for(i=[0:N])translate([i*pitch-2.75,1.9,-cavity_half])cube([.5,2.45,2*cavity_half]);
      for(x=[cx0-1.5,cx1+.5])translate([x,-12,-frame_half])cube([1,15.2,2]);
      translate([cx0-1.5,-12,-frame_half])cube([cx1-cx0+3,1.7,2]);
      translate([cx0-1.5,-9.2,-frame_half])cube([cx1-cx0+3,1.2,1.2]);
      // Wide front handle pockets supply positive ON and OFF Y stops.
      translate([.7,-9.2,-frame_half])cube([24.3,5.65,frame_half+cavity_half]);
    }
    for(x=corner_x){
      translate([x,cy,-frame_half-2.5])cylinder(d=5.9,h=18.6);
      translate([x,2.8,-frame_half-2.5])cylinder(d=3.2,h=2*frame_half+2.6);
    }
    for(i=[0:N-1]){
      // 2.4 mm handle + .85 mm stroke. Stop faces are intentional contacts.
      translate([i*pitch+1.0,-8,-cavity_half])cube([4.3,3.25,2*cavity_half+.1]);
      // Sidearm continues behind its handle to the working dog.
      translate([i*pitch+2.7,-4.8,-cavity_half])cube([.9,1.4,2*cavity_half+.1]);
    }
  }
}

module carriage_lid(){
  difference(){
    union(){
      translate([cx0-2.5,1.9,cavity_half])cube([cx1-cx0+5,2.45,6]);
      for(x=corner_x)translate([x-4.5,-6,cavity_half])cube([9,10.35,6]);
    }
    for(x=corner_x){
      translate([x,cy,cavity_half-.1])cylinder(d=9.4,h=6.2);
      translate([x,2.8,cavity_half-.1])cylinder(d=3.2,h=6.2);
    }
  }
}

module ground_keeper(){
  // Released position. Lower over one pull button with +1.05 Y offset,
  // pull forward until the peg aligns, then let the peg drop into fixed wall.
  difference(){
    union(){
      translate([-1.8,-8.5,56.1])cube([3.6,5.6,1.2]);
      translate([0,-7.5,54.6])cylinder(d=1.6,h=1.6);
    }
    translate([-1.0,-4.7,56.0])cube([2.0,1.0,1.4]);
  }
}
module ground_keeper_print(){translate([1.8,0,57.3])rotate([180,0,0])ground_keeper();}

module dog_keeper(){
  // Insert into the .85 mm empty end of the front handle pocket.
  // It positively retains either ON or OFF while the head moves.
  difference(){
    union(){cube([3.5,.8,2.85]);translate([-.2,-.3,2.85])cube([3.9,1.4,1.2]);}
    // Working sidearm passes through the center; two feet block wide handle.
    translate([1.3,-.1,-.1])cube([.9,1.0,2.96]);
  }
}
module placed_dog_keeper(i=0){
  on=is_captured()&&selected[i];
  translate([i*pitch+1.4,on?-5.55:-8,z_head()-cavity_half])dog_keeper();
}

module dog_keeper_print(){translate([3.7,1.1,4.05])rotate([180,0,0])dog_keeper();}

// Hardware envelopes: ISO-style M3 socket heads diameter 5.5 x 3;
// hex nuts across flats 5.5, thickness 2.4. Holes are 3.2 mm.
module bolt_m3(length=10){
  cylinder(d=3,h=length);translate([0,0,length])cylinder(d=5.5,h=3);
}
module nut_m3(){difference(){cylinder(d=5.5/cos(30),h=2.4,$fn=6);translate([0,0,-.1])cylinder(d=3.0,h=2.6);}}
module hardware_piece(kind="bolt",i=0){
  // 0..3 frame M3x80; 4..7 comb-root M3x10;
  // 8..9 carriage-lid M3x16. Guide sleeves surround the front frame bolts.
  if(i<4){x=stand_x[i%2];y=corner_y[floor(i/2)];translate([x,y,kind=="bolt"?-18:-16.4])if(kind=="bolt")bolt_m3(length=80);else nut_m3();}
  else if(i<8){k=i-4;x=root_x[k%2];y=-3.15+floor(k/2)*pitch;translate([x,y,kind=="bolt"?26:26.6])if(kind=="bolt")bolt_m3(length=10);else nut_m3();}
  else {x=corner_x[i-8];top=z_head()+cavity_half+6;translate([x,2.8,kind=="bolt"?top-16:z_head()-frame_half-4.8])if(kind=="bolt")bolt_m3(length=16);else nut_m3();}

}

module assembly(){
  for(i=[0:9]){color("dimgray")hardware_piece("bolt",i);color("dimgray")hardware_piece("nut",i);}
  color("silver")lower_guide();
  color("silver")bottom_guide();
  color("silver")upper_guide();
  for(j=[0:1])color("purple")translate([0,j*pitch,0])root_clamp(j);
  color("gray")ground_seat();
  for(x=stand_x,y=corner_y){
    color("gray")translate([x,y,32])spacer(16);
    color("gray")translate([x,y,-9])spacer(38);
    color("gray")translate([x,y,52.0])spacer(7.0);
  }
  for(x=stand_x,y=corner_y)color("dimgray")translate([x,y,-31])frame_foot();
  for(i=[0:N-1]){
    color(i%2?"gold":"orange")translate([i*pitch,0,active_h[i]+(selected[i]?pin_preload()+(is_shifted()?pulse:0):0)])pin();
    color("lightsteelblue")translate([i*pitch,pitch,witness_h[i]])pin();
  }
  color("crimson")comb_deformed(is_moving()?selected:[0,0,0,0]);
  if(is_moving())for(i=[0:N-1])if(selected[i])color("magenta")translate([i*pitch,0,0])ground_keeper();
  color("indianred")translate([0,pitch,0])ground_comb();
  color("navy")translate([0,0,z_head()])carriage_base();
  color("royalblue")translate([0,0,z_head()])carriage_lid();
  for(i=[0:N-1])color("lime")placed_dog_keeper(i);
  for(i=[0:N-1])color(selected[i]?"green":"teal")
    translate([i*pitch,is_captured()&&selected[i]?0:release,z_head()-key_slot_play/2])drive_key();
}

module world_component(){
  if(component=="bolt"||component=="nut")hardware_piece(component,index);
  else if(component=="pin"){
    j=floor(index/4);i=index%4;
    translate([i*pitch,j*pitch,j?witness_h[i]:active_h[i]+(selected[i]?pin_preload()+(is_shifted()?pulse:0):0)])pin();
  }
  else if(component=="ground_comb"){
    if(index==0)comb_deformed(is_moving()?selected:[0,0,0,0]);
    else translate([0,pitch,0])ground_comb();
  }
  else if(component=="drive_key")translate([index*pitch,is_captured()&&selected[index]?0:release,z_head()-key_slot_play/2])drive_key();
  else if(component=="carriage_base")translate([0,0,z_head()])carriage_base();
  else if(component=="carriage_lid")translate([0,0,z_head()])carriage_lid();
  else if(component=="ground_keeper")translate([index*pitch,0,0])ground_keeper();
  else if(component=="spacer"){j=floor(index/4);k=index%4;translate([stand_x[k%2],corner_y[floor(k/2)],j==0?32:j==1?52:-9])spacer(j==0?16:j==1?7:38);}
  else if(component=="dog_keeper")placed_dog_keeper(index);
  else if(component=="root_clamp")translate([0,index*pitch,0])root_clamp(index);
  else if(component=="lower_guide")lower_guide();
  else if(component=="bottom_guide")bottom_guide();
  else if(component=="frame_foot")translate([stand_x[index%2],corner_y[floor(index/2)],-31])frame_foot();
  else if(component=="upper_guide")upper_guide();
  else if(component=="ground_seat")ground_seat();
}

if(part=="assembly")assembly();
else if(part=="component")world_component();
else if(part=="pin")pin_print();
else if(part=="ground_comb")ground_comb_print();
else if(part=="root_clamp"||part=="root_clamp_active")translate([17.3,0,36])rotate([180,0,0])root_clamp();
else if(part=="root_clamp_witness")translate([17.3,0,36])rotate([180,0,0])root_clamp(1);
else if(part=="lower_guide")translate([-plate_x0,-plate_y0,-29])lower_guide();
else if(part=="upper_guide")translate([-plate_x0,-plate_y0,-59])upper_guide();
else if(part=="ground_seat")translate([-plate_x0,-plate_y0,-48])ground_seat();
else if(part=="bottom_guide")translate([-plate_x0,-plate_y0,14])bottom_guide();
else if(part=="frame_foot")frame_foot();
else if(part=="drive_key")translate([2.1,8,drive_tip_h/2])drive_key();
else if(part=="carriage_base")translate([-cx0+4.5,12,frame_half+2.4])carriage_base();
else if(part=="carriage_lid")translate([-cx0+4.5,9.5,-cavity_half])carriage_lid();
else if(part=="spacer_long")spacer(16);
else if(part=="spacer_bottom")spacer(38);
else if(part=="spacer_short")spacer(7.0);
else if(part=="ground_keeper")ground_keeper_print();
else if(part=="dog_keeper")dog_keeper_print();
else assert(false,"Unknown part");
assert(abs(pulse)<=5,"Prototype single pulse must not exceed 5 mm");
