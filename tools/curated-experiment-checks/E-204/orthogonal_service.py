#!/usr/bin/env python3
"""E-204: underside writer, common gate and traveling rescue.
Finite rectangular solids in mm; explicit epistemic bounds, no calibrated yield.
Run directly. JSON is disposable. No contact dynamics or hardware qualification.
"""
import importlib.util
from pathlib import Path
import sys
import json
from itertools import product

spec = importlib.util.spec_from_file_location('fork_service', Path(__file__).resolve().parents[1]/'E-203/fork_service.py')
f = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = f
spec.loader.exec_module(f)
Box, sweep = f.Box, f.swept_collision
P = 5.08
L = 40*P
EPS = 1e-9


def frame():
    # Spring/spine and old seated-stop deleted: direct command + comb replaces them.
    # Unwindowed posts; bridges remain E-198 geometry with expanded y span.
    out = [Box((-2.5,.15), y, (-46,0)) for y in ((-2.35,-1.95),(2.05,2.35))]
    out += [Box(x,(-2.35,2.35),z) for x,z in (
        ((-.25,.15),(-2.5,-2)), ((-.25,.15),(0,.4)),
        ((-1.7,-1.4),(0,.4)))]
    # Base split by longitudinal NON-GUIDING access aperture y=1.25..2.0.
    out += [Box((-2.54,2.54),y,(-47,-46)) for y in ((-2.35,1.25),(2.,2.35))]
    return out


def slider(q=0):
    return [Box((-1.75+q,.9+q),(-.2,.2),(-2,0)),
            Box((-1.75+q,-.35+q),(-1.8,1.9),(-2,0)),
            Box((-1.3+q,-.7+q),(.85,1.9),(-4.5,-2))]


def head(dx=0, dz=0):
    # U opens upward. Short jaws and bridge above a long integral drive tongue.
    return [b.move(x=dx-.2,z=dz) for b in (
        Box((-2.05,-1.65),(1.5,1.85),(-4.8,-3.6)),
        Box((.05,.45),(1.5,1.85),(-4.8,-3.6)),
        Box((-2.05,.45),(1.5,1.85),(-5.3,-4.8)),
        Box((-1.95,.35),(1.5,1.85),(-49,-5.3)))]


def comb(released=False):
    # Slot [-1.5,-.5] moves .2 mm left with tang; tang below slider rather than outboard through post.
    # Teeth repeat across 40 cells. A .6-thick back spine joins all webs below tabs.
    # All comb material y=1..1.25, outside rack envelope y=+/-.8.
    dz=-1.5 if released else 0
    return [Box(x,(1.,1.25),(-4.4+dz,-3.6+dz))
            for x in ((-2.54,-1.5),(-.5,2.54))] + [
                Box((-2.54,2.54),(1.,1.25),(-5.1+dz,-4.5+dz))]


def rank_clearance():
    checks=0
    # Actual rectangular parts and exact translational sweeps, not just envelopes.
    # ±.05 each face + ±.05 relative row/registration, modeled as .10/.05 growth.
    obstacles=frame()
    for dx,dy in product((-P,0,P),repeat=2):
        if dx or dy:
            obstacles += [b.move(x=dx,y=dy) for b in frame()]
            obstacles += [Box((.4+dx,2.2+dx),(-.8+dy,.8+dy),(-42,42.2))]
    # Inserting from underneath, commanding x, and reversing insertion.
    for a in head():
        for b in obstacles:
            assert not sweep(a.grow(.10).move(z=-50),b.grow(.05),(0,0,50))
            checks+=1
    for a in head(-1.3):
        for b in obstacles:
            assert not sweep(a.grow(.10),b.grow(.05),(1.85,0,0))
            checks+=1
    for q in (-.35,.35):
        for a in head():
            for b in slider(q):
                assert not sweep(a.grow(.10).move(z=-50),b.grow(.05),(0,0,50))
                checks+=1
    # Moving slider includes known intended zero-clearance guide faces.
    # Nominal clearance only here; no manufactured-guide-fit claim.
    for a in slider(-.75):
        for b in frame():
            assert not sweep(a,b,(1.1,0,0)), (a,b)
    # Comb actual release clear of installed fork, posts, and rack at ALL heights.
    others=frame()+head()+[Box((.4,2.2),(-.8,.8),(-42,42.2))]
    for a in comb():
        for b in others:
            assert not sweep(a.grow(.05),b.grow(.05),(0,0,-1.5))
            checks+=1
    # Gate can move down with seated tang: slot side clearances retained.
    # Bottom-spine touches tang end nominally, then recedes. Do not expand the
    # intended interface: its tolerance sensitivity is reported separately.
    for a in comb():
        for b in slider():
            assert not sweep(a,b,(0,0,-1.5))
    # Released comb must not obstruct the whole command sweep.
    for a in slider(-.75):
        for b in comb(True):
            assert not sweep(a.grow(.05),b.grow(.05),(1.1,0,0))
    # Whole parallel rank permits independently opposite head commands.
    gap=P-((.45+.55)-(-2.05-1.3))-.2
    assert gap>0
    for i in range(39):
        for a in head(.55):
            for b in head(-1.3):
                assert a.move(x=i*P).grow(.1).overlap(b.move(x=(i+1)*P).grow(.1))==0
    solid_base=Box((-2.54,2.54),(-2.35,2.35),(-47,-46))
    base_hit=max(a.move(z=-43).overlap(solid_base) for a in head())
    assert base_hit>0
    return dict(expanded_sweeps=checks,independent_rank_gap=gap,
                intact_base_collision_mm3=base_hit,base_access_slot_width=.75,
                outer_base_strip_width=.35,unwindowed_posts=True)


def takeover():
    # Fixed wide U is NOT a clamp. Positive x load can reach either wall.
    # Tang sides [-1.3,-.7], jaw inner faces [-1.85,-.15].
    # Therefore q is bounded by [-.55,+.55] after comb release at head dx=0.
    nominal=(-.55,.55)
    minimum=1e9; witness=None; cases=0
    for jaw,tab,datum,nose,rack in product((-.05,.05),repeat=5):
        qlo=-1.85+jaw-(-1.3+tab)+datum
        overlap=.9+nose+qlo-(.4+rack)
        if overlap<minimum: minimum=overlap;witness=(jaw,tab,datum,nose,rack,qlo)
        cases+=1
    assert minimum<0
    # Even the zero-error adverse wall permits complete loss of tooth support.
    assert .9+nominal[0]<.4
    # A common fixed x preposition cannot guarantee both no interference during
    # acquisition and safe left restraint for every retained q in [-.35,+.35].
    # At zero error acquisition requires f<=.35; support requires f>=.05.
    # Under independent ±.05 jaw/tab/datum, + nose/rack ±.05:
    # Reconstruct acquisition from the SAME tab and comb errors, avoiding
    # independent resampling of a retained-q bound that already contains tab error.
    acquisition=[]
    for slot,comb_datum,jaw,writer_datum,tab in product((-.05,.05),repeat=5):
        qlo=(-1.5+slot+comb_datum)-(-1.3+tab)
        tab_left=-1.3+tab+qlo
        acquisition.append(tab_left-(-1.85+jaw+writer_datum))
    acquire_max=min(acquisition)  # tab error cancels exactly
    support_min=.55-.5+.15+.1
    assert abs(acquire_max-.15)<EPS and abs(support_min-.30)<EPS
    assert support_min>acquire_max
    # Reconstruct a supported-to-unsupported path using the actual island top
    # and rack tooth footprint; no depth/readback boolean substitutes for area.
    areas=[]
    for k in range(56):
        island=slider(-k*.01)[0]
        area=max(0.,min(island.x[1],1.2)-max(island.x[0],.4))*.4
        areas.append(area)
        assert island.z[1]==0
    assert abs(areas[0]-.2)<EPS and areas[50]<EPS and areas[-1]==0
    # 40 heads are needed, even for one changed column. Count actual graph edges.
    def supported(seated,gate,head_restraint,rack_head):
        return [rh or (s and (gate or hr))
                for s,hr,rh in zip(seated,head_restraint,rack_head)]
    all_seated=[True]*40
    assert all(supported(all_seated,True,[False]*40,[False]*40))
    lost=supported(all_seated,False,[False]*40,[True]+[False]*39)
    assert sum(lost)==1
    # This is a counterfactual requirement, NOT a constructed active-clamp pass.
    assert all(supported(all_seated,False,[True]*40,[True]+[False]*39))
    return dict(nominal_free_q=nominal,corner_cases=cases,
        worst_rack_overlap=minimum,witness=witness,
        common_pose_acquisition_max=acquire_max,common_pose_support_min=support_min,
        missing_restraint_channels_for_one_cell_update=39,
        fixed_open_U_takeover_pass=False)


def rescue_and_seams(n=16):
    # A reusable traveling rigid prop on an under-row sled is the simplest
    # compression support, avoiding a new resident lock. Five discrete heights
    # tested; arbitrary h is covered by the same bottom-foot/base crossing.
    # Existing head holds the rack until prop touches bottom. Props are geometry,
    # not an adjustable jack, stock proposal or permission to release that head.
    base=frame()[-2]  # wide base rail includes rack x=1.2..2.2, y=+/-.8
    hits=[]
    for h in (0,10,20,30,40):
        prop=Box((1.3,2.1),(-.5,.5),(-52,h-42))
        shoe=Box((1.2,2.2),(-.6,.6),(h-42-.8,h-42))
        sled=Box((-2.54,L-2.54),(-1.8,1.8),(-54,-52))
        rack=Box((1.2,2.2),(-.8,.8),(h-42,h+2))
        assert prop.overlap(rack)==0 and shoe.overlap(rack)==0
        assert prop.overlap(shoe)>0
        assert prop.z[0]==sled.z[1] # compression contact to traveling sled
        penetration=prop.overlap(base)
        assert penetration>0
        hits.append(penetration)
    # An unseated rack has no slider support. Removing the base first would
    # release both grounded posts for all 40 columns, not establish recovery.
    # Optimistic control GRANTS a through-base hole and a rigid prop of exact
    # height; now test complete longitudinal sled travel with real end members.
    sled=Box((-2.54,L-2.54),(-1.8,1.8),(-54,-52))
    end=L-2.54
    member=Box((end+.2,end+1.2),(-2.35,2.35),(-54.5,-51.5))
    assert sled.overlap(member)==0
    assert sweep(sled,member,(L,0,0))
    witness=sled.move(x=1.).overlap(member)
    assert witness>0
    # Moving the member entirely below the sled is a changed cabinet, not an
    # automatic repair: inherited dock rail geometry alone did not specify it.
    low_member=member.move(z=-4)
    assert not sweep(sled.grow(.1),low_member.grow(.1),(L,0,0))
    # Transverse clearance: the prop/sled remains inside the previous row body.
    moving=Box((-2.54,L-2.54),(-2.35,2.35),(-54,44)).grow(.10)
    neighbor=moving.move(y=P)
    assert not sweep(moving,neighbor,(L,0,0))
    for k in range(n+1):
        assert moving.move(x=L*k/n).overlap(neighbor)==0
    # Outer dock seam: two rail strips have an explicit g=.5 gap. Contact
    # length has a g deficit while crossing; it was constant only for g=0.
    g=.5
    contact=[]
    for k in range(n+1):
        u=L*k/n
        cabinet=max(0.,L-u)
        dock=max(0.,min(u-g,L))
        contact.append(cabinet+dock)
    assert min(contact)>=L-g-EPS
    # A 40-pitch half-row has no nominal central clearance at x seam. Opposed
    # .10 face/datum bounds cause .20 solid base overlap unless ends relieved.
    left=Box((-2.54,end),(-2.35,1.25),(-47,-46)).grow(.1)
    right=Box((end,2*L-2.54),(-2.35,1.25),(-47,-46)).grow(.1)
    seam_overlap=left.overlap(right)
    assert seam_overlap>0
    return dict(prop_base_penetration_mm3=hits,prop_installation_pass=False,
        granted_hole_sled_end_member_collision_mm3=witness,
        lowered_member_clears=True,neighbor_gap=P-4.7-.2,
        minimum_rail_contact_length=L-g,seam_gap=g,
        central_base_seam_overlap_mm3=seam_overlap,
        dock_attachment_constructed=False)


def load_and_scale():
    # Integral long writer tongue: independent Euler-Bernoulli demand bound.
    # y thickness .35; x width 2.30. Bending in x, I=t*w^3/12.
    # No calibrated material, strength or dynamic damage threshold supplied.
    w,t,Ls=2.3,.35,43.7
    I=t*w**3/12
    rows=[]
    for E in (1000,3000,200000):
        k=3*E*I/Ls**3
        rows.append(dict(E_MPa=E,k_N_per_mm=k,
                         force_at_point1_mm=k*.1,
                         deflection_at_point1_N=.1/k))
    stress_per_N=6*Ls/(t*w*w)
    # Local limiter needed DOWNSTREAM of every shared drive, even if rack head
    # bears gravity. Common limiter ceiling H*F allows one jam to see H*F.
    return dict(tongue_compliance=rows,root_stress_MPa_per_N=stress_per_N,
        local_window='F_required < F_trip < min(F_damage, k*allowed_deflection); none qualified',
        common_limiter_overload_factor=40,
        sites=6400,cassettes=160,minimum_slider_heads_per_released_comb=40,
        added_resident_command_pins=0,
        scheduling=[dict(H=H,groups=(6400+H-1)//H,
                         strict_slot_limit_s=24/((6400+H-1)//H)) for H in (40,80,160)],
        cost='Cshared + H*chead + 6400*ccell < $500; no priced BOM')


def main():
    result=dict(evidence='finite interface falsification and analytical bounds; self-review',
        side_entry_control=f.retention_direct()['direct_writer_bridge_collision_mm3'],
        underside=rank_clearance(),takeover=takeover(),recovery=rescue_and_seams(),
        loads=load_and_scale())
    for n in (1,64,256):
        assert rescue_and_seams(n)==result['recovery']
    # Independent sweep controls: a collision only in the path interior, and
    # tangential translation that must not be classified as penetration.
    a=Box((0,1),(0,1),(0,1)); b=a.move(x=2)
    assert sweep(a,b,(4,0,0)) and not sweep(a,b.move(y=1),(4,0,0))
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
