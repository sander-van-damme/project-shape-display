# Independent revised resident-cell drive and timing audit

The heavier resident-cell geometry does **not** by itself invalidate the conditional 80 mm/s drive screen. It increases the nominal 1605 torque demand by approximately 0.055 Nm. The corrected support-transfer sequence adds 0.330 s to each worst sampled full-scene transition. The result remains conditional on measured drag, the row-write cycle and reliable handoff; it does not establish a manufacturable complete machine.

CAD SHA-256: `780423514ddddcf11fb456d94cdb64d852cbc42908f92bf5494faaf326dda157`. This audit uses the explicitly named CAD source recorded in `analysis/revised-system-results.json`. Baseline `bank_drive.py`, `timing_global_pulse.py` arithmetic and their historical results remain unchanged; release cleanup removes trailing whitespace only.

## Mass accounting

At assumed densities PLA 1.24 g/cm³ and steel 7.85 g/cm³, independent rectilinear integration gives:

| Item | Per item | Full 4096-site array | Treatment in main terrain Z drive |
|---|---:|---:|---|
| Resident terrain pin | 2939.488 mm³ / 3.644965 g | 14.929777 kg | All selected pins move; worst case is 2048 pins/bank |
| Resident C-channel, including actual end bridges/tabs | 256.632 mm³ / 2.014561 g | 8.251643 kg | Excluded from main terrain Z load |

The C-channels are **stationary in terrain Z during a pulse**, not immobile. Common A moves them laterally and the addressed row moves them during programming. Their mass, contact friction and synchronization still load those separate drives. Counting all channel mass on the lift platen would be wrong; treating it as free would also be wrong.

Known moving A parts per 2048-site bank are 0.858297 kg of 64 steel Z rails, 0.183501 kg of dogs and 0.006069 kg of local guides: **1.047866 kg total**. These are included inside the 3 kg nominal moving-frame allowance, not added again. Remaining frame, bearing, synchronization and connection mass is unconstructed. Ground roots/pawls and the separate B frame are not part of the main Z moving mass.

The pin contains a 130 mm narrow tail, 90 mm broad upper section and 1.2 mm cap. Its 221.2 mm total length is the geometry actually charged, not the prior 80 mm hollow accounting stem. Pin-plus-channel mass alone is 23.181 kg under these material assumptions, before the remaining machine. No measured mass is claimed.

## Revised bank drive

For the nominal stress scenario, moving mass is 15.464889 kg per bank: 7.464889 kg pins + 3 kg moving frame + 5 kg terrain allowance. The 5 kg is a declared concentrated stress load, not measured ordinary miniature mass. Same assumptions as D: 80 mm/s, 800 mm/s², 1.5 force factor, 1605 effective lead, 90% efficiency, and 0.103153 Nm rotational allowance.

| Mean drag / moving site | Peak upward force | Steady mechanical power | Equal-corner factored force | Total torque at 960 rpm |
|---:|---:|---:|---:|---:|
| 0.01 N | 184.56 N | 13.78 W | 69.21 N | 0.3479 Nm |
| 0.03 N | 225.52 N | 17.05 W | 84.57 N | 0.4023 Nm |
| 0.10 N | 368.88 N | 28.52 W | 138.33 N | 0.5924 Nm |
| 0.50 N | 1188.08 N | 94.06 W | 445.53 N | 1.6789 Nm |

At 0.1 N/site, the prior result was 0.5371 Nm; the revised result is 0.5924 Nm. This remains below D's approximately 0.8 Nm older vendor curve near 960 rpm, but that comparison is not a guaranteed delivered-motor rating. At 0.5 N/site the same drive still fails. Summed drag and stiction remain decision-changing physical measurements. The motor comparison already includes the 1.5 force factor; no extra unlabelled margin is claimed.

The 40 mm descent releases 6.068 J before drag in this stress scenario. Backdriving, power-loss capture, regeneration, four-screw alignment and unequal corner loads remain unresolved construction qualifications. Increasing the mass does not justify assuming the commanded acceleration survives a stall or a binding guide.

## Nominal support-transfer sequence

A's final ideal geometry uses a 3.2 mm groove and 2.6 mm dog, leaving 0.6 mm total axial backlash. Centered acquisition has 0.3 mm gap on each side. A 0.4 mm take-up raises the pin only 0.1 mm off its grounded support.

- **Upward pulse:** take up +0.4; release ground; move +d; restore ground; move **−0.7** to force seating despite stiction; move +0.3 to center the dog; withdraw; return empty by d.
- **Downward pulse:** take up +0.4; release ground; move **−d**; restore ground while the pins lie between target +0.1 and +0.7; move **−0.7** to seat every pin positively; move +0.3 to center the dog; withdraw; return empty by d.

This is the load-independent nominal sequence accepted after E's adversarial correction. The initially proposed −(d + 0.6) main stroke was rejected: a freely descending pin stays on the upper dog flank and would arrive **0.5 mm below target before the grounded pawl is restored**. A friction-held pin behaves differently, so a single early backlash compensation is unsafe across arbitrary mixed loads.

After main −d, the fixed dog center constrains the pin to `[+0.1, +0.7]`. That entire interval admits the grounded pawl. After ground restoration and a further −0.7 dog stroke, the dog constrains the pin to `[−0.6, 0]`; intersecting with grounded support `pin ≥ 0` leaves exactly zero. The final +0.3 centers the unloaded dog. The same −0.7/+0.3 stroke is required after an upward pulse: the earlier −0.4 centering move alone could leave a sticky pin 0.1 mm above ground. It was rejected as gravity-assisted rather than positively seated. The script reproduces these ideal rigid intervals explicitly. This is why the seating stroke occurs after grounding for both signs.

The 0.1 mm unloading clearance is small. Actual rack pitch, key clearance, guide tilt, elastic deformation, ground-pawl height and manufactured phase are unqualified. In particular, this ideal CAD calculation does not replace the manual take-up-until-supported instruction on B's separate specimen. No additional tolerance correction, sensing latency or force-limited seating time is silently included.

The stop-to-stop movement law is triangular below `v²/a`, otherwise trapezoidal. Micro moves use 20 mm/s and 800 mm/s²; main/empty moves use 80 mm/s and 800 mm/s². Consequently this cannot be corrected using distance divided by speed alone.

| Pulse magnitude | Added upward time | Added downward time |
|---:|---:|---:|
| 5 mm | 0.065992 s | 0.065992 s |
| 10 mm | 0.065992 s | 0.065992 s |
| 20 mm | 0.065992 s | 0.065992 s |

Five 80 ms support/check event slots remain per pulse. An additional maximum-pulse retry reserve uses the revised worst downward pulse; it remains a time reserve, not a qualified recovery procedure.

## Corrected complete-scene timing

The independent scheduler imports only the historical workload generator, implements its own pulse selection and ledger, replays every selected pin's signed displacement, and reproduces the two published dirty-row baseline anchors exactly before calculating differences. Complete full-scan category ledgers, neutral preparation, first scene, local reveals, dense stress and sustained cycle legs are in `analysis/revised-system-results.json`.

| Array / stroke | Old scene at 80 ms row | Corrected scene at 80 ms row | Corrected scene at 120 ms row | Largest full-row cycle meeting 30 s on these workloads |
|---|---:|---:|---:|---:|
| 64² / 40 mm | 24.49730 s | 24.82726 s | 32.50726 s | 106.941 ms |
| 64² / 50 mm | 24.74730 s | 25.07726 s | 32.75726 s | 105.639 ms |
| 80² / 40 mm | 28.33730 s | 28.66726 s | 38.26726 s | 85.553 ms |
| 80² / 50 mm | 28.58730 s | 28.91726 s | 38.51726 s | 84.511 ms |

The worst sampled scenes use one upward pulse, three downward pulses and one worst-pulse retry reserve, giving **+0.329958 s**. No architecture decision changes: all full-scan cases still fail at 120 ms per complete row-write cycle; the 80 ms assumption remains physically unmeasured. The 80² timings are a 5.08 mm resolution comparison, not a claim that the present 6.35 mm resident-cell CAD packs at 5.08 mm.

| Full-scan category, 80 ms row | 64² / 40 mm | 64² / 50 mm | 80² / 40 mm | 80² / 50 mm |
|---|---:|---:|---:|---:|
| Cold scene | 21.27380 s | 21.52380 s | 24.47380 s | 24.72380 s |
| Neutral preparation | 14.16690 s | 17.72035 s | 16.08690 s | 20.28035 s |
| First scene from neutral | 17.72035 s | 21.27380 s | 20.28035 s | 24.47380 s |
| Preparation + first scene | 31.88726 s | 38.99416 s | 36.36726 s | 44.75416 s |
| Worst local reveal | 17.47035 s | 17.72035 s | 20.03035 s | 20.28035 s |
| Dense all-delta-level stress | 38.75597 s | 39.52352 s | 45.15597 s | 45.92352 s |

The final paired top/bottom programming bars add 128 bars and 4096 channel lugs while retaining 128 shared data actuators. The reference 256 external steel synchronization links alone add approximately 2.346 kg outside the main Z load. They keep the nominal old-data/row-up/new-data/row-down event count while increasing required synchronized travel, friction and actuator load. Independent union-volume integration of each 32-row paired writer gives 3430.506 mm³, or 26.9295 g steel; all 128 pairs total 3.447 kg including those links. A 1.6 mm triangular move in 20 ms requires 16 m/s². Each pair plus one channel then needs **0.463 N inertia alone**, before sliding friction, return spring, impact or reserve. This is a substantial fraction of the reference solenoid's approximately 0.784 N static headline, whose force-speed-stroke behavior is unqualified. This audit does not presume they preserve the 80 ms row cycle; there is no such measurement.

## Cost consequence and axis count

The actual solid column material becomes **$298.60** at the same assumed $20/kg, versus **$141.27** for the old hollow envelope. This is raw polymer only, without support, waste, printing time or assembly. At an explicitly illustrative net deposition rate of 5–15 g/hour, these columns alone represent approximately 995–2,986 printer-hours. Actual orientation, supports and throughput are unqualified; no print-production forecast or cheap fabrication claim follows.

The conventional-drive low allocation becomes **$2309.88** with eight total axis allowances: six assigned plus two explicit reserves. It is **$2267.98** if only the six assigned axes are carried. Both count two full bank-drive provisions replacing two generic motor/driver pairs. The eight-axis arithmetic is:

`$722.24 coils/boards + 6 × $20.95 remaining motor/driver pairs + $903.34 two bank drives + $298.60 polymer + $80 frame + $30 controller + $100 coil-power allowance + $50 wiring`.

This is an **incomplete allowance, not a complete BOM or supplier quote**. Custom resident channels, dogs, pawls, joining, precision guides, programming mechanisms and full frame fabrication remain unpriced. The $100 coil-power allowance may not satisfy the 704 W reference coil demand; the lift-drive supplies are already counted separately inside the bank-drive provision. These figures do not support a $1500 machine.

## Reproduction and limits

Run from any directory:

```text
python recheck.py --repo-root /path/to/project-shape-display --cad /path/to/resident_cell.scad --output results.json
python write_review.py --input results.json --output review.md
```

Python standard library only. The repository's unchanged historical workload dependencies must be present. The source hash is recorded; explicit pin dimensions are asserted. If the channel geometry changes, update the named rectilinear boxes before rerunning instead of reusing a stale mass. The script verifies its category ledger sums and motion/baseline anchors. This report independently checks computation; it does not qualify manufactured friction, tolerance, control timing, wall playability or physical performance.
