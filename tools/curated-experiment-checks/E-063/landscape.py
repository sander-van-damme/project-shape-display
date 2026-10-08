#!/usr/bin/env python3
"""E-063 deterministic necessary bounds; SI except explicitly suffixed mm.
No fitted distributions, random seed, geometry qualification or hardware claims.
Run without arguments for compact JSON; --all includes enumerated populations.
"""
import itertools as it
import json
import math
import sys

N = 6400
PITCH = 5.08
EPS0 = 8.8541878128e-12


def move_mm(d, v=100, a=500):
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def electro():
    # Ideal series air/dielectric gap, pressure on opposing conductor.
    # Gap scenarios are epistemic correlated contamination/flatness bounds.
    out = []
    for t, gap, voltage, mu in it.product([10, 25, 50], [0, 5, 20], [200, 500], [.2, .5]):
        effective = (gap+t/3)*1e-6
        pressure = EPS0/2*(voltage/effective)**2
        force = mu*pressure*40e-6  # 2 x 20 mm contact
        out.append(dict(t_um=t, gap_um=gap, V=voltage, mu=mu,
                        force_N=force, release_pass=force>=.05, hold_pass=force>=1,
                        dielectric_MVm=voltage/(t+3*gap),
                        stored_J_two_board_arrays=N*2*.5*EPS0*40e-6/effective*voltage**2))
    return out


def magnetic():
    # Desired normalized full signal=2, half=1. Field error includes neighbor
    # field and rail variation; threshold spread includes batch and local terms.
    out = []
    for field_error, threshold_spread in it.product([.05,.15,.25], [.05,.15,.30]):
        lower=(1+field_error)/(1-threshold_spread)
        upper=2*(1-field_error)/(1+threshold_spread)
        out.append(dict(field_error=field_error, threshold_spread=threshold_spread,
                        nominal_threshold_interval=[lower,upper], survives=lower<upper))
    return out


def thermal():
    # Dynalloy 0.050mm: 500 ohm/m, 85mA ~1s heat, .4s LT cool.
    # 0.2--1.0mm release at assumed 4% working strain, straight vertical wire.
    return [dict(release_mm=s, length_mm=s/.04,
                 board_wire_m=N*s/.04/1000,
                 board_pulse_J=N*.085**2*500*s/.04/1000,
                 simultaneous_current_A=N*.085,
                 row_serial_s=80*1.4, parallel_thermal_s=1.4,
                 wire_price_lower_USD=N*s/.04/1000*(6 if N*s/.04/1000<=100 else 4))
            for s in [.2,.5,1.0]]


def phase():
    out=[]
    # Competing generic material scenarios, NOT sourced alloy constants.
    for volume, enthalpy, sink in it.product([.5,2,10], [.2,.5,1.0], [.002,.02,.2]):
        q=volume*enthalpy
        # sink W/K per site, maximum 20K thermal driving head: optimistic
        # latent-stage cooling lower bound, ignores final temperature approach.
        out.append(dict(volume_mm3=volume, enthalpy_J_mm3=enthalpy,
                        sink_W_K=sink, board_J=N*q, min_cooling_s=q/(20*sink),
                        min_average_heat_W=N*q/30,
                        sink_at_20K_board_W=N*20*sink))
    return out


def scissor():
    out=[]
    # Actual 2D bars: length L, angle theta, width L cos(theta),
    # stage height L sin(theta); pair crosses at stage midpoint.
    # Check width THROUGH monotone transition, not just travel.
    for L, lo, hi, stages, error in it.product([3,4,5], [10,20,30], [65,75,85], range(1,25), [.15,.35,.60]):
        a,b=map(math.radians,[lo,hi]); width=L*math.cos(a)+.8+2*error
        travel=stages*L*(math.sin(b)-math.sin(a))
        lateral_gain=stages/math.tan(a) # abs(dH/dw), input force/load ratio
        reasons=[]
        if width>PITCH: reasons.append('pitch')
        if travel<40: reasons.append('travel')
        out.append(dict(L_mm=L, low_deg=lo, high_deg=hi, stages=stages,
                        error_mm=error, width_mm=width, travel_mm=travel,
                        deployed_height_mm=stages*L*math.sin(b),
                        lateral_force_per_N=lateral_gain, bars=2*stages,
                        reasons=reasons))
    return out


def sparse():
    size=80
    funcs={
        'hill': lambda x,y:20+10*math.cos(2*math.pi*x/79)*math.cos(2*math.pi*y/79),
        'wall': lambda x,y:40.0 if x==39 else 0.0,
        'step': lambda x,y:40.0 if x>=40 else 0.0,
        'checker': lambda x,y:40.0*((x+y)%2),
    }
    out=[]
    for spacing in [1,2,5,10]:
        for offset in range(spacing):
            nodes=sorted(set([0,79]+list(range(offset,80,spacing))))
            spans=[]
            for x in range(size):
                low=max(n for n in nodes if n<=x); high=min(n for n in nodes if n>=x)
                spans.append((low,high,0 if high==low else (x-low)/(high-low)))
            for name,f in funcs.items():
                errors=[]; pred=[]
                for y in range(size):
                    yl,yh,fy=spans[y]
                    for x in range(size):
                        xl,xh,fx=spans[x]
                        z=(1-fy)*((1-fx)*f(xl,yl)+fx*f(xh,yl))+fy*((1-fx)*f(xl,yh)+fx*f(xh,yh))
                        errors.append(z-f(x,y));pred.append(z)
                out.append(dict(spacing_cells=spacing, offset=offset, actuators=len(nodes)**2,
                                workload=name, rms_mm=math.sqrt(sum(e*e for e in errors)/N),
                                max_mm=max(map(abs,errors)), reconstructed_peak_mm=max(pred),
                                within_1mm=sum(abs(e)<=1 for e in errors)/N))
    return out


def transitions():
    # Binary layers [10,20,40] support outputs 0..70; only 0..40 used.
    # Retract old-only layers before extending new-only: never exceeds endpoints.
    bitplanes=[]
    for old,new in it.product(range(5), repeat=2):
        state=old; path=[10*state]
        for bit in range(3):
            if old&(1<<bit) and not new&(1<<bit):
                state &= ~(1<<bit);path.append(10*state)
        for bit in range(3):
            if new&(1<<bit) and not old&(1<<bit):
                state |= 1<<bit;path.append(10*state)
        assert state==new and min(path)>=0 and max(path)<=max(10*old,10*new)
        bitplanes.append(dict(old=old*10,new=new*10,path=path))
    # Explicit abstract contact transfer, deliberately distinct from geometry.
    def acquire(ground, moving, grip_ok=True):
        assert ground or moving
        moving=grip_ok
        if not moving: return ground,moving,False
        # Ground may withdraw only AFTER successful moving contact.
        ground=False
        assert ground or moving
        return ground,moving,True
    def deposit(ground,moving,latch_ok=True):
        assert moving
        ground=latch_ok
        if not ground: return ground,moving,False
        moving=False
        assert ground or moving
        return ground,moving,True
    for old,new in it.product(range(0,41,10),repeat=2):
        z=old; ground,moving=True,False
        if old==new: continue  # unchanged columns never release ground support
        if old:
            ground,moving,ok=acquire(ground,moving)
            assert ok
            for h in [40,30,20,10,0]:
                if moving:
                    z=old-(40-h)
                    if z==0: ground,moving,ok=deposit(ground,moving)
                assert z>=0 and (ground or moving)
        assert z==0 and ground and not moving
        if new:
            ground,moving,ok=acquire(ground,moving)
            for h in [0,10,20,30,40]:
                if moving:
                    z=h
                    if z==new: ground,moving,ok=deposit(ground,moving)
                assert ground or moving
        assert z==new and ground and not moving
    assert acquire(True,False,False)==(True,False,False)
    assert deposit(False,True,False)==(False,True,False)
    return bitplanes


def main():
    assert move_mm(0)==0 and abs(move_mm(20)-.4)<1e-12
    assert abs(EPS0/2*(500/(25e-6/3))**2*.5*40e-6-.3187507612608)<1e-10
    e,m,p,g,s=electro(),magnetic(),phase(),scissor(),sparse()
    assert all(r['rms_mm']==0 for r in s if r['spacing_cells']==1)
    survivors=[r for r in g if not r['reasons']]
    assert survivors
    # Independent geometric upper bound per stage <= pitch minus allowances.
    assert all(r['stages']>=11 for r in survivors)
    t=transitions()
    result={
      'populations':dict(electro=len(e),magnetic=len(m),phase=len(p),scissor=len(g),sparse=len(s),binary_transitions=len(t)),
      'electro':dict(force_range_N=[min(r['force_N'] for r in e),max(r['force_N'] for r in e)],release_pass=sum(r['release_pass'] for r in e),one_N_pass=sum(r['hold_pass'] for r in e)),
      'magnetic':m,
      'magnetic_gap_bounds': [dict(B_T=B, gap_mm=gap, pole_area_mm2=1,
          force_N=B*B*1e-6/(2*4*math.pi*1e-7),
          ampere_turns=B*gap/1000/(4*math.pi*1e-7),
          board_gap_energy_J=N*B*B*1e-6*gap/1000/(2*4*math.pi*1e-7))
          for B,gap in it.product([.1,.2,.3],[.1,.3,.5])],
      'thermal':thermal(),
      'phase':dict(board_J=[min(r['board_J'] for r in p),max(r['board_J'] for r in p)],cooling_s=[min(r['min_cooling_s'] for r in p),max(r['min_cooling_s'] for r in p)]),
      'scissor':dict(survivors=len(survivors),rejected=len(g)-len(survivors),min_stages=min(r['stages'] for r in survivors),best=min(survivors,key=lambda r:(r['stages'],r['lateral_force_per_N']))),
      'sparse':s,
      'shared':dict(board_force_N=[N*f for f in [.05,.2,1,10]], lift_energy_J=[N*f*.04 for f in [.05,.2,1,10]],
                    dual_clamp_schedule_s={str(dwell):move_mm(40)+8*move_mm(10)+9*dwell+6 for dwell in [.02,.2,1.4]},
                    row_scan_deadline_ms=(30-move_mm(40)-8*move_mm(10)-6)/(9*80)*1000,
                    reserve250_cell_allowance={str(cap):(cap-250)/N for cap in [200,400,500]},
                    pressure_kPa=[f/(math.pi*1.5**2)*1000 for f in [.05,.2,1,10]],
                    membrane_neighbor_strain=math.sqrt(PITCH**2+40**2)/PITCH-1,
                    jamming_interfaces_for10N=math.ceil(10/(.2*50000*40e-6)),
                    binary_interfaces=3*N,
                    binary_six_pass_motion_s=2*sum(move_mm(d) for d in [10,20,40]),
                    pressure_volume_litre=N*math.pi*1.5**2*40/1e6,
                    assembly_hours_at_10_30s=[N*x/3600 for x in [10,30]],
                    expected_missed_sites=[N*p for p in [1e-3,1e-4,1e-5]],
                    heat_diffusion_length_mm=[math.sqrt(alpha*30) for alpha in [.1,10,100]])}
    if '--all' in sys.argv: result['enumerated']=dict(electro=e,phase=p,scissor=g,binary=t)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
