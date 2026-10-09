"""Finite rectangular dog/cam section; epistemic boxes, not process yield."""
from itertools import product
import json

PITCH = 5.08

def overlap(a, b):
    return min(a[1], b[1]) - max(a[0], b[0])

def screen(b, c, d, e, guide=.4):
    # Width errors +/-e and independent center errors +/-e.
    engagement = min(b-e, c-e, (b+c)/2-3*e)
    bypass = d-(b+c)/2-3*e
    packing = PITCH-(d+b+3*e+2*guide)
    # Independently evaluate all rectangular section corners.
    contacts, gaps = [], []
    for db, dc, xd, xc in product((-e,e), repeat=4):
        cam = (d+xc-(c+dc)/2, d+xc+(c+dc)/2)
        on = (d+xd-(b+db)/2, d+xd+(b+db)/2)
        off = (xd-(b+db)/2, xd+(b+db)/2)
        contacts.append(overlap(cam,on))
        gaps.append(cam[0]-off[1])
    assert abs(min(contacts)-engagement)<1e-12
    assert abs(min(gaps)-bypass)<1e-12
    # The swept dog occupies [off.left,on.right]; adjacent dogs have same range.
    assert abs((PITCH-2*guide)-(d+b+3*e)-packing)<1e-12
    return [round(x,6) for x in (engagement,bypass,packing)]

def withdrawal(lost, flex, error, reserve=.2, lift=1.):
    return lift-lost-flex-error-reserve

def main():
    rows=[]
    for e in (.05,.10,.20):
        survivors=[]
        for b,c,d in product((.6,.8,1.),(.6,.8,1.),(1.2,1.5,1.8)):
            margins=screen(b,c,d,e)
            if min(margins)>0: survivors.append([b,c,d,margins])
        rows.append(dict(error=e,survivors=survivors,count=len(survivors)))
    assert screen(.8,.8,1.5,.1)==[.5,.4,1.68]
    # Common plate may be fully withdrawn while a noncaptive pin stays inserted.
    assert withdrawal(.15,.15,.1)>.0
    assert withdrawal(.15,.6,.1)<.0
    print(json.dumps(dict(section=rows, witness=screen(.8,.8,1.5,.1),
        pullback_margin=withdrawal(.15,.15,.1),
        bent_pullback_margin=withdrawal(.15,.6,.1)),indent=2))

if __name__=='__main__': main()
