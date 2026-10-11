---
status: complete
builds-on: [E-143, E-109, E-079, E-090, E-139]
---

# Local bleed escapes a blocked exhaust, not sustained opening energy

**Stop the finite run-off pickup and this continuously bleeding air release before
finite contact construction.** Run-off stays OPEN if its pickup stalls on the
opening face. Permanent chamber bleeds permit return after finite supply loss even
with a blocked common exhaust, but cannot defeat sustained opening pressure. Their
response/air-power tradeoff and unresolved terminal route prevent promotion. This
is a scoped embodiment decision, not a fluid/escapement ban. No machine selected.

Input main `5793835`; reproduce with Python 3 standard library:
`python3 tools/curated-experiment-checks/E-144/local_release.py`.
Evidence: reduced state constraints, fluid/spring equilibrium, numerical pressure
integration and deterministic uncertainty boxes; self-review. No finite assembly,
contact dynamics, calibrated process prior, hardware or failure-rate claim.

## Causal comparison and prior failures

Recombinations, not claimed novelty: E-079 trips a command pin for passive seating,
not sustained brake clearance/loss detection; E-090 rejects rigid shared-depth
insertion; E-139's dwell cannot dissipate free-input energy. E-109's small valve
spring fails its pressure/coil-bind box. Neither that spring nor hydraulic-only
service-load retention is reused here.

All options keep separate reversible drives, grounded spring jaws **beyond capture**,
6,400 parked supports/returns and actual output proof. Spatial docking selects rods;
transverse opening allows independent rod movement/reversal, but **not independent
jaw closing**. Motors or proved parked handback hold early finishers until bank
closure. Unchanged columns remain on parked supports isolated from release.

| Option | OPEN dwell / CLOSE cause | Failure |
|---|---|---|
| Rigid tie, E-143 control | Hold bar / return bar | Local or common jam propagates |
| Run-off pickup | Finite flat maintains gap / pass its edge | Stall on flat holds OPEN |
| Run-off plus latch | Latch stores OPEN / unspecified trip | Local loss/reset path still absent |
| Sole-exhaust pressure control | Supply pressure / common vent | Blocked exhaust traps pressure |
| Permanent chamber bleed | Continuously replenish air / remove supply energy | Local vents survive common exhaust obstruction; sustained supply holds OPEN |

## Run-off dwell and reset witness

Grant a 2-mm rise, 10-mm flat and ideal immediate closure beyond the edge. A
20-mm/s sweep gives **.5-s full opening**: useful for nominal .4-s/40-mm rod travel
plus .05-s local operations. Yet a pickup seized at 7 mm holds full gap indefinitely;
passing 12 mm requires the very common motion whose failure must be tolerated.
This is a reduced unilateral support constraint, not generated contact geometry.

Longer dwell increases vulnerable positions. Rod-driven run-off fails on a
stationary/reversing rod. A timer with repeated refresh changes the mechanism; an
OPEN latch requires an explicit loss-safe CLOSE cause. Reset over the same face
reopens the jaw: bypass/one-way return or proved parked support must precede rearm.
No finite section earns promotion from the granted run-off behavior.

## Concrete pneumatic circuit and force/volume model

Tankless source → common feed → parallel spring-return chambers, each with its own
permanent atmosphere outlet **downstream of any branch obstruction**. No check
valve traps pressure away from its bleed; no shared muffler is granted clog immunity.
An optional common dump is excluded from loss-return calculations. Springs/pads
ground rod loads; pressure only opens them. **One drive losing power while the
common pump stays on does not close that head**; a local valve/disconnect is extra.

Explicit scenario, not a sourced manufactured device: air at 293.15 K, atmosphere
101,325 Pa, source .5 MPa gauge. Summed effective piston area A=**2,400 mm²/head**,
stroke g=.4 mm, preload 800 N ±20%, slope k=200,000 N/m and adverse return-guide
shunt S=40 N. An equivalent coordinate represents both jaws. Its area diameter is
55.3 mm: internal machinery, not relaxed 5.08-mm tops. Source force 1,200 N exceeds
960+80+40=1,080 N adverse opening force. Work is ≥**.416 J/head** at that corner
before other losses; swept volume **.96 ml/head**. Ideal leverage preserves work.

At minimum preload N=640 N, quasi-static return is
`q=clip((A*p_g+S−N)/k,0,g)`. Motion starts at 283.33 kPa gauge; contact occurs at
250 kPa. After contact, `D=.02*(N−S−A*p_g)`: contact is not useful holding force.
**11-N capacity** occurs at **20.833 kPa gauge**, one newton above E-143's assumed
10-N load. This is a comparison threshold, not an accepted arrest/drop requirement.
Atmospheric capacity is 12 N; shunt S=160 N instead leaves 9.6 N and fails even
fully vented. Actual jaw seizure is outside this equilibrium return assumption.

`V=V_dead+A*q+C*p_g`. Closed dead volume includes chamber and allocated tubing/feed:
2 ml baseline, .25/14 ml alternatives. Wall compliance C gives expansion at .5 MPa
of 0/.2/1 times dead volume. “No accumulator” does not remove trapped gas, spring
sweep, line expansion, compressor-head volume or pump coast. Uncounted connected
source volume invalidates response figures.

## Flow, thermal and coherent manufacturing sensitivity

Use the ideal-gas choked/subcritical nozzle law from
[NASA GUNNS, Orifice Flows](https://github.com/nasa/gunns/wiki/Standard_Flow_Equation#orifice-flows),
with [NASA Glenn's sonic relation](https://www.grc.nasa.gov/www/k-12/airplane/mflchk.html)
as a separate choked check (accessed 2026-10-11). Cd=.7 baseline, .4/.9 bounds are
**assumptions**, not print priors. Short-orifice theory does not validate long rough
printed capillaries.

For absolute pressure p, polytropic n, `T=T0*(p/p0)^((n−1)/n)` and
`dt/dp=(V/n+p*dV/dp)/(R*T*mass_flow_out)`. Chamber mass balance with well-mixed
isothermal n=1 or adiabatic n=1.4 blowdown includes piston/wall volume change.
Integrate separately at jaw-stop, seated and sonic boundaries. Jaw inertia,
asymmetry, bounce, seal stick-slip and propagation delay are excluded: results are
**equilibrium-capacity times, not actual arrest predictions or bounds**.

Baseline: isothermal, 2-ml dead volume, rigid walls, no pump coast:

| Bleed diameter | First contact | 11-N capacity | Ambient air L/min/head during dwell | Ideal compression W/head |
|---|---:|---:|---:|---:|
| .10 mm | 2,295 ms | 4,291 ms | .389 | 1.17 |
| .25 mm | 367 ms | 687 ms | 2.43 | 7.31 |
| .50 mm | 91.8 ms | 171.7 ms | 9.72 | 29.23 |
| 1.00 mm | 23.0 ms | 42.9 ms | 38.88 | 116.94 |

Reversible isothermal compression `mass_flow*R*T*ln(p0/p_atm)` is a lower power
bound **for this air-supply embodiment**, excluding inefficiency, charging and rod
drives. The .5-mm case at 121 simultaneously open heads consumes **1,176 ambient
L/min and ≥3.54 kW** during dwell. No product power ceiling or universal cost
exclusion is inferred; the proposed low-energy release benefit fails. Staggering
banks reduces peak open heads while constraining concurrency/speed/head inventory.

Adiabatic baseline gives **146.3 vs 171.7 ms**. Across 18 dead-volume/thermal/wall
combinations at .5 mm: **62.5–1,709.9 ms**. Sixteen coherent isothermal corners
(d=.45/.55 mm, Cd=.4/.9, V_dead=1.5/2.5 ml, wall expansion=0/.2) give
**91.2–498.7 ms**, not statistical tails. Nozzle bias/roughness and line expansion
can shift a whole bank together. Blockage is a separate topology fault, not a
Gaussian outlier. No qualified X1C bounds exist here for layer/first-layer effects,
warp, shrinkage, seals, alignment, spring creep/fatigue or wear; no yield follows.

Pump coast is an explicit envelope: hold at most p0 for 0/10/50/200 ms, then zero
inflow. Adding these to the upper isothermal box gives **498.7/508.7/548.7/698.7 ms**.
No real pump is shown to satisfy that bound. Continued motor power, connected tank
or indefinite replenishment defeats it. A stuck live feed is not a blocked exhaust.

Resizing A, N, k, S together for μ=.1/.3 preserves thresholds and 11-N capacity.
If all dead volume scales too, .5-mm-bleed times fall to **34.3/11.4 ms**; with
fixed 2-ml lines they remain **129.7/122.7 ms**. An illustrative 10-ms threshold
requires ≥**100.4/33.45 W/head** compression even in the fully scaled cases
(501.8 W at μ=.02); fixed lines require 379.2/358.7 W. Ten milliseconds is not an
accepted requirement. Liquid circuits need their own compliance/swept-volume model;
air results do not reject every fluid release.

## Fault graph, rearm and interface inventory

The executable finds connected pressure components: after source loss each needs
an atmosphere outlet. It grants unrestricted connections and spring return; counts
are **eventual vent paths, not proved arrested rods**:

- Blocked sole exhaust: 0/8; permanent chamber bleeds with that fault: 8/8.
- Supply obstruction partitions the bank: 8/8 with intact local bleeds.
- One blocked bleed, connected branches: 8/8 through the other seven. Identical
  perfect-manifold response grows by 8/7; real restrictions need a network model.
- Blocked bleed plus isolated branch: 7/8 (**two faults**, not one blockage alone).
- Sustained source, or coherent blockage of all outlets: 0/8.

Rearm: prove support, charge, prove clearance, move, hand back, vent/prove, index.
Baseline charge from atmosphere requires **18.74 mg air/head** including piston
sweep. Even a constant source twice steady .5-mm-bleed flow takes **48.0–96.1 ms**
by ideal isothermal net-mass bounds, before line/settling losses. Exactly steady-flow
capacity cannot deliver instantaneous full-pressure reset. Common pressure/bar
position cannot prove a local jaw; jaw position alone cannot prove grip. Failed
proof retains capture and inhibits indexing, with bounded retry or isolation/repair;
false acceptance/recovery time remain unknown.

For H heads count H independent drives/return assemblies, 2H pad contacts and jaw
guides, H equivalent chambers, H moving sealed/flexing boundaries, H restrictions
and H branches. Two pistons double relevant seals. Add source/feed/dump, power,
control, proof and access. Parked supports, guides/returns and capture/handback still
repeat at 6,400 cells. Filters, quiet exhaust and readers are unpriced; printed
integration does not remove wear interfaces or assembly. No material/time estimate.

## Full-machine disposition and next discriminator

Keep 5.08-mm tops, 40-mm travel, 6,400 cells and strict <30 s. E-143's optimistic
`6+ceil(6400/H)*(.45+t_extra)` includes six seconds preparation/registration/proof/
retry/settling and .45 s/head wave travel/local operations. Extra .01/.05/.1/.2 s
requires **124/137/149/178 heads**, versus 121 with no extra time. Using .5-mm local
bleed each wave gives **169 heads** before recharge. A common normal dump can improve
normal timing, not the failed-dump response; overlap requires an actual supported
schedule. E-132's dense-route collision and E-142's capture elasticity remain open.

Joint purchases stay <$500, ideally <$200. With inherited hypothetical $250 shared
allowance and $1.56/motor comparison, 121 heads leave <$61.24 for all other purchases;
134 leave <$40.96; 169 already exceed budget by $13.64. E-143's motor rated-power
failure remains. No fresh quote, free spring/pump, complete BOM or durability pass.

**Decision:** preserve local bleed as a conditional common-exhaust-fault improvement,
but stop these embodiments. Reopen run-off with local return independent of a seized
pickup. Reopen fluid release with enforced finite supply energy, credible response/
flow budget and chamber-side vent/recovery paths. Sustained pressure cannot mean
both OPEN and loss-safe CLOSE to the unchanged passive chamber. No fabrication.

**Next:** compare shared electromagnetic opening fields and mechanically separate
spring armatures against bleed. This removes a common moving return bar/expelled-air
loss; it differs from E-143's priced per-head solenoid array. Cross-check E-138;
screen pole/gap force, stuck-armature flux redistribution, current turn-off including
suppression/remanence, dwell heating, lever work, repeated magnetic parts and joint
cost. Powered stuck commands still require a separate interruption path. Stop if
common moving poles, per-head active release or assumed free precision magnetics
are the only escape; a survivor earns a finite bank section, then terminal routing.
No purchase, print, staffing or CEO approval is needed.

Self-review: sonic expression/continuity, zero-flow limits, area/volume scaling and
chamber mass derivative. Fixed-volume choked exponential: .0509405281 s vs numeric
.0509405275 s. Baseline 64/128/256/512 subdivisions per smooth interval:
.171648963/.171649993/.171650251/.171650315 s. These verify the reduced calculation,
not real flow/contact fidelity. Graph checks and stalled-flat witness are separate.
