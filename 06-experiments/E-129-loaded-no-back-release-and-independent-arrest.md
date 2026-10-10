---
status: complete
builds-on: [E-128, E-127, A-025, E-126, M-004]
---

# Static no-back holding does not establish controlled loaded lowering

**Stop the tested peg-released roller joint and alternating fixed-stop substitution.**
The roller holds nominally, but extraction can remain jammed at high friction;
when released, its finite input contacts do not support an overhauling output.
Two staggered positive ground stops cannot make the proposed overlap-first transfer.
An independently driven head with permanent local drag has a conditional static
load path, with substantial force/heat and repeated-interface costs. None admits a
complete two-site machine. Change the next common-datum investigation to captive
solid-length exchange, not another roller angle, brake size or dog tolerance sweep.

Input main `6855760`. Reproduce:

```
python3 tools/curated-experiment-checks/E-129/no_back.py
```

Python 3 + NumPy; imports E-128/E-127. Disposable JSON: 81 seated-force scenarios,
nine released-contact friction cases, five dimensional biases, 12 brake scenarios.
Evidence: **finite rigid sections, exact circular contacts, static Coulomb cones
and isolated spring calculation**. No assembly CAD, contact dynamics, calibrated
process/strength data or physical result. Self-review only; a counterexample
stops the embodiment before a successful complete motion cycle.

## Source and different contact topologies

[RINGSPANN datasheet, operation p.102](https://www.ringspann.de/en/files/Datasheet-IR-843.pdf)
and [installation instructions v2, 2013-04-29, pp.3–4](https://static-files.ringspann.com/InstallationInstructions-IR-1031.pdf)
describe opposed rollers, input release pegs, separate drive studs and return
spring. They explicitly exclude an output overrunning its input during loaded
descent. Accessed 2026-10-10. These are operating-principle references, not data
for our geometry. Our inference: parked no-back hold needs a separate demonstration
of controlled gravity-aided lowering; this does not reject all no-back brakes.

Compare (1) load-energized opposed roller wedges with input pegs and spring return;
(2) two phase-staggered positive collars with grounded bolts, inserting B before
withdrawing A; (3) independent positive motor heads with permanently contacting
local drag pads. The latter has no proximal clutch or powered brake release.
The manufacturer search changes source domain from prior shaft/docking work;
M-004 already covers escapement memory, so (2) is recombination. No saturation claim.

## Finite roller geometry and local access

In a shaft-normal section, ground race inner/outer radii are 5/5.7 mm. Output cam
is a radius-4.3-mm disk clipped at vertical coordinates ±3.7832567 mm. Two .6-mm
radius rollers lie at (x,z)=(.3834853, ±4.3832567) mm, touching the actual flat
and circular race. They occupy separate pockets, avoiding overlapping rollers
in the shallow wedge. Contact angle is 5°. Input pegs of radius .15 mm initially
lie at (1.1334853, ±4.3832567); the input turns these actual circles, not abstract
release flags. A radius-.25-mm input stud orbits at 2.6 mm in an output slot with
radial extent [2.1,3.1] and tangential extent [−.37,.37] mm. Its drive half-play
is **.04617025 rad**. Pegs clear the cam and race through this travel.

Each roller has a spring envelope along its flat: cam-mounted seat x=−1,
contact x=roller-center−.6, envelope radius .08 mm. Nominal installed/free length
is .7834853 mm, **zero seated preload**, assumed stiffness .5 N/mm. Withdrawal
compresses it. This is an explicit return model, not a designed printable spring;
seat/guide strength, friction, manufacture and reliable zero-load reseating remain
unqualified. Nonzero preload changes reaction torques and is not substituted here.

Retain E-128's 5.08-mm top centers, 56-mm racks, 40-mm travel, outward pinion axes
and actual dock/ground geometry. Parked heights remain **9.211850 / 28.061406 mm**.
Place the head rings at axial y=[9,10.2] and the peg-carrying disks behind at
[10.4,11.4]; peg/stud projections enter the ring plane. Ring-pair clearance is
**.88 mm**; shafts still clear both rack backings by 3.30 mm. These are local
section/access allowances, not packed housings or actuator bodies. Unselected
site keeps its loaded ground bolt and withdrawn head. Replicated pairs still
have E-128's **4.08-mm root-disk interference**; matched docks still fail E-127's
common ±.05-mm fit scenario. No-back success would not remove either failure.

## Holding, extraction and the missing lowering branch

Let outer normal be N, flat normal B, and each tangential reaction f. Roller
moment balance equates the tangentials. For contact angle a and horizontal peg
extraction P at the seated position, zero return preload and a frictionless
extractor peg give (seated extraction model only):

```
−N sin(a) + f(1+cos(a)) − P = 0
B = N cos(a) + f sin(a)
T = x B − flat_height f
```

Enforce N,B≥0 and |f|≤mu_race N, |f|≤mu_flat B. At P=0 an independent closed
form is B=N, f/N=tan(a/2), T=R_race N tan(a/2). The 3.27-N site scenario demands
11.772 N·mm; **N=B=53.9246 N**, required friction ≥.04366094 at both surfaces.
This normal-force amplification replaces external clamping; it does not make
surface pressure, housing deflection, wear or creep free.

Intersect the six affine cone inequalities over extraction force P:

| Equal contact friction | Seated hold | Largest extraction P with sticking equilibrium |
|---|---|---:|
| .05 | yes | .76574 N |
| .10 | yes | 187.987 N |
| .30 | yes | unbounded in rigid Coulomb model |

At P=20 N, normals are 226.023/226.896 N; the .1/.3 cases still admit sticking.
The unbounded branch is **not infinite real strength**: compliance/crushing or
another unloading trajectory can end it. A changed input-force direction or
lifting first needs a new loaded-lowering construction.

Now grant successful release, the favorable low-friction case. At input lead
**.02 rad**, the generated peg has moved the roller .0875693 mm inward. Actual
race clearance is **.006766 mm**, stud driving-face clearance .0680035 mm and
opposite, load-resisting-face clearance .1719965 mm. Neither stud face touches.
The other roller can react only the opposite output torque in its seated branch.

The still-touching peg and flat are also checked: without race contact and with
a frictionless peg, roller moment balance requires zero flat friction. With spring force .0437847 N,
peg/roller force balance gives only .00127272 N flat normal. Including the
spring's reaction on its cam-mounted seat, these contacts apply **+.191543 N·mm
in the aiding direction**, not the −11.772 N·mm needed to support lowering.
Then allow peg friction up to .3 and flat friction up to .3: roller moment balance
couples their tangentials, and the two contact cones give at most **−.190528 N·mm
resisting capacity** (still aiding). Nine coefficient cases reproduce this result;
the largest cones contain every smaller coefficient in those bounds. Thus peg
friction within these bounds does not rescue the released state. Seated extraction
forces above remain conditional on a frictionless peg; they are not a universal
actuator rating for rough pegs. At positive drive
contact the stud can push the output forward; it cannot restrain a faster output.
The restraining stud wall is reached at negative lead, where the release peg has
withdrawn and the load-blocking roller wedges again. The geometry therefore has
no demonstrated quasistatic, continuously supported overhauling-lowering branch.
Actual operation may jam, run ahead and rejam, or chatter; this calculation does
not predict its dynamic cycle.

| Required transition | What the finite construction establishes |
|---|---|
| Park/input absent | Nominal loaded roller can hold if contact cones and material capacity suffice; ground bolt remains independent parked support. |
| Raising against load | Opposite input peg releases the non-load roller; negative stud face can take the load before the loaded roller overruns. This is a favorable force-sign sequence, not a validated full motion/contact trace. |
| Loaded lowering | Extracting the load-blocking roller either retains the high-friction jam or enters the finite unsupported/aiding branch above. Stop here. |
| Input held after release | Output could advance .02 rad = .072 mm at the rack before nominal rewedging, **if input stays fixed and rollers follow**. Not a guaranteed catch distance. |
| Axial input removal | Springs must traverse their actual compression; they do not instantly restore race contact. |
| Power loss mid-release | Motor holding torque disappears; input/output inertias and rewedging dynamics matter. Neither a stationary-input assumption nor an instantaneous ground bolt supplies a proven arrest. |

For input removal only, an isolated .5-g roller with the stated spring and fixed
output returns through .0875693 mm in **1.57080 ms** in the undamped, frictionless
quarter-cycle model. Stored spring work is .00191710 N·mm. This includes a finite
return instead of an ideal reset; it is not a stopping-time bound. Real friction
can prevent zero-preload reseating. No numerical allowed-drop criterion exists
in stage 02, so a nonzero arrest distance alone is not a product rejection; the
failed controlled-lowering/load-transfer claim is the decision here.

## Positive-stop and independent-head controls

Generate two copies of E-127's actual radius-3.4 collar/bolt section in separate
axial planes, offset by 15°. Full-insertion half-windows are **3.38885°** each;
they are disjoint. A 721-phase scan agrees with the continuous interval bound.
The nearest windows are separated by .143506 rad, equivalent to **.516622 mm**
rack travel. There is no state for the proposed B-fully-in-before-A-out sequence.
If both bolts are withdrawn to nose radius 3.5, each has .1-mm physical clearance
and neither supports. Partial edge catching is not modeled as full insertion or
as a guaranteed fall bound. Identical-phase collars permit parked overlap but
both must release for rotation. A moving load-bearing pallet would be a changed
mechanism, not a free addition to these fixed bolts. This rejects this sequencer,
not all escapements or positive load brakes.

Independent-head control: keep two opposing 4×10-mm pads **always touching each
head's local drive rack**, each with an assumed 100-N normal spring/reaction.
Positive gear/dog transfer remains in series. With mu=.1, each head holds 20 N,
so a 10-N load has 10-N static margin. Raising requires 30 N drive force; lowering
requires 10 N against drag; at 300 mm/s each moving head dissipates 6 W.
At mu=.05 it only equals the 10-N load; 20% shared preload loss reduces capacity
to 8 N and fails. A 160-head all-moving example dissipates 960 W at nominal drag.
These are conditional force/power calculations, not a schedule or thermal design.
Continuous contact avoids a closure interval, but stopping distance from motion,
dynamic friction, wear and dock retention remain unqualified. Local arrest avoids
one shared brake failure; it multiplies brake interfaces and does not remove the
friction dependence. No complete head is admitted.

## Manufacturing bounds, repeated obligations and decision

Use loads {1,3.27,10} N, wedge angles {3,5,8}°, and independent race/flat friction
{.05,.1,.3}: **81 deterministic scenarios, no probabilities**. Equal adverse
coefficients model common material/contamination; unequal coefficients model one
contact's defect. Flat-height biases {−.05,−.025,0,+.025,+.05} mm are explicit
bounds, not X1C priors. Common −.025 raises angle to 7.89858° and required zero-
preload mu to .0690374, failing .05; +.025 leaves **.0082567-mm radial interference**
even at the widest point. A common print/batch bias can affect both pockets and
many heads; independent-cell averaging is invalid. Roughness, warp, hole bias,
layer quantization, spring free length, wear and creep may change both geometry
and friction together. No distributions or yield estimates are justified.

Stationary inventory stays 6,400 racks, pinions, ground bolts/returns and docks
plus ≥12,800 bearing surfaces. Per active roller head: two rollers, four race/cam
interfaces, two spring/seat returns, two peg contacts, bilateral stud-slot fit,
input/output bearings and axial retention. The two-stop variant adds a collar,
guided bolt, return and release per site if local. Direct heads instead add each
motor/transmission, two pad contacts, preloads/reactions and wear adjustment.
Integral printing does not eliminate these fits, service or assembly obligations.

Readback must distinguish roller release, loaded ground seating and rack height;
input angle alone misses overrun. Refuse release on uncertain support. After a
mid-transfer fault there is no proven recovery arrest; false acceptance and common
sensor bias remain open, not cured by software.

Self-review checks assembled force/moment residuals against the independent
closed-form holding solution; exact circle/peg contact and slot-face clearance
at 257 input phases; actual cam-edge tangency at 64/256/1024 segments; and positive
stop windows at 256/1024/4096 segments. No dynamics convergence claim is made.

**Next principle:** return to E-126/A-024's fixed-datum **solid compression-length
storage**, specifically captive continuous pocket exchange with a moving support
pallet, against linked-feed control. It changes the load path from torque arrest
to supported material exchange. First construct one reversible loaded exchange
with simultaneous old/new support and an explicit input-loss state. Stop if it
requires E-126's rejected four stopped shuttle strokes or merely hides a rotary
no-back lock. This is an unresolved next question, not an admitted new candidate.
No complete schedule/BOM, purchase, printing or standing review is justified.
Reopen the present roller route only with a materially changed anti-overrun or
unloading topology that closes the demonstrated branch and preserves real return.
