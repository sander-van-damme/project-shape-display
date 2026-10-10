---
status: complete
builds-on: [E-095, E-094]
---

# A rigid two-aperture pickup lock loses the capture envelope

**Reject the unpreloaded two-aperture deadbolt implementation; retain unilateral
pickup as a contact principle.** A finite nominal joint can unlock, slide and
relock, but its insertion-clearance and retaining-web requirements conflict at
the E-095 datum bounds. Even the nominal fitting lock permits enough inward
motion to lose the previous 0.1-mm capture overlap. This is new negative geometry
evidence, not a ban on positive locks, compliant preload or enlarged selectors.
Do not refine its slot widths or propose a print.

Input main `5b6151a`. Reproduce with
`python3 tools/curated-experiment-checks/E-096/pickup_lock.py`.
Evidence: generated axis-aligned solid boxes, deterministic geometry/error
screens and independent interval bounds; self-review only. No contact forces,
measured process distribution, material strength, real writer or hardware pass.

## Generated joint and transition

The E-095 2.4-mm lip still translates 1.4 mm in x. It is joined through a finite
neck to a rear tail spanning x=−0.5…2.9, y=1.2…2.8 and z=1…1.9 mm relative
to the foot. Two rectangular through apertures have x centers 0.5 and 1.9 mm
and y extent 1.6…2.4. A grounded-in-the-column bolt at x=1.9, y=1.7…2.3
engages either aperture. Thus the moving material, its voids, rails and bolt
are distinct solids; root overlap is no longer the joint model.

Nominal upper/lower guide rails surround the tail's front/rear edges; end walls
limit q to 0…1.4. A 0.4-mm-wide bolt spans z=.7…2.2 when engaged and retracts
1.7 mm before lateral movement. The generated route is unlock → slide → relock
and its reverse. Width-1.0-mm apertures pass at 1/16/64 subdivisions per leg
(**12/102/390 states**). Intermediate motion is affine: vertical withdrawal
stays in the aperture, and the retracted bolt's lower face is above the entire
sliding tail. The finite swept interval establishes clearance between samples.
Trying the same lateral move with the bolt still inserted produces a
**0.216-mm³ intersection with the middle web**.

These are prescribed translations with a vertically retained bolt **granted**;
no autonomous actuator, bolt keeper or assembled writer is credited. The rails
only bound the nominal translational path: their 0.4-mm vertical gap on each
side permits lost motion and angular play, so they do not reproduce E-095's
ideal moment-reacting guide. Under lift, the tongue can rise 0.4 mm to the upper
rails before lifting the housing. Simply carrying over the 3.6-mm setter
headroom would therefore be unjustified (3.2 mm if this added lost motion is
combined with E-095's vertical bounds). This failed joint is not the new
accepted headroom reference. Full column connection, guide reactions and bank
tiling are unproved; the rear end walls need their own adjacent-cell check.

## Bounded lock synthesis and failure witnesses

Generate aperture widths {0.8,1.0,1.2,1.6,2.0} mm, bolt widths {0.4,0.6,0.8}
mm and relative-datum scenarios e={0,.1,.2,.3} mm: **60 parameter cases,
3,840 corner evaluations** (including repeated zero-datum corners). For valid
nonoverlapping aperture solids, **4,224 inserted-solid checks** at both endpoints
agree with the insertion inequality; overlapping-hole geometries are rejected
by the web screen. Each hole
and bolt x face has ±0.1-mm error; slider and bolt datums each have ±e. Bounds
may be coherent across a bank; no independent-cell probabilities are used.
Only this insertion/retention dimension is screened under error, not all 3D
assembly faces. These are epistemic scenarios, not X1C accuracy claims.

For aperture width w and bolt width b, the independent continuous bounds are:

- Minimum insertion side clearance: `(w−b)/2−2e−0.2`.
- Minimum web between adjacent holes: `1.4−w−0.2`.
- Maximum clearance permitting inward movement at an endpoint:
  `(w−b)/2+2e+0.2`, before clipping at the opposite endpoint.

Require a **0.05-mm geometric insertion reserve** and a **0.2-mm web** solely
as rejection screens; neither establishes printability or load capacity.
The web bounds w≤1.0; insertion requires w≥b+4e+0.5. At e=.2 even the thinnest
b=.4 requires **w≥1.7**, contradicting w≤1.0. All cases at e≥.1 fail, and the
only sampled insertion/web survivor (e=0,w=1,b=.4) permits up to 0.5-mm inward
play across its edge-error box. A larger width cannot solve both constraints;
the continuous inequality covers untested widths too.

Two finite failures avoid relying only on these scalar screens:

1. At nominal dimensions, the active slider can move from q=1.4 to **1.11 mm**
   without touching the inserted bolt. Applying that 0.29-mm withdrawal to
   E-095's adverse retained lip [1.2,3.5] / finger [3.4,4.6] eliminates overlap.
   The lock dimension and deck registration errors can coexist; this is an
   explicit counterexample, not a claimed simultaneous maximum of all bounds.
2. At slider datum −.2 and bolt datum +.2, a generated deformed-aperture tail
   intersects the inserted bolt by **0.054 mm³**. Forcing insertion cannot be
   credited as successful locking.

E-095's minimum 0.1-mm capture/inactive reserve leaves only 0.05 mm for additional
inward displacement if retaining its 0.05-mm geometric gate. An unpreloaded
clearance lock cannot silently count its free play as zero. A spring bias,
wedge, over-center restraint, amplified remote key or changed selection
coordinate could escape this failure, but each changes the force/reset/packing
problem and requires a finite mechanism. A vertically unsecured bolt could
also escape; its retention remains deliberately granted, not solved here.

## Assembled writer consequence and next decision

The retained hook and bolt ride with the terrain column. Two same-row columns
at 0 and 40 mm therefore present setting handles 40 mm apart vertically. A
single short fixed-height tool cannot act on both merely because its x address
is correct. An engagement blade covering the range plus an assumed 1.5-mm
handle engagement span needs **at least 41.5 mm** of active height; this is a
reach envelope, not a working universal fork. Otherwise independent vertical
reach, repeated height visits, a ground-referenced state or a motion-converting
local interface must be paid for. Stop-setting and hook-setting are consequently
not yet demonstrated to share the 80B data channels in E-094.

The canonical E-094 allocation now charges E-095's fixed home −2 → top45 →
home−2 route, with nominal pickup/deposition waypoints at stop height +1 and
all existing support proofs, retry and final return. Its **94-mm travel is not
just an extra 4-mm time increment**: nonzero initial/final contact legs add
rest-to-rest segments. Error-dependent contact spread and actual proof remain
inside the explicitly unqualified support slots. No timing feasibility follows
from the failed lock. Under the central grants, four banks now take
**24.552 s** and permit **<0.75943 s per stop-setting round**; the eight-bank
local range is **7.389–9.249 s**. Those are competing allocations, not hardware
performance.

Continue the campaign with **ground-referenced height memory and selection**:
generate a stepped rotary stop's complete unloaded sweep and a translating
compression-stop comparator, including indexing retention and the setter's
approach/withdrawal. Test whether the actuator can stay at a common datum and
whether a changed pickup coupling avoids a moving-height hook writer. Keep the
E-095 ideal contact envelope as a comparator, not a finished assembly. Stop
this two-hole-lock refinement unless changed retention or amplified spacing
removes both the insertion contradiction and lost-contact witness. No printing,
purchase or new worker is justified.
