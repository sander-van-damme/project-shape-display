#!/usr/bin/env python3
"""E-071: necessary rigid datum equilibrium; N, mm, J, s. No calibrated priors."""
import importlib.util
import json
import math
from pathlib import Path
from itertools import product
import sys

p = Path(__file__).resolve().parents[1] / 'E-070' / 'guide_packing.py'
spec = importlib.util.spec_from_file_location('guide_packing_e070', p)
gp = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gp
spec.loader.exec_module(gp)


def datum_geometry(length):
    g = gp.geometry('captured_t', .15, .2, .4, length)
    # Two nominal 0.4-mm-tall left datum pads fill the former 0.2-mm gap.
    # Their faces intentionally touch the flange; preload source is idealized.
    xl = -g['wing']
    pads = [gp.box('datum_'+str(i), xl-g['gap'], xl, 1.6, 2., z, z+.4)
            for i,z in enumerate([2., 2.+length-.4])]
    assert gp.connected(g['fixed']+pads)
    assert not gp.collisions(g['moving'], pads, 2, -g['failed_drop'],
                             g['stroke']+g['unload'])
    # Each pad remains opposed by flange, not merely by empty space.
    flange = next(s for s in g['moving'] if s.name=='flange')
    for z in [-g['failed_drop'],g['stroke']+g['unload']]:
        f=flange.move(2,z)
        assert all(f.lo[2] <= pad.lo[2] and f.hi[2] >= pad.hi[2] for pad in pads)
    # Reference at the new left contact face; actual fork/dog overlap interval.
    drive_lo=max(g['dog'].lo[0], g['rail'][0].lo[0])-xl
    drive_hi=min(g['dog'].hi[0], g['rail'][0].hi[0])-xl
    return dict(length=length, span=length-.8, optimistic_span=length,
                datum_x=xl, shoe_x=g['spine']+2*g['wing'],
                load_x=g['spine']/2-xl, drive=[drive_lo,drive_hi],
                side_height=g['dog_z']+.6-(2.+length/2),
                width=g['width'], depth=g['depth'])


def reactions(P, S, mu, W, H, dv, dw, b, a, direction):
    # x balance: N=P-H; z balance: V=W+s*mu*(N+P).
    N=P-H
    V=W+direction*mu*(N+P)
    M=dv*V-dw*W-direction*b*mu*P-a*H
    lower=N/2-M/S
    upper=N/2+M/S
    return lower,upper,V


def preload_interval(S, mu, W, H, dv, dw, b, a, direction):
    # All inequalities affine in P. Solve exactly, no grid over preload.
    lo=max(0.,H); hi=math.inf
    r0=reactions(0.,S,mu,W,H,dv,dw,b,a,direction)
    r1=reactions(1.,S,mu,W,H,dv,dw,b,a,direction)
    for q0,q1 in zip(r0[:2],r1[:2]):
        slope=q1-q0
        if abs(slope)<1e-12:
            if q0 < -1e-10: return None
        elif slope>0: lo=max(lo,-q0/slope)
        else: hi=min(hi,-q0/slope)
    if lo>hi+1e-9: return None
    return lo,hi


def screen(length, mu_max, W, Hmax):
    g=datum_geometry(length)
    corners=list(product([0.,mu_max],[0.,W],[-Hmax,Hmax],g['drive'],[-1,1]))
    intervals=[preload_interval(g['span'],mu,w,h,dv,g['load_x'],g['shoe_x'],
                               g['side_height'],s) for mu,w,h,dv,s in corners]
    if any(r is None for r in intervals):
        return dict(length=length,mu_max=mu_max,load_max_N=W,side_max_N=Hmax,
                    result='no_preload_equilibrium')
    lo=max(r[0] for r in intervals); hi=min(r[1] for r in intervals)
    if lo>hi+1e-9:
        return dict(length=length,mu_max=mu_max,load_max_N=W,side_max_N=Hmax,
                    result='incompatible_preloads')
    # Conditions multi-affine in uncertain inputs at fixed P: box extrema suffice.
    P=lo
    upward=max(reactions(P,g['span'],mu,w,h,dv,g['load_x'],g['shoe_x'],
                          g['side_height'],s)[2] for mu,w,h,dv,s in corners)
    friction=mu_max*(2*P+Hmax)
    return dict(length=length,mu_max=mu_max,load_max_N=W,side_max_N=Hmax,
                result='ideal_preload_only',minimum_preload_N=P,
                max_upward_drive_N=upward,max_sliding_friction_N=friction,
                uniform_6400_cell_40mm_friction_J=6400*.04*friction,
                bank_80_max_upward_N=80*upward)


def checks():
    for L in [1.6,4.,8.,12.,20.,11.137]:
        g=datum_geometry(L)
        for P,mu,W,H,dv,s in product([.1,3.,31.],[0.,.23,.6],[.1,1.,10.],
                                    [-.2,0.,.2],g['drive'],[-1,1]):
            nl,nu,V=reactions(P,g['span'],mu,W,H,dv,g['load_x'],g['shoe_x'],g['side_height'],s)
            assert abs(nl+nu+H-P)<1e-9
            assert abs(V-W-s*mu*(nl+nu+P))<1e-9
            moment=(g['span']/2)*(nl-nu)+dv*V-g['load_x']*W-s*g['shoe_x']*mu*P-g['side_height']*H
            assert abs(moment)<1e-8
        # Independent frictionless closed form with H=0.
        expected=2*(g['drive'][1]-g['load_x'])*10/g['span']
        actual=screen(L,0.,10.,0.)
        assert math.isclose(actual['minimum_preload_N'],expected)
        # Closed-form upward friction feedback limit, even at ideal endpoints.
        mucrit=L/(2*(2*g['drive'][1]-g['shoe_x']))
        assert preload_interval(L,mucrit+.01,1.,0.,g['drive'][1],g['load_x'],
                                 g['shoe_x'],g['side_height'],1) is None
    # A long support is a conditional escape; short high-friction guides fail.
    assert screen(4.,.6,1.,0.)['result']=='no_preload_equilibrium'
    assert screen(12.,.6,1.,.2)['result']=='ideal_preload_only'
    assert math.isclose(screen(12.,0.,0.,0.)['minimum_preload_N'],0.)
    # Interior holdout: reconstruct contact signs away from scenario corners.
    r=screen(11.137,.43,1.7,.13); g=datum_geometry(11.137)
    assert r['result']=='ideal_preload_only'
    for mu,W,H,dv,s in product([.071,.317,.43],[.11,.79,1.7],[-.13,.041,.13],
                              [g['drive'][0],sum(g['drive'])/2,g['drive'][1]],[-1,1]):
        n1,n2,_=reactions(r['minimum_preload_N'],g['span'],mu,W,H,dv,
                          g['load_x'],g['shoe_x'],g['side_height'],s)
        assert min(n1,n2)>=-1e-8


def main():
    checks()
    geometries=[datum_geometry(L) for L in [1.6,4.,8.,12.,20.]]
    rows=[screen(L,mu,W,H) for L,mu,W,H in product([1.6,4.,8.,12.,20.],
                                                               [.2,.4,.6],[.1,1.,10.],[0.,.2])]
    out=dict(evidence='necessary rigid sliding equilibrium and nominal datum pad sweeps; no machine pass',
             scenarios=len(rows),rejected=sum(r['result']!='ideal_preload_only' for r in rows),
             geometry=geometries,
             optimistic_friction_thresholds=[dict(length=g['length'],mu_max=g['optimistic_span']/(2*(2*g['drive'][1]-g['shoe_x']))) for g in geometries],
             representative=[r for r in rows if r['mu_max']==.6 and r['load_max_N']==1. and r['side_max_N']==.2],
             rear_separate_guide_minimum_depth_mm=4.95+.8+2*(.05+.15)+2*.4+.15)
    if '--all' in sys.argv: out['population']=rows
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
