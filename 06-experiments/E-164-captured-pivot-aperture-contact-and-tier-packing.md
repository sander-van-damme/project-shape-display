---
status: complete
builds-on: [E-163, E-148, A-019]
---

# Capturing the aperture pivot changes the holding geometry

**Pause the fixed-pivot canted-plate embodiment.** A captured pivot supplies the
missing lateral reaction, but its aperture translates as it rotates: the centered
E-163 force relaxation is not this mechanism. Under the declared bounds, mu=.2
requires a 32.42-mm lever for the tested small tail. A finite bypass avoids neighboring
tails, at the expense of eight tiers and about 128.30 mm for two opposite stacks.
This is a constructed packing option, not a minimum depth or a complete lock.
No inventory advantage over a returned jaw or A-019 laminate has been established.

Input main `707f9eb`. Reproduce:
`python3 tools/curated-experiment-checks/E-164/probe.py`.
Evidence: analytic finite solids, quasistatic equilibrium, explicit coherent bounds
and self-review. No measurement, calibrated prior, compliant contact, dynamic return,
manufacturing yield, complete CAD or independent review. JSON output is disposable.
No new literature/novelty claim; this is the missing support-geometry discriminator
from E-163, not another independent architectural discovery.

## Fixed pivot, actual first contact

A rectangular slot has halfwidth a and thickness t. Tail halfwidth r and horizontal
center e are fixed by a **frictionless lateral guide**; no guide-friction holding is
credited. The captured revolute pivot is (b,0). In the x-z section every material
point (u,v) becomes:

```
x = b + (u-b) cos(q) - v sin(q)
z =     (u-b) sin(q) + v cos(q)
D = b-e+r
qseat = acos(D / hypot(b+a,t/2)) - atan2(t/2,b+a)
s = sqrt((b+a)^2 + (t/2)^2 - D^2)
```

The left inner lower corner reaches `(e-r,-s)` first; the right side remains clear.
For downward tail load F, forces **on the plate** are contact `(-N,-F)` and grounded
pivot `(+N,+F)`. Moment equilibrium about the actual pivot gives `D F = s N`, so
`mu >= s/D`. This is a single-edge jam against a guide, not the centered two-edge
collar of E-163. At F=0 the unpreloaded branch has N=0; upward F would require
negative N. A return and opposed lock or other arrest remain necessary.

With delta=a-r+e, required D is
`[delta + sqrt(delta² + mu²*(delta²+(t/2)²))]/mu²`.
For large b, threshold decreases approximately as `sqrt(2*delta/b)`, whereas the
centered model had a fixed contact span divided by b. Granting recentering hides
this change. A freely sliding horizontal pivot can recenter but cannot simultaneously
supply an arbitrary horizontal reaction without another restraint; a different
support/track is a new geometry, not a repair supplied by this calculation.

## Bounded variation, not yield

Nominal r=.75, a=1.10, t=.4 mm. Same dimensional scenarios as E-163, with explicit
pivot/guide alignment sensitivity. Tight release: a−.1, r+.1, |e|=.1 leaves only
.05-mm side gap at q=0. Weak hold: a+.1, r−.1, t+.1. The alignment case additionally
uses actual pivot b−.1 and e=+.1. Errors are coherent across a batch/row, not random
independent cells; no distribution or reliability estimate is warranted.

| Nominal b (mm) | Nominal mu minimum | Size-only weak hold | With pivot/guide alignment |
|---:|---:|---:|---:|
| 2.4 | .4885 | .6324 | .7182 |
| 8 | .2866 | .3634 | .4008 |
| 16 | .2058 | .2596 | .2843 |
| 33.02 | .1445 | .1816 | .1982 |

In contrast, E-163's centered lateral relaxation for this weak-size section at
b=2.4 gives .3407. That was an optimistic allowance, not an error or a constructed
pivot. Alignment-case b required at mu=.1/.2/.4/.6 is
129.92/32.42/8.03/3.50 mm. Friction values are scenarios, not PLA data. There is
no useful low-friction margin at b=33.02, mu=.2: the inequality barely passes.

At that point contact drops 6.633 mm below the pivot and N=50.46 N at F=10 N;
N=5.046 N at F=1 N. These loads are sensitivities, not product requirements.
An assumed .1–1 mm² contact patch would see 505–50.5 MPa at 10 N; no patch or
material allowable has been established. The grounded pivot and rod guide carry
this lateral load. Creep, rounding, bending, warp and guide friction can alter the
geometry and are not represented by the rigid calculation.

## Finite neighbor bypass and grounded capture

Construct the alignment-case plate with pivot x=32.92, a=1.20 and t=.50 mm.
A collar has outer halfwidth a+.4; two .6-mm-wide bypass rails occupy
`y=±[1.2,1.8]` and extend to x=b+.8. A boss of outer radius .8 has a .3-radius
circular bore through y; the moving solid is the union of collar, rails and boss
minus the bore. A grounded .3-radius transverse axle runs to side rails at
`|y|=1.9…2.4`; these fit within 5.08-mm row pitch. The ideal conformal frictionless
bearing grants continuous capture through open→seat→open. It does **not** qualify
an actual printed fit. The .1-mm moving-to-ground side gap and .28-mm gap between
adjacent row supports have no demonstrated manufacturing margin.

Executable polygon extrema and circular-bore checks give these conditional results:

- A straight arm across the tail corridor intersects six neighboring tail prisms
  even at the fully open state. Moving it to another tier cannot avoid those
  continuous vertical tails.
- Bypass rails run outside the tail y section; collar and boss swept envelopes
  avoid other tail prisms. The tested tails extend throughout lock depth, favorably
  granting enough length for 40-mm travel. Tail length/buckling remains owed.
- Moving-part envelope is x=−1.6009…33.8556 and z=−6.7078….9356 mm. Exact extrema
  over the continuous angular interval bound every independently selected state.
- Assign column i to tier `i mod 8`, with .4-mm extra separation. Same-tier parts
  are 40.64 mm apart in x; different tiers use 8.0434-mm z spacing. Their envelopes
  do not overlap. One direction occupies 63.9476 mm; separately mirrored stacks
  occupy 128.2952 mm with a .4-mm inter-stack gap. This conservative construction
  is not an optimized lower bound and does not establish compactness acceptance.

The construction also spends about 34 mm of outboard space beyond the final column
center for its long pivots. Its uniform, full-depth tail grant needs roughly
128.3+40=168.3 mm of active tail length before end margins; site-specific tier/tail
optimization could change that. These are packaging liabilities, not violations
of an unstated internal-footprint or total-height requirement.

The packing proof covers rigid parked parts, axle and side-rail capture under the
specified geometry. It excludes returns, release fingers, writer access, guide
bodies, frame deflection, assembly/service access and extra tolerance expansion.
Opposed stacking is an envelope allocation, not a constructed synchronized release.
A functioning transition still needs a writer to take axial load before straightening,
retain support throughout 40-mm motion, reseat/proof both directions, and withdraw
only after acceptance. The captured pivot does not supply that missing writer.

## Architecture consequence and decision

Selection remains indexed independent heads; energy remains the supported writer;
retention is unilateral self-energizing edge friction plus an opposed lock; load
path is tail→edge→plate→axle→side rails→frame, with the guide closing lateral force.
Verification needs height **and proof load**, continued capture after failed proof,
and bounded retry/module stop. A tilted plate can remain geometrically seated yet
creep; perfect height readback is not evidence of holding capacity.

Two directions repeat 12,800 plates, captured bearings and return functions, plus
at least 12,800 working tail-edge contacts and 6,400 lateral guide interfaces. Shared
printed side rails remove neither bearing fits nor correlated frame/warp faults.
At $250 reserved for shared equipment, all purchased site hardware must fit within
3.906 cents/site at the $500 ceiling: only 1.953 cents per direction before any
other site parts. This is an allowance, not a sourced BOM. Printing substitutes
assembly, wear and precision-fit risks; it does not make them free.

E-163's optimistic full-service bound still applies: 6 s overhead plus
`ceil(6400/H)*tcell` needs H=27/68/121/221 at tcell=.1/.25/.45/.8 s for strict <30 s.
This geometry earns **no** new time estimate. Capture, unload, both releases, travel,
relock, proof, empty repositioning, retry and settling must fit tcell/overhead.
Unchanged regions retain their locks by command, but shared-frame disturbance and
readback false acceptance remain unresolved; no local-isolation qualification follows.

The comparison is unfavorable enough to pause this embodiment without an FEA or
print request: it adds hinges and edge stress without eliminating local returns,
selectors or writers. E-148 broad-area jaw remains a force/preload control (its
field integration is at head scale, not a demonstrated 6,400-site memory).
A-019 distributes friction across leaves but still owes wedges, overlap, local
isolation and assembly economics; neither control is selected or qualified.

Reopen fixed-pivot plates only with changed tolerance/material evidence or a topology
that reduces the repeated bearings/edge stress while maintaining release and support.
Do not generalize this result to floating canted collars, flexure supports or all
self-energizing clamps. Next higher-value question: can A-019-style leaves be made
as shared slotted sheets with independent local clamping, avoiding individual leaf
assembly without mechanically coupling unrelated runners? Test finite reach and
cross-coupling before stress refinement; compare a broad-area jaw and positive seat.

Self-review: polygon first-contact bisection independently reconstructs the analytic
angle; 16/64/256 interval checks agree within 3.6e−15 mm/rad, and just-past-seat
geometry penetrates the tail. Actual vertex force moments close within 1e−9 N mm.
Continuous trigonometric extrema, rather than angular samples, establish the packing
envelopes. Bore-radius error is below 1e−12 mm. Zero-clearance/thickness and
opposite-load limits checked. These verify the rigid model, not contact life,
finite stiffness, dynamic support transfer or physical reliability.
