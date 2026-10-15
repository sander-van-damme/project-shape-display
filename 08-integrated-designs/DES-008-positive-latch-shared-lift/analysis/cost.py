#!/usr/bin/env python3
"""Retained-head versus direct-selector cost accounting.
All custom fabrication prices are UNQUOTED allowance scenarios; catalog price
anchors are not actuator qualification. USD, excluding VAT, shipping and labor.
"""
import csv,json
from pathlib import Path
OUT=Path(__file__).parent

def mass(length=80.,cavity=(0.,0.)):
    # 6x6 cap1.2mm, 5.4x3.8 stem. Conservative no rack-recess removal.
    vol=5.4*3.8*length+(36-5.4*3.8)*1.2-cavity[0]*cavity[1]*(length-1.2)
    return vol*4096*1.24/1e6

def ledger(b,retained):
    coils=(8 if retained else 64)*b
    n_axis=(4 if retained else 3)*b
    n_driver=coils//8
    rows=[]
    def add(item,qty,unit,low,high,basis):
        rows.append(dict(item=item,qty=qty,unit=unit,low=round(qty*low,2),high=round(qty*high,2),basis=basis))
    add('Selector solenoids',coils,'piece',4.46 if retained else 3.96,4.46 if retained else 3.96,'catalog Adafruit2776; no force/speed/duty qualification')
    add('Eight-channel solenoid driver boards',n_driver,'board',14.95 if retained else 13.46,14.95 if retained else 13.46,'catalog Adafruit6318; shared current/heat needs qualification')
    add('Motion motors',n_axis,'motor',12.60,25.,'low catalog Adafruit324 price anchor only; high procurement allowance')
    add('Motion drivers',n_axis,'driver',6.26,12.,'low catalog Adafruit6109; high allowance')
    add('Z guide/drive stock',b,'axis',18.,40.,'allowance rails/belts or screws/pulleys/bearings; not quoted')
    add('Row guide/drive stock',b,'axis',15.,35.,'allowance shafts/guides/belts/bearings; not quoted')
    add('Sequencer shaft/cam/link stock',b,'head',10.,30.,'allowance; fabricated precise cam surfaces extra below')
    if retained: add('Writer traverse hardware',b,'axis',12.,30.,'allowance; motor/driver counted above')
    add('Head polymer beyond terrain columns',b,'head',6.,18.,'0.3-0.9kg at assumed$20/kg; source CAD not available')
    add('Head common precision/load-path fabrication',b,'head',15.,60.,'Q_head UNQUOTED allowance; dogs/keys/carriers finishing/cams')
    if retained: add('Memory-specific custom fabrication',b,'head',30.,150.,'Q_memory UNQUOTED allowance; flags/rods/compliance/keepers/readers')
    add('Terrain column material',1,'display',mass(80,(3.8,1.4))*20,mass(100,(0,0))*20,'5.4x3.8 stem, rack-wall-preserving hollow low; solid high; $20/kg assumption')
    add('Fixed guide/support polymer',1,'display',25.,60.,'1.25-3kg at assumed$20/kg; not CAD volume')
    add('Fixed 4096-pawl fabrication',1,'display',150.,650.,'Q_ground UNQUOTED allowance; does not certify an actual supplier price')
    add('Frame, feet, covers',1,'display',80.,180.,'material allowance, no woodworking/metal fabrication labor')
    add('Controller / communications / limit switches',1,'display',30.,75.,'allowance; local checks only, no vision system')
    add('Power conversion/distribution',1,'display',40.+(12. if retained else 45.)*b,80.+(25. if retained else 90.)*b,'allowance; direct coils need huge peak current; no selected PSU')
    add('Wiring, connectors, fusing',1,'display',25.+.25*coils+2*n_axis,60.+.75*coils+4*n_axis,'explicit allowance for coil and motion channels')
    add('Fasteners, shims, spares',1,'display',35.+5*b,70.+10*b,'allowance')
    q_names=['Head common precision/load-path fabrication','Memory-specific custom fabrication','Fixed 4096-pawl fabrication']
    totals={k:round(sum(row[k] for row in rows),2) for k in ['low','high']}
    subtotal={k:round(sum(row[k] for row in rows if row['item'] not in q_names),2) for k in ['low','high']}
    electronics=sum(row['low'] for row in rows[:4])
    return dict(heads=b,retained=retained,counts=dict(terrain_columns=4096,ground_pawls=4096,moving_dogs=64*b,A_keys=64*b,A_vertical_guides=64*b,B_keys=64*b,reader_rods=128*b if retained else 0,mask_flags=64*b if retained else 0,keepers=2*b if retained else 0,reader_platens=2*b if retained else 0,writer_actuators=coils if retained else 0,direct_actuators=0 if retained else coils,motion_motors=n_axis,motion_drivers=n_axis,coil_driver_boards=n_driver,coil_wires=2*coils,motor_wires=4*n_axis),catalog_electronics_floor=round(electronics,2),full_allocated_total=totals,subtotal_excluding_unknown_custom_fabrication=subtotal,peak_coil_w=round(coils*5.5,1),peak_coil_A_5V=round(coils*1.1,1),coil_mass_kg=round(coils*.0126,3),rows=rows)

# Intentionally explicit hand-operation scenarios, no measured touch times or yield.
def labor(b,retained):
    common_low=4096*10/3600+64/60+8
    common_high=4096*20/3600+512*2/60+16
    head_common_low=64*5/3600+128*10/3600+.5+3*.33
    head_common_high=64*15/3600+128*30/3600+1.5+3*.75
    memory_low=64*8/3600+128*12/3600+.5+.5+8*60/3600+.2
    memory_high=64*30/3600+128*45/3600+1.5+1.5+8*180/3600+.6
    direct_low=64*45/3600+.5
    direct_high=64*180/3600+1.5
    return dict(heads=b,retained=retained,low_hours=round(common_low+b*(head_common_low+(memory_low if retained else direct_low)),1),high_hours=round(common_high+b*(head_common_high+(memory_high if retained else direct_high)),1),additional_fitting_one_min_per_terrain_site_hours=round(4096/60,2))

def global_screen():
    coils=128
    drivers=16
    axes=8  # six assigned axes plus two explicit auxiliary reserves
    electronics=coils*3.96+drivers*13.46+axes*(14+6.95)
    columns=mass(80,(3.8,.9))*20
    common_allowances=dict(terrain_column_polymer=columns,frame=80.,controller=30.,power=100.,wire_fuse_connectors=50.)
    residual=1500-electronics-sum(common_allowances.values())
    stem_bank_N=mass(80,(3.8,.9))/2*9.81
    terrain_N=5*9.81
    force=[dict(drag_N_per_moving_site=f,simultaneous_sites=2048,bank_static_force_N=round(stem_bank_N+terrain_N+2048*f,2),torque_Nm_8mm_lead_0p3eff=round((stem_bank_N+terrain_N+2048*f)*.008/(2*3.141592653589793*.3),3)) for f in [.01,.03,.1,.25,.5]]
    return dict(display_sites=4096,bank_sites=2048,ground_pawls=4096,positive_transport_dogs=4096,resident_mask_bits=4096,additional_keys_range=[4096,8192],selector_actuators=coils,coil_driver_boards=drivers,motion_axes_assigned=6,motion_axes_reserve=2,electronics_price_anchor=round(electronics,2),max_remaining_per_site_before_all_common_hardware=round((1500-electronics)/4096,4),common_low_allowances=common_allowances,remaining_for_all_other_passive_parts_at_1500=round(residual,2),remaining_per_site_after_common_low_allowances=round(residual/4096,4),peak_coil_W=704,peak_coil_A_5V=140.8,force_sensitivity=force)

if __name__=='__main__':
    scenarios=[ledger(b,r) for b in [4,6,8] for r in [True,False]]
    result=dict(price_date='2026-10-14',scenarios=scenarios,labor=[labor(b,r) for b in [4,6,8] for r in [True,False]],mass_kg={f'{L}mm_{name}':round(mass(L,cav),3) for L in [80,100] for name,cav in [('solid',(0,0)),('symmetric0p8',(3.8,2.2)),('rack_backed',(3.8,1.4)),('two_sided_rack_backed',(3.8,.9))]},break_even_catalog_saving_per_head=round(64*3.96+8*13.46-(8*4.46+14.95+12.60+6.26),2))
    result['global_platen_screen']=global_screen()
    (OUT/'cost-results.json').write_text(json.dumps(result,indent=2)+'\n')
    with (OUT/'bom-comparisons.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['heads','architecture','item','qty','unit','low','high','basis'],lineterminator='\n');w.writeheader()
        for s in scenarios:
            for row in s['rows']:w.writerow(dict(heads=s['heads'],architecture='retained' if s['retained'] else 'direct',**row))
    for s in scenarios:print(s['heads'],'retained' if s['retained'] else 'direct',s['catalog_electronics_floor'],s['full_allocated_total'],s['subtotal_excluding_unknown_custom_fabrication'])
    print(result['mass_kg']); print(result['labor'])
