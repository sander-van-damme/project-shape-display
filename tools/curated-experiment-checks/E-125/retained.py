#!/usr/bin/env python3
"""Finite retained-jaw synthesis and support-loss falsifier. Units mm, N, radians.
Deterministic design/bound scenarios, not process priors or a hardware simulator.
Standard library only. Printed JSON is reproducible; do not retain it.
"""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location('capture', Path(__file__).parents[1]/'E-124'/'capture.py')
c = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = c
spec.loader.exec_module(c)
a = c.a
SQ = math.sqrt(2)


@dataclass(frozen=True)
class Prism:
    """Convex x,z polygon extruded along y; finite solids, not centre lines."""
    name: str
    polygon: tuple
    y: tuple

    def move(self, x=0., y=0., z=0.):
        return Prism(self.name, tuple((i+x,j+z) for i,j in self.polygon),
                     (self.y[0]+y,self.y[1]+y))

    def overlap(self, other):
        depth=max(0., min(self.y[1],other.y[1])-max(self.y[0],other.y[0]))
        if depth<=0: return 0.
        for axis in (0,1):
            if max(v[axis] for v in self.polygon)<=min(v[axis] for v in other.polygon) or max(v[axis] for v in other.polygon)<=min(v[axis] for v in self.polygon): return 0.
        return depth*c.clipped_area(list(self.polygon),list(other.polygon))

    def mirror(self):
        return Prism(self.name,tuple((-x,z) for x,z in reversed(self.polygon)),self.y)


def rect(name,x,z,y):
    return Prism(name, ((x[0],z[0]),(x[1],z[0]),(x[1],z[1]),(x[0],z[1])),y)


def oblique(name,center,u,v,y):
    # u along 45-degree slide, v normal to it; orientation remains CCW.
    return Prism(name,tuple((center[0]+(s-t)/SQ,center[1]+(s+t)/SQ)
                           for s,t in ((u[0],v[0]),(u[1],v[0]),(u[1],v[1]),(u[0],v[1]))),y)


def closed_slot(name,center,length,r,g,wall,y,diagonal):
    """Four walls including BOTH end caps; moving square pin has no open escape.
    Diagonal pin has half-side r in slide coordinates; horizontal slot encloses
    the projected pin. End caps are beyond both travel endpoints.
    """
    half=r+g
    lo,hi=-half,length+half
    out=[]
    for s in (-1,1):
        vr=(-half-wall,-half) if s<0 else (half,half+wall)
        ur=(lo-wall,lo) if s<0 else (hi,hi+wall)
        if diagonal:
            out.append(oblique(name,center,(lo-wall,hi+wall),vr,y))
            out.append(oblique(name,center,ur,(-half,half),y))
        else:
            out.append(rect(name,(center[0]+lo-wall,center[0]+hi+wall),
                            (center[1]+vr[0],center[1]+vr[1]),y))
            out.append(rect(name,(center[0]+ur[0],center[0]+ur[1]),
                            (center[1]-half,center[1]+half),y))
    return out


@dataclass(frozen=True)
class Joint:
    r: float                 # square pin HALF-side in diagonal coordinates
    wall: float              # slot wall in plane, and plate/retainer thickness
    gap: float               # nominal fit gap at every separately moving interface
    lip: float = .15         # cap overhang beyond through pin

    def bodies(self,q):
        """q=0 open, 1 closed. One downward shuttle stroke=.4 mm.
        Two pins/jaw constrain yaw in x-z; four closed slots/jaw retain and reset.
        Pin stem spans stationary oblique plate then moving horizontal-slot plate;
        enlarged end cap prevents axial escape. Bilateral front/back construction.
        The shuttle is connected by side strips and a lower bridge on each y side.
        Stationary plates connect at their outer sides and at the lower bridge.
        No motor, nut, lead screw or vertical carriage is hidden in this generator.
        """
        fixed=[]; shuttle=[]; moving=[]
        # Replaces E-124 base, which would intersect translating rigid jaw webs.
        fixed.append(rect('pad',(-1,1),(-.8,0),(-1.4,1.4)))
        fixed.append(rect('pedestal',(-.5,.5),(-7,-.8),(-.7,.7)))
        for side in (-1,1):
            jaw=[rect('jaw_web',(1.6-.4*q,2.2-.4*q),(-5.8-.4*q,2.4-.4*q),(-.8,.8)),
                 rect('jaw_pad',(1.2-.4*q,1.6-.4*q),(1.6-.4*q,2.4-.4*q),(-.8,.8))]
            for ys in (-1,1):
                y0=.8+self.gap
                rail_y=(y0,y0+self.wall)
                drive_y=(rail_y[1]+self.gap,rail_y[1]+self.gap+self.wall)
                cap_y=(drive_y[1]+self.gap,drive_y[1]+self.gap+self.wall)
                def yy(yy): return yy if ys==1 else (-yy[1],-yy[0])
                rail=[]; drive=[]
                for z in (-3.,-5.):
                    pin_center=(1.9-.4*q,z-.4*q)
                    jaw.append(oblique('pin',pin_center,(-self.r,self.r),(-self.r,self.r),yy((.8,cap_y[0]))))
                    jaw.append(oblique('pin_cap',pin_center,(-self.r-self.lip,self.r+self.lip),
                                       (-self.r-self.lip,self.r+self.lip),yy(cap_y)))
                    rail+=closed_slot('fixed_channel',(1.5,z-.4),.4*SQ,self.r,self.gap,self.wall,yy(rail_y),True)
                    drive+=closed_slot('shuttle_channel',(1.5,z-.4*q),.4,self.r*SQ,self.gap,self.wall,yy(drive_y),False)
                # Connect both slot housings and bilateral halves below the jaw.
                for group,dy,zz in ((rail,rail_y,0.),(drive,drive_y,-.4*q)):
                    xmax=max(x for p in group for x,z in p.polygon)
                    group.append(rect('side_bridge',(xmax-self.wall,xmax),(-7+zz,-3+zz),yy(dy)))
                    group.append(rect('bottom_bridge',(-xmax,xmax),(-7.4+zz,-7+zz),yy(dy)))
                fixed += [p if side==1 else p.mirror() for p in rail]
                shuttle += [p if side==1 else p.mirror() for p in drive]
            moving += [p if side==1 else p.mirror() for p in jaw]
        # Back and front fixed bridges join central pedestal; shuttle stays outside.
        far=.8+self.gap+self.wall
        fixed.append(rect('frame_tie',(-.5,.5),(-7.4,-7),(-far,far)))
        far+=self.gap+self.wall
        # Downward offset separates moving bridge from fixed tie through its stroke.
        shuttle.append(rect('drive_tie',(-.5,.5),(-8.4-.4*q,-8-.4*q),(-far,far)))
        for ys in (-1,1):
            yi=(far-self.wall,far) if ys==1 else (-far,-far+self.wall)
            shuttle.append(rect('drive_link',(-.5,.5),(-8.4-.4*q,-7.2-.4*q),yi))
        return fixed,shuttle,moving

    def envelope(self):
        b=sum(self.bodies(0),[])+sum(self.bodies(1),[])
        return max(abs(x) for p in b for x,z in p.polygon),max(abs(y) for p in b for y in p.y)


def geometry_check(j,n=16):
    """Actual polygons, intentional pin/jaw joins excluded, different groups tested.
    Body paths are translations, so swept polygon convex hulls are exact against
    fixed obstacles; moving-to-moving use relative endpoint translation.
    """
    foot=rect('foot',(-1,1),(0,1.2),(-1.4,1.4))
    stem=rect('stem',(-.6,.6),(1.2,110),(-.6,.6))
    maxima={'moving_fixed':0.,'moving_shuttle':0.,'own_column':0.}
    for i in range(n+1):
        q=i/n;fixed,shuttle,moving=j.bodies(q)
        maxima['moving_fixed']=max(maxima['moving_fixed'],max(p.overlap(o) for p in moving+shuttle for o in fixed))
        maxima['moving_shuttle']=max(maxima['moving_shuttle'],max(p.overlap(o) for p in moving for o in shuttle))
        maxima['own_column']=max(maxima['own_column'],max(p.overlap(o) for p in fixed+shuttle+moving for o in (foot,stem)))
    return maxima


def hull(points):
    points=sorted(set(points))
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    def half(seq):
        h=[]
        for p in seq:
            while len(h)>1 and cross(h[-2],h[-1],p)<=0: h.pop()
            h.append(p)
        return h
    return tuple(half(points)[:-1]+half(reversed(points))[:-1])


def sweep_overlap(p0,p1,o0,o1):
    # All paths in this mechanism are affine translations; remove obstacle motion.
    dx=o1.polygon[0][0]-o0.polygon[0][0]
    dz=o1.polygon[0][1]-o0.polygon[0][1]
    assert o0.y==o1.y and p0.y==p1.y
    pp=Prism('sweep',hull(p0.polygon+p1.move(-dx,0,-dz).polygon),p0.y)
    return pp.overlap(o0)


def continuous_check(j):
    f0,s0,m0=j.bodies(0);f1,s1,m1=j.bodies(1)
    # Relative sweeps catch interior collisions that endpoint checks miss.
    pairs=((m0+s0,m1+s1,f0,f1),(m0,m1,s0,s1))
    maxima=[]
    for p0,p1,o0,o1 in pairs:
        maxima.append(max(sweep_overlap(x,y,u,v) for x,y in zip(p0,p1) for u,v in zip(o0,o1)))
    # Acquire open from below; paired guide plates are below the foot throughout.
    foot=rect('foot',(-1,1),(0,1.2),(-1.4,1.4))
    stem=rect('stem',(-.6,.6),(1.2,110),(-.6,.6))
    own=max(sweep_overlap(p.move(z=-4),p,o,o) for p in f0+s0+m0 for o in (foot,stem))
    closing=max(sweep_overlap(x,y,o,o) for x,y in zip(f0+s0+m0,f1+s1+m1) for o in (foot,stem))
    return max(maxima+[own,closing])


def synthesize():
    rows=[];witness=None
    # Same topology, not architecture diversity. No pseudo-random sampling.
    for e in (.025,.05,.1):
        gap=4*e+a.RESERVE
        failed={};survivors=[]
        for r,w in product((.1,.2,.3),(.2,.4,.6)):
            j=Joint(r,w,gap)
            x,y=j.envelope()
            # Both heads may take adverse lower-guide corners at different heights.
            hh=4*e+2*max(c.guide_excursion(h,.005)[1] for h in (0,40))+4*6*math.sin(math.atan(.01/30)/2)
            margins={'x_heads':5.08-2*x-hh,'y_heads':5.08-2*y-hh,
                     'cup':min(c.Cup().margins(e,.005).values())}
            bad=[k for k,v in margins.items() if v<a.RESERVE]
            if not bad:
                collision=continuous_check(j)
                if collision>1e-9: bad.append('finite_collision')
            if bad:
                for k in bad: failed[k]=failed.get(k,0)+1
            else:
                survivors.append({'pin_side_mm':2*r,'wall_mm':w,'x_width_mm':2*x,'y_width_mm':2*y,'margins_mm':margins})
                if witness is None: witness=j
        rows.append({'e_mm':e,'guide_half_play_mm':.005,'fit_gap_mm':gap,
                     'generated':9,'survivors':survivors,'failures_nonexclusive':failed})
    return rows,witness


def pose(p,shift,theta):
    return Prism(p.name,tuple((shift+x*math.cos(theta)+z*math.sin(theta),
                             -x*math.sin(theta)+z*math.cos(theta)) for x,z in p.polygon),p.y)


def layout_witness():
    j=Joint(.1,.2,.125)
    f,s,m=j.bodies(0)
    # Actual opposing guide-corner poses at h=40. Independent datum offsets
    # +/-e; NO manufactured face enlargement needed for this failure witness.
    e,cg=.025,.005
    shift=e+c.guide_excursion(40,cg)[1]
    theta=math.atan(2*cg/30)
    left=[pose(p,shift,theta) for p in f+s+m]
    right=[pose(p,5.08-shift,-theta) for p in f+s+m]
    volume=max(p.overlap(o) for p in left for o in right)
    assert volume>0
    # Legal wider internal layout: every-other-column heads. Actual retained
    # bodies are reused at 10.16 mm, not assumed to fit in a 5.08-mm box.
    spaced=[pose(p,10.16-shift,-theta) for p in f+s+m]
    assert max(p.overlap(o) for p in left for o in spaced)<1e-10
    # All fixed/moving head bodies across their 40-mm stroke versus columns at
    # arbitrary independent heights: swept full-height foot/stem obstacles.
    f1,s1,m1=j.bodies(1)
    swept=[Prism(p.name,hull(p.polygon+q.polygon+p.move(z=40).polygon+q.move(z=40).polygon),p.y)
           for p,q in zip(f+s+m,f1+s1+m1)]
    for dx,dy in product((-5.08,0,5.08),repeat=2):
        if dx==dy==0: continue
        obs=[rect('foot',(-1+dx,1+dx),(0,41.2),(-1.4+dy,1.4+dy)),
             rect('stem',(-.6+dx,.6+dx),(1.2,150),(-.6+dy,.6+dy))]
        assert max(p.overlap(o) for p in swept for o in obs)<1e-10
    # Cap cannot pass the nominal diagonal slot; a finite overhang exists.
    # This bounds face variation only, not worn caps, bending or assembly failure.
    cap_margin=SQ*(j.r+j.lip-e)-(SQ*j.r+j.gap+e)
    internal=continuous_check(j)
    convergence=[geometry_check(j,n) for n in (8,32,128)]
    assert internal<1e-9 and all(max(row.values())<1e-9 for row in convergence)
    return {'joint':j.__dict__,'widths_mm':[2*v for v in j.envelope()],
            'adjacent_head_max_pair_collision_mm3':volume,'nominal_head_gap_mm':5.08-2*j.envelope()[0],
            'datum_offset_mm':e,'guide_half_play_mm':cg,'theta_rad':theta,
            'sparse_spacing_mm':10.16,'sparse_nominal_column_sweep_collision_mm3':0.,
            'cap_vertical_overhang_with_face_bounds_mm':cap_margin,
            'continuous_internal_collision_mm3':internal,
            'collision_convergence':convergence}


def loaded_closure():
    """Real closing-wall contacts, including channel play, not a prescribed pin
    following the middle of a clearance slot. Downward cam force takes the pin
    to v=-gap of the diagonal guide; shuttle upper wall then bears on pin top.
    The return stroke must traverse the opposite walls: no zero-backlash credit.
    """
    j=Joint(.1,.2,.125)
    offset=j.gap/SQ
    q_touch=1-offset/.4
    def bodies(q):
        fixed,shuttle,moving=j.bodies(q)
        # Each jaw is its own rigid body, first left then right in generator.
        moving=[p.move(x=(-offset if i<len(moving)//2 else offset),z=-offset)
                for i,p in enumerate(moving)]
        return fixed,[p.move(z=-j.gap-offset) for p in shuttle],moving
    f0,s0,m0=bodies(0);f1,s1,m1=bodies(q_touch)
    foot=rect('foot',(-1,1),(0,1.2),(-1.4,1.4))
    maxima=[max(sweep_overlap(p,q,o,t) for p,q in zip(m0+s0,m1+s1) for o,t in zip(f0,f1)),
            max(sweep_overlap(p,q,o,t) for p,q in zip(m0,m1) for o,t in zip(s0,s1)),
            max(sweep_overlap(p,q,foot,foot) for p,q in zip(m0,m1))]
    assert max(maxima)<1e-9
    pads=[p for p in m1 if p.name=='jaw_pad']
    assert all(abs(min(z for x,z in p.polygon)-1.2)<1e-12 for p in pads)
    overlap=1-min(x for x,z in pads[1].polygon)
    assert math.isclose(overlap,.2-SQ*j.gap,abs_tol=1e-12)
    # Unwrapped pin normal coordinate exactly touches lower diagonal wall.
    # Shuttle upper aperture boundary exactly touches the pin's top vertex.
    px,pz=1.9-.4*q_touch+offset,-3-.4*q_touch-offset
    normal=(- (px-1.5)+(pz+3.4))/SQ
    assert math.isclose(normal,-j.gap,abs_tol=1e-12)
    aperture_top=-3-.4*q_touch-j.gap-offset+SQ*j.r+j.gap
    assert abs(aperture_top-(pz+SQ*j.r))<1e-12
    # A .025-mm inward foot-face error removes overlap at the height of first
    # top contact. Continuing the rigid diagonal path hits the SIDE of the foot.
    undersize=rect('undersize_foot',(-.975,.975),(0,1.2),(-1.4,1.4))
    q_side=(1.2+offset-.975)/.4
    _,_,later=bodies(q_side+.01)
    collision=max(p.overlap(undersize) for p in later)
    assert q_side>q_touch and collision>0
    return {'guide_normal_play_mm':j.gap,'loaded_jaw_outward_shift_mm':offset,
            'first_nominal_foot_touch_q':q_touch,'nominal_overlap_at_first_touch_mm':overlap,
            'fits_0025_overlap_reserve':overlap>=.025,
            'shuttle_pin_upper_gap_at_loaded_contact_mm':aperture_top-(pz+SQ*j.r),
            'shuttle_closing_takeup_mm':j.gap+offset,
            'reversal_slot_deadband_z_mm':2*j.gap,
            'rigid_body_sweep_collision_mm3':max(maxima),
            'undersize_foot_face_error_mm':.025,'first_side_contact_q':q_side,
            'undersize_foot_rigid_continuation_collision_mm3':collision}


def solve(A,b):
    m=[list(row)+[v] for row,v in zip(A,b)];n=len(b)
    for i in range(n):
        p=max(range(i,n),key=lambda j:abs(m[j][i]));m[i],m[p]=m[p],m[i]
        if abs(m[i][i])<=1e-14: raise ValueError('singular active contact set')
        d=m[i][i];m[i]=[x/d for x in m[i]]
        for j in range(n):
            if j!=i:
                d=m[j][i];m[j]=[x-d*y for x,y in zip(m[j],m[i])]
    return [row[-1] for row in m]


def dot(x,y): return sum(a*b for a,b in zip(x,y))


def compliance(L,E,I):
    return ((L*L*(L+30)/(3*E*I),(L*L/2+10*L)/(E*I)),
            ((L*L/2+10*L)/(E*I),(L+10)/(E*I)))


def contact(E,h,guide,warp,preload,skew,force,k=100.):
    """Convex 3-DOF pair-of-beams energy + unilateral compliant contacts.
    q=(relative x, relative rotation, relative z). Euler-Bernoulli column/head
    in series. Actual shared q reacts misfit; FREE deflections are not added as
    an alleged clamp displacement. The unlocked column has NO axial ground spring;
    local axial/jaw compliance is represented only by the contact stiffness k.
    Five contacts: bottom, two upper shoulders, two web sides. No friction credit.
    """
    A=compliance(45-h,E,1.2**4/12);B=compliance(h+10,E,2**4/12)
    # Upper column overhang points DOWN; lower head overhang points UP.
    # Reflection reverses each column force/rotation cross-compliance.
    C=[[A[i][j]*(1 if i==j else -1)+B[i][j] for j in range(2)] for i in range(2)]
    det=C[0][0]*C[1][1]-C[0][1]**2
    K=[[C[1][1]/det,-C[0][1]/det,0.],[-C[1][0]/det,C[0][0]/det,0.],[0.,0.,0.]]
    c0,c1,h0,h1=guide
    # Actual paired guide endpoint poses, not independently maximised overhangs.
    free=[c0+(c1-c0)*(h-45)/30-(h1+(h1-h0)*(h+10)/30)+warp,
          (c1-c0-h1+h0)/30,0.]
    # phi=dx/dz: x'=u+x+z*phi, z'=w+z-x*phi.
    normals=((0,0,1),(0,-.9,-1),(0,.9,-1),(1,.6,0),(-1,-.6,0))
    offsets=(0.,-preload+skew/2,-preload-skew/2,.2,.2)
    rhs0=[dot(row,free) for row in K];rhs0[2]+=force
    found=None
    for mask in range(32):
        M=[row[:] for row in K];rhs=rhs0[:]
        for j,(n,b) in enumerate(zip(normals,offsets)):
            if mask>>j&1:
                for u in range(3):
                    rhs[u]-=k*b*n[u]
                    for v in range(3): M[u][v]+=k*n[u]*n[v]
        try: q=solve(M,rhs)
        except ValueError: continue
        g=[b+dot(n,q) for b,n in zip(offsets,normals)]
        if all((v<=1e-9 if mask>>i&1 else v>=-1e-9) for i,v in enumerate(g)):
            N=[max(0.,-k*v) for v in g]
            residual=[dot(K[i],[q[j]-free[j] for j in range(3)])-(force if i==2 else 0)-sum(n[i]*f for n,f in zip(normals,N)) for i in range(3)]
            assert max(map(abs,residual))<1e-7
            assert abs(N[0]-N[1]-N[2]+force)<1e-7
            found={'q':q,'normal_N':N,'residual_N_or_Nmm':max(map(abs,residual)),
                   'upper_imbalance_N':abs(N[1]-N[2]),
                   'shoulder_overlap_enclosure_mm':.2-abs(q[0])-1.2*abs(q[1]),
                   'finite_shoulder_overlap_mm':min(
                       max(0.,min(pad[1],q[0]+xr*math.cos(q[1])+1.2*math.sin(q[1]))-
                              max(pad[0],q[0]+xl*math.cos(q[1])+1.2*math.sin(q[1])))
                       for xl,xr,pad in ((-1.,-.6,(-1.2,-.8)),(.6,1.,(.8,1.2)))),
                   'upper_nodes_valid':all(N[index]<1e-8 or pad[0]<=q[0]+x*math.cos(q[1])+1.2*math.sin(q[1])<=pad[1]
                       for index,x,pad in ((1,-.9,(-1.2,-.8)),(2,.9,(.8,1.2)))),
                   'side_contact':N[3]+N[4]>1e-8,
                   'small_angle_domain':abs(q[1])<.05 and abs(q[0])<.5,
                   'elastic_energy_Nmm':.5*sum((q[i]-free[i])*dot(K[i],[q[j]-free[j] for j in range(3)]) for i in range(3))}
            break
    assert found is not None
    return found


def contact_scenarios():
    out=[]
    for E,k in product((500.,2000.,100000.),(10.,100.,1000.)):
        n=side=lost=outside=invalid=0;peak=imbalance=0.;worst=None
        by_guide={v:{'cases':0,'invalid_upper_nodes':0,'overlap_below_reserve':0,'side_contact':0} for v in (.005,.025)}
        for h,cg,warp,pre,skew,force in product((0.,20.,40.),(.005,.025),(-.025,.025),(-.025,.01,.05),(-.05,0.,.05),(-.13405,.01095)):
            for guide in product((-cg,cg),repeat=4):
                r=contact(E,h,guide,warp,pre,skew,force,k);n+=1
                side+=r['side_contact'];lost+=r['finite_shoulder_overlap_mm']<a.RESERVE;outside+=not r['small_angle_domain'];invalid+=not r['upper_nodes_valid']
                by_guide[cg]['cases']+=1
                by_guide[cg]['invalid_upper_nodes']+=not r['upper_nodes_valid']
                by_guide[cg]['overlap_below_reserve']+=r['finite_shoulder_overlap_mm']<a.RESERVE
                by_guide[cg]['side_contact']+=r['side_contact']
                peak=max(peak,max(r['normal_N']));imbalance=max(imbalance,r['upper_imbalance_N'])
                if worst is None or r['finite_shoulder_overlap_mm']<worst['response']['finite_shoulder_overlap_mm']:
                    worst={'h':h,'c':cg,'warp':warp,'preload':pre,'skew':skew,'force':force,'guide':guide,'response':r}
        out.append({'E_N_mm2':E,'contact_k_N_mm':k,'cases':n,'side_contact_cases':side,
                    'finite_overlap_below_reserve':lost,'invalid_fixed_upper_nodes':invalid,'outside_linear_domain':outside,
                    'peak_normal_N':peak,'peak_upper_imbalance_N':imbalance,'by_guide':by_guide,'worst_overlap':worst})
    return out


def screw_torque(F,diameter,lead,mu):
    """Unwrapped square-thread force balance. Positive => brake torque required
    against overhauling. Zero-bearing-friction is a conservative allowed bound.
    Deliberately NOT a claim about a sourced screw, motor or printed friction.
    """
    slope=lead/(math.pi*diameter)
    return F*diameter/2*(slope-mu)/(1+mu*slope)


def drive_screen():
    out=[]
    for d,lead in product((1.2,2.,3.),(.25,.5,1.)):
        out.append({'mean_thread_d_mm':d,'lead_mm':lead,'self_lock_min_mu':lead/(math.pi*d),
                    'gravity_load_N':.04905,'guide_drag_N':0.,
                    'backdrive_torque_Nmm_at_mu_005':screw_torque(.04905,d,lead,.05),
                    'backdrive_torque_Nmm_at_mu_01':screw_torque(.04905,d,lead,.1),
                    'backdrive_torque_Nmm_frictionless':screw_torque(.04905,d,lead,0.)})
    # A drive with any positive lead fails an unconditional zero-friction bound.
    # Wider packaging helps nominal self-lock at mu=.1; do not universalise this.
    assert all(r['backdrive_torque_Nmm_frictionless']>0 for r in out)
    return out


def ground_and_faults():
    """Finite rectangular ground bolt witness, NOT an implemented powered lock.
    Nine rack slots at 5-mm pitch, 3-mm tall, bolt .6 tall, .4 engagement,
    .9 withdrawal. Positive ground support cannot be SET at arbitrary height.
    Bolt top at z=45; rack slot ceilings=45+h-5*k.
    """
    bolt=rect('ground_bolt',(-.5,.4),(44.4,45.),(-.4,.4))
    # Nine voids have upper faces at 45+h-5*k and height 3. The material
    # above each void rests on the bolt TOP. Rack walls outside voids are solid.
    ranges=[];low=-43.
    for lo,hi in sorted((-3-5*k,-5*k) for k in range(9)):
        if lo>low: ranges.append((low,lo))
        low=hi
    ranges.append((low,3.))
    def supported_solids(h):
        return ([rect('rack',(0,1.6),(45+h+lo,45+h+hi),(-.6,.6)) for lo,hi in ranges]
                +[rect('rack_spine',(1.6,2.2),(2+h,48+h),(-.6,.6))])
    # Four walls of finite bolt guide, outside rack; actuator is NOT granted.
    guide=[rect('guide',(-1.5,-.1),(44.275,45.125),yy) for yy in ((-.925,-.525),(.525,.925))]
    guide += [rect('guide',(-1.5,-.1),zz,(-.525,.525)) for zz in ((43.875,44.275),(45.125,45.525))]
    assert max(sweep_overlap(bolt.move(x=-.9),bolt,o,o) for o in guide)<1e-10
    seating=max(bolt.overlap(o) for o in supported_solids(0))
    insertion=max(sweep_overlap(bolt.move(x=-.9),bolt,o,o) for o in supported_solids(.8))
    midpoint=max(sweep_overlap(bolt.move(x=-.9),bolt,o,o) for o in supported_solids(2.5))
    assert seating<1e-10 and insertion<1e-10 and midpoint>0
    # Exhaust required support states with actual and reported support separated.
    states=[('idle',0,1,0),('acquire',1,1,0),('clamp',1,1,1),('unload',1,1,1),
            ('unlock',1,0,1),('up',1,0,1),('down',1,0,1),('reseat',1,1,1),
            ('proof',1,1,1),('withdraw',1,1,0),('reset',0,1,0)]
    faults=[]
    for phase,cmd,g,carrier in states:
        assert g or carrier
        if not g:
            faults.append({'phase':phase,'fault':'power_loss_with_backdrivable_axis','support_after_fault':False,
                           'positive_jaw_attachment':True,'command_retained':bool(cmd),
                           'safe_recovery_implemented':False})
    faults.extend([
        {'phase':'proof_to_withdraw','fault':'common_false_ground_and_height_read','actual_ground':False,'reported_ground':True,'support_after_fault':False},
        {'phase':'reseat','fault':'clear_command_on_ground_set','retained_through_withdrawal':False},
        {'phase':'unlock','fault':'missed_capture_common_readback','actual_carrier':False,'reported_carrier':True,'support_after_fault':False},
        {'phase':'travel','fault':'jam_detected_with_power_available','action':'retain command and carrier; stop before release','recovery_qualified':False},
        {'phase':'index','fault':'mixed_active_inactive_reset','action':'inactive ground must remain engaged; no shared-complement grant','implemented':False},
    ])
    return {'ground_seated_intersection_mm3':seating,'ground_insert_unloaded_intersection_mm3':insertion,
            'ground_midtravel_insert_collision_mm3':midpoint,'states':states,'faults':faults,
            'admitted_complete_transactions':0,
            'reason':'retained contact is not positive drive arrest; bolt cannot reset at arbitrary travel height; no reader granted'}


def beam_fem_holdout(L,E,I):
    # Independently assembled two Euler-Bernoulli elements; lateral bearings
    # constrain u at z=0,30. Unknown slopes are NOT fixed bearing rotations.
    K=[[0.]*6 for _ in range(6)]
    for nodes,l in (((0,1),30.),((1,2),L)):
        ke=((12,6*l,-12,6*l),(6*l,4*l*l,-6*l,2*l*l),
            (-12,-6*l,12,-6*l),(6*l,2*l*l,-6*l,4*l*l))
        ids=[2*nodes[0],2*nodes[0]+1,2*nodes[1],2*nodes[1]+1]
        for i,u in enumerate(ids):
            for j,v in enumerate(ids): K[u][v]+=E*I/l**3*ke[i][j]
    free=(1,3,4,5);out=[]
    for loaded in (4,5):
        q=solve([[K[i][j] for j in free] for i in free],[float(i==loaded) for i in free])
        out.append(q[-2:])
    return [[out[j][i] for j in range(2)] for i in range(2)]


def tests():
    p=rect('a',(0,1),(0,1),(0,1));assert math.isclose(p.overlap(p),1)
    assert p.overlap(p.move(x=1))==0
    assert sweep_overlap(p,p.move(x=2),p.move(x=1),p.move(x=1))>0
    # Compliance reciprocity, positive energy, modulus scaling and zero load.
    for L in (0.,5.,45.):
        A=compliance(L,2000,1.2**4/12)
        assert A[0][1]==A[1][0] and A[0][0]*A[1][1]>=A[0][1]**2-1e-12
        assert math.isclose(A[1][1],2*compliance(L,4000,1.2**4/12)[1][1])
    for L in (5.,25.,45.):
        analytic=compliance(L,2000,1.2**4/12);holdout=beam_fem_holdout(L,2000,1.2**4/12)
        assert max(abs(analytic[i][j]-holdout[i][j]) for i,j in product(range(2),repeat=2))<1e-8
    r=contact(2000,20,(0,0,0,0),0,0,0,0)
    assert max(map(abs,r['q']))<1e-10 and sum(r['normal_N'])<1e-10
    symmetric=contact(2000,20,(0,0,0,0),0,.01,0,-.10905)
    assert symmetric['upper_imbalance_N']<1e-10
    assert math.isclose(symmetric['normal_N'][0],(2*100*.01+.10905)/3)
    assert math.isclose(symmetric['normal_N'][1],(100*.01-.10905)/3)
    asymmetric=contact(2000,20,(0,0,0,0),0,.01,.05,-.10905)
    assert asymmetric['upper_imbalance_N']>0
    # Energy conservation in the frictionless helical constraint: T*dtheta=F*dz.
    for d,l in product((1.2,3.),(.25,1.)):
        assert math.isclose(screw_torque(.1,d,l,0)*2*math.pi,.1*l)
        assert abs(screw_torque(.1,d,l,l/(math.pi*d)))<1e-12
    assert c.a.packing_bound(.1)>5.08
    assert c.a.guide_collision()['witness_mm3']>0
    assert .005*9.81-.060<0
    assert c.guide_collision_witness()['volume_mm3']>0
    return {'symmetric_contact':symmetric,'asymmetric_contact':asymmetric,'legacy_failures_preserved':True}


if __name__=='__main__':
    checks=tests();population,witness=synthesize()
    print(json.dumps({'checks':checks,'population':population,
                      'layout':layout_witness(),'loaded_closure':loaded_closure(),
                      'witness':None if witness is None else witness.__dict__,
                      'witness_collision_convergence':None if witness is None else [geometry_check(witness,n) for n in (8,32,128)],
                      'contact':contact_scenarios(),'drive':drive_screen(),'transaction':ground_and_faults()},indent=2))
