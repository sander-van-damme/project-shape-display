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

**Decision:** retain B2 as a conditional comparison, not a selected architecture.
Its present sample suggests drives around 2,000 loaded rpm with adequate torque
and acceleration. Before selection, compare playable river/ravine encodings and
obtain owner/player feedback: raising surrounding land to depict water is optional,
not a required workload. Recompute the envelope if that representation changes.
Do not tighten an already holding pair unnecessarily. If needed,
find a batch setting whose weakest hold and strongest breakaway/running torque
both fit the measured load and selected drive curve. Common bias, local variation
and wear can close that window; no yield distribution follows. Avoid 6,400 hand fits.
Reuse the existing pair/seat: identify dimensions/travel, weigh miniature/pin,
record timed low/mid/high-position drift, then breakaway/slow running torque.
Separate powered stop/withdrawal from unexpected moving loss. If specimens are
unavailable, use a documented small calibration family after resolving dependency
and engagement; do not demand impossible historical provenance or blindly print
trial 5. No print is selected here. This informs shared tooling or batch fabrication
comparisons; it does not qualify molded, machined or printed production.

## Measurement method and reduction

Reuse the unchanged pair before altering fit or buying equipment. After the first
middle-position record below, repeat low/high positions and measure signed
breakaway/slow running torque, then loaded speed and powered-stop withdrawal.
Only if relevant-load hold fails should one documented tighter setting be compared
across pairs/print locations. Moving disconnect needs a separate caught-load test.
Ten-minute holding is a screen, not endurance or array qualification.

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
The widths are estimates, not tolerance intervals. No measured travel, timed
drift or torque record has yet been supplied.

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

### First check with the available tools

1. Reassemble the original setup if its support/guide is available. Record what
   prevents the pin rotating, what supports the screw axially, and whether the
   screw is free to rotate when the fingers/driver are removed. If only the two
   loose parts remain, report that; do not balance a miniature on them or call
   a hand-held check passive retention. A short assembly photo/video is useful.
2. At a comfortably engaged position away from either end, place the ruler
   beside the pin, fixed relative to the support. Keep ruler marks and the observed
   pin edge as close to the same camera depth as possible. Rest the phone in one
   position, looking squarely at both. Record the starting reading, one complete
   screw turn, and one complete return turn, keeping the pin from rotating.
   Include the viewing direction, any lost motion or binding, and what the hands
   touch. Do not force an end stop. One turn is enough initially; a longer counted
   move is useful only after clearance/engagement have been established.
3. Only if the assembly stands and supports a load without hands, use a stable
   ordinary miniature/load in the original arrangement. Record its scale reading
   and smallest displayed increment, or “not detected.” Include any cap/holder
   mass and other supports; do not assume all miniature weight reaches this pin.
   Remove the drive and hands, then record the same edge at 0, 60 and 600 seconds.
   If there is no stable load placement, stop after the unloaded motion record.
   A screw clamped against rotation tests that fixture's holding, not freely
   released screw retention. No torque apparatus or new print is needed yet.

Return format: `support/guide and hand contacts; h_start; h_after_one_turn;
h_after_return; load reading/scale increment or unknown; h_0/h_60/h_600 or not
performed; slip/binding/rotation notes`. Preserve original photos/video as raw
evidence. A coarse readable result is preferable to invented decimal places.

**Resolution calculation, not observed accuracy:** if each reading can eventually
be bounded to ±0.5 mm, two equal readings leave drift in [-1,+1] mm. A nominal
3-mm displacement over one exact turn would then mean [2,4] mm/turn; three turns
would narrow the same endpoint contribution to ±1/3 mm/turn, but require more
safe travel. A millimetre ruler alone does not establish the ±0.5-mm bound:
parallax, edge blur and support motion must also be included. Do not populate the
reducer with guessed mass/height bounds. Unknown load can accompany a useful raw
motion observation; it cannot establish a quantified load-retention margin.
