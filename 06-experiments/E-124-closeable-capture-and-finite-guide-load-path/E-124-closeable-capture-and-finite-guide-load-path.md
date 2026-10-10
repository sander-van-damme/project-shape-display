---
status: complete
builds-on: [E-123, E-115]
---

# Remote guide play defeats the nominal side shoe; balanced capture changes the load path

**Stop treating E-123's face-error pass as a guided-head pass. Retain a bilateral
lower-entry cup as a changed capture interface for powered-joint investigation.**
A finite tilted-body witness intersects the E-123 web and foot by **.439998 mm³**
at e=.05 and guide centre half-play c=.025 mm. A cup can acquire from below and
place opposing upper contacts around a narrower foot without the side shoe's
nominal eccentric load. Neither is a completed powered head: cup jaw retention,
actuators, ground-lock access, proof and fault recovery remain unimplemented.
No machine, timing/cost survivor, fabrication or purchase is admitted.

Input main `b8843b9`. Reproduce:

```
python3 tools/curated-experiment-checks/E-124/capture.py
```

Evidence: deterministic generated box solids, continuous axis sweeps, finite
rotated-polygon intersection, analytical guide/elastic enclosures and numerical
integration self-checks. No random distributions, process measurements, sourced
material allowables, calibrated friction, CAD release or physical qualification.
Output JSON is reproducible and not retained. This resolves a distinct
capture/guidance question within the direct-head campaign, not its power/lock
completion gate. Existing pad-lowering, compact e=.10 packing and closed-guide
rack-crossing failures remain executable checks from E-123.

## Finite guides and correlated pose errors

Column guide stations are centred at z=45 and 75 mm; travelling-head shaft guide
stations at z=−10 and −40 mm. Each modelled sleeve has four .8-mm walls and a
2-mm axial length, around the rectangular shaft plus clearance. The code checks
upper-sleeve packaging against the nominal column and full capture sweep. The
lower shaft's actual powered construction remains absent; its stations define a
beam/pose scenario, not a packaged actuator. Both pairs span S=30 mm.

`c` is remaining centre half-play **after** form, alignment, projected shaft
width and finite sleeve length have been allowed. It is not a specified hole
dimension or an assertion that X1C delivers that fit. For a foot at h=0…40,
column overhang Lc=45−h and head overhang Lh=h+10 give extremal centre excursions

`dc=c(1+2Lc/S), dh=c(1+2Lh/S)`.

The two overhangs belong to the same height: their sum is 55 mm, so
`dc+dh=5.666667c` throughout travel. Taking both longest overhangs simultaneously
would exaggerate the result. Opposite contacts at each guide's endpoints realise
these pose bounds. Nominal stations plus an unspecified zero-clearance shaft do
not establish a guide. Sleeve overlap, contact force and bind/wear remain gates.

An additional rotation enclosure uses `theta=atan(2c/S)` and local vertex radii
3 mm for the foot and 6 mm for the head. E-123's independent translation/face
errors still contribute 4e. The capture clearance screen therefore uses

`d=4e+5.666667c+18 sin(theta/2)`.

The head-to-head check separately doubles the worst head excursion and rotation;
neighbouring outputs need not share a height. Common rigid translation cancels;
coherent adverse guide tilt, batch size bias and spatial warp need not cancel.
These are bounded epistemic scenarios, not yield estimates. Residual warp is
charged separately below; no independent-cell probability is used.

For the original C shoe, set c=.025, e=.05, h=0. The head centre extrapolates
+.041667 mm and the column −.100000 mm. Give both their compatible +.001666665-rad
tilt and E-123's adverse opposing faces. Clipping actual rotated web and foot
polygons gives **.439998 mm³** intersection, versus .440000 mm³ in the parallel-axis
limit. This is an actual failure corner, not rejection merely because an
uncertainty enclosure overlaps. The c scenario is not a measured process floor;
it invalidates an unconditional pass, not every precision guide.

## Changed capture: bilateral cup from below

The geometric witness replaces the 4×2.8-mm foot with **2×2.8×1.2 mm**, on a
1.2×1.2-mm stem. Surface pitch remains 5.08 mm; the top cap is unchanged in the
product interface and is not generated here. A centred lower pad sits on a
pedestal/base. Two lateral webs carry upper contact pads; each pad can move over
the foot shoulder and then take up vertical play. Finite channel walls locate
the lower sliding parts. **The upper pads' positive retention, all drives and
channel fit/anti-lift retention are not implemented.** Prescribed pad coordinates
are only a contact-interface screen and cannot carry a claimed tensile load.

Open envelope is **4.4×2.8 mm**. Each horizontal closing stroke is .4 mm; vertical
upper-pad take-up is .4 mm nominal. Approach with the jaws open from below the
old foot; reach lower-pad contact; close laterally above the foot; then take up
the upper clearance. The two upper pads and lower pad touch the nominal foot
with zero slot play. Release reverses these steps only after an independently
proved ground support, which is an obligation, not implemented logic. Positive
powered take-up would need sufficient travel for actual face errors, preload,
nonparallel faces and wear, plus a retained stop/power-loss path.

Unlike a side shoe, this route approaches with its upper fingers outside the foot
and brings contacts over **both** shoulders. A symmetric realised contact force
could centre the load on the stem. Symmetric CAD alone does not balance forces:
unequal seating, warp, sliding friction and preload can restore eccentricity.
The unresolved coupled contact model must determine the actual load distribution.

Continuous swept boxes check the open approach, lateral closing and vertical
take-up against the own column. Every neighbour's height is independently swept
through 0…40; separated head hulls bound adjacent heads at different heights.
The closed interface is checked at all 81 indexed old/target pairs in the
holdout; common translation extends the same geometry continuously. This does
**not** prove an unlocked supported transaction, a loaded motion or fault safety.

Generate foot width {2,2.1,2.4,2.8}, stem 1.2, overlap/back/entry each
{.2,.225,.3,.4}, and web {.6,.8}: **512 sections per scenario**, one new capture
topology. The .025-mm reserve is inherited as a screen, not a qualified fit.

| e mm | c mm | Cup contact sections passing /512 |
|---:|---:|---:|
| .025 | 0 | 78 |
| .025 | .005 | 60 |
| .025 | .025 or .05 | 0 |
| .05 | 0 | 3 |
| .05 | .005, .025 or .05 | 0 |
| .10 | 0, .005, .025 or .05 | 0 |

Zero-play rows are mathematical limits. Counts are contact-section screens plus nominal finite sweeps, not complete
uncertain-geometry or drive/joint-retention admission. Grid/enclosure failures do not prove that every bilateral cup fails.
The witness at e=.025,c=.005 has .068667-mm entry/web/stem/overlap margins,
.532667 mm between head hulls and .297 mm vertical entry clearance. Only
**.043667 mm** remains beyond the chosen reserve for additional relative warp,
load-related pose mismatch and model discrepancy. Tightening a nominal hole does
not establish that allowance in a full bank.

For comparison, allocating a **2-mm side-spine housing** for a hypothetical
1.2-mm screw plus surrounding structure replaces E-123's .6-mm web. Applying
its eliminated section inequalities to the expanded pose enclosure requires
4.450667-mm pitch at e=.025,c=.005, but 5.250667 mm at e=.05,c=.005. This is a
conservative housing screen, **not a generated screw/nut, a proof of universal
impossibility, or a complete retained clamp**. Power cannot be assigned free
space inside the original thin web.

## Eccentric load, warp and the next fidelity gate

For a beam with two lateral simple supports S apart, an overhang L and an end
moment M, integrating Euler–Bernoulli curvature gives

`tip displacement=M(L²/2+SL/3)/(EI)`,
`tip rotation=M(L+S/3)/(EI)`.

Units are N, mm and N/mm². The code separately integrates curvature through both
supported span and overhang at 16/64/256 steps, enforcing zero displacement at
both bearings. Zero moment and inverse-modulus limits also agree. This is a
linear elastic scenario; values beyond .5-mm displacement are flagged outside
the chosen small-deflection screen and are not quantitative hardware predictions.
Buckling, shear, creep, frictional support, anisotropy and joint compliance are
not resolved by this check.

Side scenario: column I=.2304 mm⁴, screw-housing spine I=2.564879 mm⁴ after
subtracting a 1.2-mm round bore, force eccentricities .95/1.35 mm at column/head.
Balanced scenario: column I=.1728 mm⁴, a 2×2-mm lower shaft I=1.333333 mm⁴ and
**assumed residual eccentricities .05 mm** at each. Moduli {500,2000,100000}
N/mm² and forces {.06,.1,1,10} N are deliberately labelled alternatives, not
PLA/metal specifications or allowable stresses. End heights bound the convex
sum of the two responses, without mixing incompatible head/column heights.

At E=2000 and F=.06 N, summed magnitudes of **free** tip response are .183277 mm
for the side route versus .012864 mm for the balanced residual scenario. At
.1 N they are .305461/.021440 mm. A closed jaw cannot simply separate by these
amounts: it reacts the incompatibility through lateral force/moment and guide
contacts. Therefore these numbers prioritize a **coupled beam/contact solve**;
they are neither actual closed-head displacement nor binding/strength acceptance.

E-123's 5-g mass and .060-N drag require .109050 N upward at zero acceleration,
or .134050 N at 5 m/s². For the balanced residual scenario, the free-response
screen consumes .023380/.028740 mm, leaving .020286/.014926 mm of the geometric
reserve budget. Adding an explicit .025-mm relative warp bound exceeds that
budget by .004714/.010074 mm. This is a failed reduced-model budget, not a proved
physical jam. Zero warp fits this budget but earns no powered-head pass.

**Continue the existing task:** implement retained upper jaws and actual power
transmission with their finite routing; solve coupled contact/guide reactions
including preload asymmetry before accepting controlled lowering. Include a
positive ground-bolt set/reset path and physical output proof, common readback
errors, safe stop and recovery through the entire transaction. Do not advance
system timing/affordability from these partial interface counts. Stop the present
compact side housing if its loaded/retained implementation cannot fit; allow
changed internal pitch, relocated guides or a genuinely changed capture route.
No print is justified before those computational completeness gates.

Self-review only: exact sweep and polygon limiting cases, correlated guide
corners through all 41 integer heights, continuous-height envelope, all admitted
nominal interface sweeps, refined acquisition holdouts and independent curvature
integration. No independent review or physical evidence is claimed.
