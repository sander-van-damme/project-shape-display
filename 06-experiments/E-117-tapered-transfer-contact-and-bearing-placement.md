---
status: complete
builds-on: [E-116, E-115]
---

# Tapered transfer recenters, but axial pin remains an unprotected overhung follower

**Retain the tapered transfer as a conditional contact section, not a complete
selector. Stop treating two fixed output guides as a straddling bearing pair.**
The wider section escapes E-116's blunt-entry contradiction under the .10-mm
error scenario. It does not isolate a pin jammed between both plates; a finite
1.675-mm interference remains during the working stroke. A relocated energy
follower or an actual per-output disconnect is now the substantive boundary.
No powered-pawl comparison, writer routing, machine schedule or fabrication
is earned before that boundary is resolved.

Input main `b7ec21b`. Reproduce with
`python3 tools/curated-experiment-checks/E-117/tapered_transfer.py`.
Standard-library deterministic finite-section geometry and analytical bounds;
no random seed, material/process prior, measurement, dynamic contact solver,
3D assembly acceptance or hardware qualification. All errors, friction and
strength numbers are **explicit epistemic scenarios**. Self-review only.

## Changed geometry and finite contact path

The square pin has width 1.4 mm, .2-mm square tips, two 1.5-mm-long pyramidal
ends, and total length 14.2 mm. The lower keeper occupies z=−1.2…0; the upper
cam occupies 10…11.2 mm. Positive axial selection moves the pin's lower end
from q=−5.2 to +1.0 mm and back. The cam stays at home during transfer. The
home cam's straight slot obeys `|x+.5y|≤1.7`; the keeper obeys `|x|≤1.35`.
A finite cam slot spans y=−1.35…7.35 mm, accommodating the subsequent 6-mm
plate stroke and square-pin end corners. Its working motion shifts the output
−3 mm. These generated sections do not constitute a routed writer or assembly.

At every axial event, intersect each plate's occupied z range with the actual
pin profile. The greatest square section within that intersection determines
its allowed x interval. The source interval contracts against the entering
taper: an output initially at either extreme moves only after wall contact.
No hidden command places it at the slot centre. Check entry capture for **all**
source slack, nonempty intersections throughout overlap, and both directions.
All interval constraints are affine between pin-break/plate-face events; the
convex feasible strip gives continuous collision-free paths, conditional on
adequate drive force. Endpoint traces record extrema, not a dynamic solution.
Independent manufactured vertex/plane checks at 64/256/1024 divisions recover
the same witness bounds. A zero-taper-width-reduction control fails entry.

Error e={.05,.10,.20} mm applies independently to full pin width, taper length,
pin length, keeper/cam x centres, cam y datum, keeper/cam wall offset and each
plate z position: 1,024 corners × two directions per scenario. Both pin tips
share the full-width bias initially; sensitivity below relaxes that correlation.
Common absolute translation cancels. Relative errors can occur coherently
across a bank; no independent-cell probability or yield is implied. Plate
thickness, taper linearity, guide parallelism and corner rounding remain model
assumptions. Friction/roughness, strength, wear and creep are not calibrated.

| e mm | Failed directional corner cases / 2,048 | Minimum entry capture margin mm | Minimum feasible interval width mm | Largest recenter mm |
|---|---:|---:|---:|---:|
| .05 | 0 | .3625 | 1.0125 | .2375 |
| .10 | 0 | .1250 | .7250 | .4750 |
| .20 | 160 | negative in rejected cases | .1500 among survivors | .8500 among survivors |

Analytical bounds extend the .10 result beyond corner enumeration. With shared
pin-width bias, forward/reverse tip capture margins are at least `.9−4.75e`
and `.6−4.75e`. Full-width keeper/cam intersection width is at least
`1.3−5.75e`. The full-width waist exceeds the worst plate gap by `1.2−5e`,
so at least one layer constrains full pin width throughout the transfer.
Taper intervals contain the corresponding full-width intervals. Independently
varying tip and waist widths reduces the reverse capture bound to `.6−5.75e`:
only **.025 mm at e=.10**, below a .05-mm discretionary reserve. Thus nominal
shared bias matters; this is not a robust manufactured-fit release. Increasing
both slot gaps equally does not improve this capture bound. Longer tapers lower
slope but do not add tip capture width.

## Grounding, retention and packaging

At e=.10 the maximum possible horizontal displacement from home is B=.975 mm,
including oblique-slot datum errors. A blade with 1.2-mm nominal nose overlap,
3-mm withdrawal, 2.5-mm pocket depth and .1-mm relative nose error retains
**.125-mm ground overlap**, .125-mm pocket-back clearance and .725-mm withdrawn
clearance. Finite blade endpoints enclose a fixed .8-mm guide throughout motion;
minimum blade length is 5.95 mm. During set/reset the blade stays at its support
height; its nose slides on the loaded pocket roof without withdrawing from it.
Sliding force must therefore include residual service-load friction. A carrier
must separately acquire load before the 3-mm working withdrawal, as in E-115.
Neither carrier nor proof reader is implemented here.

This uses a **12.425-mm same-plane lateral allocation**, plus a cam y envelope
of about 9.9 mm with the E-116 wall/error allowances. It deliberately exceeds
surface pitch. Staggering, row-cartridge placement and connections to 5.08-mm
columns remain unimplemented; the number is not a full-board packaging pass.
The 10-mm layer gap and 14.2-mm pin also increase volume and repeated material.

Using E-116's retained axial drift `.05+5e` gives low-state cam clearance
.25 mm and high-state keeper clearance .35 mm at e=.10. The pin remains
full-width across the active layer at both retained endpoints, with ≥1.65-mm
axial reserve. A 6.2-mm-spaced retaining gate could preserve those endpoints;
its full fork attachment, gate routing, proof, strength and reset mechanism are
still absent. Prescribed bidirectional q is a drive boundary, not evidence of
an implemented writer or a safe extraction from a loaded jam.

## Force direction, bearing contradiction and jam protection

For a planar taper with slope a and Coulomb coefficient mu, resolve normal and
friction forces for insertion velocity (−a,1):

```
F_push/F_lateral = (a+mu)/(1−mu*a)
F_pull/F_outward_load = max(0,(mu−a)/(1+mu*a))
F_eject/F_outward_load = max(0,(a−mu)/(1+mu*a))
```

At zero friction the first expression equals the virtual-work slope. With
T=1.4…1.6 mm and mu=0….7, the projected keeper/cam slopes are .6/T and .9/T;
maximum projected push gain is 2.442. All sampled denominators stay positive.
High friction requires positive pull; lower friction can eject a loaded taper,
so passive retention is not credited. **For the oblique cam this is an equivalent
2D comparator, not a certified force bound:** square-pyramid corner contact has
a 3D normal cone. A later force-closure model must resolve that cone, guide drag,
corner rounding and elastic contact. Geometric feasibility alone earns no
force-completion claim.

Including endpoint drift and dimensional errors, full-width pin material common
to all selection positions is only z=3.15…6.75 mm. Two finite output guides can
occupy 3.3…4.1 and 5.7…6.5 mm. Both sit **below the active cam contact and above
the keeper contact**. A permanently engaged closed guide beyond the cam is
impossible: the pin must end below the cam when deselected. The same argument
applies below the keeper at selection. Widening the cartridge or lengthening
the pin cannot turn these fixed guides into straddling supports while preserving
complete withdrawal. A moving/split guide or separate power follower changes
the mechanism and can reopen the claim.

Consequently use an overhung bending model, not simply-supported span capacity.
For minimum square width 1.3 mm, `Z=b³/6` and cam force lever 3.4…5.6 mm,
assumed effective allowable stresses 5/10/20 MPa give force-capacity intervals
.327….538 / .654…1.077 / 1.308…2.154 N. These are static ideal-guide scenarios,
not qualified PLA properties. In a two-point planar guide model at z=3.7/6.1,
a force at z=11.3 amplifies the sum of guide reactions to 5.333 times its lateral
magnitude. Axial sliding friction adds **.533…3.733** times lateral force for
assumed guide mu=.1….7, beyond taper force. Clearance/tilt and 3D contact can
change these values; omission would systematically understate writer force.

For the E-116 drag scenarios .005/.01/.05 N per output, 80 outputs demand
.4/.8/4 N before other losses. Unlike its slender control, this wider section
has conditional common-force windows in some strength/drag cases, but none
spans all scenarios. A per-output limiter would have a nominal unloaded window
between .05 and .327 N in the weakest conservative scenario; **no such limiter
has been implemented**, and loaded recentering or bearing friction can consume
it. Do not invent a calibrated spring, clutch or perfect reader to fill that gap.

The finite stuck-pin witness uses all positive .10-mm errors, q=−2.1 mm:
K=[−.600,.800], C_home=[−.625,.725]. After the −3-mm cam stroke,
C=[−3.625,−2.275]; its nearest edge misses K by **1.675 mm**. Tapers do not
isolate this common-drive jam. The widened rigid-pin route remains unprotected;
positive pull at cam home is not proof of extraction under a deflected shared
plate. Fault detection must also avoid false acceptance before support release.

## Decision and next discriminating boundary

Retain the geometric recentering result and reject a straddling-support claim
for the same axially withdrawn pin. Do not refine this rigid two-layer pin into
a complete selector by assuming individual overload release. The next bounded
investigation should **separate the power follower from the retained selector**:
a relocated, genuinely straddled follower with a finite positive dog/disconnect,
including insertion, bidirectional energy transfer, loaded/stalled isolation,
withdrawal and reset. Its geometry must explain how it escapes the permanent-
guide contradiction and the stuck-bridge witness. Stop it on a finite conflict;
only a surviving selector earns writer routing and powered-pawl comparison.
This is the continuation of the existing campaign, not a new architecture win.

Full scale still repeats at least 6,400 pins and blades plus ≥12,800 pin-guide
lands, retention, proof and carrier interfaces. Individual disconnects would add
repeated parts and assembly. No bill of materials, durability, production yield,
regional disturbance, <30-s update or <$500 purchased-cost pass is established.
No purchase, print, staffing change or human decision is required by this result.
