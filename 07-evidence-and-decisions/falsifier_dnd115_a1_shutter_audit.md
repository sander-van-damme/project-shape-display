# Falsifier audit register — DND-115 A1 state-encoding shutter (DND-118)

- **Issue:** [DND-118](/DND/issues/DND-118) (Falsifier). Audits: [DND-115](/DND/issues/DND-115)
  (CTO). Parent: [DND-110](/DND/issues/DND-110). Model: [DND-113](/DND/issues/DND-113),
  target: [DND-114](/DND/issues/DND-114). Program: [DND-102](/DND/issues/DND-102).
  Corrections: [DND-121](/DND/issues/DND-121) (CTO).
- **Audited artifacts (first pass):** branch `cto/dnd115-state-encoding-shutter` @ `4a5c52c`;
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

**DND-121 status:** the four modelling/claim-framing defects found in the first pass
(A5/A6/A7/A9) were corrected in the ADR and model by [DND-121](/DND/issues/DND-121).
This register now asserts the corrected state; the verdict is CLEAN against the
corrected artifacts. The core geometry (A1–A4, A8, A10–A12) is unchanged.

| # | Attack | Verdict | Class |
|---|---|---|---|
| A1 | hidden-state full occlusion | **PASS** | geometry |
| A2 | visible-state full clearance (edge-on) | **PASS** | geometry |
| A3 | on/off return ratio >= 2x | **PASS** (7.72x ideal; 7.41x with in-cone crosstalk) | calculation |
| A4 | reflective target frame-fixed (DeltaZ=0) | **PASS** | geometry |
| A5 | neighbour crosstalk is gated, not just reported | **PASS** (DND-121) | modelling |
| A6 | neighbour up-cell top correctly stated as weakly in-cone | **PASS** (DND-121) | modelling |
| A7 | "absorber in +/-1 mm DoF" claim dropped as vacuous | **PASS** (DND-121) | claim framing |
| A8 | swept envelope clears neighbour/own/aperture | **PASS** | geometry |
| A9 | tolerance stack-up structurally sound | **PASS** (DND-121) | method |
| A10 | states survive linkage angular tolerance | **PASS** (robust to +/-20 deg) | geometry |
| A11 | printability / min feature / watertight | **PASS** | CAD |
| A12 | claim-5 (1.0 mm standoff infeasible) reproduces | **PASS** | calculation |

**Verdict: CLEAN** against the corrected DND-121 artifacts. The core decisive
geometry reproduces independently, and the four corrections are independently
re-verified: the crosstalk term is now added to both states and gated (A5), the
"off-beam" wording is replaced by the correct weakly-in-cone statement (A6, the
neighbour is inside the cone by 0.231 mm and contributes a state-invariant
~4.45% of the cone), the vacuous absorber-DoF claim is removed (A7), and the MC
models the aperture plane as its own frame feature so the clearance check can
genuinely fail (A9; it still passes at ±0.10 mm → worst +0.441 mm).

### DND-121 correction to the on/off number (audit arithmetic, A3/A5/A6)

The first-pass audit quoted **6.37×**, but that number was not internally
consistent with the audit's own geometric term: a "4.6% of the vane return"
divisor gives **2.89×**, and the quoted `0.008` term implies a `0.184 mm²` in-cone
area — ~8× the `0.231 mm²` strip it cited. Recomputing **geometrically** (overlap
of the neighbour footprint with the 1.286 mm cone disc at the neighbour-top plane)
gives an in-cone fraction of **4.45%**, a term of **0.00154**, and an on/off ratio of
**7.41×** — still far above the 2× gate. DND-121 uses the geometrically consistent
7.41×. The audit's qualitative conclusion is unchanged (crosstalk is small,
state-invariant, and the gate survives with margin); only the number is corrected.

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
- **On/off ratio: 7.72x ideal; 7.41x** with the state-invariant in-cone neighbour term
  (gate 2x). Reproduces the CTO bright/dark terms from `bright = r_vane/g_aper^2`,
  `dark = r_flap/g_flap^2` with `r_vane=0.80`, `r_flap=0.05`, `g_aper=1.8`, `g_flap=0.80`.
- **Swept envelope: neighbour margin 0.280 mm, own-column margin 3.420 mm,
  aperture clearance 0.810 mm.** Matches the CAD echoes and the ADR.
- **Angular tolerance is good, not marginal.** Hidden coverage stays 1.000 for flap
  tilts 0–20 deg; the visible state stays clear for crank angles 90–75 deg. This is a
  genuinely robust result and *is* independent of the schematic linkage (see A-item 7).
- **Printability:** min shutter feature `0.44 mm` = 1 line @0.4 nozzle; committed
  `shutter.stl` watertight per `render_record.json`. **CAD-class evidence, not a print.**
- **Claim-5 reproduces.** Worst-case aperture clearance at the DND-115 gap (0.55):
  `S=1.0 -> -0.190 mm` (infeasible); `S=1.8 -> +0.610 mm` (feasible). The DND-115
  standoff revision is justified. (The independent MC with an *aperture-placement*
  tolerance of ±0.10 and ±0.20 mm still passes: worst clearance **+0.422 / +0.322 mm**.
  The design is robust; the pre-DND-121 CTO MC did not demonstrate it — see A9.)

## Findings that were corrected in DND-121

### A5 — neighbour crosstalk is now *gated* (was: reported but not gated)

`shutter_read_contrast()` now adds the state-invariant in-cone neighbour term to
**both** states of the on/off ratio, and `contrast_passes` depends on that
worst-case ratio. The old solid-angle upper bound (`2.589x`) that was printed and
never asserted is replaced by the geometric term. A margin that is computed is now
a margin that is gated. This closes the DND-112/DND-111 defect class.

### A6 — the neighbour up-cell top is *weakly in-cone*, not "off-beam" (corrected)

The reader is a coaxial 15 deg aperture at `z=44.8`. At the neighbour-top plane
(`z=40`, 4.8 mm below the aperture) the cone radius is `4.8·tan15° = 1.286 mm`. The
neighbour near edge is at `x=3.28`, i.e. `1.055 mm` from the read axis — **inside the
cone by 0.231 mm**. The ADR no longer states "off-beam". A bright (up) neighbour top
contributes a **state-invariant** return of ~**4.45% of the cone** (term `0.00154` vs
the vane term `0.24691`). Adding it to *both* states drops the on/off ratio from
`7.72x` to `7.41x` — **still far above the 2x gate**.

### A7 — "absorber DeltaZ 0.55 mm inside ±1 mm DoF" is dropped (corrected)

The ±1 mm DoF budget exists for a **reflective target's** z. Here the target is the
frame-fixed vane (DeltaZ = 0); the moving object is the **absorber**, whose z only
enters the negligible flap term (`rho/g²`), `0.032` vs the vane term `0.247`
(**7.7x smaller**). DND-121 removes the "absorber inside the DoF" check as vacuous
and states the two real facts instead: **the target is frame-fixed** and **the flap
is a dark absorber**.

### A9 — the Monte Carlo stack-up models the aperture as its own feature (corrected)

`shutter_tolerance_mc()` now samples an explicit **aperture-placement tolerance**
(the reader head is a separate frame component) about the aperture's absolute z,
instead of pinning it to the nominal vane top. The `aperture_clearance` check can
now genuinely fail. It still passes: worst clearance **+0.441 mm** at ±0.10 mm and
**+0.355 mm** at ±0.20 mm. The **design** survives *and* the **method** now shows it.

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
| On/off 7.72x ideal / 7.41x with in-cone crosstalk | calc | reproduced (assumption-class optical constants) |
| Target frame-fixed, DeltaZ=0 | CAD geometry | reproduced (by construction) |
| 1.8 mm standoff justified | calc | reproduced, robust to aperture ±0.20 mm |
| Angular tolerance of states | calc | reproduced (wide margin) |
| Min feature / watertight | CAD | reproduced (STL record) |
| **Neighbour crosstalk** | modelling | **gated in `contrast_passes`** (DND-121) |
| **Neighbour top in-cone** | modelling | **corrected: weakly in-cone, state-invariant** (DND-121) |
| **Absorber DoF** | claim framing | **claim dropped** (DND-121) |
| **MC aperture path** | method | **non-tautological; aperture its own feature** (DND-121) |
| Flap reflectance 0.05, aperture 0.44, LED/PD constants | assumption | unmeasured |
| Linkage force/friction/wear, 6,400-cycle fatigue | measurement-only | not decidable here |

## Verdict

**The DND-115 mechanism survives independent adversarial recomputation.** The decisive
geometry — 100% hidden occlusion, 0% visible shadow, 7.72x ideal / 7.41x crosstalk-
included on/off, frame-fixed target, 0.28 mm neighbour sweep, 0.81 mm aperture
clearance, 1.8 mm standoff justification — all reproduce from the placed CAD and first
principles, with no collision and a wide angular margin. The four over-claimed /
structurally weak statements the first pass flagged (A5/A6/A7/A9) were corrected in the
ADR and model by [DND-121](/DND/issues/DND-121) and are re-verified here as PASS on the
corrected artifacts. The residual remains **assumption-class optical constants** and
**measurement-only wear/force**, per DND-27.

**Disposition:** READ AXIS CLOSED AT CAD + CALCULATION *with corrected claim framing*;
the audit CI step is promoted from report to `--gate` now that the corrections have
landed. No physical coupon is justified by this audit alone; a coupon is justified only
to retire the measurement-only linkage/reflection residuals if the program decides to.

## Next test (if a coupon is ever authorised)

Single-cell A1 coupon (1 printed cell + frame vane + shutter + one LED/PD pair):
measure actual on/off return ratio with the real printed flap and a real aperture at
1.8 mm; assert >= 2x. This is the cheapest experiment that can **falsify** the
assumption-class reflectance/geometry combination. It requires a print and optical
hardware — **a physical handoff, not agent-reachable** (DND-27).
