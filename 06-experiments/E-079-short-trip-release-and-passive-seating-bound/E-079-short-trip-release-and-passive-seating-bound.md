---
status: complete
builds-on: [E-078, E-077, E-075]
---

# Short-trip release trades ramp width for a narrow seating window

**A short ramp escapes E-078's full-travel obstruction, but does not provide a
robust completed selector.** With independent ±0.10-mm coordinate and stop
errors, continuous optimization leaves at most **0.0225 mm** between release,
detent crest, endpoint and neighbor constraints. The ±0.20-mm box is impossible
for this section. Two of 54 assumed spring/friction combinations seat slowly
at the optimized middle-box section, with 70.8–75.8 N all-blocked row reaction
at the conservative writer travel. Retain the tight-box section as a comparator;
stop fine-width tuning of this same-layer ramp and do not fabricate it.

Recovered interrupted work at main `d62c48d`, then extended its model to include
endpoint error, continuous synthesis and passive seating rather than inertial
arrival alone. Reproduce:
`python3 tools/curated-experiment-checks/E-079/short_trip.py`.
Standard-library deterministic geometry/energy calculation; no random seed,
contact/field solver, measurements, sourced process prior or printable CAD.
Every dimension, friction and spring parameter is a **labelled bounded
assumption**, not a calibrated X1C tolerance or probability distribution.

## Changed mechanism and finite release

Keep E-077's narrow upper cam-routing boss and lower sliding wing. A vertical
flat-topped writer pin contacts the lowest point on the inclined underside:
its right corner, not its center. For dog displacement q, the underside is
`z=z0+m*q-m*x`. End the wing after the pin has driven the dog beyond a spring
plunger's triangular detent crest. When the wing's left edge passes the pin's
right corner, contact is lost; the descending detent must finish the motion.
The pin no longer powers the whole stroke. This is a changed contact topology
within the mechanical coincidence family, not a new complete architecture.

Let nominal dog travel be d, pin width w, release position r. Bound pin/body
registration, pin width and each wing edge independently by ±e; bound crest
location by ±e and final stop location independently by ±s. Initial dog datum
is included in body registration; s is additional endpoint-to-body error.
The wing's local x interval is `[-r+w/2, w/2+3.5e+0.10]` mm. Its entire
initial pin footprint must fit; thereafter only the contacting corner must
remain on the ramp. The common top skin and y lane prohibit neighbor nesting.
Reserve 0.4 mm per side for guides, as in E-078.

Exact corner enumeration gives release in `[r−3.5e,r+3.5e]`. Three margins are:

- Beyond every crest: `M_c=r−d/2−4.5e`.
- Before every stop: `M_s=d−s−r−3.5e`.
- Arbitrary adjacent-state gap, including guide reserve:
  `M_n=5.08−d−s−r−7.5e−0.10−0.80`.

Endpoint extrema bound the affine wing sweeps. The worst neighbor pair is an
engaged left dog at its farthest stop beside a bypassed right dog. Initial
footprint coverage is separately checked. These are section obstructions, not
3D assembly collision acceptance.

The recovered coarse generator used d={1.2,1.5,1.8}, w={0.6,0.8} and seven
release fractions 0.55–0.85. With an exact endpoint, 23/42, 2/42 and 0/42 sections
pass at e=0.05/0.10/0.20 mm. Its d=1.8, w=0.8, r=1.44, e=0.10 witness leaves
0.01 mm before the stop. Adding s=0.10 makes that margin **−0.09 mm**. A fixed
stroke grid therefore neither proves a robust survivor nor rejects all strokes.

## Continuous synthesis and error sensitivity

Set `C=5.08−0.10−0.80=4.18 mm`. For all d,r,
`(4*M_c+3*M_s+M_n)/8 = C/8−4.5e−s/2`.
A minimum margin cannot exceed that weighted average. Equalizing the three
margins reaches the bound at `d=C/2−2e`,
`r=0.75d+0.5e−0.5s`. This is an exact global upper certificate for these
three affine constraints, not a numerical optimizer success claim. Other
constraints can only reduce feasibility.

At w=0.8 mm and s=e:

| e (mm) | Synthesized d / r (mm) | Maximum common margin (mm) | Initial footprint |
|---|---|---|---|
| 0.05 | 1.990 / 1.4925 | 0.2725 | Pass; minimum land 0.10 mm |
| 0.10 | 1.890 / 1.4175 | 0.0225 | Pass; minimum land 0.10 mm |
| 0.20 | 1.690 / 1.2675 | −0.4775 | Also fails |

For s=e, no positive window exists at **e≥0.1045 mm**. Requiring an additional
0.05-mm reserve for omitted edge rounding/deflection would require e<0.0945 mm
(strict excess over that reserve); at e=0.10 this cannot be repaired by tuning
d or r. The reserve is a sensitivity scenario, not a newly imposed product
requirement. Correlation can change the bound: common pin/body translation
cancels from relative release, whereas independent errors do not. The present
box admits both coherent strip shifts and adverse relative errors without
averaging over 6,400 cells. No manufacturing yield follows.

## Passive seating and shared writer load

Use E-078's frictionless spring plunger on a triangular ridge. Nominal height
a={0.2,0.3,0.4} mm varies by ±e; stiffness k={0.2,0.4,0.8} N/mm and initial
compression c={0.05,0.10,0.15} mm are competing scenarios. Guide friction
mu={0.1,0.3}, additional horizontal drag=0.01 N. These 54 cases per geometry
are not production samples; k,c,mu can shift coherently across a row.

After release, let actual endpoint D, crest x_c, height h and descending slope
`t=h/(D−x_c)`. With zero release velocity and remaining travel L,
`F_end=k*c*(t−mu)−0.01` and
`W=F_end*L + k*t*(t−mu)*L²/2` N mm.
Positive start force and W permit arrival in the friction-only inertial model;
they do **not** prove slow seating or stable readback. Require `F_end>0` to
retain positive forward force throughout descent, including arbitrarily slow
motion. Its continuous-box worst case uses h=a−e, D=d+s and x_c=d/2−e.

Five of 54 scenarios pass that stronger condition at e=s=0.05, two at 0.10;
all have mu=0.1. The middle-box survivors have a=0.4, k=0.8 and c=0.10/0.15.
Their minimum forward endpoint force is only **0.00296/0.00944 N**. Increasing
unmodelled drag by those amounts closes the corresponding seating margin.
This does not establish real friction, stiffness, spring life or creep limits.

For a 45-degree ramp, ramp friction 0.3, separate guide shoes and the same mu,
contact force gain is `G=(1−0.3)/(1+0.3)−mu`. A sufficient bounded peak pin
force is `[k*(c+a+e)*((a+e)/(d/2−e)+mu)+0.01]/G`.
With writer preload 0.01 N and stiffness 0.10 N/mm, conservatively combine this
force with the latest crest and latest release to bound drive travel. The two
middle-box cases give **0.780/0.843 N** peak bounds, **8.746/9.377 mm** driver
travel and **70.764/75.813 N** for 80 blocked springs. These are forces at that
chosen sufficient travel, not minimum possible forces. Free approach through
shutters adds travel. The tighter geometry's five cases need 35.4–60.6 N by the
same calculation. Shortening the ramp has not removed accumulated spring load.

## Decision and remaining mechanism boundary

No section earns full selector acceptance. Passive reset needs a parked cam,
a comb capable of crossing the reverse detent barrier, and positive writer
withdrawal before the comb returns a wing over the pin. Loss of ramp contact
allows the push spring to lift the pin further; a captive travel stop and
E-077's withdrawal interlock remain necessary. Rebound, finite crest rounding,
plunger packing, spring pockets, strength, wear and cam endpoint readback are
unproved. The upper boss can use E-077's section, but its y/z swept geometry
has not been combined with this lower mechanism. The dog stores a command,
not column height or service load.

Keep this result as the mechanical comparator and move the next discrimination
to the seated magnetic route, rather than another width sweep. That route must
supply a finite stop/contact law and an isolation bound beyond E-075's ideal
inelastic seat. Then compare complete gate/retention/return inventories and scan
budgets before campaign closure. A changed ramp route reopens with staggered
lanes, reduced *relative* errors backed by geometry/calibration, or another
positive completion mechanism; nominal dimension tuning cannot escape the
continuous margin certificate. No print request follows from this result.

Self-review: independent midpoint integration at 20/40/80 subdivisions agrees
with exact affine-force work; frictionless work equals spring potential loss.
Checks distinguish inertial arrival from slow seating, reconstruct all interval
corners, exercise the old witness's endpoint failure, and verify the weighted
certificate at 20,172 off-optimum points over 12 error scenarios. Interior
force holdouts verify the analytic worst endpoint force. No external review,
physical qualification, reliability rate, cost quote or <30-s claim is made.
