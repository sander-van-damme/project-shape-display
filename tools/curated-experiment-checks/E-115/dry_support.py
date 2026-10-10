#!/usr/bin/env python3
"""E-115 finite planar support screen. mm, N, radians; assumptions, not FDM priors."""
from itertools import product
from math import sin, cos, sqrt, pi, hypot
import json

PITCH = 5.08
CLEAR = .05

def corners(*ranges):
    return product(*ranges)

def clip(poly, wall):
    """Sutherland-Hodgman clip to x >= wall."""
    out = []
    for p, q in zip(poly, poly[1:]+poly[:1]):
        ip, iq = p[0] >= wall, q[0] >= wall
        if ip: out.append(p)
        if ip != iq:
            s = (wall-p[0])/(q[0]-p[0])
            out.append((wall, p[1]+s*(q[1]-p[1])))
    return out

def pawl(a, length, thick, angle):
    # pivot (-a,-thick/2); initial seated top z=0.
    return [(-a+x*cos(angle)-z*sin(angle),
             -thick/2+x*sin(angle)+z*cos(angle))
            for x,z in [(0,-thick/2),(length,-thick/2),
                        (length,thick/2),(0,thick/2)]]

def sweep(a, length, thick, theta, steps, inflate=True):
    # Every material point moves <= radius * angle_step/2 from nearest node.
    # Clip at -eps so a point just outside the rack is never missed.
    eps = hypot(length, thick/2)*theta/(2*steps) if inflate else 0.
    hi, lo, right = -1e9, 1e9, -1e9
    for i in range(steps+1):
        p = clip(pawl(a,length,thick,theta*i/steps), -eps)
        if p:
            hi=max(hi,max(z for x,z in p)+eps)
            lo=min(lo,min(z for x,z in p)-eps)
            right=max(right,max(x for x,z in p)+eps)
    return lo,hi,right

def pivot_case(a, overlap, thick, height, angle_deg, error, steps=96):
    """Evaluate a conservative interval enclosure of ALL dimensional combinations.

    Evaluate nominal swept body expanded by eta. This bounds pivot translation,
    bar length and thickness errors, and +/-2 degree commanded angle error.
    Pocket depth error and common lift error are additional.
    This avoids a corner-only nonlinear robustness claim.
    """
    length=a+overlap
    theta=angle_deg*pi/180
    # Actual angle theta_actual=theta_nominal*s, |theta_actual-theta|<=2 deg.
    # At every sweep fraction, rotation discrepancy is <=2 deg.
    radius=hypot(length+error,(thick+error)/2)
    # position changes: pivot x e; length e; centre shift t/2 e/2;
    # local half-thickness e/2. Sum norm bound 3e plus angle error.
    eta=3*error+radius*(2*pi/180)
    eps=hypot(length,thick/2)*theta/(2*steps)
    hi,lo,right=-1e9,1e9,-1e9
    for i in range(steps+1):
        p=clip(pawl(a,length,thick,theta*i/steps),-(eta+eps))
        if p:
            hi=max(hi,max(z for x,z in p)+eta+eps)
            lo=min(lo,min(z for x,z in p)-eta-eps)
            right=max(right,max(x for x,z in p)+eta+eps)
    # lift u with an additional +/-error endpoint error, pocket h +/-error.
    low=hi+CLEAR+error
    high=lo+height-error-CLEAR-error
    withdrawn=-CLEAR-max(x for x,z in pawl(a,length,thick,theta))-eta
    back=1.2-error-right-CLEAR
    engaged=overlap-2*error-CLEAR
    # Bare section width: pivot back reserve .6, tail overall depth 1.6.
    width=PITCH-(a+.6+1.6+2*error)
    margin=min(high-low,withdrawn,back,engaged,width)
    return dict(margin=margin,lift=[low,high],withdrawal=withdrawn,
                back=back,engagement=engaged,width=width,
                body_error_radius=eta)

def toggle(length, b, K, overlap, error):
    # Both link lengths vary independently; extrema below are attained
    # with both short or both long (separable monotone square-root terms).
    # Error endpoints envelope lengths, dead-centre offset, final knee travel.
    # Positive closed knee +b -> 0 -> -K. Crossbolt is grounded in square guide.
    if not 0 < b-error < b+error < length-error or K+error >= length-error:
        return None
    closed_min=2*sqrt((length-error)**2-(b+error)**2)
    closed_max=2*sqrt((length+error)**2-(b-error)**2)
    # Same link length retained between closed/open: do not independently
    # combine output span extremes and erase correlation.
    rows=[]
    for L,B,T in corners((length-error,length+error),
                         (b-error,b+error),(K-error,K+error)):
        if not 0<B<T<L: return None
        closed=2*sqrt(L*L-B*B)
        overshoot=2*L-closed
        retract=closed-2*sqrt(L*L-T*T)
        rows.append((overshoot,retract))
    # Analytic monotonic extrema over box; validated by interior holdouts.
    over=max(v[0] for v in rows); retract=min(v[1] for v in rows)
    return dict(overshoot=over,retract=retract,
                back_margin=1.2-error-(overlap+error+over)-CLEAR,
                open_margin=retract-(overlap+error)-CLEAR,
                deadcentre_margin=b-error,
                # two .4-mm-thick links with .3 radial joint envelope.
                mechanism_x=2*(length+error)+.6,
                mechanism_z=b+K+2*error+.6,
                span_range=[closed_min,closed_max],
                # x=0 rack lip, slider joint .8 behind bolt tip; finite .3
                # joint radius. Rack ends at x=1.6. Includes offset error.
                footprint=1.6-(overlap-error)+.8+closed_max+.3,
                pitch_margin=PITCH-(1.6-(overlap-error)+.8+closed_max+.3))

def crossbolt(error):
    # E-092-type rectangular comparator, positive bidirectional drive omitted.
    o,t,h,stroke=.4,.6,3.,.9
    return dict(lift=[CLEAR+error,h-error-(t+error)-CLEAR-error],
                engagement=o-error-CLEAR,
                withdrawal=stroke-error-(o+error)-CLEAR,
                back=1.2-error-(o+error)-CLEAR)

def transition_checks():
    # (command, ground support, carrier support); ideal logical gates ONLY.
    state=(1,1,0); trace=[state]
    state=(1,1,1); trace.append(state)  # acquire and prove
    state=(1,0,1); trace.append(state)  # retract unloaded ground
    state=(1,1,1); trace.append(state)  # independently reseat ground
    state=(1,1,0); trace.append(state)  # prove ground then release carrier
    state=(0,1,0); trace.append(state)  # clear command independently
    assert all(g or c for _,g,c in trace)
    # Direct ground = not command: cannot remain armed AND supported at proof.
    impossible=[s for s in trace if s[1] != 1-s[0]]
    # If command clears on reseat, same command cannot selectively release grip:
    clear_on_seat=(0,1,1)
    assert clear_on_seat[0]==0 and trace[3][0]==1
    # A false ground proof permits (1,0,0), irrespective of command readback.
    bad_proof=(1,0,0)
    assert not any(bad_proof[1:])
    return {'trace':trace,'direct_complement_violations':len(impossible),
            'false_ground_proof_witness':[1,0,0],
            'minimal_logical_output_states':['ground_only','both','carrier_only']}

def verify():
    # Nominal sweep enclosures converge; fine uninflated samples within all.
    for a,o,t,theta in [(1.5,.6,.8,60),(2.,.4,.6,75),(1.,.8,1.,90)]:
        args=(a,a+o,t,theta*pi/180)
        fine=sweep(*args,4096,False)
        for n in (32,64,128):
            coarse=sweep(*args,n)
            assert coarse[0] <= fine[0]+1e-9
            assert coarse[1] >= fine[1]-1e-9
            assert coarse[2] >= fine[2]-1e-9
    # Rigidly translating rack/pivot together changes no relative geometry.
    assert all(abs(x-y)<1e-12 for p,q in zip(pawl(1.5,2.1,.8,0),[(-1.5,-.8),(.6,-.8),(.6,0.),(-1.5,0.)]) for x,y in zip(p,q))
    # Manufactured vertex holdouts against the certified body error tube.
    a,o,t,h,th,e=1.5,.4,.6,4.,75.,.1
    r=pivot_case(a,o,t,h,th,e)
    for da,dl,dt,dth in product((-e,e),(-e,e),(-e,e),(-2.,2.)):
        for j in range(101):
            f=j/100
            nom=pawl(a,a+o,t,th*pi/180*f)
            actual=pawl(a+da,a+o+dl,t+dt,(th+dth)*pi/180*f)
            assert max(hypot(x-u,z-v) for (x,z),(u,v) in zip(nom,actual))<=r['body_error_radius']+1e-12
            p=clip(actual,0)
            if p:
                assert max(z for x,z in p)+CLEAR+e <=r['lift'][0]+1e-12
                assert min(z for x,z in p)+h-e-CLEAR-e >=r['lift'][1]-1e-12
                assert max(x for x,z in p)<1.2-e-CLEAR
    # Inverse toggle formula checked on independent knee reconstruction.
    for L,B,K in product((1.4,1.6,1.8),(.15,.25,.35),(.9,1.1,1.3)):
        if K>=L: continue
        d0=2*sqrt(L*L-B*B)
        for j in range(101):
            k=B-(B+K)*j/100
            x=sqrt(L*L-k*k)
            assert abs(hypot(x,k)-L)<1e-12
            assert 2*x <=2*L+1e-12
        assert abs(sqrt(L*L-(d0/2)**2)-B)<1e-12
    # Independent unequal-link and interior manufacturing holdouts.
    for L,b,K,o,e in [(1.2,.3,.9,.4,.05),(1.4,.4,1.1,.4,.1)]:
        r=toggle(L,b,K,o,e)
        assert r is not None
        for l1,l2,B,T in product((L-e,L-e/3,L+e/2,L+e),
                                (L-e,L+e/4,L+e),
                                (b-e,b,b+e),(K-e,K,K+e)):
            span=sqrt(l1*l1-B*B)+sqrt(l2*l2-B*B)
            over=l1+l2-span
            ret=span-sqrt(l1*l1-T*T)-sqrt(l2*l2-T*T)
            assert over<=r['overshoot']+1e-12
            assert ret>=r['retract']-1e-12
    return 'passed: sweep enclosures, refinement, unequal-link closure/extrema, supported logic'

def main():
    piv=[]
    for e in (.05,.10,.20):
        rejected={}; survivors=[]
        for a,o,t,h,theta in product((1.,1.5,2.),(.4,.6,.8),(.6,.8,1.),
                                    (2.,3.,4.),(45.,60.,75.,90.)):
            r=pivot_case(a,o,t,h,theta,e)
            row=dict(a=a,overlap=o,thick=t,height=h,angle=theta,**r)
            if r['margin']>0: survivors.append(row)
            else:
                reason=min(['withdrawal','back','engagement','width','lift'],
                           key=lambda k:r[k][1]-r[k][0] if k=='lift' else r[k])
                rejected[reason]=rejected.get(reason,0)+1
        piv.append({'error':e,'generated':324,'survivors':len(survivors),
                    'under_90_survivors':sum(r['angle']<90 for r in survivors),
                    'best_under_90':max((r for r in survivors if r['angle']<90),key=lambda x:x['margin'],default=None),
                    'best':max(survivors,key=lambda x:x['margin']) if survivors else None,
                    'reject_primary_reason':rejected})
    toggles=[]
    for e in (.05,.10,.20):
        rows=[]; rejected={}
        for L,b,K,o in product((1.,1.2,1.4,1.6),(.2,.3,.4),(.7,.9,1.1,1.3),(.4,.6,.8)):
            r=toggle(L,b,K,o,e)
            if r and min(r['back_margin'],r['open_margin'],r['deadcentre_margin'],r['pitch_margin'])>0:
                rows.append(dict(L=L,b=b,K=K,overlap=o,**r))
            else:
                reason='reach_domain' if r is None else min(
                    ('back_margin','open_margin','deadcentre_margin','pitch_margin'),key=lambda k:r[k])
                rejected[reason]=rejected.get(reason,0)+1
        toggles.append({'error':e,'generated':144,'survivors':len(rows),'reject_primary_reason':rejected,
                        'best':max(rows,key=lambda x:min(x['back_margin'],x['open_margin'],x['deadcentre_margin'],x['pitch_margin'])) if rows else None})
    # Gravity return inverse threshold: volume density are explicit scenarios.
    # Uniform bar width 2mm; bearing Coulomb friction mu*m*g*r, no service load.
    gravity=[]
    for rho,mu in product((.001,.0014),(.1,.5)): # g/mm^3
        L,t,w,theta,r=1.9,.6,2.,77*pi/180,.4
        weight=L*t*w*rho*.00981
        torque=weight*((L/2)*cos(theta)-mu*r)
        gravity.append({'density_g_mm3':rho,'mu':mu,'external_drag_limit_Nmm':torque,
                        'equivalent_tip_drag_N':torque/L})
    print(json.dumps({'checks':verify(),'crossbolt':[dict(error=e,**crossbolt(e)) for e in (.05,.1,.2)],'pivot':piv,'toggle':toggles,
                      'gravity':gravity,'logic':transition_checks()},indent=2))
if __name__=='__main__': main()
