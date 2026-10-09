---
status: complete
builds-on: [A-015, E-063]
---

# Electroadhesive command contact and channel bound

Stop the tested A-015 implementation: no robust pad case survives at 200/265 V,
and the sourced 12,800-output HV507 implementation costs **$3,217.50 in ICs
alone**, exceeding the entire $500 purchased-hardware ceiling. This does not
reject electroadhesion as a principle. Mechanical preclosure, conformal backing,
lower command force or fewer reusable channels are material changes requiring
new contact and complete-machine accounting. No printing or detailed collet CAD
is justified for the rejected circuit.

Input main `43b06b7`; recovered interrupted E-066 source, then corrected release
voltage accounting and integer-package costing. Reproduce with Python/NumPy:
`python3 tools/curated-experiment-checks/E-066/contact_channels.py --check`.
`--all` emits every case/reason and logical transfer trace; do not retain JSON.
Deterministic Cartesian enumeration, no random seed. Evidence is generated pad
overlap, analytical electrostatics/quasistatic spring bounds, sourced circuit
specifications/prices and **logical** support guards. No physical measurements,
validated compliant contact, assembled mechanism CAD or manufacturing yield.

## Contact representation and uncertainty

Two command pads per site would actuate a mechanically retained moving collet
and a grounded-pawl release link. They are not the payload/service support.
The pad is 2 × 20 mm, translated 0–0.5 mm along its length during a command.
Worst transverse placement reduces width; the final overlap is
`(2−placement) × 19.5 mm`. Removing a strip of a positive force integrand makes
the endpoint the minimum overlap. Pad-level geometry fits within pitch only;
collet, guide, insulation and release-link packaging remain unproved.

Generate two acquisition topologies: a normally open, spring-return rigid pad
pulled closed electrically; and a cam-preclosed pad whose cam withdraws before
shear transmission. The latter changes acquisition, not electrical selection.
Cam motion occurs with command bars stationary and ground support retained;
unselected contacts must open before the bar moves. No cam may unlock unrelated
columns. A rigid pad translates normally; tilt/bow remain prescribed. A flexible
film that flattens, zips or peels is **outside this model**.

| Bounded scenario | Film thickness spread | Placement/open-gap error mm | Roughness pedestal µm | Tilt mrad | Bow µm | Selected friction |
|---|---:|---:|---:|---:|---:|---:|
| Tight | ±10% | ±0.05 | 0–2 | 0–0.5 | 0–2 | 0.3 |
| Middle | ±20% | ±0.15 | 0–5 | 0–1 | 0–5 | 0.2 |
| Wide | ±30% | ±0.30 | 0–20 | 0–2 | 0–20 | 0.1 |

These are explicitly assumed bounds, not sourced X1C priors. Pad coatings need
a separate film/lamination process. Placement includes print bias, assembly and
spatial alignment; spring stiffness has an additional ±20% bound. Film, tilt,
friction and residual charge may shift coherently across a batch/module. The
screen uses weak selected-contact and strong unwanted-contact corners, including
zero-gap/flat contact for the latter; it does not average independent cells.
Warp and contamination can make all sites fail together. PLA layer quantization,
creep, fatigue and backing deformation have not been assigned false precision.

Grid: film 10/25/50 µm; nominal opening 0.15/0.35/0.60 mm; spring stiffness
0.02/0.1/0.5 N/mm; 200/265/500 V; additional residual effective-voltage fraction
0/0.02/0.1/0.3; two acquisition topologies; active-output and passive-half-voltage
addressing; three scenarios: **3,888 cases**, not distinct architectures.
Reject an opening whose lower bound reaches the roughness stop.

For y on the overlap, `u=y/20mm` and
`d(y)=t/3 + tilt*y + 4*bow*u*(1−u)`. Relative permittivity 3 is assumed.
Integrate the ideal air-gap closing force:

```
F(V,g) = epsilon0 * V²/2 * integral_A [g+d(y)]^−2 dA
V_acquire = max_x sqrt(k_max*x / F(1,g_max−x))
F_command = mu_min * max(0, F(V,g_stop)−k_max*(g_max−g_stop))
```

Require ≥0.05 N command shear, <0.01 N unwanted shear, and positive spring
separation margin after shutdown. Those are mechanism scenarios, not measured
latch forces. Strong-contact unwanted friction is bounded by 0.6. An active
output uses a conservative 35-V off bound; passive half-selection uses V/2.
The latter is a comparison mutation, not A-015's proposed active array.
For release, the effective residual voltage is **35+rV** for active channels
and rV for an ideally grounded passive array. Adding fields with the same sign
is deliberately conservative. Spring separation must exceed its electrostatic
force at the strongest contact corner. Residual fraction is not a time constant
or fitted polarization model; zero r does not erase circuit off voltage.

The free-pad acquisition criterion is quasistatic, not an inertial snap-through
simulation. Flat pads independently give the familiar zero-film threshold
`sqrt(8*k*g0³/(27*epsilon0*A))`. Dynamic overshoot, fringe fields, charge leakage,
peel, adhesive chemistry and dielectric failure are omitted. These omissions
prevent any physical pass, although explicit bounded bad cases and circuit cost
can still reject the tested implementation.

## Results and mechanism consequences

Each topology/address/scenario group contains 324 cases. Every group retains
zero except **preclosed/active/tight: 4/324**. All four use 10-µm film and 500 V;
none passes at 200/265 V or under middle/wide bounds. The four are two parameter
settings at r=0 and 0.02:

| Nominal gap mm | k N/mm | Selected shear N | Maximum additional r | Two-array spring-closing force N |
|---:|---:|---:|---:|---:|
| 0.15 | 0.5 | 0.07003 | 0.02018 | 1,520.64 |
| 0.60 | 0.1 | 0.08234 | 0.02458 | 995.33 |

Closing-force totals are 12,800 times the worst modeled spring force; cam
friction/structure add load. Serial closure reduces simultaneous load only by
adding schedule and retained-contact requirements. These four are necessary
pad survivors with no compatible sourced 500-V driver, dielectric breakdown
margin or complete support geometry, not viable machines. Passive half-selection
has no robust survivor: a favorable selected pad does not guarantee low drag
at stronger neighboring contacts.

A tight 10-µm/0.35-mm/0.1-N/mm witness at 265 V supplies only **0.01536 N** shear
and requires **2,699 V** quasistatic free acquisition. Preclosure removes that
acquisition barrier but not the weak shear. Set only its tilt and bow to zero:
shear becomes **0.09612 N** at the same 2-µm roughness pedestal. Thus a conforming
film can reverse the force conclusion; the screen must not be generalized to
all electroadhesive clutches. Its conformity and release require a different
mechanical model. [Rauf and Follmer's experiments/model](https://shape.stanford.edu/research/ModelingElectroadhesive/ModelingElectroadhesive.pdf)
show that polarization and contact dynamics matter; their fast laboratory
switching is not transferred to this field or substituted for release evidence.

The required sequence remains ground supported → acquire/prove positive moving
grip → unload and withdraw ground pawl → move → seat/prove ground support →
reset moving grip. Unchanged sites keep ground support. The script enumerates
25 old/new height pairs at 0/10/20/30/40 mm and refuses unsafe logical transfers
on failed grip, latch or release proof. **It does not solve collet or pawl
contacts**; that work stops at the decisive cost gate. A stuck command inhibits
shared motion. Failed deposition retains moving support and requires a module
service catch before power removal; persistent faults are not successful updates.

## Circuit, cost and full-board ledger

Sources accessed 2026-10-09. [Microchip HV507 DS20005845A](https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/20005845A.pdf)
specifies 64 latched push-pull outputs, 300-V recommended maximum supply and
8-MHz clock. At 300 V, 25°C and ±1-mA output tests, high is at least 265 V and
low at most 35 V. These loaded limits motivate the conservative voltage cases;
they are not measured steady-state pad voltages. Static HV supply current is
at most 0.5 mA/package with all outputs high or low. The 500-V cases exceed this
part's rating. Outputs are individually commanded, not galvanically isolated.

[DigiKey's HV507PG-G listing](https://www.digikey.com/es/products/detail/microchip-technology/HV507PG-G/4902491)
shows $16.08750 each at 100+ in USD. Two channels/site require 200 packages:
**$3,217.50**, excluding PCB, supply, logic, connectors, electrodes, motors,
readback and mechanical parts. The [manufacturer's 5K indicative table](https://www.microchipdirect.com/chart.aspx?branchID=9021&mid=11)
gives $14.47, still $2,894 for 200 chips if that unattained volume price were
available. Its 128-channel HV583 at $11.38 gives $1,138 for 100 chips, but the
[HV583](https://www.microchip.com/en-us/product/hv583) operates at only 80 V;
it is a cost counterfactual, not a voltage-compatible substitute. No sourced
complete channel exists below these component floors for these circuits.

With $250 explicitly reserved for everything outside the selector, $500 permits
$0.01953 per complete command channel or $1.25 per 64-output package even if all
other selector material were free. Even granting the 100+ unit price to a smaller order, $250 covers only 15
complete packages, at most **480 two-channel sites**, before other selector
costs; that smaller-order price is not an offer. Reusing fewer outputs needs physical multiplexing/isolation and a new
schedule; simply changing the channel count does not implement that machine.
A different custom/discrete circuit has unknown cost, not this proven floor.

200 packages add 16,000 solder pins. Assumed 10–50-mm individual output runs
sum to 128–640 m, excluding return/supply/data. Thin-film interfaces, springs,
collets, pawls and guides remain repeated precision/assembly burdens; no printed
material/time or repair advantage over the mechanical comparators is established.

One ideal flat nominal 10-µm pad has 106.25 pF capacitance. At 265 V, 12,800 pads
store 0.04775 J and require 0.3604 mC per full charge; an ideal resistive-source
step supplies 0.09551 J. Parasitics/film spread increase this estimate. Small
stored energy does not establish low power: the datasheet static-current bound
across 200 packages is 30 W at 300 V, excluding logic and dynamic loss. Naively
charging every output at 1 mA calls for 12.8 A peak; staggering and slew control
must be designed, not assumed. A single data chain takes 1.6 ms at 8 MHz before
latching/output settling. Electrical transfer time is not contact-release time.

Retain E-063's explicitly assumed full-field schedule: 0.6-s preposition,
eight 0.28284-s legs, nine contact events and 6 s preparation/registration/read/
settle/recovery. Each complete event must be **<2.3486 s** to meet <30 s.
Dwell 0.02/0.2/1.4/2.4 s gives 9.043/10.663/21.463/**30.463 s**. Cam closure,
discharge, proof and reset all belong in event dwell. Local updates still move
the shared elevator; unchanged columns must stay locked and frame deflection
is unquantified. At assumed per-site false acceptance 1e−3/1e−4/1e−5, expected
misses are 6.4/0.64/0.064; this expectation needs no independence, but board
success probabilities require a correlation model. Neither reader performance
nor production reliability is established.

## Verification and stopping rule

Self-review checks ideal flat force, overlap loss, vanishing far-gap force,
closed-form pull-in against independent dense maximization, and force against
a finite-difference derivative of capacitor energy. The 64/128/256/512 spatial
and 201/401/801/1601 opening grids converge; refining the entire population
128/401→512/1601 changes **no classification**, maximum relative force-integral
change 7.65e−5 and acquisition-voltage change 3.46e−6. Numerical agreement does
not validate the prescribed contact shape or release model.

Stop flat-pad/HV507 full-field development. Reopen only with a materially changed
contact/command mechanism **and** a complete affordable addressing path; lower
command force alone cannot repair this circuit's cost. No calibration print can
resolve the sourced cost failure. The campaign comparison belongs in ADR-012.
