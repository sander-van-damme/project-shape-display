---
status: complete
builds-on: [E-115, E-082, ADR-015, E-092]
---

# Captured cam return fails blunt-pin transfer and shared jam protection

**Reject the studied straight-slot, square-ended transfer pin as a completed
selector.** It supplies a bidirectional energy path without blocked push springs,
but clearance-mounted outputs cannot reliably transfer between its independent
keeper and cam slots. A conditional tight-bound section also lacks a shared
80-output force-limiter window under every tested drag/strength scenario.
No support, selector, complete machine or fabrication release is selected.

Input main `55827bd`. Reproduce:
`python3 tools/curated-experiment-checks/E-116/captured_transfer.py`.
Deterministic standard-library finite polygons, interval transfers, support
sweeps and force bounds; no random sampling, process priors, measurements,
contact dynamics or physical qualification. All dimensions, errors, strengths
and friction values below are **explicit epistemic scenarios**. Search counts
are not yield. Verification is self-review, not independent validation.

## Changed coupling and its actual boundary

A crossbolt carries a vertically sliding square pin. The bolt sits between a
lower grounded keeper and an upper translating cam plate, separated by G=4 mm.
The pin is 4.8 mm long. Its lower end moves from z=−1.4 to +0.6 mm: low engages
the fixed keeper and clears the cam; high clears the keeper and engages the cam.
Both plates are 1.2 mm thick. During the 2-mm selection stroke, the pin overlaps
both layers before leaving either. The cam must remain at home during transfer.
An external positive fork is the command-energy boundary; its finite attachment,
transport, collision and withdrawal are **not implemented** by prescribing z.

The active cam has a finite straight parallelogram slot. With plate travel s,
its square follower moves x=d*s/R, opening the crossbolt. Reversing s positively
returns the bolt. The inactive pin stays in the stationary keeper, below the
moving cam: there is no blocked spring accumulating the common working stroke.
Cam motion can pause open while the carrier moves, then return before support
proof. A pin midway between layers instead couples a stationary and moving slot
and jams; a common plate position cannot prove every pin withdrew.

A command tab has two horizontal retaining grooves separated by its 2-mm stroke.
A transverse gate enters around the programmed low/high tabs and stays closed
through cam return, ground proof and carrier withdrawal. It opens only at cam
home for positive reset. A .4-mm tab, slot side gap `2.5e+.05`, and .4-mm web
allocation are tested in section. **Tab slack persists after the setter departs**:
its retained z drift bound is `5e+.05`, not the writer endpoint error. At e=.05,
cam-clear/active-engagement and keeper-clear reserves are .15/.20 mm after this
slack. At e=.10 the same vertical package loses those clearance guarantees.
A halfway tab collides with the web, rather than becoming a valid third command.
This is a finite retaining-section check, not an assembled gate, force interlock
or command-reader qualification; gate y routing and the bolt/pin bearing remain
unresolved. No passive detent or gravity completion is credited.

## Finite slot, backlash and guide synthesis

Nominal square pin width p; full width error ±e; independent x/y datum errors
±e; inward/outward slot-wall error ±e. Let m=d/R and nominal slot half-width in
the coordinate x+m*y be `H=p*(1+m)/2+g`. Actual vertices of the finite slot and
square pin are checked through the entire commanded stroke. The end extension
is `p/2+g` in y; its added x extent is included. All path coordinates are affine,
so endpoint containment certifies continuous motion; 257-node manufactured
holdouts supplement that check. This certificate assumes the pin has entered.

Worst slot insertion uncertainty is `A=e*(2.5+1.5m)`. Require `g−A≥c`, c=.05 mm.
The output can then float by `B=g+A`; it cannot be silently placed at slot center.
For nose overlap o, pocket depth D, crossbolt stroke d, and nose error ±e:

```
o >= B+e+c                  retained ground overlap
d >= o+B+e+c                withdrawn rack clearance
D >= o+B+2e+c               pocket back clearance
L >= d+2B+2e+.6             blade covers a fixed .6-mm guide at every position
W = D+L+d-o+B+.8+4e         same-plane rack/blade/guide allocation
```

L is the minimum actual blade length; its manufactured interval is [L,L+2e].
The nose error includes relative tip/guide registration. The .8 term is .4-mm
rack spine plus .4-mm rear reserve; 4e covers rack position, tip datum and blade
length spread. Additional guide tilt/straightness errors are unmodelled. The actual fixed guide lies in the intersection
of all blade positions, including backlash, rather than merely being named in a
footprint. Combining the inequalities yields `W≥8B+12e+1.65≥52e+2.05`.
Thus this **same-plane allocation** needs at least 4.65/7.25/12.45 mm for
e=.05/.10/.20, before other assembly details. The middle/wide boxes cannot meet
5.08-mm pitch even outside the parameter grid. This is not a universal bound on
staggered guides, circular pins, tapered/dwell cams or correlated datums.

Generator: p={.6,.8,1}, R={1.2,2,3}, d={.9,1.1,1.4,1.8,2.2},
o={.4,.45,.55,.7,.9,1.1}, D={.95,1.2,1.8,2.4},
g={.15,.20,.23,.3,.4,.6} mm: 6,480 sections per error box.
One/zero/zero pass the horizontal section gates. The tight witness is
p=.6, R=3, d=.9, o=.45, D=.95, g=.20, L=2.295 mm, B=.3475 mm.
Its insertion/engagement/back/retraction reserves are only **.0025 mm beyond
c**; support/cam-y pitch reserves are .0375/.080 mm. No further tuning is earned.
A pocket height 3 mm, blade thickness .6±e and unloaded rack lift 1 mm clear the
finite blade sweeps in this subsection. Acquiring that lift with an actual
carrier remains E-092's separate machine obligation.

## Transfer contradiction and fault consequences

A keeper permits an interval K of pin-center positions; the home cam permits C.
A blunt pin transferring without lateral recentering needs **K⊆C** for every
allowed old position. Reset needs **C⊆K**. Both guarantees require K=C for each
manufactured assembly; independently varying slot walls/datums do not ensure it.
Enlarging just one entrance repairs one direction at the expense of the other.
Overlap in z does not cure an x/y entrance collision.

Reconstructing 64 coherent/local error corners for the tight witness, only 12
satisfy each directional containment; neither direction is robust. An explicit
finite-wall witness uses a .65-mm pin, K=[−.275,.175] and
C=[−.0525,.1825] mm. At the permitted keeper endpoint −.275 mm, a square pin
corner penetrates the cam entrance by **.2225 mm**. The independent polygon
check reproduces it. These counts are uncertainty cases, not failure frequency.
At zero error the equal nominal intervals transfer, confirming that the problem
is clearance/registration, not an impossible nominal trajectory. Common absolute
translation cancels; independent relative errors and coherent adverse bank
errors remain permitted. Exact co-registration is a changed manufacturing premise.

A stuck bridging pin also has **.205 mm** interval separation between keeper and
fully stroked cam in the witness, even granting both their maximum slack. An
unknown or failed command must inhibit common cam motion. A false selection
acceptance can open an unintended ground support before carrier acquisition;
a falsely accepted ground proof can release the carrier into no support. A
correct command reading alone proves neither load transfer nor individual
withdrawal. Failed motion requires a stopped, supported bank; no automatic
fault-safe extraction path has been established.

For p=.6, minimum pin width .55 mm and assumed effective bending lever 2.4 mm,
`F_pin=sigma*.55³/(6*2.4)` gives .0578/.1155/.2311 N at assumed effective
allowables 5/10/20 MPa. These are static cantilever scenarios, not PLA properties.
With output drag f={.005,.01,.05} N and cam friction mu={.1,.3,.5}, input gain is
`(m+mu)/(1−mu*m)`, valid here for positive denominator. One bank drive needs
at least `80f*gain`; protecting one jammed pin requires at most `F_pin*gain`.
Even 80*.005=.4 N exceeds .2311 N, so all 27 combinations lack a shared limiter
window. The result is conditional on the specified unsupported lever and drag;
it does not reject a double-supported pin, per-output limiter or smaller bank.
Loaded realignment, inertia, guide friction and compliance can only add demands
to this simplified force calculation. The frictionless limit recovers virtual
work, F_input=m*F_output; reverse motion has the same magnitude requirement.

## Disposition and next discriminating evidence

Stop this blunt-pin, unsupported-follower, same-plane embodiment. Preserve the
positive cam return and two-layer transfer as mechanism references, not accepted
selection. A powered E-115 pivot output would still need the failed selector
transfer, plus its own finite torque conversion; it gains no pass from replacing
the crossbolt. No timing or price pass is inherited from ADR-014/015.

A changed coupling must **actively recenter during both set and reset, retain
support during that lateral motion, and limit a single jam independently of the
bank's useful force**. The next bounded investigation is a tapered, positively
captured transfer with a double-supported or relocated follower; compare a wider
row cartridge with this pitch-bound control. Reject it if taper contact cannot
complete/withdraw in both directions under the declared friction/error box, or
if it simply adds an unqualified spring and repeats E-079/E-088. Investigate its
finite writer only after that transfer gate passes. This is a substantive new
contact/grounding boundary, not permission for another nominal gap sweep.

Full scale already repeats at least 6,400 pins and 6,400 bolts, before carrier
supports, tabs, gates, guides and readers. Shared work energy does not supply
independent data. A hypothetical reusable row writer still needs actual data
channels, indexing, reset and readback; 80 channels with $250 elsewhere have
<$3.125/channel before any cell purchases. No writer, quote, assembled 3D package,
manufacturing yield, fatigue, creep, wear, regional disturbance, full-machine
schedule or hardware performance is demonstrated. No print or purchase proposed.
