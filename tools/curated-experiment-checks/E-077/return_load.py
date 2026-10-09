"""Withdrawal force window: bounded linear elastic calculations, N/mm/MPa.
No process priors or hardware rating. Output is reproducible, not retained.
"""
import json
from math import isclose


def compliance(span, width, depth, modulus):
    return span**3 / (4 * modulus * width * depth**3)


def virtual_work(span, width, depth, modulus, n):
    # Unit central load: integrate M*m/EI on both half spans.
    inertia = width * depth**3 / 12
    dx = span / n
    return sum((min((i+.5)*dx, span-(i+.5)*dx)/2)**2 * dx /
               (modulus*inertia) for i in range(n))


def window(span, modulus, allowable, normal_per_pin=.05):
    width, depth, neck, pin_length = 10., 4., .7, 8.
    # One jam may take the entire limiter load; common deflection is not /80.
    beam = compliance(span, width, depth, modulus)
    axial = pin_length/(modulus*neck**2)
    # E-077 R-L-Z-C = .55; reserve an additional .05 for key/support motion.
    displacement_budget = 1.-.15-.10-.20-.05
    elastic_limit = displacement_budget/(beam+axial)
    pin_limit = allowable*neck**2
    beam_limit = allowable*2*width*depth**2/(3*span)
    upper = min(elastic_limit, pin_limit, beam_limit)
    lower = 80*normal_per_pin
    return dict(span_mm=span, modulus_MPa=modulus, allowable_MPa=allowable,
                normal_load_N=lower, compliance_mm_per_N=beam+axial,
                elastic_limit_N=elastic_limit, pin_limit_N=pin_limit,
                beam_limit_N=beam_limit, upper_limit_N=upper,
                open_force_window_N=upper-lower,
                survives=upper>lower)


def main():
    # Independent unit-load energy integral; refine midpoint quadrature.
    exact = compliance(80,10,4,1000)
    errors = [abs(virtual_work(80,10,4,1000,n)-exact) for n in (20,40,80)]
    assert all(isclose(errors[i]/errors[i+1],4,rel_tol=1e-8) for i in (0,1))
    assert isclose(compliance(160,10,4,1000),8*exact)
    assert isclose(compliance(80,10,8,1000),exact/8)
    assert window(80,1000,20)['survives'] is False
    assert window(40,1000,10)['survives'] is True
    assert window(40,1000,5)['survives'] is False
    assert window(40,1000,10,.1)['survives'] is False
    print(json.dumps(dict(assumptions='epistemic boxes; no strength qualification',
        quadrature_errors=errors, cases=[window(s,e,a)
        for s in (406.4,80,40,20) for e in (1000,3000)
        for a in (5,10,20)]),indent=2))

if __name__ == '__main__':
    main()
