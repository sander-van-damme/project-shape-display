// E-018 four-plane mask-generator coupon; CAD only.
$fn = 48;
PITCH=5.08; N=5; FIELD=N*PITCH;
FRAME_X=40; FRAME_Y=40; FRAME_T=3;
PLANE_X=34; PLANE_Y=34; PLANE_T=0.8; PLANE_GAP=1.2;
APERTURE=3; FID_D=2; FID_OFFSET=15; DATUM_W=2; DATUM_L=6;
PORT_W=4; PORT_T=1; PORT_H=0.8; PORT_X=-10.16;
READER_STANDOFF=2; DUMMY_T=2;
WRITER_INSERTION=1.0; WRITER_PARK_CLEARANCE=0.2;
READER_BODY_T=4; READER_WINDOW_X=0; READER_WINDOW_Y=0; READER_WINDOW_DEPTH=0.4;
function cell(i)=(i-(N-1)/2)*PITCH;
function plane_z(p)=FRAME_T+0.5+p*(PLANE_T+PLANE_GAP);
function tab_center_y()=-PLANE_Y/2-PORT_T/2;
function writer_center_y(engaged=true)=engaged ? tab_center_y() : -FRAME_Y/2-PORT_T/2-WRITER_PARK_CLEARANCE;

module fiducials() for (xy=[[-FID_OFFSET,-FID_OFFSET],[FID_OFFSET,FID_OFFSET]])
    translate([xy[0],xy[1],0]) cylinder(d=FID_D,h=FRAME_T+0.4,center=true);
module frame() {
    difference() {
        cube([FRAME_X,FRAME_Y,FRAME_T],center=true);
        fiducials();
        translate([0,FRAME_Y/2-DATUM_L/2,0]) cube([DATUM_W,DATUM_L,FRAME_T+0.4],center=true);
        cube([APERTURE,APERTURE,FRAME_T+0.4],center=true);
    }
}
module plane(p=0) {
    difference() {
        cube([PLANE_X,PLANE_Y,PLANE_T],center=true);
        for (i=[0:N-1]) for (j=[0:N-1])
            translate([cell(i),cell(j),0]) cube([APERTURE,APERTURE,PLANE_T+0.4],center=true);
    }
    translate([PORT_X,-PLANE_Y/2-PORT_T/2,0])
        cube([PORT_W,PORT_T,PLANE_T],center=true);
}
module writer_interface(engaged=true) for (p=[0:3])
        // Engaged tongue is registered to its matching tab for the declared 1 mm insertion.
        translate([PORT_X,writer_center_y(engaged),plane_z(p)])
        cube([PORT_W,PORT_T,PORT_H],center=true);
function top_plane_z()=plane_z(3)+PLANE_T/2;
function reader_bottom_z()=top_plane_z()+READER_STANDOFF;
module reader_target() translate([0,0,reader_bottom_z()+READER_BODY_T/2])
    // Lower face is above the upper carrier; window is at that face.
    difference() { cube([8,8,READER_BODY_T],center=true); translate([READER_WINDOW_X,READER_WINDOW_Y,-READER_BODY_T/2+READER_WINDOW_DEPTH/2]) cube([APERTURE,APERTURE,READER_WINDOW_DEPTH],center=true); }
module dummy_neighbour(side="N") {
    if (side=="N") translate([0,FRAME_Y,DUMMY_T/2]) cube([FRAME_X,FRAME_Y,DUMMY_T],center=true);
    if (side=="S") translate([0,-FRAME_Y,DUMMY_T/2]) cube([FRAME_X,FRAME_Y,DUMMY_T],center=true);
    if (side=="E") translate([FRAME_X,0,DUMMY_T/2]) cube([FRAME_Y,FRAME_X,DUMMY_T],center=true);
    if (side=="W") translate([-FRAME_X,0,DUMMY_T/2]) cube([FRAME_Y,FRAME_X,DUMMY_T],center=true);
}
module assembly() {
    color("lightgray") frame();
    for (p=[0:3]) translate([0,0,plane_z(p)]) color("orange") plane(p);
    color("blue") writer_interface(); color("red") reader_target();
    for (s=["N","E","S","W"]) color("gray") dummy_neighbour(s);
}
part="assembly";
if (part=="frame") frame(); else if (part=="plane") plane(0);
else if (part=="reader_target") reader_target(); else if (part=="writer_interface") writer_interface();
else if (part=="dummy_neighbour") dummy_neighbour("N"); else assembly();
echo(str("E018 field span = ",FIELD," mm"));
echo(str("E018 aperture web = ",PITCH-APERTURE," mm"));
