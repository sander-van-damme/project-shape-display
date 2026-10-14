#!/usr/bin/env python3
"""Rigid integral-square-column envelope. Bounds, not calibrated process priors."""
import argparse
import itertools
import json
import math


def envelope(pitch, seam, clearance, span, stroke, width_error=0., placement=0.):
    """Two 2-mm guides; bound each aperture center independently by placement.

    Straight constant square section contains an inscribed cylinder, hence its
    horizontal section has width >= w_min in either coordinate at any tilt.
    A guide confines each section to G_max. Centerline slope in one coordinate
    is therefore <= (G_max-w_min+2*placement)/(span+2). Extrapolate the support
    function to the maximum top plane. Finite top is a subset of this prism.
    This is sufficient separation for rigid columns, not a collision assertion
    when negative. Positive min_fit does not prove simultaneous screw alignment.
    """
    w = pitch-seam
    gmax = w+clearance+width_error
    wmin = w-width_error
    B, h = span+2, stroke+2
    reach = gmax+2*placement+2*h*(gmax-wmin+2*placement)/B
    return dict(gap=pitch-reach, min_fit=clearance-2*width_error,
                max_envelope=reach, stock=stroke+span+6,
                nominal_coverage=(w/pitch)**2,
                min_guide_web=pitch-gmax-2*placement)


def exact_strip(width, opening, span, stroke, placement=0.):
    """Exact yaw=0 rigid 2D prism, opposing guide-face contacts, no elasticity.

    Horizontal width = width/cos(theta); B*tan(theta)+width/cos(theta)=G+2r.
    Opposing neighboring columns share this contact witness. All dimensions
    are realized inputs, not nominal CAD. Returns the pair occupied envelope.
    """
    B,h=span+2,stroke+2
    if width>opening: raise ValueError('No guide fit')
    lo,hi=0.,math.atan((opening+2*placement-width)/B)
    for _ in range(70):
        mid=(lo+hi)/2
        if B*math.tan(mid)+width/math.cos(mid)>opening+2*placement: hi=mid
        else: lo=mid
    theta=(lo+hi)/2
    return opening+2*placement+2*h*math.tan(theta),theta


def stock_liters(n,width,wall,stock):
    # Tube only; end thread, roof, screw and print supports excluded.
    return n*n*(width*width-(width-2*wall)**2)*stock/1e6


def integral_volume(n,width,wall,stock,bore=3.2):
    """Tube plus 10-mm bottom nut block and 2-mm closed roof, no double count.

    Cylindrical bore is a volume bound; not a constructed mating thread.
    """
    cavity=(width-2*wall)**2
    return stock_liters(n,width,wall,stock)+n*n*(10*(cavity-math.pi*bore*bore/4)+2*cavity)/1e6


def rows():
    for n in (80,64,32):
        p=406.4/n
        for b in (40.,80.):
            for c,e,r in ((.24,0.,0.),(.5,.1,.1),(.8,.2,.2)):
                a=envelope(p,.4,c,b,50,e,r)
                ex,theta=exact_strip(p-.4-e,p-.4+c+e,b,50,r)
                # Required nominal seam for guaranteed non-overlap is affine.
                required=.4-a['gap']
                yield dict(n=n,span=b,clearance=c,width_error=e,placement=r,
                           **a,exact_strip_gap=p-ex,theta_deg=math.degrees(theta),
                           required_seam=required,
                           coverage_at_required_seam=max(0.,1-required/p)**2)


def search():
    # A finite comparison grammar, not an optimization over every mechanism.
    # Baseline c=.5/e=.1/r=.1 admits .3 minimum total clearance.
    out=[]
    for b,seam in itertools.product((40.,60.,80.),(.4,.8,1.2,1.6,2.,2.4,3.2)):
        a=envelope(12.7,seam,.5,b,50,.1,.1)
        if a['gap']>=0 and a['min_fit']>0:
            out.append(dict(span=b,seam=seam,**a,
                            tube_liters_wall_0p8=stock_liters(32,12.7-seam,.8,a['stock'])))
    return out


def check():
    count=0
    # Independently realize guide-plane contacts and exact rotated 2D sections.
    for p,b,S,c,e,r in itertools.product((5.08,6.35,12.7),(20.,40.,80.),(0.,20.,40.,50.),(.24,.5,.8),(0.,.1),(0.,.1)):
        w=p-.4-e; G=p-.4+c+e
        a=envelope(p,.4,c,b,S,e,r)
        ex,theta=exact_strip(w,G,b,S,r)
        B,h=b+2,S+2
        t=math.tan(theta); section=w/math.cos(theta)
        lower_center=-r-(G-section)/2
        upper_center=r+(G-section)/2
        assert abs(upper_center-lower_center-B*t)<1e-10
        assert abs(2*(upper_center+h*t)+section-ex)<1e-10
        assert ex<=a['max_envelope']+1e-10
        assert 0<=a['max_envelope']-ex<.09
        # One mm below the top-center plane is inside both finite tilted ends.
        # This checks finite stock, rather than mistaking extrapolated edges
        # beyond a tilted cap for a real collision witness.
        assert 1>w*math.sin(theta)/2
        assert h-a['stock']*math.cos(theta)+w*math.sin(theta)/2 < -B
        finite_envelope=ex-2*t
        if p==12.7 and b==40 and S==50 and c==.24 and e==0 and r==0:
            assert p-finite_envelope < -.42
        count+=1
    a=envelope(12.7,.4,0.,40,50)
    assert abs(a['gap']-.4)<1e-12
    assert abs(envelope(12.7,.4,.5,40,50,.1,.1)['min_fit']-.3)<1e-12
    assert envelope(12.7,.4,.24,40,50,.2,.1)['min_fit']<0
    for p in (5.08,6.35,12.7):
        a=envelope(p,.4,.5,40,50,.1,.1)
        z=envelope(p,.4,.5,80,50,.1,.1)
        assert z['gap']>a['gap']
        assert abs(a['gap']-envelope(12.7,.4,.5,40,50,.1,.1)['gap'])<1e-10
    # Common translation cancels; common inter-plane skew at unequal heights
    # contributes delta_h * skew / B, while local opposing errors add.
    B=42.; skew=.2
    for h1,h2 in ((52.,52.),(52.,2.),(2.,52.)):
        x1=10+h1*skew/B; x2=10+12.7+h2*skew/B
        assert abs((x2-x1-12.7)-(h2-h1)*skew/B)<1e-12
    assert len(search())==6
    assert integral_volume(32,10.3,.8,136)>stock_liters(32,10.3,.8,136)
    assert abs(stock_liters(32,12.3,.8,96)-3.6175872)<1e-8
    print(f'{count} exact-strip comparisons; fit, correlation, scale, stock and search anchors pass')


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    if args.check: check()
    else: print(json.dumps(dict(comparison=list(rows()),coarse_survivors=search()),indent=2))
