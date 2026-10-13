---
status: complete
builds-on: [E-255]
---

# Screw friction adjustment and loaded drive envelope

Reproduce: `python3 tools/curated-experiment-checks/E-256/drive_envelope.py`.
**Bounded calculations, not measurements or process priors.** Total moving masses
5/20 g include pin plus assigned miniature load;100 g is a separate stress case.
None is measured typical play. Weigh actual pieces and their support distribution;
do not treat earlier 1-N/cell stress assumptions as ordinary miniature loads.

Using the same d 2.3/lead 3 model, raising coefficient `ku=r*(s+u)/(1-s*u)`.
Static breakaway drag Ds and running drag Dk represent fit-induced preload;
**there is no CAD-clearance→drag law here**. Tightening is not prescribing μ.
Holding requires `Ds+W*kl_static>=0`; positive slow lowering resistance requires
`Dk+W*kl_running>0`. Neither inequality certifies dynamic arrest.
For labelled μstatic=.3/μrunning=.1/Dk=.5Ds/no collar:

| Total moving mass | Ds static-hold threshold, N·mm | Ds slow-lowering threshold, N·mm |
|---|---:|---:|
| 5 g | .00522 | >.03370 |
| 20 g | .02090 | >.13480 |
| 100 g stress | .10449 | >.67399 |

Ds=.05 therefore holds 20 g statically yet fails the running-resistance condition.
A loaded collar μc*rc=.2 mm changes 20-g thresholds to 0 and>.05634 N·mm.
Thread μ=.5 instead has positive lowering resistance without added drag.
These competing scenarios do not predict backdrive in Sander's successful pair.

Drive countercheck: running μ=.3/Dk=.05/no collar or guide drag,3,000 rpm,
acceleration 1,000 rev/s² (3 m/s² axial), screw-reflected rotating J=1e-8 kg m²:

| Mass | Steady / accelerating raising N·mm | 160 steady outputs W |
|---|---:|---:|
| 5 g | .0970 / .1742 | 4.87 |
| 20 g | .2379 / .3583 | 11.96 |
| 100 g stress | .9897 / 1.3400 | 49.75 |

Torque=`(m*(g+c*alpha)+Fguide)*ku+Dk+J*alpha`, c=lead/(2π) in SI;
translating inertia enters thread force, not J again. 27 cases vary mass 5/20/100 g,
μ=.1/.3/.5 and Dk=0/.05/.2. J=1e-9/1e-8/1e-7 adds.00628/.06283/.62832 N·mm
at that acceleration. Added.05-N·mm drag dissipates 26.81 J over 6,400×40-mm moves.
Modest added friction is not rejected by energy alone. Electrical/transmission
losses, startup current, binding, breakaway peaks, local heat and wear remain open.

**Speed opportunity:** bisection of the nine-transition sample gives exactly 30 s
at B2/1,000rev/s²/20-ms proof:1,613.4 loaded rpm. At 500rev/s²:1,742.8 rpm;
100-ms proof:2,034.7 rpm; B3/base settings:953.4 rpm. Strict<30 needs margin.
B2 at 2,000 rpm gives 26.9335 s; at 200rev/s² even unlimited speed gives 31.1095 s
(all moves triangular). Docking, return, retry and common 4 s stay included.
Separate dense flat→40 and mixed±40 stress cases both take29.4335 s at2,000 rpm.
This is sample timing, not gameplay compliance. B2 still needs 160 complete
channels at≤$6.325 each for the$1,500 research allocation; no sourced BOM or final<$500 path yet.

Moving-loss energy: at 3,000 rpm/20 g, reflected translating inertia 4.56e-9 kg m²
plus rotating J=1e-9/1e-8/1e-7 gives.274/.718/5.160 mJ. Arrest within 1 mm needs
average **net** braking torque.131/.343/2.464 N·mm; .1 mm needs 10× more.
Resistance must additionally cover gravity (equivalent.0936 N·mm here).
Distances are sensitivity choices, not product limits or predicted coast;
dynamic contact forces and disconnect state remain unmeasured. Normal withdrawal
following a complete commanded stop has no initial kinetic energy ideally.

**Decision:** B2 is a conditional comparison, not a selected architecture. Its
sample suggests ~2,000 loaded rpm with adequate torque/acceleration. Updated
playable encodings, raised neutral, 4096/6400 sites and $500/$1000/$1500 comparisons
remain conditional in E-258/E-259. Do not tighten an already holding pair. A batch
setting needs weakest hold and strongest drive torque inside the measured operating
window; common bias, wear and local variation can close it. Avoid 6,400 hand fits.

## Measurement method and reduction

**Measurement-design calculations, not results:** at a 10-mm perpendicular arm,
1 g tangential deadweight gives 0.09807 N·mm. That mass increment brackets onset
only to that width even with perfect geometry. A 0.01-N·mm absolute error budget
allows ≤0.10197-g mass error before radius/alignment/tare/friction errors. An
unspecified kitchen scale cannot resolve the illustrative 0.02090-N·mm added-drag
threshold simply by displaying grams. Total measured torque is not added drag.
At this arm, 0.238 N·mm needs 0.0238-N sideways force; spindle/guide friction can
change. Preserve the seat, measure the perpendicular arm, include holder tare and
apparatus effects; a pulley is not calibrated by a known hanging mass.
Finger turning is qualitative torque evidence only.

`python3 tools/curated-experiment-checks/E-256/measurements.py --check` checks
signed travel, ambiguous/resolved drift, torque endpoints, units and invalid inputs
using **synthetic** controls. `--blank` emits an unmeasured JSON template;
`--record FILE` requires observations, provenance, bounds and supported-mass interval.
Keep raw physical records with their evidence; none is fabricated here.

- `evidence`: physical_measurement or synthetic; `specimen`, `setup`, `raw_source`
  and `bounds_basis` identify input and uncertainty. Unknowns must not become
  invented bounds merely to satisfy the reducer.
- `total_supported_mass_g`: [lower, upper]. Separate different specimens/loads/setups.
- `holds`: position and observations of elapsed_s (starting at zero), height_mm
  intervals. Endpoint subtraction assumes no common-bias cancellation; equal
  heights each bounded ±0.1 mm give drift [-0.2,+0.2] mm, not zero drift.
- `travel`: before_mm, after_mm, signed_turns intervals; zero-turn intervals are
  rejected. Effective displacement/turn includes backlash unless taken up.
- Optional `torque`: direction raise/lower, observation no_motion/onset/slow_running,
  force_N and perpendicular_arm_mm intervals. Output is apparatus torque, with
  no inferred parasitic correction, friction fit or motor-speed approval.

The existing friction/work/inertia/timing checks remain calculations. E-258/E-259's
4096/6400-site, raised-neutral and $500/$1000/$1500 comparisons remain conditional.
Static hold, moving loss, powered speed and batch manufacture are separate claims.

## Recovered specimens, 2026-10-13

**Owner-reported rough physical measurements:** Sander recovered the printed parts
and has a ruler, kitchen scale and phone camera. He reports pin length about
50 mm and width about 4–5 mm; screw length about 40 mm and width about 3 mm.
Neither part registered on his scale. Mass is **unknown**, not zero or a bounded
sub-gram measurement: scale increment, minimum load and accuracy are unknown.
The widths are estimates, not tolerance intervals. The subsequent manual check
below supplies rough travel and play estimates, but no timed drift or torque record.

Provenance: [owner answer and photographs on LAB-388](/LAB/issues/LAB-388#comment-ec47dec7-7141-49a7-b009-ed683ba36eee),
following answered interaction `5ce19b24-943f-4c66-8eb7-a8422be0c929`.
Original images remain in Paperclip: [pin length](/api/attachments/03e1f8f2-359b-4adc-add2-5a77fb71eaf8/content),
[screw length](/api/attachments/65d58509-a1bf-48b5-bce5-f1bc83e281a1/content),
[pin width](/api/attachments/ef73fa02-b1be-4ed0-aa58-b6f92491e485/content),
[screw width](/api/attachments/07cf9d30-1835-414b-9946-2c02988b809e/content).
**Visual observations:** separate pale rectangular pin and helical screw beside
a millimetre ruler; approximate lengths are consistent with the owner's report.
The photographs do not show assembled guidance, screw thrust support, internal
engagement, load placement or motion. Blur, perspective and different surface
planes prevent assigning precise diameter, clearance or drift bounds. No pixel
metrology or identification of the historical calibration variant is claimed.

**Decision consequence:** the recovered roughly 40-mm screw must not inherit
trial-5's nominal 50-mm screw or a qualified 40/50-mm stroke. For a nut remaining
fully within the threaded region, stroke is at most threaded length minus nut
engagement length and end margins; these dimensions remain unknown. Other
overlap conventions require their own support check. This pair can discriminate
basic translation/holding without establishing the proposed product travel.

### Manual motion, load and failure report, 2026-10-13

**Firsthand owner observations, not a fixture-qualified load rating.** Source:
Sander's authenticated answer to interaction
`31f4a7e3-fb98-4b28-ab16-e09a310f2f44` on [LAB-388](/LAB/issues/LAB-388),
resolved 2026-10-13 16:47:18 UTC. This supersedes the unanswered setup question.

| Owner report | Evidence and remaining uncertainty |
|---|---|
| No fixture; only screw and pin | No demonstrated thrust support, guide or independently released assembly. Exact hand contacts unknown. |
| About 2 mm displacement after one turn; difficult to read | Rough effective travel estimate; no endpoint readings, return reading, direction convention or error bound. Does not identify CAD lead. |
| Turns a little roughly, but turns | Qualitative drive evidence; owner attributes rest stability to roughness. No measured torque or friction coefficient. |
| About 1 mm upward/downward play when pulling the screw; owner considers it negligible | Rough axial free-play estimate, not measured reversal backlash, creep or commanded position error. |
| Partly engaged pair pressed on kitchen scale to about 1 kg without observed screw rotation | Positive manual load/rotation observation. Scale calibration, force alignment, engagement, duration and possible hand restraint are unknown. |
| At near-full extension, only slightly inserted, screw bends and breaks under force close to 1 kg, without bending protection | Physical failure reported. Free length, eccentricity, engagement and fracture site unknown; cannot separate bending, buckling, thread-root or engagement failure. |

Preserved owner interpretation: an enclosure should protect against bending,
miniatures are much lighter, and final designs will need repeat tests. These are
reasonable hypotheses, not a demonstrated enclosure or measured miniature-load
margin. No additional destructive repeat is needed to establish this failure.

**Calculations, not calibrated measurement bounds:** a 1-kg mass-equivalent scale
reading corresponds to approximately 9.81 N using standard gravity. This is the
reported scale reaction, not a certified pure axial load through the thread or a
sustained 1-kg miniature capacity. If effective lead were 2 rather than the
historical model's 3 mm/turn, 40-mm motion would need 20 rather than 13.33 turns;
50 mm would need 25 rather than 16.67. Rotation count rises 50%; complete update
time does not necessarily rise 50% because acceleration and other operations
remain. Neither stroke was measured here; retain 2 and 3 as comparison scenarios,
not confidence bounds or a silent replacement of the historical CAD parameter.

**Decision:** continue the retained-screw campaign with stronger evidence for
basic manual motion and load resistance, while making supported engagement and
end-of-travel control explicit in the next mechanism screen. Do not tighten this
pair or add a per-cell brake on this evidence. A housing helps only if it actually
reacts lateral loads and maintains alignment/engagement; it does not automatically
repair insufficient overlap. Reserve qualified minimum engagement and end margins
inside usable stroke; do not treat nearly unthreaded extension as terrain range.
Assess the reported play by repeatable loaded settling/reversal and miniature
stability before paying for anti-backlash hardware or dismissing it as negligible.
One-millimetre play is not ten-minute drift. Broken/damaged specimens cannot
inherit the earlier intact pair's observation in a later test.

The accessible-specimen characterization is complete at this evidence level.
Timed hands-off retention, breakaway/running torque, powered speed, moving-loss
arrest and batch variability remain unmeasured. The interval reducer is deliberately
not fed guessed bounds or synthetic raw readings for this informal report. A later
supported intact article must provide axial screw reaction, pin anti-rotation and
lateral guidance while allowing screw rotation, plus limited travel; its design
and qualification are separate work. No new print or owner response is requested.

### Conditional first supported check

For a later intact specimen, not a current owner request:

1. Describe screw thrust reaction, pin anti-rotation, lateral guide and hand
   contacts. The fixture must allow screw rotation during retention testing.
2. At a comfortably engaged middle position, use a fixed ruler/phone, square
   viewing angle and similar camera depth for marks/edge. Record starting height,
   height after one complete turn and after one return; include viewing direction,
   binding and lost motion. Never force either end or use damaged parts.
3. Only with stable hands-off load placement, record ordinary miniature/load scale
   reading, scale increment, holder and other supports; then height at 0/60/600 s
   after releasing drive/hands. No stable placement means omit the hold test.

Preserve original readings/photos; leave unknowns blank. Neither an undetected
mass nor a hand-gripped screw establishes passive load retention. Later tests add
low/high positions, signed breakaway/running torque, powered stop/withdrawal and
separate caught-load moving disconnect. Ten minutes is not endurance qualification.

**Illustrative resolution:** equal readings each bounded ±0.5 mm leave drift
[-1,+1] mm. A nominal 3-mm move over one exact turn gives [2,4] mm/turn; three
turns narrow the endpoint contribution to ±1/3 mm/turn but need safe engagement.
The ruler alone does not establish ±0.5 mm: include parallax, blur and support
motion. Do not feed the reducer invented error bounds.
