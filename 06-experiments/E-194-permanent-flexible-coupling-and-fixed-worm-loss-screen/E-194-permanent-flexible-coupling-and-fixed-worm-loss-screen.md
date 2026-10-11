---
status: complete
builds-on: [E-120, E-121, E-122, E-156, E-185, A-025]
---

# Permanent coupling removes acquisition height, not retention and moving energy

**Retain guided push-pull transmission as a routing building block; stop the
screened resident worm geometries as a fast, passively contained writer.** Rounded
full-density conduits clear without a loop tensioner or perforated sprocket. Their
compression contact, reversal error and retained input remain unresolved. Worm
self-locking at rest does not arrest input inertia quickly enough in the declared
light-load/low-friction corner. No machine selected; no print or purchase proposed.

Input main `86ddd4e`. Reproduce with Python 3 + NumPy:

```
OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-194/coupling.py
```

Evidence: finite envelopes, analytical dynamics/energy and self-review; no contact
CAD, calibrated process prior, measurements, BOM or independent validation. All
inputs except stage-02 constraints are assumptions. JSON is disposable. Earlier
E-120/121/122/156 executables and E-185 default profiles were reconstructed/run.

## Changed combinations and controls

Three varied search axes: push-pull control cables, remote rotary shafts and
worm gearing combining motion with retention. Repository conduit/worm searches
found no explicit object, not a patent novelty claim. E-151 plastic forming differs
from this elastic strip; E-131 screws/A-025 racks remain controls. No saturation.

| Combination | Complete causal proposal; unqualified functions remain charged |
|---|---|
| Guided push-pull | Each top permanently joins a strip in its grounded conduit. Its perimeter end joins a translating nut on a resident screw. Reversible travelling rotary heads address fixed inputs; engaged flanks store height and support load. Actual-top/hold proof before release; keep engaged for correction, support column for repair. Screw coast, rotary dock, strip contact and fittings remain open. |
| Remote torsion | A perimeter worm/wheel drives a housed flexible shaft to a resident pinion/rack; rotary heads select fixed worm inputs. Worm friction retains angle; housings/bearings ground reactions. Read actual top, account for twist, keep drive engaged on failed proof and support the column before shaft repair. Shaft construction/ends, worm arrest and output transient remain open. |
| Local worm/rack | Private worm/wheel continuously meshes with a wheel-mounted rack pinion. A reversible travelling friction-contact rotary writer selects the worm. Continuous flanks replace a released bolt; bearings ground load. Verify top and stationary support before withdrawal; failed proof retains writer and stops source. Finite dock/return, mesh, fits and reader are unbuilt; outage calculation favorably grants instant source separation. |
| Controls | E-121 loop/E-122 tape need private retained rotary coordinates; E-156 retains nut flanks; E-185 direct setter captures old height. None earns a new pass. |

Controls reconstructed: E-120 omits finite bends/end fanout; E-121's helical riser
hits a neighboring core and its local fixed-length loop admits slack; E-122's
central keeper crosses the carriage and tested teeth fail the full error box.
Confinement changes closure and compression, not those results. E-156 retains
resident coast after source separation; E-185's active braking is not outage arrest.

## Finite rounded routing: a surviving building block

Use a left half-row j=0…39, xj=(j+.5)5.08 mm, depth Dj=R+(j+1)s. A vertical
centerline ends at (xj,Dj−R), follows a quarter-circle centered at (xj−R,Dj−R),
then runs left at Dj to x=−R. Full end-guide reserves extend vertically to
height 40 mm and horizontally another 40 mm beyond the exit. Mirror at the
board center for the other half; repeat at 5.08-mm row spacing. No inboard
return branch or spool is needed. At output h, exposed core is h at the top and
40−h at the input; total core length is invariant for either motion sign.

Conduit outer section is 1.3 mm in the bend plane and 3.2 mm across rows:
2×.1-mm strip, .4-mm total gap in both directions, .4-mm walls. These are
construction assumptions, not qualified PLA fits. Capsule envelopes around each
centerline are checked. Core moves inside the reserved channel; caps, attachments,
seams, frame and external screw fanout remain unconstructed.

Exact polyline segment distances include intersections. Subtract twice arc
sagitta to bound finite-curve separation conservatively. Translation makes all
780 intra-half-row pairs equivalent to 39 separation classes: only already
parallel, overlapping straight legs extend. 285 off-origin pair holdouts test
that reduction. Opposed halves have ≥5.08-mm centerline separation; row outer
sections have 1.88-mm clearance. Arbitrary different heights stay inside the
full end sweeps; no unchanged route has to move or release.

| R / depth step s, mm | Gap lower bound, mm (32 chords/arc) | Deepest outer depth, mm | Fixed conduit route, m/board |
|---|---:|---:|---:|
| 5 / 1.7 | .396988 | 73.65 | 923.55 |
| 10 / 1.7 | .393976 | 78.65 | 973.81 |
| 20 / 1.7 | .387953 | 88.65 | 1,074.34 |
| 10 / 3 | 1.693976 | 130.65 | 1,144.37 |

All twelve R={5,10,20}, s={1.7,3,5,10} routes clear nominally. For R=10,s=1.7,
64/128 chords give .398494/.399624 mm. R=10,s=3 gives 1.698494/1.699624.
The tight case approaches the .4-mm straight-lane upper bound. Rounded bends
increase length/outboard width without E-121's spool collision; wider depth
is not proved necessary.

For R=10,s=1.7, complete core inventory is **1,229.81 m**, before terminations;
fixed route plus both full end-guide reserves is **1,485.81 m**. Ideal separate
conduit walls total **4.398 L** (2.96 mm² section), excluding supports, seams,
screws and scrap. The 406.4-mm board extends to 506.4 mm including both outboard
40-mm end reserves and bend offset, before motors/fanout/walls. Larger internals
are allowed but not free. A 256-mm printer needs module seams in these long paths.

Coherent opposed feature/placement bounds ±e reduce outer gap by 3e. At e=.1,
the tight route retains about .10 mm; at e=.2 it admits overlap. A common rigid
translation cancels. Inside the channel, nominal .4-mm clearance also becomes
.4±3e: increasing route spacing does not repair an internal pinch at e=.2.
This is an error box, not an X1C distribution or manufactured yield.

## Signed force, local isolation and source loss

A push-pull strip changes unsupported buckling into **confined contact**, not
zero drag. With assumed E=200 GPa, width 2 mm and pinned free span 40 mm,
Euler first-buckling loads for t=.025/.05/.1/.2 mm are
**.00321/.02570/.20562/1.64493 N**. A .1-mm strip over 10 mm instead gives
3.28987 N. Full end guides are therefore charged above; these values do not
predict collapse after wall contact, nor establish a 1-N or 10-N transmission.
A labelled .5% outer-fiber strain cap requires R≥100t: 2.5/5/10/20 mm,
respectively. This is not a fatigue allowance. The .1-mm/R=5 variant exceeds that cap.
Reversal/contact/folds/abrasion need a confined-strip model.

For a fully occupied uniform elastic bend, U=EI·π/(4R), independent of feed h.
For the .1-mm/R=10 case U=2.61799 N mm, but dU/dh=0: a frictionless conduit with
free input cannot hold a loaded top. Real bend preload/friction could add drag;
no minimum holding force is established. The proposed perimeter screw must do
that work. Do not silently use the conduit as a brake or gravity as forced return.
A quarter bend's ideal inner/outer wall-switch length difference is cπ/2:
**.157/.628/1.257 mm** at total clearance c=.1/.4/.8 mm. Real elastic/contact
reversal can differ; this is a lost-motion scenario, not an error specification.

Remote torsion eliminates axial end travel but adds compliant motion downstream
of the retainer. For assumed shaft stiffness K=.0001/.001/.01 N m/rad and local
pinion radius 2 mm, output stiffness is 25/250/2,500 N/m. A 1-N load deflects
**40/4/.4 mm** even with the input fixed. Granting instantaneous input arrest,
a .1-m/s output at its loaded equilibrium has velocity-induced undamped excursion
v·sqrt(m/kz): **.089–6.325 mm** across K above and m=.002/.1 kg.
Large twist may exceed a shaft's range. This favorable clamped-input test excludes
worm coast. Wound-shaft torsion/bending cannot both inherit ideal solid-wire
properties; neither a shaft nor its housing route is qualified.

Private routes retain unselected coordinates ideally. Common frame, source or
reader faults can affect many cells. Broken strips/shafts may lose support; an
independent catch or supported repair remains necessary.

## Worm inertia discriminator

Single-start worm: module m=.4/.8 mm, pitch radius r=2/5/10/20 mm, wheel N=20/40
teeth, output pinion rp=2 mm, normal pressure angle 20°. Lead slope s=m/(2r),
height per worm radian k=rp/N. A favorable printed-density 1,250-kg/m³ rotor has
root radius r−1.25m, length 4m, .4-mm shell and .4-mm end webs. Wheel root is a
solid disk of width 3m; pinion is a solid 2-mm-long disk. Tooth material, worm
shaft extensions, writer inertia and bearing losses are omitted.
Extra grounded bearing drag could shorten coast; it is not credited without
evidence. Structural adequacy, mesh and full-density staggering remain unproved.

Set f=μ/cos(20°), signed velocity σ=±1 and

```
cσ = (k/s) (f+σs)/(1−σfs)
M = moving_mass + Jwheel/rp²
Aσ = Jworm + σ M k cσ
Aσ θddot = τ − σ W cσ
Fmesh_equivalent = W + M k θddot
Qdot = Fmesh_equivalent (cσ−σk) |θdot|
```

Wheel inertia belongs downstream of friction in M; merely adding its reflected
inertia to the worm would miss its contribution to tooth force. Require Aσ>0
and positive loaded-flank reaction; failure marks the model invalid, not physical
instant arrest. With τ=0 integrate exactly to first stop or report overhauling.
Energy includes both rotors, mass, gravity and heat. Static locking requires s≤f;
kinetic μ must be checked separately.

At W=.02 N, moving mass .002 kg, μ=.02, initial |v|=100 mm/s:

| Module / r / N, mm/mm/count | Downward first-stop travel | Optimistic stroke time lower bound | Necessary independent heads for schedule below |
|---|---:|---:|---:|
| .4 / 5 / 20 | No stop (despite hold at static μ=.05) | — | — |
| .4 / 10 / 20 | 5,773.69 mm | 9.6114 s | ≥3,200 |
| .4 / 20 / 20 | 5,433.13 mm | 9.3236 s | ≥3,200 |
| .4 / 10 / 40 | 23,095.88 mm | 19.2233 s | ≥6,400 |
| .8 / 20 / 20 | 99,301.68 mm | 39.8601 s | None ≤6,400 |

Metre-scale travel extrapolates an infinite mesh; real 40-mm mechanisms meet an
endpoint first. It is a failure witness for that speed, not a prediction of an
actual long drop.

To avoid exceeding the 40-mm travel envelope on immediate drive separation,
v(h)≤sqrt(2 a_stop h) at distance h from the endpoint. Even with infinite powered
acceleration and no speed/power ceiling, stroke time ≥sqrt(2·.04/a_stop). The
table uses the slower sign, **not two signed passes**, then grants .10 s/visit
for engagement/proof/release and 6 s/map for preparation, transport, registration,
verification, settling and one bounded retry: 6+ceil(6400/H)·(.10+t)<30 s.
These are necessary bounds for this schedule; extra travel, independent arrest
or changed geometry reopens it.

Sensitivity is decisive, not a calibrated prior: for .4/5/20, light-load μ=.05/.3
reduces the bound to 305/85 heads, but μ=.02 overhauls. At .4/10/20, μ=.02 and
W=1/10 N give 400/140 heads; an empty/light column must not inherit those payloads.
Some high-load/high-friction cases produce Aσ≤0: the single-flank rigid Coulomb
model cannot resolve that transient. A module/radius box .4±.05 mm /
10±.1 mm at μ=.02 gives 1.674–1.727-m coast at the smaller module and overhauling
at the larger module. Global bias can therefore change every cell's disposition.
Roughness, local tooth error, backlash, first layer, anisotropy, creep and wear
are not represented by this box and cannot be declared safe.

## Full-board decision and next discriminator

Strip replication: 6,400 cores/conduits/input screws/nuts/column attachments,
≥12,800 core ends and housing constraints, plus H rotary heads. Remote torsion:
6,400 shafts/housings/worms/wheels/local rack meshes. Local worms: ≥12,800 rotor
axes, ≥25,600 radial bearing interfaces (two/axis), 6,400 rack meshes and worm
thrust supports. Precision, heat, assembly and repair persist if printed. One
10-s/site operation is 17.8 h; print time/scrap remain unknown.

Even granting a strip drive 100 mm/s and 1,000 mm/s², a 40-mm rest-to-rest
stroke takes .5 s. With the same .10-s visit and 6-s board allocations, ≥165
heads are needed; this omits extra coast/contact settling and is not a validated
perimeter-screw schedule. Head transport, preparation/read/retry cannot vanish.

Joint purchases obey H·c_head+6400·c_site+c_shared<500. With $250 elsewhere,
H=3,200 leaves **<$0.078125/head** with free cell hardware; H=6,400 halves it.
Without heads, all cell purchases share <$0.0390625/site. This is an allowance,
not a sourced market floor. E-185's 82-head direct, 131-head screw and 214-head
Geneva base schedules are different active-drive assumptions; they do not supply
passive coast containment. No complete BOM/time dominance or reliability follows.
All-raising/lowering 1-N maps exchange 256 J of potential energy before losses.
Unmeasured false acceptance p=1e−4 means .64 expected misses/map without
independence; common reader bias may corrupt a row. No perfect reader is granted.

**Stop:** worm refinement justified by nominal self-locking, bend-energy-as-memory
and rigid remote-shaft readback. Not all worms/strips/shafts are rejected.
**Retain:** finite routing, tail closure and compression/reversal/arrest questions.
Next probe a short local guided strip against a straight rigid pushrod with the
same retained input. First find a route avoiding kilometre perimeter inventory
without recreating take-up/dock; stop if none exists. Only then model confined
compression and signed reversal. No printing, machine detailing or inherited
source-loss pass.

Primary sources accessed 2026-10-11; no miniature material properties transferred:

- [Sava control cables](https://www.savacable.com/sava-expertise/push-pull-components): housed cores transmit push/pull; bend clearance and casing anchorage affect lost motion.
- [Suhner shafts](https://www.suhner-components.com/en/offer/flexible-shaft-components/): torque, direction, speed, bend radius and end accommodation matter; no microshaft stiffness/life inferred.
- [SDP/SI gear technology, §9.4, T-80](https://sdp-si.com/D815/D815-Technical-Section.pdf): static boundary μ≥cos(αn)tan(γ), with uncertain friction; not this dynamic geometry or PLA properties.

Self-review: crossing/collinear/parallel distance controls, arc sagitta/refinement,
translation holdouts, core-length closure, Euler and bending-energy limits,
frictionless reflected-mass dynamics, signed heat/work conservation, torsional
energy balance, 16 worm geometries, 72 signed force cases and 27 coherent
friction/load cases. No sampled yield or independent review is claimed.
