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

**Concrete measurement discriminator (proposed, not performed):** start with the
unaltered successful pair and its resident seat. Record total supported mass and
load sharing; use the weighed miniature load first, then 5/20-g total-load cases
where physically applicable, with 100 g separately labelled stress. At low/mid/high
usable travel, log height immediately and after 1/10 minutes, reporting instrument
resolution and temperature. Measure signed breakaway and slow running torque in
both directions, then loaded speed/acceleration and powered-stop withdrawal drift.
The ten-minute interval is a screening observation, not endurance qualification.
Only if relevant-load hold fails, compare one documented tighter setting against
the original across multiple pairs/print locations. Retain adjustment only if it
restores holding while the worst measured torque permits the B2 speed/acceleration
envelope without binding; otherwise change the fit/lead/support strategy. Moving
disconnect requires a separate caught-load test and cannot pass from static drift.


Evidence: self-reviewed calculations and executable sensitivity bounds; no new physical tests. The positive owner-reported loaded hold is recorded in E-255 and stage 02.

Verification: frictionless work balance, self-lock boundary, reflected inertia, static-hold/running-loss witness, triangular/trapezoidal motion, and bracketed timing roots. E-255's default output remains byte-identical, including 15,625 ideal replay transitions.

## Measurement readiness and reduction

**New calculation, not a test result:** at a 10-mm perpendicular lever arm,
1 g of tangential deadweight produces **0.09807 N·mm**. A 1-g mass *increment*
therefore brackets onset only to about that width, even with perfect geometry.
For an absolute torque-error allowance of 0.01 N·mm, mass error alone must be
≤0.10197 g at that arm; radius, alignment, tare and friction consume additional
allowance. This is a measurement-design example, not a required instrument or
an accuracy claim. It matters because the illustrative 20-g static-drag threshold
above is only 0.02090 N·mm. A kitchen scale with unspecified uncertainty cannot
resolve that threshold merely because it displays grams. Do not conflate the
model's added-drag parameter with measured total drive torque.

A lever/drum fixture can also change the result: force at a 10-mm arm sufficient
for 0.238 N·mm applies 0.0238 N sideways to the spindle. Do not silently attribute
its changed journal/guide friction to the thread. Preserve the resident seat,
record force direction and **perpendicular** moment arm, include lever/holder tare,
and characterize apparatus effects before inferring intrinsic friction. Known
mass alone does not calibrate a pulley. A finger-turn observation remains useful
qualitative evidence but supplies no numeric torque. Do not make a torque fixture
the prerequisite for the first travel/drift observation.

**First physical record, using the unchanged successful pair if available:**

1. Identify the pair with a present-day photo or label and describe its seat,
   guide and load placement. The forgotten historical calibration variant is not
   required. Record measuring tools, temperature and what is unknown. Weigh the
   miniature and moving pin if possible; otherwise label the load unknown rather
   than inventing a typical mass. A load applied directly to one pin is a one-pin
   test, not the distribution beneath a multi-pin miniature base.
2. At a comfortably engaged middle position, record height against a fixed datum,
   turn the screw one known revolution each way while keeping away from ends,
   and record the resulting heights. Note backlash/direction reversal explicitly.
   Report only reachable, observed travel; do not force 40 or 50 mm from a part
   that may lack engagement margins. No motor or new print is needed.
3. With the normal miniature load and drive removed, record height at 0, 60 and
   600 seconds. Keep the resident seat/guide unchanged and avoid a contact probe
   that supports the pin during the wait. Take the scale image at the same view;
   include parallax/fixture movement in the height bounds. Repeat at low/high
   usable positions later if the first record is informative. This first ten-minute
   screen supplements the owner's successful hold observation; it is not an
   endurance test, high-load requirement or array pass.
4. Only after this record, choose an available torque method and powered drive.
   Record signed breakaway, slow running and loaded speed separately. A manual
   revolution gives effective displacement/turn, **not** the 1500–2000-rpm operating
   envelope or proof of moving-disconnect safety. Continue the separate caught-load
   moving-loss test only with an appropriate supported apparatus.

`tools/curated-experiment-checks/E-256/measurements.py` reduces explicit interval
observations without fitting a friction coefficient or issuing a hardware pass:

- `--blank` emits an empty **unmeasured** JSON record; `--record FILE` rejects it
  until actual observations and provenance/bounds are supplied. Raw records stay
  with the physical evidence. No measurement file is checked in by this study.
- `evidence` is `physical_measurement` or `synthetic`; `specimen`, `setup`,
  `raw_source` and `bounds_basis` identify the actual input and uncertainty basis.
  `total_supported_mass_g` is `[lower, upper]`; use separate records for different
  specimens, loads or fixture configurations. If bounds/load are unknown, keep a
  qualitative observation rather than submitting invented intervals.
- `holds`: each entry has `position` and `observations`, each with `elapsed_s`
  and `height_mm: [lower, upper]`. Start at zero elapsed time. Later signed drift
  bounds conservatively subtract interval endpoints; common bias cancellation is
  not assumed. Equal readings each bounded ±0.1 mm mean drift **[-0.2,+0.2] mm**,
  not zero drift. Output `zero_not_excluded` is not a retention pass.
- `travel`: entries contain `before_mm`, `after_mm`, `signed_turns`, all intervals.
  Effective displacement/turn includes backlash unless it has been taken up;
  intervals containing zero turns are rejected. Specify the signed-turn convention.
- Optional `torque`: entries contain `direction: raise|lower`,
  `observation: no_motion|onset|slow_running`, `force_N` and
  `perpendicular_arm_mm` intervals. Output is **applied apparatus torque** only;
  no automatic parasitic correction, static-threshold fit or motor-speed approval.
- `--check` uses explicitly synthetic controls for signed travel, unresolved and
  resolved drift, torque endpoint propagation, units and invalid input rejection.
  It performs no physical test.

**Decision consequence:** obtain the simplest existing-pair record before buying
measurement equipment or refining screw fits. A coarse unresolved record can
still establish apparatus availability and usable travel; it cannot quantify
holding margin. E-258/E-259's 4096/6400-site, raised-neutral and $500/$1000/$1500
comparisons remain conditional and unchanged. Static drift, applied torque,
loaded high-speed motion and manufacture across a batch remain separate claims.
