#!/usr/bin/env python3
"""Downward row handoff: interval geometry, not contact/hardware qualification.

All dimensions mm. A body occupies [2+h-d, 138+h-d], where h is commanded
extension and d is whole-row downward translation (no screw rotation).
Continuous 6-mm guides occupy [50,56] and [130,136]. Test a shared passive
fixture below the lower guide BEFORE any body loses its upper-guide overlap.
"""
import json
from itertools import product
from math import isclose

BODY_LENGTH = 136.
LOWER_BOTTOM, UPPER_BOTTOM = 50., 130.


def window(heights, span=24., overlap=2., length=BODY_LENGTH,
           lower=LOWER_BOTTOM, upper=UPPER_BOTTOM):
    # Most elevated body is last to expose span below the lower guide.
    earliest = max(0., 2.+max(heights)+span-lower)
    # Lowest top is first to lose the requested upper-guide overlap.
    latest = 2.+min(heights)+length-upper-overlap
    return dict(earliest_mm=earliest, latest_mm=latest,
                feasible=earliest <= latest,
                available_span_mm=length-(upper-lower)
                                  -(max(heights)-min(heights))-overlap)


def overlap(a,b,c,d):
    return max(0., min(b,d)-max(a,c))


def check():
    # Independent explicit interval enumeration verifies the endpoint formula.
    cases=0
    for heights, span, engagement in product(
            ([0,50],[0,40],[30,30],[50,50],[0,10]), (4.,6.,16.,24.), (0.,2.)):
        w=window(heights,span,engagement)
        for i in range(801):
            d=i/10
            exposed=all(2+h-d <= LOWER_BOTTOM-span+1e-9 for h in heights)
            retained=all(138+h-d >= UPPER_BOTTOM+engagement-1e-9 for h in heights)
            formula=w['earliest_mm']-1e-9<=d<=w['latest_mm']+1e-9
            assert (exposed and retained)==formula
            cases+=1
    assert not window([0,50])['feasible']
    assert not window([0,40])['feasible']
    assert window([30,30])['feasible']
    assert window([0,50],4)['feasible']  # zero-width timing window, NOT a pass
    assert window([0,50],4)['earliest_mm']==window([0,50],4)['latest_mm']
    # At 8 mm withdrawal the low body has NO upper-guide overlap, whereas
    # the high body's lower 6 mm has just become accessible below Z50.
    assert overlap(-6,130,130,136)==0
    assert isclose(50-(52-8),6)
    # Common guide/body datum translation cancels; relative spacing does not.
    assert isclose(window([0,50])['available_span_mm'],4)
    # Labelled dimensional bounds, not measured manufacturing distributions.
    bounds=[window([0,50+travel],length=136+body,
                   upper=130+spacing)['available_span_mm']
            for body,spacing,travel in product((-.2,.2),(-.4,.4),(-.2,.2))]
    assert isclose(min(bounds),3.2) and isclose(max(bounds),4.8)
    print('PASS:',cases,'explicit interval cases; limiting states and correlated bounds')


def main():
    check()
    out={}
    for name,heights in [('mixed_S50',[0,50]),('mixed_S40',[0,40]),
                         ('flat_N30',[30,30]),('flat_S50',[50,50])]:
        out[name]=window(heights)
    # Topmost body must fall below the lower-guide underside, then lateral
    # exit must also clear adjacent row spines occupying Z-34..-10.
    out['S50_clear_fixed_guides_mm']=138+50-50+2
    out['S50_clear_adjacent_spines_mm']=138+50-(-34)+2
    out['count_controls']={str(n*n):dict(
        resident_pairs=n*n,removable_spines=n,keeper_halves=2*n,
        allocated_mounts=4*n,shared_fixture_body_sites=n,
        shared_fixture_guide_contacts=2*n,
        one_row_pair_transfers=2*n,whole_array_pair_transfers=2*n*n)
        for n in (32,64,80)}
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
