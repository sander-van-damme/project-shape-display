"""E-217: finite logical media replay and necessary architecture bounds.
All dimensions, accelerations, timing overheads, forces and cost reserves are
explicit scenarios, NOT calibrated process data or physical acceptance.
Run from any cwd; standard library, stdout only. E-216 supplies support control.
"""
from functools import lru_cache
from pathlib import Path
import importlib.util
import itertools
import json
import math

spec = importlib.util.spec_from_file_location('e216', Path(__file__).resolve().parents[1]/'E-216'/'screen.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
move = base.move
PITCH, WIDTH, THROW, VALUES = 5.08, 2., 2., 160


def binary(initial, target, fault=None):
    """Three retained 0/1 stops of 3/6/12 mm plus a common closing stroke.
    No programming while head controls load. Proof precedes use. This is an
    ideal contact/state sequence, not a finite CAD or detent realization.
    """
    assert 0 <= initial <= 5 and 0 <= target <= 5
    output, bits, keeper = initial, [(initial >> k) & 1 for k in range(3)], True
    events = ['comb_seated', 'head_unloaded']
    keeper = False
    output = 0  # common stripper resets output; real return stroke charged
    events.append('strip_output')
    bits[:] = [0, 0, 0]  # physical common reset cam, not initial free memory
    events.append('erase_bits')
    for k in range(3):
        bits[k] = (target >> k) & 1
        events.append('write_and_retain_bit')
    if fault == 'stuck_bit': bits[0] ^= 1
    read = sum(b << k for k, b in enumerate(bits))
    assert read == target, 'bit readback stops before transfer'
    assert read < 6, 'illegal stop code'
    events.append('read_bits')
    # Collapsed compression stack chooses 3*code mm, common bar supplies work.
    output = sum(b * 2**k for k, b in enumerate(bits))
    events.append('common_close_to_stop')
    keeper = fault != 'keeper'
    if fault == 'wrong_stop': output = (output+1) % 6
    assert keeper and output == target, 'output proof stops before transfer'
    events += ['close_keeper', 'read_output', 'ready']
    return output, events


def commutated(initial, target, fault=None):
    """Common reset cam, five spatially staggered binary-controlled cam tracks.
    Track k sets the retained slider directly to 3*k mm; all others bypass.
    Gate commands are supplied online for the actual visiting carrier identity.
    """
    assert 0 <= initial <= 5 and 0 <= target <= 5
    value, retained = 0, True  # reset ramp + endpoint keeper precede tracks
    events = ['comb_seated', 'head_unloaded', 'reset_cam', 'read_zero']
    gates = [target == k for k in range(1, 6)]
    if fault == 'stuck_gate': gates[0] = not gates[0]
    for k, selected in enumerate(gates, 1):
        # Gate proof also detects extra contacts that a final read could hide.
        assert selected == (target == k), 'gate proof stops before transfer'
        events.append('select_track' if selected else 'bypass_track')
        if selected:
            assert value == 0
            value = k
        retained = fault != 'retention'
        assert retained, 'retention loss stops before transfer'
    if fault == 'wrong_read': value = (value+1) % 6
    assert value == target, 'final slider proof stops before transfer'
    events += ['read_output', 'retract_tracks', 'return_scan', 'ready']
    return value, events


def writer(kind, streams, accel, follower_accel, width=WIDTH, speed_fraction=.8):
    """Even streams split old/target arrays into equal external scan segments.
    Moving writer crossbars reset/write/read stationary reusable media. Each
    stream has n=160/streams sites on 5.08-mm pitch. No buffer or overlap credit.
    Cam shoes retract for return. Nonselective reset spans can exceed pitch;
    selective contact width cannot consume the next carrier's gate-update time.
    """
    assert streams % 2 == 0 and VALUES % streams == 0 and 0 < width < PITCH
    n = VALUES // streams
    tracks, follower_throw, reset_length = (3, 2., 4.) if kind == 'binary' else (5, 15., 30.)
    # Binary's three bit planes are read/written simultaneously, so one pitch.
    spatial_stations = 1 if kind == 'binary' else 5
    gate_time = move(THROW, accel) + .001  # includes assumed endpoint proof
    v_gate = (PITCH-width)/gate_time
    v_cam = width*math.sqrt(follower_accel/(2*math.pi*follower_throw))
    speed = speed_fraction*min(200., v_gate, v_cam)
    active_length = (n-1)*PITCH + reset_length + spatial_stations*PITCH + PITCH
    # Constant-speed contact span, acceleration/deceleration outside that span.
    stroke = active_length + speed*speed/accel
    scan = active_length/speed + 2*speed/accel
    back = move(stroke, accel)
    shoe = 2*move(2., accel)  # retract before return, restore before next scan
    common = 2*move(15., accel)+.005 if kind == 'binary' else 0.
    # 5-ms terminal read plus head-wide clamp proof; channel count is streams.
    t = scan+back+shoe+common+.010
    return dict(seconds=t, speed=speed, stroke=stroke,
                gate_channels=tracks*streams, reader_channels=streams,
                gate_duty_margin=(PITCH-width)/speed-gate_time,
                follower_peak_accel=2*math.pi*follower_throw*(speed/width)**2)


@lru_cache(maxsize=None)
def service_row(old, target, accel, auxiliary=.5):
    r = base.replay(old, target)
    if old == target: return 0.
    return (sum(move(y-x, accel) for x,y in zip(r['path'],r['path'][1:]))
            + (len(r['path'])-1)*.020+auxiliary+move(PITCH, accel))


def schedule(kind, banks, streams, accel, follower_accel, old=None, target=None,
             auxiliary=.5, width=WIDTH, speed_fraction=.8):
    if old is None: old, target = base.workloads()
    w = writer(kind, streams, accel, follower_accel, width, speed_fraction)
    ts = [0. if x == y else w['seconds']+service_row(tuple(x),tuple(y),accel,auxiliary)
          for x,y in zip(old,target)]
    span = 80//banks
    loads = [sum(ts[i:i+span]) for i in range(0,80,span)]
    return 2.+max(loads)+max(ts), w  # map overhead + one worst-row full rewrite/retry


def checks():
    base.checks()
    for fn in (binary, commutated):
        for initial, target in itertools.product(range(6), repeat=2):
            out, events = fn(initial, target)
            assert out == target and events[-1] == 'ready'
    for fn, faults in ((binary, ('stuck_bit','keeper','wrong_stop')),
                       (commutated, ('stuck_gate','retention','wrong_read'))):
        for fault in faults:
            try: fn(5, 2, fault)
            except AssertionError: pass
            else: raise AssertionError('undetected injected fault '+fault)
    old,target = base.workloads()
    # Physical commands include BYPASS=5 for unchanged old heights.
    for fn in (binary, commutated):
        for before, after in zip(old,target):
            commands = [5 if x==y else x//10 for x,y in zip(before,after)]
            commands += [y//10 for y in after]
            assert len(commands)==VALUES
            for i,t in enumerate(commands): assert fn(i%6, int(t))[0] == t
    # Independent rate bound: rows consume new words, no preloaded buffer credit.
    assert 80*160 == 12800 and 3*80*160 == 38400
    for kind in ('binary','commutated'):
        w=writer(kind,8,2000,20000)
        assert w['seconds'] > (160/8-1)*PITCH/w['speed']
        assert w['follower_peak_accel'] <= 20000*(1+1e-12)
        assert w['gate_duty_margin'] >= -1e-12
    # Smooth-cam acceleration bound cross-check by finite differencing velocity.
    d, duration = 15., .2
    expected = 2*math.pi*d/duration**2
    errors=[]
    for samples in (100,200,400):
        dt=duration/samples
        vel=[d/duration*(1-math.cos(2*math.pi*i/samples)) for i in range(samples+1)]
        peak=max(abs(b-a)/dt for a,b in zip(vel,vel[1:]))
        errors.append(abs(peak/expected-1))
    assert errors[2] < errors[1] < errors[0] and errors[2] < .00005


def main():
    checks()
    rows=[]
    for kind,b,a,fa in itertools.product(('binary','commutated'),(1,2,4,8,16),
                                        (2000,8000),(20000,100000)):
        for streams in (2,4,8,16,20,40,80,160):
            total,w=schedule(kind,b,streams,a,fa)
            if total < 30.:
                rows.append(dict(kind=kind,banks=b,accel=a,follower_accel=fa,
                    streams=streams,channels=b*w['gate_channels'],time=round(total,3),
                    speed=round(w['speed'],3),stroke=round(w['stroke'],3),
                    readers=b*w['reader_channels'],
                    allowance_per_gate=round(250/(b*w['gate_channels']),3)))
                break
    selected={}
    for kind in ('binary','commutated'):
        selected[kind]={str((b,s,a,fa)):round(schedule(kind,b,s,a,fa)[0],3)
            for b,s,a,fa in ((8,2,2000,20000),(8,8,8000,100000),
                            (8,16,8000,100000),(16,8,8000,100000))}
    flat=[[0]*80 for _ in range(80)]; patch=[r[:] for r in flat]
    for r in range(5):
        for c in range(5): patch[r][c]=10*(1+c%4)
    print(json.dumps(dict(evidence='assumed bounds, calculations and ideal logical replay only',
        checks='72 code overwrites; 6 fault refusals; 25600 full-map media values; E-216 support checks; cam convergence',
        smallest_sampled_stream_survivors=rows, selected_times=selected,
        width_sensitivity={str(w):round(schedule('commutated',8,16,8000,100000,width=w)[0],3) for w in (1,2,3,4)},
        auxiliary_sensitivity={str(x):round(schedule('binary',8,16,8000,100000,auxiliary=x)[0],3) for x in (.25,.5,1,2)},
        regional_5x5={k:round(schedule(k,8,16,8000,100000,flat,patch)[0],3) for k in ('binary','commutated')},
        controls={str((b,q,a)):round(base.schedule(*base.workloads(),b,q,a),3) for b,q,a in ((8,1,2000),(8,40,8000),(16,16,8000))},
        force_per_stream_peak_N={str(f):{'binary':3*2*f*2/WIDTH,
            'commutated':sum(2*f*(3*k)/WIDTH for k in range(1,6))+2*f*15/30,
            'binary_common_min_160':160*f} for f in (.3,1,3)},
        error_margin_mm={str(e):{'bit_half_clearance':.5-e,'level_half_spacing':1.5-e} for e in (.15,.35,.70)},
        speed_fraction_sensitivity={str(f):round(schedule('commutated',16,8,8000,100000,speed_fraction=f)[0],3) for f in (.6,.8,1)},
        binary_pusher_peak_N={str(k):160*(.3+15*k) for k in (.02,.06,.18)},
        head_counts={str(b):{'grips':160*b,'binary_bits':480*b,'output_sliders':160*b,
                            'binary_compliant_pushers':160*b} for b in (8,16)},
    ),indent=2))

if __name__=='__main__': main()
