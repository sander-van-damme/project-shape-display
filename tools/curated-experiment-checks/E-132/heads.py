"""E-132 finite discriminator. Geometry mm; dynamics SI. Standard library only.
Deterministic engineering bounds, not manufacturing priors or hardware validation.
Run from any directory; printed JSON is disposable. No motor braking is credited.
"""
import itertools
import json
import math


def screw_constants(mu, diameter=.012, lead=.0005):
    r, k = diameter/2, lead/(2*math.pi)
    slope = k/r
    return k, r*(mu+slope)/(1-mu*slope), r*(mu-slope)/(1+mu*slope)


def acceleration(w, mass, inertia, mu, direction, torque=0):
    """Positive speed/acceleration in chosen travel direction; torque drives it.
    Thread axial reaction F=W+m*a (up), W-m*a (down); not frozen at W.
    Contact remains on the load-bearing flank only if F>0.
    """
    k, up, down = screw_constants(mu)
    c = up if direction == 1 else down
    denom = inertia + direction*mass*k*c
    assert denom > 0, 'outside the single-flank reduced model'
    a = k*(torque-w*c)/denom
    axial = w + direction*mass*a
    assert axial > 0, 'flank loss: no continuation allowed'
    # Independent force, rotor balance and power balance.
    assert abs(inertia*a/k-(torque-c*axial)) < 1e-10
    friction_per_radian = axial*(c-direction*k)
    assert friction_per_radian >= -1e-12
    # Per unit linear speed: input - gravity - friction = d(KE)/dt / v.
    lhs = torque/k-direction*w-friction_per_radian/k
    assert abs(lhs-(mass+inertia/k**2)*a) < 1e-8
    return a


def numeric_coast(a, speed, intervals):
    """Explicit-Euler position, exact zero-velocity event; convergence holdout."""
    assert a < 0
    dt = (-speed/a)/intervals
    x, v = 0., speed
    for _ in range(intervals):
        step = min(dt, v/-a)
        x += v*step
        v = max(0., v+a*step)
    return x


def box(x0, x1, y0, y1, z0, z1):
    assert x1 > x0 and y1 > y0 and z1 > z0
    return (x0,x1,y0,y1,z0,z1)


def shifted(b, dx=0, dy=0, dz=0):
    return tuple(v+(dx,dy,dz)[i//2] for i,v in enumerate(b))


def overlap(a,b):
    return math.prod(max(0, min(a[2*i+1],b[2*i+1])-max(a[2*i],b[2*i])) for i in range(3))


def swept(b, axis, displacement):
    b=list(b)
    b[2*axis]+=min(0,displacement)
    b[2*axis+1]+=max(0,displacement)
    return tuple(b)


def transform(b, site):
    if site == 0:
        return b
    # Mirror complete route in x and y; tops at (0,0), (5.08,0).
    return (5.08-b[1],5.08-b[0],-b[3],-b[2],b[4],b[5])


def output(h):
    """Solid prisms: slotted stem, elbow, square eye and top. Holes along x."""
    holes=sorted([(-30.25-5*i-.75,-30.25-5*i+.75) for i in range(9)])
    parts={'top':box(-2.3,2.3,-2.3,2.3,0,2),
           'stem_side_a':box(-1.2,1.2,-1.2,-.75,-76,0),
           'stem_side_b':box(-1.2,1.2,.75,1.2,-76,0),
           'elbow':box(-1.2,1.2,-8,0,-72.5,-71.5)}
    last=-76
    for n,(lo,hi) in enumerate(holes):
        parts['stem_'+str(n)]=box(-1.2,1.2,-.75,.75,last,lo)
        last=hi
    parts['stem_end']=box(-1.2,1.2,-.75,.75,last,0)
    # Four real walls, rather than treating the eye as a solid bounding box.
    parts.update(eye_left=box(-1.2,1.2,-9.5,-8.75,-75.5,-72.5),
                 eye_right=box(-1.2,1.2,-7.25,-6.5,-75.5,-72.5),
                 eye_bottom=box(-1.2,1.2,-8.75,-7.25,-75.5,-74.75),
                 eye_top=box(-1.2,1.2,-8.75,-7.25,-73.25,-72.5))
    return {n:shifted(b,dz=h) for n,b in parts.items()}


def head(h, takeup=0, retract=0):
    """Bilateral pin and connected arm. Screw/nut are routing envelopes only.
    Capture translates the whole writer in x by 4 mm; x arrest is UNBUILT.
    Nut reaction/antirotation guides and thrust bearings need detailed contacts.
    """
    z=h+takeup
    p={'pin':box(-2,2,-8.5,-7.5,-74.5+z,-73.5+z),
       'pin_root':box(-4,-2,-9,-7,-74.5+z,-71+z),
       'arm':box(-10,-3,-9,-7,-72+z,-71+z),
       'nut_envelope':box(-18,-2,-16,0,-77+z,-71+z),
       'screw_envelope':box(-16.125,-3.875,-14.125,-1.875,-82,-12)}
    return {n:shifted(b,dx=-retract) for n,b in p.items()}


def geometry():
    # Full independent 40-mm sweeps are exact unions for axis-translating boxes.
    # The .5-mm head allowance includes capture play and ground-stop unload.
    parts={**{'output_'+n:swept(b,2,40.25) for n,b in output(0).items()},
           **{'head_'+n:swept(swept(b,2,40.5),0,-4) for n,b in head(0).items()}}
    cross=max(overlap(a,transform(b,1)) for a in parts.values() for b in parts.values())
    assert cross == 0
    clearances=[]
    for intervals in (16,64,256):
        collision=0
        for j in range(intervals+1):
            # Centered pin insertion followed by vertical take-up to actual ceiling.
            retract=4*(1-j/intervals)
            collision=max(collision,max(overlap(head(0,retract=retract)['pin'],b) for b in output(0).values()))
            q=.25*j/intervals
            collision=max(collision,max(overlap(head(0,takeup=q)['pin'],b) for b in output(0).values()))
        assert collision == 0
        assert head(0,takeup=.25)['pin'][5] == output(0)['eye_top'][4]
        clearances.append(collision)
    # Exact continuous x insertion and z take-up sweep, not only samples.
    assert max(overlap(swept(head(0,retract=4)['pin'],0,4),b) for b in output(0).values()) == 0
    assert max(overlap(swept(head(0)['pin'],2,.25),b) for b in output(0).values()) == 0
    # Ground pin bears on a distinct slotted stem while head pin is inserted.
    ground=box(-2,2,-.5,.5,-30.5,-29.5)
    for h in range(0,41,5):
        assert max(overlap(ground,b) for b in output(h).values()) == 0
        assert max(overlap(ground,b) for b in output(h+.25).values()) == 0
        # After head lifts .25 mm, full withdrawal also clears the selected output.
        assert max(overlap(swept(ground,0,-4),b) for b in output(h+.25).values()) == 0
    # Alternative drive geometry: a 90-mm rail joined to the same carriage arm.
    # Opposed 4x10-mm pads contact y faces continuously over the 40-mm stroke.
    rail=box(-12,-8,-10,-6,-89,1)
    pad_a=box(-12,-8,-11,-10,-47,-37)
    pad_b=box(-12,-8,-6,-5,-47,-37)
    spring_a=box(-11,-9,-15,-11,-43,-41)
    spring_b=box(-11,-9,-5,-1,-43,-41)
    back_a=box(-13,-7,-16,-15,-48,-36)
    back_b=box(-13,-7,-1,0,-48,-36)
    pad_parts={n:b for n,b in parts.items() if 'envelope' not in n}
    pad_parts.update(rail=swept(rail,2,40.5),pad_a=pad_a,pad_b=pad_b,
                     spring_a=spring_a,spring_b=spring_b,back_a=back_a,back_b=back_b)
    for n in ('rail','pad_a','pad_b','spring_a','spring_b','back_a','back_b'):
        pad_parts[n]=swept(pad_parts[n],0,-4)
    pad_cross=max(overlap(a,transform(b,1)) for a in pad_parts.values() for b in pad_parts.values())
    assert pad_cross == 0
    for h in (0,40.5):
        moving=shifted(rail,dz=h)
        assert moving[4] < -47 and moving[5] > -37
        assert overlap(moving,pad_a) == overlap(moving,pad_b) == 0
    # Connected carriage stays between the opposing pads, without releasing them.
    for n in ('arm','pin_root','pin'):
        assert max(overlap(swept(head(0)[n],2,40.5),b) for b in (pad_a,pad_b,spring_a,spring_b,back_a,back_b)) == 0
    # Pair separation is not full-board routing. A third unchanged row is a witness.
    arm=output(20)['elbow']
    neighbor={n:shifted(b,dy=-5.08) for n,b in output(0).items()}
    witness=max((overlap(arm,b),n) for n,b in neighbor.items())
    total=sum(overlap(arm,b) for n,b in neighbor.items() if n.startswith('stem'))
    assert total > 0
    # Correlated/adverse uncertainty box: pin growth, hole shrink and registration
    # each e gives centered-insertion per-side margin .25-3e. No fitted priors.
    fits={str(e):.25-3*e for e in (.025,.05,.1)}
    # Explicit e=.1: enlarged/misaligned pin intersects shrunken upper wall.
    e=.1
    pin=box(-2,2,-8.5-e,-7.5+e,-74.5-e+e,-73.5+e+e)
    upper=box(-1.2,1.2,-8.75,-7.25,-73.25-e,-72.5)
    fit_witness=overlap(pin,upper)
    assert fit_witness > 0
    return dict(two_site_swept_intersection_mm3=cross,pad_two_site_intersection_mm3=pad_cross,refinement_collisions_mm3=clearances,
                centered_pin_margin_mm=fits,adverse_pin_intersection_mm3=fit_witness,
                next_row_largest_body_intersection_mm3=witness,
                next_row_total_stem_intersection_mm3=total,
                top_gap_mm=5.08-4.6)


def run():
    # Constructed solid core, 70 mm long, r=5.875 mm; density is a bounded
    # engineering scenario, not measured filament density. Excludes thread/rotor.
    core=lambda density: density*math.pi*.005875**4*.070/2
    j=core(1000)
    loaded_nut=head(20,takeup=.25)['nut_envelope']
    screw_bottom=head(20)['screw_envelope'][4]
    full_coverage=loaded_nut[4]-screw_bottom
    disengagement=loaded_nut[5]-screw_bottom
    assert abs(full_coverage-25.25) < 1e-12
    assert abs(disengagement-31.25) < 1e-12
    k,up,down=screw_constants(.02)
    records=[]
    for w,m,rho,jmotor,mu,v,direction in itertools.product(
            (1.,10.),(.05,.5),(1000.,1300.),(0.,1e-7,1e-6),(.02,.05,.1,.3),(.05,.1,.3),(-1,1)):
        if m*9.81 > w:  # no unmentioned upward force to cancel translator weight
            continue
        a=acceleration(w,m,core(rho)+jmotor,mu,direction)
        distance=v*v/(-2*a)
        records.append(distance)
    # Frictionless conservation, independent of the self-locking specialization.
    for direction in (-1,1):
        a=acceleration(1,.05,j,0,direction)
        assert abs(a+direction/(.05+j/k**2)) < 1e-12
    assert screw_constants(k/.006)[2] == 0
    a=acceleration(1,.05,j,.02,-1)
    exact=.1**2/(-2*a)
    numeric=[numeric_coast(a,.1,n) for n in (64,256,1024)]
    errors=[abs(x-exact) for x in numeric]
    assert errors[0]/errors[1] > 3.99 and errors[1]/errors[2] > 3.99
    # Energy dissipated equals initial rotor+translator KE plus gravitational work.
    # The dynamic thread load from a (not W) is essential to this identity.
    axial=1-.05*a
    dissipation=axial*(down+k)*exact/k
    initial_energy=.5*(.05+j/k**2)*.1**2
    assert abs(dissipation-(initial_energy+exact)) < 1e-10
    # Best possible coast-only downward schedule: speed <= sqrt(2*a_remaining*height).
    # Infinite powered acceleration and zero restart cost make this optimistic.
    best_lower_time=math.sqrt(2*.04/-a)
    min_channels=next(n for n in range(1,6401) if math.ceil(6400/n)*(best_lower_time+.05)+6 < 30)
    # Kinetic pad loss, through net load in either direction. Includes reflected mass.
    pads=[]
    for w,c,preload,mu,meff,direction in itertools.product(
            (1.,10.),(4.4,5.5,6.6),(80.,100.,120.),(.02,.05,.1,.3),(.05,.5,5.),(-1,1)):
        drag=2*preload*mu
        residual=w-c
        a_pad=(-direction*residual-drag)/meff
        pads.append(a_pad)
    pad_loss=(10-4.4-2*80*.02)/.5
    # Low-load opposite fault: upward acceleration at excessive spring force.
    pad_up=(6.6-1-2*80*.02)/.5
    assert abs(pad_loss-4.8)<1e-12 and abs(pad_up-4.8)<1e-12
    # At favorable mu, reflected inertia changes distance, never rescues negative drag margin.
    pad_stops={str(m):1000*m*.1**2/(2*(8-5.6)) for m in (.05,.5,5.)}
    # Same-cost allocations as E-131, explicitly not a BOM or completed schedule.
    costs={str(n):{'400_ceiling':150/n,'500_ceiling':250/n} for n in (160,min_channels)}
    torque=screw_constants(.3)[1]*10
    print(json.dumps(dict(
        geometry=geometry(),
        screw=dict(cases=len(records),core_inertia_kg_m2=j,reflected_mass_kg=j/k**2,
                   slope=k/.006,static_margin_mu_005=.05-k/.006,
                   loss_deceleration_m_s2=-a,stop_from_100mm_s_mm=exact*1000,
                   full_thread_coverage_loss_mm=full_coverage,
                   thread_disengagement_mm=disengagement,
                   down_stop_table_mm={str(mu):[1000*.1**2/(-2*acceleration(w,.05,j,mu,-1)) for w in (1,10)] for mu in (.02,.05,.1,.3)},
                   numeric_stop_mm=[1000*x for x in numeric],
                   range_stop_mm=[1000*min(records),1000*max(records)],
                   rpm_at_100mm_s=60*.1/.0005,
                   generous_40mm_stop_speed_mm_s=1000*math.sqrt(-2*a*.04),
                   best_loss_safe_lower_time_s=best_lower_time,
                   minimum_channels_optimistic=min_channels,
                   torque_at_W10_mu03_Nm=torque,
                   steady_raise_heat_W=(torque/k-10)*.1,
                   acceleration_torque_at_3m_s2_Nm=j*3/k),
        pads=dict(cases=len(pads),low_mu_accel_down_m_s2=pad_loss,
                  low_mu_accel_up_m_s2=pad_up,positive_mu_stop_mm=pad_stops,
                  min_nominal_preload_per_pad_N=5.6/(2*.02*.8),
                  static_margin_low_mu_N=8-5.6,
                  heat_W_at_mu03_preload120_v01=2*.3*120*.1,
                  peak_drive_bound_N=2*.3*120+5.6),
        per_head_bought_allocations_USD=costs),indent=2))


if __name__ == '__main__':
    run()
