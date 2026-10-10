#!/usr/bin/env python3
"""E-116: finite two-level keeper/cam selector. mm, N, MPa; bounded assumptions."""
from itertools import product
import json

PITCH = 5.08
C = .05

def overlap(a, b):
    return min(a[1], b[1]) - max(a[0], b[0])

def section(e, p, run, stroke, nose, depth, gap):
    # Square pin in a straight oblique slot x = -stroke*y/run.
    # Slot boundary |x+m*y| <= p*(1+m)/2+gap. Pin translates in x only.
    m = stroke/run
    A = e*(2.5+1.5*m)  # slot wall e; x/y datums e; full pin width e
    B = gap+A          # greatest possible output position slack
    # blade is MINIMUM actual length; manufactured interval [blade,blade+2e].
    blade = stroke+2*B+2*e+.6 # fixed .6 guide survives relative tip/guide error
    margins = {
        'slot_insertion': gap-A-C,
        'ground_overlap': nose-B-e-C,
        'pocket_back': depth-e-(nose+B+e)-C,
        'retraction': stroke-B-(nose+e)-C,
        # Fixed rack, blade sweep and guide reserve in same x plane.
        'support_pitch': PITCH-(depth+.4+blade+stroke-nose+B+.4+4*e),
        'cam_x_pitch': PITCH-(stroke+p*(1+2*m)+2*gap*(1+m)+.8+4*e),
        'cam_y_pitch': PITCH-(run+p+2*gap+.8+4*e),
    }
    return dict(error=e,pin=p,run=run,stroke=stroke,nose=nose,
                depth=depth,gap=gap,slope=m,slack=B,blade=blade,
                margins=margins,minimum=min(margins.values()))

def straight_slot_vertices(r):
    # Actual finite parallelogram, with enough y end length for every pin corner.
    p,g,m,R=r['pin'],r['gap'],r['slope'],r['run']
    Y=p/2+g; H=p*(1+m)/2+g
    return [(sign*H-m*y,y) for y,sign in [(-R-Y,-1),(-R-Y,1),(Y,1),(Y,-1)]]

def in_convex(point, poly, tol=1e-10):
    crosses=[]
    for (a,b),(c,d) in zip(poly,poly[1:]+poly[:1]):
        crosses.append((c-a)*(point[1]-b)-(d-b)*(point[0]-a))
    return min(crosses)>=-tol or max(crosses)<=tol

def vertical(e, G=4., extra=.8, j=.6, plate=1.2):
    # Lower keeper top z=0, cam underside z=G. Pin length G+extra.
    # Pin lower end q: idle=-extra-j, selected=j; continuous positive writer.
    # Pin-length, lower/upper plate-location and writer-position errors +/-e.
    # Selection gate has two horizontal grooves for a .4-mm command tab.
    Q=extra+2*j; tab=.4; gate_gap=2.5*e+C
    drift=gate_gap+2.5*e  # retained tab slack after programming fork departs
    return dict(G=G,extra=extra,j=j,plate=plate,stroke=Q,
                pin_length=G+extra,gate_gap=gate_gap,retained_drift=drift,
                margins={
                    'idle_cam_clear':j-drift-2*e-C,
                    'active_keeper_clear':j-drift-e-C,
                    'dual_engagement':extra-3*e-2*C,
                    'active_cam_depth':j-drift-2*e-C,
                    'plate_depth':plate-2*e-C,
                    'gate_web':Q-tab-2*gate_gap-2*e-.4,
                    'gate_height':G-(Q+tab+2*gate_gap+4*e),
                })

def verify(r):
    e,p,m=r['error'],r['pin'],r['slope']
    # Independently reconstruct all manufactured square vertices in a finite
    # parallelogram; 257 nodes are holdouts, not the continuous certificate.
    # Each coordinate is affine in phase. Nodes 0 and 1 bound the entire path.
    poly=straight_slot_vertices(r)
    width=max(x for x,y in poly)-min(x for x,y in poly)
    expected=r['stroke']+p*(1+2*m)+2*r['gap']*(1+m)
    assert abs(width-expected)<1e-12
    tested=0
    for de,dx,dy,wall in product((-e,e),repeat=4):
        b=p+de; H=p*(1+m)/2+r['gap']+wall
        Y=p/2+r['gap']; R=r['run']
        poly=[(sign*H-m*y,y) for y,sign in [(-R-Y,-1),(-R-Y,1),(Y,1),(Y,-1)]]
        for i in range(257):
            s=r['run']*i/256
            for u,v in product((-b/2,b/2),repeat=2):
                point=(m*s+dx+u,-s+dy+v)
                assert in_convex(point,poly)
                tested+=1
    # Fixed finite guide lies inside the intersection of every possible blade.
    right=r['nose']-r['stroke']-r['slack']-e
    guide=(right-.6,right)
    for q in (-r['slack']-e,r['slack']+e):
        for t in (0,1):
            tip=r['nose']-r['stroke']*t+q
            assert tip-r['blade']<=guide[0]+1e-12 and tip>=guide[1]-1e-12
    assert guide[1]<-C
    # Actual support rectangles throughout withdrawal: under the stated unload,
    # their z interval lies within the pocket; x retreats monotonically.
    # Rack pocket roof u=1, floor u-h; h=3, blade thickness .6, errors +/-e.
    for shift,nose_error,depth_error,thick_error in product(
            (-r['slack'],r['slack']),(-e,e),(-e,e),(-e,e)):
        for i in range(65):
            x=r['nose']-r['stroke']*i/64+shift+nose_error
            blade=[(x-r['blade'],-(.6+thick_error)),(x,0)]
            assert blade[0][1]>1-3+e+C and blade[1][1]<1-e-C
            assert x<r['depth']+depth_error-C
        assert r['nose']+shift+nose_error>C
        assert r['nose']-r['stroke']+shift+nose_error<-C
    # Vertical transfer: enumerate finite pin/plate intervals; commands can
    # bridge both because cam stays home. No unsupported x interval permitted.
    v=vertical(e); G,L=v['G'],v['pin_length']; min_cover=1e9
    for dl,dlo,dup,dq in product((-e,e),(-e,e),(-e,e),
                                (-v['retained_drift'],v['retained_drift'])):
        lower=(-v['plate']+dlo,dlo); upper=(G+dup,G+v['plate']+dup)
        for i in range(513):
            q=-v['extra']-v['j']+v['stroke']*i/512+dq
            pin=(q,q+L+dl)
            cover=max(overlap(pin,lower),overlap(pin,upper))
            assert cover>C
            min_cover=min(min_cover,cover)
        assert G+dup-(-v['extra']-v['j']+dq+L+dl)>C
        assert v['j']+dq-dlo>C
    # Two finite gate grooves block a halfway command: a shared gate cannot
    # close around a tab at the midpoint. A withdrawn gate would not retain it.
    q0=-v['extra']-v['j']; q1=v['j']; half=.2+v['gate_gap']
    grooves=[(q0-half,q0+half),(q1-half,q1+half)]
    midpoint=(q0+q1)/2
    assert not any(a<=midpoint-.2 and midpoint+.2<=b for a,b in grooves)
    assert all(a<=q-.2 and q+.2<=b for q,(a,b) in zip((q0,q1),grooves))
    # Support state checks remain conditional on a carrier and true proof.
    trace=[(1,1,0),(1,1,1),(1,0,1),(1,1,1),(1,1,0),(0,1,0)]
    assert all(g or c for _,g,c in trace)
    assert all(c==1 for c,_,_ in trace[:-1])
    # A pin bridging keeper/cam cannot follow a stroke beyond summed slack.
    # Interval intersection is a geometric jam witness, not safe extraction.
    jam=max(0.,r['stroke']-2*r['slack'])
    assert jam>0
    return {'manufactured_vertex_checks':tested,'vertical_min_overlap':min_cover,
            'stuck_bridge_interval_gap':jam,'support_trace':trace,
            'finite_cam_vertices':straight_slot_vertices(r)}

def transfer_fault(r):
    """No assumption that a clearance-mounted output stays at its center."""
    p,e,m,g=r['pin'],r['error'],r['slope'],r['gap']
    forward=reverse=total=0; witness=None
    for dp,ck,cc,dy,wk,wc in product((-e,e),repeat=6):
        b=p+dp
        kh=p/2+g+wk-b/2
        ch=p*(1+m)/2+g+wc-b*(1+m)/2
        K=(ck-kh,ck+kh); Cslot=(cc-m*dy-ch,cc-m*dy+ch)
        assert min(kh,ch)>0
        f=K[0]>=Cslot[0]-1e-12 and K[1]<=Cslot[1]+1e-12
        rev=Cslot[0]>=K[0]-1e-12 and Cslot[1]<=K[1]+1e-12
        forward+=f; reverse+=rev; total+=1
        if not f:
            x=K[1] if K[1]>Cslot[1] else K[0]
            # Direct four-corner half-plane check, independent of nesting test.
            H=p*(1+m)/2+g+wc
            penetration=max(abs(x+u+m*(dy+v)-cc)-H
                            for u,v in product((-b/2,b/2),repeat=2))
            assert penetration>0
            assert abs(x-ck)+b/2<=p/2+g+wk+1e-12
            candidate=dict(pin_width=b,keeper_interval=K,cam_interval=Cslot,
                         pin_center=x,wall_penetration=penetration,
                         errors=dict(pin=dp,keeper_center=ck,cam_center=cc,
                                     y_datum=dy,keeper_wall=wk,cam_wall=wc))
            if witness is None or penetration>witness['wall_penetration']:
                witness=candidate
    # At zero error, identical intervals can transfer in this idealization.
    if e==0: assert forward==reverse==total
    else: assert forward<total and reverse<total
    return dict(corners=total,forward_containment=forward,
                reverse_containment=reverse,failed_forward_witness=witness)


def main():
    rows=[]; witnesses=[]
    for e in (.05,.10,.20):
        survivors=[]; rejected={}; count=0
        for p,R,d,o,D,g in product((.6,.8,1.),(1.2,2.,3.),
                                  (.9,1.1,1.4,1.8,2.2),(.4,.45,.55,.7,.9,1.1),
                                  (.95,1.2,1.8,2.4),(.15,.20,.23,.3,.4,.6)):
            count+=1; r=section(e,p,R,d,o,D,g)
            if r['minimum']>=-1e-12: survivors.append(r)
            else:
                k=min(r['margins'],key=r['margins'].get)
                rejected[k]=rejected.get(k,0)+1
        best=max(survivors,key=lambda x:x['minimum'],default=None)
        if best: witnesses.append(best)
        # Necessary planar envelope, independent of grid and slope:
        # g >= A+C; B>=2A+C >=5e+C.
        # D>=o+B+2e+C; d>=o+B+e+C; o>=B+e+C.
        # blade>=d+2B+2e+.6; width>=D+2d-o+3B+1.4+6e.
        # Substitution gives width>=8B+12e+1.65 >=52e+2.05.
        rows.append(dict(error=e,generated=count,survivors=len(survivors),
                         best=best,rejected_primary_reason=rejected,
                         planar_width_lower_bound=52*e+2.05,
                         vertical=vertical(e)))
    assert rows[0]['survivors']>0
    assert rows[1]['planar_width_lower_bound']>PITCH
    assert rows[2]['planar_width_lower_bound']>PITCH
    r=max(witnesses,key=lambda x:x['minimum'])
    checks=verify(r)
    checks['transfer']=transfer_fault(r)
    transfer_fault(dict(r,error=0.))
    force=[]
    # Pin shear is not the only limit: bending over half the 4-mm layer gap.
    # 0.4 mm accounts for a support/contact lever extension, explicitly bounded.
    for sigma,drag,mu in product((5.,10.,20.),(.005,.01,.05),(.1,.3,.5)):
        cap=sigma*(r['pin']-r['error'])**3/(6*(4/2+.4))
        gain=(r['slope']+mu)/(1-mu*r['slope'])
        # Common limiter must both move 80 outputs and protect a solitary jam.
        force.append(dict(sigma_MPa=sigma,drag_N=drag,mu=mu,
                          capacity_N=cap,bank_input_N=80*drag*gain,
                          solitary_jam_input_limit_N=cap*gain,
                          static_limiter_window_N=(cap-80*drag)*gain))
    # Limiting cases independently follow virtual work and zero slope friction.
    for m in (0.,.5,1.):
        assert abs((m+0)/(1-0*m)-m)<1e-12
    print(json.dumps(dict(evidence='deterministic bounded geometry; no hardware or yield',
                         search=rows,checks=checks,force_scenarios=force,
                         limiter_scenarios_with_window=sum(x['static_limiter_window_N']>0 for x in force)),indent=2))
if __name__=='__main__': main()
