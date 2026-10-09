---
status: complete
builds-on: [E-090, E-089]
---

# Square-key retention consumes the decoder's error reserve

**Stop the alpha=1, 21-level square-key/free-clearance embodiment under the
composed adverse bounds.** The positive lock can remain fully engaged while
its cursor moves far enough to miss the intended slot or admit a wrong neighbor.
No lock-slot width simultaneously guarantees insertion and adequate decoder
accuracy in that scenario. This is a scoped rejection of this retention
principle/precision combination, not of multilevel commands or measured X1C
capability. E-090's result at an *assumed* 0.4-mm datum bound remains correct;
this investigation replaces that bound with an explicit retention stack.

The finite two-track sign gate passes its rigid contact subsection. Its
84-mm body / 164-mm sweep preserves most of E-090's conditional sign-isolation
saving, but adds two locally independent sign probes and stop tongues per cell.
The 5/9-level comparators still pass the combined geometric section. Keep the
9-level comparator for investigating output coupling and loaded support; do
not optimize the failed 41-position square lock or treat 18 levels as a new
product specification. No complete mechanism, loaded release, time/cost pass,
manufacturing yield or hardware performance is established.

Input main `fefb372`. Reproduce:
`python3 tools/curated-experiment-checks/E-091/retention_gate.py`.
Deterministic rigid polygon sections, exhaustive state/error corners, interval
inversion and swept envelopes; no random seed, calibrated priors or physical
measurements. Source imports E-090's convex-polygon checker. The checks are
self-review, not independent external validation.

## Finite retained word and coupled uncertainty

Generate H-level commands q=−(H−1)…H−1 at pitch `p=40/(H−1)` mm; alpha=1,
80-mm signed cursor stroke. The cursor carries separate lanes for the equality
slot, positive/negative sign windows and indexing rack. Lane separation and
full 3D guide/column packing are **not** established.

The rack has 2H−1 rectangular holes, nominal width W=1.3 mm, in a 1-mm plate.
A square D=0.6-mm dog at a fixed station enters 1.5 mm into the selected hole.
Its square walls provide positive restraint along the cursor coordinate;
retention does not rely on friction. A collar behind the dog and a transverse
keeper prevent withdrawal: seated collar y=[−1.9,−1.5], keeper
[−2.4,−2.0] mm. Relative keeper placement ±0.1 mm permits at most 0.2-mm axial
retreat before hard contact, leaving ≥1.3-mm dog insertion. This is a local
keeper section, not a finished row actuator. The keeper itself needs a
positively retained drive; row bending, fracture and escape out of plane remain
unmodelled.

Required setting order: grounded columns and inhibited outputs; engage and
hold the writer; release keeper; positively withdraw dog and prove clearance;
move cursor; insert dog while writer holds; engage keeper; release writer;
prove the retained command before enabling output. Clearing uses the same
sequence. Withdraw sign/query pins before cursor movement. The writer's
positive coupling, force, registration and readback are **interface
requirements**, not generated hardware credited by this result.

Uncertainty is expressed as competing bounded scenarios, not distributions:

- Each rack-hole and dog-width error is ±0.1 mm, independently permitted to
  reach its bound. Common hole enlargement/key shrinkage across a bank is allowed.
- Writer placement relative to the actual index hole is bounded by ±0.2 mm.
  This includes its as-yet-unimplemented drive/coupling error; no measured
  capability is assumed.
- Residual index-to-decoder datum error is ±0.2 mm, combining uncalibrated
  relative feature placement, registration and guide alignment. This is
  separate from cursor movement inside the engaged key.
- Decoder slot/pin sizes retain E-090's ±0.1-mm bounds; shared reader gain
  error remains ±1%. Datum, clearance direction and gain can align coherently.
  Wear, elastic deflection and dynamic overshoot are not free additional margin.

The narrowest hole/widest dog leave 0.25-mm half-clearance, hence **0.05-mm
insertion reserve** at the assumed writer error. The widest hole/narrowest dog
leave **0.45-mm possible cursor movement** from the nominal center while the
key remains seated. Adding the 0.2-mm residual datum gives **E0=0.65 mm**;
1% gain contributes another 0.4 mm at the extreme reader coordinate.
No passive centering, maintained preload or post-release immobility is assumed.

This is not repaired by tuning W. With nominal gap `g=W−D`, width bound s=0.1,
`Cmin=g/2−s`, `Cmax=g/2+s`. Guaranteed capture of setter error S requires
`Cmin≥S`, so even with zero insertion reserve, `Cmax≥S+2s`. At S=0.2 and
residual datum R=0.2, the best achievable E0 is ≥0.6 mm. E-090's strict decoder
condition at p=2 is `p>2(E0+0.4)+0.2`; its right side is already ≥2.2 mm.
Positive capture reserve makes it worse. The source also enumerates 24
setter/datum/gain scenarios and checks this interval result against seven
nominal lock gaps; these are parameter sensitivities within one topology.

Concrete same-sign witnesses at H=21:

- q=20, reader=20, datum +0.65, gain +1%, slot 2.3 and pin 0.5 mm:
  dx=1.05 mm; the pin fails to enter. The independent polygon contact result
  stops essentially at the plate surface.
- q=19, reader=20, datum −0.65, gain −1%, slot 2.5 and pin 0.3 mm:
  dx=0.95 mm; the wrong neighbor fully enters 1.5 mm. Sign gating cannot
  reject it, and the depth threshold cannot distinguish it from a true match.

A dog-depth sensor can accept both extremes of the 0.45-mm lateral clearance.
A position reading immediately after writing does not prevent subsequent
motion within that clearance. Reopen this 41-position embodiment only with
changed evidence: the generated key needs gain uncertainty **strictly below
0.625%** with the other bounds unchanged; retuning the gap at 1% requires
`S+R<0.3 mm` plus positive reserves. Alternatively change retention to a
mechanism that establishes a persistent datum, or change the encoding. None
of these improved capabilities is granted here.

## Finite sign isolation and transitions

A stationary pair of sign pins reads two separate cursor lanes; these pins do
**not** ride on the moving equality reader. In the positive lane, cut a window
in cursor coordinates `[−41.1, −p+1.1]`; in the negative lane use
`[p−1.1, 41.1]` mm. Each lane's blocking body extends from −42 to +42 mm.
At command q the stationary pin is at cursor coordinate `−qp+datum`.
The same 0.4-mm nominal pin/0.2-mm tip/0.4-mm chamfer as E-090 is used, with
±0.1-mm shank width and independently ±0.1-mm window endpoint errors.

The generated polygons guarantee full insertion for every correct nonzero
sign under ±0.65-mm datum error, with a minimum **0.1-mm edge reserve**.
Neutral and opposite-sign commands cannot fully insert; finite outer lands
also cover the extrema. Unlike equality sensing, sign sensing has no moving
reader gain term: it is local to the fixed index reference. Any additional
error of that local reference must fit the declared 0.65-mm bound.

Each sign plunger carries a tongue in a separate output-follower lane. The
output lug must traverse x=0…1 mm with transverse extent [0,1]; the tongue
occupies x=[0,1], transverse `[−2−d, 0.8−d]`, where d is sign-pin insertion.
The finite rectangles block the stroke while the tongue overlaps the lug and
clear it on full sign insertion. Independent ±0.1-mm stop placement and
±0.1-mm depth error leave ≥0.2-mm blocking overlap at any wrong-sign partial
entry and ≥0.5-mm clearance on full insertion. This prevents E-090's
wrong-sign face-end bypass from enabling that output path.

A common phase drive queries only the corresponding sign lane, retaining its
pin through acquisition and every deposition query. Acquisition uses the
sign-authorized follower; deposition additionally requires the equality
probe's depth-authorized follower. Their common energy cam and the physical
series connection to the loaded support are **still ungenerated**. Two local
stop sections do not prove this complete linkage. In RETURN, the common stop
limits sign insertion to 0.3±0.1 mm; even adding 0.1-mm depth error cannot clear
the shortest tongue. Return-stop strength/retention/proof remain required.

Pins withdraw to −0.2±0.1 mm before setting, wholly outside the plate.
A square key that stays inserted blocks a command move at the intervening land,
even when both old and new indexed endpoints are collision-free. The source
checks full withdrawn swept rectangles for every old/new command pair and
retains this midpoint collision witness. Commands to pull a jammed part are
not proof of withdrawal: captive pullback hardware, available force and
individual clearance sensing remain open. A failed proof must retain existing
terrain support and inhibit motion. There is no friction, fatigue or jam-force
qualification.

## Resolution, repeated burden and decision

For the generated key and ±1% gain box, capture and neighbor-exclusion reserves
are both `p/2−1.15` mm. The analytic boundary is H≤18, with almost no reserve
at H=18; this is sensitivity, not a recommended resolution or fabrication pass.

| Levels H | Command positions | Pitch mm | Combined reserve mm | Section outcome |
|---|---:|---:|---:|---|
| 5 | 9 | 10 | 3.85 | conditional survivor |
| 9 | 17 | 5 | 1.35 | conditional survivor |
| 17 | 33 | 2.5 | 0.10 | conditional survivor |
| 18 | 35 | 2.353 | 0.0265 | conditional survivor, small reserve |
| 19 | 37 | 2.222 | −0.0389 | fails adverse box |
| 21 | 41 | 2 | −0.15 | fails adverse box |

An 84-mm common cursor body also covers all permitted equality-reader pairs
in these cases; its swept length is 164 mm before guides, setter and installation
allowance. This is one-axis geometry, not full bank packaging or board volume.
The long windows remove material; bending of the remaining lands is an open
model discrepancy, not accounted for by a rigid-polygon pass.

This embodiment has 12,800 sign pins/tongues, 6,400 query pins, 6,400 square
keys and 6,400 memory cursors: **32,000 local sliding members**, before support
parts and keeper/guide interfaces. Independently compliant sign/query push paths number
19,200. Reusing E-090's three spring scenarios, the conservative sign-plus-query
upper reaction for an 800-cell bank is **152/640/2,080 N**; simultaneous
all-blocked sign/query states need not be attainable. Holding a sign query
through the phase avoids repeating its insertion at every level but retains
its static reaction. Neither motor sizing, setting time nor a priced channel
follows. Individual sign clearance, key engagement/withdrawal, query depth and
retained-position proof remain in the time/cost boundary.

Continue the same campaign with the 9-level square-key/sign-gate section as a
**geometric comparator** for loaded transfer and output coupling; preserve
E-089's selective deck and direct writer controls. A support/packing failure
may reject this embodiment regardless of encoder resolution. No new campaign,
printing, purchase or nominal 41-state tolerance-refinement is justified.

Verification covers 5,504 sign error cases and 22,016 stop/lug cases, 1,376
index-hole insertion cases, 5,734 withdrawn command sweeps, and 43,168
same-sign equality state/width/datum/gain cases. Every equality full-entry
decision is compared with the finite 84-mm plate polygons. Separate bisection witnesses reproduce
both H=21 failures. Slot contact is monotone for the specified 1.5-mm stroke
and 3-mm shank; bisection resolution <3e−11 mm is far below the 1e−8-mm test
tolerance and implies no physical precision. Bounds, not sampling, cover the
piecewise-linear free sweeps. No probability, complete assembly, dynamic
settling, wear, stiffness, readback reliability or support qualification follows.
