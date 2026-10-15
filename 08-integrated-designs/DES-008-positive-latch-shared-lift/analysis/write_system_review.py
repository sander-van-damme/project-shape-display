#!/usr/bin/env python3
"""Write the human-readable audit from recheck.py's JSON (stdlib only)."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path(__file__).with_name('revised-system-results.json'));p.add_argument('--output',type=Path,default=Path('work/des008-revised-system.md'));a=p.parse_args();r=json.loads(a.input.read_text());m=r['mass'];c=r['cost_update'];d=r['drive'];nom=[x for x in d['cases'] if x['case']=='nominal'];sha=next(v for k,v in r['source_hashes'].items() if k.endswith('resident_cell.scad'))
lines=[f'''# Independent revised resident-cell drive and timing audit

The heavier resident-cell geometry does **not** by itself invalidate the conditional 80 mm/s drive screen. It increases the nominal 1605 torque demand by approximately 0.055 Nm. The corrected support-transfer sequence adds 0.330 s to each worst sampled full-scene transition. The result remains conditional on measured drag, the row-write cycle and reliable handoff; it does not establish a manufacturable complete machine.

CAD SHA-256: `{sha}`. This audit uses the explicitly named CAD source recorded in `analysis/revised-system-results.json`. Baseline `bank_drive.py`, `timing_global_pulse.py` arithmetic and their historical results remain unchanged; release cleanup removes trailing whitespace only.

## Mass accounting

At assumed densities PLA 1.24 g/cm³ and steel 7.85 g/cm³, independent rectilinear integration gives:

| Item | Per item | Full 4096-site array | Treatment in main terrain Z drive |
|---|---:|---:|---|
| Resident terrain pin | {m['pin_volume_mm3']:.3f} mm³ / {m['pin_PLA_g']:.6f} g | {m['pins_full_4096_kg']:.6f} kg | All selected pins move; worst case is 2048 pins/bank |
| Resident C-channel, including actual end bridges/tabs | {m['channel_volume_mm3']:.3f} mm³ / {m['channel_steel_g']:.6f} g | {m['channels_full_4096_kg']:.6f} kg | Excluded from main terrain Z load |

The C-channels are **stationary in terrain Z during a pulse**, not immobile. Common A moves them laterally and the addressed row moves them during programming. Their mass, contact friction and synchronization still load those separate drives. Counting all channel mass on the lift platen would be wrong; treating it as free would also be wrong.

Known moving A parts per 2048-site bank are {m['A_Z_rails_bank_kg']:.6f} kg of 64 steel Z rails, {m['A_dogs_bank_kg']:.6f} kg of dogs and {m['A_dog_guides_bank_kg']:.6f} kg of local guides: **{m['known_A_Z_parts_bank_kg']:.6f} kg total**. These are included inside the 3 kg nominal moving-frame allowance, not added again. Remaining frame, bearing, synchronization and connection mass is unconstructed. Ground roots/pawls and the separate B frame are not part of the main Z moving mass.

The pin contains a 130 mm narrow tail, 90 mm broad upper section and 1.2 mm cap. Its 221.2 mm total length is the geometry actually charged, not the prior 80 mm hollow accounting stem. Pin-plus-channel mass alone is {(m['pins_full_4096_kg']+m['channels_full_4096_kg']):.3f} kg under these material assumptions, before the remaining machine. No measured mass is claimed.

## Revised bank drive

For the nominal stress scenario, moving mass is {nom[0]['moving_mass_kg']:.6f} kg per bank: {m['pins_bank_2048_kg']:.6f} kg pins + 3 kg moving frame + 5 kg terrain allowance. The 5 kg is a declared concentrated stress load, not measured ordinary miniature mass. Same assumptions as D: 80 mm/s, 800 mm/s², 1.5 force factor, 1605 effective lead, 90% efficiency, and {d['rotational_allowance_Nm']:.6f} Nm rotational allowance.

| Mean drag / moving site | Peak upward force | Steady mechanical power | Equal-corner factored force | Total torque at 960 rpm |
|---:|---:|---:|---:|---:|''']
for x in nom:lines.append(f"| {x['drag_N_site']:.2f} N | {x['up_peak_N']:.2f} N | {x['steady_mechanical_power_W']:.2f} W | {x['ideal_equal_corner_design_N']:.2f} N | {x['torque_1605_at960rpm_Nm']:.4f} Nm |")
x=next(v for v in nom if v['drag_N_site']==.1)
lines.append(f'''
At 0.1 N/site, the prior result was {x['prior_torque_same_case_Nm']:.4f} Nm; the revised result is {x['torque_1605_at960rpm_Nm']:.4f} Nm. This remains below D's approximately 0.8 Nm older vendor curve near 960 rpm, but that comparison is not a guaranteed delivered-motor rating. At 0.5 N/site the same drive still fails. Summed drag and stiction remain decision-changing physical measurements. The motor comparison already includes the 1.5 force factor; no extra unlabelled margin is claimed.

The 40 mm descent releases {x['descent_40mm_gravity_J']:.3f} J before drag in this stress scenario. Backdriving, power-loss capture, regeneration, four-screw alignment and unequal corner loads remain unresolved construction qualifications. Increasing the mass does not justify assuming the commanded acceleration survives a stall or a binding guide.

## Nominal support-transfer sequence

A's final ideal geometry uses a 3.2 mm groove and 2.6 mm dog, leaving 0.6 mm total axial backlash. Centered acquisition has 0.3 mm gap on each side. A 0.4 mm take-up raises the pin only 0.1 mm off its grounded support.

- **Upward pulse:** take up +0.4; release ground; move +d; restore ground; move **−0.7** to force seating despite stiction; move +0.3 to center the dog; withdraw; return empty by d.
- **Downward pulse:** take up +0.4; release ground; move **−d**; restore ground while the pins lie between target +0.1 and +0.7; move **−0.7** to seat every pin positively; move +0.3 to center the dog; withdraw; return empty by d.

This is the load-independent nominal sequence accepted after E's adversarial correction. The initially proposed −(d + 0.6) main stroke was rejected: a freely descending pin stays on the upper dog flank and would arrive **0.5 mm below target before the grounded pawl is restored**. A friction-held pin behaves differently, so a single early backlash compensation is unsafe across arbitrary mixed loads.

After main −d, the fixed dog center constrains the pin to `[+0.1, +0.7]`. That entire interval admits the grounded pawl. After ground restoration and a further −0.7 dog stroke, the dog constrains the pin to `[−0.6, 0]`; intersecting with grounded support `pin ≥ 0` leaves exactly zero. The final +0.3 centers the unloaded dog. The same −0.7/+0.3 stroke is required after an upward pulse: the earlier −0.4 centering move alone could leave a sticky pin 0.1 mm above ground. It was rejected as gravity-assisted rather than positively seated. The script reproduces these ideal rigid intervals explicitly. This is why the seating stroke occurs after grounding for both signs.

The 0.1 mm unloading clearance is small. Actual rack pitch, key clearance, guide tilt, elastic deformation, ground-pawl height and manufactured phase are unqualified. In particular, this ideal CAD calculation does not replace the manual take-up-until-supported instruction on B's separate specimen. No additional tolerance correction, sensing latency or force-limited seating time is silently included.

The stop-to-stop movement law is triangular below `v²/a`, otherwise trapezoidal. Micro moves use 20 mm/s and 800 mm/s²; main/empty moves use 80 mm/s and 800 mm/s². Consequently this cannot be corrected using distance divided by speed alone.

| Pulse magnitude | Added upward time | Added downward time |
|---:|---:|---:|''')
for size,v in r['pulse_corrections'].items():lines.append(f"| {size} mm | {v['1']:.6f} s | {v['-1']:.6f} s |")
lines.append('''
Five 80 ms support/check event slots remain per pulse. An additional maximum-pulse retry reserve uses the revised worst downward pulse; it remains a time reserve, not a qualified recovery procedure.

## Corrected complete-scene timing

The independent scheduler imports only the historical workload generator, implements its own pulse selection and ledger, replays every selected pin's signed displacement, and reproduces the two published dirty-row baseline anchors exactly before calculating differences. Complete full-scan category ledgers, neutral preparation, first scene, local reveals, dense stress and sustained cycle legs are in `analysis/revised-system-results.json`.

| Array / stroke | Old scene at 80 ms row | Corrected scene at 80 ms row | Corrected scene at 120 ms row | Largest full-row cycle meeting 30 s on these workloads |
|---|---:|---:|---:|---:|''')
for n in (64,80):
 for stroke in (40,50):
  v=r['scene_cases'][f'N{n}_stroke{stroke}_row80_full_scan'];slow=r['scene_cases'][f'N{n}_stroke{stroke}_row120_full_scan']
  lines.append(f"| {n}² / {stroke} mm | {v['baseline_seconds']:.5f} s | {v['revised_seconds']:.5f} s | {slow['revised_seconds']:.5f} s | {v['revised_row_time_limit']*1000:.3f} ms |")
lines.append('''
The worst sampled scenes use one upward pulse, three downward pulses and one worst-pulse retry reserve, giving **+0.329958 s**. No architecture decision changes: all full-scan cases still fail at 120 ms per complete row-write cycle; the 80 ms assumption remains physically unmeasured. The 80² timings are a 5.08 mm resolution comparison, not a claim that the present 6.35 mm resident-cell CAD packs at 5.08 mm.

| Full-scan category, 80 ms row | 64² / 40 mm | 64² / 50 mm | 80² / 40 mm | 80² / 50 mm |
|---|---:|---:|---:|---:|''')
for name,label in [('cold_start','Cold scene'),('neutral_preparation','Neutral preparation'),('first_from_neutral','First scene from neutral'),('neutral_then_first','Preparation + first scene'),('local_reveal','Worst local reveal'),('dense_all_levels','Dense all-delta-level stress')]:
 vals=[r['category_cases'][f'N{n}_stroke{stroke}_row80_full_scan'][name]['revised_seconds'] for n in (64,80) for stroke in (40,50)]
 lines.append('| '+label+' | '+' | '.join(f'{v:.5f} s' for v in vals)+' |')
lines.append(f'''
The final paired top/bottom programming bars add 128 bars and 4096 channel lugs while retaining 128 shared data actuators. The reference 256 external steel synchronization links alone add approximately {m['paired_writer_reference_steel_links_full_kg']:.3f} kg outside the main Z load. They keep the nominal old-data/row-up/new-data/row-down event count while increasing required synchronized travel, friction and actuator load. Independent union-volume integration of each 32-row paired writer gives {m['paired_writer_volume_mm3']:.3f} mm³, or {m['paired_writer_steel_g']:.4f} g steel; all 128 pairs total {m['paired_writers_full_128_kg']:.3f} kg including those links. A 1.6 mm triangular move in 20 ms requires 16 m/s². Each pair plus one channel then needs **{m['writer_and_one_channel_inertial_force_N']:.3f} N inertia alone**, before sliding friction, return spring, impact or reserve. This is a substantial fraction of the reference solenoid's approximately 0.784 N static headline, whose force-speed-stroke behavior is unqualified. This audit does not presume they preserve the 80 ms row cycle; there is no such measurement.

## Cost consequence and axis count

The actual solid column material becomes **${c['revised_column_polymer_dollars']:.2f}** at the same assumed $20/kg, versus **${c['previous_column_polymer_dollars']:.2f}** for the old hollow envelope. This is raw polymer only, without support, waste, printing time or assembly. At an explicitly illustrative net deposition rate of 5–15 g/hour, these columns alone represent approximately 995–2,986 printer-hours. Actual orientation, supports and throughput are unqualified; no print-production forecast or cheap fabrication claim follows.

The conventional-drive low allocation becomes **${c['low_allocation_eight_axes']:.2f}** with eight total axis allowances: six assigned plus two explicit reserves. It is **${c['low_allocation_six_assigned_axes']:.2f}** if only the six assigned axes are carried. Both count two full bank-drive provisions replacing two generic motor/driver pairs. The eight-axis arithmetic is:

`$722.24 coils/boards + 6 × $20.95 remaining motor/driver pairs + $903.34 two bank drives + ${c['revised_column_polymer_dollars']:.2f} polymer + $80 frame + $30 controller + $100 coil-power allowance + $50 wiring`.

This is an **incomplete allowance, not a complete BOM or supplier quote**. Custom resident channels, dogs, pawls, joining, precision guides, programming mechanisms and full frame fabrication remain unpriced. The $100 coil-power allowance may not satisfy the 704 W reference coil demand; the lift-drive supplies are already counted separately inside the bank-drive provision. These figures do not support a $1500 machine.

## Reproduction and limits

Run from any directory:

```text
python recheck.py --repo-root /path/to/project-shape-display --cad /path/to/resident_cell.scad --output results.json
python write_review.py --input results.json --output review.md
```

Python standard library only. The repository's unchanged historical workload dependencies must be present. The source hash is recorded; explicit pin dimensions are asserted. If the channel geometry changes, update the named rectilinear boxes before rerunning instead of reusing a stale mass. The script verifies its category ledger sums and motion/baseline anchors. This report independently checks computation; it does not qualify manufactured friction, tolerance, control timing, wall playability or physical performance.
''')
a.output.write_text('\n'.join(lines));print(a.output)
