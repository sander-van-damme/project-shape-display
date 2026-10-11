---
status: complete
builds-on: [E-160, E-133, E-139, E-151, E-147]
---

# Crossed rolling support has a force-singular transfer and an essential swivel reaction

**Stop zero-pitch retention and counterbalance-as-memory. Retain crossed rolling
contacts only for one finite contact/swivel discriminator.** Unequal rolling directions
can constrain height and shaft rotation without opening all contacts. Matching them
permits writing, but near alignment no finite preload provides instantaneous static
capture. Finite dissipative arrest remains unresolved. No machine or fabrication selected.

Input main `6792a3e`; LAB-262. Reproduce: Python 3 + NumPy,
`python3 tools/curated-experiment-checks/E-161/screen.py` (roughly a minute).
Evidence: primary-source analogies, exact virtual work/nullspaces, assigned-parameter
ODEs, independent quadrature and bounded scenarios; self-review. No assembly/contact
CAD, calibrated manufacturing prior, impact model, measurements or hardware pass.
JSON is disposable. Loads 0/.02/1/10 N are generalized downward-force scenarios,
including output weight in hardware application, not new service requirements.

## Search and causal machines

Two source domains plus recombination: wire-winding rolling-ring transmission;
robotics gravity compensation; replace exact zero pitch by **two unequal rolling
directions**. Repository rolling/counterbalance/spring/differential searches and
E-133/E-139/E-151/E-147 found no crossed-support witness. New topology to this
repository, not a new physical law; no search saturation claim.

[Uhing's operating instructions](https://www.uhing.com/docs/uhing-operating-instructions-rolling-ring-drive.pdf),
printed pp.1,3,24,26, describe angled rolling bearings, pitch through zero, precision
hardened shafts and vertical-support loss when the free-movement lever opens.
[US20110187036A1](https://patents.google.com/patent/US20110187036A1/en), translational
counterbalance discussion, combines positive/negative stiffness for adjustable force.
Accessed 2026-10-11; operating analogies, no transferred material/performance claims.

All proposals owe ~6,400 guided 5.08-mm-pitch tops, 40-mm reach and independent maps.
Wider/tiered internals are permitted; no packing pass is granted.

| Combination | Selection, energy, memory, ground and recovery |
|---|---|
| Zero-pitch rolling | Indexed head rotates vertical runner and steers grounded preloaded rollers. Thrust swivel isolates square top from rotation. Signed rotation raises/lowers; zero pitch proposes retention. Grounded torsion return and separate radial preload required. Read height/skew; prove support before undocking. Bare retention fails bias/coast. |
| Crossed pair | Fixed +20° roller, spring-returned −20° roller; head aligns second to +20° while delivering signed torque. Both stay preloaded. Unequal directions ground height/rotation through holders. Read height/orientations; prove after torque removal; keep head on failed proof. Unpowered return unresolved. |
| Counterweights | Independent grounded pulley/cord/guided mass per site exchanges gravity work during head-driven motion. Separate positive seat still needed for memory. Read top and mass travel; failed proof retains writer. Energy-assist control only. |
| Balanced springs | Grounded positive/negative pair supplies force bias; alternatively head translates a positive-spring anchor. Read top/anchor/load; retain writer on failed proof. Cancellation has no isolated minima; released anchor restores common motion. |
| Positive-seat control | Grounded pin/slot and retained bilateral writer exchange load after capture/unload/seating proof; motor supplies work. Failed transfer keeps donor. Existing access/arrest limitations remain. |

E-133 internal instability remains. Unlike E-139's rank-one cam, distinct rolling
rows remove the free rotor direction at park. Unlike E-151's common tie, holders
here ground locally. E-147 still separates stored energy from live-command evidence.

## Constraint, transfer and hidden swivel

Let z be height, s=R*theta circumferential travel, alpha roller skew. Ideal lateral
no-slip gives `cos(alpha)*z_dot−sin(alpha)*s_dot=0`; rolling spin is free, not a brake.
Radial preload and holder supply lateral friction; no tooth engagement is implied.
One row allows `(sin(alpha),cos(alpha))`; gravity's virtual work is `−F*sin(alpha)`.
At 20° this is 0/−.0068404/−.342020/−3.42020 N. At zero pitch only rotation is free.
Equal rows retain rank one; unequal rows have determinant `sin(alpha1−alpha2)`.
An independently grounded neighbor has zero displacement in every ideal null mode.
Floating holders change this result; incompatible rolling is not infinite-force support.

At +20°/−20° park each traction is `.532089F`. With mu=.2, required radial preload
per contact is 0/.05321/2.6604/26.6044 N; mu=.1/.4 doubles/halves these demands.
Solve `A.T*lambda=(F,0)` while second roller returns from +20° to −20°:

| Second angle | Peak traction at F=1 N | Preload/contact at mu=.2 |
|---:|---:|---:|
| +20° | singular; no static load equilibrium | no finite solution |
| +19.9° | 195.963 N | 979.816 N |
| +19° | 19.5973 N | 97.9865 N |
| +10° | 1.96962 N | 9.84808 N |
| 0° | 1 N | 5 N |
| −20° | .532089 N | 2.66044 N |

Scale by load. Zero-load motion still carries inertia. **Instantaneous static catch
fails exactly** near alignment; this does not reject finite sliding/dissipative arrest.
During .1-m/s writing, mismatch .01/.1/.5° requires lateral slip
.05103/.51030/2.55147 mm/s. Unequal perfect no-slip directions forbid writing.

Angles cannot silently be fixed. Add the second swivel DOF: its contact row is
`(cos(alpha2),−sin(alpha2),e)`, where e [m/rad] is a local contact-motion coefficient.
At crossed park the internal mode obeys `dz/dalpha2=−e/(2*cos(20°))`.
e=0 assumes a contact-centered pivot; otherwise the return spring/stop is essential.
For e=0/.05/.2 mm, 10 N applies swivel moments 0/.26604/1.06418 mN m.
These are local Jacobian scenarios, not finite geometry.

Illustrative return: swivel inertia 1e−8 kg m², critically damped time constant
20 ms implies k=2.5e−5 N m/rad, c=1e−6 N m s/rad. A 40° return stores
6.092 microjoules and starts at .01745 mN m. Even .05-mm coupling overwhelms this
spring. Preload eccentricity adds moments. Grounded bearings, centering, stronger
return and seated stops require actual construction; rank alone earns no support pass.

## Input cuts in the single-pitch control

Favorable assumptions: contact-centered swivel, perfect traction, no separation,
no bearing drag. Independent grounded spring/damper gives
`alpha=delta+(alpha0−delta)*(1+t/tau)*exp(−t/tau)` from rest, alpha0=20°.
This solves a linear torsional return, not the crossed-pair transient. Output mass
m=.02 kg, reflected circumferential inertia M0=J/R²=.005 kg; roller spin inertia omitted.
With b=tan(alpha), v=s_dot after torque cut:

`(M0+m*b²)*v_dot=−F*b−m*b*b_dot*v`, `z_dot=b*v`.

Constraint work is zero; `.5*(M0+m*b²)*v²+F*z` is conserved. The steering damper
dissipates its separate return energy. At delta=0, tau=20 ms, time=.4 s:

| F N | z from downward .1-m/s cut, mm | z from rest cut, mm | Residual rotor energy, downward cut, mJ |
|---:|---:|---:|---:|
| 0 | −4.36160 | 0 | .288716 |
| .02 | −4.69105 | −.329451 | .382537 |
| 1 | −20.8341 | −16.4725 | 21.1229 |
| 10 | −169.087* | −164.725* | 1691.16* |

*Unbounded-path extrapolation exceeds 40-mm reach: a real endpoint is encountered
earlier; no 169-mm hardware travel or impact prediction.* Upward .1-m/s cuts end at
+4.3616/+4.03215/−12.1109/−160.364 mm; the 1-N case first rises .28871 mm then reverses.
Zero load retains .288716 mJ rotor energy. No allowable outage excursion is invented.

Script compares tau=5/20/100 ms, including slow returns through 20 tau. Any fixed
nonzero bias eventually gives
`z_ddot=−F*tan(delta)²/(M0+m*tan(delta)²)`: downward drift for nonzero F, either bias sign.
Zero-load rotor coast also drifts. At 1 N, downward cut and 2 s, delta=−.1/0/+.1°
gives −12.0724/−20.8341/−31.9289 mm; negative bias reverses temporarily, not stably.

## Stores, manufacturing bounds and full board

For a counterweight speed ratio beta and 1-N balance, mass=1/(g*beta), reflected
inertia=beta/g, weight stroke=beta*40 mm:

| beta | kg/site | Stroke mm | Reflected kg | Board kg |
|---:|---:|---:|---:|---:|
| .25 | .40775 | 10 | .02548 | 2,609.6 |
| 1 | .10194 | 40 | .10194 | 652.4 |
| 4 | .02548 | 160 | .40775 | 163.1 |

Hardware is additional. A .02-N balance scales mass/inertia by .02, not load range.
Residual work over 40 mm is −40/−39.2/0/+360 mJ at 1-N balance; exact match is neutral.
Resetting mass at fixed output requires another support and replenishes energy.
Shared cord `z1+z2+y=constant` leaves `(1,−1,0)` exchange; unequal loads drive it,
and editing can move the neighbor.

Positive spring with moving anchor: `U=k*(z−a)²/2+F*z`, Hessian eigenvalues 0,2k;
common `(1,1)` motion survives without grounded anchor retention. Balanced grounded
springs have `U''=k_positive−k_negative`: neutral, unstable or one load-dependent
minimum, not arbitrary-map memory. Assigned k=1 N/mm and independent ±1/5/20%
bias give net stiffness up to ±.02/.1/.4 N/mm, force change .8/4/16 N over reach.
Equal correlated biases cancel stiffness, not external load mismatch; no polymer prior.

Crossed-park angle scenarios: coherent −2/0/+2° bank bias plus local ±1° each.
All 12 remain nonsingular; at 10 N peak traction is 5.2881–6.0787 N, needing
26.44–30.39 N preload at mu=.2. **Not yield.** Hole shrinkage, guide/assembly skew,
layer stepping, first-layer distortion and warp affect angle/e/preload; roughness,
friction, wear, creep, orientation/interlayer strength affect traction/return.
No calibrated distribution, force-tail probability or lifetime; commercial hardened
precision surfaces do not qualify printed rings. Swivel reaction dominates angle rank.

R=1.5 mm, 20° skew needs 11.6607 turns/40 mm, 1,749 rpm at .1 m/s. Work remains
0/.8/40/400 mJ/site or 0/5.12/256/2,560 J/board. Individually docked shafts leave
neighbors uncommanded. Broadcast rotation gives zero-pitch neighbors
.01918/.19181/.95907-mm drift per 40-mm write for .01/.1/.5° zero error; crossed
parked pairs instead block a rigid common shaft and require local decoupling.
Assumed shared-frame stiffness 10^4–10^6 N/m under a 10-N change gives .01–1-mm
neighbor shift; sensitivity only, not predicted disturbance.

Inventory: 6,400 runners/thrust swivels/guides, 12,800 rolling contacts/preload paths,
6,400 steer pivots/returns/stops; H torque/steering heads plus drives, readers, wiring,
power and service cartridges. No routed CAD or print-time estimate. Even 10–30 s/site
assembly/inspection means 17.8–53.3 hours before module work.

Assume 6 s/map preparation/registration/indexing/final proof/settling/one retry;
.10 s/site acquisition/steering/return/proof; two 40-mm-equivalent motions for output
and head return. `T=6+ceil(6400/H)*(.08/v+.10)` needs H=458/247/137 at
v=.05/.1/.2 m/s for strict <30 s. At .2 m/s, H=160 gives 26 s; H=80 gives 46 s.
Allocations, not earned timings. Avoiding return needs a real docking/reset route;
persistent faults abort the module.

Assumed $250 shared bought reserve leaves $150/$250 at the $400/$500 bands for
`6400*c_site+H*c_head`; ideal <$200 already fails. H=160 and $.03/site leaves
<$.3625/head under $500 and exceeds $400 with free heads. Free heads leave
$.02344/$.03906/site. Budget inequalities, **not quotes/BOM**. False acceptance
p=1e−4 gives .64 expected misses/board without independence; shared datum bias
defeats retry. Read actual height/support, not command; failed proof keeps capture.

## Disposition and verification

Retire bare zero-pitch retention, balance-as-memory and shared-counterweight isolation.
Crossed support earns one finite discriminator because its parked rank differs from
E-139; no machine pass or sourcing. Construct fixed/returned contacts, actual swivel
and ground, preload, shaft/thrust guide, signed drive and unchanged neighbor. Test
frictional input-cut return, rotor energy, swivel reaction and recovery. Stop on absent
return equilibrium, lost traction, inaccessible recovery, neighbor motion or hidden
local brake. Compare to the returned jaw; abandon if steering only complicates a clamp.
Braid/granular remain paused; no print or resource escalation.

Self-review: nullspace residuals, reactions, shared-weight mode, anchor Hessian,
angle-sign symmetry, constant-angle acceleration and energy limits checked.
RK4 dt=.4/.2/.1 ms gives 1-N downward-cut endpoints
−20.834144058/−20.834144056/−20.834144056 mm; finest energy error ~6.1e−15 J.
Independent solution: `I=integral(b/sqrt(M0+m*b²) dt)`, `z=w0*I−F*I²/2`.
Simpson 1,000/2,000/4,000 intervals converges to −20.8341440555 mm, within
asserted 1e−7 mm of RK4. These check restricted equations, not real contact,
return torque, manufacturing or physical reliability.
