#!/usr/bin/env python3
"""Fixed whole-board stereo: sourced geometry, assumed errors, no image proof."""
import json
import math

D, B = 650., 95.
FX = 1280 / (2 * math.tan(math.radians(90 / 2)))
R = 1.93 / 2 / 2  # nominal focal length / f-number / 2, mm
GRIDS = [(5.08, 4.4, 80), (6.35, 4.4, 64), (12.7, 10.3, 32)]


def clear_rectangle(p, w, x, y, z, high):
    """Sufficient continuous-pupil square-well clearance, not necessary visibility."""
    t = (high-z)/(D-z)
    widths = []
    for c, b in ((x, B), (y, 0)):
        a = p-w/2
        center = t*c/(1-t)
        half = (a-t*(b/2+R))/(1-t)
        widths.append(max(0., min(w/2, center+half)-max(-w/2, center-half)))
    return widths


def hit_box(start, end, low, high):
    near, far = 1e-10, 1-1e-10
    for s,e,l,h in zip(start,end,low,high):
        v=e-s
        if abs(v)<1e-14:
            if not l<=s<=h: return False
        else:
            a,b=sorted(((l-s)/v,(h-s)/v))
            near,far=max(near,a),min(far,b)
            if near>far: return False
    return True


def checks():
    tested=0
    for p,w,n in GRIDS:
        for z,h in ((0.,40.),(0.,50.),(30.,50.),(0.,0.)):
            for x,y in ((0.,0.),((n-1)*p/2,0.),(p/2,p)):
                wx,wy=clear_rectangle(p,w,x,y,z,h)
                if not wx*wy: continue
                t=(h-z)/(D-z)
                intervals=[]
                for c,b in ((x,B),(y,0)):
                    half=(p-w/2-t*(b/2+R))/(1-t)
                    center=t*c/(1-t)
                    intervals.append((max(-w/2,center-half),min(w/2,center+half)))
                boxes=[((x+i*p-w/2,y+j*p-w/2,-1.),
                        (x+i*p+w/2,y+j*p+w/2,h))
                       for i in (-1,0,1) for j in (-1,0,1) if i or j]
                for ax in (.01,.5,.99):
                    for ay in (.01,.5,.99):
                        q=(x+intervals[0][0]+ax*wx,y+intervals[1][0]+ay*wy,z)
                        for side in (-1,1):
                            for dx,dy in ((-R,0),(R,0),(0,-R),(0,R)):
                                end=(side*B/2+dx,dy,D)
                                assert not any(hit_box(q,end,l,hb) for l,hb in boxes)
                                tested+=1
        # Exact obstruction by ONE adjacent square column, not a seamless wall.
        # Select a real row under the camera y=0; x is the rightmost column.
        x=(n-1)*p/2
        face=x-p+w/2
        # Max height at near wall face over all cap x and left circular pupil.
        # qx max and pupil x max maximize this fractional-linear expression.
        zmax=D*p/(x+w/2+B/2-R)
        assert zmax<40
        # Entire y footprint contracts toward pupil inside the same neighbor width.
        assert R<w/2
        for ix in range(11):
            for iy in range(11):
                q=(x-w/2+w*ix/10,-w/2+w*iy/10,0.)
                for k in range(16):
                    end=(-B/2+R*math.cos(k*math.pi/8),R*math.sin(k*math.pi/8),D)
                    assert hit_box(q,end,(x-p-w/2,-w/2,-1),(face,w/2,40))
                    tested+=1
        assert clear_rectangle(p,w,x,0,0,0)==[w,w]
    for z in (0,30,50):
        d=FX*B/(D-z)
        for e in (.05,.1,.25):
            formula=(D-z)*e/(d-e)
            assert abs(formula-(FX*B/(d-e)-(D-z)))<1e-10
    return tested


def main():
    rows=[]
    for p,w,n in GRIDS:
        for z,h in ((0.,40.),(0.,50.),(30.,50.),(0.,0.)):
            area=nonzero=full=0
            for i in range(n):
                for j in range(n):
                    # Camera aligned with one central row; true 406.4-mm grid.
                    x=(i-(n-1)/2)*p; y=(j-n/2)*p
                    widths=clear_rectangle(p,w,x,y,z,h)
                    a=math.prod(widths)/w**2
                    area+=a; nonzero+=a>1e-12; full+=a>1-1e-12
            rows.append(dict(pitch=p,z=z,neighbor_height=h,cells=n*n,
                             sufficient_patch_cells=nonzero,whole_cap_cells=full,
                             average_sufficient_area=area/n**2))
    sensitivity=[]
    for z in (0,30,50):
        depth=D-z; d=FX*B/depth
        sensitivity.append(dict(z=z,mm_per_pixel=depth/FX,disparity=d,
          error_mm={str(e):depth*e/(d-e) for e in (.05,.1,.25)},
          disparity_budget_for_0_5mm=d*.5/(depth+.5)))
    witnesses=[]
    for p,w,n in GRIDS:
        x=(n-1)*p/2
        witnesses.append(dict(pitch=p,x=x,maximum_near_face_z=D*p/(x+w/2+B/2-R),
                              cap_width_pixels=w*FX/D))
    print(json.dumps(dict(checks=checks(),fx=FX,pupil_radius=R,
                         sensitivity=sensitivity,whole_board=rows,
                         bought_USD=[797.678+1.10*(499+40-175),
                                    1768.233+1.15*(499+120-490)],
                         fully_blocked_witnesses=witnesses),indent=2))

if __name__=='__main__': main()
