#!/usr/bin/env python3
"""Finite direct-head acquisition screen. mm, N, s; deterministic bounds, no priors.
Run directly for self-checks and compact JSON. No generated files retained.
"""
from dataclasses import dataclass
from itertools import product
import json
import math

PITCH = 5.08
RESERVE = .025  # geometric screen only

@dataclass(frozen=True)
class Box:
    x: tuple
    y: tuple
    z: tuple

    def move(self, dx=0., dy=0., dz=0.):
        return Box(*[(a+d,b+d) for (a,b),d in zip((self.x,self.y,self.z),(dx,dy,dz))])

    def grow(self, r):
        return Box(*[(a-r,b+r) for a,b in (self.x,self.y,self.z)])

    def volume_intersection(self, other):
        return math.prod(max(0.,min(b,d)-max(a,c)) for (a,b),(c,d) in
                         zip((self.x,self.y,self.z),(other.x,other.y,other.z)))

    def sweep(self, axis, distance):
        axes=[self.x,self.y,self.z]
        a,b=axes[axis];axes[axis]=(a+min(0.,distance),b+max(0.,distance))
        return Box(*axes)

@dataclass(frozen=True)
class Shoe:
    flange: float = 2.8  # y; x width fixed at 4
    stem: float = 1.2    # y; x width fixed at 1.6
    overlap: float = .5
    back_gap: float = .25
    web: float = .6
    gap: float = .4      # each side of 1.2-mm flange in z
    lip: float = .8

    @property
    def depth(self): return self.overlap+self.back_gap+self.web
    @property
    def shift(self): return (PITCH-self.flange)/2+self.overlap-self.depth/2

    def parts(self, h=0., engaged=True):
        back=-self.flange/2-self.back_gap
        nose=-self.flange/2+self.overlap
        dy=0 if engaged else -self.shift
        # C section: positive top/bottom lips and connecting web, plus drive spine.
        return [b.move(dy=dy,dz=h) for b in (
            Box((-2,2),(back-self.web,nose),(-self.gap-self.lip,-self.gap)),
            Box((-2,2),(back-self.web,nose),(1.2+self.gap,1.2+self.gap+self.lip)),
            Box((-2,2),(back-self.web,back),(-self.gap,1.2+self.gap)),
            Box((-1,1),(back-self.web,back),(-50,-self.gap-self.lip)),
        )]

    def margins(self,e):
        # Each solid has independent +/-e translation per axis and +/-e face error.
        # Thus two distinct surfaces close by at most 4e. Common rigid shifts cancel.
        d=4*e
        return {'aisle':(PITCH-self.flange-self.depth)/2-d,
                'web_to_flange':self.back_gap-d,
                'nose_to_stem':(self.flange-self.stem)/2-self.overlap-d,
                'contact_overlap':self.overlap-d,
                'vertical_entry':self.gap-d,
                'x_neighbor':PITCH-4-d,
                'home':4-(1.2+self.gap+self.lip)-d,
                'fixed_frame':44.5-(40+.6+2*self.gap+1.2+self.lip)-d}


def column(s,h):
    return [Box((-2,2),(-s.flange/2,s.flange/2),(h,h+1.2)),
            Box((-.8,.8),(-s.stem/2,s.stem/2),(h+1.2,h+110))]


def exact_sweep_check(s,e):
    """Sufficient clearance proof with swept solids, including arbitrary neighbors.
    Contact legs intentionally touch flange; those use exact unilateral constraints.
    All unrelated solids are inflated by 2e each, not sampled probability draws.
    """
    # Parked head rising from home to any old height, including every z between.
    parked=[b.sweep(2,44) for b in s.parts(-4,False)]
    # Insertion at relative old height 0; any old height is a common translation.
    entry=[b.sweep(1,s.shift) for b in s.parts(0,False)]
    # Entire engaged trajectory, including contact take-up and .6-mm unload.
    # Range deliberately includes too much for each own-column contact state;
    # only compare this envelope to OTHER columns and stationary frame.
    drive=[b.sweep(2,44.6+s.gap) for b in s.parts(-4,True)]
    # Neighbor column h in [0,40], independently and continuously.
    neighbor_base=[b.sweep(2,40) for b in column(s,0)]
    for dx,dy in product((-PITCH,0,PITCH),repeat=2):
        if dx==dy==0: continue
        obstacles=[b.move(dx,dy).grow(2*e) for b in neighbor_base]
        for phase in (parked,entry,drive):
            assert all(a.grow(2*e).volume_intersection(b)==0 for a in phase for b in obstacles)
    assert all(a.grow(2*e).volume_intersection(b.grow(2*e))==0
               for a in entry for b in column(s,0))
    # Own column at ANY height cannot meet parked head during vertical acquisition.
    assert all(a.grow(2*e).volume_intersection(b.grow(2*e))==0
               for a in parked for b in neighbor_base)
    # Returning/scanning at home: highest point below every foot, for any XY path.
    assert max(b.z[1] for b in s.parts(-4))+2*e < -2*e
    return True


def population():
    values=((2.4,2.8,3.2,3.6),(1.2,1.6,2.),(.3,.5,.7),(.15,.25,.45),(.6,.8),(.25,.4,.6))
    out={}
    for e in (.025,.05,.1,.2):
        n=0;best=None;reasons={}
        for f,stem,o,b,w,g in product(*values):
            s=Shoe(f,stem,o,b,w,g)
            bad=[k for k,v in s.margins(e).items() if v<RESERVE-1e-12]
            if bad:
                for k in bad: reasons[k]=reasons.get(k,0)+1
            else:
                exact_sweep_check(s,e)
                n+=1
                if best is None or s.depth<best.depth:best=s
        out[str(e)]={'generated':math.prod(map(len,values)), 'admitted_sections':n,
                      'failed_gates_nonexclusive':reasons,'shallowest':None if best is None else best.__dict__}
    return out


def packing_bound(e,stem_min=1.2,web_min=.6):
    # Necessary for robust side entry: o,b >= d+r, f >= stem+2o+2(d+r),
    # pitch >= f+(o+b+web)+2(d+r); eliminate o,b,f. No grid assumption.
    return stem_min+web_min+8*(4*e+RESERVE)


def pad_check(e):
    # Centered unilateral pad: contact face below collar, no upper lip or side entry.
    pad=Box((-2,2),(-1.4,1.4),(-.8,0))
    s=Shoe()
    for dx,dy in product((-PITCH,0,PITCH),repeat=2):
        if dx==dy==0: continue
        for b in column(s,0):
            assert pad.sweep(2,40.6).grow(2*e).volume_intersection(
                b.sweep(2,40).move(dx,dy).grow(2*e))==0
    return {'x_neighbor_margin':PITCH-4-4*e,
            'y_neighbor_margin':PITCH-2.8-4*e}


def supported_transaction(s,old,target):
    """Friction-free prescribed coordinates, not a powered implementation.
    Records (head_reference, column_height, ground_contact, lower_lip_contact).
    Closing lock and readback are still task-2 obligations.
    """
    return [(old,old,True,False),
            (old+s.gap,old,True,True),
            (old+s.gap+.6,old+.6,False,True),
            (target+s.gap+.6,target+.6,False,True),
            (target+s.gap,target,True,True),
            (target,target,True,False)]


def guide_collision():
    # Fixed rectangular guide's rear wall, aperture around 1.6-mm stem.
    wall=Box((-1.7,1.7),(-1.7,-.9),(44.5,45.5))
    tooth=Box((-.4,.4),(-2,-.2),(44.6,45.4))
    assert math.isclose(wall.volume_intersection(tooth),.512)
    # Common acquisition datum must reach the shortest material at old=40.
    # A +40 move from old=0 then necessarily crosses the guide plane.
    acquisition_min=40+1.2
    datum_max_to_avoid=44.5-40-.4
    return {'witness_mm3':wall.volume_intersection(tooth),
            'common_acquisition_min_z':acquisition_min,
            'max_z_avoiding_guide_on_plus40':datum_max_to_avoid,
            'nominal_discrete_phase_window':3-.8,
            'phase_window_at_e_005':3-.8-8*.05}


def tests():
    # Box sweep is exact for a translation along one coordinate.
    a=Box((0,1),(0,1),(0,1));b=Box((.5,2),(.5,2),(.5,2))
    assert math.isclose(a.volume_intersection(b),.125)
    assert a.sweep(0,-2).x==(-2,1)
    s=Shoe();assert min(s.margins(.05).values())>=RESERVE
    assert packing_bound(.1)>PITCH
    # Independently instantiate equality dimensions from the eliminated constraints.
    d=4*.1+RESERVE
    eq=Shoe(1.2+4*d,1.2,d,d,.6,d)
    assert math.isclose(eq.flange+eq.depth+2*d,packing_bound(.1))
    exact_sweep_check(s,.05)
    # Fine nominal holdouts: insert, then move touching bottom lip. Independent
    # check of sample vertices against actual own foot/stem, not just margins.
    for steps in (16,64,256):
        for i in range(steps+1):
            q=i/steps
            for a in s.parts(0,False):
                assert all(a.move(dy=s.shift*q).volume_intersection(b)==0 for b in column(s,0))
            h=40*q
            for a in s.parts(h+s.gap):
                assert all(a.volume_intersection(b)<1e-10 for b in column(s,h))
    # At both retained endpoints, flange contacts (does not intersect) lower or upper lip.
    for h in (0,20,40):
        for H in (h+s.gap,h-s.gap):
            assert all(a.volume_intersection(b)<1e-10 for a in s.parts(H) for b in column(s,h))
    for old,target in product(range(0,41,5),repeat=2):
        states=supported_transaction(s,old,target)
        assert all(g or p for _,_,g,p in states)
        assert all(math.isclose(H-s.gap,h) for H,h,g,p in states if p)
    # Finite coherent bank error, not a proof by failed sufficient bounds:
    # at e=.1, shoe shifts +e with web forward face +e; flange shifts -e
    # with rear face -e. Nominal .25-mm web gap becomes -.15 mm.
    web=s.parts()[2].move(dy=.1)
    web=Box(web.x,(web.y[0],web.y[1]+.1),web.z)
    flange=column(s,0)[0].move(dy=-.1)
    flange=Box(flange.x,(flange.y[0]-.1,flange.y[1]),flange.z)
    witness=web.volume_intersection(flange)
    assert math.isclose(witness,.72,abs_tol=1e-12)
    # Exact lower-pad force balance N=m(g-a_down)-drag.
    m=.005;drag=.06;g=9.81
    assert m*g-drag<0
    # 2g slot play remains at nominal geometry; opposite errors expand by 4e.
    play=2*s.gap+4*.05
    v=math.sqrt(2*g*play/1000)
    assert math.isclose(.5*m*v*v,m*g*play/1000)
    return {'shoe_nominal':s.__dict__,'margins_e_005':s.margins(.05),
            'web_collision_e_01_mm3':witness,'shared_y_entry_stroke_mm':s.shift,
            'nominal_vertical_play_mm':2*s.gap,'play_upper_e_005_mm':play,
            'unloaded_drop_speed_over_play_m_s':v,
            'guide_collision':guide_collision(),
            'necessary_pitch_at_e_01':packing_bound(.1),
            'continuous_error_ceiling_mm':(PITCH-1.2-.6-8*RESERVE)/32,
            'pad_e_02':pad_check(.2),
            'nominal_shoe_volume_mm3':sum(math.prod(b-a for a,b in (v.x,v.y,v.z)) for v in s.parts()),
            'guide_side_reaction_N_at_10N_30mm_span':10*(s.flange/2-s.overlap/2)/30}


if __name__=='__main__':
    print(json.dumps({'checks':tests(),'population':population()},indent=2))
