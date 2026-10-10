#!/usr/bin/env python3
"""Direct-head capture/guidance screening; mm, N, radians. No process priors.
Finite solids and deterministic error enclosures; NOT a powered machine model.
"""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location('acquisition', Path(__file__).parents[1]/'E-123'/'acquisition.py')
a = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = a
spec.loader.exec_module(a)
Box, PITCH, RESERVE = a.Box, a.PITCH, a.RESERVE
SPAN = 30.


def guide_excursion(h, c):
    """c = remaining centre half-play at each finite guide station.
    Column guide centres z=45,75; head guide centres z=-10,-40.
    h is common foot height, not two independently maximised heights.
    R bounds local rotation of capture vertices beyond the centreline motion.
    """
    lc, lh = 45-h, h+10
    angle = math.atan(2*c/SPAN)
    col = c*(1+2*lc/SPAN)
    head = c*(1+2*lh/SPAN)
    return col, head, 2*(3+6)*math.sin(angle/2)


def relative_bound(e, c):
    return 4*e + max(sum(guide_excursion(h,c)) for h in (0,40))


def clipped_area(subject, clip):
    """Convex polygon intersection, CCW vertices; independent finite witness."""
    def cross(a,b,p): return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
    for i,start in enumerate(clip):
        end=clip[(i+1)%len(clip)]; result=[]
        if not subject: return 0.
        for j,p in enumerate(subject):
            q=subject[(j+1)%len(subject)]
            dp,dq=cross(start,end,p),cross(start,end,q)
            if dp>=0: result.append(p)
            if (dp>=0)!=(dq>=0):
                t=dp/(dp-dq)
                result.append(tuple(v+t*(w-v) for v,w in zip(p,q)))
        subject=result
    return abs(sum(p[0]*subject[(i+1)%len(subject)][1]-p[1]*subject[(i+1)%len(subject)][0]
                   for i,p in enumerate(subject)))/2


def rotated_rect(y,z,theta,dy):
    co,si=math.cos(theta),math.sin(theta)
    return [(dy+v*co+w*si,-v*si+w*co)
            for v,w in ((y[0],z[0]),(y[1],z[0]),(y[1],z[1]),(y[0],z[1]))]


def guide_collision_witness():
    # Same positive tilt at both shafts is compatible with opposite extrapolated
    # positions because one bearing pair is above the foot and the other below.
    c,e=.025,.05
    dc,dh,_=guide_excursion(0,c)
    theta=math.atan(2*c/SPAN)
    web=rotated_rect((-2.25,-1.65+e),(-.4,1.6),theta,dh+e)
    foot=rotated_rect((-1.4-e,1.4),(0,1.2),theta,-dc-e)
    area=clipped_area(web,foot)
    assert area>0
    # Rectangular zero-angle limiting case: 1.2 times overlap .0916667.
    nominal=clipped_area(rotated_rect((-2.25,-1.65+e),(-.4,1.6),0,dh+e),
                         rotated_rect((-1.4-e,1.4),(0,1.2),0,-dc-e))
    assert math.isclose(nominal,1.2*(4*e+dc+dh-.25),abs_tol=1e-12)
    return {'e_mm':e,'guide_half_play_mm':c,'angle_rad':theta,
            'volume_mm3':4*area,'parallel_axis_limit_volume_mm3':4*nominal}


def sleeve(centre, shaft_x, shaft_y, c, wall=.8, length=2):
    """Four actual walls, open rectangular bore; c excludes form/alignment error.
    Only packaging is tested here; no frictionless bearing qualification.
    """
    x,y=shaft_x/2+c,shaft_y/2+c
    z=(centre-length/2,centre+length/2)
    return [Box((-x-wall,-x),(-y-wall,y+wall),z),
            Box((x,x+wall),(-y-wall,y+wall),z),
            Box((-x,x),(-y-wall,-y),z),
            Box((-x,x),(y,y+wall),z)]


@dataclass(frozen=True)
class Cup:
    flange: float = 2.0  # x, changed from E-123; y remains 2.8
    stem: float = 1.2
    overlap: float = .2
    back: float = .2
    entry: float = .2
    wall: float = .6
    gap: float = .4

    @property
    def stroke(self): return self.overlap+self.entry

    @property
    def half_width(self):
        return self.flange/2+self.back+self.wall+self.stroke

    def parts(self, opening=1., takeup=0., h=0.):
        """Fixed base/pad plus two C jaws. opening 1 -> 0; takeup closes z gap.
        Jaw feet remain on/in a finite two-wall channel. No actuator grant:
        these are geometric coordinates, explicitly awaiting powered linkage.
        """
        w=self.half_width
        out=[Box((-w,w),(-1.4,1.4),(-2.4,-1.6)),
             Box((-.5,.5),(-.7,.7),(-1.6,-.8)),
             Box((-self.flange/2,self.flange/2),(-1.4,1.4),(-.8,0))]
        # Retaining channel walls in y; slide foot is 1.6 wide in y.
        for sign in (-1,1):
            ya,yb=(.85,1.4) if sign==1 else (-1.4,-.85)
            out.append(Box((-w,w),(ya,yb),(-1.6,-.9)))
        inner=self.flange/2+self.back+opening*self.stroke
        tip=self.flange/2-self.overlap+opening*self.stroke
        top=1.2+self.gap-takeup
        for sign in (-1,1):
            def reflect(interval):
                return interval if sign==1 else (-interval[1],-interval[0])
            # Fixed web and sliding upper contact pad. Its vertical retention and
            # drive are deliberately NOT claimed by this interface-only model.
            out.extend([
                Box(reflect((inner,inner+self.wall)),(-.8,.8),(-1.6,1.2+self.gap+.8)),
                Box(reflect((tip,inner)),(-.8,.8),(top,top+.8)),
            ])
        return [b.move(dz=h) for b in out]

    def column(self,h=0.):
        return [Box((-self.flange/2,self.flange/2),(-1.4,1.4),(h,h+1.2)),
                Box((-self.stem/2,self.stem/2),(-.6,.6),(h+1.2,h+110))]

    def margins(self,e,c):
        d=relative_bound(e,c)
        rotation=guide_excursion(0,c)[2]
        # Independent heads can take opposite guide corners in x.
        hh=4*e+2*max(guide_excursion(h,c)[1] for h in (0,40))
        hh+=4*6*math.sin(math.atan(2*c/SPAN)/2)
        return {'entry':self.entry-d,'web':self.back-d,
                'stem':(self.flange-self.stem)/2-self.overlap-d,
                'overlap':self.overlap-d,
                'head_head':PITCH-2*self.half_width-hh,
                'upper_entry':self.gap-4*e-rotation,
                'y_neighbor':PITCH-2.8-d}


def finite_cup_check(cup, holdout=False):
    """Continuous axis sweeps against arbitrary-height neighbours, not snapshots.
    Own-column approach/closing/takeup separate intentional contact from obstacles.
    No slender drive bodies or command path are hidden in this geometry result.
    """
    obstacle=[b.sweep(2,40) for b in cup.column()]
    # Per-body bounding boxes span open/closed/taken-up configurations, including
    # any gaps between endpoint solids when stroke exceeds a member's width.
    hull=[Box(*[(min(x[0],y[0]),max(x[1],y[1])) for x,y in
                zip((b.x,b.y,b.z),(c.x,c.y,c.z))])
          for b,c in zip(cup.parts(1.),cup.parts(0.,cup.gap))]
    swept=[b.sweep(2,40) for b in hull]
    for dx,dy in product((-PITCH,0,PITCH),repeat=2):
        if dx==dy==0: continue
        assert all(b.volume_intersection(o.move(dx,dy))<1e-10 for b in swept for o in obstacle)
    # Exact own-foot sweeps for entry, closing and vertical take-up. Intentional
    # pad/foot and upper-jaw/foot contact has zero intersection volume.
    own=cup.column()
    for b in cup.parts(1.,h=-4):
        assert all(b.sweep(2,4).volume_intersection(o)<1e-9 for o in own)
    # First five bodies are stationary; each remaining pair is one moving jaw.
    for index,b in enumerate(cup.parts(1.)):
        shift=0 if index<5 else (cup.stroke if index<7 else -cup.stroke)
        assert all(b.sweep(0,shift).volume_intersection(o)<1e-9 for o in own)
    for index,b in enumerate(cup.parts(0.)):
        shift=-cup.gap if index in (6,8) else 0
        assert all(b.sweep(2,shift).volume_intersection(o)<1e-9 for o in own)
    for steps in ((16,64,256) if holdout else ()):
        for i in range(steps+1):
            q=i/steps
            # Acquire from below, close laterally above foot, then remove vertical play.
            for bodies in (cup.parts(1.,h=-4*(1-q)),cup.parts(1-q),cup.parts(0.,cup.gap*q)):
                assert all(b.volume_intersection(o)<1e-9 for b in bodies for o in cup.column())
    # Closed capture translates together over 40 mm; zero rigid nominal slot play.
    for old,target in (product(range(0,41,5),repeat=2) if holdout else [(0,40)]):
        for h in (old,target):
            assert all(b.volume_intersection(o)<1e-9 for b in cup.parts(0.,cup.gap,h)
                       for o in cup.column(h))
    # Upper finite guides stay above highest jaw; bore contains the stem.
    for z in (45,75):
        for g in sleeve(z,cup.stem,1.2,.025):
            assert all(g.volume_intersection(o)==0 for o in cup.column())
            assert all(g.volume_intersection(b)==0 for b in swept)
    return True


def beam_tip(moment, length, span, modulus, inertia):
    """Overhanging Euler-Bernoulli beam: two lateral simple bearings, end moment.
    Signed moment accepted. Deflection and slope; elastic small-angle scenarios.
    """
    return (moment*(length*length/2+span*length/3)/(modulus*inertia),
            moment*(length+span/3)/(modulus*inertia))


def beam_holdout(moment, length, span, modulus, inertia, n):
    # Independent numerical integration of curvature including supported span.
    # M rises linearly 0 -> moment between bearings, then is constant.
    dx=span/n
    theta=y=0.
    for i in range(n):
        k0=moment*(i/n)/(modulus*inertia)
        k1=moment*((i+1)/n)/(modulus*inertia)
        y+=theta*dx+(2*k0+k1)*dx*dx/6
        theta+=(k0+k1)*dx/2
    correction=-y/span
    theta+=correction
    # Enforce both guide displacements zero before integrating the overhang.
    y=0.
    dx=length/n
    k=moment/(modulus*inertia)
    for _ in range(n):
        y+=theta*dx+k*dx*dx/2
        theta+=k*dx
    return y,theta


def force_screen():
    out=[]
    # E is an explicit epistemic scenario, NOT a PLA or metal material allowable.
    # Side clamp head: 4 x 2 section around screw bore approximated by subtracting
    # a circular 1.2-mm bore. Cup load shaft: solid 2 x 2 lower stem.
    i_head=4*2**3/12-math.pi*1.2**4/64
    i_col=1.6*1.2**3/12
    for name,ec,eh,ih,ic in [('side',.95,1.35,i_head,i_col),
                           ('balanced_residual_005',.05,.05,2*2**3/12,1.2**4/12)]:
        for E,F in product((500.,2000.,100000.),(.06,.1,1.,10.)):
            vals=[]
            for h in (0.,40.):
                dc=beam_tip(F*ec,45-h,SPAN,E,ic)[0]
                dh=beam_tip(F*eh,h+10,SPAN,E,ih)[0]
                vals.append(dc+dh)
            out.append({'capture':name,'E_N_mm2':E,'force_N':F,
                        'relative_tip_bound_mm':max(vals),
                        'within_small_deflection_screen':max(vals)<.5})
    return out


def load_margin():
    # Deliberately paired with E-123's labelled 5-g/.060-N guide-drag scenario.
    # Sum FREE beam responses as a misfit screen; this is not a coupled contact
    # solver. A closed joint reacts this misfit, rather than separating by it.
    cup=Cup()
    remaining=min(cup.margins(.025,.005).values())-RESERVE
    per_force=max(beam_tip(.05,45-h,SPAN,2000,1.2**4/12)[0]
                  +beam_tip(.05,h+10,SPAN,2000,2*2**3/12)[0] for h in (0,40))
    upward=.005*9.81+.060
    out=[]
    for warp,acceleration in product((0.,.025,.05),(0.,5.)):
        force=upward+.005*acceleration
        deflection=per_force*force
        out.append({'relative_warp_bound_mm':warp,'upward_acceleration_m_s2':acceleration,
                    'required_column_force_N':force,'elastic_bound_mm':deflection,
                    'remaining_free_response_budget_mm':remaining-warp-deflection,
                    'fits_free_response_budget':remaining-warp-deflection>=0})
    return out


def synthesize():
    out={}
    variants=list(product((2.,2.1,2.4,2.8),(1.2,),(.2,.225,.3,.4),
                          (.2,.225,.3,.4),(.2,.225,.3,.4),(.6,.8)))
    for e,c in product((.025,.05,.1), (0.,.005,.025,.05)):
        passed=[]; failures={}
        for f,s,o,b,en,w in variants:
            v=Cup(f,s,o,b,en,w)
            bad=[k for k,x in v.margins(e,c).items() if x<RESERVE-1e-10]
            if bad:
                for k in bad: failures[k]=failures.get(k,0)+1
            else:
                finite_cup_check(v)
                passed.append(v)
        best=min(passed,key=lambda v:v.half_width) if passed else None
        # Adapt the side-clamp section to a 2-mm screw/nut housing, with
        # only the guide-error envelope added to E-123's conservative section bound.
        side_envelope=1.2+2.+8*(relative_bound(e,c)+RESERVE)
        out[f'{e:g}/{c:g}']={'generated':len(variants),'cup_sections':len(passed),
            'failed_gates_nonexclusive':failures,'narrowest':None if best is None else best.__dict__,
            'side_clamp_required_pitch_under_enclosure_mm':side_envelope}
    return out


def tests():
    # Guide heights must be coupled to the same actual column height.
    for c,h in product((0.,.005,.025,.05),range(41)):
        dc,dh,_=guide_excursion(h,c)
        assert math.isclose(dc+dh,(2+110/SPAN)*c,abs_tol=1e-12)
        for low,high in product((-c,c),repeat=2):
            xc=low+(high-low)*(h-45)/SPAN
            assert abs(xc)<=dc+1e-12
            xh=high+(high-low)*(h+10)/SPAN
            assert abs(xh)<=dh+1e-12
    for L in (0.,5.,45.):
        exact=beam_tip(.095,L,30,2000,.2304)
        for n in (16,64,256):
            numeric=beam_holdout(.095,L,30,2000,.2304,n)
            assert max(abs(x-y) for x,y in zip(exact,numeric))<1e-10
    assert beam_tip(0,45,30,2000,.2304)==(0,0)
    assert math.isclose(beam_tip(.1,45,30,4000,.2304)[0]*2,
                        beam_tip(.1,45,30,2000,.2304)[0])
    witness=Cup()
    finite_cup_check(witness,holdout=True)
    assert min(witness.margins(.025,.005).values())>RESERVE
    # Existing exclusions remain executable, not superseded by new capture names.
    assert a.packing_bound(.1)>PITCH
    assert a.guide_collision()['witness_mm3']>0
    assert .005*9.81-.060<0
    return {'cup_witness':witness.__dict__, 'margins_at_e0025_c0005':witness.margins(.025,.005),
            'E123_finite_rotated_collision':guide_collision_witness(),
            'remaining_relative_warp_plus_bending_allowance_mm':min(witness.margins(.025,.005).values())-RESERVE,
            'relative_enclosure_at_e005_c0025_mm':relative_bound(.05,.025),
            'side_spine_I_mm4':4*2**3/12-math.pi*1.2**4/64,
            'column_I_mm4':1.6*1.2**3/12,
            'cup_nominal_closure_stroke_x_mm':witness.stroke,
            'cup_nominal_takeup_z_mm':witness.gap}


if __name__=='__main__':
    print(json.dumps({'checks':tests(),'population':synthesize(),'force':force_screen(),
                      'combined_load':load_margin()},indent=2))
