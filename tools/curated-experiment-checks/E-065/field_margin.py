#!/usr/bin/env python3
"""E-065: finite closed conductor loops; bounded scalar flag discriminator.
Run with Python 3 + numpy. All distances SI internally; output mT/A.
No ferromagnetics, flag dynamics, process priors or yield predictions.
"""
import argparse
import itertools
import json
import math
import numpy as np

PITCH = .00508
MU_FACTOR = 1e-7  # mu0/(4*pi), sufficient precision for this screen
AXIS = np.array([1., -1., 0.]) / math.sqrt(2)


def segment(points, a, b):
    """Exact integral of dl cross r / |r|^3 for a finite line segment."""
    a, b = np.asarray(a), np.asarray(b)
    length = np.linalg.norm(b-a)
    direction = (b-a)/length
    r = points-a
    along = r @ direction
    perp = r-along[..., None]*direction
    radius2 = np.sum(perp*perp, axis=-1)
    assert np.all(radius2 > 1e-20), 'observation on wire axis'
    factor = (along/np.sqrt(radius2+along**2)
              -(along-length)/np.sqrt(radius2+(along-length)**2))/radius2
    return MU_FACTOR*np.cross(direction, perp)*factor[..., None]


def loop(points, corners):
    return sum(segment(points, a, b)
               for a, b in zip(corners, corners[1:]+corners[:1]))


def influence(n, h, return_mm, offset=(0., 0., 0.)):
    yy, xx = np.indices((n, n))
    points = np.stack([xx.ravel()*PITCH, yy.ravel()*PITCH,
                       np.zeros(n*n)], axis=1)+np.array(offset)
    low, high = -.010, (n-1)*PITCH+.010
    rows, cols = [], []
    for k in range(n):
        q = k*PITCH
        ret = high+.010 if return_mm == 'edge' else q+return_mm/1000
        rows.append(loop(points, [(low,q,-h),(high,q,-h),
                                  (high,ret,-h),(low,ret,-h)]) @ AXIS)
        # Separate planes by 0.2 mm; rotate row loop x->y, y->x.
        cols.append(loop(points, [(q,low,-h-.0002),(q,high,-h-.0002),
                                  (ret,high,-h-.0002),(ret,low,-h-.0002)]) @ AXIS)
    return np.array(rows), np.array(cols)


def extrema(rows, cols, e=0.):
    """One active row; arbitrary subset of same-polarity columns.
    Independent line-current +/-e boxes: conservative for correlated droop.
    Exact bitmask extrema because field is affine in each column bit.
    Nonselected sites must resist either sign (set or reset).
    """
    n = len(rows)
    yy, xx = np.indices((n,n))
    yy, xx = yy.ravel(), xx.ravel()
    idx = np.arange(n*n)
    rlo, rhi = rows-e*abs(rows), rows+e*abs(rows)
    clo, chi = cols-e*abs(cols), cols+e*abs(cols)
    neg, pos = np.minimum(clo,0).sum(axis=0), np.maximum(chi,0).sum(axis=0)
    ownlo, ownhi = clo[xx,idx], chi[xx,idx]
    selected_min = float('inf')
    unwanted_max = 0.
    for r in range(n):
        chosen = yy == r
        sel = rlo[r]+neg-np.minimum(ownlo,0)+ownlo
        selected_min = min(selected_min, float(sel[chosen].min()))
        # Selected row, own column OFF; elsewhere all column subsets allowed.
        lo = rlo[r]+neg-np.where(chosen,np.minimum(ownlo,0),0)
        hi = rhi[r]+pos-np.where(chosen,np.maximum(ownhi,0),0)
        unwanted_max = max(unwanted_max,float(np.maximum(abs(lo),abs(hi)).max()))
    return selected_min, unwanted_max


def brute(rows, cols, e=0.):
    n=len(rows); s=float('inf'); u=0.
    yy,xx=np.indices((n,n)); yy,xx=yy.ravel(),xx.ravel()
    for r in range(n):
        for values in itertools.product((0.,1.-e,1.+e),repeat=n):
            values=np.array(values)
            for row_current in (1.-e,1.+e):
                field=row_current*rows[r]+values@cols
                sel=(yy==r)&(values[xx]>0)
                if sel.any():s=min(s,float(field[sel].min()))
                if (~sel).any():u=max(u,float(abs(field[~sel]).max()))
    return s,u


def verify():
    # Independent midpoint Biot-Savart quadrature on a skew segment.
    a=np.array([-.013,-.006,-.002]);b=np.array([.014,.008,.001])
    p=np.array([[.001,-.002,.007]])
    exact=segment(p,a,b)[0];errors=[]
    for count in (200,400,800):
        dl=(b-a)/count
        mid=a+(np.arange(count)+.5)[:,None]*dl
        rr=p-mid
        quadrature=MU_FACTOR*np.sum(np.cross(dl,rr)/np.linalg.norm(rr,axis=1)[:,None]**3,axis=0)
        errors.append(float(np.linalg.norm(quadrature-exact)/np.linalg.norm(exact)))
    assert errors[-1]<1e-6 and errors[0]>3.9*errors[1]>3.9**2*errors[2]
    # Infinite-wire limiting case and reversal.
    p=np.array([[0.,0.,.001]])
    field=segment(p,[-10.,0.,0.],[10.,0.,0.])[0]
    assert np.allclose(field,[0.,-2e-4,0.],rtol=1e-8,atol=1e-14)
    assert np.allclose(segment(p,[10.,0.,0.],[-10.,0.,0.]),-field)
    rows,cols=influence(4,.0008,1.)
    for e in (0.,.15):
        assert np.allclose(extrema(rows,cols,e),brute(rows,cols,e),rtol=1e-12,atol=1e-15)
    # Identically zero currents and an isolated scalar ideal 2:1 case.
    assert extrema(np.zeros_like(rows),np.zeros_like(cols))==(0.,0.)
    assert np.allclose(extrema(np.eye(2).repeat(2,axis=1),
                               np.tile(np.eye(2),(1,2))), (2.,1.))
    return {'quadrature_relative_errors_200_400_800':errors,
            'checks':'finite-segment quadrature, infinite wire, reversal, zero, ideal 2:1, exhaustive 4-column masks/current corners'}


def scan():
    output=[]
    for h_mm,ret in itertools.product((.4,.8,1.2),(1.,2.,'edge')):
        for name,offset_mm,current_error,threshold_spread in (
                ('nominal',0.,0.,0.),('tight',.05,.05,.05),
                ('middle',.15,.15,.15),('wide',.30,.15,.30)):
            # Corners + center are stress cases, NOT a certified continuous-box bound.
            offsets=[(0.,0.,0.)] if offset_mm==0 else [(0.,0.,0.)]+list(itertools.product((-offset_mm/1000,offset_mm/1000),repeat=3))
            smin=float('inf');umax=0.
            for off in offsets:
                s,u=extrema(*influence(80,h_mm/1000,ret,off),current_error)
                smin=min(smin,s);umax=max(umax,u)
            low=umax/(1-threshold_spread);high=smin/(1+threshold_spread)
            output.append({'h_mm':h_mm,'return_mm':ret,'scenario':name,
                           'placement_cases':len(offsets),'selected_min_mT_A':smin*1000,
                           'unwanted_max_mT_A':umax*1000,
                           'threshold_interval_mT_A':[low*1000,high*1000],
                           'margin_mT_A':(high-low)*1000,
                           'sampled_window':bool(high>low)})
    return output


def burden():
    # Explicit copper resistivity scenario, not a qualified wire purchase.
    length=2*((79*PITCH+.020)+.001)
    resistance=1.72e-8*length/(.2e-3*.035e-3)
    return {'loop_length_m':length,'trace_R_ohm_at_assumed_rho':resistance,
            'two_arrays_conductor_m':320*length,
            'two_arrays_81_lines_each_P_W_at_1A':162*resistance,
            'two_arrays_81_lines_each_P_W_at_1_5A':162*resistance*1.5**2,
            'nominal_driver_count_dual_H_bridge':160,
            'row_phase_budget_ms_sequential_arrays_two_polarities':(30-(.6+8*2*math.sqrt(10/500)+6))/(9*80*2*2)*1000,
            'driver_unit_allowance_USD':{str(reserve):(500-reserve)/160 for reserve in (150,250,350)},
            'guided_normalized_leakage_allowance':[
                {'field_error':e,'threshold_spread':d,
                 'L_max':(1-3*e-3*d+e*d)/2}
                for e,d in ((.05,.05),(.15,.15),(.25,.30))]}


def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
    checks=verify()
    if args.check:print(json.dumps(checks,indent=2));return
    rows=scan()
    print(json.dumps({'checks':checks,'grid':rows,'burden':burden()},indent=2))

if __name__=='__main__':main()
