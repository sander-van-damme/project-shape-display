"""Rigid rectangular wing/parallel-shelf necessary confinement, mm/radians.
No friction, force equilibrium, deformation or probabilistic yield model.
"""
import json
import math


def corners(length, thickness, angle):
    c, s = math.cos(angle), math.sin(angle)
    return [(x*c-z*s, x*s+z*c)
            for x in (-length/2, length/2)
            for z in (-thickness/2, thickness/2)]


def first_contact(length, thickness, gap):
    height = thickness + gap
    diagonal = math.hypot(length, thickness)
    if height > diagonal:
        return None
    # Rising branch of L sin(theta) + t cos(theta) = H.
    return math.asin(height/diagonal)-math.atan2(thickness, length)


def run():
    out = {}
    for e in (.15, .35):
        L, t, gap = .8, 2., e+.2
        H = t+gap
        assert first_contact(L,t,gap) is None
        # Independent corner rotation checks, with converging angle grids.
        maxima=[]
        for intervals in (90,900,9000):
            heights=[]
            for i in range(intervals+1):
                theta=math.pi*i/(2*intervals)
                pts=corners(L,t,theta)
                height=max(z for x,z in pts)-min(z for x,z in pts)
                assert abs(height-(L*math.sin(theta)+t*math.cos(theta)))<1e-12
                assert height < H
                heights.append(height)
            maxima.append(max(heights))
        assert abs(maxima[-1]-math.hypot(L,t))<1e-8
        # Necessary L for upper/lower shelf contact no later than alpha.
        lengths={}
        for degrees in (5,10,15):
            alpha=math.radians(degrees)
            need=(H-t*math.cos(alpha))/math.sin(alpha)
            assert abs(first_contact(need,t,gap)-alpha)<1e-12
            lengths[str(degrees)]=need
        out[str(e)]={'slot_height':H,'wing_diagonal':math.hypot(L,t),
                     'first_shelf_stop_degrees':None,
                     'max_gap_for_any_stop':math.hypot(L,t)-t,
                     'max_gap_for_5_degree_stop':L*math.sin(math.radians(5))+t*(math.cos(math.radians(5))-1),
                     'required_length_by_stop_degrees':lengths,
                     'sampled_maxima':maxima}
    assert abs(first_contact(.8,2,0))<1e-12
    assert first_contact(.8,2,.05) is not None
    return out

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
