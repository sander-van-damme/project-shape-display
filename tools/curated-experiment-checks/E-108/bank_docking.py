#!/usr/bin/env python3
"""E-108: arrangement comparison, not passage optimization. mm,N,s,MPa.
Deterministic assumption bounds; no component or manufacturing qualification.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import sys

spec=importlib.util.spec_from_file_location('e107',Path(__file__).parents[1]/'E-107/fixed_passage.py')
e107=importlib.util.module_from_spec(spec);sys.modules[spec.name]=e107;spec.loader.exec_module(e107)
e106=e107.e106;e104=e106.e104
A=math.pi
P=e107.Passage('round',.6,40.)
B=e107.Bounds('tight',.025,.008,.012)


def schedule(work,banks=1,extra=0.,speed_scale=1.,mode='fixed',starts=None,chunk=80):
    """Disjoint 40-row zones with independent 8-L/min sources for two banks.
    One global detected fault: pessimistically append the largest row recovery
    after both zones finish. Extra charges complete acquisition+proof+reset cost
    beyond the inherited 40-ms acquire/withdraw and 20-ms read allocations.
    speed_scale stretches flow time only; pressure windows are still B's.
    """
    assert banks in (1,2) and 0<speed_scale<=1 and extra>=0 and 1<=chunk<=80
    sc=e104.Scenario(bore=2.)
    if starts is None:starts=[0] if banks==1 else [0,79]
    times=[];retry=0.;visits=[]
    for bank in range(banks):
        zone={r:cs for r,cs in work.items() if r//(80//banks)==bank and cs}
        if not zone:times.append(0.);visits.append(0);continue
        t=e104.route(zone,starts[bank],sc)
        for cs in zone.values():
            row=.06+extra;rec=.06+extra
            for sign in (1,-1):
                phase_cs=tuple((c,h) for c,h in cs if sign*h>0)
                recovery=tuple((c,sign*40.) for c,h in cs)
                def phase(ch):
                    if not ch:return 0.
                    if mode=='fixed':v=e107.phase(ch,sign,P,B)[0]
                    else:v=e106.phase(ch,sign,'throttled',error=.5,spread=.1,transition=.002)[0]
                    # Both controllers charge 10+2 ms for these full-stroke cases.
                    # For short strokes conservatively stretch any unused transition.
                    return .012+max(0.,v-.012)/speed_scale
                row+=sum(phase(phase_cs[i:i+chunk]) for i in range(0,len(phase_cs),chunk))
                rec+=sum(phase(recovery[i:i+chunk]) for i in range(0,len(recovery),chunk))
            t+=row;retry=max(retry,rec)
        times.append(t);visits.append(len(zone))
    return dict(seconds=(.5+max(times)+retry if any(visits) else 0.),
                bank_seconds=times,retry=retry,visits=visits)


def exchange(volume,gas_fraction,k_wall,pi,pf,n=1.,bulk=1500.):
    """Cavity initially at pi; quasistatic equalization to constant-load pf.
    pi,pf gauge MPa; gas_fraction is at pi, not atmospheric. Linear wall
    compliance volume/k_wall; rigid-wall liquid exponential compressibility;
    polytropic gas P V^n constant. Positive result expels into piston.
    Excludes source replenishment: head valve must already be isolated.
    """
    assert min(pi,pf)>-.101325 and 0<=gas_fraction<1 and n>0
    dp=pi-pf;vl=volume*(1-gas_fraction);vg=volume*gas_fraction
    liquid=vl*math.expm1(dp/bulk)
    gas=vg*(((pi+.101325)/(pf+.101325))**(1/n)-1)
    wall=volume*dp/k_wall
    return liquid+gas+wall


def sequence(early_open=False,early_undock=False):
    """Logical state audit, NOT mechanism/contact or leak proof.
    Target subset only is allowed to open. All 80 faces may dock.
    No live source while passively equalizing; no dump before chamber isolation.
    """
    sealed=False;chamber=False;source=False;trace=[]
    actions=['seal','condition','isolate_head','open_check','flow','close_check',
             'proof','close_head','dump','undock']
    if early_open:actions[0],actions[3]=actions[3],actions[0]
    if early_undock:actions.insert(5,'undock')
    for action in actions:
        if action=='seal':sealed=True
        elif action=='condition':assert sealed and not chamber;source=True
        elif action=='isolate_head':source=False
        elif action=='open_check':assert sealed and not source;chamber=True
        elif action=='flow':assert sealed and chamber;source=True
        elif action=='close_check':chamber=False
        elif action=='proof':assert sealed and not chamber
        elif action=='close_head':source=False
        elif action=='dump':assert not chamber and not source
        elif action=='undock':assert not chamber and not source;sealed=False
        trace.append((action,sealed,chamber,source))
    return trace


def conservative_envelope():
    """Any direction/subset/load assignment within the eight-level bounds.
    At most 40 open channels prevent the discovered easy-load starvation.
    Every active branch retains at least v_coarse even at pump saturation:
    at b_min+loss(Q/(40A)), each of <=40 branches draws <=Q/40.
    Cover all 40 mm coarsely AND the largest terminal band again finely.
    Deliberately loose bound, including up to three chunks per row and four during conservative retry.
    """
    phase_bounds=[]
    fast,slow=e107.extrema(P,B)
    for sign in (1,-1):
        bs=e106.thresholds(tuple((c,sign*40.) for c in range(80)),sign,.1)
        upper=.5 if sign==1 else -.01
        # Actual selected subset may set a lower coarse pressure than b_max.
        # Each branch is still driven at least loss(400) above its own threshold
        # before saturation. Use the lesser of that and global pump reserve.
        pump_speeds=[e106.speed(min(bs)+e106.loss(e106.PUMP/(40*A),.6,mu)-max(bs),.6,mu)
                     for mu in (B.mu_lo,B.mu_hi)]
        vc=min(400.,*pump_speeds,
               e106.speed(upper-2*B.eps-max(bs),.6,B.mu_hi))
        u=min(upper-B.eps,max(bs)+e106.loss(400,.6,B.mu_hi)+B.eps)
        band=e106.speed(u+B.eps-min(bs),.6,B.mu_lo)*.002+.05
        uf=e107.fine_pressure(bs,fast,sign,.5,B.eps)
        vf=e107.speed(uf-B.eps-max(bs),slow)
        assert min(vc,vf)>0
        phase_bounds.append(dict(sign=sign,coarse_min=vc,fine_min=vf,band=band,
                                 seconds=40/vc+band/vf+.012))
    phase_max=max(x['seconds'] for x in phase_bounds)
    chunks=max(math.ceil(n/40)+math.ceil((80-n)/40) for n in range(81))
    assert chunks==3
    row=.06+chunks*phase_max
    recovery=.06+4*phase_max
    total=.5+e104.route(range(40),0,e104.Scenario(bore=2.))+40*row+recovery
    return dict(seconds=total,phase_bounds=phase_bounds,
                max_extra_seconds_per_visit=(30-total)/41)


def checks():
    assert schedule({})['seconds']==0
    assert exchange(0,.1,100,.3,.1)==0
    assert exchange(10,.1,100,.1,.1)==0
    assert math.isclose(exchange(20,.1,100,.3,.1),2*exchange(10,.1,100,.3,.1))
    # Independent exact isothermal gas volume: 1 mm3 at .4 MPa absolute doubles
    # at .2 MPa; subtract separately computed liquid and wall components.
    assert math.isclose(exchange(10,.1,math.inf,.298675,.098675)-
                        9*math.expm1(.2/1500),1.)
    for pi,pf in ((.5,.08),(.01,.14)):
        # Independent numerical compliance integration, refine midpoint mesh.
        exact=exchange(10,.05,100,pi,pf,n=1.4)
        errs=[]
        for steps in (100,200,400):
            dp=(pi-pf)/steps;total=0
            for i in range(steps):
                p=pf+(i+.5)*dp
                vl=9.5*math.exp((pi-p)/1500)
                vg=.5*((pi+.101325)/(p+.101325))**(1/1.4)
                total+=(vl/1500+vg/(1.4*(p+.101325))+10/100)*dp
            errs.append(abs(total-exact))
        assert errs[-1]<errs[0]/10 and errs[-1]<1e-5
    sequence()
    for bad in ('early_open','early_undock'):
        try:sequence(**{bad:True})
        except AssertionError:pass
        else:raise AssertionError('unsafe sequence accepted')
    ws=e104.workloads()
    assert math.isclose(schedule(ws['checkerboard'])['seconds'],e107.evaluate(ws['checkerboard'],P,B)['seconds'])
    assert schedule(ws['checkerboard'],2)['seconds']<schedule(ws['checkerboard'])['seconds']
    bound=conservative_envelope()['seconds']
    for w in ws.values():assert schedule(w,2,chunk=40)['seconds']<=bound
    assert schedule(ws['checkerboard'],2,extra=.02)['seconds']>schedule(ws['checkerboard'],2)['seconds']
    assert schedule(ws['checkerboard'],2,speed_scale=.8)['seconds']>schedule(ws['checkerboard'],2)['seconds']
    return 'PASS: conservation/limits, independent compliance quadrature, sequence failure injection, inherited schedule replay, monotonicity'


def main():
    report={'input_revision':'301aa30','checks':checks(),'workloads':{},'sensitivity':[], 'wet_exchange':[]}
    ws=e104.workloads()
    for name,w in ws.items():
        report['workloads'][name]={k:schedule(w,**kw) for k,kw in {
            'single_fixed':{},'dual_fixed':{'banks':2},'dual_chunk40':{'banks':2,'chunk':40},
            'wet_ideal_no_extra':{'mode':'ideal'},
            'wet_ideal_extra20ms':{'mode':'ideal','extra':.02}}.items()}
    # Direction/load correlations: enumerate all contiguous direction cuts and
    # 16 offsets relative to eight paired payload levels, including unmixed rows.
    worst=(0.,None)
    for split,offset in itertools.product(range(81),range(16)):
        cs=[(c,40. if (c-offset)%80<split else -40.) for c in range(80)]
        t=schedule({r:cs for r in range(80)},2)['seconds']
        if t>worst[0]:worst=(t,(split,offset))
    report['conservative_envelope']=conservative_envelope()
    bs=[.35/A]*79+[.45/A]
    u=max(bs)+e106.loss(400,.6,.012)
    try:
        e106.pressure_rates(bs,u,list(range(80)),.6,.012)
        raise AssertionError('expected starvation witness absent')
    except ValueError as exc:report['starvation_witness']=str(exc)
    vs=e106.pressure_rates(bs,u,list(range(39))+[79],.6,.012)
    assert min(vs.values())>=400.-1e-7
    report['chunk40_starvation_witness_min_speed']=min(vs.values())
    report['direction_scan']={'cases':1296,'worst_seconds':worst[0],'split_offset':worst[1]}
    for scale,extra in itertools.product((1.,.8,.5), (0.,.04,.1)):
        report['sensitivity'].append(dict(scale=scale,extra=extra,
          seconds=schedule(ws['minority_down'],2,extra,speed_scale=scale,chunk=40)['seconds']))
    local=[]
    for r0,c0 in itertools.product(range(71),range(16)):
        w={r:[(c,40.*(-1 if (r+c)%2 else 1)) for c in range(c0,c0+10)] for r in range(r0,r0+10)}
        for starts in ([0,79],[39,40]):local.append(schedule(w,2,starts=starts,chunk=40)['seconds'])
    report['local']={'cases':len(local),'min':min(local),'max':max(local),'columns':'16 distinct load/direction offsets; 71 row placements; both zone endpoint starts'}
    # Nonlinear air, wall, dead volume and pressure history. Explicit scenario
    # grid; not process data, probability, or calibrated upper bounds.
    for v,g,k,pi,pf,n in itertools.product((1.,10.,100.),(0.,.01,.1),(10.,100.,1000.),(.01,.5),(.08,.14),(1.,1.4)):
        dv=exchange(v,g,k,pi,pf,n)
        report['wet_exchange'].append(dict(volume=v,gas_at_pi=g,wall_k=k,pi=pi,pf=pf,n=n,dx=dv/A))
    report['wet_inverse']={
        'extra_ms_per_visit_ideal':1000*(30-schedule(ws['checkerboard'],mode='ideal')['seconds'])/81,
        'swept_mm3_for_point1mm':.1*A,
        'air_loss_ml_per_map_at_01mm3_per_dock':6400*.01/1000,
        'air_loss_ml_per_1000maps_at_01mm3_per_dock':6400*.01,
        'board_displacement_litres':6400*A*40/1e6,
        'dual_ideal_power_w_at_point5MPa':2*.5*8*1000/60,
        'pressure_separation_force_80_faces_2mm_bore_point5MPa':80*A*.5}
    report['joint_cost']=[dict(banks=n,shared=s,cell=c,max_complete_head=(500-s-6400*c)/(80*n))
        for n,s,c in itertools.product((1,2),(150,250,350),(.0,.01,.02,.04))]
    report['reference_exchange']=[dict(pi=pi,pf=pf,dx=exchange(10,.01,100,pi,pf)/A) for pi,pf in ((.5,.08),(.01,.14))]
    if '--all' not in sys.argv:
        pop=report.pop('wet_exchange');report['wet_grid']={'cases':len(pop),'min_mm':min(x['dx'] for x in pop),'max_mm':max(x['dx'] for x in pop)}
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
