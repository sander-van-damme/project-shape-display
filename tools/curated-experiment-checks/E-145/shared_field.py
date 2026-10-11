#!/usr/bin/env python3
"""E-145 finite reluctance networks; SI; explicit bounds, no fitted process priors.
Not FEM, hysteresis, contact dynamics, a coil design or hardware qualification.
"""
import itertools
import json
import math

import numpy as np

MU0 = 4*math.pi*1e-7
RHO_CU = 1.72e-8  # assumed room-temperature engineering value


def iron_drop(phi, area, length, mur=1000, knee=1.5):
    b = phi/area
    return length/MU0*(min(b, knee)/mur + max(b-knee, 0))


def iron_energy(phi, area, length, mur=1000, knee=1.5):
    b = phi/area
    lo, hi = min(b, knee), max(b-knee, 0)
    return area*length/MU0*(lo*lo/(2*mur)+hi*knee/mur+hi*hi/2)


def invert_branch(v, gap, area, length, mur, knee):
    slope = (2*gap+length/mur)/(MU0*area)
    pk = knee*area
    if v <= slope*pk:
        return v/slope
    return pk+(v-slope*pk)*MU0*area/(2*gap+length)


def parallel(ampturn, gaps, area=.0004, root=.0016, mur=1000,
             knee=1.5, leak=.2, common_length=.32, branch_length=.06):
    """Shared finite root, n two-gap branches, explicit bypass leakage.
    Uniform root is a geometry surrogate, not a distributed rail or bound.
    Leakage permeance fixed to leak*n times reference 0.6-mm-gap permeance.
    """
    rleak = .0012/(MU0*area*len(gaps)*leak) if leak else math.inf
    def branches(v):
        return [invert_branch(v, g, area, branch_length, mur, knee) for g in gaps]
    lo, hi = 0., ampturn
    for _ in range(65):
        v = (lo+hi)/2
        total = sum(branches(v))+v/rleak
        if v+iron_drop(total, root, common_length, mur, knee) > ampturn:
            hi = v
        else:
            lo = v
    v = (lo+hi)/2
    phis = branches(v)
    total = sum(phis)+v/rleak
    energy = iron_energy(total, root, common_length, mur, knee)+v*v/(2*rleak)
    energy += sum(p*p*g/(MU0*area)+iron_energy(p, area, branch_length,mur,knee)
                  for p,g in zip(phis,gaps))
    return dict(flux=total, branch_flux=phis, force=[p*p/(MU0*area) for p in phis],
                root_B=total/root, energy=energy, coenergy=ampturn*total-energy,
                mmf_error=abs(v+iron_drop(total,root,common_length,mur,knee)-ampturn))


def rail_bank(ampturn, gaps, area=.0004, root=.0016, mur=1000, knee=1.5):
    """Four physical taps, two 40-mm rail segments per tap; 60-mm root.
    Independent Newton solution of convex magnetic energy with flux continuity.
    Fifth unknown is a leakage bypass at the root, as in the lumped model.
    """
    n=len(gaps)
    paths=[]
    for i,g in enumerate(gaps):
        v=np.zeros(n+1);v[i]=1
        paths.append((v,area,.12,2*g/(MU0*area)))
    paths.append((np.ones(n+1),root,.06,0))
    for k in range(n):
        v=np.zeros(n+1);v[k:n]=1
        paths.append((v,root,.08,0))
    v=np.zeros(n+1);v[-1]=1
    paths.append((v,1,0,.0012/(MU0*area*n*.2)))
    def evaluate(x):
        residual=np.full(n+1,-ampturn,dtype=float)
        jac=np.zeros((n+1,n+1)); energy=-ampturn*sum(x)
        for v,a,l,r in paths:
            phi=float(v@x)
            if phi < 0: raise ValueError('negative flux outside this unipolar model')
            drop=r*phi+iron_drop(phi,a,l,mur,knee)
            slope=r+l/(MU0*a)*(1/mur if phi/a<knee else 1)
            residual+=v*drop;jac+=np.outer(v,v)*slope
            energy+=r*phi*phi/2+iron_energy(phi,a,l,mur,knee)
        return residual,jac,energy
    x=np.zeros(n+1)
    for iteration in range(100):
        r,j,e=evaluate(x)
        if max(abs(r))<1e-7: break
        dx=np.linalg.solve(j,-r)
        alpha=1.
        while np.any(x+alpha*dx<0) or evaluate(x+alpha*dx)[2]>e+1e-4*alpha*(r@dx):
            alpha*=.5
            if alpha<1e-12: raise AssertionError('Newton line search stalled')
        x+=alpha*dx
    else: raise AssertionError('Newton iteration limit')
    return dict(force=[float(p*p/(MU0*area)) for p in x[:n]],
                iterations=iteration,residual_AT=float(max(abs(evaluate(x)[0]))))


def series(ampturn, gaps, area=.0001, mur=1000, knee=1.5, length=.4):
    # Single serpentine circuit, two moving gaps per independent armature.
    phi = invert_branch(ampturn,sum(gaps),area,length,mur,knee)
    return dict(flux=phi, force=phi*phi/(MU0*area), B=phi/area)


def coil(ampturn, turns=400, copper_window=.0002, mean_turn=.25):
    # copper_window = fill factor * gross winding window; no free packing.
    resistance = RHO_CU*turns*turns*mean_turn/copper_window
    return dict(turns=turns,current_A=ampturn/turns,resistance_ohm=resistance,
                power_W=RHO_CU*ampturn*ampturn*mean_turn/copper_window,
                copper_kg=8960*copper_window*mean_turn)


def decay(ampturn, cutoff, clamp, steps=256):
    # Armatures frozen at attracted stops. Includes nonlinear flux linkage.
    # dt = -d(lambda)/(R*i+Vclamp). Does NOT integrate moving armatures.
    c = coil(ampturn)
    turns, resistance = c['turns'], c['resistance_ohm']
    result = 0.
    for j in range(steps):
        a = cutoff+(ampturn-cutoff)*j/steps
        b = cutoff+(ampturn-cutoff)*(j+1)/steps
        fa = parallel(a,[.0002]*4)['flux']
        fb = parallel(b,[.0002]*4)['flux']
        result += turns*(fb-fa)/(resistance*(a+b)/(2*turns)+clamp)
    return result


def min_heads(extra):
    return next(h for h in range(1,6401) if 6+math.ceil(6400/h)*(.45+extra)<30)


def main():
    out = {}
    # E-144 loads at mu=.02, rescaled together to .1 (competing friction box).
    out['load_boxes'] = []
    for mu in (.02,.1,.3):
        scale=.02/mu
        out['load_boxes'].append(dict(mu=mu, opening_peak_N=1080*scale,
            opening_work_J=(960*.0004+.5*200000*.0004**2+40*.0004)*scale,
            return_start_N=(640+80-40)*scale, contact_hold_N=mu*(640-40)*scale))
    mmf=1100.
    out['parallel_states']={}
    for name,gaps in [('all_rest',[.0006]*4),('one_attracted',[.0002]+[.0006]*3),
                      ('three_attracted',[.0002]*3+[.0006]),('all_attracted',[.0002]*4),
                      ('one_missing_armature',[.010]+[.0006]*3)]:
        out['parallel_states'][name]=parallel(mmf,gaps)
    out['distributed_holdout']={name:rail_bank(mmf,gaps) for name,gaps in [
        ('all_rest',[.0006]*4),('near_three_attracted',[.0002]*3+[.0006]),
        ('far_three_attracted',[.0006]+[.0002]*3)]}
    out['state_sweep']=[]
    for root in (.0008,.0016,.0032):
        needed=[]
        # Complete endpoint state enumeration; moving heads must defeat 216 N.
        # Grant that full stroke force at start: deliberately sufficient screen.
        for bits in itertools.product((0,1),repeat=4):
            if all(bits): continue
            gaps=[.0002 if b else .0006 for b in bits]
            lo,hi=0.,20000.
            while min(fi for fi,b in zip(parallel(hi,gaps,root=root)['force'],bits) if not b)<216:
                hi*=2
            for _ in range(40):
                a=(lo+hi)/2
                f=parallel(a,gaps,root=root)['force']
                if min(fi for fi,b in zip(f,bits) if not b)>=216: hi=a
                else: lo=a
            needed.append(hi)
        out['state_sweep'].append(dict(root_mm2=root*1e6,
            min_required_AT=min(needed) if min(needed)<20000 else '>20000',
            max_required_AT=max(needed) if max(needed)<20000 else '>20000'))
    out['uncertainty_corners']=[]
    # Coherent errors across the bank: no iid sampling, no yield inference.
    for bias,area_scale,mur,knee,leak in itertools.product(
            (-.0001,.00015),(.8,1.),(200,5000),(1.3,1.8),(0.,.5)):
        r=parallel(mmf,[.0006+bias]*4,area=.0004*area_scale,
                   mur=mur,knee=knee,leak=leak)
        out['uncertainty_corners'].append(min(r['force']))
    out['corner_summary']=dict(count=len(out['uncertainty_corners']),
        min_force_N=min(out['uncertainty_corners']),max_force_N=max(out['uncertainty_corners']),
        passes_216N=sum(f>=216 for f in out['uncertainty_corners']))
    del out['uncertainty_corners']
    out['fringing_force_factor']={str(k):k*parallel(mmf,[.0006]*4)['force'][0] for k in (.7,1.,1.2)}
    out['coil']=coil(mmf)
    out['hold_coil']=coil(600)
    c=coil(mmf)
    inductance=400*parallel(mmf,[.0006]*4)['flux']/c['current_A']
    start_current=c['current_A']*math.sqrt(200/out['parallel_states']['all_rest']['force'][0])
    out['fixed_rest_rise_ms']={str(v):1000*(-inductance/c['resistance_ohm']*
        math.log(1-start_current*c['resistance_ohm']/v)) for v in (12,24)}
    out['slab_diffusion_diagnostic']=[dict(thickness_mm=d*1000,
        tau_ms=[1000*MU0*mur*d*d/(math.pi**2*1e-7) for mur in (50,1000)])
        for d in (.0005,.005,.02,.04)]

    out['series_lever']={}
    # 4:1 armature travel / pad travel; area divided by four, 216/4 N needed.
    for name,gaps in [('rest',[.0018]*4),('three_attracted',[.0002]*3+[.0018]),
                      ('one_jammed_rest',[.0018]+[.0002]*3)]:
        target=math.sqrt(54*MU0/.0001)
        needed=2*sum(gaps)*target/MU0 + iron_drop(target*.0001,.0001,.4)
        out['series_lever'][name]=dict(required_AT=needed,B=target,
            coil=coil(needed,copper_window=.0002,mean_turn=.12))
    # Independent coil control: same poles/local return, no shared flux path.
    target=math.sqrt(216*MU0/.0004)
    independent_at=target*(.0012+.10/1000)/MU0
    out['independent_custom_coil']=dict(required_AT=independent_at,
        coil=coil(independent_at,mean_turn=.10,copper_window=.0001))
    threshold_lo,threshold_hi=0.,mmf
    for _ in range(50):
        a=(threshold_lo+threshold_hi)/2
        if parallel(a,[.0002]*4)['force'][0]>136: threshold_hi=a
        else: threshold_lo=a
    cutoff=threshold_hi
    out['decay']={'return_start_AT':cutoff,'frozen_stored_J':parallel(mmf,[.0002]*4)['energy'],
        'convergence':[]}
    for steps in (64,128,256,512):
        out['decay']['convergence'].append(dict(steps=steps,
            diode_start_ms=1000*decay(mmf,cutoff,.7,steps),
            clamp_start_ms=1000*decay(mmf,cutoff,48,steps),
            diode_zero_ms=1000*decay(mmf,0,.7,steps),
            clamp_zero_ms=1000*decay(mmf,0,48,steps)))
    out['remanence_contact']=[dict(gap_B_T=b,magnetic_N=b*b*.0008/(2*MU0),
        grip_N=.1*(128-8-b*b*.0008/(2*MU0))) for b in (0,.1,.3,.6)]
    out['schedule']=[dict(extra_s=x,heads=min_heads(x),
        residual_USD=250-1.56*min_heads(x)) for x in (0,.01,.05,.1,.2,.6)]
    # Explicit rectangular iron stock volume (not an optimized lower bound).
    iron_volume=2*.16*.0016+4*(2*.03*.0004+.06*.0004)+.06*.0016
    out['stock']=dict(iron_kg_bank=7870*iron_volume, copper_kg_bank=coil(mmf)['copper_kg'],
        banks_at_121_heads=math.ceil(121/4),
        iron_kg_31_banks=31*7870*iron_volume,copper_kg_31_banks=31*coil(mmf)['copper_kg'])
    # Self-review: infinite-root independent analytic limit, NI balance, force via
    # coenergy derivative, power identity and independent linear energy identity.
    r=parallel(200,[.0006]*4,common_length=0,leak=0)
    expected=200*MU0*.0004/(.0012+.06/1000)
    assert math.isclose(r['branch_flux'][0],expected,rel_tol=1e-12)
    assert math.isclose(r['energy'],r['coenergy'],rel_tol=1e-12)
    assert max(x['mmf_error'] for x in out['parallel_states'].values()) < 1e-7
    g=[.0002,.0006,.0006,.0006]
    eps=1e-9
    gp=g.copy(); gm=g.copy(); gp[1]+=eps;gm[1]-=eps
    force_fd=-(parallel(mmf,gp)['coenergy']-parallel(mmf,gm)['coenergy'])/(2*eps)
    force=parallel(mmf,g)['force'][1]
    assert math.isclose(force_fd,force,rel_tol=1e-6)
    assert parallel(0,g)['flux']==0
    c=coil(mmf)
    assert math.isclose(c['power_W'],c['current_A']**2*c['resistance_ohm'])
    assert math.isclose(series(100,[.001]*4)['flux'],
                        series(100,[.004])['flux'])
    assert min_heads(0)==121
    assert min(out['distributed_holdout']['all_rest']['force'])>216
    assert out['distributed_holdout']['near_three_attracted']['force'][-1]<200
    assert out['distributed_holdout']['far_three_attracted']['force'][0]<200
    assert out['state_sweep'][-1]['max_required_AT']<1100
    assert out['decay']['convergence'][-1]['clamp_start_ms'] < out['decay']['convergence'][-1]['diode_start_ms']

    out['checks']=dict(coenergy_force_N=force_fd,stress_force_N=force,
                      passed=True,kind='self-review of reduced model')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
