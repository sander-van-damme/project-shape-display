---
status: complete
builds-on: [E-168, E-056]
---

# Wider bayonet bearings escape mean pressure at the expense of rotating clearance

**Retain a conditional wider-lug escape; defer rotary-head detail.** A 4.3×2.4-mm
lug on a 1.48-mm-radius stem with 4.6-mm cap has 1.702 mm² of adverse centered
bearing area: 5.875 MPa mean at the assumed 10 N, versus 28.409 MPa for the
original 4×.9 lug on that same thick stem. But larger lugs can hit a stationary
neighbor's cap, and eccentric loading still requires substantial pressure or a
moment through the guides. No load capacity, reliability or machine selection
follows. This is a new reciprocal interference / loaded-bearing discriminator
within the E-167/E-168 topology, not discovery of a new mechanism family.

Input main `7ef15a1`; LAB-276. Run:
`python3 tools/curated-experiment-checks/E-169/bearing.py`.
Standard library, deterministic enumeration and exact geometry/contact integrals;
JSON is disposable. Evidence: rigid geometry, explicit bounded scenarios,
ideal elastic foundation calculation and self-review. No calibrated material or
X1C priors, fabrication CAD, physical measurement or independent review.

## Reciprocal interference changes the bearing search

Retain five lug stations at 10-mm spacing, 1.2-mm lug thickness, 2.3-mm release
lift, 2-mm-thick cap, gate at 0 and lower guide at −25. L/W are lug half-length/
half-width; r is stem radius; gate half-aperture a=r+.2; slot/pocket halfwidth
s=W+.2. The constrained search uses W≤r, keeping the seated lands rectangular.

E-168 checks a rotating cap against an unchanged stem. The reverse matters too:
the **upper active lug at z=42.3…43.5 overlaps an unchanged highest cap at
z=42…44**. Other height pairs repeat this relationship. The maximum lug projection
is sqrt(L²+W²), attained between the endpoints of the turn. A 4.8×2.96 lug
(L=2.4,W=1.48) hits even an ideally aligned 4.6 cap: .039645-mm nominal intrusion.
Generated polygon sections find 4/14/55 collisions at 16/64/256 turn intervals.
The single exact maximum-projection angle independently confirms the collision.

Use E-168's explicit in-plane edge/registration bound e=.05 and residual guide
half-play c=.025, not a measured process distribution. An unchanged stem can
lean toward its neighbor with slope 2c/25. The highest cap center is at z=43;
its whole tilted prism projects no farther than its half-width plus
`Dcap=c(1+2*44/25)=.113 mm`. Thus the sufficient directional separation budget is

`sqrt((L+e)²+(W+e)²) + d/2 + 2e + Dcap < 5.08`.

Common rigid displacement cancels; common size bias, differential alignment and
opposite guide contacts need not. No independent-cell sampling or yield is used.
An initially plausible L=2.25,W=1.3 passes if neighbor tilt is omitted, but the
**actual horizontal section of the tilted cap at z=42.9** intersects with
.097732-mm intrusion. This control prevents a centered-neighbor false pass.
Nominal axial dimensions, ideal active-head alignment beyond the stated e,
and tilt in the neighbor direction are explicit limits; arbitrary yaw, compound
warp, loaded curvature and whole-machine manufactured reach are not certified.

The retained L=2.15,W=1.2 witness has **.036684-mm envelope margin** (.038879
at the exact tilted section). Nominal own-gate/lower-guide sweeps cover all twenty
unequal transitions: 8,500/32,500 lug poses at 16/64 intervals, zero intersections.
All 128 engaged/transit cases from 64 coherent in-plane corners also clear.
Continuous phase separation from E-168 still applies: turn above the pocket,
translate aligned in the widened slot, then seat; lower guide remains between
lug levels. Circle-envelope checks cover lug/stem and diagonal active-lug
separation; separate aligned checks cover cap/lug travel and unchanged lug pairs,
including directional guide drift. Adjacent simultaneous cap turns remain
prohibited; checkerboard rotation is only a geometric scheduling possibility.

## Finite bearing and conditional load result

Clip the actual generated gate boxes against the seated lug. Sixty-four shape/
placement corners give 1.702…2.850 mm². In the centered small-lug/large-aperture
corner the two patches are x=[−1.15,1.15], y=[−2.1,−1.73] and [1.73,2.1].
The area and second area moment from those rectangles independently reproduce
the contact formulas. Moving the lug in y shortens one land and lengthens the
other; it does not reduce both simultaneously. Minimum individual land is .32 mm.

For downward F at transverse eccentricity q and zero longitudinal eccentricity,
first omit all guide moments. Nonnegative vertical contact requires |q|≤w,
w=1.15. Equality is a marginal edge reaction with no finite pressure distribution.
A flat, rigid lug on **equal local normal stiffness** gives full contact for
q≤w/3, with `pmax=F/A*(1+3q/w)`. For w/3<q<w the compressed interval is
[t,w], t=3q−2w, and `pmax=F/[3*land*(w−q)]`, land=.37.
This is an alternative ideal contact law, not a prediction of PLA pressure.

| q mm, F=10 N | Compressed area fraction | Calculated peak MPa |
|---:|---:|---:|
| 0 | 1 | 5.875 |
| .3 | 1 | 10.474 |
| .6 | .7174 | 16.380 |
| 1.0 | .1957 | 60.060 |

The singular rise near the edge flags the model's failure to supply benign
bearing; the very large mathematical stresses are not physically achievable
elastic predictions. At a nominal cap-edge load q=2.3, vertical bearing alone
cannot balance the moment. If the ground/lower guide pair alone supplies the
missing couple over the full 25 mm, each lateral reaction must exceed the
**.46-N infimum**; finite pressure requires more. Pocket side contact or a
shorter effective span changes that reaction model and must be constructed.
Guide contact, curved lug root, plate bending, stem deflection, anisotropy,
nonparallel lands, roughness, creep, wear and input-loss arrest remain unsolved.
E-056's pawl likewise has conditional seated equilibrium, not a qualified control.

E-168's infinitely stiff lug / favorable-clamp Rayleigh bound remains valid when
lug in-plane dimensions change but axial intervals do not. For r=1.48 and e=.05,
its load upper bounds are **5.616/11.233/16.849 N** at E=1000/2000/3000 MPa.
Thus 2 GPa merely avoids the 10-N exclusion; 1 GPa still fails it. Neither an
upper bound above the load nor a low mean bearing pressure establishes strength.

## Trade, scope and disposition

The area search spans L=1.8…2.5 and W=.45…r, at .02/.01/.005-mm grids. At
r=1.48,d=4.6,e=.05,c=.025, best areas converge through 1.9400/1.9404/1.9503 mm².
Independent differentiation of the active circular envelope gives a relaxed
continuous supremum **1.95780 mm²**, L=2.26453,W=1.06016. This is an area bound
within the rectangular encoding, not an optimum machine. It has zero extra
clearance; the retained witness sacrifices area for more width and margin.

The source compares d=4.4/4.6/4.8, r=1.44/1.48/1.54 and e=.025/.05/.075.
At e=.075 every fixed-.2-clearance case fails the slot budget .2−3e; widening
the slot changes the topology's bearing trade and is not ruled out by that
encoding failure. Smaller caps improve bearing clearance but lose surface area:
4.4/4.6/4.8 caps cover **75.02/82.00/89.28%** of a level 5.08-mm-pitch plane,
with .68/.48/.28-mm nominal gaps. These are geometric coverage metrics, not
miniature stability tests or invented product thresholds. Exposed round stems
also leave vertical terrain faces open; skirts would invalidate the sweep.

Relative to the same thick stem with narrow lugs, exact rectangle/circle union
volume adds about **120 cm³** across 32,000 lugs. Fixed modular gate/guide plates
can reduce placements. Column-as-lock still removes 6,400 separate pawls and
their return functions, but owes 6,400 angular pockets, 6,400 lower guide sites,
72-mm rotating stems and retained rotary-linear service. This is a component
trade, not evidence of lower total cost or easier repair. The pawl keeps cap
orientation and avoids the rotary service step. E-167's conditional 229–267
head scenarios, <$500 purchased bound, verification/false acceptance, retry,
settling, regional vibration and power-loss arrest remain unresolved.

**Stop** rejecting all thick-stem bayonets from narrow-lug mean pressure, and
stop enlarging lugs without the reciprocal tilted-cap check. **Retain** this
changed bearing as a conditional escape; **defer** further bearing optimization,
rotary-head detail and printing because no comparative full-machine advantage
is established. The next higher-value axis is **sharing powered motion while
preserving independent positive seating** across rotary-column and nonrotating
pawl families: construct the selector/load-transfer path and count channels,
contacts and map completion. Stop a shared-drive embodiment if it merely moves
independent costly clutches or creates unsupported half-selected cells. Reopen
local bearing detail only when that complete service comparison gives a reason
for this family to lead. This is not global search saturation or family rejection.

Self-review: exact peak-angle and ±.001-mm threshold holdouts, tilted-prism
sections, two path resolutions, generated bearing corners, force/moment balance,
pressure scaling, and 32/128/512-strip quadrature (final moment error <.0001 Nmm).
These validate reduced calculations, not hardware; no fabrication or purchase.
