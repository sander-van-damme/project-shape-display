/* DES-008 mechanical RAM fixture, revision 3. Units mm.
   Captive flag shoulders, loading port, tall guides and keyed bar keepers.
   part = assembly | plate | base | cassette | flag | codebar | shim | keeper | key
   Unloaded memory test only: no terrain actuation or powered-speed claim. */
part="assembly";
show_old=[0,1]; show_other=[1,0]; selected_row=0;
$fn=40;
pitch=6.35; bit_travel=2; row_lift=2.7;
datum=1.5; floor_z=2+datum; bar_z=floor_z+6.4;
cols=[12,18.35]; rows=[12,18.35]; posts=[4,31.5];
module base(){
 difference(){
  union(){
   cube([36,32,floor_z]);
   for(y=rows){
    for(x=posts) translate([x,y,floor_z]) cylinder(d=2.4,h=13.1);
    for(x=[7,27]) for(dy=[-1.9,1.9]) translate([x-1.5,y+dy-.5,floor_z]) cube([3,1,.4]);
   }
   for(y=[1.5,26]) translate([8.5,y,floor_z]) cube([15,4.5,7.4]);
   for(y=[4,28]) for(x=[5,27]) translate([x-1.6,y-1.6,floor_z]) cube([3.2,3.2,10.1]);
  }
  for(y=rows) for(x=cols) for(b=[0,1])
   translate([x+bit_travel*b-.6,y-1.4,floor_z-2.3]) cube([1.2,2.8,2.4]);
  for(x=cols){
   translate([x-1.9,2.3,bar_z]) cube([5.8,3.8,1.1]);
   translate([x-1.9,25.9,bar_z]) cube([5.8,3.8,1.1]);
  }
  for(y=[4,28]) for(x=[5,27])
   translate([x-1,y-1.7,floor_z+7.9]) cube([2,3.4,1.4]);
 }
}
// Captured shoulder: 4.0 Y x 1.2 Z in a 4.4 Y x 1.4 Z channel.
// The 4.2 x 4.4 top loading port is outside both bits' operating ranges.
// Load rightmost flag first, slide it left, then load the other flag.
module cassette(){
 difference(){
  union(){
   translate([1.1,-2.7,0]) cube([33.3,5.4,3]);
   for(x=posts) translate([x-2.9,-2.7,0]) cube([5.8,5.4,10]);
  }
  translate([9,-2.2,.8]) cube([18.5,4.4,1.4]);
  translate([9,-1.4,-.1]) cube([18.5,2.8,3.2]);
  translate([23.2,-2.2,.7]) cube([4.3,4.4,2.4]);
  for(x=posts) translate([x,0,-.1]) cylinder(d=2.9,h=10.2);
 }
}
module flag(){
 union(){
  translate([-.4,-1.2,0]) cube([.8,2.4,3.3]);
  translate([-1.7,-2,3.3]) cube([3.4,4,1.2]);
  translate([-.5,-1.2,4.5]) cube([1,2.4,3.5]);
 }
}
module codebar(){
 difference(){
  translate([-1.9,2.5,0]) cube([3.8,27,3.5]);
  translate([-.7,7,-.1]) cube([1.4,18,2.7]);
 }
}
module shim(){
 difference(){
  translate([-4,-2.9,0]) cube([13,5.8,row_lift]);
  translate([1,-1.5,-.1]) cube([8.1,3,row_lift+.2]);
 }
}
module keeper(){
 difference(){
  union(){
   translate([5,-1,2.6]) cube([22,2,1.6]);
   for(x=[5,27]) translate([x-2.6,-2.8,0]) cube([5.2,5.6,4.2]);
  }
  for(x=[5,27]){
   translate([x-1.8,-1.8,-.1]) cube([3.6,3.6,2.7]);
   translate([x-1,-2.9,.4]) cube([2,5.8,1.4]);
  }
 }
}
module key(){
 union(){
  translate([-.8,0,0]) cube([1.6,7.5,1.2]);
  translate([-1.8,-1.5,0]) cube([3.6,1.5,1.2]);
 }
}
module assembly(){
 color("lightgray") base();
 for(i=[0:1]){
  lift=(selected_row==i)?row_lift:0;
  color("gold") translate([0,rows[i],floor_z+.4+lift]) cassette();
  for(j=[0:1]){
   bit=(i==0)?show_old[j]:show_other[j];
   color("crimson") translate([cols[j]+bit_travel*bit,rows[i],floor_z-2.1+lift]) flag();
  }
  if(i==selected_row){
   color("seagreen") translate([0,rows[i],floor_z+.4]) shim();
   color("seagreen") translate([35.5,rows[i],floor_z+.4]) mirror([1,0,0]) shim();
  }
 }
 for(j=[0:1]){
  bit=selected_row==1?show_other[j]:show_old[j];
  color("steelblue") translate([cols[j]+bit_travel*bit,0,bar_z]) codebar();
 }
 for(y=[4,28]){
  color("slategray") translate([0,y,floor_z+7.5]) keeper();
  for(x=[5,27]) color("darkorange") translate([x,y-3,floor_z+8]) key();
 }
}
// Side printing leaves open channel walls vertical; guide-hole roofs bridge 2.9 mm.
module cassette_print(){translate([-1.1,10,2.7]) rotate([90,0,0]) cassette();}
// Side-down flag. Sacrificial end towers anchor 3.6 / 3.8 mm short bridges.
// Clip the one-layer necks at FOOT BOTTOM and LUG TOP, never the side faces.
module flag_print(){translate([1.7,8,2]) rotate([90,0,0]) flag();}
module flag_support(){
 translate([.7,8.3,0]) cube([2,1.2,.96]);
 translate([1.3,8,.8]) cube([.8,.3,.16]);
 translate([.7,-1.5,0]) cube([2,1.2,.96]);
 translate([1.2,-.3,.8]) cube([1,.3,.16]);
}
module supported_flag_print(){union(){flag_print();flag_support();}}
module codebar_print(){translate([1.9,29.5,3.5]) rotate([180,0,0]) codebar();}
module shim_print(){translate([4,2.9,0]) shim();}
module keeper_print(){translate([-2.4,2.8,4.2]) rotate([180,0,0]) keeper();}
module key_print(){translate([1.8,1.5,0]) key();}
module plate(){
 base();
 for(i=[0:1]) translate([40,1+i*14,0]) cassette_print();
 for(i=[0:3]) translate([40+i*10,34,0]) supported_flag_print();
 for(i=[0:1]) translate([40+i*7,47,0]) codebar_print();
 for(i=[0:3]) translate([2+i*17,82,0]) shim_print();
 for(i=[0:1]) translate([2+i*33,94,0]) keeper_print();
 for(i=[0:3]) translate([61+i*6,47,0]) key_print();
}
if(part=="assembly") assembly();
else if(part=="plate") plate();
else if(part=="base") base();
else if(part=="cassette") cassette_print();
else if(part=="flag") flag_print();
else if(part=="flag_support") flag_support();
else if(part=="supported_flag") supported_flag_print();
else if(part=="codebar") codebar_print();
else if(part=="shim") shim_print();
else if(part=="keeper") keeper_print();
else if(part=="key") key_print();
