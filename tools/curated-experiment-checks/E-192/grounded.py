#!/usr/bin/env python3
"""Finite aisle packages and explicit counterexamples. Units mm, N, s.
Engineering bounds, not manufacturing priors or contact qualification.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1]/filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


arc = load('aisle', 'E-191/aisle.py')
time = load('transport', 'E-190/transport.py')
P = 5.08
X = P/2


def ring(ro, ri, n=64):
    # Actual polygonal sleeve, circumscribed bore and inscribed outer surface.
    # ri is MINIMUM bore radius; ro is MAXIMUM outer radius.
    rb = ri/math.cos(math.pi/n)
    assert rb < ro*math.cos(math.pi/n)
    out = []
    for k in range(n):
        a, b = 2*math.pi*k/n, 2*math.pi*(k+1)/n
        out.append([(X+r*math.cos(t), r*math.sin(t))
                    for r,t in ((ro,a),(ro,b),(rb,b),(rb,a))])
    return out


def clip(poly, axis, boundary, sign):
    out = []
    for a,b in zip(poly, poly[1:]+poly[:1]):
        da, db = sign*(a[axis]-boundary), sign*(b[axis]-boundary)
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            q = da/(da-db)
            out.append(tuple(a[j]+q*(b[j]-a[j]) for j in (0,1)))
    return out


def area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1]
                   for a,b in zip(poly, poly[1:]+poly[:1])))/2


def overlap(poly, box):
    for axis, bound, sign in ((0,box[0],1),(0,box[1],-1),
                              (1,box[2],1),(1,box[3],-1)):
        poly = clip(poly,axis,bound,sign)
        if not poly:
            return 0.
    return area(poly)


def package(f, d, g, w, tip, delta, nested=False):
    # Axially stacked carrier/thrust/rotor is favorable: no extra radial wall.
    # A nested yoke adds a second .4-mm wall and .1-mm bearing gap.
    ro = d/2+g+w+(.5 if nested else 0.)
    ri = d/2+g
    end = X-ri/math.cos(math.pi/64)
    lp = arc.arc_bounds(arc.rect(tip,end,-.3,.3),X)
    solids = [(*lp,-1.,-.5),(*lp,1.7,2.2),
              (X-ro,X+ro,-ro,ro,-4.,2.2)]
    # Carrier throat toward drive at +y is below the rotor, connected at z=-1.
    # 0.3-mm strands, 0.6-mm-wide pulleys, and brackets share this x aisle.
    solids += [(X-.3,X+.3,0.,2.15,-4.,-1.),
               (X-.15,X+.15,1.85,2.15,-10.,50.),
               (X-.15,X+.15,3.05,3.35,-10.,50.)]
    obstacles = [(-f/2,f/2,-1.4,1.4,0.,1.2),
                 (-.6,.6,-.6,.6,1.2,121.2)]
    for i,j in itertools.product(range(-1,2),repeat=2):
        if (i,j)==(0,0):
            continue
        obstacles += [(i*P-f/2,i*P+f/2,j*P-1.4,j*P+1.4,-40.,41.2),
                      (i*P-.6,i*P+.6,j*P-.6,j*P+.6,-38.8,121.2)]
    swing = min(arc.gap(a,b) for a in solids for b in obstacles)-delta
    route = (P-f)/2-max(ro,.7)-delta
    engagement = f/2-tip-delta
    stem = tip-.6-delta
    # Nominal guide radial gap must survive two size bounds and .025 alignment.
    return dict(foot=f,rail_d=d,gap=g,wall=w,tip=tip,outer_r=ro,
                margin=min(swing,route,engagement,stem),route_margin=route,
                swing_margin=swing,engagement_margin=engagement)


def free_response(c, E=100000., F=.13405):
    # Favorable perfectly CLAMPED ground at z=-10; eccentric force at 40.5.
    # Short sleeve does not shorten the grounded rail's 50.5-mm bending span.
    ell = X-(c['tip']+c['foot']/2)/2
    I = math.pi*c['rail_d']**4/64
    return F*ell*50.5**2/(2*E*I)


def sweep():
    out=[]
    for e,pose in ((.025,.05),(.05,.15),(.1,.15)):
        delta=4*e+pose+.025
        for nested in (False,True):
            passes=[]
            for f,d,g,w,tip in itertools.product(
                    (2.6,2.8,3.,3.2,3.4),tuple(.4+.1*k for k in range(10)),
                    (.05,.1,.15,.25),(.2,.4,.8),tuple(.8+.01*k for k in range(56))):
                if g <= 2*e+.025:
                    continue
                ro=d/2+g+w+(.5 if nested else 0.)
                if min((P-f)/2-ro-delta,f/2-tip-delta,tip-.6-delta)<=1e-10:
                    continue
                c=package(f,d,g,w,tip,delta,nested)
                if c['margin']>1e-10:
                    passes.append(c)
            thicker_wall=[c for c in passes if c['wall']>=.4]
            thick_best=min(thicker_wall,key=lambda c:free_response(c)/c['route_margin']) if thicker_wall else None
            best=min(passes,key=lambda c:free_response(c)/c['route_margin']) if passes else None
            out.append(dict(e=e,pose=pose,delta=delta,nested=nested,
                            geometric_sections=len(passes),wall_at_least_04=len(thicker_wall),
                            best_free_compliance_ratio=(free_response(best)/best['route_margin'] if best else None),
                            best=best,thicker_best=thick_best,
                            thicker_ratio=free_response(thick_best)/thick_best['route_margin'] if thick_best else None))
    return out


def witnesses(n=64):
    # Same section as the central best shoulder choice: f=2.8, rail=.6,
    # g=.15, w=.4. A nested sleeve has Ro=1.35 and intersects nominal feet.
    result={}
    for name,ro,closure in (('nested_nominal',1.35,0.),('stacked_error_corner',.85,.35)):
        shell=(ring(.85,.45,n)+ring(ro,.95,n) if name=='nested_nominal'
               else ring(ro,.45,n))
        # At y=P and 2P the neighboring unchanged foot overlaps rotor height.
        # Pose+dimension closure is applied to foot relative to package.
        vols=[]
        for row in (1,2):
            box=(-1.4+closure,1.4+closure,row*P-1.4,row*P+1.4)
            moved=[[(x,y+row*P) for x,y in poly] for poly in shell]
            vols.append(sum(overlap(poly,box) for poly in moved)*1.2)
        assert min(vols)>0
        result[name+'_mm3']=vols
    # A proposed top x-crossbar is real solid material, across all stem lanes.
    # Stems occupy z=41.2..121.2 for every allowed column height.
    bar=((-2.,-.4,48.),(P+2.,.4,50.))
    stem=((- .6,-.6,41.2),(.6,.6,121.2))
    result['top_crossbar_stem_mm3']=time.box_overlap(bar,stem)
    assert abs(result['top_crossbar_stem_mm3']-1.92)<1e-10
    # Retained sliding channel: E-191 central sliding stroke, with finite .4
    # walls and a grounded underfoot actuator's pushrod at its far x end.
    c=arc.section(2.8,.6,.6,1.,.375,'slide')
    stroke=c['stroke']
    web_right=X+.3+stroke
    foot=((P-1.4,-1.4,0.),(P+1.4,1.4,1.2))
    # Actual right wall (not the channel's hollow bounding box).
    wall=((web_right,-.7,-4.),(web_right+.4,.7,2.2))
    result['sliding_channel_right_wall_mm3']=time.box_overlap(wall,foot)
    assert result['sliding_channel_right_wall_mm3']>0
    result['sliding_stroke_mm']=stroke
    return result


def finite_routes():
    # Idler/drive wheels rotate about x; two strands run at y=2 and y=3.2.
    # Grounded drive center z=-10; idler center z=50, supported by rail bracket.
    # These envelopes contain finite disks and circular strands, NOT empty lines.
    boxes={
        'rail':(X-.3,X+.3,-.3,.3,-12.,52.),
        'ground_block':(X-1.5,X+1.5,-1.5,1.5,-14.,-10.),
        'top_bracket':(X-.3,X+.7,-.3,2.6,51.,52.),
        'top_cheek':(X+.4,X+.7,2.4,2.8,49.8,51.5),
        'bottom_bracket':(X-.3,X+.7,-.3,2.6,-12.,-11.),
        'bottom_cheek':(X+.4,X+.7,2.4,2.8,-11.5,-9.8),
        'top_idler':(X-.3,X+.3,2.,3.2,49.4,50.6),
        'drive_wheel':(X-.3,X+.3,2.,3.2,-10.6,-9.4),
        'active_strand':(X-.15,X+.15,1.85,2.15,-10.,50.),
        'return_strand':(X-.15,X+.15,3.05,3.35,-10.,50.),
        'upper_wrap':(X-.15,X+.15,1.85,3.35,50.,50.75),
        'lower_wrap':(X-.15,X+.15,1.85,3.35,-10.75,-10.)}
    # Cheeks are outside wheel width; crosspieces clear the finite cord wraps.
    assert arc.gap(boxes['top_cheek'],boxes['top_idler']) >= .1-1e-12
    assert arc.gap(boxes['top_bracket'],boxes['upper_wrap']) >= .25-1e-12
    assert arc.gap(boxes['bottom_cheek'],boxes['drive_wheel']) >= .1-1e-12
    assert arc.gap(boxes['bottom_bracket'],boxes['lower_wrap']) >= .25-1e-12
    assert all(b[1]-b[0] <= 3 for b in boxes.values())
    # Withdrawn slide route must contain every x envelope, continuously across
    # two pitches. Broad ground block always remains BELOW lowest foot.
    for key,b in boxes.items():
        assert key=='ground_block' or b[0]>1.4 and b[1]<P-1.4
    for h in (-.5,0.,20.,40.,40.5):
        assert h-4.>-10. and h+2.2<49.4
    return dict(boxes=boxes,loop_length_mm=120+2*math.pi*.6,
                top_to_ground_span_mm=60.,
                unsolved='yaw drive, antirotation, thrust preload, capstan traction, shaft bearings, arrest, resident locks and proof')


def handoff():
    # Foot is z=[0,1.2]. At neutral, neither lip touches it. This contact
    # counterexample needs no assumed force, solver or retention friction.
    lower_top, upper_bottom = -.5, 1.7
    neutral_gaps = (-lower_top, upper_bottom-1.2)
    assert min(neutral_gaps) > 0
    assert abs((lower_top+.5)-0.) < 1e-12
    assert abs((upper_bottom-.5)-1.2) < 1e-12
    return dict(neutral_contact_gaps_mm=neutral_gaps,
                contact_to_opposite_contact_mm=1.,
                premature_stop_release='no vertical contact at neutral; unsupported until a lip closes the gap',
                required_order=['ground supported / rotate in', 'take up 0.5 mm / prove force',
                                'unload and release resident stop', 'translate with input arrest available',
                                'reseat and prove resident stop', 'neutralize 0.5 mm / rotate out'],
                status='ordering obligation only: stop, force proof and input arrest not generated')


def timing():
    out=[]
    for turn in (.02,.05,.1):
        # Original .05 slots remain charged for support operations. Additional
        # .5-mm take-up plus quarter-turn per acquire AND release, no overlap.
        extra=time.loaded(.5)+turn
        for banks in range(1,81):
            n=math.ceil(80/banks)
            sec=6+time.bypass_bank(n)+(n-1)*time.empty(P)+time.empty((n-1)*P)+2*n*extra
            if sec<30:
                break
        out.append(dict(turn_s=turn,extra_per_transfer_s=extra,banks=banks,
                        vertical_motors=80*banks,seconds=sec,
                        two_bank_seconds=6+time.bypass_bank(40)+39*time.empty(P)+time.empty(39*P)+80*extra,
                        branch_allowance_usd=250/(80*banks)))
    return out


def checks():
    assert abs(overlap([(0,0),(2,0),(2,2),(0,2)],(1,3,1,3))-1)<1e-12
    assert overlap([(0,0),(2,0),(2,2),(0,2)],(3,4,3,4))==0
    refinements=[witnesses(n) for n in (32,64,128,256)]
    for key in ('nested_nominal_mm3','stacked_error_corner_mm3'):
        assert all(refinements[k+1][key][0]>refinements[k][key][0] for k in range(3))
    c=dict(rail_d=.6,foot=2.8,tip=1.)
    assert free_response(c,F=0)==0
    assert abs(free_response(c,E=2000)/free_response(c,E=100000)-50)<1e-10
    # Independent midpoint curvature integration for a constant moment cantilever.
    exact=free_response(c)
    L=50.5
    M=.13405*(X-1.2)
    EI=100000*math.pi*.6**4/64
    y=theta=0.
    for _ in range(100):
        dx=L/100
        y+=theta*dx+.5*M/EI*dx*dx
        theta+=M/EI*dx
    assert abs(y-exact)<1e-12
    return refinements


if __name__=='__main__':
    print(json.dumps(dict(sweep=sweep(),counterexamples=witnesses(),
                         finite_routes=finite_routes(),handoff=handoff(),timing=timing(),
                         refinement=checks()),indent=2))
