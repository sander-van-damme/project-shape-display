---
status: complete
builds-on: [E-060, E-108, E-109, E-147, E-156]
---

# Overlapping closures isolate the source, not the moving pressure boundary

**Stop the unrestrained roller/front embodiments.** Overlap can prevent a direct
chamber–reservoir path, but pressure still backdrives the moving closure coordinate.
A single front also loses isolation on reset. Tube elasticity supplies conditional
wells, not arbitrary-angle retention or demonstrated settling. This rejects an
assumed self-holding pump, **not all peristaltic machines**. No selection, fabrication,
purchase or seal-coefficient fitting.

Input main `e3f052f`. Replay:
`python3 tools/curated-experiment-checks/E-157/occlusion.py`.
Evidence: exact connection intervals, generated radial-gap section, conservation,
analytical dynamics and deterministic bounds. Self-review; no complete CAD/contact
solution, calibrated tubing/FDM prior or measurement. JSON is disposable. Downward
loads 0/.02/1/10 N are scenarios; 10 N everywhere is not a product requirement.

## Causal comparison and sources

| Embodiment | Selection, motion, intended retention | Missing support/return |
|---|---|---|
| Resident train | Independent reusable rotary heads dock to 6,400 local three-roller rotors. Reservoir–tube–piston circuits have overlapping closures; rotor angle meters volume; reversal withdraws volume. | Piston → liquid → tube/race/rollers → bearings **and shaft torque restraint** → frame. Radial support alone omits torque reaction. Tube recovery refills behind rollers; piston return, starvation and cavitation remain. |
| Travelling front | Dry head rolls a pinch toward the chamber. A second closes before the first lifts/recycles. | Liquid → last pinch → **longitudinal carriage restraint** → frame. Normal clamp/anvil support does not prevent sealed rollback. Leaving a front behind repeats resident clamps/locks. |
| E-109 control | Shared pressure; independently opened fine/bypass poppets; spring return to grounded seats. | Stationary closed seat avoids the moving boundary. Tested spring loses closure under source pressure; priced heads fail joint cost. No reopening. |

All retain 6,400 guided ≥40-mm outputs, seals, reservoir/return, fill/bleed and sensing.
Trial 2-mm pistons are not packed sealed cartridges; square tops stay at 5.08-mm pitch.
Independent termination, docking and top/hold proof precede supported withdrawal.
Failed proof retains a supported head and aborts; this cannot recover missing support.

Search moves: medical peristalsis combines pumping/shutoff; travelling material
boundary replaces stem actuation; reversed packet delivery exposes reset mixing.
Known principles recombined, not patent novelty; no prior repo peristaltic construction. E-060's intermediate-volume exchange, E-108's compliance/
closure displacement and E-147's repeated reset failures still apply without glands.

Primary sources, accessed 2026-10-11:

- [Watson-Marlow 601 P/R manual, pp.4–6](https://www.wmfts.com/globalassets/literature/m-601pr-gb-01.pdf):
  spring-loaded rollers compensate wall variation; excess occlusion shortens tube life,
  insufficient occlusion reduces efficiency. Industrial 3.2-mm walls are no prior for
  the .5-mm-wall scenario below; quoted flow depends on operating conditions.
- [Saint-Gobain tubing guidance](https://www.medical.saint-gobain.com/resources/blog/choosing-your-peristaltic-pump-tubing):
  compression cycles, recovery, permanent set and dimensions affect performance.
  No miniature closure-force, static-leak or lifetime qualification is supplied.
- [EP0745400A2, Figs.11–13 description](https://patents.google.com/patent/EP0745400A2/en):
  occlusion adjustment has an explicit brake or alternative spring return. That
  brake restrains the **adjuster**, not necessarily the pump rotor. No free rotor
  restraint or prototype performance follows from the patent.

## Connectivity and finite radial section

Graph: R — upstream pinch — packet P — downstream pinch — chamber C. Closed
pinches delete edges. Executable advance/reversal/stop/source-loss states with at
least one closed pinch lack R–C connection. Single-front reset
`(open,closed) → (open,open) → (closed,open)` exposes R–C; stopping in the
middle leaves it open indefinitely. Overlap reset
`(open,closed) → (closed,closed) → (closed,open)` avoids that connection,
but joins **P to C**. Source disconnection changes neither graph nor pressure force.
Reversal retraces closures; lifting both to reverse repeats the open-path failure.

Exact circular interval unions: 2/3 equally spaced rollers, full-occlusion arcs
110/130/200°, adverse entry/exit erosion 0/5/10° each (18 cases). Three rollers
with 200° remain isolated; three with 110° expose **30°/revolution**. Three with
130° pass nominally but expose **30°** after 10° erosion at each edge. Two with
200° lose strict overlap margin at that corner. Equality is not a sealing pass.
Removing one of three rollers from the 200° case exposes **40°**.

Generated radial section: 10-mm roller-center orbit, 2-mm roller radius, 12.9-mm
race radius over 200°; entry/exit relief grows .02 mm/degree. Tube ID/wall 1/.5 mm;
ideal closure requires gap strictly smaller than twice wall thickness. Nominal
closure spans 210° including relief. Phase sweeps at 720/1,440/2,880 midpoints
retain ≥1 nominal closed section; a missing roller opens the circuit. Nine common
wall/gap corners ±.05 mm include **no closure** for thin wall/large gap and no
qualified closure at thin wall/nominal gap (equality). A 1e−12-m comparison guard
prevents floating-point equality becoming closure. Exact extrema agree.
This checks the defined geometry, not tube flattening, stress, stretch, roller-axis
fit or a complete assembly. Nominal gap closure is not a seal qualification.

## Pressure work, source loss and elastic wells

Piston `Ap=π(2 mm)²/4`, tube `At=π(1 mm)²/4`. An incompressible closed front at q
obeys `Ap dh=At dq`; reaction `Fq=p At=F At/Ap`. Ten millimetres of backward
front travel lowers the column **2.5 mm** without opening R–C. Full stroke needs
**160 mm** front travel or 16 transfers of a 10-mm front stroke. Reaction at
.02/1/10 N output is **.005/.25/2.5 N**. Moving two pinches together retains this
free coordinate; normal clamp reaction does not supply longitudinal restraint.

Ideal homogenized rotary displacement: `V=Kq θ`, `Kq=At R`, R=10 mm.
Thus `dh/dθ=2.5 mm/rad`, torque `p Kq=.0025 F N m`; a revolution transfers
49.348 mm³/15.708-mm output travel. Independent virtual work gives `p dV=F dh`.
This smooth volume law omits roller entry/exit ripple: short-phase trajectories
are conditional on this law, **not bounds for the finite-gap rotor** above.

True drive disconnection, effective inertia J, no qualified loss/barrier:
`J θddot=−p Kq`. J=1e−6 kg m² includes reflected output/fluid inertia as a
scenario; it is not a rotor mass estimate. Applied force and inertia are independent,
not an inferred gravity-only payload. Exact 50-ms witnesses:

| Downward force | Initial rotor speed | Column change |
|---|---:|---:|
| 0 | 0 | 0 |
| 0 | ±20 rad/s | ±2.500 mm |
| .02 N | 0 | −.15625 mm |
| 1 N | 0 | −7.8125 mm |
| 10 N | 0 | −78.125 mm ideal extrapolation |

The last exceeds travel: no internal arrest in this model, not physical motion
beyond an endpoint. Overlap persists during reverse pumping. A powered stop needs torque; retaining the cut drive adds inertia/elasticity. Viscous loss can limit speed
under pressure while leaving nonzero flow; it does not supply static retention.

Competing tube-energy scenarios `U=U0[1−cos(3θ)]`, U0=0/.1/1/10 mJ, give
`J θddot=−p Kq−3U0 sin(3θ)` before unspecified loss. Strict wells exist only
if `p Kq<3U0`. At U0=1 mJ, .02-N backward barrier is **1.94792 mJ**, equilibrium
shift **−.01389 mm**; at 1 N these become **.129399 mJ / −.82093 mm**. At that
1-N minimum, J=1e−6 and 20 rad/s supply .2 mJ: sufficient to cross backward.
Successive downhill barriers decrease in absolute potential. At 10 N there is no
well; U0=10 mJ restores a **1.29399-mJ** backward barrier.
At zero load nonzero U0 still drives a rotor away from nonminimum positions.
Minima are **5.23599 mm apart** under the nominal volume law; conservative motion
oscillates or traverses wells, with no settled arbitrary-height hold.

These 16 cases are model uncertainty, not tube properties. Total compression energy
is not periodic barrier energy: entry/exit contributions may cancel. Sufficient
barriers/damping could change disposition; the present design has no established
lower barrier, arbitrary-state restraint or release path. Zero-loss limits do not
prove every commercial pump backdrives.

## Reset volume and closure force

For packet V, effective linear bulk modulus B, `Cp=V/B`. Opening into a moving
constant-load chamber at pf from packet pressure pi gives
`Δh=[Cp(pi−pf)−Vreopen]/Ap`. Vreopen is net connected space created by pinch
withdrawal, not the entire packet. With Vreopen=0, elastic-energy change + load
work + `.5 Cp(pi−pf)²` equilibration heat = 0. A fixed piston instead changes
pressure; this is quasistatic, not a transient bound.

A 10-mm packet holds **7.854 mm³**. B=10/100/1,000 MPa, pi=0/.5 MPa,
F=.02/1/10 N (18 cases) give **−.795775…+.123408 mm** per merge. Largest
p/B=.318 is beyond small-strain liquid behavior: only an effective-compliance stress
scenario. B=100 MPa, pi=0, F=10 N gives **−.079577 mm**; 16 refreshed packets
permit **−1.27324 mm** until stroke runs out. Reopening the same equilibrated
packet does not repeat the debit; restoring pi does (E-060/E-147).
An assumed .2-mm³ reopening consumes **.063662 mm**, even at zero pressure
mismatch. Precompressing a packet requires `Δq=Cp pf/At`, work `.5 Cp pf²`;
it can avoid the pressure mismatch, but needs independently restrained front motion.
Closure-volume compensation and post-closure proof remain. Reversal swaps histories.

Constructed normal section: rigid guided roller/anvil, wall .5 mm, gap .9 mm,
pressure width `b=π d/2`, axial contact 2 mm. Scenario tube force
`k(OD−gap)` at k=1/10/100 N/mm plus `p b ell` gives **1.1–120 N** over
zero–10-N loads, storing **.605–60.5 mJ/contact**. This projected-area/linear-force
construction is neither a rigorous lower bound nor a circular-tube constitutive law.
Actual self-contact, pressure penetration, hysteresis and buckling are unresolved.
Fixed axles/race react normal force; tube recovery opens the lumen. Adjustable
rollers instead need counted springs/preload/stops. Neither supplies shaft restraint.
Nine wall/gap corners ±.05 mm span closure margin **−.05…+.25 mm** around nominal
.10 mm. Negative margin cannot seal; equality has no pressure qualification.

Common wall lot bias, ovality, runout, race warp, layer steps and mounting error
can affect a bank together. Tube set/wear/fatigue, PLA frame creep/anisotropy,
interlayer weakness, hole/first-layer bias and fluid compatibility remain uncalibrated.
No probability, yield or lifetime follows. For stationary sealed volume, C=0/1e−15/
1e−14 m³/Pa gives static 10-N sag **0/1.013/10.132 mm** before leakage. A diagnostic,
unapproved .1-mm/four-hour allowance requires **≤.021817 nL/s** per piston.
Single-acting return at zero downward load has at most **.31832 N** ambient suction
at 101325 Pa, before vapor/gas/line losses: .35-N drag cannot be overcome. Bias or
a second chamber changes inventory. Tube refill is not proof of piston return.

## Board obligations and decision

Optimistic obligations for a **repaired** topology, not a survivor score:

- Swept volume **.80425 L**; full upward writing requires **>1.60850 L/min** at
  30 s before overhead. Uniform 1/10-N work: 256/2,560 J; 10-N chamber pressure
  **3.183 MPa**, with no small-tube rating established.
- **19,200 rollers/axles**, 6,400 rotors/races, chamber seals/guides and independent
  hold interfaces. Trial 60-mm local tubing gives **384 m** before leads/plumbing.
  ~26-mm race envelopes require unbuilt tiers/remote routing at 5.08-mm top pitch.
  Fronts replace rotors with 160-mm working lengths or reset/handoff hardware.
  Printed volume/time is unknown. Full stroke is **2.5465 turns / 7.6394 tube
  compression cycles**; 10,000 full strokes imply ~76,394 cycles, not a life rating.
- New ideal schedule `T=6+ceil(6400/H)*(2*2.5465*60/rpm+t_extra)` charges two
  signed passes/group, independent termination, six seconds for preparation,
  registration/indexing, final proof/settling and one retry. These are unearned
  allocations; t_extra covers local dock/reset/proof. At .05 s extra, 60/300/600
  rpm require **1,600/291/153 heads** for strict <30 s. This is not E-108’s pressure-flow schedule or actual timing.
- Joint purchases `shared+H*head+6400*cell < $500`. At assumed $250 shared and
  free cells: **<$.156/$.859/$1.634 per complete head** respectively. Free heads
  instead leave **<$.03906/cell**, or tube alone **<$.651/m**. These exclusive
  maxima cannot be added. No BOM or market-floor rejection is claimed.

Unchanged regions require independently retained rotors/fronts. A free common shaft
couples volumes; slipping selection repeats E-156's arrest problem. Closed local
boundaries can isolate a shared reservoir, but graph isolation establishes neither
frame stiffness nor pressure-transient independence. Reader bias may accept drift;
no false-accept probability or guaranteed recovery is assumed. Persistent leak,
missing roller or jam requires supported module service outside successful-map timing.

Stop seal, roller-packing and return tuning. Reopen only with a grounded boundary
restraint through every stop/reversal/reset, controlled packet pressure/closure
volume, zero-load return and credible joint cost/time. A stipulated locked shaft,
ideal check or large elastic barrier is not a constructed repair.

**Next axis:** stationary field-induced yield plugs: permanent-magnet-biased MR valve
versus confined granular plug and E-109. It removes the travelling boundary but adds
field selection, carrier seepage, remanence and particle reset. A
[Brno primary paper](https://doi.org/10.1051/matecconf/202032201049) describes an
MR valve/damper with permanent magnet; its abstract is a lead, not static-seal proof.
Repository MR/electrorheological searches had no match; E-063's jamming is laminar
friction. First test yield pressure versus off-state conductance, source-loss volume
and regional field exposure. Reject viscosity-as-lock or free resident magnetic
hardware. This is an independent search axis, not a fluid winner or saturation claim.

Self-review: exact interval union/analytical gap length, radial-section refinement,
reset graph, signed energy residuals <2e−16 J, equal-pressure/zero-volume/reversal
limits, exact potential extrema, strict integer scheduling and SI conversions.
No dynamics timestep applies to these exact solutions. Ripple, fluid transients,
material/contact discrepancy and hardware reliability remain outside scope.
