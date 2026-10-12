"""E-214 finite interface comparison. mm, N, s; bounded scenarios, not priors.
NumPy only. Imports canonical E-213 solids/SAT. JSON is reproducible, disposable.
Prescribed contact-seeking pads are output envelopes, not built actuators.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
import numpy as np
s=importlib.util.spec_from_file_location('tail',Path(__file__).resolve().parents[1]/'E-213/tail.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
c=t.c; B=t.B


def rotated(parts,angle,dy=0.,pivot=0.):
    co,si=math.cos(angle),math.sin(angle)
    return [((p-[0,pivot])@np.array([[co,-si],[si,co]])+[dy,pivot],x) for p,x in parts]


def pose(angle,size=0.,dy=0.,dx=0.):
    parts=rotated(t.tail(size),angle,dy)
    low=min(p[:,1].min() for p,x in parts)
    return t.shift(parts,x=dx,z=-low)


def root(a,b,span):
    lo,hi=0.,.3
    for _ in range(65):
        v=(lo+hi)/2
        if span*math.tan(v)+2*a/math.cos(v)>2*b:hi=v
        else:lo=v
    return (lo+hi)/2


def resident():
    # E-212 web bearing at z=7.5/20.5; local tail coordinates add 76.
    # Center web in y about 1.95; its half-thickness is .25.
    out=[]
    for play in (.005,.025,.075,.15):
        a=root(.25,.25+play,13.)
        # Guides center at global z=14; pin at -74+h. Rigid pose bounds.
        rows=[]
        for h in (0.,20.,40.):
            pivot=90.-h
            actual=rotated(t.tail(),a,pivot=pivot)
            shift=(2-pivot)*math.tan(a)
            # Test pin rectangle against inverse-transformed actual window; absence
            # of collision alone can also mean the pin missed the tail entirely.
            fixed=np.array([[-.3,1.7],[-.3,2.3],[.3,1.7],[.3,2.3]])
            co,si=math.cos(a),math.sin(a)
            local=(fixed-[0,pivot])@np.array([[co,si],[-si,co]])+[0,pivot]
            inside=bool(np.all(abs(local[:,0])<=.5) and np.all((local[:,1]>=1.5)&(local[:,1]<=2.5)))
            # Independently construct the actual web pose at the resident bands.
            web=rotated([B(-.8,.8,-.25,.25,-42,86)],a,pivot=14.)
            guide=t.shift(c.guide(web=.8,gap=play),y=-1.95)
            assert not c.hits(web,guide)
            rows.append(dict(h=h,pin_plane_offset_mm=shift,pin_hits_tail=bool(c.hits(actual,t.pin())),
                             full_pin_section_inside_window=inside))
        out.append(dict(half_play_mm=play,angle_rad=a,cases=rows))
    # Necessary transverse budget with .05 registration + .05 hole error + .02 pin error.
    # At lowest height, remaining .08 out of nominal .20. Solve exact guide relation.
    th=math.atan(.08/88.)
    max_play=(13*math.tan(th)+.5/math.cos(th)-.5)/2
    assert .005<max_play<.006
    return dict(cases=out,maximum_half_play_for_declared_parallel_budget_mm=max_play,
                guide_stations=12800,bearing_faces=64000)


def open_frame():
    # 4.9-mm outside, 3.3-mm open aperture, no floor (pin carries BOTH z signs).
    out=[]
    for sx,sy in it.product((-1,1),repeat=2):
        xx=sorted((sx*1.65,sx*2.45)); yy=sorted((sy*1.65,sy*2.45))
        out.append(B(*xx,*yy,0,18.5))
    # Bridges behind pads; connected to all four posts.
    for z in (6.,18.):
        out += [B(-2.45,2.45,-2.45,-2.05,z-.5,z+.5),B(-2.45,2.45,2.05,2.45,z-.5,z+.5),
                B(-2.45,-2.05,-2.05,2.05,z-.5,z+.5),B(2.05,2.45,-2.05,2.05,z-.5,z+.5)]
    return out


def pads(actual=None):
    out=[]
    for z in (6.,18.):
        xmin,xmax=-1.65,1.65; ymin,ymax=-1.65,1.65
        if actual is not None:
            # Exact polygon clipping to finite band; no midpoint/nominal-face grant.
            ys=[]; xs=[]
            for p,x in actual:
                q=p.tolist()
                for sign,bound in ((1,z+.5),(-1,-z+.5)):
                    qq=[]
                    for aa,bb in zip(q,q[1:]+q[:1]):
                        da=sign*aa[1]-bound;db=sign*bb[1]-bound
                        if da<=1e-12:qq.append(aa)
                        if (da<0<db) or (db<0<da):qq.append((np.array(aa)+(np.array(bb)-aa)*da/(da-db)).tolist())
                    q=qq
                    if not q:break
                if q:ys.extend(p[0] for p in q);xs.extend(x)
            xmin,xmax=min(xs),max(xs);ymin,ymax=min(ys),max(ys)
        out += [B(-2.05,xmin,-1.65,1.65,z-.5,z+.5),B(xmax,2.05,-1.65,1.65,z-.5,z+.5),
                B(xmin,xmax,-2.05,ymin,z-.5,z+.5),B(xmin,xmax,ymax,2.05,z-.5,z+.5)]
    return out


def carriage(dy=0.,dz=0.):
    # Hollow pin bearing with integral upper/lower flanges. Y slide retained in x/z.
    out=[B(1.05,1.85,-.8,-.4,1.3,2.7),B(1.05,1.85,.4,.8,1.3,2.7),
         B(1.05,1.85,-.4,.4,1.3,1.6),B(1.05,1.85,-.4,.4,2.4,2.7),
         B(.95,1.95,-.8,.8,1.,1.3),B(.95,1.95,-.8,.8,2.7,3.)]
    return t.shift(out,y=dy,z=dz)


def rails():
    out=[B(.85,2.05,-1.95,1.95,.6,.9),B(.85,2.05,-1.95,1.95,3.1,3.4)]
    for z0,z1 in ((.9,1.4),(2.6,3.1)):
        out += [B(.85,.90,-1.95,1.95,z0,z1),B(2.,2.05,-1.95,1.95,z0,z1)]
    for sign in (-1,1):
        yy=sorted((sign*1.55,sign*1.95))
        out.append(B(.85,2.05,*yy,.6,3.4))
    # Bridges meet corner posts at x>=1.65, |y|>=1.65.
    return out


def floating():
    frame=open_frame()+rails()
    cases=[]
    for angle in (.005,.01,.02):
        counts=dict(acquisition=0,closed_guide=0,pin_path=0,slide_contact=0); first=None
        n=0; travel=0.
        for sign,size,dy,dx,dz,sx in it.product((-1,1),(-.05,.05),(-.05,.05),(-.05,.05),(-.1,.1),(-.05,.05)):
            actual=pose(sign*angle,size,dy,dx)
            # Centerline at pin z=2 accounting for bottom seating. Height/pin pose
            # must be acquired; formula is an oracle geometric target, not readback.
            bottom=(.8+size)*abs(math.sin(angle))
            fy=dy+math.tan(sign*angle)*(2-bottom)
            travel=max(travel,abs(fy));n+=1
            counts['acquisition']+=bool(c.hits(t.sweep(frame+pads()+carriage(),2,-20,0),actual))
            closed=pads(actual)
            collision=c.hits(closed+frame,actual)
            counts['closed_guide']+=bool(collision)
            if collision and first is None:
                i,j=collision[0];aa=(closed+frame)[i];bb=actual[j]
                first=dict(angle=sign*angle,half_size_error=size,x_offset=dx,y_offset=dy,
                           body_index=i,tail_part=j,x_penetration_mm=min(aa[1][1],bb[1][1])-max(aa[1][0],bb[1][0]))
            moving=t.shift(t.sweep(t.pin(),0,0,1.7),x=sx,y=fy,z=dz)
            counts['pin_path']+=bool(c.hits(moving,actual+frame))
            counts['slide_contact']+=bool(c.hits(t.shift(carriage(fy,dz),x=sx),actual+frame))
        cases.append(dict(pitch_bound_rad=angle,cases=n,failures=counts,required_y_float_mm=travel,first_collision=first))
    # Explicit mechanical retention: permitted y travel and z backlash, stop beyond.
    assert not c.hits(carriage(.65,.1),rails())
    assert c.hits(carriage(.751,0),rails())
    assert c.hits(carriage(0,.101),rails())
    assert c.hits(t.shift(carriage(),x=.051),rails())
    # Free transverse motion is bounded .75; x and z play are .05/.10.
    # These are assumed remaining clearances, not manufactured-fit qualification.
    return dict(cases=cases,retention_limits=dict(y_mm=.75,z_mm=.1,x_mm=.05),
                frame_volume_mm3=t.volume(frame),carriage_volume_mm3=t.volume(carriage()),
                resident_guide_volume_cm3_board=t.volume(c.guide(web=.8,gap=.15))*6400/1000)


def release_tool(q=(0.,0.,0.),ez=.3,ey=.2,dx=0.):
    # E-211 four-shoe tool, identical finite output envelopes, no new miniature fit.
    parts=[B(-2.,-1.05,-.65,-.25,.94,1.06),B(-1.25,-1.,-.7,-.2,1+ez,1.1+ez),
           B(-1.25,-1.,-.7,-.2,.9-ez,1-ez),B(-1.25,-1.,-.65-ey,-.55-ey,.85,1.15),
           B(-1.25,-1.,-.35+ey,-.25+ey,.85,1.15),B(-2.2,-1.8,-.7,-.2,.6,1.4),
           B(-1.2,-1.05,-.6,-.3,1,1.05+ez),B(-1.2,-1.05,-.6,-.3,.95-ez,1),
           B(-1.2,-1.05,-.6-ey,-.55,.95,1.05),B(-1.2,-1.05,-.35,-.3+ey,.95,1.05)]
    return c.move(parts,q,dx)


def integration():
    # Evaluate new mechanisms against explicit inherited release envelope. Its
    # original pocket/rod feasibility and force limits remain E-211/E-209, not rerun.
    frame=c.r.fixed(.2,0,.2);resident=c.guide(web=.8,gap=.15)
    head=open_frame()+pads()+rails()+carriage()+t.pin(1.7)
    lower=t.installed(t.sweep(head,2,-20,41.5))
    assert not c.hits(lower,frame+resident)
    bad=0
    for n in (16,32,64):
        for q in [(0,0,a) for a in np.linspace(0,.22,n+1)]+[(-w,0,.22) for w in np.linspace(0,1.2,n+1)]:
            bad+=bool(c.hits(release_tool(q),lower+resident))
    assert bad==0
    # Old 40-mm prescribed path remains valid only in nominal parallel poses.
    t.finite()
    # Resident guide nominal full rack sweep and neighbors, no hidden column guide.
    assert not c.hits(resident,t.sweep(c.rack(web=.8),2,0,41.5))
    neighbors=[]
    for x,y in [(5.03,0),(-5.03,0),(0,5.03),(0,-5.03)]:
        neighbors+=t.shift(t.sweep(t.assembly(),2,0,40),x=x,y=y)
    assert not c.hits(lower,neighbors)
    packing=[]
    for spacing in (5.08,10.16):
        packing.append(dict(x_spacing_mm=spacing,collision=bool(c.hits(head,t.shift(t.sweep(head,2,-61.5,61.5),x=spacing)))))
    return dict(release_new_geometry_conflicts=bad,nominal_neighbor_clear=True,packing=packing,
                release_outputs_per_head=8,release_status='four shoes plus y/z/pitch and insertion; inherited unresolved drives/stem')


def state_and_bounds():
    # Support flags are actual mechanical conditions, never commanded/report bits.
    states=[('resident',1,0,0),('capture_proof',1,1,0),('unload_release',0,1,0),
            ('travel',0,1,0),('resident_reseat',1,1,0),('unload_head_proof',1,1,1),('depart',1,0,1)]
    assert all(r or h for _,r,h,p in states)
    # False proof permits an unsafe departure: do not turn this into a sensor pass.
    def depart(actual_resident,reported_resident):
        head_support=not reported_resident
        return bool(actual_resident or head_support)
    assert depart(False,False) and not depart(False,True) and depart(True,True)
    rows=[]
    for H in (40,80,160):
        times=[]
        for acc,aux in it.product((1000,5000,20000),(.08,.16,.32)):
            # Existing safe park (both use 20-mm clearance to make comparison equal).
            motion=sum(2*math.sqrt(d/acc) for d in (30,1.5,30,1.5,60,1.7,1.7))
            times.append(dict(a=acc,aux=aux,cycle_s=motion+aux,necessary_pass=motion+aux<24*H/6400))
        rows.append(dict(H=H,slot_s=24*H/6400,A_active_outputs=10*H,B_active_outputs=18*H,
                         B_additional_passive_slides=H,rows_at_sparse_pitch=math.ceil(H/40),
                         dollars_per_head_with_250_elsewhere=250/H,timing=times))
    friction=[dict(mu=mu,Fz=F,lateral_slide_resistance=mu*F,
                   moment_at_12mm=12*mu*F) for mu,F in it.product((0,.1,.3),(1,10))]
    return dict(states=states,false_accept_can_lose_support=True,heads=rows,friction_scenarios=friction,
                resident_purchase_sensitivity=[dict(per_cell=v,total=6400*v) for v in (0,.01,.02,.04)],
                inspection_hours_at_10s=6400*10/3600)


def departure_contact():
    # E-208 rack/toe vertical bearing is y=.8..1.2, x=+/-.4.
    # Toe keys restrain TOE, not rack. A single rack/web side normal cannot
    # balance horizontal equilibrium with no opposed ground contact.
    # A generous endpoint pressure cone is an upper bound on that whole pad.
    rows=[]
    for yload,ratio in it.product((.8,1.,1.2,1.95),(0.,-.005,.005)):
        F=10.; H=ratio*F; lever=40.
        resultant=yload+lever*H/F
        right=F*(resultant-.8)/.4;left=F-right
        assert abs(left+right-F)<1e-12
        assert abs(.8*left+1.2*right-(F*yload+lever*H))<1e-12
        rows.append(dict(y_load_mm=yload,H_over_F=ratio,left_N=left,right_N=right,
                         supported_without_resident_moment_guide=bool(left>=-1e-12 and right>=-1e-12),
                         moment_even_granting_separate_horizontal_reaction=True))
    # Even granting a lateral reaction, the axial-centered downward load fails.
    centered=next(r for r in rows if r['y_load_mm']==1.95 and r['H_over_F']==0.)
    assert centered['left_N']<0
    return dict(pad_y_mm=[.8,1.2],cases=rows,
                guide_missing_moment_at_10N_Nmm=10*(1.95-1.2),
                contact_model='necessary frictionless moment cone, not service-load requirement')


def controls():
    # Reconstruct decisive retained-cup arithmetic directly, rather than count
    # it as novelty. The finite witnesses remain in their canonical sources.
    gap=.125
    overlap=.2-math.sqrt(2)*gap
    assert overlap < .025
    compact_clearance=5.08-5.002082-2*.046667
    assert compact_clearance<0
    assert abs(.9-.85-.05)<1e-12  # independent B rail overlap witness
    # E-054 distinct wall and shelf thickness; E-056 edge pressure yields no
    # positive pitch reserve. No invented material allowable or friction prior.
    width=1.6+4*.35+4*.1+2*.4+2*.4
    stress=3*10*.1/(.8*.8**2)
    assert abs(width-5.)<1e-12 and abs(stress-5.859375)<1e-12
    return dict(E125_loaded_overlap_mm=overlap,E125_compact_translation_margin_mm=compact_clearance,
                E054_width_mm=width,E054_shelf_demand_MPa=stress,E056_edge_pitch_margin_mm=0,
                E213_tail_failure_cases=len(t.loaded_contact()))


def run():
    # Independent contact equation/zero-gap limits and inherited exact controls.
    assert abs(root(.8,.8,13))<1e-12
    assert not c.hits(c.guide(gap=.15),c.r.p.writer(1.099))
    assert c.hits(c.guide(gap=.15),c.r.p.writer(1.101))
    out=dict(departure=departure_contact(),controls=controls(),resident=resident(),floating=floating(),integration=integration(),bounds=state_and_bounds())
    assert all(r['failures']['acquisition']==16 and r['failures']['closed_guide']==16
               and r['failures']['pin_path']==0 for r in out['floating']['cases'])
    assert not out['resident']['cases'][-1]['cases'][0]['full_pin_section_inside_window']
    return out

if __name__=='__main__':print(json.dumps(run(),indent=2))
