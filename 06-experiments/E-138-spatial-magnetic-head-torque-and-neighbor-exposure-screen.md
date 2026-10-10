---
status: complete
builds-on: [E-137, E-128, E-129, E-074, E-080, A-007]
---

# Spatial magnetic heads: finite torque and resident-neighbor exposure

**Reject the tested unshielded 4×2-mm permanent-magnet direct rack drive under
≥1-N moving load. No complete contactless architecture is admitted.** The head
removes dog insertion phase/contact wear, but not load-angle acquisition, torque
limits, grounded retention or readback. Four resident neighbors can oppose the
selected rotor more strongly than its head even without payload. This is a
finite-geometry counterexample, not rejection of all magnetic transmissions.
Steel attraction and soft/hysteretic torque routes remain implementation questions,
not survivors inferred from assumed fields. Stop this bounded head search before
full-machine CAD, purchases or printing; change to positive mechanical support
through a moving escapement rather than tune another unsupported coupler.

Input main `7533b5e`; LAB-238. Reproduce with Python 3/NumPy:
`OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-138/magnetic_head.py`.
JSON is disposable. Evidence: primary-source mechanism/material references,
finite-surface magnetostatic quadrature, analytical bounds and self-review.
No manufactured geometry, calibrated X1C prior, dynamic arrest model, price quote,
hardware measurement or yield claim.

## Different causal routes, not new names for threshold selectors

Spatial positioning selects a head; resident seats support unchanged columns.
These functional proposals have explicit gaps and no local powered decoder.

| Route / analogy | Signed work, retention and missing implementation |
|---|---|
| Steel armature / lifting magnet | Two-pole reusable yoke attracts a steel tail plate and follows it through 40 mm. Overhead tension raises and pays out under downward load; an underside head only pulls down. Either load sign needs opposed heads or captive mechanical return. Rack pawl grounds the column; a co-located finger releases it only after head takeover. Electromagnet outage loses capture; permanent attraction still needs arrested carriage and force/gap margin. Reversal of current is not reversal of attraction (E-074). Stop single-pole reversible-drive claim. |
| PM rotor / sealed rotary coupling | Rotating head faces a diametric resident magnet on a rack-pinion shaft. Reverse rotation reverses work while synchronized; overload slips. Acquire load angle with ground bolt seated, then release/move/reseat/prove/withdraw. During transfer the magnetic gap and head arrest are in series; permanent field survives outage, but a free head rotor backdrives. Tested geometry fails below. |
| Soft-steel rotor / synchronous reluctance machine | Rotating two-axis field drives a salient steel rotor; reverse field rotation reverses work. Single alternating field lacks commanded continuous rotation from every phase. Repeats steel rotor, rack, ground bolt, bearings and release interface; head needs multiphase windings or rotating poles plus return yoke. Coil outage loses torque; permanent poles retain only finite torque. No finite steel/neighbor solution or passive arrest. Conditional reserve, not survivor. |
| Hysteretic rotor / overload clutch | Reusable magnet head drives a resident hysteresis ring; slip dissipates work. Unlike a pure eddy-current disk it can transmit static torque, bounded by material. Same grounded bolt/release/arrest sequence; 6,400 special rings, hubs and bearings plus thermal/remanence obligations. No tiny-ring material/cost/torque basis; stop before design. |
| Direct keyed control | Independently phase motor, insert positive dogs, take flank, release ground bolt, move, reseat/prove, withdraw. E-127/128 already expose fit/routing/arrest failures. Eliminates magnetic slip and exposure, retains dock wear/keeper/arrest. No admitted alternative. |

M-010 is frequency selection; A-016 and E-063/065/074/080 are crossed-field
**command memory plus separate shared motion**, not moving power heads. E-127/128
already study phase acquisition and E-129 tests failed no-back/dual-stop repairs.
A-007/E-132 preserve screw throughput and moving-arrest failures. E-136's
whole-history energy-isolation gate is preserved: small neighbor amplitude alone
cannot justify unlocking a neighbor.

Sources accessed 2026-10-10 UTC:
[KTR magnetic couplings](https://www.ktr.com/ch/en/products/magnetic-coupling/)
and its [hysteresis instructions](https://www.ktr.com/dam/jcr%3A4c78dc32-7ad9-4124-8c2b-1eef705f4160/46532EN000000.PDF)
motivate synchronous/hysteretic routes, not scale transfer.
[K&J coupling experiment](https://www.kjmagnetics.com/blog/magnetic-coupling)
reports finite slip torque and troublesome axial attraction; its empirical
shear/pull multiplier is **not** used here.
[K&J steel comparison](https://www.kjmagnetics.com/blog/magnets-vs-steel)
identifies finite steel area/thickness and air gap as limitations; a catalog
zero-gap pull force is not our finite armature force.
Four analogies yielded no complete survivor: bounded saturation of this cheap
search, not landscape exhaustion. No new A/M object is justified.

## Executable finite magnetic discriminator

Construct two parallel cylinders, radius 2 mm, length 2 mm, diametric uniform
magnetization; axes normal to a planar 5.08-mm grid. A head faces the selected
resident rotor across gap g. No steel shield/return is present: the entire
external air field is included by the finite-source model. Resident edge separation is 1.08 mm;
hubs/bearings/pinions remain unpacked. Larger/staggered internals are permitted
by stage 02 but change this geometry.

[Arnold's N35 table](https://www.arnoldmagnetics.com/products/neodymium-iron-boron-magnets/)
gives typical Br=1.210 T. Set fixed M=Br/mu0, assuming recoil permeability one
and no demagnetization, temperature dependence or magnetic steel. This is a
material-anchored idealization, not a purchased-part tolerance. Use the surface
pole representation sigma=M·n, derived in
[Fitzpatrick, Permanent Ferromagnets](https://farside.ph.utexas.edu/teaching/jk1/lectures/node60.html).
Our cylinder has no end charge; integrate its side using midpoint angular/axial
patches. For rotor directions a and b, interaction energy is `U=aᵀ C b`, where
`C=mu0/(4pi) Σ(q_i q_jᵀ / distance_ij)`. The negative derivative with respect to receiver angle
is torque. Singular values of C give the minimum/maximum available torque
amplitude over head orientation; these are stall amplitudes, not working margins.

| Face gap / coherent lateral head offset, mm | Selected torque amplitude range, N·mm | Worst of four head-to-neighbor torque amplitudes, N·mm |
|---|---:|---:|
| .3 / 0 | 1.840 / 1.840 | .471 |
| .3 / .5 | 1.698 / 1.791 | .529 |
| .6 / 0 | 1.465 / 1.465 | .389 |
| .6 / .5 | 1.372 / 1.433 | .416 |
| 1 / 0 | 1.107 / 1.107 | .295 |
| 1 / .5 | 1.048 / 1.087 | .342 |

Nine scenarios include .25-mm offsets. Gaps and lateral bias are coherent
rail/mount/clearance/warp bounds, not process priors or yield samples. Tilt,
runout, dimensions, housing creep, layer steps, friction, anisotropic strength,
wear and magnetic constitutive discrepancy remain additional uncertainty.

E-127's 3.6-mm pitch-radius rack needs **3.6/11.772/36 N·mm** at **1/3.27/10 N**,
before friction/inertia. These loads are scenario bounds, not stage-02 service
requirements. Even the best tested geometry fails the 1-N direct-drive scenario.
A common ±10% M scenario multiplies every pair torque by .81/1.21; even +10%
gives only 2.23 N·mm at the smallest gap. Reducing payload can remove this
particular failure; a gearbox adds turns/interfaces and does not cure the
following resident coupling at its magnetic input.

**Resident magnets do not turn off when the head leaves.** A same-plane neighbor
at 5.08 mm has torque amplitude .485–1.053 N·mm, depending on selected phase.
For four cardinal neighbors, choose each parked angle to oppose positive motion
at selected phase 45°. The exact sum is **3.280 N·mm**, above the head's 1.840.
The executable emits the four fixed parked angles; they do not need feedback.
For pair matrix diag(cx,cy), symmetry gives `2 sqrt(2) sqrt(cx²+cy²)` for this
maximum, independently checking the angular search. A small five-site cluster
thus supplies a static start/stall counterexample even at zero payload. This assumes independently reachable phases; constrained
height alphabets need separate checks. It is neither a dynamic barrier-crossing
model nor a 6,400-body worst-case bound. Other magnets/heads can add or cancel
exposure; cancellation is not guaranteed.

Unchanged bolts must react neighbor torque and remain physically unselected;
a threshold substitution returns to E-074/080. Common M scaling leaves the
resident/head ratio unchanged. Stronger head-only magnets, spacing, tiers,
multipoles or finite steel returns can reopen it, counting material, saturation,
axial force, space and assembly; no free shield.

Self-review: 32×6 / 64×12 / 128×24 surface meshes give selected .3-mm-gap torque
1.82892 / 1.84017 / 1.84307 N·mm; last change .158%. Neighbor maximum is
1.05566 / 1.05313 / 1.05251 N·mm. Far-field axial/lateral/oblique cases agree with
independent point-dipole energy within .081% at 100–141 mm; the point dipole is
**not** used at operating gaps. Checks also cover reciprocity, coaxial rotational
symmetry, energy derivative, zero net work for one receiver revolution with fixed
head, gap trend and the analytic four-neighbor maximum. Numerical convergence
does not validate the fixed-M material model. No external validation claimed.

## Attraction bound, complete-machine accounting and decision

For an assumed total normal pole area 6 mm², ideal gap pressure `B²/(2mu0)` gives
.0955/.382/1.528 N at B=.2/.4/.8 T. These B values are explicit scenarios, not
predicted steel-armature fields. Two equal gaps require ideal `NI=2gB/mu0`:
95–382 AT at g=.3 mm; 318–1,273 AT at g=1 mm, before leakage/steel reluctance.
Doubling gap at fixed NI quarters ideal force. Coil packing, heat, saturation,
neighbor force and force over 40-mm travel remain unproved; no signed capture
or force margin is established. Stop unsourced field/threshold optimization.

All proposals retain 6,400 guides and service seats plus seat returns/release
interfaces. Rotary routes repeat 6,400 racks, pinions/hubs, grounded bolts,
and at least 12,800 radial bearing interfaces plus thrust reactions. PM rotors
add **6,400 magnets, 160.85 cm³ total magnetic material**, retainers/orientation
inspection and exposed resident fields. K heads add K drives, bearings, gap
registration, ground-bolt release fingers, carriage arrest and height readers.
Reluctance adds head returns/windings; PM shielding adds resident material.
Printing does not remove fits. Housing material/print time is unknown; 10–30 s
assembly/site alone is 17.8–53.3 hours. The 406.4-mm board needs X1C modules.

With a hypothetical $250 frame/power/reader reserve excluding heads/local parts,
**all local bought parts**
together must average <$0.0390625/site at $500, or <$0.0234375 at $400. At K=33,
`6400*c_local + 33*c_head < $250` is the residual allowance; its terms cannot
both spend the whole reserve. $200 ideal is already missed by that reserve.
No supplier quote or complete <$500 BOM is established.

Forty millimetres requires 1.768 rack revolutions and work 256F J/board at moving
load F N. A coupled magnetic rotor must keep transmitting throughout that travel;
an initial attraction pulse is not stored 40-mm work. Replaying E-137's optimistic
allocation `T=6+ceil(6400/K)*(.04/v+t)` gives K≥29/33 at v=.4 m/s and
local event t=5/20 ms. Six seconds explicitly reserve preparation, shared transit,
final proof, one supported retry and settling; t covers capture, acquisition,
release, reseating and withdrawal. **Neither allocation is earned here.** Detailed
spatial transit, load-angle acquisition and shared-head interactions can make it
slower. Local updates keep unchanged seats loaded, but vibration/displacement
is unqualified. No cost or complete-update pass follows from coupling strength.

Read actual height and loaded seat proof; motor angle misses slip. On mismatch
keep capture, inhibit withdrawal, restore support, retry once or isolate module.
Mid-transfer outage recovery remains unproved; an ideal brake does not close it.
False acceptance/common registration faults are unbounded; no yield claim.

**Next decision:** stop contactless transfer-head refinement unless a changed
finite topology escapes both the torque/exposure cut and supported input-loss
obligation. Change functional axis to **positive moving support in reversible
escapements**, comparing load-bearing travelling pallets/conjugate cams with the
fixed-slot control. E-129's disjoint fixed-bolt windows and E-130/134's free moving
coordinate are negative controls, not proof against every escapement. The first
useful result must generate a reversible loaded step whose contacts constrain
support during every handover, including a freely responding input after power
loss. Enumerate actual contact states and allowable motion; stop if both supports
must release or an ideal frozen cam/friction brake is smuggled in. No new candidate
is claimed yet, no arbitrary acceptable drop is invented, and no printing follows.
