---
status: complete
builds-on: [E-110, E-126, E-158, E-195]
---

# Stored electrochemical matter: bulk growth is slow; gas is compliant; keys still need clearance

**Stop end-grown copper and ungated gas as sole support; deprioritize full-strip
keys under the reference rate/clearance scenarios.** Continuous key sizing finds
a 25.06-s extreme corner; it has no qualified rate, geometry or joint. Chemistry
changes how state is written, but no complete-machine advantage is established.
A micron chemical switch controlling a dry support is a different, unbuilt route.
No architecture, purchase or print selected.

Input main `84da421`. Reproduce:
`python3 tools/curated-experiment-checks/E-196/stored_matter.py`.
Standard library; deterministic analytical/finite-section screening, self-review.
No electrochemical transport simulation, assembled CAD, calibrated process prior,
measurement, lifetime qualification or sourced BOM. All loads, strength, error,
current-efficiency and timing allocations below are scenarios unless attributed.

## Discovery and complete causal routes

Two independently useful source domains: reversible electrodeposition (dynamic
windows/electroforming) and electrolytic MEMS. Recombining electrodeposition from
whole support into only a key is a functional change, not a third independent
literature search. Repository searches found no electrochemical/electrodeposition/
electrolysis result. E-110 already changes material phase in a keyed collar;
E-126 transports solid supports; E-158 retains hydraulic inventory. The changed
functions are material creation/removal and charge delivery, not
grounding a load. No saturation claim.

| Hypothesis | Addressing, motion and memory | Load, observation and recovery |
|---|---|---|
| End-grown strut | Individually switched electrode grows/dissolves a copper rod in a lateral guide; growth lifts the top, dissolution lowers it. Deposited length is retained matter. | Top → rod → grounded electrode; actual height and continuous compression contact must be read. Cut during dissolution stops electrical removal but corrosion/contact continuity remain unproved. Replacing a broken deposit requires temporary support and electrolyte access. |
| Gas inventory | Per-cell electrodes generate gas in a sealed piston/bellows chamber; commanded recombination or fuel-cell consumption lowers it under load/down-bias. Gas amount is the proposed memory. | Top → gas pressure → chamber/frame. Read actual height/pressure, not integrated current alone. Catalytic reset can continue after power loss; gas separation plus switched recombination requires additional barriers. Venting spends inventory and needs refill. |
| Plated key | A selected captured setter unloads an annular key, electrochemically strips it, moves the conductive shaft 40 mm, and plates a new key into a stationary insulating housing groove. | Shaft → bonded metal key → groove lip → frame. Prove height, engagement and load transfer before releasing setter. Cut mid-strip/replate leaves the setter carrying the load; its independent arrest is still owed. |
| Controls | Dry retained support plus direct setter; E-110 thermal key; E-126 solid feed. | These avoid charge-limited metal growth, but retain their documented capture, force, routing, arrest and cost problems. None is promoted by this screen. |

All need electrode addressing, contacts, containment and service access. Crossed
wires owe a bidirectional selector; shared electrolyte permits ionic cross-current
and shared gas permits height exchange. No regional-isolation pass is assumed.

## Primary-source anchors and transfer limits

Accessed 2026-10-11; no source establishes X1C capability:

- [NIST density](https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=029&mode=text)
  and [molar mass](https://webbook.nist.gov/cgi/cbook.cgi?Name=Copper):
  copper 8.96 g/cm³, 63.546 g/mol. F=96,485.33212 C/mol; Cu(II) assumed.
- [Janssen, pp.339–346](https://pure.tue.nl/ws/files/2271764/620039.pdf):
  9-mm bar in acidic CuSO4 with controlled circulation/temperature; efficiency
  depends on flow and falls at high current. Includes around 1.5 A/cm²;
  **10 A/cm² below is an extrapolation**, not a process ceiling or proven rate.
- [Mariani et al.](https://www.nature.com/articles/s41598-022-22650-x): indexed
  primary text reports 17.5 A/dm² DC limiting density for its bath, motivating
  the .175-A/cm² scenario. Full-page access blocked; no other parameter used.
- [McAndrews et al.](https://onlinelibrary.wiley.com/doi/10.1002/aenm.202202843):
  stress/delamination in Cu–Bi window films, different Bi behavior. Nanofilms
  establish neither structural joint strength nor terrain-service life.
- [Sheybani and Meng](https://biomems.usc.edu/publications/2015/2015_SNB_RecombinationAcceleration.pdf):
  catalyst area, gas transport and orientation affect recombination; no rate transferred.
- [Uvarov et al.](https://arxiv.org/pdf/1801.00481): fast cycles in a microfabricated
  500-µm-diameter, 8-µm-deep chamber rely on gas termination after switching off.
  Fast reset is not retained height or demonstrated 40-mm travel.

## Copper conservation and front speed

With volume in mm³, `Q/V = 2 F rho/M = 27.208906 C/mm³` at unit efficiency.
For current density j in A/cm², uniform advancing-front speed is
`v = eta*j/(100*27.208906)` mm/s. Smaller cross-sections reduce current,
**not axial growth time** at fixed j.

At j=.175/1/10, a 40-mm end-grown strut needs **621,918 / 108,836 / 10,884 s**
for growth alone. This assumes perfect mass transport/morphology, no competing
reaction and immediate compression contact. It fails <30 s before reset, readback
or assembly. Hollow sections reduce inventory, not end-growth distance. Growth along a
scaffold changes topology and owes its own front/load path.

Inventory sensitivity grants pinned circular struts at E=110 GPa and 100-MPa
stress bound: `A=max(W/100,sqrt(4 W L²/(pi E)))`. At .1/1/10 N, diameters
.234/.416/.740 mm require 46.84/148.11/468.37 C per cell. Even lateral guidance
removing Euler buckling cannot repair end-growth time. These are bulk-like
scenarios, not electrodeposit allowables. Current sums reported by the code are
not necessarily bus current: series wiring exchanges current for voltage and
arbitrary-map bypass. Reaction charge does not disappear.

## A finite annular key still spends charge crossing its clearance

Generated axisymmetric section: shaft radius r=1.2 mm; frame lip begins at r+c;
groove ends at r+c+k; axial groove width w. Deposit fills the annulus from r to
r+c+k inside 0≤z≤w. Ground lip occupies w≤z≤w+1 and extends .5 mm radially
outside the groove. Favorably grant an adherent dense metal deposit, rigid frame,
electrolyte access during growth/stripping and controlled radial current density.

For c=k=.05,w=.25 mm, the parked ring has zero overlap with the lip; translating
it upward .01 mm creates **.00400553 mm³** intersection, a real geometric stop.
After complete stripping to r, the shaft clears the lip over all 40-mm travel;
radial separation makes this true continuously, not only at sampled endpoints.
This is a finite section witness, not a housing/seal/captured-writer CAD assembly.
Downward seating uses the corresponding lower lip. Bond failure and creep are
not bounded by positive engagement at the housing.

Ideal shear/bearing screening uses
`min(2*pi*r*w, pi*((r+c+k)²-(r+c)²))*S`, with S=10 MPa, **not an allowable**.
The nominal section gives 4.006 N. Its deposit is .19635 mm³, **5.34246 C**.
Full stripping plus regrowth time is `2(c+k)/v`; grant stripping the same favorable
normal speed as growth, with no shielded metal, roughness or residual key.

| j A/cm² | Conditional map time including 6 s overhead |
|---:|---:|
| .175 | 3,115.59 s |
| 1 | 550.18 s |
| 10, deliberately extrapolated | 60.42 s |

The optimistic 6 s covers preparation, captured motion, registration, settling,
verification and one short retry; it is not a built schedule. Parallelism cannot
reduce the per-key reaction dwell.
Nominal round-trip board charge demands **2,849 A summed cell current** over
24 s; power/flow/temperature hardware and unsupported input-loss arrest remain.

A deterministic 1,080-case grid uses c=.005/.01/.025/.05/.1; k=.01/.025/.05/.1;
w=.1/.25/1 mm; j=.175/1/10; eta=.5/1; radial surface error e=.005/.025/.05 mm.
Enumerate eight shaft/lip/groove-radius corners ±e; require clear/engaged radial
geometry, .5-mm frame allocation inside 5.08-mm pitch and ≥1-N ideal capacity.
Coherent batch/registration errors can realize adverse corners; no IID yield.
Reaction times use nominal dimensions; transport/error penalties remain omitted.

At e=.005/.025, fastest surviving grid cases take **33.209/114.836 s** at
j=10,eta=1. At e=.05 none clears the radial margins. **Grid failure is not a
continuous-design rejection.** An independent continuous sizing holdout chooses
c=2e+.001, w=max(.1,1/[2*pi*(r-e)*S]+.001), and
`k=e+sqrt((r+c+e)^2+1/(pi*S))-(r+c)+.001`, for W=1,S=10.
The added .001 mm is an explicitly unqualified reserve. Exact radius corners
verify capacity >1 N and positive clearance/overlap:

| e mm | c / k mm | Map time at j=1 | At j=10, eta=1 |
|---:|---:|---:|---:|
| .005 | .011 / .024019 | 196.56 s | **25.06 s** |
| .025 | .051 / .063413 | 628.61 s | 68.26 s |
| .050 | .101 / .112730 | 1,169.07 s | 122.31 s |

The fine case escapes the coarse grid, but eta=.5 alone raises it to **44.11 s**.
Its .1-mm-wide deposited ring, 1-µm clearance reserve, 5-µm surface-error bounds,
10-A/cm² local process, adhesion and complete access are unqualified. There is no
X1C or assembly pass. At j=1, <30 s requires c+k<**.0044103 mm** with the 6-s
allocation, before strength/margin. Keep the extreme corner visible; do not
fabricate to a nominal analytical timing pass.

Leaving a conducting seed or stripping only a fracture neck changes the model:
a 1-µm normal switch layer has ideal round-trip time **31.10/5.44/.544 s** at the
three j values, before overhead. It still needs an actual reusable supported
joint, solvent access and clearance for motion. An electrically conducting filament
is not automatically a structural bond. A micron switch driving a dry latch
moves the load into a separate support and must be compared as a command actuator.

## Gas: conserved inventory is not conserved height

Grant ideal gas at 298.15 K, ambient pressure P0=101,325 Pa, frictionless sealed
piston area A, a 1-mm-equivalent dead volume and fixed downward load W.
`P=P0+W/A`; mixed H2+O2 production gives `n=3Q/(4F)`.
The additional 40-mm stroke needs `Q=4F*P*A*.04/(3RT)`; eta=1, no dissolved gas,
no ongoing recombination or membrane force. Existing dead-volume gas is retained.

For a 2-mm bore at W=.1/1/10 N, stroke charge is **.868/2.737/21.419 C/cell**;
24-s board sums are **232/730/5,712 A**. The stroke displaces 125.664 µL/cell,
**804.25 mL/board**. This is no microchamber scale transfer. Larger/tiered cylinders
are allowed by the product constraints; their gas volume, charge and routing count.

At fixed gas amount, adding ΔW gives
`h_new+hd=(h+hd)*(P0*A+W)/(P0*A+W+ΔW)`.
For ΔW=.1 N and h=40, drops are **7.910/2.891/.394 mm** at the three loads.
A 4-mm bore still drops **2.783/1.728/.360 mm**. These are equilibrium changes,
not predicted oscillation peaks; membrane elasticity, leakage and temperature
are omitted. No stage-02 numerical deflection acceptance is invented.

As a sensitivity target only, ≤.1-mm drop for ΔW=.1 needs P0*A+W≥**40.9 N**.
At W=1, an atmosphere-referenced piston would need radius **11.196 mm** (22.39-mm
bore). At 2-mm bore it instead needs about 39.58 N extra downward preload,
with a corresponding internal reaction per cell; antagonistic pressure changes
this equation but adds a second containment/load path. A stiff mechanical seat
or isolating hydraulic lock returns to a separate retention architecture.

At fixed W and n, a shared +5 K temperature change moves h by **+.688 mm**.
Under an explicitly hypothetical first-order gas loss, n=n0 exp(-kt), h+hd follows
that same decay. Half-lives 30/300/3600 s produce .1-mm lowering in
**.106/1.057/12.683 s**. These are competing bounds, not empirical rates.
The zero-loss control retains gas but still exhibits load/thermal compliance.
Fast recombination improves commanded reset while worsening source-loss retention
unless separately gated. No latch is smuggled into the gas model.

## Board consequences, verification and disposition

All keep 6,400 guided tops, 40-mm travel and local chemical interfaces, with
at least two electrode surfaces, containment and addressing/site. Keys still need
setters; gas needs pressure boundaries. Electronics, wiring, sensors, circulation,
reservoirs, seals, supplies and service fittings count as purchases. With an
assumed $250 shared reserve, $400/$500 totals leave **$.02344/$.03906 per site**
before setters; this is a threshold, not a BOM. One 10-s operation/site means
17.8 h assembly. Print mass/time/scrap are unestimated: no complete geometry gate.

Actual top/support readback is required; charge cannot distinguish side reactions,
porosity, dissolution or partial keys. A hypothetical false-acceptance rate 10^-4
means .64 expected misses/board without independence; common bath/reader errors
are not cured by retries. Key proof failure keeps the setter captured and owes
independent arrest. Gas service needs temporary top support and chamber isolation.
No supported module-extraction path is built; persistent faults are outside the
successful-map allocation. No service or power-loss pass.

X1C hole shrinkage, warp, layers, first-layer growth and alignment affect
clearance. Wet morphology, stress, corrosion, adhesion and voids affect keys;
housing anisotropy, leakage, creep and fatigue remain unqualified. The bounds
are not process priors. No yield, lifetime or physical reliability estimate.

Self-review verifies Faraday mass balance independently, exact integrated charge
on a growing cylindrical area (1/10/100/1,000 subdivisions; residual <5e-15 C),
Euler/stress back-substitution, continuous key-sizing holdouts against the grid,
finite lip collision/clear state, gas conservation,
zero stroke/load increment and finite-difference stiffness convergence. These
validate the reduced equations and section witness, not electrochemical transport
or physical performance. No dynamical solver pass or external review is claimed.

**Close this bounded discovery campaign.** Stop end growth on timing and ungated
gas as sole memory on load/source-loss dependence. Deprioritize reference-rate
keys; retain the extreme synthesis corner as conditional, with no machine pass.
Keep the micron-switch hypothesis as an unresolved command route. Reopen support
chemistry with changed front topology,
measured effective thickness/rate plus mechanically credible bond/clearance, or a
separate pressure isolation that beats the dry control after full accounting.
Next valuable comparison: use fast small chemical stroke only to command a
backed dry support, versus magnetic/thermal command controls; first construct
quiescent and source-loss states, address/reset and sealed force transmission.
Reject duplicate local-control burden before detailed chemistry or fabrication.
