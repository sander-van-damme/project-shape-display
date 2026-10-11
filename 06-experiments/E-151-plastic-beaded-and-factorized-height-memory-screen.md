---
status: complete
builds-on: [E-130, E-131, E-133, E-134, E-135, E-150, E-120, E-148, A-023]
---

# Permanent forming changes memory physics; shared support does not erase local state

**Stop common-tie arch retention and low-order separable support. Retain plastic
forming through a stationary guide for a finite-path discriminator.** Irreversible
material work changes E-133's elastic-front physics, but hysteresis proves neither
static hold nor input-loss arrest. No machine, material or print selected.

Input main `09022de`. Run `python3 tools/curated-experiment-checks/E-151/memory.py`
(standard library, about 5 s; JSON disposable). Evidence: sourced analogies,
constitutive calculation, algebraic counterexamples and bounded scenarios;
self-review. No complete CAD, contact dynamics, calibrated X1C prior, measurements,
fatigue prediction, sourced BOM or independent review. Except for stage-02 limits,
all numerical inputs are assumptions, not material allowables or process priors.

## Discovery and causal combinations

Three distinct axes: permanent material forming, shared tensile confinement and
support-field factorization. Reworded knitting/patent searches supplied no further
principle and are not independent attempts. No saturation claim.

Primary analogies, accessed 2026-10-11:
[Charpentier et al.](https://arxiv.org/html/2412.06022v1) use localized plastic hinges,
springback and increased stretch to obtain subsequent shapes; this does not prove
arbitrary bidirectional cycling or lifetime.
[Dreier et al.](https://www.nature.com/articles/s41467-025-61809-8) link bead
superjamming to geometry, thread tension, friction and boundary constraints;
clamped ends matter. Our strip/arch constructions below are hypotheses, not their
machines. An optical-superposition search supplied no mechanical evidence for the
third, independently derived construction.

Cross-check: E-130/131 assembled compression support lacks input arrest; E-133/134
leave elastic-front/track coordinates free; E-135/136 command addressing supplies
no service retention. E-120–122 relocate locks into cable lengths; A-002/A-022
already encode structural state. A-023 does not provide independent tops with
vertical steps. None supplies the changed plastic law or counterexamples below.

| Combination | Selection + signed energy | Memory + grounded load path | Observation / recovery obligation |
|---|---|---|---|
| Plastic front | Indexed bank of bilateral heads pushes/pulls strip tails through fixed alternating bends into vertically guided tops. Motor supplies lift and forming work; lowering may return energy. | Deformed strip and bending resistance proposed as continuous memory; strip compression → fixed former/guide → frame. No release command; buckling and tail capture remain real hardware. | Actual top plus feed/guide force; cut/hold proof before undocking; stay captured on failure. Independent abort and supported cartridge replacement required. Recoil, breakage recovery unbuilt. |
| Common-tie arches | Bank heads change selected arch spread/height; perimeter tensioner manages shared slack. Both directions need bilateral force. | Rigid beads/struts → grounded feet; common tie constrains total spread, proposed as shared lock. | Read top and local slack/spread. Tie cannot isolate failed arch; separate keepers restore repeated retention. |
| Separable supports | Edge screws retain reversible row/column coordinates. Series translation adder at each crossing gives a+b; top rests on highest of K tips. | Positive seat → adder → retained rails → frame. K guided tips/adders per top; captive/down-biased follower needed for lowering. | Read actual tops/contacts; prove receiving support before withdrawing donor. Rail faults affect up to 80 cells; backup arrest, bypass and handover unbuilt. |
| Controls | E-131 threaded rotary heads; E-148 drive field opens a local spring jaw during signed motion. | Thread friction / returned jaw and grounded thrust/bracket. | Existing speed, capture, friction, gap, field-decay, readback and coast limitations remain; no new pass. |

Broadcast writing still owes physical local gates, half-selection and reset.
Unchanged sites are not commanded, but shared frame/guide motion can disturb them.

## Plastic front: derive dissipation, do not assign a brake

Grant rectangular strip width b, thickness t, modulus E and symmetric
elastic-perfect-plastic yield stress sy. Frictionless guides impose
`0 → +1/R → 0 → −1/R → 0` curvature per millimetre fed. Straight entry/exit,
four supported contact stations, no tension or ovalization are assumptions,
**not constructed contact geometry**. Outer strain e=t/(2R), yield strain ey=sy/E.
Each stabilized fiber at y loses `4 sy max(|y|/R−ey,0)` per unit volume/cycle.
Section integration gives work per transported length [N mm/mm = N]:

`Ccycle = b sy/R * max(t−2 sy R/E,0)^2`.

Rigid-perfect-plastic limit: `b sy t²/R`. In an established spatial front with
unchanged elastic inventory, Ccycle is mean feed resistance, not minimum
instantaneous resistance, startup force, reversal force or parked capacity.
Elastic material dissipates zero. The symmetric law gives equal stabilized loss
for either cycle direction; hardening, Bauschinger effect, softening, cracking and
creep are omitted. Virgin forming/residual stresses can differ.

Independent fiber return mapping integrates stress work, plastic heat and stored
energy for three cycles. Nominal E=200,000 MPa, sy=200 MPa, b=3, t=.25, R=3 mm
is a **generic metal-like scenario**: **11.9072 N**, **4.167% outer strain**.
32/64/128/256 fibers and increments/quarter-cycle give
11.9000/11.90654/11.90654/11.907196 N. Work−heat−elastic-energy residual magnitude
falls .01471→.000223 N per mm; elastic-only and rigid-plastic limits pass.
This verifies the section law, not transport or lifetime.

For b≤3, t≤.4 mm and total-strain scenario caps, best section uses maximum b,t
and R=t/(2 cap). Caps are not fatigue allowables:

| E / sy MPa | .5% cap; R=40 mm | 2% cap; R=10 mm |
|---|---:|---:|
| 2,000 / 20, polymer-like | 0 N | .240 N |
| 2,000 / 50, polymer-like | 0 N | 0 N |
| 200,000 / 200, metal-like | 1.536 N | 8.664 N |
| 200,000 / 500, metal-like | 1.500 N | 18.375 N |

Stop these polymer sections **as ≥1-N steady dissipative brakes** under these
caps; this is not a static-capacity bound or rejection of all polymer memories.
Metal-like cases straddle 1/10-N scenarios. Larger/more bends change inventory;
80-mm-diameter formers at 6,400 sites need tiered routing (internal pitch is free).

32 coherent corners use b=2.9/3.1, t=.20/.30, R=2.8/3.2 mm, E=160/240 GPa and
sy=160/240 MPa. Mean resistance **5.435–23.030 N**, outer strain **3.125–5.357%**:
common weak thickness/material defeats 10 N even in the mean model. Corners are
bounds, not yield. Printed die shrinkage, layer quantization, first-layer swelling,
warp and frame/assembly error change imposed curvature. Die anisotropy/interlayer
weakness/creep affect support; friction, wear, edge damage, metal thickness/yield
and residual curvature need their own evidence. No IID or calibrated prior.

A favorable constant-drag surrogate requires C>W for downward arrest, with coast
`m v²/[2(C−W)]`: nominal C, W=10 N, m=1.1 kg, v=.1 m/s gives **2.884 mm**;
W=0, m=.02 kg gives **.00840 mm**. Generalized masses are scenarios; no allowable
drop is invented. This is **not a front bound**: recoil, unloading, buckling and
changing contact precede steady forming. Finite geometry with free input must
establish equilibrium and cut dynamics. Plastic work supplies no positive seat.

## Common tie: unstable exchange survives infinite cable stiffness

Grant two rigid symmetric arches, each two struts length l, with sliding grounded
feet, half-span r and `h=sqrt(l²−r²)`. A common inextensible tie fixes r1+r2;
actual base-length factors of two do not remove the free exchange coordinate.
For q=r1−r and r2=r−q under downward loads:

`V(q)=W1*h(r+q)+W2*h(r−q)`.

Equal positive loads give V'(0)=0 but `V''(0)=−(W1+W2)*l²/h³<0`.
The tie stores no energy in this constant-length mode. At l=4,r=2 mm and 1 N
on each top, curvature is **−.769800 N/mm**; .5-mm redistribution releases
**.097605 N mm**. At W1=1,W2=10 N, initial slope is **5.19615 N**: no equilibrium.
All 12 coherent l=3.9/4.1, r=1.9/2.1 mm, W=.02/1/10 N cases remain unstable
(curvature −8.57084…−.014021 N/mm). Finite differences converge to derivatives.

At zero load the mode is neutral; .02-kg generalized mass at .1 m/s retains
.1 mJ kinetic energy. Closing the tie cannot arrest it; editing moves the neighbor.
This rejects **one-common-tie retention**, not bead materials generally. Local
seats/ties/friction may repair it but restore E-120/122-style repeated retention.
Stop before 40-mm/full-board construction: assumed friction or stationary writer
cannot repair the stated geometry-only claim.

## Separable support: worst-case reach restores replication

Grant perfect `h_ij=max_k(a_ik+b_kj)`. Each series adder has two grounded retained
rail coordinates; highest-contact selection is passive. Plain row+column sums
cannot raise one isolated cell; max is the changed escape.

Request 40-mm diagonal cells and 0-mm off-diagonals on the 80×80 board. One term
covering diagonals i,j obeys `(a_i+b_i)+(a_j+b_j)=(a_i+b_j)+(a_j+b_i)`.
Left side is 80 mm; right cannot exceed zero. Each term covers at most one
diagonal: **K≥80**. With final absolute height error e, contradiction remains
for `80−2e>2e`, i.e. **e<20 mm** (not a product tolerance). Adder errors cannot
rescue low rank inside this bound; nonseparable geometry changes representation.
Source constructs exact K=n witnesses at n=2,8,80 and checks rectangle identities.

Literal K=80 needs **12,800 physical rail registers** (12,720 independent after
gauge offsets) and **512,000 tip/adders**. With $250 shared reserve, registers
alone get <$0.01953 each under $500; not a quote. Rail support/bypass, frame,
handover, proof and fault recovery remain. Stop low-order detailing on missing
reach; this does not prove all shared memories need 6,400 locks.

## Full-board ledger and decision

Plastic front retains 6,400 tops at 5.08-mm pitch, 40-mm travel, strips, guides,
formers, capture interfaces and replaceable tails. Four contacts/site means
**25,600 wear stations**. An assumed 80×3×.25-mm strip/site totals **.384 L**
before tails/scrap; 10–30 s/former assembly totals **17.8–53.3 hours** before
columns, calibration and repairs. No routed geometry or lifetime pass.

Assume .10 s/cell for capture/read/cut-proof/withdrawal and 6 s/map for preparation,
registration/indexing, final proof, one bounded retry and settling. Optimistic
`T=6+ceil(6400/H)*(.04/v+.10)` at v=.05/.1/.2 m/s requires **247/137/82 heads**
for strict <30 s. Separate 40-mm empty returns raise that to **458/247/137**.
Proof time/acceleration are unearned. At .1 m/s without return, free cells and
$250 elsewhere leave **<$1.825/head**. Joint condition:
`6400*c_cell+H*c_head<250`; free heads leave **<$0.03906/site**. A $400 total
leaves $150; the $200 ideal is exceeded by the assumed reserve alone. Motors,
readers, abort, electronics, wiring, bearings, power, guides and fasteners all
count. No sourced BOM or purchased-cost pass.

Nominal plastic loss/full 40-mm map: **3,048 J**, plus **256/2,560 J** useful work
at all-cell 1/10 N; loads are scenarios, not requirements. Nominal lowering at
10 N dissipates more than released gravity work; weak corners can need absorption,
strong ones higher drive power. All-cell frame loads are **6.4/64 kN**. Shared
frame deflection, seams and vibration can disturb unchanged sites; section law
bounds none. Assumed false acceptance p=1e−4 gives **.64 expected misses/board**
without independence; common bias defeats retries. Failed proof retains capture
for one supported retry. Broken strip/guide or persistent jam needs unbuilt local
service support; repair is outside successful-map timing.

**Close this batch.** Stop common tie, low-order separable support and the stated
polymer steady-drag cases; keep screw/field-jaw controls. No E-150 repair or print.
Next: bounded finite strip/grounded former with signed feed and unilateral contact,
zero-friction and elastic controls, multiple input-cut phases at 0/1/10 N, coherent
guide/frame errors and unchanged neighbor. Include elastic inventory and buckling.
Stop on absent parked stability, runaway, unsupported transfer or inaccessible
routing. Only a survivor earns cyclic-material sourcing and full shared-writer
accounting. Geometry can change the decision; more section sweeps cannot. No CEO
resource boundary arose.
