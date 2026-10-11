#!/usr/bin/env python3
"""SI units. Deterministic bounded scenarios, NOT calibrated manufacturing priors.
Torque-loss holonomic cam with position-dependent output inertia and passive RL
sink. RK4; energy/barrier certificate is distinct from stationary-well proof.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import itertools
import json
import math
from dataclasses import dataclass, replace

TAU = 2*math.pi
PERIOD = TAU/4

@dataclass(frozen=True)
class Model:
    force: float = 10.
    mass: float = 1.02
    inertia: float = 1e-6
    damping: float = 1e-4
    lead: float = .004
    amplitude: float = .0003
    delay: float = .003
    electrical_tau: float = 0.
    # With R=1, K=sqrt(c), L=tau. Equivalent normalized circuit,
    # preserving c, L/R, stored energy, and electrical heat, not physical amps.

    def path(self, q):
        sn, cs = math.sin(4*q), math.cos(4*q)
        return (self.lead/TAU*q+self.amplitude*sn,
                self.lead/TAU+4*self.amplitude*cs, -16*self.amplitude*sn)

    def extrema(self):
        peak=math.acos(-self.lead/(TAU*4*self.amplitude))/4
        return peak, PERIOD-peak

    def energy(self, y):
        q,v,i,_=y
        h,hp,_=self.path(q)
        return .5*(self.inertia+self.mass*hp*hp)*v*v + self.force*h + .5*self.electrical_tau*i*i

    def rhs(self, y, active):
        q,v,i,_=y
        _,hp,hpp=self.path(q)
        j=self.inertia+self.mass*hp*hp
        if active and self.electrical_tau:
            torque=math.sqrt(self.damping)*i
            di=(math.sqrt(self.damping)*v-i)/self.electrical_tau
            heat=i*i
        else:
            torque=self.damping*v if active else 0.
            di=0.
            heat=torque*v
        return (v,(-self.mass*hp*hpp*v*v-self.force*hp-torque)/j,di,heat)


def rk4(m,y,dt,active):
    a=m.rhs(y,active)
    b=m.rhs(tuple(x+dt*s/2 for x,s in zip(y,a)),active)
    c=m.rhs(tuple(x+dt*s/2 for x,s in zip(y,b)),active)
    d=m.rhs(tuple(x+dt*s for x,s in zip(y,c)),active)
    return tuple(x+dt*(w+2*u+2*v+z)/6 for x,w,u,v,z in zip(y,a,b,c,d))


def run(m,phase=.0,rpm=-1200.,dtmax=.001,horizon=3.,refinement=1,initial_current=0.):
    peak,valley=m.extrema()
    # Start in basin 30, with phase measured between its bounding crests.
    q0=peak+(30+phase)*PERIOD
    y=(q0,rpm*TAU/60,initial_current,0.)
    e0=m.energy(y); h0=m.path(q0)[0]
    t=0.; capture=None; settle=None; last_peak=30; downhill=0; uphill=0
    min_q=q0; max_drop=0.; max_rise=0.; max_residual=0.; max_heat_power=0.
    while t<horizon:
        q,v,i,heat=y
        basin=math.floor((q-peak)/PERIOD)
        if basin<last_peak: downhill+=last_peak-basin
        if basin>last_peak: uphill+=basin-last_peak
        last_peak=basin
        energy=m.energy(y)
        barrier=m.force*m.path(peak+basin*PERIOD)[0]
        min_q=min(min_q,q); max_drop=max(max_drop,h0-m.path(q)[0])
        max_rise=max(max_rise,m.path(q)[0]-h0)
        max_residual=max(max_residual,abs(energy+heat-e0))
        # After circuit closure, total stored energy below the lower adjacent
        # crest is an analytical trapping criterion, evaluated numerically here.
        if m.force>0 and t>=m.delay and energy<barrier-1e-12 and capture is None:
            capture=t
        qmin=valley+basin*PERIOD
        excess=energy-m.force*m.path(qmin)[0]
        # Reporting convention, NOT an allowed-drop/height specification:
        # Energy envelope bounds ALL subsequent speeds by .01 rad/s, and
        # equivalent potential excess by 1 micrometre, while sink stays closed.
        if capture is not None and excess<min(m.force*1e-6,.5*m.inertia*.01**2):
            settle=t
            break
        if q<q0-40*PERIOD:
            break  # unbounded path diagnostic exceeded full nominal stroke
        active=t>=m.delay-1e-14
        _,hp,hpp=m.path(q)
        jeff=m.inertia+m.mass*hp*hp
        natural=math.sqrt(max(m.force*abs(hpp)/jeff,1e-12))
        metric_rate=abs(m.mass*hp*hpp*v)/jeff
        dt=min(dtmax,.04/(natural+abs(v)*4+metric_rate+1),
               .15*jeff/m.damping if active and m.damping else dtmax)
        if active and m.electrical_tau: dt=min(dt,.15*m.electrical_tau)
        dt/=refinement
        dt=min(dt,horizon-t)
        if not active: dt=min(dt,m.delay-t)
        if dt<1e-15: raise AssertionError('zero timestep')
        max_heat_power=max(max_heat_power,m.rhs(y,active)[3])
        y=rk4(m,y,dt,active); t+=dt
    residual=abs(m.energy(y)+y[3]-e0)
    return dict(captured=capture is not None,settled=settle is not None,
        capture_s=capture,settle_s=settle,time_s=t,downhill_crest_crossings=downhill,
        uphill_crest_crossings=uphill,basin_shift=last_peak-30,
        max_drop_mm=max_drop*1000,max_rise_mm=max_rise*1000,rotor_travel_rad=q0-min_q,
        heat_J=y[3],peak_heat_W=max_heat_power,final_speed_rad_s=y[1],
        final_q=y[0],energy_error_J=max(max_residual,residual),
        full_stroke_exit=y[0]<q0-40*PERIOD)


def aggregate(rows):
    return dict(cases=len(rows),captured=sum(x['captured'] for x in rows),
        settled=sum(x['settled'] for x in rows),stroke_exits=sum(x['full_stroke_exit'] for x in rows),
        max_downhill_crossings=max(x['downhill_crest_crossings'] for x in rows),
        max_drop_mm=max(x['max_drop_mm'] for x in rows),
        max_capture_s=max((x['capture_s'] or 0) for x in rows),
        max_settle_s=max((x['settle_s'] or 0) for x in rows),
        max_heat_J=max(x['heat_J'] for x in rows),
        max_energy_error_J=max(x['energy_error_J'] for x in rows))


def sweep_group(pair):
    force,c=pair
    rows=[]
    for j,mass,rpm,phase in itertools.product((1e-7,1e-5),
            (max(.002,force/9.81),1.1),(-600.,-2400.),
            (.001,.251,.501,.751)):
        rows.append(run(Model(force=force,mass=mass,inertia=j,damping=c),phase,rpm,horizon=1.,
                        refinement=4 if force==.02 and c==1e-5 else 1))
    return dict(force_N=force,c_Nms=c,**aggregate(rows))


def sweep():
    # Two local numerical workers; finite deterministic cases, no fitted priors.
    pairs=list(itertools.product((.02,1.,10.),(1e-5,1e-4,1e-3)))
    with ProcessPoolExecutor(max_workers=2) as pool:
        return list(pool.map(sweep_group,pairs))


def diagnostics():
    base=Model()
    # Independent differential energy balance, including variable inertia.
    rl=replace(base,electrical_tau=.001)
    differential_error=0.
    for q,v,i in itertools.product((.1,.7,1.3),(-250.,0.,250.),(-2.,0.,2.)):
        _,dv,di,heat=rl.rhs((q,v,i,0.),True)
        _,hp,hpp=rl.path(q)
        power=(rl.inertia+rl.mass*hp*hp)*v*dv+rl.mass*hp*hpp*v**3+rl.force*hp*v+rl.electrical_tau*i*di
        differential_error=max(differential_error,abs(power+heat))
    assert differential_error<1e-10
    rows=[]
    for c in (0.,1e-5,1e-4,1e-3):
        for speed in (-2400.,-1200.,0.,1200.):
            rows.append(dict(c_Nms=c,rpm=speed,**run(replace(base,damping=c),.001,speed)))
    bounds=[]
    # Exact no-load / constant inertia / viscous limit: travel=v0*(delay+J/c).
    free=Model(force=0,mass=0,inertia=1e-6,damping=1e-4)
    for refinement in (1,2,4):
        r=run(free,.2,-1200.,horizon=.3,refinement=refinement)
        exact=1200*TAU/60*(free.delay+free.inertia/free.damping)
        assert abs(r['rotor_travel_rad']-exact)<2e-7
        bounds.append(dict(refinement=refinement,exact_travel_rad=exact,**r))
    undamped=run(replace(base,damping=0,delay=0),.999,0)
    assert undamped['full_stroke_exit'] and not undamped['captured']
    # RL holdout includes magnetic energy. Three resolutions; no instant brake.
    convergence=[]
    for c,tau in itertools.product((1e-4,1e-3),(0.,.001,.01)):
        runs=[run(replace(base,damping=c,electrical_tau=tau,delay=0),.251,-2400.,refinement=r,
                  initial_current=math.sqrt(c)*(-2400*TAU/60) if tau else 0.)
              for r in (1,2,4)]
        assert abs(runs[-1]['max_drop_mm']-runs[-2]['max_drop_mm'])<.003
        assert max(r['energy_error_J'] for r in runs)<2e-5
        convergence.append(dict(c_Nms=c,electrical_tau_s=tau,runs=runs))
    weak=Model(inertia=2e-8,damping=.004546295548320662**2/7.5)
    weak_checks=[run(weak,.251,-2400.,refinement=r) for r in (1,2,4,8)]
    assert all(r['full_stroke_exit'] for r in weak_checks)
    assert weak_checks[-1]['energy_error_J']<1e-7
    corners=[]
    for lead,amp,delay in itertools.product((.0039,.0041),(.00025,.00035),(0.,.02)):
        m=replace(base,lead=lead,amplitude=amp,delay=delay)
        rs=[run(m,p,-2400.) for p in (.001,.251,.501,.751)]
        corners.append(dict(lead_mm=lead*1000,amplitude_mm=amp*1000,delay_s=delay,**aggregate(rs)))
    return dict(differential_energy_error_W=differential_error,
                witnesses=rows,zero_load_exact=bounds,RL_convergence=convergence,
                coherent_geometry_and_delay=corners,weak_rotor_convergence=weak_checks)


def motor():
    # Pololu 1117 approximate 6-V data. Derived constant; no-load friction
    # removed for Ke estimation, but no passive friction credited thereafter.
    resistance=6/.8
    ke=(6-.07*resistance)/(11500*TAU/60)
    out=[]
    for ratio in (1,3,6):
        c=(ratio*ke)**2/resistance
        for jm in (1e-8,1e-7):  # explicit unknown rotor-inertia bracket
            m=Model(inertia=1e-8+jm*ratio**2,damping=c)
            rs=[run(m,p,-2400.,refinement=8 if m.inertia<3e-8 else 1)
                for p in (.001,.126,.251,.376,.501,.626,.751,.876)]
            out.append(dict(ratio=ratio,motor_inertia_kgm2=jm,c_Nms=c,
                brake_current_2400rpm_A=ratio*ke*2400*TAU/60/resistance,
                drive_voltage_peak_static_load_at_2400rpm=ratio*ke*2400*TAU/60+resistance*.0183662/(ratio*ke),
                **aggregate(rs)))
    return dict(R_ohm=resistance,Ke_SI=ke,cases=out)


def board():
    rows=[]
    for turns,rpm in itertools.product((10,11),(600,1200,2400)):
        service=turns*60/rpm+.1
        heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30)
        rows.append(dict(turns=turns,rpm=rpm,heads=heads,
            time_s=6+math.ceil(6400/heads)*service,
            head_purchase_allowance_with_250_shared_USD=250/heads,
            motor_plus_relay_favorable_100_unit_price_USD=heads*(2.30+2.8039)))
    contacts=[]
    for rpm in (600,1200,2400):
        acceleration=.0003*16*(rpm*TAU/60)**2
        contacts.append(dict(rpm=rpm,peak_output_acceleration_m_s2=acceleration,
            vertical_contact_force_range_N=[10-1.02*acceleration,10+1.02*acceleration]))
    return dict(schedule=rows,constant_speed_contact=contacts,
        gravity_only_contact_loss_threshold_rpm=math.sqrt(9.81/(.0003*16))*60/TAU,
        lowering_6400_by_40mm_J={str(f):6400*f*.04 for f in (.02,1,10)},
        permanent_generator_2400rpm_heat_per_nominal_40mm_J={str(c):c*(2400*TAU/60)*(10*TAU) for c in (1e-4,1e-3)},
        no_bias_exact_limit='zero force: no parked potential barrier',
        damping_running_energy_scale_at_10N_J1e6_Nms=(.004/TAU)*math.sqrt(10*1e-6/(2*.000186607)))


def low_load_checks():
    refined=sweep_group((.02,1e-5))
    holdouts=[]
    for c,phase in itertools.product((1e-4,1e-3),(.251,.751)):
        model=Model(force=.02,mass=1.1,inertia=1e-7,damping=c)
        rows=[run(model,phase,-2400,horizon=1,refinement=r) for r in (1,2,4)]
        assert len({r['captured'] for r in rows})==1
        assert abs(rows[-1]['max_drop_mm']-rows[-2]['max_drop_mm'])<1.1e-5
        holdouts.append(dict(c_Nms=c,phase=phase,runs=rows))
    return dict(refined_group=refined,holdouts=holdouts)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--sweep',action='store_true')
    p.add_argument('--low-load-check',action='store_true')
    a=p.parse_args()
    if a.low_load_check:
        result=low_load_checks()
    else:
        result=dict(diagnostics=diagnostics(),motor=motor(),board=board())
        if a.sweep: result['sweep']=sweep()
    print(json.dumps(result,indent=2))
