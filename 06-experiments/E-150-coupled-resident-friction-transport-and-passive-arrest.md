---
status: complete
builds-on: [E-149, E-148, E-131]
---

# Coupled resident friction: transport survives; tolerant continuous support does not

**Stop this shared-head/resident-foot embodiment.** A force-driven elastic section
can transport and dissipate post-cut motion, including at zero load. However,
soft preload permits simultaneous separation despite opposed head coupling; a
stiff common-mode bridge removes that gap while restoring an unsupported gap-setting
requirement. Loaded/unloaded neighbors do not remain parked across the tested
frame-coupling bounds. This closes LAB-250's bounded probe, not ultrasonic motors
or all frequency-selective supports. Keep the screw and E-148 field jaw as controls;
no machine, physical qualification, print, purchase or staffing selected.

Input main `26858a3`. Reproduce with Python/NumPy and a C++17 compiler:
`python3 tools/curated-experiment-checks/E-150/probe.py`.
Compile products/JSON are disposable, in run-owned scratch when available.
Evidence: sourced modeling principles, assigned-parameter elastic/contact simulation,
finite contact envelopes and analytical bounds. Self-review only. This is a
lumped resonator section, **not a constructed elastic wave, piezo electrical model,
FEA-derived mode, calibrated contact law, assembly CAD or physical measurement**.

## Mechanism, sources and bounded model

A shared two-force head elastically docks to opposed resident shoes on a guided
runner. Soft grounded springs preload hard pads; resident motion, stick/slip,
separation, backloading and ringdown are solved. After cut the unpowered head stays
docked; the same pads arrest. An unpowered adjacent runner couples through frame
springs. No capture brake or local powered driver is granted.

Primary sources, accessed 2026-10-11:
[Li et al. 2016](https://doi.org/10.1016/j.jsv.2016.07.003) motivates mutually coupled
stator/slider dynamics and stick/slip/separation rather than assigned surface motion.
[Popov and Li 2017](https://arxiv.org/abs/1705.03379) separates tangential elasticity
from the all-sliding limit under normal/tangential oscillation.
[Takano et al. 2011](https://doi.org/10.1299/kikaic.77.4144) demonstrates a spring-based
preload concept with a constant-force region. These establish principles; their
parameters, miniature packaging and measured performance are **not transferred**.

Two cells × two feet × normal/tangential coordinates, two head coordinates and two
runner coordinates give 12 DOFs. For each foot, incremental inward displacement x,
axial displacement z, runner height y and tangential elastic memory e:

- `N=max(N0+kn*x,0)`; support normal force `N0−ks*x`; tangential ground force `−kg*z`.
- `f=kt*e` acts upward on runner and oppositely on foot. Integrate relative motion
  into e, then project to `|kt*e|≤mu*N`; separation erases contact shear memory.
- Selected-foot dock energy is `kc*(x−sigma*hx)^2/2 + kc*(z−sigma*hz)^2/2`,
  sigma=+1/−1. Reciprocal reaction acts on head; head has finite mass/stiffness.
- Corresponding neighbor coordinates couple through `kf*(q0−q1)^2/2`.
  Optional resident bridge adds `kb*(x_left+x_right)^2/2` in each cell.
- Head forces are `40*cos(omega*t)` and `sign*20*sin(omega*t+phase)` N, with a
  1-ms ramp. Set both to zero at cut; no state/energy reset. This grants actual
  excitation removal, not merely loss of the upstream supply.

Assigned nominal SI parameters: N0=6 N/foot, mu=.1, kn=60 MN/m, kt=20 MN/m,
ks=.060 MN/m, kg=40 MN/m, kc=25 MN/m; foot modal mass 1 g, head coordinate mass
2 g, head stiffness `mh*(2*pi*40kHz)^2−2*kc=76.331 MN/m`. Mass-proportional damping
`c=m*2*pi*40kHz/Q`, Q=40, is a scenario, not measured piezo/PLA loss. Grounded
supports carry preload and modal reactions; assigned mode masses are not a parts BOM.
Nominal kf=.001*kg. Signed downward generalized loads 0/1/10 N pair with runner
masses .02/.12/1.1 kg. W is total generalized bias; zero W is a bias-free
diagnostic, not free counterbalance hardware; no new requirements. Strong case uses
60 N/foot. One coefficient represents both static/sliding limits; .02/.1/.3 and
kt=2/20/60 MN/m bracket constitutive uncertainty without claiming real friction tails.

Initialize loaded equilibrium only where capacity permits; otherwise contact slips.
Drive is 30 ms then 120 ms unpowered; 90-ms drive
checks steady behavior. Q=200, coherent preload .8/1.2, phase ±.2 rad and frame
coupling .001/.03/.1 are explicit scenarios, not a full Cartesian bound or yield.
No independent cell errors or fabricated process distributions are sampled.

## Discriminator and changed embodiment

Velocity averages the last 6 ms powered; excursions are relative to cut height.
Steps: 50 ns, stiff bridge 25 ns:

| Case | Powered velocity, m/s | Both feet absent | Post-cut extreme, mm | Largest neighbor motion |
|---|---:|---:|---:|---:|
| 1-N raise, soft preload | +.05875 | 14.4% | +.0954 | .195 µm, loaded neighbor |
| 1-N lower | −.08631 | 14.4% | −2.193 | .323 µm, loaded |
| Zero load, raise | +.07401 | 14.4% | +.0462 | .000081 µm, unloaded |
| 10-N attempted raise, 60-N pads | −.06865 | 0% | −1.346 | .000176 µm, loaded |
| 1-N raise, kt=2 MN/m | −.04548 | 14.4% | −.754 | .000176 µm, loaded |
| 1-N raise, kf=.1*kg | +.05854 | 13.6% | +.0941 | 43.7 µm, loaded |
| Same, unloaded neighbor | +.05864 | 13.6% | +.0944 | 411 µm |
| kb=60 MN/m bridge, 1-N raise | +.05681 | 8.0% | +.0898 | .190 µm, loaded |
| kb=600 MN/m bridge, 1-N raise | +.04852 | 0% | +.0661 | .199 µm, loaded |
| Same stiff bridge, lower | −.06760 | 0% | −1.349 | .263 µm, loaded |

**Opposed dock signs do not constrain x_left+x_right=0.** Nonlinear normal motion
changes phase/mean; each foot contacts 42.8% of a cycle. Refined tangential stick
occupies ~30.4% of foot-time. The high-preload case
keeps 120-N minimum total normal but cannot raise 10 N with this finite writer.
This is a force/frequency/coupling-specific failure, not a maximum motor capability.
E-149's ideal 60-N/90-N-modulation, 1-µm/40-kHz ellipses instead yield 10.401-N
stall traction. The differing imposed stroke/normal modulation is precisely what
must be earned; the table is not a matched-stroke efficiency comparison.

The 600-MN/m **cross-foot bridge is a material topology change**, penalizing common
normal motion while leaving the differential drive mode. It attains 12.645-N minimum
total normal while powered, 11.355 N across startup/cut/decay. It shunts the soft spring.
For parked symmetric total gap error dg, static solution gives per-foot change
`dN/dg=(kn/2)*(ks+2*kb)/(kn+ks+2*kb)`.
To keep 6-N preload within ±20%, total gap allowances are **40.04 µm / .05999 µm /
.04200 µm** for kb=0/60/600 MN/m. Docking adds kc to ks in this formula:
even the soft case then needs **.1358 µm** unless docking accommodates actual foot
positions independently. Perfectly centered docking was assumed in the dynamics.
These are requirements, not X1C accuracy; adjustment/frequency-selective support
needs another mechanism. Stop instead of granting a free fit.

Illustrative metal cantilever: stipulated E=200 GPa, L=10 mm, width=2 mm,
thickness=.8434 mm gives ks=60 kN/m. At 6 N, deflection=.1 mm, root stress≈253 MPa,
initial energy=.6 mJ/pair; at 60 N, 1 mm, ≈2.53 GPa, 60 mJ/pair. No alloy/yield,
fatigue, nonlinear-deflection or packing qualification. This makes the low-force
soft-preload escape concrete without claiming a printable micron interference.
Changing bridge/contact stiffness changes both manufacturing sensitivity and modes.

## Arrest, isolation and verification limits

Cut does not stop the output instantaneously. Nominal stored dynamic/contact energy
at cut is .280 mJ (10-N case 2.764 mJ); these exclude the constant baseline preload
spring energy, whose incremental work is already included. Residual foot motion,
runner inertia and elastic shear all remain. At 120 ms the nominal output still has
~7.34e−5 m/s peak velocity over the final 2 ms. Small elastic oscillation is **not
exact arrest**; no product disturbance/settling
threshold is invented. End-stop impact/rebound and all-height containment are unbuilt.

At mu=.02, capacity is only .24 N: a 1-N load cannot remain parked after decay.
The .8-preload corner similarly has .96-N capacity. This analytical failure is
decisive independently of the mu=.02 unrestricted >40-mm escape, where the finite
runner model expires. With excitation absent and initial .1 m/s, simulated
total travel agrees within 1 µm with `m*v²/(2*C)=.08333 mm` for m=.02 kg, C=1.2 N.
This independently checks inertia/friction; zero load is not zero coast.

Neighbor elastic displacement is distinguishable from slip. At kf=0 a loaded
neighbor remains exactly parked; nominal coupling accumulates ~.390 µm of summed
pad plastic slip and ~.195 µm runner motion. The 90-ms exposure grows runner motion
to .602 µm. Larger coupling moves even the unloaded neighbor substantially.
Two cells do not bound bank resonances, repeated exposure or common faults.

Wrong and correct sustained commands can have identical forces. An external
stall fixture dissipates 17.24 mJ with zero travel; this diagnostic adds no brake.
Actual force removal permits passive decay, while driver backfeed, stored electrical
energy or a stuck source can prevent it. Count switching, discharge and energy
handling. Over the nominal 30-ms drive, summed positive mechanical source
work is 30.32 mJ and returned work 15.66 mJ; lowering returns 16.31 mJ while still
consuming 10.06 mJ net. Instantaneous source/sink capability cannot be replaced by
positive average input. Electrical efficiency and peak current are unmodeled.

Keep head grounded/docked through cut, actual height/settling/support proof. Failed
proof inhibits indexing and permits one supported retry after independent cut.
Pad/frame-breakage recovery is unbuilt.
Readback has no measured false-accept bound; assumed p=1e−4 gives .64 expected
misses per 6,400 reads without independence. Shared bias can defeat repeated proof.

## Geometry, full-display accounting and controls

Runner spans z=y−42…y+2 mm across y=0…40 mm. Each fixed shoe has 1-mm axial length,
1-mm² face, .4-mm lateral thickness. Bound tangential mode travel by ±10 µm (all
simulated feet remain inside); exact affine endpoint extrema give **1.490-mm minimum
end land** and **2.260-mm adjacent pad-envelope clearance** at 5.08-mm pitch.
A putative front/back bridge outside |y_lateral|=1.6 mm has .590-mm runner clearance.
These translated envelopes do not establish spring, mass, guide, docking, bridge
or head assembly fit. Compression represents deformable layers. Full-transient
peak pad force≈43.9 N means 43.9 MPa; strong case≈108.8 MPa. No PLA pad/creep claim.

Retain 6,400 columns/guides, **12,800 hard wear interfaces**, resident resonator and
preload paths, possibly 6,400 bridges/adjustments; H heads require two force modes,
piezos, docking couplers, phase drivers/matching, cables, return-energy handling,
readers and abort. Total preload closes mostly locally: 76.8 kN at 6 N/foot,
768 kN at 60 N. All cells at 1/10 N give 6.4/64 kN axial frame reaction. Printed
parts do not erase guide drag, spring calibration, wear, assembly or repair.

The permanent-preload **direct-sliding control** uses a captured translating head
pushing the runner through fixed resident pads: no ultrasonic mode needed, but
full-stroke head return/capture/routing remain. At C=1.2 N, W=1 N it needs 2.2-N
raising force, .2-N downward force for lowering, and .048-J friction heat/40 mm.
At C=12 N, W=10 N these become 22 N, 2 N downward, .48 J. Passive downward coast
from .1 m/s is 3.00/2.75 mm before elastic corrections. Reduced friction defeats
hold; screw/field-jaw controls receive no new pass.

Optimistic schedule `T=6+ceil(6400/H)*(.04/v+.05+.03+.12)` includes 30-ms startup,
120-ms decay/proof, 50-ms local dock/read/withdrawal and 6 s preparation,
registration, transport, final read, bounded retry and settling. Allocations are
not earned, and finite tail motion means the 120-ms allowance is not a proven lock.
At .025/.05/.059/.075/.1/.2 m/s strict <30 s needs **493/279/238/200/165/109 heads**.
The .059 point is not verified full-stroke performance; 10-N raising fails.
Returns/height access can worsen timing; all-raising useful work is 256*W J.

With an assumed $250 shared reserve, `6400*c_cell+H*c_head<250` is necessary for
<$500 purchases. At H=238 even free local parts leave **<$1.05/complete head**;
free heads leave <$.0391/cell, <$.0195/interface/preload assembly before other parts.
No quoted BOM or cost pass. $400 leaves only $150; $200 is already missed.
10–30 s/interface assembly is 35.6–106.7 h before guides, setting and inspection.

No calibrated manufacturing/yield prior: gap/shrinkage, wall/layer/first-layer bias,
warp and alignment couple preload/docking; roughness, wear and contamination alter
shear; orientation, interlayer weakness, creep and fatigue alter support stiffness.
Common biases cannot average away. kt changes transport sign; frame coupling changes
isolation. No X1C PLA parameter ranking is established.

## Verification and decision

35 deterministic cases, no probabilistic yield. Kick-drift-kick with exact viscous
half-steps and contact return mapping; slip heat integrates `f*dp`, with negative
quadrature increments tracked rather than silently clipped. Elastic, gravitational,
kinetic, driver and damping energies are accounted. Nominal dt=100/50/25/12.5 ns:
velocity .058726/.058755/.058901/.058901 m/s; post-cut excursion
.095282/.095354/.095796/.095793 mm. Energy residual falls from −4.39 µJ to +4.38 nJ;
negative contact-work quadrature <1 nJ in the refined nominal case. These check
numerics, not the constitutive law. Conservative no-slip energy, zero forcing,
zero frame coupling, mirrored zero-load motion and the independent coast formula
are separate checks. Stiff bridge, strong load and large neighbor excursion have
additional step refinements. No forced-elastic wave or hardware validation claimed.

**Actions:** retire these soft-preload feet and stiff-bridge repair; no calibration
or wave FEA while support/isolation/manufacturing gates fail. Reopen only with a
support that separates slow preload accommodation from high-frequency common motion,
plus resident inventory, actual docking and bidirectional load/neighbor evidence.
This is a reopening condition, not the next automatic refinement task.

**Next:** discover height memory with persistent geometric support, challenging
resident duplication and serial head service together. Cross-check positive-seat,
structural-memory, particle-stack and wave-command failures; compare genuinely
changed combinations with screw/field-jaw controls. No renamed latch/hidden arrest.
