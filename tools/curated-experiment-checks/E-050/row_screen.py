"""Finite necessary-condition synthesis. SI-derived mm/N/s units; no priors.
All scenario values are explicit bounds, not X1C capability or supplier quotes.
Run: python3 tools/curated-experiment-checks/E-050/row_screen.py
"""
import itertools as it
import json
from math import ceil, pi, sqrt

N, PITCH, STROKE = 80, 5.08, 40.
SCENARIOS = {
 'fast': dict(v=400., a=20000., rpm=6000., contact=.04, read=.01, index=.025, overhead=2., retry=0),
 'central': dict(v=200., a=5000., rpm=3000., contact=.08, read=.02, index=.05, overhead=4., retry=1),
 'slow': dict(v=80., a=1000., rpm=1000., contact=.16, read=.04, index=.10, overhead=8., retry=8),
}
FAMILIES = {
 'rack': ('linear lane', 'tooth/pawl', 'linear motor', 'pawl/local grid', 3, 0),
 'screw': ('rotary lane', 'thread angle', 'spindle', 'nut/local grid', 2, 0),
 'fluid': ('docking lane', 'trapped volume', 'pump/return', 'piston/valve/base', 3, 1),
}

def move(d, v, a):
    """Rest-to-rest trapezoid/triangle, no jerk constraint; optimistic lower bound."""
    return 2*sqrt(d/a) if d <= v*v/a else d/v+v/a

def evaluate(family, lanes, scenario, lead=1., region=(80,80)):
    s=SCENARIOS[scenario]
    # Each physical row needs its own lane subset. No fictitious packing of
    # a narrow region into otherwise idle columns on the same row.
    rows=lanes//80 if lanes>=80 else 1
    cols=min(lanes,80)
    stations=ceil(region[0]/rows)*ceil(region[1]/cols)
    if family=='screw':
        # Rotation acceleration omitted deliberately: lower bound only.
        motion=STROKE/lead*60/s['rpm']
    elif family=='rack':
        # Stop at acquisition and target: path length alone misses the
        # extra acceleration required by intermediate-height transitions.
        motion=max(sum(move(d,s['v'],s['a']) for d in
                   (old*10,abs(new-old)*10,new*10))
                   for old,new in it.product(range(5),repeat=2) if old!=new)
    else:
        motion=2*move(STROKE,s['v'],s['a'])
    dwell=motion+s['contact']+s['read']
    # Indexing cannot outrun carriage acceleration. Row-wrap travel for
    # partial-width heads remains omitted, making those times lower bounds.
    index=max(s['index'],move(PITCH*(rows if lanes>=80 else cols),s['v'],s['a']))
    t=s['overhead']+stations*(dwell+index)+s['retry']*dwell
    return t, stations

def geometry(overlap, tooth, error, modulus, load):
    """2D rectangular rack/pawl support-section screen; not full mechanism CAD.
    Error is adverse relative alignment, mm. Lateral envelope includes
    a 2.4-mm rack web, overlap, 0.8-mm support wall and two error clearances.
    Tooth width 2.4 mm, 1.0-mm cantilever reach; 10-mm vertical state pitch.
    """
    effective=overlap-error
    width=2.4
    stress=6*load/(width*tooth**2)  # N/mm² with 1-mm reach
    deflection=4*load/(modulus*width*tooth**3)
    return dict(overlap=effective, envelope=2.4+overlap+.8+2*error,
                stress=stress, deflection=deflection,
                passes=effective>=.4 and 2.4+overlap+.8+2*error<=PITCH
                and stress<=8 and deflection<=.1 and tooth+2*error<10)

def transitions():
    count=0
    for old,new in it.product(range(5),repeat=2):
        # Every unchanged cell remains latched. Selected cell transfer order:
        # latch -> latch+grip -> grip -> grip+latch -> latch.
        supports=[(True,False),(True,True),(False,True),(True,True),(True,False)]
        assert all(latch or grip for latch,grip in supports)
        distance=old*10+abs(new-old)*10+new*10
        assert distance<=80
        count+=1
    return count

def main():
    assert move(0,400,20000)==0
    assert abs(move(40,400,20000)-.12)<1e-12
    assert abs(move(40,200,5000)-.24)<1e-12
    assert abs(evaluate('rack',80,'fast')[0]-(2+80*(.31+2*sqrt(5.08/20000))))<1e-10
    assert evaluate('rack',160,'fast',(1.),(1,1))[1]==1
    assert evaluate('rack',160,'fast',region=(5,5))[1]==3
    assert transitions()==25
    rows=[]
    for f,h,s in it.product(FAMILIES,(8,16,40,80,160),SCENARIOS):
        for lead in ((1.,2.,4.) if f=='screw' else (1.,)):
            t,_=evaluate(f,h,s,lead)
            # Friction scenarios 0.08..0.30; robust self-locking at minimum.
            hold=lead/(pi*3)<.08 if f=='screw' else None
            rows.append(dict(family=f,lanes=h,scenario=s,lead=lead,seconds=round(t,4),
                timing=t<30,retention_bound=hold))
    geom=[]
    # Nested errors aggregate batch bias + regional warp + local fit error.
    errors={'tight':.05+.05+.05,'middle':.10+.10+.15,'wide':.20+.20+.20}
    for o,h,e,E,F in it.product((.6,.9,1.2),(1.,1.5,2.),errors,(500.,1500.,3000.),(1.,10.,100.)):
        g=geometry(o,h,errors[e],E,F)
        geom.append(dict(o=o,h=h,error=e,E=E,F=F,**g))
    assert not any(g['passes'] for g in geom if g['F']==100)
    robust=[(o,h) for o,h in it.product((.6,.9,1.2),(1.,1.5,2.))
            if all(g['passes'] for g in geom if g['o']==o and g['h']==h and g['F']==10)]
    # A common closure defect is NOT 6400 independent events. Enumeration,
    # not a sampled yield claim: leaking piston bore 3 mm, 0.1 mm drift/4 h.
    allowed_leak=pi*1.5**2*.1/(4*3600) # mm³/s per cell
    costs=[]
    for h,reserve,head,cell in it.product((80,160),(150,250,350),(1,3,6),(0,.02,.05)):
        costs.append(dict(lanes=h,reserve=reserve,head=head,cell=cell,
                          total=reserve+h*head+6400*cell))
    summary=dict(seed=None,method='exhaustive Cartesian enumeration; no probabilities',
      schedule_cases=len(rows),timing_passes=sum(r['timing'] for r in rows),
      timing_passes_by_family={f:sum(r['timing'] for r in rows if r['family']==f) for f in FAMILIES},
      screw_hold_passes=sum(r['retention_bound'] for r in rows if r['family']=='screw'),
      rack_schedules=[r for r in rows if r['family']=='rack' and r['timing']],
      geometry_cases=len(geom),geometry_passes=sum(g['passes'] for g in geom),
      geometry_passes_by_error={e:sum(g['passes'] for g in geom if g['error']==e) for e in errors},
      robust_geometry_at_10N=robust,fluid_leak_limit_mm3_s=allowed_leak,
      fluid_pressure_MPa_at_10N=10/(pi*1.5**2),
      cost_cases=len(costs),cost_passes=sum(c['total']<=500 for c in costs),
      undetected_expected_cells={str(p):6400*p for p in (1e-3,1e-4,1e-5)},
      correlated_false_accept_cells_per_bad_row=80,
      local_rack_times={s:round(evaluate('rack',160,s,region=(5,5))[0],4) for s in SCENARIOS},
      timing_sensitivity_acceleration_10000=2+80*(move(40,400,10000)+2*move(20,400,10000)+.04+.01+move(5.08,400,10000)),
      central_160_seconds=evaluate('rack',160,'central')[0],
      min_column_solid_volume_litres=6400*2.4*2.4*60/1e6)
    print(json.dumps(dict(summary=summary,scenarios=SCENARIOS,descriptors=FAMILIES,
                         schedules=rows,geometry=geom,costs=costs),indent=2))
if __name__=='__main__': main()
