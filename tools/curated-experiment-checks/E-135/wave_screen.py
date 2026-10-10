#!/usr/bin/env python3
"""E-135: deterministic necessary-condition screens; no measured process priors.
Python + NumPy. Prints reproducible results, never writes generated artifacts.
"""
import itertools
import json
import math
import numpy as np


# Energy barrier +/-20%, forcing gain +/-10%; amplitude ratio needed.
REQUIRED = math.sqrt(1.2 / .8) * 1.1 / .9


def solve_chain(diag, off, rhs):
    """Complex tridiagonal solve, independently checked against dense solve."""
    d, b = diag.copy(), rhs.astype(complex).copy()
    for i in range(1, len(d)):
        r = off[i-1] / d[i-1]
        d[i] -= r * off[i-1]
        b[i] -= r * b[i-1]
    b[-1] /= d[-1]
    for i in range(len(d)-2, -1, -1):
        b[i] = (b[i] - off[i] * b[i+1]) / d[i]
    return b


def spectrum(n, q, coupling, pattern):
    # Frequency in units of low-band angular frequency; mass=1.
    nominal = np.geomspace(1., 10., n)
    local = np.where(np.arange(n) % 2, -.01, .01)
    shifts = {'ideal': np.zeros(n), 'alternating_1pct': local,
              'common_5pct': np.full(n, .05),
              'split_bank_5pct_plus_local': np.where(np.arange(n)<n//2,.05,-.05)+local}
    w = nominal * (1 + shifts[pattern])
    springs = coupling * np.minimum(w[:-1], w[1:])**2
    stiffness = w*w + np.r_[springs, 0.] + np.r_[0., springs]
    worst = (float('inf'), None)
    for target, drive in enumerate(nominal):
        diagonal = (stiffness - drive*drive + 1j*drive*w/q).astype(complex)
        response = solve_chain(diagonal, -springs, np.ones(n))
        # Peak local spring+kinetic energy normalized by .5*w_i^2*s^2,
        # s=1: max(w_i^2, drive^2)*|X|^2 / w_i^2.
        # Coupling spring energy is NOT credited as beneficial isolation.
        score = abs(response) * np.maximum(1., drive/w)
        off = score.copy()
        off[target] = 0.
        j = int(np.argmax(off))
        ratio = float(score[target]/off[j])
        if ratio < worst[0]: worst = ratio, [target, j]
    return {'n':n,'Q':q,'coupling':coupling,'pattern':pattern,
            'min_amplitude_ratio':worst[0], 'witness_target_off':worst[1],
            'window':worst[0]>REQUIRED}


def advance(x, v, duration, w, q, force, drive, phase=0.):
    """Exact damped oscillator response to Re(force*exp(i*(drive*t+phase)))."""
    a = w/(2*q)
    wd = math.sqrt(w*w-a*a)
    h = force / complex(w*w-drive*drive, 2*a*drive)
    z0 = h * complex(math.cos(phase),math.sin(phase))
    zt = h * complex(math.cos(phase+drive*duration),math.sin(phase+drive*duration))
    xh, vh = x-z0.real, v-(1j*drive*z0).real
    c, s = math.cos(wd*duration), math.sin(wd*duration)
    decay = math.exp(-a*duration)
    y = decay*(xh*c+(vh+a*xh)*s/wd)
    dy = decay*(vh*c-(a*vh+w*w*xh)*s/wd)
    return y+zt.real, dy+(1j*drive*zt).real


def pulse_history(q, pulses, samples):
    # One cycle ON, one cycle OFF, fixed global phase, on resonance.
    # Force normalized so steady forced resonant displacement amplitude=1.
    w=1.; force=1/q; cycle=2*math.pi
    x=v=peak=0.
    for k in range(pulses):
        for enabled in (True,False):
            x0,v0=x,v
            for t in np.linspace(0.,cycle,samples+1):
                xx,vv=advance(x0,v0,float(t),w,q,force if enabled else 0.,w)
                peak=max(peak,xx*xx+vv*vv) # energy / (.5*m*w^2)
            x,v=advance(x0,v0,cycle,w,q,force if enabled else 0.,w)
    return peak


def main():
    # Algebraic, limit, and solver holdouts (self-review).
    d=np.array([3+1j,4+2j,5+1j]); o=np.array([-.2,-.3]); b=np.ones(3)
    dense=np.diag(d)+np.diag(o,1)+np.diag(o,-1)
    assert np.allclose(solve_chain(d,o,b),np.linalg.solve(dense,b),rtol=1e-12)
    x,v=advance(.3,-.2,0.,1.,20.,.1,1.)
    assert abs(x-.3)+abs(v+.2)<1e-14
    # Semigroup: phase continuity, and no-force energy dissipation.
    x,v=advance(.3,-.2,3.,1.,20.,.1,.9)
    x2,v2=advance(x,v,4.,1.,20.,.1,.9,phase=2.7)
    xa,va=advance(.3,-.2,7.,1.,20.,.1,.9)
    assert abs(x2-xa)+abs(v2-va)<1e-13
    x,v=advance(.3,-.2,7.,1.,20.,0.,1.)
    assert x*x+v*v < .3**2+.2**2
    # Dense off-diagonal coupling and the uncoupled analytic limit agree.
    w=np.geomspace(1.,10.,8); drive=w[3]; q=20.
    diagonal=(w*w-drive*drive+1j*drive*w/q).astype(complex)
    assert np.allclose(solve_chain(diagonal,np.zeros(7),np.ones(8)),1/diagonal)
    # Scaling all natural/drive frequencies together scales X by 1/s^2;
    # relative normalized energy scores are unchanged if coupling also scales.
    scale=1.05
    original=solve_chain(diagonal,np.zeros(7),np.ones(8))
    shifted=solve_chain(diagonal*scale**2,np.zeros(7),np.ones(8))
    assert np.allclose(original,shifted*scale**2)
    # Uncoupled harmonic witness.
    row=spectrum(8,100,0.,'ideal')
    assert row['window']
    assert spectrum(80,5,0.,'ideal')['window'] is False
    frequencies={'range_ratio':10., 'required_amplitude_ratio':REQUIRED,
        'capacity_nonoverlap':{str(e):math.floor(math.log(10)/math.log((1+e)/(1-e)))+1
                               for e in (.01,.05,.10)},
        'max_fractional_error_6400':math.tanh(math.log(10)/(2*6399))}
    rows=[spectrum(n,q,c,p) for n,q,c,p in itertools.product(
        (8,80),(5,20,100),(0.,.001,.01,.05),
        ('ideal','alternating_1pct','common_5pct','split_bank_5pct_plus_local'))]
    pulses=[]
    for q in (5,20,100):
        single=pulse_history(q,1,128)
        repeated=pulse_history(q,80,128)
        fine=pulse_history(q,80,256)
        assert abs(repeated-fine)/fine < .002
        pulses.append({'Q':q,'single_energy':single,'80_pulse_energy':fine,
                       'ratio_to_single':fine/single,
                       'peak_sampling_relative_change':abs(repeated-fine)/fine})
    # Energy envelope after incoherent deposition, not a general wave solver.
    # E[k+1] = rho*E[k] + e. Coherent phase can be worse (pulse test above).
    energy=[]
    for rho in (0.,.5,.9,.99,1.):
        accumulation=sum(rho**k for k in range(80))
        max_off_amplitude=math.sqrt(.8/1.2)*(1-.1)/(1+.1)/math.sqrt(accumulation)
        energy.append({'rho':rho,'80_history_factor':accumulation,
                       'max_off_to_target_amplitude':max_off_amplitude,
                       'crossed_half_ratio_0.5_pass': .5<max_off_amplitude})
    # Discrete ghost cross: simultaneous rows {0,1}, columns {0,1} cannot
    # address a diagonal pair via equal additive fields or Cartesian blockers.
    desired={(0,0),(1,1)}
    actual=set(itertools.product((0,1),(0,1)))
    assert actual-desired == {(0,1),(1,0)}
    # Per-map ledger: favorable known zero command state; set + final clear.
    timing=[]
    for q in (5,20,100):
        f=1000.
        ringdown=q*math.log(100)/(math.pi*f) # amplitude to 1%
        for events in (12800,3440):
            # Serial frequency-coded set/clear visits every geometric code twice.
            # Row-parallel hypothesis reserves the slowest tone per transaction.
            inv_f = (float(np.mean(1/np.geomspace(1000.,10000.,6400)))
                     if events==12800 else 1/f)
            event_time=inv_f*(1+q*math.log(100)/math.pi)+.001
            total=6+1.01*events*event_time
            timing.append({'Q':q,'events':events,'low_band_ringdown_s':ringdown,
                           'mean_or_slowest_inverse_frequency_s':inv_f,
                           'time_s_6s_reserve_1ms_read_1pct_retry':total})
    # Assumed cantilever sensitivity, NOT an X1C property/tolerance prior.
    beam_ratios=[(t/.6)*(8/L)**2*math.sqrt(E/2e9)
                 for t,L,E in itertools.product((.55,.65),(7.9,8.1),(1.6e9,2.4e9))]
    manufacturing={'beam_frequency_ratio_bounds':[min(beam_ratios),max(beam_ratios)],
                   'dimensions_mm':'t=.6+/- .05, L=8+/- .1',
                   'E_Pa':[1.6e9,2.4e9], 'density_held_fixed':True}
    costs={str(cap):{'receiver_allowance_with_150_elsewhere':(cap-150)/6400,
                     '32_channel_allowance_with_250_elsewhere':(cap-250)/32}
           for cap in (200,400,500)}
    print(json.dumps({'frequency':frequencies,'coupled_bank_scenarios':rows,
                      'pulse_history':pulses,'energy_memory':energy,
                      'timing':timing,'cost_allowances_usd':costs,
                      'manufacturing_sensitivity':manufacturing,
                      'checks':'passed'},indent=2))

if __name__=='__main__': main()
