---
status: complete
builds-on: [E-199, E-198, E-116]
---

# A sliding tip removes the leaf couple, but does not remove guide wedging

**Retain force-contact return as a changed coupling; stop the specific coplanar
button package at the ±.025-mm relative-error bound.** A grounded cantilever
with a round tip pushes a separate slider without clamping its end rotation.
Nominal geometry clears. Guide sticking needs much higher friction than E-199,
but remains admissible, and the button collides with the neighboring rack under
a small explicitly bounded error scenario. This is neither a machine selection
nor a rejection of cantilevers, sliders or sliding contacts generally.

Input main `fd45a5c`; LAB-327. Reproduce with
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-200/sliding_tip.py`
(Python + NumPy). Evidence: finite section/envelope generation, analytical beam
calculation, unilateral spring/contact-cone feasibility and self-review. No
measurements, sourced process distributions, nonlinear coupled beam/contact
simulation, dynamic return, manufacturing qualification or independent review.
JSON is disposable. No fabrication or purchases proposed.

## Changed function and comparison

The new-here combination disconnects **spring rotation from grounded lock
orientation** through unilateral force contact, rather than cancelling two
opposed leaf moments. E-198/199 attach leaf ends rigidly; E-116 supplies positive
cam return but retains its captured-transfer failures. Repository searches for
free-tip/sliding-contact and captured/carrier/bilateral mechanisms, plus those
source results, found no existing construction of this coupling to E-198's
backed island. This is one functional recombination within shared manufacture,
not an independent literature search or landscape-saturation claim.

| Combination | Causal chain and changed obligation |
|---|---|
| Sliding-tip sheet + separate backed slider | Independent head captures/unloads rack, retracts slider against leaf, moves rack, releases slider; tip pushes slider to an explicit ground stop; head seats and proves support before leaving. Eliminates the clamped leaf end couple; adds 6,400 sliding tip contacts and separate slider placement. |
| E-199 integral folded sheet | Same intended update sequence; retains the ~21-mm moment/force lever and short-guide sticking near μ=.009. One integral island/return sheet placement, two moving legs/site. |
| Carrier-assembled slider + bilateral powered reset | Head positively retracts/reinserts slider and proves engagement; no passive return claim. Actual push/pull acquisition, departure, retained state, sensing, jam recovery and moving-power-loss arrest remain unconstructed. E-116's old captured-slot failure is not bypassed by naming a fork. |

All retain five heights 0/10/20/30/40 mm and 5.08-mm pitch. Unchanged cells remain
seated in the intended local sequence. Failed support proof must retain the
head, allow only supported recovery and inhibit departure. No readback accuracy,
channel implementation, adjacent-displacement or outage-arrest credit is earned.

## Finite nominal construction

Use E-198's island x=[−1.75+q,.9+q], z=[−2,0], y=±.2; q∈[−.75,0], its
rack and three backed guide faces. A separate .2-mm-wide, .4-mm-thick leaf rises
41 mm from (x,z)=(−1.7,−42.7). Its natural round-tip center is (−1.7,−1.7),
with radius .15 mm in the x/z plane. Assembly deflects it left by d=.2−q;
the button's rightmost point contacts the island's rear face. Its free vertical
shortening slides along that face. A short root rib x=[−1.8,−1.6], z=[−43,−42.7]
connects it to E-198's common spine and grounded frame; the root clamp is ideal.
The circle rotates with the beam without changing its contact envelope.

A slider lug x=[−1.2+q,−.9+q], z=[−2.6,−2], y=±.2 meets a fixed stop at
x=−.9. That stop spans x=[−.9,−.5], z=[−2.6,−2.1], y=±1.4 and joins the
side posts. It bounds seated travel instead of prescribing a free slider's
endpoint. The rightmost button force maintains contact with the stop at q=0;
the return/jamming calculations concern q→0 from the open interval and omit
this intentional stop reaction.

Free-tip small-slope beam shape, u∈[0,1]:
`x=xroot−d(1.5u²−.5u³)`;
`z=zroot+Lu−d²(3u³−2.25u⁴+.45u⁵)/(2L)`.
The source generates rotated stem cross sections, conservative segment boxes,
a square envelope around the circular button, the lug, root and ground solids.
At 4/16/64 stroke subdivisions it checks 125/425/1,625 release/height poses,
including all twenty unequal rack transitions after .2-mm unloading. The
neighbor rack's entire swept envelope is checked, including arbitrary heights.
Root/spine contacts and the lug/stop contact are intended bonds/touches.

The minimum button-to-neighbor gap is **.08 mm** at full withdrawal. The stem
setback is functional: removing it (button radius=.1, equal to stem half-width)
produces a positive-volume stem/island collision, verified by clipping the actual rotated
stem polygon against the island rather than intersecting bounding boxes. A contact point imposed at a
beam endpoint with no finite nose would hide that collision. Nominal stem
clearance also has a continuous bound: `r−w/2−max|slope|*.32 > .038 mm` in the
island's occupied z band; max slope=.03476. Segment discretization is therefore
not the only evidence of this separation. Root connectivity and rack/island
sweeps are geometry checks, not loaded support-transfer or fit qualification.

## Force, contact and the decisive limiting case

E=200,000 MPa is a metal-like assumption. With I=tw³/12, the frictionless
cantilever has `H=3EId/L³`, tip shortening `.6d²/L`, zero end bending moment,
and root bending strain `3wd/(2L²)` (maximum .01696%). These are elastic demands,
not material allowables. The circle's horizontal normal transmits no end couple
to the slider. Tip tangential traction V transmits vertical force with
`|V/H|≤μtip`; it can apply a small couple up to `r μtip H` to the leaf itself.
That coupled beam-column correction is not included in the nominal shape.
Its geometric-stiffness scale is `|V|L²/EI≤3 μtip d/L` (≤.03476 for μtip=.5),
not a certified displacement-error bound. No manufactured geometry pass is
claimed from the separate wrench screen.

Guide model uses E-199's six unilateral endpoint springs. For displacement
(z,θ), each normal is `Ni=max(−ki ni(z+xiθ),0)`, with no imposed interference
preload. Contacts lie at z=0 or 2 relative to the lower guide. Enumerate all
64 active sets. Unlike E-199's common traction-ratio witness, allow independent
static Coulomb tractions: their total upper force is φH and lower force
(−1−φ)H. Let v=V/H and g=W/H; external moment/H is
`xcontact*v − c − xmass*g`, where c is contact height above the lower guide.
Solve vertical and moment balance for affine normals in (v,φ), then intersect
contact-activity and friction half-planes, including `|v|≤μtip`. Polygon vertices
provide feasible witnesses; reported thresholds are infima found by bisection.
This preserves normal compatibility while allowing different upper/lower
tractions, including singular cases missed by a prescribed common ratio.

**Even a horizontal force through the lower guide with no weight or tip
traction can stick at μguide=.2.** An independent witness has lower contact
x=−.25, upper x=.15, both N=2.5H; each friction is −.5H. Vertical forces cancel;
normal moment −.4N and upper-friction moment +H cancel. The normal springs admit
this contact pair without an imposed interference preload. This is a static
wedged equilibrium, not a prediction that the slider reaches it dynamically.
The zero-force-normal intuition is insufficient once friction itself supplies
torque. E-199's narrower no-witness control at μ=.05 remains consistent.

For μtip=.3, the following infimum μguide values permit static sticking:

| q mm | H N | c mm | W/H | No weight | With weight |
|---:|---:|---:|---:|---:|---:|
| 0 | .00046430 | .299415 | .37051 | .17259 | .16002 |
| −.30 | .00116075 | .296341 | .14820 | .15925 | .14927 |
| −.75 | .00220542 | .286793 | .07800 | .14230 | .13453 |

Weight=.00017203 N includes the island and lug, using the explicit assumed
density .008 g/mm³ and g0=9.81 m/s². It is not a sourced material prior. This
raises the friction threshold roughly an order of magnitude relative to E-199,
but it does not prove return at an unknown real friction. Tip adhesion, burrs,
interference, out-of-plane forces and finite guide play are absent.

Self-review reconstructs all three balances and nonnegative reactions for each
witness, independently checks force against the derivative of beam energy,
checks shortening quadrature at 32/128/512 intervals, and recovers E-199's
independent equal-leg threshold `.4/43`. The new pure-horizontal witness checks
the formerly singular case. No simulated yield or dynamic completion time is
inferred. Shared guide stiffness ratios .1/1/10 and bounded tip/weight/contact
height cases are retained in the executable output as sensitivity, not priors.

## Manufacturing, scale and disposition

The neighbor gap is `.38−2r`. With relative rear-face registration, button radius
and adjacent rack edge each uncertain by ±e, the adverse gap is `.08−4e`:
.08/.04/−.02/−.12 mm for e=0/.01/.025/.05. At e=.025 an actual circular button
penetrates the neighbor web by .02 mm at its leftmost point; this is not merely
an overlap of conservative boxes. A common absolute translation cancels; a
common radius or relative registration bias can affect an entire sheet/bank.
These are explicit bounds, not a claim that the X1C or a cutting process achieves
them. Changing button radius/leaf width or routing in another y plane is a
changed package; this failure does not reject force-contact return generally.

The nominal guide still has zero play. Gap/interference, sheet flatness, kerf,
burrs, root clamp compliance, friction, wear, print shrinkage/warp/first layer,
anisotropy, creep and fatigue remain unqualified. The .2-mm metal-like leaf is
a cut-sheet hypothesis, not a printable or procured part. The static sensitivity
screen varies c=.15/.45 mm, μtip=0/.3/.5, W/H=0/.5/2/10, q=0/−.75; these 48
cases are competing bounded assumptions, not independent cells or probabilities.
Thirteen of these 48 cases admit sticking at μguide=.05, and all 48 at .3;
these counts are not frequencies. At q=0, c=.3 and W/H=.36, the three opposing
contact-stiffness scenarios give the same threshold .16045. It does not apply
geometric manufacturing errors to a coupled contact solve.

A forty-site sheet can still share return placement (160 sheets, about 1.46 m²
allocated stock before nesting/waste), but **160 additional carrier batches of
separate sliders** and carrier removal are now required. There are 6,400 leaves,
6,400 sliding tip contacts, 6,400 positive rack engagements, 19,200 guide faces
and 6,400 additional seated stops. Lug/stop and spring-root features can be
integral; counting them is not counting purchased parts. The leaf count halves
relative to E-199, while placement and wear contacts increase. No net assembly,
print-time, scrap, calibration or service advantage is established. Replacing
a sheet still requires independent support of its forty columns; independent
slider extraction through a removable frame is not constructed.

The full bought boundary remains `Cshared+Hheads*chead+6400*ccell<500 dollars`;
with a hypothetical $250 reserve the resident allowance alone is <$0.03906/site.
These are ceilings, not quotations. The inherited accounting
`6+ceil(6400/Hheads)*s` is 26 s at 160 heads and s=.5 s, but exactly 30 s at
s=.6 s fails the strict target. Neither allowance is earned here: capture,
unload, commanded opening, 40-mm travel, return, seating, output/support readback,
transport, preparation, settling and bounded recovery all remain charged. A
small spring force does not establish a return time. Full support pressure,
frame coupling and service loads retain E-198's unresolved demands.

**Decision:** preserve the change from clamped rotation to force contact and
the full-cone guide-wedging counterexample; stop tuning this narrow coplanar
nose. No friction coupon is justified before a geometry tolerant of the chosen
error bounds exists. The next useful branch is an orthogonal contact lane with
actual return-force eccentricity and accessible slider replacement, compared
against a carrier-assembled rigid slider with powered reset. Reopen only if that
construction earns clearance or assembly/service benefit without hiding guide
roll, new transmission contacts or head acquisition. Do not simply increase
spring stiffness: that does not remove friction-induced wedging.
