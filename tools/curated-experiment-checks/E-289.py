#!/usr/bin/env python3
"""Ideal laser-plane encoding screen. No rendered images or hardware accuracy claim.

python3 tools/curated-experiment-checks/E-289.py
All unreferenced errors and acquisition times are labelled scenario allocations.
"""
import itertools
import json
import math


def project(x, y, z, D, b, f):
    return f*x/(D-z), f*(y-b)/(D-z)


def decode(u, v, D, b, f):
    return -b*u/v, D+f*b/v


def blocked(a, q, boxes):
    """Open segment against closed axis-aligned solids; exact slab calculation."""
    for lo, hi in boxes:
        t0, t1 = 1e-8, 1-1e-8
        for start, end, lower, upper in zip(a, q, lo, hi):
            d=end-start
            if abs(d)<1e-12:
                if not lower<=start<=upper:
                    t0,t1=1,0
                    break
            else:
                v,w=sorted(((lower-start)/d,(upper-start)/d))
                t0,t1=max(t0,v),min(t1,w)
        if t0<=t1:
            return True
    return False


def scenario(p, width, k, D, b, S):
    W=(k-1)*p
    # Horizontal field includes full caps at maximum height; vertical field is
    # the full ideal stripe displacement. Favorably recenter principal point.
    f=min(.9*1920*(D-S)/(W+width), .9*1080/(b*(1/(D-S)-1/D)))
    # Sufficient central-patch clearance to tallest adjacent row/column.
    # .2 patch half-width + .2 total allocated ray/solid placement reserve.
    mx=p-width/2-(W/2*S/D+.2*(1-S/D))-.2
    my=p-width/2-b*S/D-.4
    hidden=0
    for i in range(k):
        x=(i-(k-1)/2)*p
        boxes=[]
        for row in (-1,0,1):
            for j in range(-1,k+1):
                if row==0 and j==i:
                    continue
                xx=(j-(k-1)/2)*p; yy=row*p
                boxes.append(((xx-width/2,yy-width/2,-10),(xx+width/2,yy+width/2,S)))
        q=(x,0,0)
        hidden+=int(blocked((0,0,D),q,boxes) or blocked((0,b,D),q,boxes))
    # Exact worst error corners for centroid location and image-coordinate bias.
    errors={}
    for dy in (0,.005,.02,.05):
        errs=[]
        for z,y,dv in itertools.product((0,S/2,S),(-dy,dy),(-.1,.1)):
            u,v=project(0,y,z,D,b,f)
            errs.append(abs(decode(u,v+dv,D,b,f)[1]-z))
        errors[str(dy)]=round(max(errs),6)
    return dict(pitch=p,stroke=S,k=k,D=D,b=b,f=round(f,3),
                margins=[round(mx,4),round(my,4)],hidden_centers=hidden,
                error_mm_by_centroid_y_bound=errors)


def check():
    count=0
    for D,b,f,x,z in itertools.product((300,600),(8,16,40),(1200,8000),(-20,0,20),(0,20,50)):
        xx,zz=decode(*project(x,0,z,D,b,f),D,b,f)
        assert abs(xx-x)<1e-10 and abs(zz-z)<1e-10
        count+=1
    # Distinct heights with a displaced stripe have exactly equal pixels at x0.
    D,b,f=300,8,8000
    y=b*(1-299/300)  # z1=1 rather than z0=0; stripe moves toward the camera.
    assert abs(project(0,0,0,D,b,f)[1]-project(0,y,1,D,b,f)[1])<1e-10
    assert abs(decode(*project(0,y,1,D,b,f),D,b,f)[1])<1e-10
    # A constant sheet-offset error is calibratable with a shared reference:
    # b_eff = b-y. A scene-dependent centroid bias is not that constant.
    for z in (0,20,50):
        assert abs(decode(*project(0,y,z,D,b,f),D,b-y,f)[1]-z)<1e-10
    cube=[((1,-1,-1),(2,1,1))]
    assert blocked((0,0,0),(3,0,0),cube)
    assert not blocked((0,2,0),(3,2,0),cube)
    # Receiver shadow and transmitter shadow independently.
    box=[((-2,4,-10),(2,8,50))]
    assert not blocked((0,0,300),(0,0,0),box)
    assert blocked((0,40,300),(0,0,0),box)
    box=[((4,-2,-10),(8,2,50))]
    assert blocked((40,0,300),(0,0,0),box)
    # Opaque miniature: no target photon on either released hidden top.
    base=[((-12.7,-12.7,30),(12.7,12.7,32))]
    for z in (28,29):
        assert blocked((0,0,300),(0,0,z),base)
        assert blocked((0,8,300),(0,0,z),base)
    # Blind whole-pitch coordinate shift survives a lattice check.
    assert math.isclose((0+6.35)/6.35,1)
    return count


if __name__=='__main__':
    print(json.dumps({'exact_roundtrips':check(),'fault_witnesses':'passed'}))
    for S in (40,50):
        for p,w in ((5.08,4.4),(6.35,4.4),(12.7,10.3)):
            for k,D,b in ((4,300,8),(8,600,16),(16,600,40)):
                print(json.dumps(scenario(p,w,k,D,b,S)))
    # One shared reader, .1-s light-off and .1-s light-on allocation per group.
    # This is dense read-only lower accounting, no seeks/settling/retries.
    for n in (32,64,80):
        print(json.dumps({'grid':n,'read_only_s':{k:n*math.ceil(n/k)*.2 for k in (4,8,16)}}))
