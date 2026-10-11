---
status: complete
builds-on: [E-161, E-148]
---

# A grounded swivel can stall before crossed rolling support is restored

Input main `43c2a5a`; LAB-263. Reproduce with Python 3 + NumPy:
`python3 tools/curated-experiment-checks/E-162/probe.py --suite nominal`;
also `--suite bounds` and `--suite convergence`. JSON is disposable.
Evidence: finite primitive contact geometry, rigid-body generalized coordinates,
compliant-normal/Coulomb impulse simulation, independent analytical bounds and
self-review. No manufactured assembly, calibrated prior, measurement or hardware pass.

## Constructed contact mechanism and evidence boundary

A 3-mm-diameter translating/rotating shaft carries a nonrotating square top through
a thrust swivel. Two grounded radial bushings remove shaft lateral/tilt motion but
permit translation and rotation. Two 1-mm-diameter spherical rollers bear on opposite
sides; each spins on its own axle in a radial sliding carrier. A grounded compression
spring preloads each carrier. The first axle is bolted at +20°; the second sits in a
radial-axis swivel with a grounded torsion spring whose free angle is −20°. A thrust
washer reacts its preload. There is **no swivel angle prescription after the cut**,
no rotor brake, detent or infinite-force tangential constraint. No stop is credited.

The indexed writer supplies shaft torque and holds the swivel aligned; the cut removes
both torques. Start at prepared ±.1 m/s or rest. Docking, finite drive control and
passive electrical release are not constructed; extra head inertia/drag remains owed.
A separate unchanged cell is initialized parked. No shared shaft/swivel/tie exists.

Coordinates are `(z,s=R*theta,alpha,q1,q2,w1=r*phi1,w2=r*phi2)`; all seven remain
live. For side sign sigma=±1, roller radius r, shaft radius R, and signed eccentricity e:

`C=(sigma*(R+r+q), sigma*e*cos(alpha), e*sin(alpha))`

`rho=hypot(Cx,Cy); n=(Cx,Cy,0)/rho; gap=rho−R−r`

`axis=(0,−sigma*sin(alpha),cos(alpha)); swivel_axis=(sigma,0,0)`.

Sphere/cylinder witnesses are `C−r*n` and `R*n+(0,0,Cz)`. Relative surface velocity:
`Cdot+(alpha_dot*swivel_axis+phi_dot*axis) cross (−r*n)−z_dot*ez−s_dot*t`,
`t=(-ny,nx,0)`. Its normal/tangent projections give the geometry-derived Jacobian;
eccentric translation, surface rotation and separation all contribute virtual work.
At ±20°, e=50/200 µm gives lateral coefficients 38.792/155.046 µm/rad; normal
coefficients at −20° are .40786/6.52576 µm/rad (even in e). This replaces E-161's
assigned scalar contact-motion coefficient.

Assigned inertias: output .02 kg, shaft inertia/R² .005 kg, radial carrier .002 kg
including a .0001-kg spherical ball (`I=2*m*r²/5`), holder 1e−8 kg m². The constant
mass matrix includes eccentric translation and ball swivel/spin inertia. Loads
0/.02/1/10 N are downward generalized scenarios, not new product requirements;
10 N on .02 kg is an imposed force, not a gravitational payload. A heavy bound
changes inertia explicitly. All numbers are assumptions, not a manufactured BOM.

Normal stiffness 1e6 N/m, carrier spring 1e4 N/m and nominal preload 30 N/contact
imply 30-µm indentation and ~3-mm spring compression. Coulomb coefficient .2 bounds
**total** two-dimensional tangent force, including roller acceleration. Radial
contact is unilateral. Thrust friction is `mu_b*r_b*abs(preload_spring_force)`,
with assigned mu_b=.02, r_b=.25 mm. It can stick or slip and dissipates swivel work.
The weak return uses E-161 k=2.5e−5 N m/rad, c=1e−6 N m s/rad. Strong comparison:
k=.003, c=1e−5, same preload, geometry and friction. Spring energies at release:
6.092 µJ versus .7311 mJ; starting moments .017453 versus 2.0944 mN m.

[Drake friction](https://drake.mit.edu/doxygen_cxx/group__friction__model.html) supplies
the finite Coulomb-cone principle; [contact documentation](https://drake.mit.edu/doxygen_cxx/group__compliant__contact.html)
identifies point-contact omissions. Accessed 2026-10-11. The custom solver uses linear
unilateral compliance, not Drake/Hunt–Crossley. Finite-patch spin friction, Hertz stress,
ball/axle deformation, guide drag, backlash and wear are model discrepancy. All material
numbers are assigned bounds; E-161's hardened commercial shaft does not qualify PLA.

## Grounded-return discriminator

At release the nominal thrust breakaway moment is .15 mN m: **8.59 times** the weak
spring's maximum. Even e=0 therefore admits a stuck, aligned swivel while shaft and
rollers move. Increasing normal preload also increases this return obstacle.
The parked 10-N sphere-contact traction is 5.3207 N/contact, within the 6-N nominal
cone, but parked rank alone still misses the swivel equilibrium:

| e µm | Net contact swivel moment at −20°, mN m | Washer capacity, mN m |
|---:|---:|---:|
| −200 | +1.02032 | .15 |
| −50 | +.21864 | .15 |
| 0 | 0 | .15 |
| +50 | −.19417 | .15 |
| +200 | −.62877 | .15 |

Positive moment opens toward alignment. Normal preload contributes an even-in-e
moment while load traction contributes a signed moment. The spring has zero moment
at its free angle; all four eccentric parked cases exceed nominal washer capacity
at 10 N. This is loss of that equilibrium, not proof that every other angle is unstable.
A manufactured contact-centered pivot is not equivalent to assuming e=0.

Cuts use h=.2 ms, up to .15 s, and stop at first crossing of ±20 mm from midstroke.
Boundary overshoot is a discrete event bound, not an impact calculation. Values below
are simulation, not an accepted outage allowance. Signed triplets are downward/rest/
upward initial speed:

| Load N | Weak return: displacement mm, or boundary time ms | Strong return: final displacement mm |
|---:|---|---|
| 0 | −15 / 0 / +15; still aligned and coasting when moving | −.200 / −.032 / +.188 |
| .02 | −18.855 / −3.855 / +11.145; still aligned | −.202 / −.032 / +.186 |
| 1 | boundary 42.8 / 48.4 / 54.6 | −.275 / −.046 / +.104 |
| 10 | boundary 14.8 / 15.2 / 15.8 | −9.243 / −6.683 / −4.571 |

Weak alpha remains +20° in all 12 cuts. Strong final angles span −16.96…−21.37°;
shaft/roller/swivel kinetic energy decays numerically to rest. Its finite contact slip
is allowed; it does not cross alignment through ideal sticking. Normal forces remain
positive in the nominal cases. The strong 1-N downward run dissipates ~1.218 mJ
(including released spring/gravity work); numerical energy loss is separately .0776 mJ.
**Strong nominal arrest is a conditional result, with significant discretization
uncertainty at 10 N**, not evidence of .001-mm precision or recovery at every height.

Independent aligned bound: reflected mass .0584489222 kg gives
`z=v0*t−F*t²/(2*m_eff)` and −20 mm at 42.8595 ms for 1 N/downward .1 m/s.
Zero load preserves .292245-mJ kinetic energy and travels 15 mm/.15 s. Weak simulation
converges to this. Ideal locked crossed constraints forbid shaft motion, but cannot
remove momentum instantaneously with finite preload; E-161's static singularity stands.

The uncommanded weak cell at −20° remains at numerical zero under 0/.02/1 N, but
at 10 N leaves the traction-supporting region and reaches the boundary: its own
return-equilibrium failure, not neighbor exchange. Separate rigid grounds give block-
diagonal cell Jacobians. Real frame stiffness 1e4–1e6 N/m under a 10-N change implies
1–.01-mm common deflection (assigned bound); no regional-isolation pass.

## Bounded variation and independent static discrimination

Bounds, not production distributions: e=0/±.05/±.2 mm; washer friction .002/.02/.1;
preload 24/30/36 N; traction .1/.2/.4; bank angle ±2°; spring seat ±.1 mm; local
mismatch +1°; contact stiffness .5/1/2 MN/m. Loose/tight settings are shared coherent
bank biases, not independent cell draws. A separate +4-mm seat fault loses both
contacts even though alpha returns: returned angle alone cannot prove support.

Selected .2-ms outcomes at 10 N/downward cut:

- Weak contact-centered or high washer friction: stays aligned, boundary by 14.8 ms.
- Strong with e=−.2 mm: stalls near alignment (−.19° at boundary), boundary by 19.4 ms.
- Strong coherent loose case: ~23 N/contact and mu=.1 give total traction ≤4.62 N,
  insufficient for 10 N regardless of angle; boundary by 11.6 ms.
- Strong with output mass 1.1 kg and rotor inertia/R² .05 kg: arrests after 7.45 mm;
  this changes both kinetic energy and load acceleration, not just an energy scalar.
- Local +1° mismatch can arrest the unloaded weak runner at an unintended +26.9°;
  that is not successful −20° return, nor enough traction for the 10-N case.
- Strong contact-stiffness bounds give 9.23–9.27-mm 10-N excursion: this uncertainty
  is smaller than the demonstrated timestep and eccentricity sensitivity.

An independent static solve eliminates the two free roller spins and shaft force/
torque balance, then solves both radial spring/contact equilibria. On a .1° grid
from −80° to +19.9°, the strong nominal e=+.05-mm pair supports traction over
−25.2…−14.9° and admits washer/spring equilibrium over −25.2…−20.8°.
For e=−.2 mm its traction-admissible interval is −24.8…−14.6°, but **none** of those
angles has swivel equilibrium: even the best is .635 mN m beyond washer capacity.
This reconstructs the dynamic failure without using the time integrator. The weak
nominal case likewise has no admissible equilibrium on this grid (minimum excess
.0240 mN m). These are bounded numerical equilibrium searches, not a proof over all
possible roller shapes, stop topologies, loads or angles.

Dimensional bias, holes, layers, first-layer effects, warp and assembly alignment map
to e/angle/seat bounds; roughness/contamination to friction; creep, anisotropy,
inter-layer weakness, fatigue/wear to spring, preload and alignment drift. No calibrated
correlation length, yield, tail probability or life model exists. Common bias and e's
sign alter disposition; successful corners are not yield. Even the entire projected
.5-mm-radius ball disc under 30 N would average 38.2 MPa; actual contact stress is
higher. Contact deformation, creep and axle manufacture remain unqualified.

## Returned-jaw control and full-display gate

A direct returned jaw removes roller spins, skew matching and loaded steering; it
opens pads during writing. Same two 30-N preloads/mu=.2 give 12-N capacity versus
`12*cos(20°)=11.276 N` for centered crossed rollers. At 10 N/.1 m/s, ideal zero-delay
arrest is .050 mm for .02-kg output alone, **.146 mm with the same .05845-kg reflected
inertia**. A hypothetical .4-mm pad closure driven by 30 N on .002 kg takes .231 ms
without damping/rebound; including free fall gives .269/.312 mm respectively.
These are favorable bounds, not jaw qualification. E-148's field decay, donor capture,
energy and recovery failures remain; a downstream jaw must arrest accessible rotor
energy too, rather than conceal it in a disconnected-rotor assumption.

All machines still owe 6,400 independent 5.08-mm tops, 40-mm reach and arbitrary maps.
The nominal roller envelope is ~4.94 mm, leaving ~.14 mm total before housings;
no .07-mm printed walls are proposed. Tiers/wider internals need routed geometry.
Count 12,800 balls/spin axles/bearings, radial carriers/preloads and guide stations;
6,400 shafts/top thrust swivels, returned pivots/washers/torsion returns; H complete
heads/readers/drives, power/wiring and accessible module frames. E-161's 17.8–53.3-hour
assembly bound stands; no print-time estimate is earned. Each preload stores .045 J
at assembly; each strong return reload costs .731 mJ/site (4.68 J/board). A 10-N full
lift separately needs 2,560 J/board; rotor/return/slip energy cannot disappear.

E-161's unearned full schedule remains `T=6+ceil(6400/H)*(.08/v+.10)`: 6 s preparation,
registration, transport, final proof, settling and one retry; .10 s/site acquire/steer/
return/proof plus 40-mm motion and empty-head reset. At .1 m/s H=247 gives 29.4 s;
H=160 gives 42 s. At .2 m/s H=137 gives 29.5 s. No actual docking/reset/proof or overlap
is earned. Failed proof aborts the module. Near-endpoint writes lack the midstroke
clearance used here. Keep supported capture until height, preload and park are proved;
unattended recovery remains unbuilt. Angle-only readback accepts failed preload.
Assumed false accept p=1e−4 gives .64 expected misses/board without independence;
common datum errors survive retry.

Budget: `6400*c_site+H*c_head+c_shared < band`. Assumed $250 shared reserve already
loses <$200 ideal; $400/$500 allow $150/$250 for sites/heads, or <$.02344/$.03906/site
with free heads. At H=247 and $.03/site, $500 leaves <$.234 per complete head; $400
fails even with free heads. Include every bought item above. These are ceilings, not
quotes/BOM. No cost, packing, physical reliability or sourcing pass follows.

## Verification and disposition

Self-review: 21 swivel states give gap-Jacobian error <1.9e−11 and witness closure
<4.1e−19 m; independent material-point rotation checks swivel velocity to <1.1e−15
m/rad. Signed rolling, virtual work and static radial balance are checked. Implicit
springs, unilateral contact, Coulomb discs and washer stiction keep all internal
coordinates live. Source reports residuals/unresolved steps; unresolved solves cannot
earn a capture pass. Rigid-guide and point-contact discrepancy remains.

For a common 30-ms 1-N/downward observation, h=.4/.2/.1/.05 ms gives weak displacement
−10.80168/−10.75036/−10.72469/−10.71186 mm, tending to the independent analytical
−10.69903 mm. Strong displacement is −.27776/−.27483/−.27013/−.26821 mm;
alpha −17.3926/−17.4108/−17.4233/−17.4306°. Its numerical energy loss falls from
.1418 to .02068 mJ. At 10 N, the same steps give −10.2223/−9.2431/−8.8180/−8.6095 mm;
return angle changes by .016°, but excursion is materially timestep-sensitive.
These are convergence bounds, not a millimetre-accurate hardware prediction. All these
runs meet the solver tolerance after increasing the iteration ceiling; energy loss
from discretization is reported separately from contact/washer heat.

**Stop the constructed weak plain-thrust-swivel embodiment.** It lacks reliable
return even at zero load and has no supported 10-N parked equilibrium in the examined
region. **Do not select the strong comparison:** it demonstrates that finite sliding
can traverse alignment with unchanged preload, but loses equilibrium under a signed
assembly-offset bound, has substantial outage excursion and no complete recovery or
cost/packing advantage over a direct jaw. This rejects these constructions, not all
crossed rolling constraints. Keep the executable geometry and negative evidence.

Reopen only with a changed grounded load/return path (e.g. thrust bypass or an explicit
preloaded stop) that escapes the demonstrated moment balance **and** earns a comparison
against the direct jaw on repeated precision and recovery. A larger spring parameter
sweep alone is not the next campaign. Return to architectural search across support
and selection arrangements; do not print, buy or refine this into a chosen machine.
