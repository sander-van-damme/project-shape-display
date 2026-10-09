---
status: complete
builds-on: [E-081, E-091, E-052]
---

# Finite support transfer requires reader decoupling

**Retain a conditional nine-level pocket-dog support section; reject direct
attachment of the equality reader to the unloading elevator.** The generated
3-mm pockets admit a common 2.2-mm unloading excursion under the declared
bounds. That excursion makes E-091's otherwise surviving nine-level decoder
miss a true command and accept a neighboring command if its coordinate simply
follows the elevator. Even after offset compensation, leaving the probe inserted
while reseating produces interference. Support transfer therefore requires a
compensated query plus retained selection or a separate stationary reader dwell.
An energy cam driven directly from instantaneous equality is not a complete path.

Input main `24f9ee4`. Reproduce with
`python3 tools/curated-experiment-checks/E-092/support_transfer.py`.
Evidence: deterministic finite rectangle sweeps, quasistatic spring/contact
calculation, interval synthesis and E-090 polygon counterexamples. No measured
process priors, yield, dynamic simulation, manufactured parts or physical
qualification. Self-review only. This is parameter synthesis within a positive
pocket-dog topology, not another architecture family.

## Generated load path and uncertainty

At each cell, two separate rack lanes carry nine blind rectangular pockets at
5-mm pitch over 40 mm: one for a grounded dog, the other for an elevator dog.
Each rack section spans x=0…1.2 mm with pockets open to x<0, 0.8-mm deep, leaving
a 0.4-mm spine. A dog moves from x=[−1.2,−0.2] to [−0.5,0.5], a 0.7-mm lateral
stroke with 0.5-mm nominal bearing overlap. Each rack includes solid lands
between all pockets and 1-mm end lands. These are **separate section lanes**;
their 3D connection, lateral error, strength, guides, retention and packing at
5.08-mm surface pitch are not established. E-052's different pawl and guide
claims are not inherited.

Ground → grounded dog → pocket ceiling → column is the stationary load path.
Elevator → its dog → the acquisition pocket ceiling → column is the moving
path. The elevator dog stays at the same tooth throughout a displacement; the
ground dog enters the target tooth. Mixed old heights therefore keep their
individual offsets, as required by E-081. Unchanged columns keep their ground
dogs inserted and elevator dogs withdrawn; no deliberate regional reset is
required by this section, but frame-induced disturbance is unmodelled.

Labelled competing bounds, not calibrated X1C distributions:

- Nominal pocket height h is synthesized over 1.4/1.8/2.4/3.0 mm; each actual
  pocket height is h±0.1. Dog thickness is 0.8±0.1 mm. Ground and grip dimensions
  can differ. Their free vertical clearances are cG and cE.
- The elevator dog is centered in the acquisition pocket with ±0.2-mm vertical
  datum error a. Its initial top gap is **g=cE/2+a**. This dependence is retained;
  clearance and gap are not independently sampled.
- Ground target-to-acquisition tooth error Δ is ±0.2 mm. It is zero when the
  same tooth is used. It is an aggregate relative bound, not an independent
  ±0.2 error added at every tooth. Absolute terrain accuracy remains unqualified.
- Full-load downward elastic deflection of the elevator support is d=0…0.2 mm.
  Ground is rigid in this model. This is a competing compliance bound, not a
  fitted material property. The adverse values may occur together in one bank.
- A 0.05-mm noncontact reserve is imposed. Roughness, warp, angular error,
  first-layer effects, creep, wear and dynamic motion need to fit revised bounds
  or be separately modelled; there is no claim that this reserve covers them.

Enumerating corners covers local variation and coherent bank extremes without
inventing probabilities. Common equal deflection shifts the required lift;
differential deflection consumes its feasible window. Common motion alone cannot
remove differential errors.

## Continuous transfer and independent interval check

Use e relative to the nominal target displacement, with high coordinate u and
low coordinate v. The ground seat is at relative rack height Δ. Under downward
load F and support stiffness k (d=F/k), elevator force is
`FE=clamp(k(e−g−Δ),0,F)` and ground force is `FG=F−FE`.
The rack height relative to its nominal target is
`max(Δ,e−g−d)`. The elevator dog top is `e−g−FE/k`.
The d=0 rigid limiting case transfers load at contact. No lateral friction or
impact is credited.

The ground dog must insert while fully unloaded, without hitting either pocket
wall. The elevator dog must then unload and withdraw without hitting its lower
wall. With reserve c=0.05, the common-coordinate conditions are:

```
max(g+Δ+d+c) ≤ u ≤ min(g+Δ+d+cG−c)
max(g+Δ−cE+c) ≤ v ≤ min(g+Δ−c)
```

They include the relevant correlated cE/g endpoints. Independent closed forms
for this error box are `u∈[h/2+0.35, 1.5h−1.95]` and
`v∈[−h/2+0.95, h/2−0.95]`, in mm.

| h mm | Feasible u interval mm | Feasible v interval mm | Result |
|---|---|---|---|
| 1.4 | [1.05, 0.15] | [0.25, −0.25] | empty; reject |
| 1.8 | [1.25, 0.75] | [0.05, −0.05] | empty; reject |
| 2.4 | [1.55, 1.65] | [−0.25, 0.25] | interval-only survivor |
| 3.0 | [1.85, 2.55] | [−0.55, 0.55] | retain u=2.2, v=0 |

The continuous threshold is h≥2.3 mm for this box; tuning the searched grid is
not the basis of rejection. Larger pockets reduce the intervening land and need
strength/packing evaluation. At h=3, raising d's bound from 0.2 to 0.5 and Δ's
bound from 0.2 to 0.4 collapses the 0.7-mm u-window to zero. This sensitivity is
not evidence supporting either input bound.

The executable geometry tests the **whole horizontal dog sweep** against all
nine finite pockets, not just endpoint engagement. During reseating, contact
breakpoints and intermediate positions check nonpenetration, force balance and
contact at every loaded interface. Monotone piecewise-affine motion means those
breakpoints bound each segment; 1/16/64 subdivision holdouts agree. Acquisition
is the same supported transfer reversed at the old tooth. This tests the local
transfer for every old/target pair; it does not validate an assembled bank.

A grip-depth reading at e=0 can report full lateral engagement while the entire
load still rests on ground. Releasing ground at that moment permits **0.8–1.6 mm
of drop** before full-load equilibrium in the chosen section. Failed grip/load
proof must keep ground engaged; failed ground proof must keep the grip engaged
and inhibit departure. A jam during horizontal withdrawal requires a stopped,
supported recovery; the sweep calculation supplies no extraction-force limit.
A falsely accepted proof remains unsafe. There is no physical reader here.

## Decoder contradiction and complete-machine consequences

For H=9, E-091 uses a 5.4±0.1-mm slot, 0.4±0.1-mm probe, ±0.65-mm datum error
and ±1% gain. Querying at elevator coordinate `delta+2.2` without compensating
that 2.2-mm lift gives explicit finite-polygon witnesses:

- Intended +40-mm command: relative error 3.272 mm at adverse positive datum
  and gain; the 0.5-mm pin does not enter the 5.3-mm slot.
- At the +35-mm group, a +40-mm command has relative error −1.778 mm with
  the same error direction; the 0.3-mm pin fully enters the 5.5-mm slot.
- With compensated coordinate, a valid query at −1.05-mm relative error fully
  inserts. Lowering the attached reader by 2.2 mm changes that error to
  −3.228 mm (−1% gain), colliding with the slot wall while inserted.

Both commands have the same sign, so E-091's sign gate does not prevent these
faults. Withdraw the probe before reseating, and retain the selected output
through ground insertion/proof, elevator unloading and grip release/proof; or
provide a finite reader dwell independent of elevator movement. Neither missing
linkage is silently granted. A common cam may supply energy only after these
selection and support conditions are physically implemented.

For the adverse nine-level workload with eight deposit groups per sign,
explicit paths including acquisition take-up, each reseat and empty return
increase common travel from E-081's **160 to 199.6 mm**: 84.4 negative-phase plus
115.2 positive-phase. Eighteen extra motion legs enter the rest-to-rest schedule.
Some carried columns rise above their initial or target height; the chosen
section needs up to 1.6-mm headroom above the actual seated target under this
box. Therefore E-081's old/target-interval invariant cannot be inherited. This
is not a regional disturbance qualification or a timing pass.

With hypothetical total moving load 0.1/0.5/1 N per cell, 800 simultaneously
carried cells exert 80/400/800 N before inertia, guides or probe reactions.
The initial take-up drive-work upper allocation for 6,400 changed cells is
1.408/7.04/14.08 J (`NFu`); this is not whole-cycle work or motor sizing. No
load requirement or measured PLA stiffness is inferred. Loaded lateral release
would additionally need friction-dependent force, which the unload sequence is
intended to avoid; misalignment and residual contact can defeat that intention.

Two dogs add **12,800 sliding members**, bringing this embodiment to at least
**44,800 local sliding members** with E-091's memory/readers, before the output
retention, energy coupling, guides and readback. At $250 elsewhere, even one
bought part per cell has <$0.0391 allowance under the strict $500 ceiling.
No cost, printing, assembly, service-life or hardware pass follows.

## Decision and remaining discriminator

Stop the small-pocket cases and uncompensated/directly carried query linkage
under these bounds. Retain the h=3 section only as the support comparator for
one finite coupling investigation: compensated query → retained output →
separate energy cam → supported reseat → positive withdrawal/reset. The
alternative is a finite reader dwell; compare its repeated and bank burden.
Do not tune the rejected 41-command lock. Keep the selective-deck and direct
writer controls available for the campaign's complete-machine comparison.
Reopen these scoped failures only with changed error/compliance evidence,
changed pocket/support topology, or an explicitly decoupled query mechanism.

Checks: 9,216 deposit cases, 1,152 acquisition cases, 94,464 deposition contact
states, 114 refined holdouts, three support fault witnesses and three decoder
counterexamples. No unqualified spring, reader, keeper or cam is counted as a
passed machine component. No printing is justified by this subsection alone.
