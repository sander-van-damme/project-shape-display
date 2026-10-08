"""E-064 deterministic necessary-condition geometry/force synthesis; not FEA.
mm, N, kPa. NumPy only. --all emits every rejected/retained population.
"""
import argparse
import itertools
import json
import math
import numpy as np

PITCH, STROKE, COUNT = 5.08, 40.0, 6400


def sine_length(q, a, samples=1025):
    u = np.linspace(0, 1, samples)
    speed = np.sqrt(q*q + (2*np.pi*a*np.sin(2*np.pi*u))**2)
    ds = (speed[:-1]+speed[1:]) / (2*(samples-1))
    return float(ds.sum()), np.r_[0, np.cumsum(ds)], u


def sine_amplitude(q, length, upper, samples):
    if q > length:
        return None
    lo, hi = 0., upper
    for _ in range(38):
        mid = (lo+hi)/2
        if sine_length(q, mid, samples)[0] > length:
            hi = mid
        else:
            lo = mid
    return (lo+hi)/2


def sine_case(n, q0, a0, t, samples=257, states=41):
    # Mean radius fixed at 1.2 mm; axial period increases uniformly.
    # Material coordinates follow constant meridian arclength, not wave phase.
    rm = 1.2
    length, s0, u0 = sine_length(q0, a0, samples)
    q1 = q0+STROKE/n
    record = dict(family='sinusoidal', n=n, q0=q0, a0=a0, t=t,
                  compressed_mm=n*q0, extended_mm=n*q0+STROKE)
    if q1 >= length:
        return dict(record, reject=['insufficient_meridian_length'])
    material = np.linspace(0, 1, samples)
    r0 = np.interp(material, s0/length, rm+a0*np.cos(2*np.pi*u0))
    max_hoop = 0.
    min_curvature_radius = math.inf
    min_nonlocal = math.inf
    for q in np.linspace(q0, q1, states):
        a = sine_amplitude(q, length, a0, samples)
        _, s, u = sine_length(q, a, samples)
        r = rm+a*np.cos(2*np.pi*u)
        mapped = np.interp(material, s/s[-1], r)
        max_hoop = max(max_hoop, float(np.max(np.abs(mapped/r0-1))))
        # Exact maximum meridional curvature occurs at sinusoidal extrema.
        rho = q*q/(4*np.pi*np.pi*a) if a else math.inf
        min_curvature_radius = min(min_curvature_radius, rho)
        # Nonlocal mid-surface distance screen across three periods.
        # Only material separations >= one quarter meridian period are checked;
        # local offset regularity is screened independently by t/(2 rho).
        rr = np.tile(r[:-1], 3)
        zz = np.arange(len(rr))*q/(samples-1)
        ss = np.concatenate([s[:-1]+i*length for i in range(3)])
        middle = np.arange(samples-1, 2*(samples-1))
        d = np.hypot(rr[middle,None]-rr[None,:], zz[middle,None]-zz[None,:])
        d[np.abs(ss[middle,None]-ss[None,:]) < length/4] = np.inf
        min_nonlocal = min(min_nonlocal, float(d.min()))
    strain = t/(2*min_curvature_radius)
    # Explicit scenarios, NOT calibrated material limits.
    reject=[]
    if strain > 0.10: reject.append('bend_exceeds_10pct_scenario')
    if max_hoop > 0.20: reject.append('hoop_exceeds_20pct_scenario')
    if min_nonlocal < t: reject.append('nonlocal_skin_overlap')
    return dict(record, reject=reject, bend_strain=strain, hoop_strain=max_hoop,
                nonlocal_gap_mm=min_nonlocal-t, outer_radius_mm=rm+a0+t/2,
                curvature_radius_mm=min_curvature_radius)


def rolling_case(rp, gap, t, wall, error, bend_limit=.10, hoop_limit=.20):
    # gap: hardware radial clearance; membrane midlines occupy each wall.
    ri, ro = rp+t/2, rp+gap-t/2
    rho=(ro-ri)/2
    # Error is inward gap loss or outward pitch demand, applied conservatively.
    worst_rho=(gap-error-t)/2
    reject=[]
    if 2*(rp+gap+wall+error) > PITCH: reject.append('pitch')
    if worst_rho <= 0: reject.append('closed_convolution')
    bend = t/(2*worst_rho) if worst_rho>0 else math.inf
    hoop = (gap+error-t)/(rp+t/2)
    if bend > bend_limit+1e-12: reject.append('bend')
    if hoop > hoop_limit+1e-12: reject.append('hoop')
    # Material centreline lengths and sampled U sweep; piston stroke is axial.
    margin=1.
    length=STROKE+2*margin+math.pi*rho
    lengths=[]
    for x in np.linspace(0,STROKE,81):
        zc=(length+x-math.pi*rho)/2
        theta=np.linspace(0,math.pi,129)
        arc_r=(ri+ro)/2+rho*np.cos(theta)
        arc_z=zc+rho*np.sin(theta)
        assert arc_r.min() >= ri-1e-12 and arc_r.max() <= ro+1e-12
        assert zc-x >= margin-1e-12 and arc_z.max() <= STROKE+margin+rho+1e-12
        lengths.append(zc+(zc-x)+math.pi*rho)
    assert max(lengths)-min(lengths)<1e-10
    area=math.pi*((ri+ro)/2)**2
    return dict(family='rolling',rp=rp,gap=gap,t=t,wall=wall,error=error,
                reject=reject,bend_strain=(bend if math.isfinite(bend) else None),hoop_strain=hoop,
                effective_area_mm2=area,film_meridian_mm=length,
                skirt_swept_depth_mm=1.5*STROKE+margin+rho,
                cell_od_mm=2*(rp+gap+wall),
                volume_litres=COUNT*area*STROKE/1e6)


def inverse_roll(t, wall, error, b, h):
    # Smallest radial gap allowed by bending; smallest piston by hoop cycling.
    gap=t*(1+1/b)+error
    rp=(gap+error-t)/h-t/2
    row=rolling_case(rp,gap,t,wall,error,b,h)
    row.update(bend_limit=b,hoop_limit=h,required_pitch_mm=2*(rp+gap+wall+error))
    return row


def force_case(area, preload, k, drag, load, hysteresis, vent_kpa, cap_kpa):
    # Shared epistemic extremes; +/-30% spring and +/-10% area bounds.
    # Gravity omitted for descent. Include drag/hysteresis in both directions.
    up=(1.3*(preload+STROKE*k)+drag+load+hysteresis)/(0.9*area)*1000
    down=(0.7*preload-drag-hysteresis)/(1.1*area)*1000
    return dict(area_mm2=area,preload_N=preload,k_N_per_mm=k,drag_N=drag,
                load_N=load,hysteresis_N=hysteresis,vent_kpa=vent_kpa,
                cap_kpa=cap_kpa,raise_min_kpa=up,lower_max_kpa=down,
                reject=(['raise_pressure'] if up>cap_kpa else [])+
                       (['return_stall'] if down<vent_kpa else []))


def verify():
    assert abs(sine_length(1,0)[0]-1)<1e-12
    assert sine_amplitude(2,1,1,257) is None
    # Independent flat-profile maximum arclength bound: L <= q+4a.
    assert sine_length(.6,.7)[0] <= .6+4*.7
    f=force_case(10,1,0,0,0,0,0,300)
    assert abs(f['raise_min_kpa']-1000*1.3/9)<1e-10
    assert abs(f['lower_max_kpa']-1000*.7/11)<1e-10
    r=rolling_case(1.2,.25,.025,.4,0)
    # Work-volume identity, Pa*m3 = N*m, for ideal rolling area.
    p=50_000; a=r['effective_area_mm2']*1e-6
    assert abs(p*a*.04*COUNT-p*r['volume_litres']/1000)<1e-10
    inv=inverse_roll(.025,.4,.05,.1,.2)
    assert abs(inv['required_pitch_mm']-2*(60.5*.025+12*.05+.4))<1e-12
    assert not inv['reject']
    assert inverse_roll(.030,.4,.05,.1,.2)['reject']==['pitch']
    convergence=[]
    for points,states in [(129,21),(257,41),(513,81)]:
        s=sine_case(40,.6,.7,.025,points,states)
        convergence.append({k:s[k] for k in ['bend_strain','hoop_strain','nonlocal_gap_mm']})
    assert abs(convergence[-1]['hoop_strain']-convergence[-2]['hoop_strain'])<.002
    return convergence


def summary(rows):
    reasons={}
    for row in rows:
        for reason in row['reject']: reasons[reason]=reasons.get(reason,0)+1
    return dict(total=len(rows),survivors=sum(not r['reject'] for r in rows),reasons=reasons)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--all',action='store_true')
    args=parser.parse_args()
    check=verify()
    # Factor thickness after geometry to avoid recomputing identical sweeps.
    sine=[]
    for n,q,a in itertools.product([20,40,60],[.3,.6,1.],[.4,.7,1.]):
        base=sine_case(n,q,a,.025)
        for t in [.025,.05,.1]:
            row=dict(base,t=t)
            if 'bend_strain' in base:
                row['bend_strain']=base['bend_strain']*t/.025
                row['nonlocal_gap_mm']=base['nonlocal_gap_mm']+.025-t
                row['outer_radius_mm']=1.2+a+t/2
                row['reject']=[]
                if row['bend_strain']>.10:row['reject'].append('bend_exceeds_10pct_scenario')
                if row['hoop_strain']>.20:row['reject'].append('hoop_exceeds_20pct_scenario')
                if row['nonlocal_gap_mm']<0:row['reject'].append('nonlocal_skin_overlap')
            sine.append(row)
    roll=[rolling_case(*p) for p in itertools.product([.8,1.2,1.6],[.15,.25,.3,.35,.4,.6],[.025,.05,.1],[.4,.6],[0,.05,.15])]
    sensitivity={str((b,h)):summary([rolling_case(r['rp'],r['gap'],r['t'],r['wall'],r['error'],b,h) for r in roll]) for b,h in [(.05,.1),(.1,.2),(.2,.4)]}
    inverse=[inverse_roll(*p) for p in itertools.product([.025,.030,.05,.1],[.4,.6],[0,.05,.15],[.05,.1,.2],[.1,.2,.4])]
    force=[force_case(*p) for p in itertools.product([4.,7.,10.],[.1,.25,.5],[.002,.01,.03],[.02,.1],[.05,.2,1.],[0.,.05,.2],[.5,2.],[30.,100.,300.])]
    out=dict(units='mm N kPa; strain dimensionless; deterministic epistemic scenarios',verification=check,
             sinusoidal=summary(sine),rolling=summary(roll),rolling_by_error={str(e):summary([r for r in roll if r['error']==e]) for e in [0,.05,.15]},
             rolling_strain_sensitivity=sensitivity,force=summary(force),
             rolling_survivors=[r for r in roll if not r['reject']],
             inverse_rolling=summary(inverse),
             inverse_witness=inverse_roll(.025,.4,.05,.1,.2),
             film_variation_witness=inverse_roll(.030,.4,.05,.1,.2),
             force_witness=force_case(inverse_roll(.025,.4,.05,.1,.2)['effective_area_mm2'],.25,.002,.02,.2,.05,2,100))
    if args.all:out.update(sine_population=sine,rolling_population=roll,force_population=force,inverse_population=inverse)
    print(json.dumps(out,indent=2,allow_nan=False))

if __name__=='__main__':main()
