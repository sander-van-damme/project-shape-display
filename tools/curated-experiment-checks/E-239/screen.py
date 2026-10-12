"""E-239: load concentration, gravity following and sourced procurement screen.
Stdlib, stdout only. Prices/specifications: report's dated supplier observations.
All loads, friction, response times, efficiencies and torque scenarios are BOUNDS,
not process priors or motor/retention qualification. No hardware acceptance.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e236', Path(__file__).resolve().parents[1]/'E-236'/'screen.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
G = 9.81
SEQ = (-20, -10, 30, -10, 10)


def move(mm, a=8., v=.2):
    d = abs(mm)/1000
    assert a > 0 and v > 0
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def schedule(banks, a=8., writer=None, rows=None):
    # Change lift acceleration only. Contact/feed retain inherited fast motion.
    w = move(2)+.003 if writer is None else writer
    h = 4*(move(2)+.003)
    cycle = sum(move(d,a) for d in SEQ)+5*(h+w)+move(5.08)
    n = math.ceil(80/banks) if rows is None else rows
    return 2+move(30,a)+.010+(n+1)*cycle


def load(banks=5, payload=2., active_fraction=1., drag=.005, a=8.,
         head_mass=.5, column_mass=.003):
    n = 80*banks
    m = banks*head_mass+n*column_mass+payload*active_fraction
    force = m*(G+a)+n*drag
    return dict(moving_kg=m, peak_up_N=force, static_N=m*G,
                ideal_peak_W=force*.2, assumed_input_W=force*.2/.7,
                output_Nm=force*.01,
                d12_end_loaded_twist_mm=.01*(force*.01)*.4/
                    (80e9*math.pi*.012**4/32)*1000)


def bank_motor(payload=0., drag=.005, a=8., ratio=1., inertia=1e-5):
    x = load(1,payload,1.,drag,a)
    return dict(payload_kg=payload, ratio=ratio,
                rpm=.2/.01*ratio*60/(2*math.pi),
                torque_Nm=x['peak_up_N']*.01/(.8*ratio)+inertia*a*ratio/.01,
                static_brake_Nm=x['static_N']*.01/ratio)


def payload_capacity(torque, drag=.005, a=8., ratio=1., inertia=1e-5):
    # Hypothetical available torque AT THE RESULTING SPEED, not holding torque.
    f=(torque-inertia*a*ratio/.01)*.8*ratio/.01
    return (f-80*drag)/(G+a)-.74


def arrest(mass, delay, speed=.2, brake_torque=.7, radius=.01):
    # Favorable dynamic oracle: grant rated holding torque as dynamic torque,
    # zero reflected inertia and immediate constant torque after delay.
    # Delay assumes no motor torque, brake or helpful guide friction.
    d_delay=speed*delay+.5*G*delay**2
    v=speed+G*delay
    decel=brake_torque/(radius*mass)-G
    return dict(delay_ms=delay*1000,mass_kg=mass,delay_drop_mm=d_delay*1000,
        total_drop_mm=(d_delay+v*v/(2*decel))*1000 if decel>0 else None)


def reserve(banks=5, architecture='common'):
    # E-236 lean non-channel ledger: channel+retention both excluded here.
    # No entry becomes sourced just because another component is quoted.
    items=dict(controller=15,power=20,frame=25,wiring=15,freight_spares=10,
        common_lift_motor_driver=30,common_brake=10,common_phase_drive=10,
        common_feed_drive=10,common_writer_drives=20,common_shafts_bearings=30,
        bank_readers=10*banks,bank_enable=3*banks,local_arrest=3*banks,
        bank_mounts_guides=4*banks)
    if architecture=='bank_motors':
        del items['common_lift_motor_driver']; del items['common_brake']
        # Keep local_arrest: motor brake does NOT cover downstream belt failure.
        items['quoted_motor_brakes']=banks*28.05
        items['quoted_drivers']=banks*19.02
    return items


def main():
    # Independent units/formula check against inherited scheduler, no expensive
    # rerun of unchanged synthesis/support combinatorics.
    for b in range(1,81):
        assert abs(schedule(b)-prior.schedule(tuple(d//10 for d in SEQ),
            prior.control.writer('direct',80)['seconds'],b))<1e-9
    for d in (0,2,5,10,20,30,40):
        assert abs(move(d)-prior.move(d))<1e-12
    assert move(0)==0 and load(payload=0,drag=0,a=0)['peak_up_N']==3.7*G
    # Mass additivity / concentration linearity is an independent force check.
    for p,drag,a in it.product((0,.5,2,5),(.001,.005,.02,.05),(2,4,8)):
        x=load(5,p,1,drag,a)
        assert abs(x['peak_up_N']-sum(load(1,p/5,1,drag,a)['peak_up_N']
                                    for _ in range(5)))<1e-9
        assert abs(x['peak_up_N']-load(5,0,1,drag,a)['peak_up_N']-p*(G+a))<1e-9
    assert arrest(1.74,.020)['total_drop_mm']>arrest(1.74,.010)['total_drop_mm']
    assert arrest(100,.01)['total_drop_mm'] is None
    rows=[]
    for p in (0,.5,2,5):
        for concentration,alpha in [('uniform_board',5/80),('all_in_active_rows',1)]:
            rows.append(dict(payload_kg=p,concentration=concentration,
                             **load(payload=p,active_fraction=alpha)))
    follow=[]
    for drag in (.001,.005,.01,.02,.025,.03):
        limit=G-drag/.003
        if limit<=0:
            follow.append(dict(drag_N=drag,accel_limit=limit,decision='cannot follow even quasistatically'))
            continue
        # Equality is zero contact preload: a necessary-condition boundary, not
        # a permissible operating setpoint. No margin is silently granted.
        a=min(8.,limit)
        b=next(b for b in range(1,81) if schedule(b,a)<30)
        follow.append(dict(drag_N=drag,accel_boundary=a,banks=b,channels=80*b,
            seconds=schedule(b,a),seconds_B5=schedule(5,a)))
    prices={'Adafruit_2776_solenoid':3.96,'Adafruit_858_geared_stepper':3.96,
            'Pololu_2818_FS90_servo':7.90}
    costs=[]
    for arch in ('common','bank_motors'):
        r=sum(reserve(architecture=arch).values())
        costs.append(dict(architecture=arch,reserve=r,items=reserve(architecture=arch),
            complete_channel_ceiling_at_500=(500-r)/400,
            complete_channel_ceiling_at_400=(400-r)/400,
            catalog_bare_actuator_totals={k:400*p for k,p in prices.items()},
            partial_machine_totals={k:r+400*p for k,p in prices.items()}))
    # Tipping points do not require guessed assembly or controller prices.
    ceilings={str(r):{'complete_channel_cap':(500-r)/400,
        'max_channels_at_3_96_bare':math.floor((500-r)/3.96)}
        for r in (0,150,250,295)}
    lo,hi=1.,8.
    for _ in range(60):
        mid=(lo+hi)/2
        if schedule(5,mid)<30: hi=mid
        else: lo=mid
    accel_tip=hi
    assert abs(schedule(5,accel_tip)-30)<1e-9
    print(json.dumps(dict(gravity_B5_tipping=dict(acceleration=accel_tip,
        max_drag_without_contact_margin=.003*(G-accel_tip)),checks=dict(schedule_comparisons=80,force_cases=48),
        legacy_uniform_board_payload_kg=6400*3.27/G,
        legacy_active_five_rows_payload_kg=400*3.27/G,
        load_scenarios=rows,gravity_following=follow,
        torque_scenarios=[bank_motor(p,ratio=r,inertia=j)
            for p,r,j in it.product((0,.125,.4,1.,2.,5.),(1.,2.),(1e-5,5e-5))],
        payload_capacity_at_assumed_speed_torque={str(t):payload_capacity(t)
            for t in (.15,.30,.45)},
        arrest_scenarios=[arrest(.74+p,t) for p,t in it.product((.4,1.,2.,5.),(.001,.010,.020))],
        costs=costs,reserve_sensitivity=ceilings,
        solenoid_all_on_A=400*1.1,solenoid_all_on_W=400*5*1.1,
        solenoid_bare_mass_kg=400*.0126,
        timing=dict(B5=schedule(5),regional_five_rows=schedule(5,rows=5),
                    B4=schedule(4),B5_max_write_s=(30-schedule(5,writer=0))/(17*5)),
        static_whole_board_N=(6400*.003+5)*G),indent=2))

if __name__=='__main__': main()
