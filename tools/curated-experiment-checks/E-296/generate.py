#!/usr/bin/env python3
"""E-296: engineering CAD for a MIN-gated single sliding hex sleeve.

Units mm. This is precision-mechanism research CAD, NOT print-ready or a
validated mechanism. Screws and hollow terrain pins are labelled ENVELOPES;
their functional thread remains the tested E-295 profile, not a new thread.
Run: python generate.py; python validation.py. CadQuery 2.6 / OCP required.
"""
from __future__ import annotations
import json, math
from functools import lru_cache
from pathlib import Path
import cadquery as cq

HERE = Path(__file__).resolve().parent
CAD = HERE / "cad"
P = 5.08
D = dict(pitch=P, pin_width=4.4, screw_diameter=3.2,
         male_af=1.8, female_af=1.95, sleeve_od=3.0,
         sleeve_bottom=-.6, sleeve_top=4.1, sleeve_flange_bottom=3.7,
         sleeve_flange_od=4.2, mouth_chamfer=.375, mouth_af=2.70,
         lower_flange_top=-.2, lower_flange_bottom=-.6, lower_flange_od=3.4,
         row_id=3.2, row_od=4.7, row_thickness=.3,
         column_id=2.4, column_od=4.7, column_thickness=.4,
         roof_z=4.1, selector_stroke=1.4, row_return_lash=.2,
         input_hex_bottom=-1.9, input_hex_top=3.3,
         output_hex_bottom=4.7, output_hex_top=7.4,
         spring_od=3.9, spring_wire=.2, spring_active_turns=5,
         spring_total_turns=7, spring_free_length=3.716,
         spring_G=79000.0, journal_od=2.0, journal_bore=2.02,
         journal_length=4.0, axial_gap_each_face=.02, axial_endplay_total=.04)
COLORS = {"input":(.30,.35,.40), "output":(.42,.46,.50),
          "sleeve":(.88,.55,.16), "clip":(.55,.30,.05),
          "spring":(.65,.64,.60), "row":(.12,.47,.72),
          "column":(.77,.20,.25), "frame":(.74,.77,.80),
          "pin_envelope":(.40,.69,.53), "screw_envelope":(.42,.46,.50)}

def cyl(d, z, h):
    return cq.Solid.makeCylinder(d/2, h, cq.Vector(0,0,z))

def box(x0,x1,y0,y1,z0,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))

def hexwire(af,z):
    rr=af/math.sqrt(3)
    vv=[cq.Vector(rr*math.cos(i*math.pi/3),rr*math.sin(i*math.pi/3),z)
        for i in range(6)]
    return cq.Wire.makePolygon(vv+[vv[0]])

def hexprism(af,z,h):
    return cq.Solid.extrudeLinear(hexwire(af,z), [], cq.Vector(0,0,h))

@lru_cache(maxsize=None)
def sleeve():
    s=cyl(D["sleeve_od"],-.6,4.7).fuse(cyl(4.2,3.7,.4)).fuse(cyl(3.4,-.6,.4))
    s=s.cut(hexprism(1.95,-.7,4.8))
    lead=cq.Solid.makeLoft([hexwire(1.95,4.1-D["mouth_chamfer"]),hexwire(D["mouth_af"],4.1)])
    s=s.cut(lead)
    return s.clean()

@lru_cache(maxsize=None)
def input_shaft():
    # Two collars sandwich a stationary 4-mm journal plate with .02 mm clearance
    # per face. These are support features, not the shared transmission design.
    return (hexprism(1.8,-1.9,5.2).fuse(cyl(2,-6.02,4.04))
            .fuse(cyl(3.6,-6.42,.4)).fuse(cyl(3.6,-1.98,.4))).clean()

@lru_cache(maxsize=None)
def output_shaft():
    return (hexprism(1.8,4.7,2.7).fuse(cyl(2,7.4,4.6))
            .fuse(cyl(3.6,7.08,.4)).fuse(cyl(3.6,11.52,.4))
            .fuse(cyl(2,12,1.0))).clean()

@lru_cache(maxsize=None)
def output_screw_envelope():
    # One integral rotating body. Merely touching separate head/screw faces
    # would not define a torque joint. This union reserves an integral blank;
    # production of the exact E-295 thread on that blank is NOT qualified.
    return output_shaft().fuse(cyl(3.2,13,23.2)).clean()

@lru_cache(maxsize=None)
def spring(bottom,top):
    # Five helical active turns, plus two flat closed end turns. The short
    # transitions into the end turns are schematic. Solid height=7*.2=1.4.
    w=.2; rr=1.85
    h=top-bottom-.4
    path=cq.Wire.makeHelix(h/5,h,rr).translate((0,0,bottom+.2))
    helix=(cq.Workplane("XZ").workplane(offset=0)
           .center(rr,bottom+.2).circle(w/2).sweep(path,isFrenet=True).val())
    rings=[]
    for z in [bottom+.1,top-.1]:
        rings.append(cq.Solid.makeTorus(rr,w/2,cq.Vector(0,0,z)))
    # CAD compound keeps the schematic closed turns identifiable.
    return cq.Compound.makeCompound([helix]+rings)

def row_comb(y,r):
    s=box(-5.8,10.0,y-.4,y+.4,r,r+.3)
    for x in [0,P]:
        s=s.fuse(cyl(4.7,r,.3).translate((x,y,0)))
    for x in [0,P]:
        s=s.cut(cyl(3.2,r-.01,.32).translate((x,y,0)))
    return s.clean()

def split_row(y,r):
    """Two metal half-combs closed around integral-flange sleeves.

    Exterior bridge clamps close the longitudinal split. Fastener holes are
    omitted from the precision fixture; positive fastening is required before
    load. The vertical shoe is one of these external bridge clamps and keeps
    the row horizontal throughout its stroke.
    """
    s=row_comb(y,r)
    halves=[s.intersect(box(-6,10.1,y-3,y-.02,r-.01,r+.31)),
            s.intersect(box(-6,10.1,y+.02,y+3,r-.01,r+.31))]
    shoe=box(-5.25,-3.35,y-.8,y+.8,r+.3,r+3.3)
    end=box(7.8,9.7,y-.8,y+.8,r+.3,r+3.3)
    return halves,shoe,end

def column_comb(x,c):
    z=4.1+c
    s=box(x-.4,x+.4,-5.8,10.0,z,z+.4)
    for y in [0,P]:
        s=s.fuse(cyl(4.7,z,.4).translate((x,y,0)))
    for y in [0,P]:
        s=s.cut(cyl(2.4,z-.01,.42).translate((x,y,0)))
    return s.clean()

def journal_plate(z):
    s=box(-5.5,8.28,-5.5,8.28,z,z+4)
    for x in [0,P]:
        for y in [0,P]:
            s=s.cut(cyl(D["journal_bore"],z-.01,4.02).translate((x,y,0)))
    return s.clean()

@lru_cache(maxsize=None)
def frame_parts():
    # Split bearing plates allow the captive collars to be assembled. The
    # .08-mm saw/split gaps are represented explicitly, never sealed bearings.
    parts={}
    for label,z in [("lower",-6),("upper",7.5)]:
        plate=journal_plate(z)
        ycuts=[(-5.5,-.04),(.04,P-.04),(P+.04,8.28)]
        for k,(lo,hi) in enumerate(ycuts):
            parts[f"frame_{label}_split_{k}"]=plate.intersect(box(-6,9,lo,hi,z-.01,z+4.01))
    # Independent comb-end guides at opposite outer tile boundaries. Both are
    # constrained in x/y and free only in z. The demonstration frame is larger
    # than the repeating 10.16 x 10.16-mm active cell tile.
    for j,y in enumerate([0,P]):
        guide=box(-5.5,-3.1,y-1.0,y+1.0,-2,4.8)
        guide=guide.cut(box(-5.27,-3.33,y-.82,y+.82,.28,4.72))
        guide=guide.cut(box(-5.6,-3.0,y-.42,y+.42,-.02,1.72))
        parts[f"frame_row_guide_{j}"]=guide.clean()
        guide=box(7.55,9.95,y-1.,y+1.,-2,4.8)
        guide=guide.cut(box(7.78,9.72,y-.82,y+.82,.28,4.72))
        guide=guide.cut(box(7.4,10.1,y-.42,y+.42,-.02,1.72))
        parts[f"frame_row_distal_guide_{j}"]=guide.clean()
    for i,x in enumerate([0,P]):
        guide=box(x-1,x+1,-5.5,-3.1,.9,7.5)
        guide=guide.cut(box(x-.82,x+.82,-5.27,-3.33,1.08,5.52))
        guide=guide.cut(box(x-.42,x+.42,-5.6,-3.0,4.08,5.92))
        parts[f"frame_column_guide_{i}"]=guide.clean()
        guide=box(x-1,x+1,7.55,9.95,.9,7.5)
        guide=guide.cut(box(x-.82,x+.82,7.78,9.72,1.08,5.52))
        guide=guide.cut(box(x-.42,x+.42,7.4,10.1,4.08,5.92))
        parts[f"frame_column_distal_guide_{i}"]=guide.clean()
    # Upper terrain-guide strips: square openings retain pin antirotation;
    # longitudinal pin guidance is an envelope, not a full-travel prototype.
    g=box(-5.5,8.38,-5.5,8.38,19,21)
    for x in [0,P]:
        for y in [0,P]:
            g=g.cut(box(x-2.3,x+2.3,y-2.3,y+2.3,18.9,21.1))
    parts["frame_pin_guide"]=g.clean()
    parts["frame_pin_guide_upper"]=g.translate((0,0,10)).clean()
    for x,y in [(-4.8,8.0),(8.0,-4.8),(8.0,8.0)]:
        parts[f"frame_post_{x}_{y}"]=box(x-.35,x+.35,y-.35,y+.35,-2,29)
    return parts

def q_nominal(r,c): return min(c,r+.2)

def phase_block_q(phi_degrees=30):
    # At the first axial intersection the .375-mm 45-degree lead-in permits
    # extra entry. This is the centered polygon-support contact calculation.
    phase=abs(((phi_degrees+30)%60)-30)
    required_af=2*(1.8/math.sqrt(3))*math.cos(math.radians(30-phase))
    return .6+D["mouth_chamfer"]-max(0,(required_af-1.95)/2)

def model(rows=(1.4,0),cols=(1.4,0),blocked=False,include_springs=True):
    parts={}
    for name,s in frame_parts().items(): parts[name]=(s,"frame")
    for j,y in enumerate([0,P]):
        halves,shoe,end=split_row(y,rows[j])
        for h,s in enumerate(halves):parts[f"row_{j}_half_{h}"]=(s,"row")
        parts[f"row_{j}_guide_shoe"]=(shoe,"row")
        parts[f"row_{j}_end_clamp"]=(end,"row")
    for i,x in enumerate([0,P]):
        parts[f"column_{i}"]=(column_comb(x,cols[i]),"column")
        # This exterior shoe is rigidly attached to the column bridge below
        # the comb face. Its full 3-mm height remains guided at both end states.
        parts[f"column_{i}_guide_shoe"]=(box(x-.8,x+.8,-5.25,-3.35,1.1+cols[i],4.1+cols[i]),"column")
        parts[f"column_{i}_distal_shoe"]=(box(x-.8,x+.8,7.8,9.7,1.1+cols[i],4.1+cols[i]),"column")
    poses={}
    for j,y in enumerate([0,P]):
        for i,x in enumerate([0,P]):
            cell=f"{i}_{j}"; r=rows[j]; c=cols[i]
            q=q_nominal(r,c)
            phi=0
            if blocked and i==j==0: q=phase_block_q();phi=30
            poses[cell]=dict(row=r,column=c,q=q,output_phase=phi,
                             output_overlap=max(0,q-.6))
            for name,s in [("input",input_shaft()),("output",output_screw_envelope()),
                           ("sleeve",sleeve())]:
                if name=="sleeve": s=s.translate((0,0,q))
                if name=="output":s=s.rotate((0,0,0),(0,0,1),phi)
                parts[f"{name}_{cell}"]=(s.translate((x,y,0)),name)
            if include_springs:
                parts[f"spring_{cell}"]=(spring(.3+r,3.7+q).translate((x,y,0)),"spring")
            # The demonstrated pin is 4.4 mm square and hollow with the exact
            # E-295 upper 3.52-mm square bore. Lower functional 6-mm thread
            # is represented by a 3.55-mm clearance ENVELOPE, no fit claim.
            pin=(box(-2.2,2.2,-2.2,2.2,15,45)
                 .cut(box(-1.76,1.76,-1.76,1.76,14.9,44.6)))
            parts[f"pin_envelope_{cell}"]=(pin.translate((x,y,0)),"pin_envelope")
    return parts,poses

def assembly(parts,name):
    a=cq.Assembly(name=name)
    for key,(shape,kind) in parts.items():
        a.add(shape,name=key,color=cq.Color(*COLORS[kind]))
    return a

def main():
    CAD.mkdir(parents=True,exist_ok=True)
    variants={"matrix_R10_C10":((1.4,0),(1.4,0),False),
              "matrix_phase_blocked":((1.4,0),(1.4,0),True)}
    for r in [0,1]:
        for c in [0,1]:
            variants[f"truth_R{r}C{c}"]=((r*1.4,)*2,(c*1.4,)*2,False)
    info={"dimensions_mm":D,"states":{},"cadquery_version":cq.__version__,
          "evidence":"engineering BREP CAD only; no physical qualification",
          "assembly_sequence":[
              "Place input shafts into split lower journal plates; close plate halves.",
              "Place coils over the 3.4-mm integral lower flanges from below (3.5-mm coil ID, .05-mm nominal radial installation clearance).",
              "Slide sleeve-and-spring pairs onto permanent input hex splines.",
              "Close two row-comb halves radially around each row between integral lower flanges and coil lower seats.",
              "Clamp both comb halves together at both outside ends, using rigid exterior bridge clamps; fixture fastener detail remains to be specified.",
              "Install column roof combs above sleeve flanges.",
              "Insert output shafts downward through roofs, then close split upper journals.",
              "Install terrain pins and guide frame; use established E-295 functional threads."]}
    for name,(rows,cols,blocked) in variants.items():
        parts,poses=model(rows,cols,blocked)
        a=assembly(parts,name)
        a.export(str(CAD/f"{name}.step"))
        info["states"][name]=poses
        if name=="matrix_R10_C10":
            bb=cq.Compound.makeCompound([s for s,k in parts.values()]).BoundingBox()
            info["full_fixture_envelope_mm"]={"x":[bb.xmin,bb.xmax],
                "y":[bb.ymin,bb.ymax],"z":[bb.zmin,bb.zmax],
                "size":[bb.xlen,bb.ylen,bb.zlen]}
    # Standalone source geometry in its engineering datum, not arranged for print.
    for name,shape in [("sliding_sleeve",sleeve()),
                       ("input_head",input_shaft()),("integral_output_screw_envelope",output_screw_envelope()),
                       ("split_row_comb",cq.Compound.makeCompound(split_row(0,0)[0])),
                       ("column_roof",column_comb(0,0))]:
        cq.exporters.export(shape,str(CAD/f"part_{name}.step"))
    (HERE/"cad_manifest.json").write_text(json.dumps(info,indent=2)+"\n")
    print(json.dumps({"assemblies":len(variants),"parts":5,"directory":"cad",
                      "blocked_q_mm":phase_block_q()},indent=2))

if __name__=="__main__": main()
