"""Necessary packing bound for a fixed, same-plane grounded pawl guide (mm).
No calibrated process priors, structural qualification, or probability model.
"""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('pawl', Path(__file__).resolve().parents[1] / 'E-052/pawl_sweep.py')
pawl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pawl)


def dimensions(e, guide_span):
    overlap = .4 + e
    reach = max(.8, overlap + e + .1)
    length = max(.8, overlap + e + .1 + guide_span)
    width = 1.6 + reach + length + 3*e + .2
    return overlap, reach, length, width


def verify(e, guide_span):
    o, r, length, width = dimensions(e, guide_span)
    errors, section = pawl.screen(1.6, r, length, o, 2., 2., e+.1, e)
    assert ('pitch' in errors) == (width > 5.08 + 1e-9)
    assert not set(errors) - {'pitch'}
    # Fixed guide starts beyond every rack-tip placement; common bank motion
    # cancels in relative coordinates. Its necessary rear-tail allowance is smallest while engaged.
    # This does not check a finite track retaining front coverage on withdrawal.
    tip = e+.1+1.6+r
    guide_left = tip + e/2 + .1
    for dr in (-e/2, e/2):
        assert guide_left - (tip+dr) >= .1-1e-9
        for dp in (-e/2, e/2):
            for travel in (0., o+e+.1):
                tail = tip-o+length+dp+travel
                assert tail-guide_left >= guide_span-1e-9
    return {'error': e, 'guide_span': guide_span, 'pawl_length': round(length, 6),
            'minimum_width': round(width, 6), 'necessary_width_pass': not errors}


def run():
    results = [verify(e,g) for e in (.15,.35,.60) for g in (0.,.4,.9)]
    # Independent width-budget form: maximum possible engaged guide span.
    for e in (.15,.35,.60):
        o,r,_,_ = dimensions(e,0.)
        max_length = 5.08-1.6-r-3*e-.2
        max_guide = max_length-o-e-.1
        expected = {.15:1.23,.35:-.17,.60:-1.92}[e]
        assert abs(max_guide-expected)<1e-9
    # E-052 interior witness: zero rear tail exists outside rack sweep at
    # adverse placement, even though its tooth/pawl section passes.
    assert abs((.8-.77-.35-.1)-(-.42))<1e-9
    # With 0.9 guide span, r=.5+2e and L=1.4+2e near the threshold.
    threshold = (5.08-3.7)/7
    assert verify(threshold-1e-5,.9)['necessary_width_pass']
    assert not verify(threshold+1e-5,.9)['necessary_width_pass']
    # Optimistic two point-contact guide reactions, no finite pad stresses:
    # upward near reaction Rn, downward far reaction Rf; F at distance a
    # left of the near reaction and reaction separation g.
    reactions=[]
    for force in (1.,10.,100.):
        a,g=.8,.9
        far=force*a/g; near=force+far
        assert abs(near-far-force)<1e-12
        assert abs(far*g-force*a)<1e-12
        reactions.append({'cell_load_N':force,'near_up_N':near,'far_down_N':far})
    return {'sections':results,'guide_0_9_error_threshold_mm':threshold,
            'optimistic_tight_guide_reactions':reactions}

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
