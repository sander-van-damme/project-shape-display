#!/usr/bin/env python3
"""Quasistatic versus lossless single-pulse bistable flag, mm/N, explicit bounds.
Ideal one-gap reluctance, no field solution, physical detent or repeat-pulse pass.
"""
import json
import math
from itertools import product

MU0=4*math.pi*1e-7


def peak(f, a, b):
    """Golden-section maximum; tested functions are unimodal on these bounds."""
    ratio=(math.sqrt(5)-1)/2
    c=b-ratio*(b-a);d=a+ratio*(b-a)
    for _ in range(100):
        if f(c)>f(d):
            b,d=d,c;c=b-ratio*(b-a)
        else:
            a,c=c,d;d=a+ratio*(b-a)
    x=(a+b)/2
    return x,f(x)


def thresholds(gap,stroke=.2,k=.1):
    assert gap>stroke>0 and k>0
    # U=k*x^2*(s-x)^2/(2*s^2), restoring force = dU/dx.
    # Ideal constant-current magnetic force = a/(g-x)^2.
    s=stroke;g=gap
    static=lambda x:k*x*(s-x)*(s-2*x)*(g-x)**2/s**2
    energy=lambda x:k*g*x*(s-x)**2*(g-x)/(2*s**2)
    xs,fs=peak(static,0,s/2)
    xe,fe=peak(energy,0,s)
    return dict(gap_mm=g,stroke_mm=s,k_N_per_mm=k,
                static_saddle_mm=xs,static_coefficient_Nmm2=fs,
                energy_saddle_mm=xe,energy_coefficient_Nmm2=fe,
                single_pulse_to_static_ampere_turn_ratio=math.sqrt(fe/fs))


def ampere_turns(coefficient,area=1.):
    # Conversion from N mm^2 and mm^2 cancels 10^-6 factors in the ratio.
    return math.sqrt(2*coefficient/(MU0*area))


def window(gap,gap_error,k_error,current_error,leakage,stroke=.2,k=.1):
    # All errors are coherent adverse scenarios, not iid stochastic samples.
    # Fixed stroke: thresholds increase monotonically with k and gap.
    weak=thresholds(gap-gap_error,stroke,k*(1-k_error))
    strong=thresholds(gap+gap_error,stroke,k*(1+k_error))
    lower=ampere_turns(strong['static_coefficient_Nmm2'])/(2*(1-current_error))
    old_upper=ampere_turns(weak['static_coefficient_Nmm2'])/(1+current_error+leakage)
    upper=ampere_turns(weak['energy_coefficient_Nmm2'])/(1+current_error+leakage)
    return dict(gap_mm=gap,gap_error_mm=gap_error,k_error=k_error,
                current_error=current_error,parasitic_ampere_turn_fraction=leakage,
                selected_quasistatic_min_AT=lower,half_select_static_max_AT=old_upper,
                half_select_lossless_single_pulse_max_AT=upper,
                quasistatic_window=lower<old_upper,single_pulse_window=lower<upper)


def checks():
    for g,s in product((.3,.5,1.),(.1,.2)):
        r=thresholds(g,s)
        assert 0<r['energy_coefficient_Nmm2']<r['static_coefficient_Nmm2']
        # Grid convergence lower estimates validate optimized interior maxima.
        for n in (100,1000):
            static=max(.1*x*(s-x)*(s-2*x)*(g-x)**2/s**2 for x in (s*i/(2*n) for i in range(n+1)))
            assert static<=r['static_coefficient_Nmm2']*(1+1e-12)
            assert static>=r['static_coefficient_Nmm2']*(1-20/n**2)
        x=r['energy_saddle_mm'];a=r['energy_coefficient_Nmm2']
        U=.1*x*x*(s-x)**2/(2*s*s)
        W=a*(1/(g-x)-1/g)
        assert math.isclose(U,W,rel_tol=1e-12)
        # At the maximum energy ratio, equality of force holds too.
        F=.1*x*(s-x)*(s-2*x)/s**2
        assert math.isclose(F,a/(g-x)**2,rel_tol=1e-6)
        assert math.isclose(thresholds(g,s,.2)['static_coefficient_Nmm2'],2*r['static_coefficient_Nmm2'])
    # Large-gap force is effectively constant. Independent quartic-barrier limits.
    g=10000.;s=.2;k=.1;r=thresholds(g,s,k)
    assert math.isclose(r['static_coefficient_Nmm2']/g**2,k*s/(6*math.sqrt(3)),rel_tol=1e-4)
    assert math.isclose(r['energy_coefficient_Nmm2']/g**2,2*k*s/27,rel_tol=1e-4)
    assert math.isclose(ampere_turns(MU0/2),1.)


def main():
    checks()
    rows=[window(g,d,k,e,l) for g,d,k,e,l in product((.3,.5,1.),(.025,.05),(.15,.30),(.05,.15),(0.,.06))]
    print(json.dumps(dict(evidence='ideal gap/energy necessary screen; no finite field or mechanism qualification',
                         nominal=[thresholds(g) for g in (.3,.5,1.)],
                         cases=len(rows),static_pass=sum(r['quasistatic_window'] for r in rows),
                         single_pulse_pass=sum(r['single_pulse_window'] for r in rows),
                         newly_rejected=[r for r in rows if r['quasistatic_window'] and not r['single_pulse_window']],
                         cases_all=rows),indent=2))

if __name__=='__main__':main()
