// E-303 B2-10: packaging concept, NOT a printable/high-voltage-qualified assembly.
// Units mm. Functional thread MUST be reused from E-295, not this envelope.
// Render: openscad -o B-concept.png --imgsize=1200,900 --viewall --autocenter B-floating-electrode.scad
// Housing is sectioned for visibility; purchased films exaggerated only in SVG.
$fn=96;
carrier_d=10; active_ro=4.5; active_ri=1.8; sector_gap=0.4;
foil_t=0.035; dielectric_t=0.012; output_film_t=0.025;
air_gap=0.050; rotor_top=2;
output_film_z=rotor_top+dielectric_t+air_gap;
show_housing=true; section_housing=true; explode=0;
module disc(d,h,z){translate([0,0,z]) cylinder(d=d,h=h);}
module annulus(ro,ri,h,z){difference(){disc(2*ro,h,z);disc(2*ri,h+0.02,z-0.01);}}
module input_hub(){union(){disc(carrier_d,rotor_top-foil_t,0);disc(3,10,-10);disc(5,0.8,-3);}}
module output_hub(){union(){disc(3.2,1,output_film_z+output_film_t);disc(2,12-output_film_z-output_film_t-1,output_film_z+output_film_t+1);disc(4.4,0.8,8);disc(3.2,12,12);}}
module housing(){difference(){translate([-9,-7,-4])cube([18,14,15]);disc(10.4,5,-1);disc(3.3,4,-4.01);disc(2.3,7.1,4);disc(5.2,0.9,-3.05);disc(4.6,0.9,7.95);for(x=[-7,7])translate([x,0,3.5])rotate([90,0,0])cylinder(d=2.3,h=16,center=true);}}
// Structural bodies. Two separate journal/thrust systems; no hidden ball bearings.
color("cornflowerblue")input_hub();
color("lightsteelblue")translate([0,0,explode*2])output_hub();
// Both copper electrodes rotate on input; center hole and split channel are real.
for(s=[-1,1])color(s<0?"darkorange":"goldenrod")translate([0,0,explode])intersection(){annulus(active_ro,active_ri,foil_t,rotor_top-foil_t);translate([s<0?-10:sector_gap/2,-10,rotor_top-foil_t])cube([10-sector_gap/2,20,foil_t]);}
color([0.3,0.8,0.7,0.7])translate([0,0,explode*1.4])disc(carrier_d,dielectric_t,rotor_top);
color("silver")translate([0,0,explode*1.8])disc(9,output_film_t,output_film_z);
// Two local rotating copper tracks. These clearances are geometry, not HV ratings.
for(z=[-9,-6])color("darkorange")disc(3.07,1,z);
// Stationary flexible brushes and two insulated internal links are not solid modeled.
// Counted in SVG/BOM. Ordinary insulated leads connect tracks to matching sectors.
if(show_housing)color([0.5,0.5,0.5,0.35])difference(){housing();if(section_housing)translate([-10,-10,-5])cube([20,10,30]);}
