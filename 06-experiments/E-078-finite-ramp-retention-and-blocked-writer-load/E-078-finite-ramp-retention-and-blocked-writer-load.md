---
status: complete
builds-on: [E-077, E-076]
---

# Full-travel sliding ramps consume the dog packing reserve

**Reject the full-travel sliding-ramp embodiment at the middle/wide error
boxes; retain only a tight-box section, not a complete selector.** The E-077
0.8-mm dog/1.5-mm stroke witness does not establish room for its command ramp.
A ramp maintaining pin-footprint coverage throughout that stroke needs a much
wider lower wing. A spring writer also amplifies all-blocked reaction, rather
than maintaining E-076's illustrative constant preload.

Input main `895476d`. Reproduce with
`python3 tools/curated-experiment-checks/E-078/ramp.py`.
Standard-library deterministic corner enumeration and quasistatic force bounds;
no seed, measurements, sourced process priors, contact solver or printable CAD.
All dimensions, friction and spring parameters below are **labelled epistemic
scenarios**, not X1C distributions or a manufacturing-yield estimate.

## Finite ramp and arbitrary neighboring states

The pin rises along z through the two shutters. A dog moves x by d, carrying a
lower ramp wing with underside `z=z0+m*q-m*x`, where q is dog displacement and
m is rise/run. Its upper cam-contact boss can remain E-077's narrow section;
the lower wing must sweep without colliding with neighboring wings. A pin's
upper corner contacts the slope; pin width is not a distributed contact area.
The wing is required to cover the **entire pin footprint**, with 0.10-mm end
land, for every q from 0 to d. This is a specific full-travel embodiment.

Bound pin and dog x registration independently by ±e, pin width by ±e and
each ramp end by ±e. Reserve 0.4 mm per side for guides. For pin width w,
the designed ramp local x interval is
`[-d-w/2-3.5e-0.1, w/2+3.5e+0.1]`.
Its length is `d+w+7e+0.2`. The extra e per edge permits fabrication error
without losing the end land. These are worst-corner robust bounds, including
coherent shifts; errors are not averaged over cells.

The closest arbitrary-map neighbor is a fully engaged left dog beside a
bypassed right dog. Independent ramp/body errors make its guide-reserved gap
`5.08-2d-w-11e-0.2-0.8`. Enumerating actual interval positions independently
confirms both this gap and the 0.10-mm minimum footprint land. Because all
positions vary affinely, endpoint extrema bound every intermediate q; a finer
motion grid cannot uncover an interior x extremum. This is an exact projected
sweep obstruction, not a 3D collision pass.

Generate d={1.2,1.5,1.8} and w={0.6,0.8,1.0} mm:

| Error bound e | Passing sections / 9 | Survivors |
|---|---:|---|
| 0.05 mm | 3 | d=1.2; gaps 0.53/0.33/0.13 mm for increasing w |
| 0.10 mm | 0 | Best gap −0.02 mm |
| 0.20 mm | 0 | Best gap −1.12 mm |

The earlier d=1.5, w=0.8, e=0.10 witness has **−0.82 mm** gap here.
At d=1.2, w=0.8, e=0.05 the ramp is 2.55 mm long with 0.33-mm reserve.
Its upper 0.8-mm boss and 0.8-mm cam retain E-077 engagement/bypass margins
0.65/0.25 mm. Separate layers are necessary; this does not prove room for
vertical guides, retention, parked cam, keys or spring pockets.

This rejection depends on full-footprint, full-travel coverage and the stated
error box. A roller/edge follower, staggered wings or a ramp ending just beyond
the retention saddle changes the geometry and may escape. A shorter ramp also
changes loss-of-contact, snap energy and return contact; it cannot inherit this
full-stroke analysis. No result establishes that ±0.05 mm is manufacturable.

## Retention work and blocked-pin reaction

For a decision-relevant force example, assume an ideal triangular detent ridge
of height a=0.20 mm over dog travel d=1.2 mm. A ground-mounted frictionless
spring plunger has stiffness 0.4 N/mm and initial compression 0.1 mm. The ridge
rises to its apex at d/2 then falls symmetrically. Its pre-apex resistance is
`H_det(q)=k_det*(c0+2a*q/d)*(2a/d)`, reaching **0.04 N**; beyond the apex it
assists motion toward the other stop. Barrier energy is **0.016 N mm**.
This defines a finite profile and an assumed constitutive element, not a
packed or fatigue-qualified detent. Stops are necessary, and the apex is not
a safe retained command. Plunger friction, apex rounding and snap dynamics
remain absent; the values are optimistic force examples.

With ramp friction mu, guide friction mu_g and additional horizontal drag
0.01 N, resolving the contact normal and sliding tangent gives
`H/P=(m-mu)/(1+mu*m)-mu_g`. P is vertical pin force. Separate guide shoes conservatively carry the ramp
and detent-plunger reactions without cancellation; the plunger adds
`mu_g*F_plunger` to the horizontal resistance. A guide permitting reaction
cancellation would require a different contact model. If this gain is nonpositive, pushing harder cannot
produce forward quasistatic motion in this model. For m={0.5,1.0,1.5},
mu={0.1,0.3,0.5}, mu_g={0.1,0.3}, **3/18** cases have no positive gain.
The remaining cases are force bounds, not geometric or dynamic survivors.

Each writer pin has a linear push spring, initial force P0=0.01 N and
stiffness k_s=0.10 N/mm. A blocked pin cannot rise, so common driver travel D
compresses its spring. The selected pin must reach rise h=m*d and overcome
maximum detent resistance immediately before the apex. A necessary driver
stroke bound is the maximum of h, `h/2+max(0,P_peak-P0)/k_s` and
`h+max(0,P_end-P0)/k_s`. Here `P_peak=(0.05+0.12*mu_g)/[H/P]`, and
`P_end=max(0,0.01+(mu_g-1/3)*0.04)/[H/P]`. The plunger force is 0.12 N
at the apex and 0.04 N at the ends; residual guide drag can require a positive
post-apex drive force. Piecewise-affine force/travel extrema are at the apex
or endpoint. Free approach through shutters is omitted, making these lower
bounds within this separate-guide-shoe model.

For the all-zero mask, every spring is blocked and row reaction is
`80*(P0+k_s*D)`: **11.7–211.2 N** over the 15 transferable cases.
For m=1, mu=0.3, mu_g=0.1:

| Push spring stiffness | Minimum driver travel | All-blocked row reaction |
|---|---:|---:|
| 0.02 N/mm | 7.170 mm | 12.272 N |
| 0.05 N/mm | 3.228 mm | 13.712 N |
| 0.10 N/mm | 1.914 mm | 16.112 N |

All have peak selected pin force 0.141 N. Softer push springs exchange force
for travel and do not remove the common load. These are compression loads;
**do not compare them directly with E-077's separate tensile return-limiter
rating**. Both drive directions, shutter support and spring energy need their
own load paths. Shared friction/material shifts affect the entire row. No
independent-cell probability, actuator size or <30-s timing claim follows.

## Decision, checks and next discrimination

Stop treating the full-stroke sliding ramp as a moderate-tolerance completion
of E-077. Retain its tight-box section only as a comparator. Do not print it.
Next compare a positive short-stroke trip followed by mechanically isolated
cam engagement against a seated magnetic flag; require explicit loss-of-contact,
endpoint retention/reset and blocked-load paths before more fine-width tuning.
A revised mechanical route must escape the full-travel wing or demonstrate
supported packing, and bound accumulated push-spring load. Captive withdrawal
and key geometry remain mandatory. The selector campaign is not complete.

Self-review independently resolves vector contact forces, checks frictionless
work conservation (`P*m=H`), exercises frictional stalls, enumerates ramp/body
corners and arbitrary adjacent commands, and evaluates the detent profile on
100/200/400 pre-apex samples. In the force-dominated case stroke error halves
with each refinement; the end-stroke-dominated case agrees exactly. A 1,001-point whole-stroke
check also covers residual post-apex drag for both guide-friction bounds. No external
validation is claimed. Corner pressure, 3D guide/retention packing, wear,
stiffness, snap impact, readback and fault recovery still bound the evidence.
