# Falsifier audit register — DND-115 A1 state-encoding shutter (DND-118)

- **Issue:** [DND-118](/DND/issues/DND-118) (Falsifier). Audits: [DND-115](/DND/issues/DND-115)
  (CTO). Parent: [DND-110](/DND/issues/DND-110). Model: [DND-113](/DND/issues/DND-113),
  target: [DND-114](/DND/issues/DND-114). Program: [DND-102](/DND/issues/DND-102).
- **Audited artifacts:** branch `cto/dnd115-state-encoding-shutter` @ `4a5c52c`;
  `08-integrated-designs/a1-reliability-first/scad/a1_binary_latch_cell.scad` (`shutter_crank`/`shutter_flap`);
  `08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py` (`shutter_read_contrast`,
  `shutter_tolerance_mc`); `07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md`;
  the CTO-authored `07-evidence-and-decisions/falsifier_dnd115_checks.py`.
- **Method:** independent recomputation from the placed CAD dimensions and first
  principles, in `falsifier_dnd115_a1_shutter_audit.py`. That file imports **nothing**
  from `a1_writer_rate.py` and does **not** trust `falsifier_dnd115_checks.py`; the
  CAD constants are hard-coded so no code path is shared. Default-deny: CLEAN only if
  every attack is PASS.
- **Evidence class: CALCULATION + CAD geometry only.** No print, no purchase, no
  measurement ([DND-27](/DND/issues/DND-27)). No board contact
  ([DND-32](/DND/issues/DND-32)). **Nothing here is a physical validation.**
- **Companion checker:** `python 07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py --gate`

## Verdical summary (default-deny)

| # | Attack | Verdict | Class |
|---|---|---|---|
| A1 | hidden-state full occlusion | **PASS** | geometry |
| A2 | visible-state full clearance (edge-on) | **PASS** | geometry |
| A3 | on/off return ratio >= 2x | **PASS** (7.72x) | calculation |
| A4 | reflective target frame-fixed (DeltaZ=0) | **PASS** | geometry |
| A5 | neighbour crosstalk is gated, not just reported | **FAIL** | modelling |
| A6 | neighbour up-cell top is truly "off-beam" | **FAIL** | modelling |
| A7 | "absorber in +/-1 mm DoF" is meaningful | **FAIL** | claim framing |
| A8 | swept envelope clears neighbour/own/aperture | **PASS** | geometry |
| A9 | tolerance stack-up structurally sound | **FAIL** (tautological aperture check) | method |
| A10 | states survive linkage angular tolerance | **PASS** (robust to +/-20 deg) | geometry |
| A11 | printability / min feature / watertight | **PASS** | CAD |
| A12 | claim-5 (1.0 mm standoff infeasible) reproduces | **PASS** | calculation |

**Verdict: NOT CLEAN.** The core decisive geometry reproduces independently, but four
attacks fail. Three are **modelling/claim-framing defects** (A5/A6/A7) and one is a
**method defect** (A9). None is a geometric collision. The consequence is a
**downgrade of two sub-claims**, not a falsification of the mechanism.

## What reproduces (the decisive numbers, independently recomputed)

All recomputed from `HINGE_X = BODY/2 + LATCH_T/2 + CLEAR = 2.225 mm`,
`FLAP_R = Z_SHUT_HINGE - (Z_VANE_TOP + SHUT_GAP + SHUT_T/2) = 2.03 mm`, and the
placed flap corners. **No number was taken from the CTO summary.**

- **Hidden occlusion: 100%.** Flat flap projects `1.405 mm` of the `1.405 mm` spot in X
  and `1.600 mm` in Y; coverage `1.000`. Confirmed at the *finite* cone too: the beam
  diameter at the flap plane (z=43.77, 1.03 mm below the aperture) is only `0.992 mm`,
  smaller than the `1.55 mm` flap width.
- **Visible clearance: 0%.** Edge-on plate projects `0.44 mm` (thickness) at
  x in [-0.025, 0.415], far off the read axis at x=2.225. Shadow `0.000`.
- **On/off ratio: 7.72x** (gate 2x). Reproduces the CTO number exactly from
  `bright = r_vane/g_aper^2`, `dark = r_flap/g_flap^2` with `r_vane=0.80`,
  `r_flap=0.05`, `g_aper=1.8`, `g_flap=1.25`.
- **Swept envelope: neighbour margin 0.280 mm, own-column margin 3.420 mm,
  aperture clearance 0.810 mm.** Matches the CAD echoes and the ADR.
- **Angular tolerance is good, not marginal.** Hidden coverage stays 1.000 for flap
  tilts 0–20 deg; the visible state stays clear for crank angles 90–75 deg. This is a
  genuinely robust result and *is* independent of the schematic linkage (see A-item 7).
- **Printability:** min shutter feature `0.44 mm` = 1 line @0.4 nozzle; committed
  `shutter.stl` watertight per `render_record.json`. **CAD-class evidence, not a print.**
- **Claim-5 reproduces.** Worst-case aperture clearance at the DND-115 gap (0.55):
  `S=1.0 -> -0.190 mm` (infeasible); `S=1.8 -> +0.610 mm` (feasible). The DND-115
  standoff revision is justified. (My added independent MC with an *aperture-placement*
  tolerance of ±0.10 and ±0.20 mm still passes: worst clearance +0.442 / +0.347 mm. The
  design is robust; see A9 for why the CTO MC did not demonstrate it.)

## Findings that fail

### A5 — neighbour crosstalk is *reported but not gated* (modelling defect)

`shutter_read_contrast()` computes `neighbour_crosstalk_ratio_upper_bound = 2.589x`
(the neighbour body's solid-angle term is **2.6x the vane term**), yet
`contrast_passes` depends only on `on_off_ratio`, `hidden_ok`, `visible_ok`. The
crosstalk number is printed and then never asserted. A margin that is >1x the signal
and is not part of the gate is not a margin. **This is the same class of defect that
DND-112 found in DND-111** (a number computed and then not carried into the verdict).

### A6 — the neighbour up-cell top is *not* "off-beam" (modelling defect)

The ADR §3 and the model verdict claim "the neighbour top is >= 4 mm below the
aperture plane and **off-beam**". This is **false for the illumination/detection cone.**
The reader is a coaxial 15 deg aperture at `z=44.8`. At the neighbour-top plane
(`z=40`, 4.8 mm below the aperture) the cone radius is `4.8·tan15° = 1.286 mm`. The
neighbour near edge is at `x=3.28`, i.e. `1.055 mm` from the read axis — **inside the
cone by 0.231 mm.** So a bright (up) neighbour top contributes a **state-invariant**
return.

How large? The neighbour occupies `0.231 mm²` of the cone at `g=4.8 mm`
(`4.4%` of the cone), giving a return term of `~0.008` vs the vane term `0.174`
(≈4.6%). Adding it to *both* states drops the on/off ratio from `7.72x` to `6.37x` —
**still above the 2x gate**. So A6 does **not** break the gate, but it **falsifies the
"off-beam" wording** and shows the crosstalk accounting is incomplete. The correct
statement is: "the neighbour is weakly in-cone (≈5% of the vane return in the clear
state) and state-invariant; the gate survives with margin."

### A7 — "absorber DeltaZ 0.55 mm inside ±1 mm DoF" is vacuous (claim framing)

The ±1 mm DoF budget (DND-112) exists for the **reflective target's** z, because the
target z set the read standoff. Here the **target is the frame-fixed vane (DeltaZ = 0)**;
the moving object is the **absorber**, whose z only enters the negligible flap term
`r_flap/g²`. The absorber term is `0.032` vs the vane term `0.247` (**7.7x smaller**).
Moving the absorber 0.55 mm — or 55 mm — barely changes the contrast. So the
"absorber inside the ±1 mm DoF" check certifies nothing. It is harmless but must not be
counted as evidence; the real statements are "the target is frame-fixed" and "the flap
is a dark absorber."

### A9 — the Monte Carlo stack-up is structurally tautological (method defect)

`shutter_tolerance_mc()` perturbs the vane top `vt`, the gap `g2`, and the flap
thickness, but sets the aperture plane to the **nominal** value
`aper = (TRAVEL+3.0) + SHUT_APER_GAP`. The `aperture_clearance` check is therefore
`aper_nominal - (vt_perturbed + g2 + tt)`, which can only fail if the *vane* moves up —
it **never** models a reader/aperture placement error against the vane. As written the
check cannot demonstrate what it claims to demonstrate. Re-running with an explicit
aperture-plane tolerance (±0.10 / ±0.20 mm) still passes (worst +0.442 / +0.347 mm), so
the **design** survives; the **method** does not yet show it. This is a required fix
before any tolerance claim is cited downstream.

## Item 7 (schematic linkage) — assessed

The shutter crank is drawn as a bare hinge pin; the linkage from the toe arm to the
flap is not modelled. **Are the flap/sweep claims independent of that linkage?** Mostly
yes, with one dependency:

- The **hidden** and **visible** states are *positions*, not force paths. A1–A3, A8 and
  A10 depend only on the flap reaching a bounded set of angles, and A10 shows a very
  wide angular tolerance (±20 deg hidden, ±25 deg visible). So a linkage that stops the
  flap anywhere within that band preserves the read contrast.
- The **dependency** is the over-centre stop force and the *ratio* `k =
  swing_flap/swing_arm`. If `k` has variance, the flap can stop short of flat. A10 shows
  this is extremely forgiving, so the *read* survives a sloppy linkage. But the linkage
  must still (a) produce a hard stop at both ends and (b) not add friction/wear that
  stalls the latch toggle. Those are **not** decidable from CAD and are **measurement-only**
  (DND-27). They belong on the coupon handoff, not in a CAD-closure claim.

**Conclusion on item 7:** the flap+sweep read claims are independent of the unmodelled
linkage *geometry* (because of the wide angular margin), but the linkage's *force,
friction and fatigue* behaviour is unmodelled and remains a physical-only residual. The
DND-115 ADR should say "linkage schematic; read contrast is coupling-independent within
±20 deg; linkage force/friction/wear is measurement-only."

## Evidence classification (what is settled vs not)

| Claim | Class | Status |
|---|---|---|
| Hidden/visible coverage, sweep, clearances | CAD + calc | **Independently reproduced** |
| On/off 7.72x | calc | reproduced (assumption-class optical constants) |
| Target frame-fixed, DeltaZ=0 | CAD geometry | reproduced (by construction) |
| 1.8 mm standoff justified | calc | reproduced, robust to aperture ±0.20 mm |
| Angular tolerance of states | calc | reproduced (wide margin) |
| Min feature / watertight | CAD | reproduced (STL record) |
| **Neighbour crosstalk "off-beam"** | modelling | **falsified as written**; gate survives at 6.37x |
| **Crosstalk gated in verdict** | modelling | **missing** |
| **Absorber DoF meaningful** | claim framing | **vacuous** |
| **MC aperture path** | method | **tautological; design OK, method not** |
| Flap reflectance 0.05, aperture 0.44, LED/PD constants | assumption | unmeasured |
| Linkage force/friction/wear, 6,400-cycle fatigue | measurement-only | not decidable here |

## Verdict

**The DND-115 mechanism survives independent adversarial recomputation.** The decisive
geometry — 100% hidden occlusion, 0% visible shadow, 7.72x on/off, frame-fixed target,
0.28 mm neighbour sweep, 0.81 mm aperture clearance, 1.8 mm standoff justification — all
reproduce from the placed CAD and first principles, with no collision and a wide angular
margin. **But the closure statement is over-claimed:** the "off-beam neighbour" wording
is false (weakly in-cone, state-invariant, gate survives at 6.37x), the crosstalk number
is not gated, the "absorber in DoF" check is vacuous, and the MC can never fail its
aperture check. These must be corrected/downgraded in the ADR and in
`a1_writer_rate.py` before the read axis is called "closed" on this basis. The residual
remains **assumption-class optical constants** and **measurement-only wear/force**, per
DND-27.

**Recommended disposition:** READ AXIS CLOSED AT CAD + CALCULATION *with corrected
claim framing*; open a CTO correction task for A5/A6/A7/A9 wording (no geometry change).
No physical coupon is justified by this audit alone; a coupon is justified only to
retire the measurement-only linkage/reflection residuals if the program decides to.

## Next test (if a coupon is ever authorised)

Single-cell A1 coupon (1 printed cell + frame vane + shutter + one LED/PD pair):
measure actual on/off return ratio with the real printed flap and a real aperture at
1.8 mm; assert >= 2x. This is the cheapest experiment that can **falsify** the
assumption-class reflectance/geometry combination. It requires a print and optical
hardware — **a physical handoff, not agent-reachable** (DND-27).
