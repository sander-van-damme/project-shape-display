"""Deterministic analytical screens, Python 3.11+ stdlib; mm, s, N, USD.

No dynamics/contact solver and no measured mechanical pass. Test08 is imported
only for an explicitly labelled cross-check and its unchanged mass calculation.
"""
from pathlib import Path
import csv
import hashlib
import importlib.util
import itertools
import json
import math

HERE = Path(__file__).resolve().parent
OUT = HERE / 'results'


def save(name, data):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def table(name, rows):
    OUT.mkdir(exist_ok=True)
    with (OUT / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def cad_parameters(p):
    """Share detent/structural dimensions with the coupon source."""
    OUT.mkdir(exist_ok=True)
    vals={f'detent_{k}':v for k,v in p['detent'].items()}
    vals.update({k:p['structure'][k] for k in ['beam_width_mm','beam_height_mm','beam_wall_mm']})
    vals['cell_pitch_mm']=p['grid']['pitch_mm']
    vals['cam_levels']=p['grid']['levels']
    (OUT/'coupon_parameters.scad').write_text('\n'.join(f'{k}={v};' for k,v in vals.items())+'\n',encoding='utf-8')


def travel(d, v, a):
    if d < 0 or v <= 0 or a <= 0:
        raise ValueError('invalid motion')
    # Independent derivation: accelerate half distance unless speed limited.
    peak = min(v, math.sqrt(d*a))
    return 2*peak/a + (d-peak*peak/a)/v


def schedule(p, targets, detail=False):
    g, m = p['grid'], p['timing']
    if len(targets) != g['rows'] or any(len(r) != g['columns'] for r in targets):
        raise ValueError('map shape')
    if any(type(k) is not int or not 0 <= k < g['levels'] for r in targets for k in r):
        raise ValueError('map level')
    step = 360/g['levels']/m['step_deg']
    if abs(step-round(step)) > 1e-9:
        raise ValueError('levels require a different motor or fractional-step validation')
    if m['rate_hz'] <= 0 or m['home_steps']*m['step_deg'] < 360:
        raise ValueError('motor rate or incomplete homing')
    if any(v < 0 for k, v in m.items() if k.endswith('_s')):
        raise ValueError('negative duration')
    events = []
    def add(kind, duration, row=None):
        events.append({'kind': kind, 'duration_s': duration, 'row': row})
    add('reference_reset_command', m['reference_s'])
    lift = travel(g['travel_mm']+m['clearance_mm'], m['lift_v_mm_s'], m['lift_a_mm_s2'])
    add('raise_unload_all', lift)
    for row, values in enumerate(targets):
        add('index', travel(g['pitch_mm'] if row else 0, m['scan_v_mm_s'], m['scan_a_mm_s2']), row)
        for kind, dt in [('command',m['command_s']), ('engage',m['engage_s']),
                         ('home',m['home_steps']/m['rate_hz']), ('home_settle',m['home_settle_s']),
                         ('program',max(values)*step/m['rate_hz']), ('write_settle',m['write_settle_s']),
                         ('disengage',m['disengage_s']), ('detent_seat',m['seat_s'])]:
            add(kind, dt, row)
    add('park', travel((g['rows']-1)*g['pitch_mm'],m['scan_v_mm_s'],m['scan_a_mm_s2']))
    add('lower_gravity_return', lift)
    add('final_settle', m['ready_s'])
    add('inspect',m['inspection_s'])
    add('recovery',m['recovery_s'])
    elapsed = 0
    for e in events:
        e['start_s'] = elapsed
        elapsed += e['duration_s']
    result = {'time_s':elapsed, 'cells_commanded':g['rows']*g['columns'],
              'mechanical_status':'unverified', 'timing_basis':'calculated conditional fault-free schedule'}
    if detail:
        result['events'] = events
    return result


def maps(p):
    g = p['grid']; n, c, hi = g['rows'],g['columns'],g['levels']-1
    return {'low':[[0]*c for _ in range(n)], 'high':[[hi]*c for _ in range(n)],
            'checker':[[hi*((x+y)%2) for x in range(c)] for y in range(n)],
            'inverse_checker':[[hi*(1-(x+y)%2) for x in range(c)] for y in range(n)],
            'one_high_per_row':[[hi if x == y%c else 0 for x in range(c)] for y in range(n)],
            'alternating_rows':[[hi*(y%2)]*c for y in range(n)]}


def old_module():
    spec = importlib.util.spec_from_file_location('test08_reference',HERE.parent/'test08_architecture_search'/'analysis.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def geometry(p, old, op):
    c = op['cam']; toe = math.degrees(math.atan2(c['toe_width_mm']/2,c['toe_x_mm']-c['center_x_mm']))
    levels = []
    for k in [3,4,5,6,8,9,10]:
        # Nearest full step; ideal detent must correct quantization too.
        step=p['timing']['step_deg']
        err = max(abs(j*360/k-round(j*360/k/step)*step) for j in range(k))
        levels.append(dict(levels=k,increment_mm=p['grid']['travel_mm']/(k-1),half_sector_deg=180/k,
                           toe_envelope_deg=toe,nominal_margin_deg=180/k-toe,
                           nearest_full_step_error_deg=err,
                           margin_after_6deg_seating_deg=180/k-toe-6,
                           direct_full_steps=abs(360/step/k-round(360/step/k))<1e-9))
    table('levels.csv',levels)
    fits=[]
    for width, clear, error, tilt in itertools.product([4.48,4.68],[.05,.1,.15,.2],[0,.05,.1],[0,.1,.25,.5]):
        fits.append(dict(body_mm=width,clearance_per_side_mm=clear,combined_size_error_mm=error,
                         tilt_deg=tilt,web_mm=5.08-width-2*clear,
                         free_clearance_across_12mm_guides_mm=2*clear-error-12*math.tan(math.radians(tilt))))
    table('fit_sensitivity.csv',fits)
    variants={}
    for hollow in [0,1]:
        q=json.loads(json.dumps(op));q['grid']['body_hollow']=hollow
        geo=old.geometry(q)
        variants['hollow' if hollow else 'solid']={'calculated_mass_g':geo['column_mass_g'],
            'drag_gate_mn':geo['column_mass_g']*9.81*.5, 'measured_mass_g':None,'measured_drag_mn':None}
    return {'mass':variants,'test08_notch_point_follower_capture_half_deg':math.degrees(math.asin(.25/1.65)),
            'neighbor_rigid_cell_envelope_gap_mm':op['grid']['pitch_mm']-2*max(2.50,op['grid']['body_width_mm']/2,abs(c['center_x_mm'])+1.65),
            'neighbor_bound_scope':'Conservative +/-2.50 mm XY boxes of original individual parts; arbitrary heights/rotations. Excludes shared guide plates, new detent, retention and deformation.',
            'test08_geometry':old.geometry(op)}


def detent(p):
    d=p['detent']; records=[]
    for E in p['material']['modulus_mpa']:
        stiffness=E*d['width_mm']*d['thickness_mm']**3/(4*d['length_mm']**3)
        for deg in range(-36,37):
            theta=math.radians(deg); k=p['grid']['levels']
            delta=d['preload_mm']+d['depth_mm']/2*(1-math.cos(k*theta))
            force=stiffness*delta
            # Energy gradient F * dr/dtheta; N mm equals mN m.
            torque=-force*d['depth_mm']/2*k*math.sin(k*theta)
            records.append(dict(E_assumed_mpa=E,angle_deg=deg,force_n=force,restoring_torque_mnm=torque,
                                surface_strain=1.5*d['thickness_mm']*delta/d['length_mm']**2))
    table('detent_torque.csv',records)
    return {'basis':'calculated frictionless small-deflection leaf; not capture validation',
            'peak_restoring_mnm_at_1500mpa':max(abs(r['restoring_torque_mnm']) for r in records if r['E_assumed_mpa']==1500),
            'disturbance_mnm_1N_1deg_plateau_slope_at_1p35mm':1.35*math.tan(math.radians(1)),
            'ideal_basin_half_deg':36,'measured_capture_deg':None}


def structures(p,mass_g):
    s=p['structure']; rows=[]; cells=p['grid']['rows']*p['grid']['columns']
    I=(s['beam_width_mm']*s['beam_height_mm']**3-(s['beam_width_mm']-2*s['beam_wall_mm'])*(s['beam_height_mm']-2*s['beam_wall_mm'])**3)/12
    for platen,drag,E,span in itertools.product(s['platen_kg'],s['drag_n_per_cell'],p['material']['modulus_mpa'],s['span_mm']):
        mass=cells*mass_g/1000+platen; force=mass*(9.81+p['timing']['lift_a_mm_s2']/1000)+cells*drag
        w=force/(s['beams']*p['grid']['columns']*p['grid']['pitch_mm'])
        rows.append(dict(platen_kg=platen,column_kg=mass-platen,drag_n=drag,force_n=force,E_mpa=E,span_mm=span,
                         beam_I_mm4=I,ideal_beam_deflection_mm=5*w*span**4/(384*E*I),
                         flat_2mm_strip_deflection_mm=5*w*span**4/(384*E*(20*2**3/12))))
    table('structure.csv',rows)
    drives=[]
    for count,lead,eta in itertools.product([4,9,16],s['screw_lead_mm'],s['screw_efficiency']):
        force=max(r['force_n'] for r in rows)
        drives.append(dict(screws=count,lead_mm=lead,efficiency_assumed=eta,force_n=force,
                           total_torque_nm=force*lead/1000/(2*math.pi*eta),
                           worst_screw_torque_nm=2*force/count*lead/1000/(2*math.pi*eta),
                           rpm=p['timing']['lift_v_mm_s']/lead*60,rack_per_10deg_mm=lead*10/360))
    table('lift_drive.csv',drives)


def reliability():
    rows=[]
    for cell,row,module in itertools.product([1e-3,1e-4,1e-5,1e-6],[0,1e-4,1e-3],[0,1e-4,1e-3]):
        rows.append(dict(cell_error=cell,row_event_error=row,module_event_error=module,
                         perfect_map=(1-cell)**6400*(1-row)**80*(1-module)**64,
                         basis='independent cells plus independent correlated group-event model'))
    table('reliability.csv',rows)
    q=-math.expm1(math.log(.99)/6400)
    return {'cell_q_for_99pct_map':q,'zero_failure_trials_95pct':math.ceil(math.log(.05)/math.log1p(-q)),
            'zero_failures_80000_cell_trials_upper_q':-math.expm1(math.log(.05)/80000),
            'zero_failures_10000_row_trials_upper_q':-math.expm1(math.log(.05)/10000),
            'measured_failures':None,'measured_cycles':None}


def multirow(p):
    g,m,s=p['grid'],p['timing'],p['multirow']; rows=[]
    for r,c,v,mode in itertools.product(s['rows'],s['columns'],s['stroke_v_mm_s'],['independent_full_stroke','shared_stroke_local_select']):
        positions=[]
        for group,x in enumerate(range(0,g['columns'],c)):
            ys=list(range(0,g['rows'],r))
            if group%2:ys.reverse()
            positions.extend((x*g['pitch_mm'],y*g['pitch_mm']) for y in ys)
        index=0.; last=(0,0)
        for xy in positions+[(0,0)]:
            index+=travel(math.dist(last,xy),m['scan_v_mm_s'],m['scan_a_mm_s2']);last=xy
        n=r*c; stops=len(positions)
        if mode=='independent_full_stroke':
            tx=2*travel(g['travel_mm'],v,s['stroke_a_mm_s2'])+s['transaction_overhead_s']
            mass=s['head_base_kg']+n*s['direct_kg_per_axis'];act=n;wires=4*n
            costs=[s['base_cost_usd']+n*u for u in s['direct_axis_usd']]
            localstroke=g['travel_mm']
        else:
            # Four upward 10 mm increments; select/release each level, then retract 40 mm.
            increments=g['levels']-1
            tx=increments*(travel(g['travel_mm']/increments,v,s['stroke_a_mm_s2'])+s['selector_s_per_level']+s['settle_s_per_level'])+travel(g['travel_mm'],v,s['stroke_a_mm_s2'])+s['transaction_overhead_s']
            mass=s['head_base_kg']+s['shared_drive_kg']+n*s['selector_kg'];act=n+1;wires=2*n+4
            costs=[s['base_cost_usd']+s['shared_drive_usd']+n*u for u in s['selector_usd']]
            localstroke=1
        rows.append(dict(mode=mode,rows=r,columns=c,stops=stops,actuators=act,wires=wires,
            local_actuator_stroke_mm=localstroke,shared_stroke_mm=g['travel_mm'] if mode=='shared_stroke_local_select' else 0,
            stroke_v_mm_s=v,head_mass_assumed_kg=mass,scan_accel_m_s2=m['scan_a_mm_s2']/1000,
            scan_inertial_force_n=mass*m['scan_a_mm_s2']/1000,index_and_park_s=index,
            allowed_transaction_27_s=(27-s['fixed_s']-index)/stops,
            allowed_transaction_30_s=(30-s['fixed_s']-index)/stops,
            assumed_transaction_s=tx,total_s=s['fixed_s']+index+stops*tx,
            optimistic_usd=costs[0]*1.2,realistic_allowance_usd=costs[1]*1.2,conservative_usd=costs[2]*1.2,
            max_local_axis_usd_for_500=(500/1.2-s['base_cost_usd']-(s['shared_drive_usd'] if localstroke==1 else 0))/n,
            qualified=False))
    table('multirow.csv',rows)
    return rows


def bom(p):
    with (HERE/'bom.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
    totals={band:sum(float(r['quantity'])*float(r[band+'_unit_usd']) for r in rows) for band in ['optimistic','realistic','conservative']}
    return {'base_usd':totals,'with_contingency_usd':{k:v*(1+p['cost']['contingency_fraction']) for k,v in totals.items()},
            'delivered_quote_complete':False,'qualification':'blocked: no matched motor quote; realistic estimate exceeds ceiling'}


def main():
    p=json.loads((HERE/'params.json').read_text()); old=old_module();op=json.loads((old.HERE/'params.json').read_text())
    if p['grid'] != {'rows':80,'columns':80,'pitch_mm':5.08,'travel_mm':40,'levels':5}:
        raise ValueError('This validation baseline is 80x80, 5.08mm, 40mm, five levels. Changing it requires revising the historical geometry/mass and reliability screens together; use levels.csv for alternatives.')
    cad_parameters(p)
    with (HERE/'multirow_bom.csv').open(newline='',encoding='utf-8') as f:
        fixed=sum(float(r['allowance_usd']) for r in csv.DictReader(f))
    if fixed != p['multirow']['base_cost_usd']:raise ValueError('multirow base BOM mismatch')
    mp=maps(p);cases={k:schedule(p,v) for k,v in mp.items()}
    save('worst_schedule.json',schedule(p,mp['high'],True))
    # All possible OLD patterns are deliberately lifted clear before any write.
    table('transitions.csv',[dict(old=a,new=b,**cases[b]) for a in mp for b in mp])
    sweep=[]
    for rate,couple,settle,accel,inspect in itertools.product(*[p['sweep'][k] for k in ['rate_hz','couple_each_s','settle_each_s','scan_a_mm_s2','inspection_s']]):
        q=json.loads(json.dumps(p));q['timing'].update(rate_hz=rate,engage_s=couple,disengage_s=couple,home_settle_s=settle,write_settle_s=settle,seat_s=settle,scan_a_mm_s2=accel,inspection_s=inspect)
        t=schedule(q,mp['high'])['time_s']
        sweep.append(dict(rate_hz=rate,couple_each_s=couple,settle_each_s=settle,accel_mm_s2=accel,inspection_s=inspect,time_s=t,under_27=t<=27,under_30=t<30,basis='assumed'))
    table('timing_sweep.csv',sweep)
    geo=geometry(p,old,op);structures(p,geo['mass']['solid']['calculated_mass_g'])
    mr=multirow(p)
    result={'status':'NO PRODUCT QUALIFICATION; physical measurements absent',
        'inputs_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(HERE.glob('*')) if f.suffix in ['.py','.json','.csv','.scad']},
        'test08_params_sha256':hashlib.sha256((old.HERE/'params.json').read_bytes()).hexdigest(),
        'baseline_s':cases['high']['time_s'], 'test08_crosscheck_s':old.schedule(op,old.patterns(op)['all_high'])['time_s'],
        'margin_to_27_s':27-cases['high']['time_s'],
        'extra_per_row_budget_to_27_ms':(27-cases['high']['time_s'])*1000/80,
        'geometry':geo,'detent':detent(p),'reliability':reliability(),'bom':bom(p),
        'multirow_conditional_timing_regions':[{k:r[k] for k in ['mode','rows','columns','stroke_v_mm_s','total_s','optimistic_usd','realistic_allowance_usd']} for r in mr if r['total_s']<=27 and r['optimistic_usd']<=500]}
    save('summary.json',result)
    print(json.dumps({k:result[k] for k in ['status','baseline_s','margin_to_27_s','extra_per_row_budget_to_27_ms','detent','bom']},indent=2))


if __name__=='__main__':main()
