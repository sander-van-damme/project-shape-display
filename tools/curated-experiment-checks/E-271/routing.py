#!/usr/bin/env python3
"""Finite 16-output packaging and itemized allocation screen, not CAD or BOM.

mm, USD; deterministic bounding boxes. All non-catalog geometry/costs are
explicit design allocations. No probabilities, torque, safe RPM or optical proof.
"""
import argparse
import itertools
import json
import math
from pathlib import Path
import importlib.util

CATALOG = {
    'encoder_motor': (29.85, 32.45),  # Pololu 5180: qty16 / qty1
    'encoder_cable': (2.76, 3.00),   # Pololu 4763
    'bare_motor': (1.76, 1.95),     # Adafruit 711
    'dual_bridge': (5.95, 5.95),    # Adafruit 3297, qty8 / qty1
    'solenoid': (4.46, 4.95),       # Adafruit 2776
}


def box(i, name, x0, x1, y0, y1, z0, z1):
    assert x0 < x1 and y0 < y1 and z0 < z1
    return dict(channel=i, name=name, lo=(x0,y0,z0), hi=(x1,y1,z1))


def gap(a,b):
    # Positive iff separated on at least one axis; L-infinity envelope margin.
    return max(max(a['lo'][k]-b['hi'][k],b['lo'][k]-a['hi'][k]) for k in range(3))


def conflicts(parts,e):
    return [(a['channel'],a['name'],b['channel'],b['name'],round(gap(a,b)-2*e,6))
            for a,b in itertools.combinations(parts,2)
            if a['channel'] != b['channel'] and gap(a,b) < 2*e+.05-1e-9]


def offset(p,route,lanes,diameter=6):
    """Whole-channel Z translation 0..3: union boxes covers every subset/state.

    Motors farther in Y have higher transmission decks. This order keeps belts
    above nearer motors; output shafts still cross every higher deck explicitly.
    Envelopes include bearing carriers, a narrow cantilever, selector/slide and
    cable exit. Internal fits/interfaces within a channel are NOT validated.
    """
    parts=[]; width=20 if route=='encoder' else 25
    for i in range(16):
        x=i*p; lane=i%lanes; y=30+30*lane; z=-30-12*(lanes-1-lane)
        add=lambda name,*v: parts.append(box(i,name,*v))
        # Finite catalog motor included in a larger slide/selector cartridge.
        # Encoder conservatively <=16x16x33; bare <=15x20x27.5, shafts 3x9 / 2x8.
        add('motor_slide_selector',x-width/2,x+width/2,y-12,y+12,z-94,z-5)
        add('motor_shaft',x-1.5,x+1.5,y-1.5,y+1.5,z-8,z+4)
        add('belt_pulleys',x-diameter/2,x+diameter/2,-diameter/2,y+diameter/2,z-1,z+4)
        add('output_shaft',x-1,x+1,-1,1,z-5,-1+3)
        add('tip',x-1.5,x+1.5,-1.5,1.5,-4,2)
        add('bearing_riser',x-2.2,x+2.2,-2.2,2.2,z-8,-5)
        for b in (-10,z-6):
            add('bearing_carrier',x-2.2,x+2.2,-2.2,2.2,b-2,b+2+3)
        add('moving_beam',x-2.2,x+2.2,-2.2,y,z-8,z-6+3)
        bottom=-30-12*(lanes-1)-110
        add('cable_drop',x-1.5,x+1.5,y-2,y+2,bottom,z-90)
        add('cable_comb_lane',x-1.5,x+1.5,y,30*lanes+25,bottom-4,bottom)
    return parts


def coax(p,route,lanes):
    parts=[]; width=10.5 if route=='encoder' else 15
    for i in range(16):
        x=i*p; z=-30-45*(i%lanes)
        parts += [box(i,'body',x-width/2,x+width/2,-8,8,z-33,z),
                  box(i,'long_output',x-1,x+1,-1,1,z,-1)]
    return parts


def screen(p,route,e=.2,diameter=6):
    tried=[]; selected=None
    for lanes in range(1,9):
        parts=offset(p,route,lanes,diameter)
        bad=conflicts(parts,e)
        tried.append(dict(lanes=lanes,conflicts=len(bad),first=bad[:1]))
        if not bad:
            selected=(lanes,parts); break
    result=dict(pitch=p,route=route,error_bound_each_mm=e,attempts=tried)
    if selected:
        lanes,parts=selected
        lo=[min(v['lo'][k] for v in parts) for k in range(3)]
        hi=[max(v['hi'][k] for v in parts) for k in range(3)]
        # Shared driver tray (8x26x18 boards in a4x2 array with pitch30x24),
        # controllers/connectors another30mm Y, and edge posts outside moving X.
        xwidth=max(120,hi[0]-lo[0]+12)
        ydepth=30*lanes+95
        depth=-lo[2]+20
        result.update(lanes=lanes,boxes=len(parts),minimum_separation_mm=min(
            gap(a,b)-2*e for a,b in itertools.combinations(parts,2) if a['channel']!=b['channel']),
            head_envelope_mm=[xwidth,ydepth,depth],
            machine_swept_envelope_mm=[406.4-15*p+xwidth,406.4+ydepth,depth],
            longest_output_shaft_mm=34+12*(lanes-1),
            coax_conflicts=len(conflicts(coax(p,route,lanes),e)))
    # Full resident plane begins at0, except intended socket engagements.
    result['parked_axial_gap_mm']=1-2*e
    result['engaged_depth_mm']=2-2*e
    result['unselected_neighbor_radial_gap_mm']=p-1.5-2.2-2*e
    result['docking_envelope_clear']=min(1-2*e,1-2*e,p-3.7-2*e)>0
    return result


def ledger(n,route,k=16):
    idx=0 if k==16 else 1
    cat={'motors': k*CATALOG[route+'_motor'][idx],
         'dual_bridges':math.ceil(k/2)*CATALOG['dual_bridge'][idx],
         'docking_solenoids':k*CATALOG['solenoid'][idx]}
    if route=='encoder': cat['encoder_cables']=k*CATALOG['encoder_cable'][idx]
    # Each entry: quantity, low/unit, high/unit. Bounds, not quotations.
    allocation={
        'shaft_tip_two_bushings':(k,2.5,7),
        'slide_two_guides_stops_return_mount':(k,3,8),
        'solenoid_MOSFET_flyback':(k,1,2),
        'harness_connectors_strain_relief':(k,1,3),
        'two_dock_state_switches':(k,2,4),
        'head_precision_plates_and_jig':(1,120 if k==16 else 30,300 if k==16 else 80),
        'head_power_distribution_and_capture':(1,40 if k==16 else 15,100 if k==16 else 40),
        'XY_guides_belts_position_motors_limits':(1,120,240),
        'chassis_enclosure_service_fasteners':(1,35,75),
        'power_protection_cooling':(1,80 if k==16 else 30,150 if k==16 else 60),
        'controller':(1,35,70),
        'resident_beds_keepers_guides_ribs':(n*n,.02,.08),
        'actual_cap_reader_lighting_references':(1,80,250),
        'reader_mount_or_carrier':(1,80,180),
    }
    if k==16: allocation['two_pulleys_belt_tensioner']=(k,4,12)
    if route=='bare': allocation['output_or_motor_encoder_and_attachment']=(k,5,15)
    pre=[sum(cat.values())+sum(q*v[t] for q,*v in allocation.values()) for t in (0,1)]
    bought=[pre[0]*1.10+20,pre[1]*1.15+60]  # explicit landed allowances
    # Material/process allowance is separate from bought hardware target.
    material=[60,160]
    # Resident8s is E-260 illustrative handling, not fitted manufacturing data.
    hours=[8+n*n*8/3600+k*10/60,16+n*n*20/3600+k*30/60]
    return dict(n=n,route=route,outputs=k,catalog_USD=cat,allocation_q_low_high=allocation,
        pre_tax_shipping_USD=pre,bought_with_landed_allowance_USD=bought,
        remaining_at_tiers={b:[b-c for c in bought] for b in (500,1000,1500)},
        printing_material_USD=material,maker_hours=hours,
        all_in_at_20_USD_per_hour=[bought[j]+material[j]+20*hours[j] for j in (0,1)],
        solenoid_A=1.1*k,solenoid_W=5.5*k,
        resident_pairs=n*n,resident_guide_apertures=2*n*n,
        shared_bushings=2*k,dock_state_switches=2*k,
        motor_encoder_is_cap_proof=False)


def checks():
    assert gap(box(0,'a',0,1,0,1,0,1),box(1,'b',2,3,0,1,0,1))==1
    for p,route in itertools.product((6.35,5.08),('encoder','bare')):
        r=screen(p,route)
        if p==6.35:
            assert 'lanes' in r and r['coax_conflicts']>0
            assert r['minimum_separation_mm']>=.05-1e-9 and r['docking_envelope_clear']
            assert r['attempts'][-1]['conflicts']==0
            parts=offset(p,route,r['lanes'])
            assert all(v['hi'][2] < 0 for v in parts
                       if v['name'] not in ('output_shaft','tip'))
        else:
            assert 'lanes' not in r # beam/belt swept volumes intersect
        # Enlarged pulley makes adjacent shaft intersections; more lanes cannot fix.
        assert 'lanes' not in screen(p,route,diameter=12)
        # Expanded deck sweep creates inter-channel crossings on this finite route.
        bad=offset(p,route,r.get('lanes',5))
        for v in bad:
            if v['name']=='belt_pulleys':
                v['lo']=(v['lo'][0],v['lo'][1],-140)
                v['hi']=(v['hi'][0],v['hi'][1],-20)
        assert conflicts(bad,.2)
    assert 'lanes' not in screen(5.08,'encoder',e=.4) # bearing carriers
    assert not screen(6.35,'encoder',e=.6)['docking_envelope_clear']
    for n,route,k in itertools.product((64,80),('encoder','bare'),(1,16)):
        c=ledger(n,route,k)
        for budget,res in c['remaining_at_tiers'].items():
            for j in (0,1): assert math.isclose(res[j]+c['bought_with_landed_allowance_USD'][j],budget)
        assert c['maker_hours'][1]>c['maker_hours'][0]
    # No velocity is inferred from catalog no-load speed or packing.
    return 'finite collision/failure witnesses, uncertainty limits, ledger identities passed'


def slower():
    spec=importlib.util.spec_from_file_location('short',Path(__file__).resolve().parents[1]/'E-267/screen.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    rows=[]
    for n in (64,80):
        # One encoder spindle at400rpm, lead3; optimistic actual-cap transaction
        # added .28s/station to old .1s, never an implemented decoder.
        def paid(d):
            q=m.schedule(d,1,rpm=400,extra_dock=.28)
            if not q['stations']: return 0.
            return q['seconds']-q['retry_s']+.38+m.a.r.spin(50/3,400)+1
        local=max(paid(d) for d in m.local_cases(n,50).values())
        dense=paid([[50]*n for _ in range(n)])
        prep=paid([[30]*n for _ in range(n)])
        rows.append(dict(n=n,assumed_rpm=400,local_max_s=local,
                         dense_s=dense,neutral_prep_s=prep))
    return rows


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--slower',action='store_true')
    args=parser.parse_args()
    verified=checks()
    if args.check: print(verified)
    else: print(json.dumps(dict(verification=verified,
        layouts=[screen(p,r,e) for p,r,e in itertools.product((6.35,5.08),('encoder','bare'),(.1,.2,.4))],
        ledgers=[ledger(n,r,k) for n,r,k in itertools.product((64,80),('encoder','bare'),(16,1))],
        slower_comparator=slower() if args.slower else 'use --slower'),indent=2))
