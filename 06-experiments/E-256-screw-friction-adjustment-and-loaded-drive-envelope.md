---
status: complete
builds-on: [E-255]
---

# Screw friction adjustment and loaded drive envelope

Reproduce: `python 3 tools/curated-experiment-checks/E-256/drive_envelope.py`.
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

**Decision:** retain B2; source drives around 2,000 loaded rpm with adequate torque
and acceleration. Do not tighten an already holding pair unnecessarily. If needed,
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


Evidence: self-reviewed calculations and executable sensitivity bounds; no new physical tests. The positive owner-reported loaded hold is recorded in E-255 and stage 02.

Verification: frictionless work balance, self-lock boundary, reflected inertia, static-hold/running-loss witness, triangular/trapezoidal motion, and bracketed timing roots. E-255's default output remains byte-identical, including 15,625 ideal replay transitions.
