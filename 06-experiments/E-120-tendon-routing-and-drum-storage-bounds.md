---
status: complete
builds-on: [M-009, E-099, E-119]
---

# Dedicated tension routing is costly, not excluded by wire count alone

**Allocate one bounded investigation to local drum storage with tension transmission;
keep perimeter routing and direct rack heads as controls.** This changes service
load from a shared elevator/command disconnect to an independently retained rotary
coordinate and tensile transmission. It avoids E-119's common mixed-reset operation
only if every drum can be privately acquired, supported, unlocked, moved, relocked
and released. No such complete mechanism is established here. Do not reopen the
failed synchronous dog or select a cable machine on these bounds.

Input main `c5f9244`. Reproduce:
`python3 tools/curated-experiment-checks/E-120/tendon_bounds.py`.
Deterministic generated rectangular routing corridors and necessary rotary-service
budgets, standard library; self-review. No sourced cable properties, prices,
process priors, finite pulley/lock geometry, CAD or physical measurements.
All dimensions beyond stage-02 pitch/travel are explicit design assumptions.

## Changed hypotheses and complete-machine obligations

| Hypothesis | State, energy, support and selection | Main tradeoff |
|---|---|---|
| Perimeter drums | 6,400 retained drum angles; reusable powered torque heads at perimeter; each tendon supports one guided column through fixed redirection | Accessible storage but long tendons, endpoint fanout, stretch/friction and service volume |
| Distributed layered drums | Same memory/load principle; drums under local tiles, independently accessed by reusable heads | Shorter possible routes, but layer passage, head access and module repair can defeat packing |
| Direct rack heads | E-099 reference: head takes old column, repositions it and transfers to grounded support | Avoids tendons/drums; finite acquisition and complete affordable channel still unqualified |

One tendon only pulls. Gravity lowering needs a force margin against guide and
routing drag at minimum moving mass; that margin is unknown. An antagonistic pair
or closed pull-pull loop changes force closure and approximately doubles routed
members/terminations, adds preload and consumes routing space. A drum angle alone
is not verified column height under slack, slip or stretch. Each hypothesis needs
actual output readback, load proof before head release, a bounded retry while
supported, and a stopped-module recovery path after a jam or broken tendon.
Unchanged sites must retain their own locks throughout local updates. No assumed
spring, friction brake, gravity reset or perfect reader supplies those functions.

## Generated two-edge routing control

For 80 rows at 5.08-mm pitch, send each row's left/right 40 sites to its nearest
x edge. For index j=0…39 measured inward from that edge, descend from z=0 to
`z=−(j+.5)(d+c)`, then turn horizontally to the edge. Here d is the **entire
reserved routing-corridor diameter**, not a selected cable diameter; c is free
separation. Deeper inner routes pass below the shorter outer vertical routes.
The executable generates finite rectangular occupied envelopes for both legs,
checks every intersite leg pair within the row and uses row separation to cover
the board. All nine d={.6,1,1.4}, c={.1,.2,.4}-mm cases are nonoverlapping in this
ideal model. This is a static routing counterexample to treating 6,400 individual
members as a topological impossibility, not a manufacturable cable path. Rounded
bends, tube walls, supports, moving tails and outboard fanout remain absent.

Horizontal centerline total is 650.24 m. Including the generated vertical legs,
right-angle centerline lengths are **739.84–880.64 m** with deepest corridor bottom
27.95–71.8 mm below the routing datum. These are lengths of this itinerary, not
universal shortest-path bounds (finite rounded bends alter length). Other exit
choices, local drums and a changed routing topology can change them. They exclude
column tails, winding, anchors and perimeter-to-drum fanout.

For d=1,c=.4: **829.44 m**, depth **55.8 mm**. A $250 allowance after all other
purchases would leave **<$0.30141/m for that route alone**. This is an optimistic
budget ceiling, not a cable quote; adding heads/locks/terminations only reduces it.
The route has 6,400 members and 12,800 ends before any return members. With only
$250 available to *all* cell purchases, mean allowance is <$0.0390625/site.
These burdens deprioritize the perimeter control; they do not prove a cost failure.

For relative lane-position errors ±e and corridor-diameter error ±e, adjacent
horizontal separation is at least `c−3e`. Absolute common z translation cancels;
neighbor differential errors can repeat coherently over an entire board. The
c=.4 case retains .25/.10/−.20 mm at e=.05/.10/.20. Negative margin means the box
admits contact, not a yield estimate. Inter-row and vertical-x separations are
larger under the same box. This bounds only corridor placement, not bending,
sag, guide friction, creep or manufacturing accuracy. No distribution is invented.

## Drum-size / rate boundary

A constant-radius winding making n turns per 40-mm stroke has effective tendon
centerline radius `r=40/(2πn)`; cable thickness is not a qualified core allowance.
Assume an additional 1.5-mm radial rim/structure envelope. With drum centers on
the top grid, a regular k×k residue coloring, `k=ceil((2r+3)/5.08)`, separates
disk envelopes within each of k² planes. This is a **particular disk-only layout**,
not an optimal layer lower bound or complete packing proof; axles, locks, groove
width, finite tendon thickness, moving heads and cross-layer cable passage are
unmodeled. Multi-turn axial winding or multilayer radius growth cannot be free.

| Turns / 40 mm | Effective radius mm | Outer envelope mm | Disk-only planes | Required rpm, 80 heads | Required rpm, 320 heads |
|---:|---:|---:|---:|---:|---:|
| 1 | 6.366 | 15.732 | 16 | >266.67 | >50 |
| 2 | 3.183 | 9.366 | 4 | >533.33 | >100 |
| 4 | 1.592 | 6.183 | 4 | >1066.67 | >200 |
| 8 | .796 | 4.592 | 1 | >2133.33 | >400 |

Rates assume 6,400 full-stroke independent visits, balanced over heads, .1 s per
visit for all nonrotation functions, 4 s map overhead, no travel/acceleration or
retry time, and strict <30 s. Formula:
`rpm > 60n / [(30−4)H/6400 − t_nonrotation]`.
Source also compares 160 heads and .05-s service overhead. These are necessary
constant-rate offers for this visit architecture, not measured motor capability,
a complete schedule or universal lower bounds for a shared broadcast mechanism.
The two-turn option reduces the tested disk planes relative to one turn without
entering the eight-turn speed/small-radius extreme. Keep it as a finite-geometry
seed, not an optimum. Torque is r N·mm per N tendon force; torque×angle remains
40 N·mm per N, checked explicitly. Smaller drums do not save ideal lifting work.

At 320 heads, a $250 remainder with zero bought cell items gives <$0.78125/head,
the same severe complete-head allowance as E-099. The hoped-for benefit is a
simpler accessible rotary coupling/support, **not** a demonstrated price saving.
Direct heads' 18.854-s E-099 central case uses different unqualified operation
assumptions; no time dominance follows from this rotation-only bound.

## Decision and next discriminator

No whole-machine Pareto winner. Perimeter routing is an expensive control;
distributed drums merit a bounded finite return/locking/routing investigation.
Stop if a complete local path cannot both lower under explicit drag uncertainty
and preserve unchanged support without recreating the shared mixed-reset problem.
Require a private torque takeover and positive lock before scheduling or price
research. Compare gravity-return and antagonistic routing, including all grooves,
anchors and approach/withdrawal through unequal neighboring heights. Larger
internal pitch is permitted; added volume and repeated interfaces must be counted.

Self-review: 80 generated routes × four leg pairs for every site pair in each of
nine scenarios; common-translation invariance; independent closed-form length
sums and a .4-mm separation witness; all 6,400 disk centers assigned once; travel
and work identities; explicit fit/error and head/overhead sensitivities. These
checks validate only this reduced model. No print, purchase or hardware claim.
