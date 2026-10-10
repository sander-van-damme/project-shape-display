#!/usr/bin/env python3
"""E-134 finite rigid toggle/front negative. Units mm, N, N mm, radians.
Explicit deterministic bounds; no process distributions or hardware predictions.
"""
import itertools
import json
import math


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm(a):
    return math.sqrt(dot(a, a))


def overlap(a, b):
    return math.prod(max(0, min(hi, hj)-max(lo, lj))
                     for (lo, hi), (lj, hj) in zip(a, b))


class Unit:
    def __init__(self, length=2., high=.5, low=1.7, radius=.65, pad=.15,
                 angle_bias=0.):
        self.l, self.r, self.pad = length, radius, pad
        self.lo = -math.asin(high/length)+angle_bias
        self.hi = math.asin(low/length)+angle_bias
        assert -math.pi/2 < self.lo < 0 < self.hi < math.pi/2
        self.delta = 2*math.asin(pad/radius)
        self.seats = [self.p(self.lo-self.delta), self.p(self.hi+self.delta)]

    def p(self, phi):
        return (self.r*math.sin(phi), self.r*math.cos(phi))

    def height(self, phi):
        return 2*self.l*math.cos(phi)

    def dh(self, phi):
        return -2*self.l*math.sin(phi)

    def points(self, phi, base=0.):
        return [(0., base), (self.l*math.sin(phi), base+self.l*math.cos(phi)),
                (0., base+self.height(phi))]

    def gaps(self, phi):
        return [norm(sub(self.p(phi), seat))-2*self.pad for seat in self.seats]

    def seat_reaction(self, phi, seat, force=1.):
        # Actual normal on the moving circular lug from a stationary circular tip.
        p=self.p(phi)
        n=tuple(v/(2*self.pad) for v in sub(p, seat))
        dp=(self.r*math.cos(phi), -self.r*math.sin(phi))
        # Generalized contact force N*n.dp balances -F*dH/dphi.
        return force*self.dh(phi)/dot(n, dp)


def geometry(u):
    # Two adjacent SERIAL units. Three boundary rings have ideal vertical guides.
    # Lower unit is the confined active front, upper stays on either integral stop.
    # Bars are .2-radius capsules in separate y planes (0 and .8 mm), joined by
    # transverse hinge pins. Lug and stop cylinders occupy y=[-1.0,-.6].
    # Grounded shoe has a circular pin-center track, radius l, fixed to lower ring.
    # Its 0.2-radius knee pin has radial slot clearance .1 (walls l+/- .3).
    # The slot's exact radial reaction does no work along the circular path.
    refinements=[]
    for count in (64,256,1024):
        mingap=1e9
        max_constraint=0.
        poses=0
        for upper in (u.lo,u.hi):
            for direction in (1,-1):
                for i in range(count+1):
                    j=i if direction==1 else count-i
                    phi=u.lo+(u.hi-u.lo)*j/count
                    a=u.points(phi)
                    b=u.points(upper, a[2][1])
                    assert a[2]==b[0]
                    for pts in (a,b):
                        for x,y in zip(pts,pts[1:]):
                            max_constraint=max(max_constraint,abs(norm(sub(y,x))-u.l))
                    mingap=min(mingap,*u.gaps(phi),*u.gaps(upper))
                    # No release of the unchanged stage's endpoint stop.
                    assert min(abs(g) for g in u.gaps(upper))<1e-12
                    # Slot walls at l+/- .3 with a .2-radius centered pin:
                    # .1-mm clearance means nominal wall contact is not assumed.
                    pin_r=norm(a[1])
                    assert min(pin_r-.2-(u.l-.3),u.l+.3-(pin_r+.2))>.099999999
                    # Even granting contact, a radial shoe force does no work.
                    radial=(math.sin(phi),math.cos(phi))
                    tangent=(math.cos(phi),-math.sin(phi))
                    assert abs(dot(radial,tangent))<1e-12
                    # The actual circular shoe shares the lower-link radius.
                    max_constraint=max(max_constraint,abs(norm(a[1])-u.l))
                    poses+=1
        assert mingap>-1e-12 and max_constraint<1e-12
        refinements.append({'intervals':count,'pair_poses':poses,
                            'minimum_tip_gap_mm':mingap,'length_error_mm':max_constraint})
    # All-state x envelope includes bars/pins and both circular stop tips.
    xmin=min(u.l*math.sin(u.lo)-.2, min(s[0]-.15 for s in u.seats))
    xmax=max(u.l*math.sin(u.hi)+.2, max(s[0]+.15 for s in u.seats))
    # Pair separated in x clears in this conservative envelope; not complete CAD.
    # Actual neighbor guide and transverse shoe arm intersect at phi=0:
    # each site's guide is x=+/- .35, y=[-2,-1.6], z=[0,110].
    neighbor= ((-.35,.35),(5.08-2,5.08-1.6),(0.,110.))
    arm= ((-.3,.3),(1.,8.),(u.l-.2,u.l+.2))
    collision=overlap(arm,neighbor)
    assert collision>0
    return {'refinements':refinements,'body_x_envelope_mm':[xmin,xmax],
            'x_neighbor_envelope_gap_mm':5.08-(xmax-xmin),
            'shoe_arm_neighbor_guide_overlap_mm3':collision,
            'nominal_radial_slot_clearance_mm':.1,
            'slot_clearance_adverse_0.05_wall_pin_pose_mm':.1-3*.05,
            'geometry_scope':'generated bars, lug/tips, circular track, arm and guide; bearings, frame and full self-contact unresolved'}


def mechanics(u):
    states=[]
    for f in (.2,1.,10.):
        states.append({'load_N':f,
            'high_barrier_Nmm':f*(2*u.l-u.height(u.lo)),
            'low_barrier_Nmm':f*(2*u.l-u.height(u.hi)),
            'endpoint_normal_N':[u.seat_reaction(u.lo,u.seats[0],f),
                                 u.seat_reaction(u.hi,u.seats[1],f)],
            'max_tangential_input_N':2*f*max(abs(math.sin(u.lo)),abs(math.sin(u.hi)))})
    witness=math.asin(.8/u.l)
    # Unit-speed tangent t=(cos phi,-sin phi); upper bar force at knee
    # is (F*tan phi,-F). Lower bar and shoe-normal reactions are radial.
    tangential=dot((math.tan(witness),-1.),(math.cos(witness),-math.sin(witness)))
    assert abs(tangential-2*math.sin(witness))<1e-12
    # Grounded contacts cannot cancel this tangent unless an added restraint acts.
    assert min(u.gaps(witness))>0 and tangential>0
    # Both branch endpoints are constrained potential minima for F>0.
    assert u.dh(u.lo)>0 and u.dh(u.hi)<0
    return {'loads':states,'loss_phi_rad':witness,'loss_tip_gaps_mm':u.gaps(witness),
            'loss_unbalanced_tangent_per_N':tangential,
            'loss_available_drop_to_low_mm':u.height(witness)-u.height(u.hi),
            'saddle_curvature_Nmm_per_rad2_at_1N':-2*u.l,
            'front_backtracks_after_loss':'interior moves toward an endpoint, not retained',
            'zero_load_geometric_barrier_Nmm':0.,
            'barrier_energy_equivalent_speed_mps_at_1N_0.05kg':math.sqrt(2*(2*u.l-u.height(u.lo))/1000/.05),
            'pair_endpoint_heights_mm':[u.height(a)+u.height(b)
                                       for a,b in itertools.product((u.lo,u.hi),repeat=2)]}


def uncertainty():
    # 81 coherent scenarios. Stop angles = nominal geometry plus common registration
    # bias; length errors change actual travel; no invented normal distributions.
    scenarios=[]
    for length,bias,radius,pad in itertools.product((1.95,2.,2.05),(-.05,0.,.05),
                                                   (.60,.65,.70),(.125,.15,.175)):
        # Keep manufactured stop angular nominal, with coherent error independent
        # of manufactured link length (actual pads are placed by these angles).
        u=Unit(length, length*.25, length*.85, radius,pad,bias)
        stroke=u.height(u.lo)-u.height(u.hi)
        scenarios.append({'stroke':stroke,'barrier':2*u.l-u.height(u.lo),
                          'normal':max(u.seat_reaction(u.lo,u.seats[0]),
                                       u.seat_reaction(u.hi,u.seats[1]))})
    return {'coherent_scenarios':len(scenarios),
            'stage_stroke_mm':[min(s['stroke'] for s in scenarios),max(s['stroke'] for s in scenarios)],
            '23_stage_travel_mm':[23*min(s['stroke'] for s in scenarios),23*max(s['stroke'] for s in scenarios)],
            'high_barrier_at_1N_Nmm':[min(s['barrier'] for s in scenarios),max(s['barrier'] for s in scenarios)],
            'max_endpoint_normal_at_1N_N':[min(s['normal'] for s in scenarios),max(s['normal'] for s in scenarios)],
            'worst_bound_stages_for_40':math.ceil(40/min(s['stroke'] for s in scenarios))}


def board(u):
    stroke=u.height(u.lo)-u.height(u.hi)
    n=math.ceil(40/stroke)
    # A changed cell handles every stage serially. 6 s non-cell work, .05 s/cell
    # acquisition/proof, stage times include conversion, front reposition, settling.
    rows=[]
    for t in (.005,.02,.05):
        service=.05+n*t
        heads=next(c for c in range(1,6401) if 6+math.ceil(6400/c)*service<30)
        rows.append({'stage_s':t,'cell_s':service,'minimum_heads':heads,
                     'at_80_heads_s':6+80*service,
                     'head_bought_ceiling_at_500_and_250_reserve':250/heads})
    return {'stages':n,'stroke_mm':n*stroke,
            'stack_endpoint_height_mm':[n*u.height(u.hi),n*u.height(u.lo)],
            'board_links':6400*2*n,'board_unique_pin_axes_shared_boundaries':6400*(2*n+1),
            'board_stop_interfaces_two_per_stage':6400*2*n,
            'bought_per_joint_ceiling_at_250_residual':250/(6400*(2*n+1)),
            '1N_full_40mm_ideal_work_J':6400*40/1000,
            'schedules':rows,
            'reader_expected_missed_sites':{str(p):6400*p for p in (1e-3,1e-4,1e-5)}}


def checks(u):
    errs=[]
    for n in (64,256,1024):
        dx=(u.hi-u.lo)/n
        work=dx*(.5*u.dh(u.lo)+.5*u.dh(u.hi)+sum(u.dh(u.lo+i*dx) for i in range(1,n)))
        errs.append(abs(work-(u.height(u.hi)-u.height(u.lo))))
    assert errs[2]<errs[1]<errs[0]
    for p in (u.lo,0.,.3,u.hi):
        eps=1e-5
        assert abs((u.height(p+eps)-u.height(p-eps))/(2*eps)-u.dh(p))<1e-9
    # Each circular stop's actual normal balances the generalized load.
    for p,s in ((u.lo,u.seats[0]),(u.hi,u.seats[1])):
        dp=(u.r*math.cos(p),-u.r*math.sin(p))
        normal=tuple(v/(2*u.pad) for v in sub(u.p(p),s))
        assert u.seat_reaction(p,s)>0
        assert abs(u.seat_reaction(p,s)*dot(normal,dp)-u.dh(p))<1e-12
    # Explicit path witness: fixed inactive angle plus shared ring
    # continuity does not constrain it. Explicit path leaves inactive H unchanged.
    upper=u.hi
    assert abs(u.height(upper)-(u.points(upper,u.height(u.lo))[2][1]-u.height(u.lo)))<1e-12
    # Translation-invariant smooth tape has d2V/dx2=0 even if F equals release g.
    # Solid stop control can fix coordinate; it has a second support during release.
    return {'force_work_error_Nmm':errs,'finite_difference_and_contact_checks':'passed',
            'smooth_tape_curvature':0,'active_pair_remaining_dof':1,
            'control_support_sequence':['stop','stop+writer','writer','writer+stop','stop']}


if __name__=='__main__':
    u=Unit()
    print(json.dumps({'geometry':geometry(u),'mechanics':mechanics(u),
                      'bounds':uncertainty(),'board':board(u),'checks':checks(u)},indent=2))
