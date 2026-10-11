---
status: complete
builds-on: [E-138, E-065, E-148, E-149, E-156, E-164, E-181, A-016]
---

# Passive flux gates do not give resident screws a load-independent deadband

**Stop these linear series-gap and shunt routes as machine leads.** They remove
pickup but retain 6,400 screws and moving-loss risk. A 2.5-mm gate yields 33.16:1
nominal / 17.09:1 adverse torque contrast versus 3,887:1 for the specified 1-N/.02-N
mixed-load no-slip guarantee. This is a circuit-model failure, not a rejection of
magnetic selectors or quantified acceptable disturbance; dynamics remain unsolved.
No machine selection, fabrication or purchase.

Input main `7859d6d`; LAB-297 after E-181. Run standard Python:
`python3 tools/curated-experiment-checks/E-182/flux.py` (imports E-156; disposable
JSON). Evidence: sourced principles, lumped circuits, exact extrema, uncertainty
boxes, signed screw calculations and scheduling. Self-review only; no field FEA,
pole CAD, manufacturing prior, measurement, independent validation or yield.

## Causal alternatives and prior-art distinction

Field writers drive a soft salient rotor joined to E-156's fixed-height rotating
nut; a guided translating screw carries the column. Threads, thrust/radial supports
and antirotation guide remain engaged over 40 mm. Friction governs hold/arrest.

| Route | Causal difference and missing functions |
|---|---|
| Series gates | Row/column strips insert iron bridges; both closed selects. Either withdrawn adds gap. Shared rotating field drives/reverses. Repeats two precision bridge interfaces/site plus rotor/stator/screw; strip commands, guides, returns and readback remain. |
| Parallel shunts | Row/column strips bypass the rotor; both withdrawn selects. Finite source feed reluctance is essential: with zero feed reluctance, shunts increase source flux without shielding. Two bypass interfaces/site plus feed paths. |
| Local closed-yoke head | Reusable rotating poles face a soft rotor without mechanical dogs. May avoid E-138's resident-PM interaction/global fanout; finite leakage, acquisition, gaps, inertia and transport remain unbuilt. |
| Crossed-field control | Grant equal co-rotating row/column vectors: twice amplitude, four times reluctance torque. Each contributor needs two quadrature components; E-065's scalar wire fields do not implement this. Half-selected cells remain excited. |
| Mechanical controls | Direct B4/separate B8 retain capture/proof gaps (E-181). E-148 shares excitation, not jaw/return; E-164 apertures still need writing; E-156 belt/screw retains selector contact and coast. None qualified. |

A-016/E-065 write flags, not sustained work: loaded rotors replace roughly equal
switch thresholds with heterogeneous breakaway. E-138 already proposed soft rotors;
E-149's magnetic height wells differ from thread retention. No new A/M object.
Two searches—switch-matrix shunts and reluctance coenergy—add a feed-path discriminator,
not a new physical principle. Only this cheap linear-routing axis is provisionally
screened, not the wider landscape.

Sources checked 2026-10-11: [MIT coenergy](https://web.mit.edu/6.013_book/www/chapter11/11.7.html)
supplies ideal gap force/torque derivation. Indexed claims of
[US4135136A](https://patents.google.com/patent/US4135136A/en) describe shunt paths,
row/column excitation and self-holding switches; full-page retrieval failed, so no
geometry/performance transfers. [Roton backdriving](https://www.roton.com/screw-university/screw-actions/screw-backdriving-efficiency/)
distinguishes overhauling/powered lowering; its friction is not transferred to PLA.
These proposed circuits are not patent replicas or legal novelty conclusions.

## Rotor circuit, torque and signed motion

SI internally. Assume A=8 mm², infinite iron permeability, no leakage/hysteresis/
eddy currents and effective gap `g(delta)=G+a(1−cos(2 delta))`, G=.4 mm, a=.2 mm.
Delta is field minus rotor angle; G includes .2-mm working gap and two .1-mm seated
gates. These are circuit lengths, not constructed teeth. The prescribed rotating
field grants real two-phase routing and start/acquisition; neither is built.

For branch magnetomotive force F (ampere-turns), reluctance R=g/(mu0 A), coenergy
`W'=mu0 A F²/(2g)` and rotor torque
`tau=mu0 A F² a sin(2 delta)/g²`. Its positive peak is exact at
`cos(2 delta)=4a/(G+a+sqrt((G+a)²+8a²))`. Changing F's sign does not change torque;
reversing rotating-field sequence changes commanded motion. A stationary field
cannot do net work over repeated rotor turns. Start/acquire under actual height
observation; do not credit peak torque as continuous synchronized capacity.

A stipulated minimum-gap B cap sets F=B G/mu0; **not a sourced saturation curve**:

| B cap, T | Branch AT | Peak torque, N mm | Maximum single-gap attraction, N |
|---|---:|---:|---:|
| .4 | 127.3 | .1134 | .5093 |
| .8 | 254.6 | .4536 | 2.0372 |
| 1.2 | 382.0 | 1.0206 | 4.5837 |

Attraction uses ideal B²A/(2mu0). Eighty gates at the last cap could load one strip
by 366.7 N if forces align. Field-off gate switching avoids that powered release
load but adds settling/acquisition; remanence/return remain unmodeled.

For mean screw radius r=1.5 mm, lead L=.15 mm and s=L/(2pi r)=.0159155,
quasistatic raising torque is `W r (mu+s)/(1−mu s)`; lowering needs negative torque
of magnitude `W r (mu−s)/(1+mu s)` when mu>s. Both motions then consume drive work;
friction plus released gravitational energy must leave as heat. If mu<s, gravity
can overhaul. These formulas assume the loaded flank, no collars/guide drag and
Coulomb friction. Continuous flanks give support geometry, not unconditional hold.

At mu=.3, 1/10 N require .4761/4.7615 N mm raising: the 1.2-T ceiling covers the
first peak but fails the second. Loads and friction are scenarios, not requirements
or measured PLA data. Larger/tiered internals are allowed; count their added iron,
return flux, bearings, assembly and inertia.

## Mixed loads determine isolation; increasing current cannot fix the ratio

A .02-N neighbor with static mu=.02 starts lowering at only **.00012250 N mm**
external negative torque. Arbitrary selected/neighbor phases can place selected
raising torque and neighbor lowering torque at their opposite maxima. A fixed field
then gives an incipient-slip witness; displacement at operating frequency is unsolved.
For all-phase no-slip, selected/unwanted peak ratio must exceed selected raising /
neighbor lowering breakaway. Common current/area scaling cannot fix that ratio.

| Selected W / mu | Required contrast | Formal extra gate gap, nominal / adverse 50-µm box |
|---|---:|---:|
| .02 N / .02 | 8.80 | 1.015 / 1.690 mm |
| .02 N / .3 | 77.74 | 4.136 / 5.763 mm |
| 1 N / .02 | 439.94 | 10.649 / 14.248 mm |
| 1 N / .3 | 3,887.03 | 32.827 / 43.133 mm |
| 10 N / .3 | 38,870.33 | 105.103 / 137.262 mm |

Roots above extrapolate the nonfringing law; gaps near/beyond sqrt(A)=2.83 mm lose
uniform-gap credibility. They are not physical stroke predictions. A finite field
solution is required to reopen; no blanket shielding rejection. Crossed-field ratio
4 fails even the first declared all-phase deadband case.

Series-gate contrasts for extra gaps .5/2.5/5/10 mm are nominally
3.94/33.16/108.82/390.62. At ±.05-mm adversarial errors they become
1.50/17.09/59.65/221.69. The envelope places all three selected gaps +e, all three
neighbor gaps −e and the withdrawn gate's added stroke −e. It can describe a warped
sheet plus local/row offsets; it is **not** an independent-cell distribution. A
separate common bias ±.05 mm/gap yields 64.12…21.50 at 2.5 mm. Error magnitudes are
labelled bounds, not X1C capability. No corner fraction is yield.

Ranking depends strongly on the unknown lower friction bound. At selected 1 N,
mu=.3, changing neighbor static mu=.02/.05/.1/.3 changes required contrast to
3,887/466/189/56.1. At .01 the unpowered screw already overhauls; at the threshold
s the guaranteed external disturbance margin vanishes. Uniform high friction helps
isolation but increases drive heat; a guessed nominal coefficient is not a closure.

For the shunt variant, use rotor minimum gap .2 mm, feed equivalent gap f and two
parallel bypass gaps hR,hC. Rotor flux is
`Phi=mu0 A F/[f+g_rotor(1+f/hR+f/hC)]`. Selected: both h=.1+d mm; half-selected:
one h=.1 mm. Exact peak torque follows from `−.5 Phi² dR_rotor/dtheta`, retaining
the feed/shunt source reaction. At f=0 the torque contrast is **1 for every d**.
At d=2.5 mm, f=.2/2/20 mm gives contrast **4.09/9.51/11.21**, while selected
1-N/mu=.3 demand needs **285/1,426/12,727 AT**. These are ideal circuit requirements,
not feasible currents: bypass/feed saturation, copper volume/heat and finite iron
only add unresolved obligations. A free zero-reluctance source plus an effective
passive shunt is an inconsistent grant. This topology does not rescue the deadband.

## Board interaction, input loss and complete-machine cost/time

For one selected row with S selected columns, series-gate populations are
`S selected, 80−S+79S half-selected, 79(80−S) fully off`. Model all 6,400 branches
on a common same-polarity excitation bus for one field component. With finite
common reluctance Rc, bus MMF is `Fsource/(1+Rc sum(1/Ri))`; one blocked/changed
branch changes every other branch's field. Perfect source regulation was the
favorable assumption in the torque-ratio screen.

Off flux accumulates. With 2.5-mm extra gap and 1.2 T at the selected minimum gap,
aligned rotors require common return area **3,881/5,724/7,614 mm²** for S=1/40/80
at the same field cap; at 10 mm, 1,036/1,800/2,585 mm². This is a common-bus witness,
not a universal lower bound. Local returns/segmented sources exchange it for poles,
wiring/drive or head transport. No opposite-phase cancellation is credited.
Saturation invalidates the linear law; it does not supply a qualified selector.

Excitation loss is generously instantaneous. Removing field removes neither nut
inertia nor gravity. Reusing E-156's signed loaded-flank equations at .02 N,
translated mass .002 kg, J=2.15769e−10 kg m² and kinetic mu=.02 gives downward/upward
first-stop distances **368.41/42.43 mm at .1 m/s** and **14.74/1.697 mm at .02 m/s**.
Adding a 5× inertia scenario gives 1,844.07/210.14 mm at .1 m/s. Actual iron-rotor
inertia is unbuilt; the baseline is a favorable lightweight reference, not an iron
rotor design. These ideal extended-thread distances beyond 40 mm diagnose failure
to certify containment; they do not predict motion after nut disengagement/end impact.
The .01 kinetic-friction cases can continue accelerating downward despite a higher
static coefficient having held before motion. Magnetic damping, rotor detents or
an independent arrest need an explicit model and inventory; they are not supplied
by switched-off excitation. Wrong sustained excitation still requires independent
output observation and cut.

A row writer must allow arbitrary old/target heights and both signs. Grant separate
raise/lower passes, immediate independent column deselection, no missed steps and
.02 s/row for gate setting/clear/height checks. Grant 6 s/map for data preparation,
registration, final support proof, one supported retry and settling. These allocations
are **unearned lower-complexity scenarios**, not measured budgets. With B independently
powered row banks, `T=6+ceil(80/B)*(2*.04/v+.02)`:

| v, m/s | Rotor rpm | One-bank time | Minimum banks for <30 s | Row / column command strips |
|---|---:|---:|---:|---:|
| .02 | 8,000 | 327.6 s | 16 | 80 / 1,280 |
| .05 | 20,000 | 135.6 s | 6 | 80 / 480 |
| .1 | 40,000 | 71.6 s | 3 | 80 / 240 |
| .2 | 80,000 | 39.6 s | 2 | 80 / 160 |

One-sign maps are faster; partial updates leave other threads engaged but not
protected from half-excitation/shared-frame forces. Reset gates with field off;
prove pattern before rotation. Read actual height, not just phase/current. Failed
proof cuts excitation; bounded retry requires proved support. Coast, screw damage
or reader/common-gate faults can require module isolation and a physical prop.
No universal safe recovery is constructed.

Per board: 6,400 screws, nuts/rotors, thrust/radial supports, antirotation guides,
steel pole/return assemblies and **12,800 passive gate interfaces**. Two field
components need routing; this is a functional minimum, not a finished parts count.
B banks add phase sources/drivers, independent command strips, returns/guides,
alignment and readers. Strip warp/jams are correlated faults. Friction, creep,
first-layer/wall/hole bias, roughness, wear, anisotropy and layer quantization remain
uncalibrated. 10 s/site assembly is 17.8 hours. X1C modules need boundary registration;
no printed mass/time/scrap estimate is credible without stator/strip geometry.

With hypothetical $250 shared reserve, `6400*c_site+c_controls<250` is needed for
<$500 purchases: free controls allow <3.906 cents/site for all resident bought parts
(<2.344 cents at $400; $200 ideal already missed). At v=.1, 320 command strips and
three phase sources spend the same residual, not another budget. No quote/BOM pass.
At 1-N all-raising load, thread drive work is **578/1,061/5,106 J/map** at
mu=.02/.05/.3 versus 256 J useful work; copper/core/acceleration losses are extra.
Reader false acceptance is unbounded; 6,400p expected misses needs no independence,
and common registration errors defeat retries.

## Decision, reopening and verification

Stop current/dimensional optimization: the tested gates add contrast, flux, speed
and interface burdens without improving arrest. Local-yoke writing remains unbuilt.
Reopen only with changed isolation/return topology **and** bounded retained motion;
a favorable selected-force number is insufficient. No gap-calibration print yet.

Next: nonlinear coincidence without mechanical gap switching. Cross-check
A-016/E-074/E-080; reconstruct one closed circuit through select/half-select/reset
and signed work. Stop if it hides local active gates, repeats flags plus capture,
or retains the same high-speed screw as its only motion/retention proposition.

Self-review checks: torque/coenergy finite difference error <2.6e−14 N m; angular
peak errors 2.17e−5/9.79e−7/8.11e−8 at 256/1,024/4,096 intervals; zero saliency,
zero MMF, current-sign and rotation-sign symmetries, squared excitation scaling,
closed-cycle work <6e−22 J; exact thread frictionless/overhaul limits; exhaustive
four-row mask counts; independent Kirchhoff and flux-energy balances for common
feed and bypass circuits. Coast source retains its energy/flank checks. Strict
integer schedules checked. This verifies the declared reduced models, not actual
pole geometry, transient motion, independent validation or hardware performance.
