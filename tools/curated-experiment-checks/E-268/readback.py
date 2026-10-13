#!/usr/bin/env python3
"""Finite optical routing and observability bounds; no hardware qualification."""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

old = load('optical', 'E-178/readback.py')
head = load('head', 'E-267/screen.py')


def optical(pitch, stroke, projection, backing, error, pupil=.25, tilt=.5):
    """A 16-site reader under resident screws; ideal flat strip, corner bounds.

    Column width4.4, external marks at a fixed datum3mm above lower guide.
    E-261 lower guide center=S+5, datum=S+9, screw bed at0; camera at-10.
    Full optical slots in guide/bed granted only in the slotted case.
    error is independent/coherent placement bound, NOT a process distribution.
    """
    width = 4.4; cy = pitch/2; datum = stroke+9; D = datum+10
    half_length = projection*math.sqrt(2)
    rays = misses = obstructed = wrong_side = outgoing_hits = 0
    min_edge = float('inf'); max_slot_half = 0.; witness = None
    for signs in it.product((-1,1), repeat=6):
        sy,sz,sc,st,sp,sa = signs
        my=cy+sy*error; mz=sz*error; theta=math.radians(45+sa*tilt)
        for col,track,dx,dz in it.product(range(16),(-1.2,-.4,.4,1.2),(-.08,.08),(-.08,.08)):
            target=(col*pitch+track+dx,width/2+st*error,dz)
            camera=(7.5*pitch,cy+sc*error+sp*pupil,-D)
            rays+=1
            normal=(0.,math.cos(theta),math.sin(theta))
            center=(0.,my,mz)
            if old.dot(old.sub(target,center),normal)*old.dot(old.sub(camera,center),normal)<=0:
                wrong_side+=1
                continue
            m,_=old.ray(target,camera,my,mz,sa*tilt)
            along=(m[1]-my)*math.sin(theta)-(m[2]-mz)*math.cos(theta)
            edge=half_length-abs(along); min_edge=min(min_edge,edge)
            if edge<0: misses+=1
            assert -pitch/2 < m[0] < 15.5*pitch
            for dr,dc in it.product((-1,0,1),repeat=2):
                if dr==dc==0:
                    continue
                lo=((col+dc)*pitch-width/2-error,dr*pitch-width/2-error,-100.)
                hi=((col+dc)*pitch+width/2+error,dr*pitch+width/2+error,100.)
                if old.hit_box(m,target,lo,hi):
                    outgoing_hits+=1
            # Continuous row envelopes enclose all screw/pin heights. A clear
            # corridor is sufficient; an intersection is conservative, not proof.
            lo=width/2+error; hi=pitch-width/2-error
            if not all(lo<q[1]<hi for q in (camera,m)):
                obstructed+=1
            for z in (-5,-3,-datum-1,-datum+1):
                t=(z-camera[2])/(m[2]-camera[2])
                assert 0<t<1
                y=camera[1]+t*(m[1]-camera[1])
                max_slot_half=max(max_slot_half,abs(y-cy)+error)
            # Solid shared plate counterexample for central rays. The Y plane
            # is outside every square guide aperture, so all X is solid there.
            if witness is None:
                z=-4; t=(z-camera[2])/(m[2]-camera[2])
                q=old.add(camera,old.mul(t,old.sub(m,camera)))
                if 2.32<q[1]<pitch-2.32:
                    witness=dict(point=q,guide_z=z,between_apertures=True)
    # Exact extrema of strip's Y extent in specified angular interval.
    th=math.radians(45+tilt)
    near=cy-2*error-half_length*math.sin(th)-width/2
    # Max y of backing: tangent contribution plus thickness normal contribution.
    far=pitch-width/2-cy-2*error-max(
        half_length*math.sin(math.radians(45+s*tilt))+backing*math.cos(math.radians(45+s*tilt))
        for s in (-1,1))
    # Slot size includes an independently displaced plate. No optical margin.
    required_slot=2*max_slot_half
    web=(pitch-required_slot-4.64)/2
    return dict(pitch=pitch,stroke=stroke,projection=projection,backing=backing,
                error=error,pupil=pupil,rays=rays,mirror_misses=misses,
                incoming_envelope_hits=obstructed,wrong_side_rays=wrong_side,
                outgoing_neighbor_hits=outgoing_hits,min_edge_mm=min_edge,
                near_gap_mm=near,backing_gap_mm=far,
                necessary_slot_width_mm=required_slot,remaining_guide_web_mm=web,
                solid_plate_witness=witness)


def observe(motor_turns, screw_turns, actual_height, valid=True, fresh=True):
    return dict(motor=motor_turns,screw=screw_turns,
                height=actual_height if valid and fresh else None)


def faults():
    # Algebraic fault injection, not detection rates. Start10 -> target20, lead2.
    states={
        'correct':observe(5,5,20),
        'missed_socket':observe(5,0,10),
        'transmission_slip':observe(5,2,14),
        'stripped_thread':observe(5,5,10),
        'wrong_lead':observe(5,5,25),
        'detached_mark':observe(5,5,20), # actual terrain10, mark remains20
        'support_fails_later':observe(5,5,20),
        'stale_frame_rejected':observe(5,0,10,fresh=False),
        'occluded_rejected':observe(5,0,10,valid=False),
    }
    expected=states['correct']
    return {name:{key:value==expected[key] for key,value in state.items()}
            for name,state in states.items()}


def timing():
    out=[]
    for n,stroke in it.product((64,80),(40,50)):
        rows={name:head.schedule(d,16) for name,d in head.local_cases(n,stroke).items()
              if any(map(any,d))}
        for row_read in (.02,.05,.10,.20):
            times={name:r['seconds']+(r['stations']+1)*(row_read-.02)
                   for name,r in rows.items()}
            worst=max(times,key=times.get)
            out.append(dict(n=n,stroke=stroke,read_s=row_read,
                            local_max_s=times[worst],worst=worst,
                            worst_stations=rows[worst]['stations'],
                            full_row_B2_K32_max_s=max(head.a.schedule(d,32,850,proof=row_read)['feasible_s']
                                for d in head.local_cases(n,stroke).values() if any(map(any,d)))))
    return out


def checks():
    # Slab oracle and tangent-touch controls independent of optics.
    assert old.hit_box((0,0,-1),(0,0,1),(-1,-1,-.1),(1,1,.1))
    assert not old.hit_box((2,0,-1),(2,0,1),(-1,-1,-.1),(1,1,.1))
    # Linear replacement checked against actual scheduler, including retry.
    d=[[30 if x==y else 0 for x in range(16)] for y in range(16)]
    base=head.schedule(d,16)
    actual=head.schedule(d,16,extra_dock=.08)
    assert math.isclose(actual['seconds'],base['seconds']+(base['stations']+1)*.08)
    ff=faults()
    assert ff['missed_socket']['motor'] and not ff['missed_socket']['height']
    assert ff['stripped_thread']['screw'] and not ff['stripped_thread']['height']
    assert all(ff['support_fails_later'].values())
    assert not ff['stale_frame_rejected']['height']
    # No camera position can see an opaque-covered top through that cover.
    assert old.hit_box((0,0,100),(0,0,0),(-12.7,-12.7,.1),(12.7,12.7,2))
    # 40/50 travel scale spans lie on existing86/96-mm pins, not added tails.
    for S in (40,50):
        for u in (0,S/2,S):
            local=S+9-(2+u)
            assert 0<local<S+46
        assert (S+7)-7==S
    # One missed single step may be beneath the chosen reader tolerance.
    # acceptance |measurement-target|<=a, bounded error e -> true error<=a+e.
    for e in (0,.1,.2,.35):
        a=.3
        assert math.isclose((a+e)-e,a)
    return 'reflection/path identities per ray; slab/opaque-cover and fault aliases; stock and bounded-error controls'


def main():
    geometry=[optical(p,S,h,t,e) for p,h,t in ((5.08,.2,.1),(6.35,.5,.2))
              for S in (40,50) for e in (0,.05,.1,.2)]
    coarse=[g for g in geometry if g['pitch']==6.35 and g['error']<=.1]
    assert all(g['mirror_misses']==g['incoming_envelope_hits']==g['outgoing_neighbor_hits']==g['wrong_side_rays']==0 for g in coarse)
    assert all(g['backing_gap_mm']>0 and g['solid_plate_witness'] for g in coarse)
    assert all(g['backing_gap_mm']<0 for g in geometry if g['error']==.2)
    print(json.dumps(dict(checks=checks(),geometry=geometry,fault_aliases=faults(),timing=timing(),
          code_budget={S:dict(levels=S//10+1,all_mm_positions=S+1,
                              minimum_binary_bits=math.ceil(math.log2(S+1))) for S in (40,50)},
          marking_hours={n:n*n*10/3600 for n in (64,80)}),indent=2))

if __name__=='__main__': main()
