---
status: complete
builds-on: [E-054, E-055, A-013]
---

# Side-cheek shelves admit seated equilibrium but lack robust pitch margin

## Decision

Retain the simple slot as a static comparator. E-055's missing opposing-shelf
stop does **not** require spontaneous tipping or longer bearings under vertical
service load: a horizontal seated pawl has admissible lower-shelf reactions.
However, arbitrary tooth pressure gives zero guaranteed pitch margin. Do not
promote this into robust support or spend on detailed shelf FEA yet. Next compare
an explicit inset tooth-contact pad against keyed guidance, including unloaded
capture/return and retention. The pad must bound pressure eccentricity without
losing overlap under manufacturing error; a static seated solution alone cannot
replace restraint during unloaded travel. No fabrication is justified.

Input main `79ebcd1`. Analytical rigid unilateral contact, deterministic bounded
scenarios; no physical measurements, process priors, dynamic/contact simulation
or independent external review. Run:
`python3 tools/curated-experiment-checks/E-056/contact_equilibrium.py`.

## Contact reconstruction and force balance

Use E-054's generated wings, length L=0.8 mm and thickness h=2 mm, with shelves
covering the entire longitudinal wing in the seated state. Choose local wing
coordinates x=[0,L], bottom z=0, tooth load z=h. E-054 clearance is removed by
seating before this calculation; continued tooth overlap and parallel horizontal
contact are assumptions, not proven acquisition behavior. Its two lower shelves
supply the combined pitch reaction. Transverse load is symmetric here; roll,
yaw, structural deflection and nonparallel surfaces remain unmodeled.

For relative placement dr-dp in [-e,e], the tooth contact interval is the
intersection of [o-r+dr-dp,o+dr-dp] with [0,L]. Generated o=0.4+e+0.02 and
r=max(0.8,o+e+0.1)+0.02. The intersection is [0,a]: a ranges 0.42–0.72 mm
at e=0.15 and 0.42–0.8 at e=0.35. Import E-054 to check both packaging
witnesses, rather than silently substituting longer wings. These are competing
rigid-placement bounds; common bias can place an entire bank at a bad corner.
No independence, probability, yield or calibrated X1C accuracy is assumed.

Let downward F>0 act at tooth pressure centroid x, horizontal H act at height h,
and lower-shelf resultant act at s. Balance gives `s=x+h H/F`.
For usable lower support [d,L-d], equilibrium requires
`d <= s <= L-d`. Endpoint reactions are
`Rright=[F(x-d)+Hh]/(L-2d)` and `Rleft=F-Rright`, both nonnegative.
They represent existence of a nonnegative pressure distribution, not actual
endpoint stress or a solved elastic contact patch. Horizontal balance additionally
requires shelf friction or an explicit link. If shelf friction alone balances H,
`|H/F| <= mu` is necessary; no value of mu is established here. A free applied
pitch couple adds its signed value divided by F to s and is omitted in the table.

## Sensitivity and changed implication

| Assumed shelf edge exclusion d (mm) | Minimum centroid margin, uniform tooth pressure (mm) | Maximum symmetric absolute H/F from pitch balance |
|---|---:|---:|
| 0 | 0.210 | 0.105 |
| 0.05 | 0.160 | 0.080 |
| 0.10 | 0.110 | 0.055 |

Values apply to both e bounds. Uniform pressure is a favorable explicit scenario,
not a prediction. Edge exclusion represents lost usable bearing, not a measured
chamfer/warp distribution. Actual contact pressure can concentrate anywhere in
[0,a]; vertical loading then remains supportable for d=0, but x=0 is marginal.
An arbitrarily small adverse H makes one reaction negative. At d>0 even purely
vertical edge loading can lie outside the support polygon. Thus neither a nominal
centroid nor a free-rotation calculation establishes loaded robustness. A contact
pad that enforces x in [m,L-m] supplies at most m/h symmetric force-ratio margin
before bearing loss; its geometry and pressure bounds must actually be checked.

Loads 1/10/100 N reproduce identical normalized pitch limits (336 reaction and
center-of-pressure checks). They are sensitivity loads inherited from E-054,
not new product requirements. F changes stress and deflection, which this model
cannot assess. Under vertical loading total lower-shelf reaction is F; opposing
upper-shelf amplification is not inherently required in this seated pose.

## Verification and limits

Self-review checks force/moment residuals, independent center-of-pressure versus
reaction-sign criteria, symmetric loading, zero-height limiting case, vertical
edge load, and a just-outside-margin failure. Affine placement/contact limits
and centroid monotonicity bound the continuous error interval; no mesh/time-step
or random seed applies. Endpoint contact is only a marginal rigid solution.

This changes the next geometry comparison, not A-013's status. The 6,400 pawls,
25,600 shelf faces, channel-cost and update-time gates remain. Shelf grounding,
creep, wear, roughness, pressure distribution, bank deformation, false support
acceptance, acquisition and all support transfers remain unresolved. Stop
inferring that anti-rotation lengthening is mandatory for static vertical support;
retain E-055's angular freedom as a real unloaded/capture concern. A grounded,
retained state sequence and complete channel cost must survive before structural
refinement or a targeted physical calibration can change selection.
