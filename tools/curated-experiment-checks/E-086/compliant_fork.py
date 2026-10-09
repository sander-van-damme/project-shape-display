"""Finite stopped-fork screen. mm, N, s; every input is a labelled bound.

No empirical priors, yield, dynamic contact solution or hardware claims.
Run with Python's standard library; optional --svg exports nominal solids.
"""
import argparse
import itertools as it
import json
import math
from dataclasses import dataclass
from pathlib import Path

P = 5.08
D = 1.2
W = .8


@dataclass(frozen=True)
class Box:
    x0: float
    x1: float
    y0: float
    y1: float
    z0: float
    z1: float

    def moved(self, x=0., y=0., z=0.):
        return Box(self.x0+x, self.x1+x, self.y0+y, self.y1+y,
                   self.z0+z, self.z1+z)


def overlap(a, b):
    return (max(0., min(a.x1,b.x1)-max(a.x0,b.x0)) *
            max(0., min(a.y1,b.y1)-max(a.y0,b.y0)) *
            max(0., min(a.z1,b.z1)-max(a.z0,b.z0)))


def boss(x, y=0., width=W):
    return Box(x-width/2, x+width/2, y-.3, y+.3, 0., 1.)


@dataclass(frozen=True)
class Fork:
    gap: float = 2.6
    wall: float = .6
    depth: float = 1.2

    @property
    def contact(self):
        return D/2 + (self.gap-W)/2

    def solids(self, q=0., row=0., lift=0.):
        left, right = D/2-self.gap/2, D/2+self.gap/2
        return [b.moved(x=q, y=row, z=lift) for b in (
            Box(left-self.wall,left,-self.depth/2,self.depth/2,.2,2.4),
            Box(right,right+self.wall,-self.depth/2,self.depth/2,.2,2.4),
            Box(left-self.wall,right+self.wall,-self.depth/2,self.depth/2,2.4,3.2))]


def path(f, old, command, n=80):
    """Unilateral quasi-static contact with endpoint retention on unloading.
    Fork q is actual output position, not the flexure drive coordinate.
    Hard stops are 0,D. Spring deflection supplies further commanded overrun.
    """
    x = old*D
    sign = {'set':1, 'reset':-1, 'bypass':0}[command]
    poses = []
    # Rest above, lower at neutral, drive to contact, unload at neutral, raise.
    for stage in range(5):
        for i in range(n+1):
            u=i/n
            q = sign*f.contact*(u if stage==1 else 1-u if stage==2 else 0)
            z = 1.2*(1-u) if stage==0 else 1.2*u if stage==3 else 1.2 if stage==4 else 0.
            if stage in (1,2):
                left=D/2-f.gap/2+q
                right=D/2+f.gap/2+q
                x=max(x,left+W/2) if sign>0 and stage==1 else x
                x=min(x,right-W/2) if sign<0 and stage==1 else x
            assert -.000001 <= x <= D+.000001
            solids=f.solids(q,lift=z)
            assert max(overlap(a,boss(x)) for a in solids)<1e-9
            for col,row,state in it.product((-1,0,1),(-1,0,1),(0,1)):
                if not col and not row:
                    continue
                assert max(overlap(a,boss(col*P+state*D,row*P)) for a in solids)<1e-9
            poses.append((q,z,x))
    expected=old*D if not sign else D if sign>0 else 0.
    assert math.isclose(x,expected,abs_tol=1e-9)
    return poses


def finite_checks():
    f=Fork()
    paths={(old,cmd):path(f,old,cmd) for old,cmd in it.product((0,1),('set','reset','bypass'))}
    # Opposite commands at adjacent columns: even endpoint solids collide.
    a=f.solids(f.contact)
    b=[v.moved(x=P) for v in f.solids(-f.contact)]
    witness=max(overlap(x,y) for x,y in it.product(a,b))
    assert witness>0
    # Adjacent columns moved one row apart; same-lane spacing becomes 2P.
    max_stagger_overlap=0.
    for q,r in it.product((-f.contact,0.,f.contact),repeat=2):
        for col,row in ((1,1),(2,0)):
            for x,y in it.product(f.solids(q),f.solids(r,row*P)):
                max_stagger_overlap=max(max_stagger_overlap,overlap(x,y.moved(x=col*P)))
    assert max_stagger_overlap==0.
    # Replay 2x2 maps through two staggered column stations; flush extra stop.
    maps=list(it.product((0,1),repeat=4))
    for old,target in it.product(maps,repeat=2):
        state=list(old)
        for stop in range(3):
            for col in range(2):
                row=stop-col
                if not 0<=row<2:
                    continue
                k=2*row+col
                cmd='bypass' if old[k]==target[k] else 'set' if target[k] else 'reset'
                state[k]=round(paths[old[k],cmd][-1][2]/D)
        assert tuple(state)==target
    # Stuck-low transport intersects next dog, including neutral bypass fork's
    # cross-row entry: the bridge is clear, but legs can strike shifted bosses
    # if the fork also failed to unload. Commanded common lift is not proof.
    stuck=max(overlap(a,boss(0)) for a in f.solids(f.contact))
    assert stuck>0
    return dict(nominal_paths=6,maps=256,single_station_collision_mm3=witness,
                staggered_endpoint_overlap_mm3=max_stagger_overlap,
                stuck_extended_fork_collision_mm3=stuck)


def bank_boundary_checks():
    f=Fork()
    # Last staggered stop in bank A coincides with first stop in parked bank B.
    # Nominal 1.2-mm withdrawal clears DOGS, not another complete fork.
    active=f.solids(0.)
    parked=f.solids(0.,lift=1.2)
    collision=max(overlap(a,b) for a,b in it.product(active,parked))
    assert collision>0
    # Fork-only extra park height. Flexures/top drives extend beyond this;
    # the result is NOT a whole-head parking solution.
    clears=max(overlap(a,b) for a,b in it.product(active,f.solids(0.,lift=3.2)))
    assert clears==0
    # At synchronous full scan, banks with >=2 rows are separated in y.
    # Check both 40-column parity stations and all ternary endpoints.
    synchronous={}
    for n in (1,2,4,5,10,20,80):
        worst=0.
        for pa,pb,qa,qb in it.product((0,1),(0,1),(-f.contact,0.,f.contact),(-f.contact,0.,f.contact)):
            a=f.solids(qa,row=-pa*P)
            b=[v.moved(x=(pb-pa)*P) for v in f.solids(qb,row=(n-pb)*P)]
            worst=max(worst,max(overlap(x,y) for x,y in it.product(a,b)))
        synchronous[n]=worst
    assert synchronous[1]>0 and all(v==0 for n,v in synchronous.items() if n>=2)
    return dict(local_active_parked_collision_mm3=collision,
                fork_only_3p2mm_park_collision_mm3=clears,
                synchronous_rows_per_bank_overlap_mm3=synchronous)


def bounds(f,e):
    """Exact interval corners, including separately uncertain jaw faces.
    b=head offset; t=dog-stop offset; dw=full boss-width error;
    j=inner jaw-face error; outer wall thickness error independent +/-e.
    A mechanical fork stop has additional +/-e uncertainty.
    All can be coherent by batch/rail; no statistical averaging.
    """
    corners=list(it.product((-e,e),repeat=4))
    insert=[]
    demands=[]
    for b,t,dw,j in corners:
        for old in (0,D):
            x=old+t
            insert.extend((x-(W+dw)/2-(D/2-f.gap/2+b+j),
                           D/2+f.gap/2+b+j-x-(W+dw)/2))
        demands.append(D+t-(W+dw)/2-(D/2-f.gap/2+b+j))
    mismatch=3.5*e
    assert math.isclose(min(demands),f.contact-mismatch,abs_tol=1e-10)
    assert math.isclose(max(demands),f.contact+mismatch,abs_tol=1e-10)
    # Stop nominal must still allow furthest endpoint when its own error is -e.
    stop=f.contact+mismatch+e
    # Finite missing-dog / failed-retention case at largest positive fork stop.
    # This is an actual wall box against the nearest adjacent zero-state boss.
    right=D/2+e+stop+e+f.gap/2+e
    wall=Box(right,right+f.wall+e,-.6,.6,.2,2.4)
    neighbor=boss(P-e,width=W+e)
    neighbor_gap=neighbor.x0-wall.x1
    witness=overlap(wall,neighbor)
    # Whole swept x envelope; staggered same-lane distance is 2P.
    half=f.gap/2+e+f.wall+e+stop+e+e
    same_lane_gap=2*P-2*half
    # All z positions are safe during insertion if the 2-D neutral gap passes.
    # Two opposite z offsets leave .2 mm less raised clearance at e=.1.
    raised_clearance=.4-2*e
    # y: fork depth/boss depth plus opposite phase errors.
    axial_gap=P-(f.depth+.6)/2-2*e
    assert (witness>1e-10)==(neighbor_gap<0)
    return dict(gap_mm=f.gap,wall_mm=f.wall,error_mm=e,
                insertion_mm=min(insert),mismatch_mm=mismatch,stop_mm=stop,
                neighbor_mm=neighbor_gap,neighbor_collision_mm3=witness,
                staggered_fork_mm=same_lane_gap,raised_mm=raised_clearance,
                row_mm=axial_gap,
                geometric_reserve=min(min(insert),neighbor_gap,same_lane_gap,raised_clearance,axial_gap)>0)


@dataclass(frozen=True)
class Spring:
    length: float=16.8
    thickness: float=1.
    width: float=.6

    def coefficients(self,E):
        # Two clamped-guided beams, shape phi=3u²-2u³, I=b*t³/12.
        # If guide fixes z, arc extension DeltaL≈3 delta²/(5L) adds cubic force.
        k=2*E*self.width*self.thickness**3/self.length**3
        cubic=36*E*self.width*self.thickness/(25*self.length**3)
        return k,cubic

    def force(self,d,E,axial=True):
        k,c=self.coefficients(E)
        return k*d+(c*d**3 if axial else 0.)

    def energy(self,d,E,axial=True):
        k,c=self.coefficients(E)
        return k*d*d/2+(c*d**4/4 if axial else 0.)  # N mm

    def stress(self,d,E,axial=True):
        return E*(3*self.thickness*d/self.length**2+
                  (.6*d*d/self.length**2 if axial else 0.))

    def deflection(self,F,E,axial=True):
        lo,hi=0.,1.
        while self.force(hi,E,axial)<F:
            hi*=2
        for _ in range(70):
            mid=(lo+hi)/2
            if self.force(mid,E,axial)<F: lo=mid
            else: hi=mid
        return (lo+hi)/2


def spring_screen(s,e,F=.3,Elo=1000.,Ehi=3000.,cap=1.,stress_cap=20.):
    # Robust to two competing guide models: axial relief vs fixed separation.
    # Design stroke using softer model; reject by stiffer model. No probability.
    mismatch=3.5*e
    necessary=s.deflection(F,Elo,False)
    overrun=mismatch+necessary
    max_deflection=overrun+mismatch
    peak=s.force(max_deflection,Ehi,True)
    stress=s.stress(max_deflection,Ehi,True)
    drive=Fork().contact+overrun
    # Drive crossbar/flexure is above dog, but must fit same-lane pitch 2P.
    crossbar_half=Fork().gap/2+Fork().wall+2*e
    drive_gap=2*P-2*(crossbar_half+drive+e)
    domain=max_deflection/s.length <= .1  # declared reduced-model use limit
    return dict(length_mm=s.length,thickness_mm=s.thickness,error_mm=e,
                required_N=F,E_range_MPa=[Elo,Ehi],overrun_mm=overrun,
                drive_mm=drive,max_deflection_mm=max_deflection,
                peak_N=peak,stress_MPa=stress,drive_lane_gap_mm=drive_gap,
                force_pass=peak<cap,stress_pass=stress<stress_cap,
                package_pass=drive_gap>0,
                in_model_domain=domain,
                survives=domain and peak<cap and stress<stress_cap and drive_gap>0)


def verification():
    s=Spring()
    # Independent quadrature of shape derivatives reconstructs linear beam
    # energy and axial elongation. Refinement should reduce integration error.
    errors=[]
    for n in (20,40,80,160):
        h=1/n
        integral=lambda fn: h*sum((.5 if i in (0,n) else 1)*fn(i*h) for i in range(n+1))
        curvature=integral(lambda u:(6-12*u)**2)
        slope=integral(lambda u:(6*u-6*u*u)**2)
        assert abs(slope-1.2)<1e-4
        errors.append(abs(curvature-12))
    assert all(math.isclose(a/b,4.,rel_tol=1e-8) for a,b in zip(errors,errors[1:]))
    for d,E in it.product((0.,.1,.5,1.),(1000.,2000.,3000.)):
        eps=1e-5
        derivative=(s.energy(d+eps,E)-s.energy(d-eps,E))/(2*eps)
        assert math.isclose(derivative,s.force(d,E),rel_tol=1e-8,abs_tol=1e-8)
        assert math.isclose(s.deflection(s.force(d,E),E),d,abs_tol=1e-10)
    return dict(curvature_integral_errors=errors,energy_derivative=True)


def capture():
    # Conditional example: known E, fixed-z cubic spring, .1N dog resistance.
    # Fixed drive base during arrest, no further input work. Energy capacity
    # is not a solution for the continuing-drive trajectory or its settling.
    s=Spring(); E=2000.; F=.1; cap=1.; mass=.005
    equilibrium=s.deflection(F,E)
    limit=s.deflection(cap,E)
    spare=(s.energy(limit,E)-s.energy(equilibrium,E)-F*(limit-equilibrium))/1000
    vmax=math.sqrt(2*spare/mass)
    lo,hi=0.,limit
    for _ in range(70):
        mid=(lo+hi)/2
        if s.stress(mid,E)<20.: lo=mid
        else: hi=mid
    stress_limit=(lo+hi)/2
    stress_spare=(s.energy(stress_limit,E)-s.energy(equilibrium,E)-F*(stress_limit-equilibrium))/1000
    return dict(E_MPa=E,load_N=F,cap_N=cap,mass_kg=mass,
                preload_mm=equilibrium,limit_mm=limit,energy_J=spare,
                necessary_capture_limit_m_s=vmax,
                stress_at_limit_MPa=s.stress(limit,E),
                stress_limited_capture_m_s=math.sqrt(2*stress_spare/mass),
                stress_limited_deflection_mm=stress_limit,
                axial_force_ratio_at_1mm=s.force(1,E)/s.force(1,E,False))


def recoil():
    # At neutral drive, residual fork oscillation can hit the opposite jaw.
    # This budget does not assert that terminal energy survives unloading;
    # an actual damping/trajectory model must show how much remains.
    f=Fork();s=Spring();e=.05
    gap=bounds(f,e)['insertion_mm']
    maximum=spring_screen(s,e,F=.1)['max_deflection_mm']
    fraction=s.energy(gap,2000.)/s.energy(maximum,2000.)
    # Nominal right jaw starts pulling a set dog back once q < -0.3 mm.
    collision=max(overlap(a,boss(D)) for a in f.solids(-.4))
    assert collision>0
    return dict(adverse_neutral_gap_mm=gap,
                maximum_residual_energy_fraction=fraction,
                nominal_reverse_recoil_collision_mm3=collision)


def move(d,a):
    return 2*math.sqrt(d/1000/a) if d else 0.


def timing(banks,drive=2.5,a=20.,proof=.002):
    """Conditional lower-detail complete itinerary, not force-qualified time.
    Two parity stations separated by P: n+1 stopped writes/mask.
    Bidirectional fork writing permits serpentine sweeps; no empty return.
    Shared z axes lower then raise; x moves out and back. No overlap credited.
    All legs start/end at rest. Per-map other allowance remains assumed 6s.
    """
    n=80//banks
    transaction=2*move(1.2,a)+2*move(drive,a)+proof
    masks=43
    stops=masks*(n+1)
    # n row-pitch moves per mask; serpentine ends are already staging points.
    indexes=masks*n
    total=stops*transaction+indexes*move(P,a)+6
    channels=80*banks+2*banks  # per-column x plus shared z and index per bank
    # Moving comparator: continuous open forks drag dogs sideways only when
    # energized; insertion requires stationary registration, so no flying credit.
    return dict(banks=banks,acceleration_m_s2=a,drive_mm=drive,
                row_transaction_ms=transaction*1000,stops=stops,indexes=indexes,
                full_seconds=total,channels=channels,
                allowance_USD=250/channels,
                ideal_patch_35_transactions_seconds=35*(transaction+move(P,a))+6,
                retry_one_mask_seconds=(n+1)*transaction+n*move(P,a))


def svg(path):
    f=Fork(); items=[]
    for q,color in ((0,'#888'),(f.contact,'#168'),(-f.contact,'#c73')):
        for b in f.solids(q):
            items.append(f'<rect x="{b.x0*50}" y="{-b.z1*50}" width="{(b.x1-b.x0)*50}" height="{(b.z1-b.z0)*50}" fill="{color}" fill-opacity=".35" stroke="{color}"/>')
    for x in (0,D,P,P+D):
        b=boss(x)
        items.append(f'<rect x="{b.x0*50}" y="{-50}" width="40" height="50" fill="none" stroke="black"/>')
    Path(path).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-170 -180 550 210">'+''.join(items)+'</svg>')


def main():
    p=argparse.ArgumentParser();p.add_argument('--svg');args=p.parse_args()
    if args.svg: svg(args.svg)
    geometry=[bounds(Fork(g,w),e) for g,w,e in it.product((2.4,2.6,2.8),(.6,.8),(0.,.05,.1,.2))]
    springs=[spring_screen(Spring(L,t),e,F) for L,t,e,F in it.product((12.,16.8,24.),(.8,1.),(.05,.1),(.1,.3))]
    print(json.dumps(dict(checks=finite_checks(),bank_boundaries=bank_boundary_checks(),verification=verification(),
                          geometry=geometry,springs=springs,capture=capture(),recoil=recoil(),
                          timing=[timing(b,a=a) for b,a in it.product((1,4,8,16,20,40,80),(20.,100.))]),indent=2))


if __name__=='__main__':
    main()
