#!/usr/bin/env python3
"""E-109 bounded dual-poppet rejection. mm, N, MPa, seconds, USD.
Finite axisymmetric solids, prescribed contact motion; NOT a dynamics/seal model.
No random distributions; corners are explicit uncalibrated manufacturing bounds.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

spec = importlib.util.spec_from_file_location('e108', Path(__file__).parents[1]/'E-108/bank_docking.py')
e108 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = e108
spec.loader.exec_module(e108)

# Actual catalog spring, nominal rate from N/cm (page rounds N/mm to .06).
FREE, SOLID, RATE = 5.8, 1.15, .059
INSTALLED = 2.4
PORT, STEM, PITCH = 1.4, .8, 5.08

def area(d): return math.pi*d*d/4

def pressure_closing(pc, ps, port=PORT, stem=STEM):
    # Two wetted sides of disk cancel except projected seat and dry stem.
    return pc*area(port)-ps*(area(port)-area(stem))

def lift(s, branch): return max(0., s-(0. if branch=='fine' else .6))

def solids(h):
    # (name, inner radius, outer radius, low z, high z), common axis.
    # Disk-seat/head-tail contacts are allowed at zero overlap only.
    return [('shell',.95,1.15,-1.8,1.6),
            ('seat',.7,.95,-.4,0.), ('gland',.5,.95,-1.8,-1.3),
            ('cap',0.,.95,1.5,1.6),
            ('disk',0.,.9,h,h+.3), ('stem',0.,.4,-6.+h,h),
            ('collar',.4,.8,-4.4+h,-4.2+h),
            ('spring_envelope',.55,.65,-4.2+h,-1.8),
            ('tip',0.,.6,-6.3+h,-6.+h)]

def overlaps(a,b):
    return min(a[2],b[2])-max(a[1],b[1])>1e-9 and min(a[4],b[4])-max(a[3],b[3])>1e-9

def geometric_checks(n):
    # Spring is an occupied annular envelope, not an invented solid coil.
    # Coil bind is separately checked against the manufacturer's finite height.
    minimum=math.inf
    for i in range(n+1):
        s=i/n
        for branch in ('fine','bypass'):
            h=lift(s,branch); parts=solids(h)
            for a,b in itertools.combinations(parts,2):
                assert not overlaps(a,b), (s,branch,a,b)
            minimum=min(minimum,INSTALLED-h-SOLID)
    # Parallel axes at +-1.2: disjoint outer cylinders, including asynchronous motion.
    assert 2.4>2*1.15 and PITCH-2.4>2*1.15
    # Fully withdrawn tip clears all closed tails while indexing.
    assert -6.-1.<-6.
    return minimum

def return_bounds(port=PORT,stem=STEM,rate=RATE,free=FREE,solid=SOLID,drag=.03):
    # Worst unselected pressure history from E-105's declared 0...0.5 MPa box.
    opening=-pressure_closing(0.,.5,port,stem)
    preload=rate*(free-INSTALLED)
    # Even a hypothetically adjustable collar cannot consume the working stroke.
    max_preload=rate*(free-solid-1.)
    required_length=free-(opening+drag)/rate
    return dict(opening=opening,preload=preload,max_preload_with_stroke=max_preload,
                seated_margin=preload-opening-drag,
                demanded_closed_length=required_length,
                coil_bind_overlap=solid-required_length,
                critical_supply_at_chamber_08=(preload+.08*area(port))/(area(port)-area(stem)))

def connected_fluid_volume(h):
    # Exact slice union in plenum+chamber above gland. Disk stays fully wetted;
    # its translation cannot change total occupied volume. Side-port volume
    # and fixed shell cancel between states. Integrate all radial intervals.
    parts=[v for v in solids(h) if v[0] in ('seat','disk','stem')]
    zs=sorted(set([-1.3,1.5]+[max(-1.3,min(1.5,v[j])) for v in parts for j in (3,4)]))
    volume=0.
    for lo,hi in zip(zs,zs[1:]):
        mid=(lo+hi)/2
        intervals=sorted((v[1],v[2]) for v in parts if v[3]<mid<v[4])
        occupied=0.;end=0.
        for r0,r1 in intervals:
            r0=max(r0,end)
            if r1>r0: occupied+=math.pi*(r1*r1-r0*r0)
            end=max(end,r1)
        volume+=(math.pi*.95**2-occupied)*(hi-lo)
    return volume

def main():
    assert geometric_checks(100)==geometric_checks(200)
    for h in (.1,.35,.4,1.):
        assert math.isclose(connected_fluid_volume(0)-connected_fluid_volume(h),area(STEM)*h,abs_tol=1e-12)
    assert math.isclose(pressure_closing(.2,.2),.2*area(STEM))
    # Independent SI reconstruction, projected pressure areas.
    for pc,ps in itertools.product((0.,.08,.5),repeat=2):
        si=(pc*1e6*math.pi*(PORT/2000)**2 -
            ps*1e6*math.pi*((PORT/2000)**2-(STEM/2000)**2))
        assert math.isclose(si,pressure_closing(pc,ps),abs_tol=1e-12)
    cases=[]
    # Includes common batch shifts and opposite local diameter extremes. Rate +-10%
    # is a scenario, NOT catalog tolerance; free length +-0.51 is catalog tolerance.
    for dp,ds,kr,df in itertools.product((-.05,0.,.05),repeat=4):
        r=return_bounds(PORT+dp,STEM+ds,RATE*(1+2*kr),FREE+df*10.2)
        cases.append(r)
    assert all(c['seated_margin']<0 for c in cases)
    # 0...1...0 motion state ordering; fine precedes bypass, remains during reset.
    for s in [i/200 for i in range(201)]+[i/200 for i in range(200,-1,-1)]:
        assert lift(s,'fine')>=lift(s,'bypass')
        if lift(s,'bypass')>0: assert lift(s,'fine')>0
    # Closed-state failure is not cured by index withdrawal or by common head force.
    # Stem geometry exchanges volume while ports are open; do NOT call it final error.
    sweep=area(STEM)*(1.+.4)
    timing=e108.conservative_envelope()['seconds']
    # 5mm effective output arm; servo motion rating is nominal, not loaded bound.
    angle=math.asin(1./5.)
    move=angle/(math.pi/3)*.1
    # Per chunk: full -> fine (.65), fine -> closed (.35). Charge optimistic
    # nominal motion only beyond inherited 2ms for each of those transitions.
    close=math.asin(.35/5.)/(math.pi/3)*.1
    coarse_fine=move-close
    extra_chunk=max(0.,coarse_fine-.002)+max(0.,close-.002)
    timing_nominal=timing+(40*3+4)*extra_chunk
    counts=dict(piston_seals=6400,stem_glands=12800,seats=12800,
                resident_springs=12800,complete_heads=160)
    # Prices are supplier list tiers, not universal minima or negotiated quotes.
    costs=dict(servo_only=160*4.76,bare_motor_only=160*2.80,
               bare_motor_plus_shared250=160*2.80+250,
               maximum_spring_each_shared250_free_heads=(500-250)/12800,
               servo_plus_shared250_free_cells=160*4.76+250)
    assert costs['servo_only']>500
    assert costs['bare_motor_plus_shared250']>500
    print(json.dumps(dict(checks='PASS: finite solid transitions/refinement, pressure SI/limits, independent fluid-volume union, state order, return corners, budget arithmetic',
          nominal=return_bounds(),variation_cases=len(cases),
          seated_margin_range=[min(c['seated_margin'] for c in cases),max(c['seated_margin'] for c in cases)],
          finite_spring_solid_clearance=geometric_checks(200),
          stem_swept_mm3=sweep,open_path_piston_equivalent_mm=sweep/math.pi,
          final_fine_stem_sweep_equivalent_mm=area(STEM)*.35/math.pi,

          output_force_floor_two_valves=2*(.5*area(PORT)+return_bounds()['opening']+.03),
          nominal_servo_move_s=move,nominal_closure_s=close,
          inherited_schedule_s=timing,nominal_transition_only_schedule_s=timing_nominal,
          closure_error_at225mm_s=.05+225*close,
          counts=counts,costs=costs),indent=2))

if __name__=='__main__': main()
