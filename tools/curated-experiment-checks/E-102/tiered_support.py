#!/usr/bin/env python3
"""E-102: finite routing screens and independent column-stability bound.
All mm, N, MPa; deterministic design/scenario bounds, not process priors.
No geometry acceptance is inferred from a selected set of clearance tests.
"""
from dataclasses import dataclass
from math import pi, sqrt, hypot, isclose
import json

P = 5.08
D = 3.0
R = D/2 + 2*.6 + 1.2 + .2 + 2.5  # captured groove E-101
STATION = 8*P
LOAD = 8*(.1+(1.5*pi/4+1)/2)  # eight loaded cells at an internal support
EXPANSION = .1  # each of two opposing objects, adversarial bound

@dataclass(frozen=True)
class Box:
    name: str
    lo: tuple
    hi: tuple

    def gaps(self, other):
        return tuple(max(c-b, a-d) for a,b,c,d in zip(self.lo,self.hi,other.lo,other.hi))

    def collision(self, other):
        return max(self.gaps(other)) < 0


def box(name, center, widths):
    return Box(name, tuple(c-w/2 for c,w in zip(center,widths)),
               tuple(c+w/2 for c,w in zip(center,widths)))


def shaft_box_gap(y, z, radius, body):
    """Exact separation of an x-directed infinite cylinder from an AABB.
    Cylinder is solid; a negative gap is penetration, zero is contact.
    """
    dy=max(body.lo[1]-y, y-body.hi[1], 0.)
    dz=max(body.lo[2]-z, z-body.hi[2], 0.)
    return hypot(dy,dz)-radius


def generated_line_array(colors):
    """Repeated lower-family fragment with alternating 10/18-mm shaft axes.
    Cam stations use two/four phases across the 8-cell support span. Bearings are 5.08
    mm either side of each disk. Housing is a finite square tube, represented
    by its outer AABB for foreign-object checks; its own shaft is excluded.
    Fork is two axial cheeks + bridge, pin passes through groove. A solid swept
    disk contains all cam material. Disk tests are sufficient clearance tests,
    not solid collision witnesses or contact validation.
    """
    disks=[]; bearings=[]; posts=[]; cheeks=[]; bridges=[]; shafts=[]
    for j in range(-4,5):
        y=j*P; z=10+8*(j%2)
        shafts.append((j,y,z))
        for k in range(-1,2):
            x=(.5+(8/colors)*(j%colors))*P+k*STATION
            disks.append((j,box('cam swept cylinder box',(x,y,z),(1.2,2*R,2*R))))
            # Housing d=3, diametral clearance=.2, wall=1: 5.2 side.
            for side in (-1,1):
                bx=x+side*P
                bearings.append((j,box('bearing outer',(bx,y,z),(1.2,5.2,5.2))))
                posts.append((j,box('bearing neck',(bx,y,(z-2.6)/2),(1.2,1.6,z-2.6))))
            # Prescribed rail/fork stroke -0.2..2.7 includes a chosen clearance
            # envelope. Actual groove-rise contact has NOT established that
            # bound; these are routing tests conditional on prescribed motion.
            low=D/2+.6+.7
            for side in (-1,1):
                cheeks.append((j,box('fork cheek swept',(x+side*1.1,y,(z+low-.8+32.7)/2),
                                    (.6,1.2,32.7-(z+low-.8)))))
            bridges.append((j,box('fork bridge swept',(x,y,30+2.5/2),(2.8,1.2,2.5+.4+.6))))
    # Cross-family upper bearing necks: x at column centers; y between rows.
    # y stations use the same phase rule; 1.6 x 1.2 necks reach z=55.4.
    upper=[]
    for i in range(-4,5):
        for k in range(-1,2):
            cy=(.5+(8/colors)*(i%colors))*P+k*STATION
            for side in (-1,1):
                upper.append(box('upper bearing ground neck',
                                 (i*P,cy+side*P,55.4/2),(1.6,1.2,55.4)))
    count=0; min_gap=float('inf')
    # Selected finite routing checks. All contacts excluded by construction
    # are named: own cam/pin, own shaft/bearing bore, fork/rail attachment.
    for owner,body in disks+bearings+posts+cheeks+bridges:
        for j,y,z in shafts:
            if j==owner: continue
            # For disks with displaced axial stations, neighboring shafts are
            # still continuous: use enclosing AABB here conservatively.
            gap=shaft_box_gap(y,z,D/2,body)
            # Disk AABBs overlap neighboring shafts despite cylinder clearance;
            # exact parallel-cylinder radial gap replaces that one loose box.
            if body.name.startswith('cam'):
                axis_z=(body.lo[2]+body.hi[2])/2
                axis_y=(body.lo[1]+body.hi[1])/2
                gap=hypot(y-axis_y,z-axis_z)-R-D/2
            assert gap > 2*EXPANSION, (body.name,owner,j,gap)
            min_gap=min(min_gap,gap); count+=1
        for post in upper:
            gap=max(body.gaps(post))  # sufficient axis separation
            assert gap > 2*EXPANSION, (body.name,body,post,gap)
            min_gap=min(min_gap,gap); count+=1
    # Disks from different tiers must have disjoint axial slabs; same tier
    # cams can share a slab, provided their bounding cylinders are disjoint.
    pair_count=0
    for n,(owner,a) in enumerate(disks):
        for other,b in disks[n+1:]:
            if owner==other: continue
            if a.hi[0]+2*EXPANSION < b.lo[0] or b.hi[0]+2*EXPANSION < a.lo[0]:
                pass
            else:
                dy=(a.lo[1]+a.hi[1]-b.lo[1]-b.hi[1])/2
                dz=(a.lo[2]+a.hi[2]-b.lo[2]-b.hi[2])/2
                # Same-tier stations of different lanes need additional axial
                # coloring if swept disks overlap. Report rather than hide it.
                gap=hypot(dy,dz)-2*R
                if gap <= 2*EXPANSION:
                    return dict(partial_pairs=count,partial_gap_mm=min_gap,
                                collision_family='same-tier cam disks',
                                axis_spacing_mm=hypot(dy,dz),swept_overlap_mm=-gap,
                                witness_lane_indices=[owner,other],
                                next_tested_axial_colors=4)
            pair_count+=1
    # Foreign moving parts and ground supports: conservative whole-stroke
    # boxes. Own-line pairs include intentional connections and are excluded.
    # Distinct support stations on the same line are separated by 40.64 mm.
    solids=disks+bearings+posts+cheeks+bridges
    foreign_tests=0
    for n,(owner,a) in enumerate(solids):
        for other,b in solids[n+1:]:
            if owner==other: continue
            gap=max(a.gaps(b))
            assert gap>2*EXPANSION, (a.name,b.name,owner,other,gap)
            min_gap=min(min_gap,gap); foreign_tests+=1
    return dict(axial_colors=colors,partial_pairs=count,partial_gap_mm=min_gap,
                disk_pairs=pair_count,foreign_box_pairs=foreign_tests,
                scope='one axis family plus upper ground-neck crossings; not complete selector')


def riser():
    """Exact cylinder/vertical rectangular riser collision and corridor move.
    Beam endpoints at +/-sqrt(2); upper shafts at sqrt(2)+i*pitch.
    Nearest shaft is at sqrt(2)-pitch. Riser spans the shaft axis in z/y.
    """
    nearest=P-2*sqrt(2)
    old_gap=nearest-D/2-.8
    centered_gap=P/2-D/2-.8
    assert old_gap < 0
    assert centered_gap-2*EXPANSION > 0
    return dict(straight_riser_shaft_gap_mm=old_gap,
                midpoint_reroute_mm=P/2-nearest,
                centered_gap_mm=centered_gap,
                centered_gap_after_two_point1_mm=centered_gap-2*EXPANSION,
                disclaimer='rerouted riser needs finite offset pad and anti-yaw/return geometry')


def support_stability():
    """Schedule-conditioned linear-elastic support bounds.
    One selected row: its cams carry 8 selected endpoints. A column cam
    carries 8 preloads + at most one valve endpoint (one row at a time).
    Equal sharing by two posts/cheeks and fixed ends are optimistic.
    No assumed boundary fixity is converted into manufacturing evidence.
    """
    sparse=8*.1+(1.5*pi/4+1)/2
    cases=[]
    for name, load, length, b, h in (
        ('upper column neck pair',sparse,55.4,1.6,1.2),
        ('lower row neck pair',LOAD,15.4,1.2,1.6),
        ('lower row fork cheek pair',LOAD,30-(10+D/2+.6+.7),1.2,.6),
    ):
        # Weak axis; orientation matters for location but not this free-column bound.
        I=min(b*h**3,h*b**3)/12
        for E in (500.,1500.,3000.):
            one_pin=pi*pi*E*I/length**2
            pair_fixed=8*one_pin
            # Rayleigh y=1-cos(2*pi*x/L), integrated energy ratio.
            rayleigh=2*(E*I*(2*pi/length)**4*length/2)/((2*pi/length)**2*length/2)
            assert isclose(rayleigh,pair_fixed,rel_tol=1e-12)
            axial=load*length/(2*E*b*h)
            shaft_sag=load*(2*P)**3/(48*E*(pi*D**4/64))
            cases.append(dict(component=name,E_MPa=E,load_N=load,
                unsupported_length_mm=length,weak_I_mm4=I,
                pair_pinned_N=2*one_pin,pair_fixed_N=pair_fixed,
                axial_shortening_mm=axial,local_shaft_sag_mm=shaft_sag,
                max_fixed_length_unit_load_ratio_mm=sqrt(8*pi*pi*E*I/load)))
    fork=[r for r in cases if r['component']=='lower row fork cheek pair']
    assert fork[0]['axial_shortening_mm']>.2
    assert fork[1]['pair_fixed_N']<LOAD
    assert isclose(fork[2]['pair_fixed_N']/fork[0]['pair_fixed_N'],6.)
    assert isclose(fork[0]['axial_shortening_mm']/fork[2]['axial_shortening_mm'],6.)
    return dict(dense_row_load_N=LOAD,sparse_column_load_N=sparse,scenarios=cases,
                scope='unbraced pair, preload maintained; no arbitrary simultaneous-row loading')


def main():
    assert isclose(R,6.6)
    # Independent limiting and deliberately bad geometry controls.
    assert shaft_box_gap(0,0,1,box('hit',(0,0,0),(1,1,1))) < 0
    assert not box('a',(0,0,0),(1,1,1)).collision(box('b',(2,0,0),(1,1,1)))
    # With two axial phases, same-tier disks collide as ACTUAL material:
    # at a common -90-degree shaft angle the left high outer dwell web
    # intersects the right low outer dwell web. Both phases are admissible
    # during concurrent column input changes. Interval lies on z=axis height.
    high_web=(R-.6,R)
    low_web=(2*P-(R-2.5),2*P-(R-2.5-.6))
    overlap=min(high_web[1],low_web[1])-max(high_web[0],low_web[0])
    assert isclose(overlap,.54)
    result=dict(two_phase_route=generated_line_array(2),
                two_phase_exact_web_overlap_mm=overlap,
                four_phase_route=generated_line_array(4),
                riser=riser(),support=support_stability(),
                shaft_pair_gap_mm=hypot(P,8)-R-D/2,
                same_tier_cam_shaft_gap_mm=2*P-R-D/2,
                evidence='finite envelopes + exact witness + elastic bounds; self-review only')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
