---
status: complete
builds-on: [E-167, E-124]
---

# Lower bayonet guidance trades cap clearance against stem and bearing capacity

**A lower slotted guide is kinematically possible; it does not establish an
adequate exposed stem.** At 4.8-mm cap width, in-plane edge bound e=.05 mm,
residual guide half-play c=.025 mm and E=2000 MPa, the coupled clearance / elastic
screen gives **Pcr ≤9.4511 N**, below the assumed 10-N service screen. Even
infinitely stiff lug segments and an unrealistically favorable upper clamp do
not escape this case. This is a conditional model exclusion, not a measured PLA
capacity or rejection of quarter-turn locks. Reducing cap width to 4.6 mm avoids
that exclusion but leaves bearing, powered capture and input-loss arrest open.

Input main `10acee3`; LAB-274. Reproduce with standard Python:
`python3 tools/curated-experiment-checks/E-168/guidance.py`.
Source imports retained E-167 polygon primitives. Output JSON is disposable.
Evidence: generated rigid geometry, deterministic pose bounds, elastic energy
upper bounds and self-review. No fabrication CAD, calibrated process priors,
loaded contact solution, measured reliability or independent review. No print
or purchase; this discriminator precedes detailed rotary-head construction.

## Finite guidance and access

Retain E-167's five 10-mm-spaced, 4×.9×1.2-mm lugs, 2.3-mm lift and square
2-mm-thick cap. Test a 1.4-radius circular stem and enlarge the grounded gate's
central square half-aperture to 1.6. A second guide centered **z=−25**, thickness
1.2, has that aperture plus the full-width |y|<.65 slot. Six finite blocks form
it. Extend the stem to z=−30…42 before the −40…0 state shift. The original ground
gate supplies the upper lateral station; guidance is not assigned to empty space.

Twenty unequal old/new transitions at 16/64/256 steps per phase check
**8,500/32,500/128,500 lug poses**, without collision against the modified gate
and lower guide. Cap prisms also clear those solids; the circular shaft fits
inside the central square throughout. A continuous argument closes the sample
gaps: at locked-angle lift/reseat the lugs occupy multiples of 10 plus [0,3.5],
clear of the lower guide [−25.6,−24.4]; at the turning phases they remain clear
in z; during translation the lugs are aligned with the slot. Stem length retains
both lateral stations at every state and during release lift.

Controls: moving the same lower guide to z=−20 intersects a locked lug during
lift. A stem-fitting fixed guide at z=12 intersects the cap during a low-to-high
translation. More generally, the cap sweeps the central axis through the height
range: a closed, small-bore fixed upper sleeve in that range is not a free brace.
This does not exclude retracting, telescoping or peripheral guides, which require
new geometry and mechanisms. A cap-sized aperture is not a close stem guide.

The extended stem is **72 mm long**, and a proposed bottom foot's upper face
would span z=−70…−27.7 including release lift. Thus below-entry access remains
geometrically possible beneath the −25.6 guide bottom; no foot, retained jaw,
rotary drive, axial drive or power-loss arrest has been constructed. The entire
machine would extend below this foot for head travel/transport. Longer tails
add print volume and guide/assembly work; no compactness advantage is established.

## Residual play and actual neighboring-cap witness

Let c be effective center half-play at the ground gate z=0 and lower guide z=−25
**after** local form, alignment and finite sleeve-length allowances. It is a
bounded scenario, not a specified hole clearance or X1C accuracy. Opposite station
contacts allow a straight stem axis with slope 2c/25. At z=35.3 its transverse
excursion is `D=c(1+2*35.3/25)=3.824c`.

This height is inside the selected level-1 cap during interlevel rotation
(cap z=34.3…36.3). A highest-position unchanged neighbor has stem through that
height. Give the active head perfect centering; its omitted play only worsens
the allowance. With cap half-edge error +e, shaft radius error +e and relative
registration error e, a necessary robust clearance bound is

`r_nom ≤5.08−sqrt(2)(d/2+e)−2e−D`.

Common rigid translation cancels. Common size bias and differential guide tilt
need not cancel; a whole bank can realize an adverse pattern. No independent-cell
sampling, yield estimate or assumed probability enters. The e scenarios apply
to in-plane geometry; nominal axial intervals are retained as one allowed case.
Yaw, cap flexure, loaded stem curvature, warp and active-head error are omitted,
so this is an optimistic allocation, not a complete manufactured fit envelope.

At e=.05,c=.025,d=4.8, r_nom must not exceed **1.41958 mm**. Actual horizontal
sections of a cylinder tilted by .002 rad against the 45-degree cap prism give
no intersection at r=1.4, but an intersection at r=1.45, with **.03043-mm horizontal
penetration**. Inscribed ellipse polygons at 32/128/512 vertices agree. The exact
ellipse accounts for the tilted circular cylinder; strict intersection at the
interior cap height persists over a nonzero vertical interval. This is a finite
kinematic witness under the residual pose allowance, not a solved loaded contact
equilibrium or a prediction that every rested column takes that pose.

## Upper bound that includes lug stiffening

A plain circular-shaft Euler calculation is not an upper bound on a lugged
shaft: lugs can stiffen it. Instead, grant perfect fixation at z=2 and apply the
compressive force at cap underside z=42, leaving only 40 mm. These are more
favorable than the actual gate at 0 and load on the cap top. Grant infinite
bending stiffness to the four lug intervals [10j,10j+1.2], j=1…4.

For the slope trial function `theta=sin(pi*s/(2*Lf))`, s accumulates only the
flexible length and Lf=35.2 mm. Hold theta constant through each lug. It satisfies
the clamped slope condition; lug curvature and bending energy are zero. The
Rayleigh quotient therefore bounds the first elastic buckling load from above:

`Pcr ≤ EI * integral(theta'^2 dz)/integral(theta^2 dz)`.

Piecewise exact integrals give **q=.001710079588 mm⁻²**, so
`Pcr ≤ E*pi*(r_nom−e)^4*q/4`. This uses a different allowed manufacturing corner
with a smaller shaft radius; a design robust to the declared population must
satisfy both that case and the larger-radius clearance case. It does not assign
opposite radius errors to one physical part. Uniform radius between lugs,
linear isotropic elastic response and concentric static compression are explicit
model conditions. No strength, creep, wear or imperfection safety margin is taken.

The quotient is only 1.10891 times the uniform-shaft, fixed-free Euler value.
Without lug intervals the integration exactly recovers pi²/(4L²), consistent
with [University of Maryland Statics notes, §7.3.2, Eq. 7.32](https://huginn.eng.umd.edu/ebooks/staticsF2016/resources/_pdfs_/StaticsF16S17__.pdf)
(accessed 2026-10-11). This source supports the ideal boundary condition, not a
PLA material prior. Independent midpoint integrations at 16/64/256 points per
segment converge to the piecewise integral (relative discrepancy <1e−8 at 256).

For d=4.8 and e=.05, the coupled **upper bounds**, N, are:

| Modulus scenario MPa | c=0 | c=.025 | c=.05 |
|---:|---:|---:|---:|
| 1000 | 6.190 | 4.726 | 3.538 |
| 2000 | 12.379 | 9.451 | 7.076 |
| 3000 | 18.569 | 14.177 | 10.614 |

The code also checks e=0/.025/.10. Bounds below 10 reject the declared 10-N
screen; bounds above 10 merely avoid this necessary-condition failure. E and c
are competing assumptions, not calibrated distributions or material allowables.
The 10 N is inherited research loading, not an additional stage-02 requirement.

## Changed cap trade and portfolio disposition

At E=2000,e=.05,c=.025, avoiding the 10-N exclusion requires nominal radius
at least **1.43904** and cap width at most **4.77247 mm**. A 4.6 cap gives an upper
bound of 14.0021 N and a .48-mm nominal surface gap instead of .28 mm. It is not
rejected by an invented gap requirement, nor accepted without assessing terrain
coverage and miniature support. At E=1000 the corresponding cap limit is 4.40079.

The enlarged central aperture consumes lug bearing. For original half-length 2,
nominal aperture `r+.2`, and centered adverse size errors, each wing's remaining
land is `2−r−.2−2e`; available area is `4(.45−e)*land`. Translation shortens one
wing and lengthens the other, so it must not be charged twice in total area.
At the minimum E=2000 radius the adverse centered area is **.417530 mm²**:
mean pressure **at least 23.9504 MPa** at 10 N for any larger radius. No allowable
is asserted; peak/root stress and creep remain unresolved. Minimum individual
wing land with additional e offset is .210956 mm. At E=1000 the necessary radius
1.70186 eliminates both wings in the adverse centered size case. Longer/wider
lugs could change that failure; they need new gate/neighbor sweeps.

**Stop** claiming a robust 4.8-cap, 2-GPa, e=.05/c=.025 bayonet embodiment at
10 N, and defer detailed powered-head construction for it. **Retain** smaller
caps, changed lug geometry or higher effective stiffness as conditional reopening
routes. A higher upper bound alone cannot justify their head development.
The pawl control keeps square-top orientation and avoids this turning-cap radius
constraint, while retaining its separate support, guidance and arrest problems.

Full-board accounting now includes 6,400 longer rotating columns, 32,000 lugs,
6,400 gate/pocket sites **plus 6,400 lower guide sites**; modular guide plates can
reduce placements but not contacts. E-167's 229–267-head timing scenarios and
<$500 purchased-cost obligation remain unresolved. No new throughput advantage,
BOM, reader false-acceptance rate or fault-arrest capability is claimed. Unguided
or false-seated columns can still drop; unchanged-region vibration is unbounded.

Next highest-value discriminator: compare the smaller-cap / wider-lug escape
against a nonrotating pawl using **finite loaded bearing geometry and cap utility**
before committing to rotary head/arrest detail. Require a meaningful inventory or
service advantage; otherwise switch the architecture/function axis. Printing
fit coupons cannot settle this load-path trade first. No global search saturation
claim: this work tests a new guide topology and coupled envelope within E-167,
not independent discovery of another mechanism family.
