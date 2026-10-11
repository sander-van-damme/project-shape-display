---
status: complete
builds-on: [E-098, E-099, E-170, E-125, E-156]
---

# One travelling crossbolt exchanges ground and carrier support through a bridge state

**Retain a conditional three-position transfer topology; stop the one-shot flat
handoff and tested serial schedule.** A crossbolt carried by each nonrotating column
replaces separately selected pickup and ground sliders. Its intermediate position
overlaps fixed and moving periodic ladders; a shared unloading stroke tolerates
unequal support heights. The finite shelf/key section admits this route under
explicit bounds. Guides, connected ladders, selector retention/access and carrier
arrest are unbuilt. The straightforward eight-group schedule takes **30.942 s at
16 banks**, missing the update target. No machine or hardware is admitted.

Input main `6af327f`; LAB-281. Reproduce:
`python3 tools/curated-experiment-checks/E-172/routing.py` (standard library).
Evidence: finite rectangular solids, quasistatic unilateral contact, deterministic
bounds, state reach and schedule arithmetic; self-review only. No physical data,
calibrated priors, sourced price, fabrication CAD or independent validation.

## Discovery and controls

Three different recombination strategies: invert the selector's supporting body;
remove selective pickup through always-available traction; replace mechanical pickup
with a common pressure field. Repository crossbolt/transfer-key/shuttle/make-before
searches and E-098/E-099/E-125/E-139/E-150/E-156/E-166 were checked. Only the first
produced a new combination here. This is not literature novelty or search saturation.

| Combination | Selection + energy + retention/load + recovery; disposition |
|---|---|
| Column-carried transfer key | Spatial writer shifts ground→bridge→carrier; common ladder translates; reverse sequence deposits onto fixed ladder. Retained ground position stores height. Read actual key/load/top; retain carrier on failed proof. Removes one independent local slider, adds travelling key guidance and two five-seat ladders. Conditional section below. |
| Always-coupled traction + dog | Shared friction sleeve slips on locked columns; release a ground dog to follow signed source motion; reclose at target. Read output/support; input loss while released needs arrest. Removes pickup command but adds 6,400 preload/wear contacts and unchanged-column drag. Recombines E-150/E-156; no new survivor. |
| Common pressure + latch | Pressure-driven columns use local ground release/target stops; reverse pressure or a real return lowers. Read height/support; recover with retained support, not pressure alone. Removes deck pickup, reinstates A-020/E-064 cells, seals, returns and selectors. Duplicate burden. |
| Separate deck pad + dog | E-098/E-099: shared lift and separate retained pickup/ground sliders; serial/parallel writers, individual support proof. Nine-height embodiment needs 20 scans; 16 banks/20.636 s under grants. Partitioning did not remove writing. |
| Direct heads | Spatial bilateral powered capture transfers between ground supports; failed proof retains head. E-099 grants 4 banks/18.854 s; E-123/E-125 compact capture/guide failures prevent treating that as machine performance. |
| Screws | Spatial rotary drive, thread height memory, grounded flank reactions; read output after release and arrest moving loss. A-007 rejects its scanning embodiment; E-156 shared drive adds inertia/backdrive/contact burdens. Neither excludes every screw or supplies a free brake. |

Cheap bounds for the duplicates: if each always-engaged sleeve slides with the
same traction F needed for motion, 6,400 locked sites dissipate `6400 F L`:
**51.2/512/5,120 J per 80-mm cycle** at F=.1/1/10 N. This same-traction scenario
is not a thermal limit; static/kinetic ratios and preload can change it. An
untiered piston confined to one pitch has area ≤25.8064 mm² and ideal pressure
≥**3.88/38.8/387.5 kPa** at those loads, before walls/seals. Neither earns a new
model of an existing family. All loads are scenarios, not product requirements.

## Generated section and supported transfer

Five heights are `j*10.1 mm`, j=0…4: 40.4-mm nominal travel, **40.3 mm** after
independent ±.05-mm endpoint errors. Five levels are a design choice. Periodic
seats preserve E-170's common-datum acquisition at different old heights.

Key: 3.4×1.6×.8 mm; x center q=−.7/0/+.7 mm. Fixed shelf x=−2.3…−1.4;
carrier shelf x=1.4…2.3; both y=±.8, thickness 1 mm below support. Fixed planes
are `j*10.1+g_j`, moving planes `j*10.1+c_j+d`. The key has an **ideal horizontal
prismatic joint to the column**. No cap rotates. Shelf footprints are laterally
disjoint, avoiding E-170's crossing plates, but missing connecting spines/bridges
receive no clearance credit. Maximum key span is 4.8 mm at 5.08-mm pitch; a
4.6-mm cap is an envelope only. Carrier shelves sweep **122.6 mm vertically**
over ±40.4-mm motion and preload, before frame, caps, brakes or service space.

Grant moment-reacting column/key guides, three positively retained selector states,
a writer accessing/reading keys at arbitrary terrain height, powered lift and a
grounded carrier brake. None is generated. A long moving command tongue might
provide fixed-datum access, but adds repeated structure/guidance and earns no fit
or cost pass. A two-position solenoid is not a three-position selector. Key-joint
clearance, force transmission and preload are separate from shelf contact.

For `g_j,c_j ∈ [−e,e]`, e=.05, set `a=2e+.1=.2 mm`. With old=o, target=t,
Δ=(t−o)*10.1, execute:

1. At d=−a, slide ground→bridge with carrier below the seated key.
2. Raise to d=+a: key height is `max(o*10.1+g_o,o*10.1+c_o+d)`.
   Carrier acquires before ground unloads; shift bridge→carrier.
3. Move d to Δ+a, entirely clear of fixed shelves.
4. Shift carrier→bridge above target; lower d to Δ−a. Height becomes
   `max(t*10.1+g_t,o*10.1+c_o+d)`: ground acquires before carrier unloads.
5. Shift bridge→ground; return d to −a. Unchanged ground-selected keys are
   x-disjoint from every carrier shelf throughout its complete return.

**1,024 support-height sign patterns × 20 ordered pairs = 20,480 routes /
983,040 states** check finite collisions and positive vertical contact under
.1/1/10-N downward loads; ideal guides react moments. Every support switch and
lateral overlap breakpoint plus interval midpoints are included. Nonsymmetric
interior cases use 4/16/64 subdivisions. Affine geometry, x separation and a
conservative **7.8-mm upper-shelf clearance** bound cover intervals between
samples. This is continuous quasistatic contact, not dynamic lowering, signed-load
qualification or a reliability sample. Independent box-touch/volume identities,
reaction sums, state reach and a hand-summed schedule provide self-checks.

## Bounds, failures and support limits

Horizontal scenarios allow key registration ±e, key half-width error ±e and
facing shelf-edge error ±e. Bridge overlap is `.3−3e`, off-clearance `.4−3e`,
adjacent-key gap `.28−4e`; corner enumeration agrees. Breadth allows ±e face
size error with ideal y alignment; transverse misalignment/rotation are excluded.

| e (mm) | Bridge overlap | Off-clearance | Neighbor key gap |
|---:|---:|---:|---:|
| .025 | .225 | .325 | .180 |
| .050 | .150 | .250 | .080 |
| .075 | .075 | .175 | −.020 |
| .100 | 0 | .100 | −.120 |

At .075, actual opposed end-selected key solids overlap by **.0256 mm³**.
At .05, bridge bearing
area ≥.225 mm² implies mean pressure **.444/4.44/44.4 MPa** at .1/1/10 N;
no strength allowable or pass is assigned. Correlated batch/assembly biases and
opposing local errors are allowed; a common adjustment cannot correct differing
cell errors. These are **bounds, not X1C priors**. Warp, hole/first-layer effects,
roughness/friction, layers, anisotropy, guide play, bending, creep, fatigue and
wear remain discrepancy. No yield or calibrated fit capability is inferred.

A one-shot flat slide at d=0 fails either floor-mismatch sign: +.05 gives
**.024 mm³** key/shelf penetration at bridge; −.05 leaves a .05-mm fall after
donor release. Thus bridge/unload is functional for this rigid section. Ramps
or compliance would change contact and required input force.

Missed bridge→carrier selection leaves the key under the next fixed shelf:
at d=9.5, actual intersection is **.288 mm³**. A falsely accepted ground command
left at bridge lifts an unchanged column **.5 mm** at d=.5. Four setting/retention
observations and two support proofs per changed site mean at least **38,400
proof opportunities/map**, before final reading/registration. Common reader bias
can defeat many cells; no false-accept probability or independent retry is known.

During carrier-only travel, torque loss leaves a free collective vertical
coordinate: **40/400/4,000 N** of column load in a fully selected 400-cell bank
at .1/1/10 N/site, before carrier weight. Retained key position cannot arrest it.
A grounded bank brake must survive input loss and bound excursion/energy; it is
unbuilt. Failed proof retains key/carrier for supported correction and one budgeted
retry. Persistent fault, carrier breakage or false proof is not map completion.

## Complete schedule and cost boundary

Group changed sites by signed difference −4…−1,+1…+4. Each of eight groups runs
the complete route from/to carrier home. Exhaustive **625 two-cell old/new maps**
check reach; disjoint memberships extend to arbitrary maps. Every row containing
all 20 unequal pairs four times exercises all groups. This is a constructive
schedule, **not an optimum or universal lower bound**.

For B parallel banks, n=80/B rows: four key scans/group give **32n setting slots**
and `32(n−1)` stopped index moves; even serpentine scans return home. Lift time is
`sum over signs and k=1…4 [2move(2a)+2move(k*10.1)]`. Grant v=200 mm/s,
a=5,000 mm/s², .1-s 80-channel slots including approach/set/retention/read/withdraw,
.1 s per 16 group support proofs, 2 s/map for preparation/registration/final
settling, one slot retry plus .4-mm up/down reseat and .1-s proof. Parallel proof,
writer capability, braking and settling have not earned these allowances.

| Banks | Total seconds | Slots/bank |
|---:|---:|---:|
| 1 | 423.941 | 2,560 |
| 2 | 214.341 | 1,280 |
| 4 | 109.542 | 640 |
| 8 | 57.142 | 320 |
| 16 | 30.942 | 160 |

B=16 requires `slot < .1−.941931043420695/161 s` (~94.1495 ms). Central
.02/.05-s slots permit B=16; .1/.2 do not through B=16. Fast 400/20,000 motion
permits B=8/16/16/none at .02/.05/.1/.2 s; slow 80/1,000 permits none. Raising
map overhead 2→6 s adds 4 s. No measured time/force tails. Local changes can
skip empty groups/rows with other keys grounded; no physical disturbance/local
speed is established. E-099's nine-height deck is a different resolution, so its
20.636 s is context, not a matched optimization comparison.

Favorable **82B channels** means 80 selectors + row/lift axes per bank; brakes,
readers and retention must be paid. At B=16, <$500 with $250 elsewhere permits
**<$0.19055/channel** with free bought sites, **<$0.09299** at $.02/site.
$.05/site plus $250 already exceeds $500. $400/$200 caps leave $150/negative
before site purchases under the same reserve. These are allowances, not prices.

Repeat inventory: **6,400 keys/guides/retained three-state commands, 12,800
five-seat ladder strips / 64,000 shelf sites**, plus column guides, frames,
writers, brakes, readers and service routes. Co-printing changes handling, not
loaded-interface count. One 10-s operation/site takes 17.8 assembly hours;
actual print time, material, calibration and repair burden remain unpriced.

## Decision and next discriminator

Stop the one-shot handoff and 32-scan protocol as central-allocation product
proposals; retain the new conditional routing topology. No printing or purchase.
Next compare **co-scheduled difference groups with independent support routing**
at matched five-height resolution/channel boundaries. Preserve actual bridge/
unload motion, every carried support, returns and arbitrary-height writer access.
Stop if fewer scans hide a second resident selector or unbuilt parallel writer.
Only a system advantage warrants retained-key/guide and bank-arrest geometry.
Shared-motion discovery remains unsaturated; do not return to rotating-cap repair.
