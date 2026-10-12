---
status: complete
builds-on: [E-247, E-251, E-252]
---

# One programmed crank radius removes parking, but enlarges physical writing

**Park the offset-radius crank embodiment before lock, yoke or guide detail.**
It replaces nine independently moving rails with one crank shaft and a shared
compensating translation. It removes E-252's intermediate parking and E-247's
80-mm bridge-over-rails obstruction. However, the radius writer must span at
least 80 mm. A single planar head is at least **111.199 mm wide** in the declared
clearance geometry. The base three-head machine takes **177.424 s**; even free
writing and free parallel color decks give **50.662 s** at the best sampled
planar angle. Neither more precise detents nor faster software removes this
mechanical travel. These are scoped scenario results, not universal bounds on
crank mechanisms, attainable speed or component prices.

Input main `6fde094`. Reproduce:
`python3 tools/curated-experiment-checks/E-253/screen.py` (stdlib; imports E-251).
Evidence: **invented mechanism, analytical section geometry, ideal state replay,
and calculations under assumptions; self-review**. No constructed assembly,
contact simulation, measured process distribution, procurement BOM or physical
qualification. The five 0/10/20/30/40-mm levels are a comparison grammar.

## Changed architecture and the first routing cut

Let x run along a row, y across the head, and z vertically. A shaft along x turns
80 radial slotted arms together through theta=0…alpha. Each arm has one positively
locked adjustable-radius follower. A horizontal slot in its vertically guided
output yoke accepts follower y motion and transmits z force. The reusable output
captures and turns a changed column; its finished resident support remains a
fixed bayonet rail as in E-251/E-252. Unchanged columns never transfer support.

A symmetric signed radius r=d/sin(alpha), d=target−old, would give the desired
motion from one fixed shaft. But at theta=0, a connected horizontal yoke slot
covering negative through positive radii crosses the continuous shaft at y=z=0.
An open interrupted slot needs another actual load route. This is a section
obstruction for that construction, not rejection of all signed-radius drives.

Concrete escape: put every follower on the same side of the shaft and move the
shaft carrier downward while it turns. For a chosen positive rmin:

```
r = rmid + d/sin(alpha); rmid = rmin + 40/sin(alpha)
shaft z = -rmid sin(theta)
output displacement = r sin(theta) - rmid sin(theta)
                    = d sin(theta)/sin(alpha)
```

Thus lambda=sin(theta)/sin(alpha) rises monotonically from 0 to 1 for
0<alpha<90 degrees. Every output follows its endpoint interval; no independent
midstroke clutch or parking dog is required. The radial lock now carries load:
programming an unloaded radius does not make subsequent program retention free.
A common cam may couple shaft rotation and carrier translation, but its finite
route, stiffness and two grounded reactions are unbuilt.

Assume an 8-mm shaft-center exclusion for the innermost follower and a 4-mm
outer frame allowance. The exclusion is an analytical envelope allocation,
not a qualified shaft diameter, structural member or FDM tolerance. Keeping
rmin cos(alpha)>=8 gives:

`W(alpha) = 8/cos(alpha) + 80/sin(alpha) + 4 mm`.

Differentiation gives tan(alpha)^3=80/8, alpha=65.1012 degrees and
Wmin=(80^(2/3)+8^(2/3))^(3/2)+4=**111.1993 mm**. At most three nonoverlapping
bays fit 406.4 mm, before other structure. At alpha=60 degrees: rmin=16,
rmid=62.188, rmax=108.376, writer span=92.376, radius step=11.547,
W=112.376, and compensating vertical stroke=53.856 mm.

This removes the competing-rail crossing, not all routing. Cross-arm bending,
shaft/yoke axial separation inside 5.08-mm pitch, vertical guide access,
resident stem passages, modular shaft joints and full capture routing are
unconstructed. Extra decks or external heads can evade the planar bank cap;
they pay extensions, service access and transport. No whole assembly is claimed.

## Supported sequence, isolation and recovery

Use one physical shaft/head and service checkerboard colors serially. Program
all 80 radii once while all columns remain on fixed supports. Reset the writer,
lock and read every radius. A neutral-radius code also inhibits capture;
color gating selects only changed outputs of the current color. The physical
neutral-code reader, gate and retained bilateral capture are obligations.

For each color: select/capture/prove, raise the shared frame 3.2 mm, quarter-turn
captured columns, execute the crank/compensation stroke, turn back, lower onto
the resident seats, prove support, detach, then reverse the empty crank and
carrier. Opposite-color neighbors remain at integer heights. Repeat for the
other color, then index the row. This avoids granting two coincident shafts in
one plane. A parallel-color comparison grants separate 3.2/6.4-mm frames,
arbitrary deck packing and their extra hardware for free; it is an oracle.

Transient load path: column lug → retained capture → output yoke → follower →
radial lock/arm → shaft bearings and compensating carrier → arrested frame.
All loaded coordinates must remain grounded on power loss; a brake on only one
of two uncoupled motions is insufficient. Lost radius retention, follower
escape or a downstream fracture remains a support fault. No brake or proof
sensor is physically qualified. Retention stays engaged during empty reset.

E-252's deeper −60-mm pickup allocation avoids the original capture plane rising
above the resident support: highest nominal pickup is −16.8 mm in serial service.
It still owes ten fixed lug forms/column and the actual jaw/column routing.
E-251's inherited 6,800 nominal cap checks are rerun. During translations caps
are square-aligned; during turns only one checkerboard color is active. Banks
must synchronize color stages for this cap argument; asynchronous off-grid
neighbors are not accepted. Extra transient release height is not usable travel.

Ideal replay covers **15,625 three-cell map pairs / 1,593,750 support
observations**, 2,525 direct coordinate checks and four deliberately broken
support interlocks. These are conditional logic checks, not contact evidence.
125 stable wrong-result/retry cases regenerate the radius from the actual
supported height. One full extra row service covers a completed erroneous row;
there is no promised bounded recovery for off-grid arrest, jam or damaged parts.
Finish under retained support or stop for supported service. Height sensing
alone cannot certify that a follower, radial lock or resident seat bears load.

All unchanged columns retain their primary fixed seat ideally, including the
79 neighbors of a one-cell edit. Frame vibration and actual displacement remain
unmeasured. One local row at the base serial rates, including one complete retry,
takes **14.540 s** before additional distant seek. Skipping an inactive color
could improve sparse changes but does not improve the arbitrary mixed-row case.

## Physical writing and full schedule

Assume rest-to-rest linear v=200 mm/s, a=8,000 mm/s², 2-mm contact strokes,
3-ms contact proof and the inherited 90-degree yaw time .225 s. For the crank,
limit outer-point tangential speed to 200 mm/s and choose tangential acceleration
`8000 - 200²/rmax`; then the conservative sum of tangential and centripetal
accelerations stays <=8000. `R=t(rmax*alpha)` with that adjusted acceleration.
At 60 degrees R=.593665 s. The longer carrier/arm motions are charged, rather
than assigning every output the .225-s time of a free 40-mm straight stroke.

Let J=t(2)+.003, D=80/sin(alpha), n=80/q. The inherited stopped sweep physically
resets radii, carries them through eight positions, releases selected channels,
returns the writer, clamps and reads:

```
Wwrite = 2t(D)+2J+.010
       + n[8t(D/8)+10J+t(D)] + (n-1)t(5.08)+t((n-1)5.08)
ends = 3J + 2[t(3.2)+.003] + 2[.225+.003]
row = Wwrite + 2[ends+2R] + t(5.08)
T = 2.010 + [ceil(80/B)+1] row
```

Temporary retention of released radii before the common lock remains unbuilt.
Eight selective masks are still **51,200 decisions/map**. The three endpoint
stages allocate capture-enable, capture and detach; no extra arbitrary target
word is silently prewritten. All reset, first writing, two color strokes,
empty returns, feed and one causal complete-row retry are inside the boundary.
The two-second allowance covers receipt/computation, registration and final
settling; .010 covers fault read/regeneration. These rates and proof allowances
are not measurements. Expanded timelines independently match the formula.

Scan alpha=20…80 degrees in 1-degree steps plus the analytic width optimum,
B=1…80, and all q divisors of 80. Best allocation among <30-s cases:

| Construction | B / writers / loaded outputs | Seconds | Assumed dollars |
|---|---:|---:|---:|
| Stopped writer, serial colors, routing granted | 27 / 2,160 / 2,160 | 26.983 | $1,858.20 |
| Stopped writer, parallel decks granted | 16 / 1,280 / 1,280 | 28.769 | $1,180.60 |
| Independent absolute writer oracle, serial | 27 / 1,080 / 2,160 | 29.362 | $1,318.20 |
| Independent absolute writer oracle, parallel | 20 / 800 / 1,600 | 26.986 | $1,027.00 |
| Actual three planar bays, 60°, stopped/serial | 3 / 240 / 240 | 177.424 | $379.80 |
| Same three bays, parallel decks free | 3 / 240 / 240 | 127.047 | $379.80 |

Absolute writing replaces each group bracket by 2t(D)+.010 and grants independent
multilevel positioning at binary-channel cost; it is not a constructed writer.
With writing entirely deleted, the fastest sampled planar parallel case still
takes **50.662 s at 42 degrees**. Arbitrary external decks and free writing can
produce faster cases: do not interpret the planar result as a universal limit.
Even deleting the shaft exclusion entirely (an interfering geometric oracle),
the best sampled planar/free-writing/parallel case takes **38.259 s**; reducing
the exclusion from 8 to 4 mm gives **42.015 s** (20…89-degree scan). The stop
is not contingent on treating the 8-mm allocation as a product requirement.
The $195+$20B+$.50Bq+$.02(80B) inherited allocation grants **zero incremental
cost** for crank arms, bearings, compensation cam, radial locks, yokes or extra
decks. At B16, its non-writer subtotal alone is $540.60. No supplier price floor
is asserted. E-247's broad routing-granted control needed B8/640 writers,
27.748 s/$831.80; E-252 needed B10/800 outputs,28.627 s/$811 with added parking
hardware free. The new machine improves a support topology but loses at scale.

## Replication, manufacture and force

Ledger for the serial routing-granted B27 case; largest bank has three rows:

| Function | Per cell / row | Shared head / largest bank | Board |
|---|---|---:|---:|
| Column / guide stations | 1/2; 80/160 | 240/480 resident | 6,400/12,800 |
| Fixed lug forms / primary bearing seats | 10/1; 800/80 | 2,400/240 resident | 64,000/6,400 |
| Adjustable radial slider / positive lock / temporary hold | shared | 80 each | 2,160 each |
| Radial arms / captured followers / output yokes | shared | 80 each | 2,160 each |
| Radius index sites / radial sliding pairs | shared | 720/80 | 19,440/2,160 |
| Yoke sliding contacts / output guide stations | shared | 80/160 | 2,160/4,320 |
| Retained bilateral capture / yaw transmission / enable duty | shared | 80 each | 2,160 each |
| Writer channels / radius readback duties | shared | 80 each | 2,160 each |
| Shaft / compensation carrier / release frame / yaw drive / feed | shared | 1 each | 27 each |

Fixed forms are not moving failure sites. Springs, journals, sockets, inserts,
wire terminations, return details and calibration fixtures remain unknown,
not zero. There are no new resident hinges, individual springs or installed
local latches. Yet thousands of head sliders and loaded lock contacts are not
saved by calling them shared. A broken head blocks up to 240 cells; a shared
shaft/carrier failure affects the active color. Replacement needs columns on
proved resident support, or independent props for interrupted service.

At 60 degrees, a deliberately crude stock allocation of one 3×6-mm crank bar
and two same-length yoke rails per channel is **12.641 L at B27**, excluding
followers, output rods and frames. Add E-252's 2.198-L resident stem/lug stock:
14.839 L, about **305–916 extrusion hours** at assumed 15–5 mm³/s and 10% scrap.
These blanks do not prove stiffness or nesting and are not sliced print times.
At five seconds per column insertion plus ten seconds for each of four head
placements/channel, assembly already totals **8.89+24.0 hours**, before wiring,
2,160 individual proofs and 27 head alignments. Long members and layer direction
must be reconciled with the 256-mm bed; no yield estimate is assigned.

The 11.547-mm radial index spacing is generous compared with E-247's narrow
selector cases; timing fails without a microscopic fit argument. With an
illustrative 2-mm follower, half-clearance `(pitch-2)/2-e` is 4.423 mm at e=.35.
That is indexing geometry, not radial holding accuracy or bearing strength.
For radius and common-carrier errors each bounded by ±.15/.35/.70 mm plus
±.5-degree common angle error, exact endpoint calculations give maximum height
errors **.482/.855/1.509 mm**, assuming the ideal compensation law otherwise.
No product height-error threshold or X1C distribution is inferred. Carrier bias,
shaft phase/twist and reader zero are correlated across a color, while slider
error is local. Additional compensation mismatch, wear and flexure worsen the
model; no independent-cell reliability multiplication is justified.

At alpha60 a vertical output force F gives radial lock force F sin(alpha).
Forty outputs at 1 N each give **.866 N per lock**, up to **4.335 N m starting
shaft torque**, and 40 N carrier reaction, before moving mass, friction and
inertia. At .1/10 N the torque scales to .434/43.350 N m. These are load
scenarios, not miniature requirements. Large opposing shaft/carrier work cannot
be deleted because useful net displacement is small; cancellation needs a real
coupled transmission. Positive capture avoids a gravity-following assumption,
but makes follower/yoke retention and reverse-force capacity mandatory.

## Decision and next discriminator

Retain the offset-radius identity and its exact width bound as scoped knowledge.
Stop the single-plane crank and stopped radius writer. Do not optimize detents,
yoke slots or smaller shaft clearances; the free-writing planar oracle already
misses the timing boundary. Reopen only for a concrete routed encoding/drive
that removes substantial travel or multiplicity with a better full ledger.

Next, leave the shared solid-selector campaign: reconstruct E-222's **head-only
hydraulic** comparison and test whether a shared positive-displacement source
with independently closed head ports can reduce physical target writing. This
is distinct from 6,400 resident wet circuits and E-246's clamping-pressure strip.
First bound required valve functions, signed movement, flow, trapped-volume
compliance, leakage and loaded stopping at the full channel count; compare a
sourced complete allocation to the mechanical controls before seals or manifolds.
A common shutoff still cannot ground differential cylinder motion, and shared
optical height feedback does not certify independent support. No fabrication
is authorized by this direction alone.
