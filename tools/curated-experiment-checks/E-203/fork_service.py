#!/usr/bin/env python3
"""E-203: finite fork/row service constructions, mm/N; bounded, not calibrated.
AABB solids, piecewise-affine sweeps, inherited frustum paths, support graphs.
No dynamics, contact strength, probabilistic manufacturing or qualified readback.
"""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import importlib.util
import json
import sys

spec = importlib.util.spec_from_file_location('taper', Path(__file__).resolve().parents[1]/'E-202/taper_transfer.py')
t = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = t
spec.loader.exec_module(t)
EPS=1e-9

@dataclass(frozen=True)
class Box:
    x: tuple
    y: tuple
    z: tuple

    def move(self, x=0., y=0., z=0.):
        return Box(tuple(a+x for a in self.x), tuple(a+y for a in self.y), tuple(a+z for a in self.z))

    def grow(self, e):
        return Box(*[(a-e,b+e) for a,b in (self.x,self.y,self.z)])

    def overlap(self, other):
        v=1.
        for a,b in zip((self.x,self.y,self.z),(other.x,other.y,other.z)):
            v*=max(0.,min(a[1],b[1])-max(a[0],b[0]))
        return v


def swept_collision(a,b,delta):
    """Exact open-interval SAT for translation; touching is not penetration."""
    enter,leave=0.,1.
    for aa,bb,d in zip((a.x,a.y,a.z),(b.x,b.y,b.z),delta):
        if abs(d)<EPS:
            if min(aa[1],bb[1])-max(aa[0],bb[0])<=EPS:
                return False
        else:
            p,q=sorted(((bb[0]-aa[1])/d,(bb[1]-aa[0])/d))
            enter=max(enter,p);leave=min(leave,q)
    return leave-enter>EPS


def retained_fork():
    # Existing slabs and their positive-y structural rims, not infinite plates.
    keeper=Box((-2.5,2.5),(.60,1.00),(-1.2,0.))
    cam=Box((-2.5,2.5),(.60,1.00),(4.,5.2))
    # Tab root is wholly between slabs, at every inherited retained z endpoint.
    tab=Box((-.7,.7),(-.4,1.8),(2.45,2.95))
    # z clearance includes ±.30 retained drift plus independent ±.05 tab,
    # jaw face and writer datum errors. Opening is 1.4 mm (2.00..3.40).
    lower=Box((-1.1,1.1),(1.25,1.75),(1.60,2.00))
    upper=Box((-1.1,1.1),(1.25,1.75),(3.40,3.80))
    back=Box((-1.1,1.1),(1.95,2.35),(1.60,3.80))
    # Connector ledges from jaws to back; y gap is outside tab endpoint.
    connectors=[Box((-1.1,1.1),(1.75,2.35),z) for z in ((1.6,2.),(3.4,3.8))]
    jawparts=[lower,upper,back]+connectors
    min_capture=1e9; min_tab_slab=1e9; poses=0
    for state,drift,taberr,jawerr,datum in product((-2.,.6),(-.3,.3),(-.05,.05),(-.05,.05),(-.05,.05)):
        zlo=state+drift+2.45+taberr
        zhi=state+drift+2.95+taberr
        bottom=state+2.+jawerr+datum
        top=state+3.4+jawerr+datum
        min_capture=min(min_capture,zlo-bottom,top-zhi)
        min_tab_slab=min(min_tab_slab,zlo-.05,3.95-zhi)
        assert zlo>=bottom-EPS and zhi<=top+EPS
        poses+=1
    # Nominal axial jaws placed across the positive-y rim repeat the conflict.
    inboard=[Box(j.x,(.65,.95),j.z) for j in (lower,upper)]
    control=max(j.move(z=s).overlap(p) for j in inboard for s in (-2.,.6) for p in (keeper,cam))
    assert control>0
    # Attempt a real keeper gate: two slots around the low/high collar,
    # separated by a central web. Gate spans y1.2..1.6 and x±1.3. It fits
    # outside the plates, but overlaps the already installed fork jaws.
    gate=[Box((-1.3,1.3),(1.2,1.6),z)
          for z in ((-.3,.1),(1.3,2.7),(3.9,4.3))]
    gate_collision=max(g.overlap(j.move(z=state)) for g in gate
                       for j in jawparts for state in (-2.,.6))
    assert gate_collision>0
    # With .45 nominal axial lost motion each way, active driving needs
    # f=q+.45 on set and f=q-.45 on reset, NOT only a 2.6-mm head stroke.
    drive_range=(-2.-.45,.6+.45)
    # Independent axial packing necessary condition for close-following jaws.
    # Full retained q range 3.2; slab translations consume .1; tab .5 plus two
    # .4 jaws and two .05 clearances consume 1.4 before jaw-size error.
    free_axial=3.9-3.2
    required_axial=.5+2*.4+2*.05
    assert required_axial>free_axial
    # Outboard fork extends in +y; reverse this exact sweep to withdraw.
    # Expand both solids by .05, extra .05 relative y registration on fork.
    collision_checks=0
    for state in (-2.,.6):
        for part in jawparts:
            for plate in (keeper,cam):
                a=part.grow(.05).move(y=-.05,z=state)
                assert not swept_collision(a,plate.grow(.05),(0,3.,0))
                collision_checks+=1
    # tab overlap under ±.05 edge shifts on each part plus ±.05 y datum.
    bearing=min(1.75-.05,1.8-.05)-max(1.25+.05+.05,-.4+.05)
    assert bearing>=.35-EPS
    # ±.65 float rail stops; worst .05 errors on each stop/reference leave .55.
    # A home centering cam is NOT credited: arbitrary prior fork offset retained.
    # Wide funnel: half opening 1.90, narrows to .90 over .80 approach travel.
    rail=.65-.1
    max_pin=max(abs(v) for h in t.horizontal(.8) for q in (-2.3,.9)
                for v in t.bounds(t.Pin(h[0],.2,5.4,.4),q,t.make_slots(h,nominal=.8),h[3]))
    # Incoming pin offset and prior fork offset can have opposite signs.
    mouth_reserve=1.90-.05-(.7+.05)-(max_pin+rail+.05)
    assert mouth_reserve>=-EPS
    # Pocket side slack after independent face/datum error: no zero-play guide.
    side_reserve=.9-.05-(.7+.05)-.05
    assert side_reserve>.0
    # Floating carrier uses two separated T shoes, heads 1.2 x .6 x .4,
    # groove height .8, .2-wide neck, x endpoints ±.65. Reactions go via rail roofs,
    # side webs and z-drive; bearing friction/couple remain force obligations.
    # Wide funnel outer width 4.6 (3.8 opening + .4 walls each), swept ±.65;
    # housing walls .4 each, four adverse edges .05.
    head_width=4.6+1.3+.8+.2
    # Make the float guide finite behind the fork. Two T shoes run in x;
    # split roofs capture them in z. No spring recenters or locks this slide.
    guide=[]; shoes=[]; necks=[]
    for y in (2.6,4.0):
        shoes.append(Box((-.6,.6),(y-.3,y+.3),(1.2,1.6)))
        necks.append(Box((-.6,.6),(y-.1,y+.1),(1.6,2.2)))
        guide.append(Box((-1.5,1.5),(y-.5,y+.5),(.6,1.0)))
        guide.extend(Box((-1.5,1.5),yy,(1.8,2.2))
                     for yy in ((y-.5,y-.25),(y+.25,y+.5)))
        guide.extend(Box((-1.5,1.5),yy,(1.0,1.8))
                     for yy in ((y-.5,y-.45),(y+.45,y+.5)))
        guide.extend(Box(xx,(y-.5,y+.5),(1.0,1.8))
                     for xx in ((-1.65,-1.25),(1.25,1.65)))
    # Upper integral spine joins necks to fork back; cantilever strength unknown.
    spine=Box((-.6,.6),(1.95,4.1),(2.2,2.6))
    guide_clear=0
    for dx in (-.65,0.,.65):
        for moving in shoes+necks+[spine]:
            for fixed in guide:
                assert moving.move(x=dx).overlap(fixed)==0
                guide_clear+=1
    # The narrow roof/neck clearances are nominal; ±.05 each consumes the
    # .15 nominal side reserve to .05, z .20 reserve to .10. Tilt is unmodelled.
    # No head envelope can be hidden inside the old 5.20-mm row allocation.
    resident_row=4.0+1.8+.2  # cam rear rim, positive tab end, relative edge bounds
    row_allocation=4.0+4.5+.2 # actual guide rear edge; writer only, not resident
    row_with_rear_wall=row_allocation
    return dict(retained_capture_poses=poses,min_capture_gap=min_capture,
        min_tab_slab_gap=min_tab_slab,inboard_penetration_mm3=control,
        available_axial=free_axial,required_axial=required_axial,gate_fork_collision_mm3=gate_collision,nominal_head_drive_range=drive_range,
        outboard_sweeps=collision_checks,min_tab_bearing_y=bearing,
        max_pin_offset=max_pin,float_half_travel=rail,
        mouth_reserve=mouth_reserve,side_reserve=side_reserve,
        head_x_allocation=head_width,resident_row_allocation=resident_row,guide_nominal_checks=guide_clear,row_y_lower_bound=row_allocation,
        row_with_rear_wall=row_with_rear_wall)


def transfer_with_float():
    cases=0; max_shift=0.; max_x=0.; min_cover=1e9
    # Explicit inherited clipped vertices, retain the carriage position as a
    # state variable. Carriage can follow x; .05 relative datum leaves .50 travel.
    for h in t.horizontal(.8):
        for dl,dlo,dup,dt,dtip in product((-.05,.05),repeat=5):
            p=t.Pin(h[0],.2+dtip,5.4+dl,.4+dt)
            slots=t.make_slots(h,dlo,dup,.8)
            ks=t.knots(p,slots,-2.3,.9)
            for grid in (ks,ks[::-1]):
                for x in t.bounds(p,grid[0],slots,h[3]):
                    initial=x
                    for q in grid:
                        lo,hi=t.bounds(p,q,slots,h[3]);x=min(hi,max(lo,x))
                        assert abs(x)+.05<=.55+EPS
                        assert t.vertices_clear(p,q,x,h[3],slots)>=-EPS
                        max_shift=max(max_shift,abs(x-initial));max_x=max(max_x,abs(x))
                        min_cover=min(min_cover,max(t.shank(p,q,s) for s in slots))
            # Use inherited entry check: projecting endpoints alone hides jumps.
            assert t.trace(p,slots,h[3],-2.3,.9)['failure'] is None
            cases+=1
    assert abs(max_shift-.2225)<EPS
    return dict(cases=cases,max_shift=max_shift,max_x=max_x,min_shank_cover=min_cover)


def retention_direct():
    # Direct slider's outboard tab x=[-1.1,-.5]+q, y=[1.2,1.8]. A removable
    # row comb has a finite slot [-1.3,-.3] in x; slots repeat at 5.08 pitch.
    # Insert/remove comb along y only at q=0, keeping writer capture until closed.
    # Same physical slot cannot lock a retracted q=-.75; explicit fault control.
    retained=[];min_overlap=1e9;fail=False
    for left,right,tab_l,tab_r,datum,nose,rack in product((-.05,.05),repeat=7):
        qlo=(-1.3+left)-(-1.1+tab_l)+datum
        qhi=(-.3+right)-(-.5+tab_r)+datum
        assert qlo<=0<=qhi
        retained.extend((qlo,qhi))
        min_overlap=min(min_overlap,.9+nose+qlo-(.4+rack))
        fail |= -.75<qlo
    # Finite y comb slab [1.3,1.7], tab [1.2,1.8]; ≥.25 bearing under errors.
    bearing=(1.7-.05)-(1.3+.05)-.05
    assert min_overlap>=.05-EPS and fail
    # Fully retracted command held by head, not comb: worst relative tip/rack.
    withdrawn_gap=(.4-.05)-(.9+.05-.75)
    assert withdrawn_gap>.0
    # Bilateral x head acquisition: a U fork open in y has x slot width 1.5,
    # tab width .6, half slack .45: covers retained ±.35 with two .05 faces.
    acquire=.75-(.3+.05)-.35-.05
    assert acquire>=-EPS
    # Finite direct jaws x=[-1.95,-1.55] and [-.05,.35] around tab center -.8,
    # opening [-1.55,-.05], y=[1.95,2.35], tab extended to y=2.4. This writer
    # uses the outer tab; its back bridge blocks same-plane acquisition.
    # Comb uses tab inner segment y 1.3..1.7; writer uses outer segment.
    # The tab cannot pass through E-201's solid +y post. Cut a real window
    # x[-2.05,-.05], z[-2.2,.2]; retain .45/.20 wide pillars and an upper
    # connecting bridge. These thin frame ligaments have no strength pass.
    postparts=[Box(xx,(1.95,2.35),zz) for xx,zz in (
        ((-2.5,-2.05),(-46.,.6)), ((-.05,.15),(-46.,.6)),
        ((-2.05,-.05),(-46.,-2.2)), ((-2.05,-.05),(.2,.6)))]
    tab=Box((-1.1,-.5),(1.2,2.4),(-2.,0.))
    for q in (-.75,0.,.35):
        assert all(tab.move(x=q).grow(.10).overlap(p)==0 for p in postparts)
    # Finite U back bridge closes the x force path behind the tab. Its volume
    # intersects the next row's grounded -y post even at nominal dimensions.
    back=Box((-1.95,.35),(2.55,2.95),(-2.,0.))
    neighbor=Box((-2.5,.15),(5.08-2.35,5.08-1.95),(-46.,0.))
    collision=back.overlap(neighbor)
    assert collision>0
    # This rear bridge is the construction's failed function, not a silently
    # omitted guide. Front and rear alternatives are not tested here.
    return dict(direct_writer_bridge_collision_mm3=collision,retained_q=[min(retained),max(retained)],min_rack_overlap=min_overlap,
        comb_bearing_y=bearing,withdrawn_rack_gap=withdrawn_gap,
        fork_acquisition_reserve=acquire,retracted_comb_blocked=fail,
        writer_outer_y=2.35,tab_outer_y=2.4)


def service(n=16):
    # Intact 40-cell, 203.2-mm row cassette. Use asymmetric occupied bounds:
    # mirroring the +2.40 tab onto the other side would invent a pitch failure.
    # Tops ±2.40 with .10 outer error retain .08 inter-row clearance.
    pitch=5.08;length=40*pitch
    cases=[]
    for lo,hi,name in ((-2.35,2.35,'bare_direct_body'),
                       (-2.35,2.40,'direct_body_with_tab'),
                       (-2.60,2.60,'inherited_5.20_row'),
                       (-4.0,1.8,'taper_tab_resident_row')):
        # .05 face error + .05 independent row datum = .10 per outer edge.
        row=Box((-2.54,length-2.54),(lo,hi),(-48.,44.)).grow(.10)
        neighbor=row.move(y=pitch)
        hit=swept_collision(row,neighbor,(length,0.,0.))
        gap=pitch-(hi-lo+.2)
        # A collision of conservative envelopes is not a solid collision.
        # Construct edge rails for each listed package to distinguish the two.
        rail=Box(row.x,(hi-.4,hi),(-48.,-46.)).grow(.10)
        near=Box(row.x,(lo,lo+.4),(-48.,-46.)).grow(.10).move(y=pitch)
        actual=rail.overlap(near)
        assert (actual>EPS)==(gap<0)
        if not hit:
            assert all(row.move(x=length*k/n).overlap(neighbor)==0 for k in range(n+1))
        cases.append(dict(name=name,resident_width=hi-lo,gap=gap,blocked=hit,rail_overlap_mm3=actual))
    # Support topology follows the cassette, not the fixed main frame. The
    # carriage rails overlap external dock rails continuously along extraction.
    # At translation u, cabinet contact [u,L] and dock [L,L+u] partition row.
    for u in (length*k/n for k in range(n+1)):
        supported=max(0.,length-u)+min(length,u)
        assert abs(supported-length)<EPS
    # Fault: remove row lock when one column is withdrawn, the other 39 remain
    # seated. Ground->cassette->slider->rack path is absent for that column.
    supports=lambda seated,head: [s or h for s,h in zip(seated,head)]
    ok=supports([True]*40,[False]*40)
    faulty=supports([True]*39+[False],[False]*40)
    rescued=supports([True]*39+[False],[False]*39+[True])
    assert all(ok) and not all(faulty) and all(rescued)
    return dict(rows=cases,sweep_nodes=n+1,locked_row_has_support=all(ok),
        jammed_row_without_traveling_support=all(faulty),
        traveling_recovery_support_needed=not all(faulty),dock_extension_mm=length)


def forces():
    # Local axial limiter MUST be downstream of the shared actuator for every
    # simultaneously driven fork. No physical limiter or tip allowable is granted.
    gain=t.contact_gain(1.,.3,.5)
    # Do not assign a shank bending limit or an axial punch capacity to
    # frustum-lip contact: its damage law is not supplied by E-202.
    # Eccentric tab force loads float guide moment: at offset 1.8 mm, rail span
    # 1.4 mm, abs reaction sum ≥F*max(1,2e/L), friction adds μ*sum to R.
    ratio=max(1.,2*1.8/1.4)
    far=(1.5-2.6)/1.4;near=1.-far
    assert abs(near*2.6+far*4.-1.5)<EPS
    assert abs(abs(near)+abs(far)-ratio)<EPS
    # F=G*(R0+mu_g*ratio*F) => finite positive branch only G*mu_g*ratio<1.
    feedback=[dict(mu=mu,loop_gain=gain*mu*ratio,
                   finite_branch=gain*mu*ratio<1.) for mu in (.05,.1,.2)]
    sensitivity=[gain*.1*max(1.,2*e/L) for e,L in product((1.55,2.05),(1.3,1.5))]
    assert min(sensitivity)>1.
    return dict(mu01_loop_sensitivity=[min(sensitivity),max(sensitivity)],taper_gain=gain,guide_reaction_ratio=ratio,
                guide_friction_feedback=feedback,
                local_limiter='not constructed: no force or machine pass')


def main():
    # Collision implementation controls, including an interior collision missed
    # by endpoints and grazing contact, validate the continuous sweep function.
    a=Box((0.,1.),(0.,1.),(0.,1.)); b=a.move(x=2.)
    assert swept_collision(a,b,(4.,0.,0.))
    assert not swept_collision(a,b.move(y=1.),(4.,0.,0.))
    assert a.overlap(a)==1 and a.overlap(b)==0
    result=dict(evidence='finite bounded geometry and conditional force bounds; self-review',
        fork=retained_fork(),transfer=transfer_with_float(),direct=retention_direct(),
        service=service(),forces=forces())
    for n in (1,64,256):
        assert service(n)['rows']==result['service']['rows']
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
