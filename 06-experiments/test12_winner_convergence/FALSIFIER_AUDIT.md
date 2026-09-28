# DND-46 - Adversarial audit of the DND-44 S5 readiness closure

**Question.** [DND-44](/DND/issues/DND-44) closed or bounded K1/K5/K6/K8/K10/K11
analytically. [DND-46](/DND/issues/DND-46) asks the Falsifier to *break* those
closures before the CTO writes a readiness verdict - to find the flaw that makes a
claimed closure false, not to agree.

**Evidence class.** CALCULATION / adversarial audit. No print, no measurement
([DND-27](/DND/issues/DND-27)). Every counter-number here is arithmetic over the
repo's own parameters and the closure modules' own inputs.

**Method.** Read all four `*_closure.py` modules and their `*_checks.py`, plus
`model.py`, `checks.py`, `test08/params.json`, `test09/params.json`,
`test08/analysis.py`, `test09/analyze.py` and `bom_S5_delivered.csv`. Re-derived
each closure's inputs independently and attacked the claimed result with the
strongest counter-calculation. Encoded every attack as a failing-if-wrong gate in
[`falsifier_checks.py`](falsifier_checks.py) (19 tests, CI-runnable).

## Verdict summary

| Killer | Claimed by DND-44 | Falsifier verdict | Strongest counter-argument |
|---|---|---|---|
| **K6** timing | "not a rate problem"; floor 18.65 s; ~268 pps meets 30 s | **CONFIRMED-WITH-CAVEAT** | The floor arithmetic is real and cross-checked. But the boundary is a *dwell assumption*, and ~268 pps is ~804 rpm - an unmeasured loaded speed. The 26.25 s pass also assumes **zero inspection time**. |
| **K1** buckling | service load <= 0.39 N/column, 12.7x margin | **BROKEN** | The base-distribution argument assumes the base rests on *all* columns beneath it. On a height-varying field a rigid base is a three-point contact: 1 kg loads a column at **~3.27 N**, not 0.39 N. Margin ~1.5x, not 12.7x. |
| **K5/K7** cost | machine-preserving path $424.95, $75 margin | **BROKEN AS STATED** | The $75 margin needs four simultaneous best-case choices. Restore spares and the four bundled lines to `unit_expected` and the margin is **$17.05**; at the *sourced* DRV8833PWPR it is **$25.09**; with an expected motor it is **over $500**. |
| **K8** lateral | guide carries lateral; 1 N -> 0.01 mm; limit ~9.4 N | **BROKEN** | The 12 mm free length is hard-coded in `__main__` with no geometry basis. The repo's own `unrelieved_upper_body_length_mm = 40 mm`; at 40 mm a 1 N lateral load deflects **0.356 mm** - 3.5x the 0.10 mm gate. |
| **K10** regional | bounded; 1 row 3.9 s ... 80 rows 24.7 s | **CONFIRMED** | The bound is complete and monotonic. Caveat only: it shows regional time is set by the mandatory full platen stroke (~3.6 s fixed), not region size. |
| **K11** cycle life | ~1e8 cycles (order-of-magnitude) | **PSEUDO-QUANTITATIVE** | The point estimate 9.98e7 rests on two asserted constants. A conservative FDM endurance (0.2 % vs 0.3 %) drops it **25x** to ~3.9e6. Report as ">1e6, order unknown", not a number. |

## 1. K6 - timing (CONFIRMED-WITH-CAVEAT)

**What is right.** `full_map_s` reproduces `test09/analyze.schedule()` to 3.6e-15 s
at the design point, the rate-independent floor is a genuine lower bound (confirmed
`full_map_s(1e9) -> floor`), and the worst corner (45.07 s) truly cannot be
recovered by step rate because its floor (34.47 s) already exceeds 30 s. That part
of the closure withstands attack.

**Strongest counter-argument.** "Not a rate problem" is a **framing change, not a
closure.** The pass/fail boundary sits exactly on two *assumed*, unmeasured
quantities:

1. **The rate is still an unmeasured mechanical speed.** The required rate for 30 s
   is 267.9 pps. At 18 deg/step that is **804 rpm**; the design point of 400 pps is
   **1200 rpm**. The repo itself records "no loaded torque-speed curve"
   (`test11_falsification_library/make_register.py:205`) and `test08` only asserts a
   `running_torque_target_nm = 0.00015`. "Only ~268 pps" without a pull-out curve
   for an 8 mm PM stepper at 804 rpm is the same unverified claim the sweep exposed,
   just smaller.
2. **The 26.25 s pass assumes `inspection_s = 0`.** A full-map reconfiguration that
   verifies its own result pays an inspection pass; the sweep's own grid includes
   3 s. At `inspection_s = 3` the design point is 29.25 s - it still meets the hard
   30 s cap but **misses the 27 s engineering target**, with 0.75 s margin.

**Minimal residual to keep.** K6 is conditional on **two** unmeasured quantities: the
realised loaded engage/settle dwell (the module's own lever) **and** a loaded
>=268 pps / ~804 rpm torque-speed point. Reword "not a rate problem" to "the rate
term is small *if* 268 pps is available; the binding uncertainty is the dwell."

## 2. K1 - buckling (BROKEN)

**Claim.** A miniature's base spreads its weight over N columns; even 1 kg on a
25.4 mm base gives 0.39 N/column (12.7x margin vs the 4.96 N core).

**Two independent flaws.**

1. **Column overcount.** `columns_under_base` returns `ceil(d/pitch)^2 = 25` for a
   25.4 mm base. The circular footprint is `pi(12.7)^2/5.08^2 = 19.6` cells.
   Returning 25 raises the divisor and lowers the reported per-column load - the
   "conservative worst case" is conservative in the wrong direction.
2. **The distribution premise is invalid (decisive).** The argument is only true if
   the base conforms to, and rests on, *every* column top beneath it. A shape
   display's defining property is that the column tops are at **different heights**.
   A rigid miniature base therefore stands on the **highest three** columns (a
   three-point contact), not all 25:

   | support model | per-column load, 1 kg miniature | vs 4.96 N core |
   |---|---:|---:|
   | distributed over 25 (claimed) | 0.392 N | 7.9 % (12.7x margin) |
   | circular area, ~19.6 cells | 0.500 N | 10.1 % |
   | **rigid 3-point contact (real)** | **3.270 N** | **65.9 % (1.5x margin)** |

   At a 1.5x margin the *service* case is no longer comfortably closed, and the
   `assumption_was_conservative = True` honesty gate is false: the 1 N working
   assumption was *not* conservative relative to a 3.27 N three-point service load.

**Minimal residual to keep.** K1-service is **not** bounded; it lies between 0.39 N
(conforming base) and 3.27 N (rigid tripod). The exact quantity is the **real base
contact** (soft vs rigid base). Either size the core for the tripod case or source a
base-compliance argument. The localized 5 N abuse case remains open as stated; the
1.10 mm core re-size is a real geometry trade (step height 0.5 -> 0.4 mm) on top of
the open K9 margin, not a free fix.

## 3. K5/K7 - cost (BROKEN AS STATED)

**Claim.** A machine-preserving path lands at $424.95 delivered, $75.05 under the
ceiling; K7 (motor) is the single residual.

**Strongest counter-argument.** The $75 margin is the product of **four** best-case
choices stacked at once. Remove any one and the margin collapses:

| Variant | Parts | Delivered | Margin |
|---|---:|---:|---:|
| Closure as published | $366.34 | **$424.95** | $75.05 |
| E6 removed (bundled lines at `unit_expected`) | $401.34 | $465.55 | $34.45 |
| Spares allowance kept (E5 removed) | $381.34 | $442.35 | $57.65 |
| **E5 + E6 removed** | $416.34 | **$482.95** | **$17.05** |
| Driver = *sourced* DRV8833PWPR $1.3338 (E1 weakened) | $409.40 | $474.91 | $25.09 |
| **E5 + E6 + expected motor $1.25** | $432.34 | **$501.51** | **-$1.51 (over)** |

Specific attacks the issue names, confirmed:

- **E6 is best-case repricing, not sourcing.** E6 sets four *bundled structural*
  lines - guide rods, belts, head shafts, fasteners - to their own `unit_best_usd`
  ($25/$12/$12/$8). The BOM's `unit_expected_usd` ($40/$20/$20/$12) exists precisely
  because these are bundled allowances that ship above the best single listing. E6
  is $35 of the $144 total reduction and consumes the *entire* best-to-expected gap
  on lines with no machine change. That is exactly "quietly assume best-case for
  pinned lines."
- **The driver swap is legitimate in kind but best-case in price.** Both the BOM
  line and TB6612FNG are dual H-bridges driving one bipolar stepper, so the
  substitution preserves the machine. But $0.7955 is the @100 LCSC price; the repo's
  *other* sourced driver (DRV8833PWPR C50506) is $1.3338, and using it costs $43
  more. The headline relies on the cheapest of two sourced options.
- **Deleting spares (E5) is arguable, not free.** It is debatable that spares are
  "not part of the machine definition"; a build needs some replacement stock.
  Restoring $15 removes 20 % of the claimed margin.

**Minimal residual to keep.** K5 is **not** "$424.95 with $75 margin". It is
**"$424.95 at four simultaneous best cases; $482.95 with a defensible bundled-price
and spares basis; over $500 if the motor is at its expected $1.25."** The binding
residual is stronger than "K7": it is **K7 + the best-case-pricing basis of E5/E6**.
Use the robust figure ($482.95) as the planning number.

## 4. K8 - lateral holding (BROKEN)

**Claim.** Lateral load is carried by the column body against its guide and its
free-length bending; a 1 N lateral load deflects ~0.01 mm (< 0.10 mm gate); the
governing limit is ~9.4 N guide shear.

**Decisive counter-argument.** The deflection scales as `L^3`, so the entire result
is set by the assumed free length. `cross_cutting_closure.py` hard-codes
`free = 12.0` in `__main__` ("Test09 geometry gives ... ~12 mm apart at the top" - an
un-cited assertion). The repo's **own** `test08/params.json` / `analysis.py` report
`unrelieved_upper_body_length_mm = body_length - body_relief_height = 80.2 - 40.2 =
40 mm`; `test08/README.md:142` states the 80.2 mm body was chosen so a "full 40 mm
square upper segment hides this relief". The free cantilever above the guide is
therefore **40 mm at full extension**, not 12 mm:

| free length | force for 0.10 mm gate | deflection at 1 N | passes 0.10 mm gate? |
|---:|---:|---:|---|
| 12 mm (hard-coded) | 10.41 N | 0.0096 mm | yes |
| 20 mm | 2.25 N | 0.045 mm | yes |
| **40 mm (repo geometry)** | **0.281 N** | **0.356 mm** | **no** |

At the real free length the closure's "governing limit ~9.4 N" is wrong by ~33x, and
a 1 N lateral knock (the Test08 protocol load) exceeds the 0.10 mm neighbour gate by
3.5x. The companion `guide_shear_allowable` is also an unsourced
`0.5 MPa x 18.72 mm^2 = 9.36 N`; changing that constant moves the answer, so the
reported limit is set by a chosen number, not by the mechanism.

**Minimal residual to keep.** K8 is **open and worse than before**: the lateral gate
is exceeded by the repo's own protocol load at the column's extended positions. The
exact quantity to settle is the **free length vs height** (guide capture length and
tier geometry) plus the printed guide-wall shear strength. A single free-length /
guide-capture coupon answers it.

## 5. K10 - regional time (CONFIRMED, with a framing note)

The bound is complete, monotonic and includes reference + full 41 mm stroke + ready.
Confirmed. One framing caveat: a one-row update is 3.93 s, of which the fixed
platen/reference/ready overhead is 3.59 s (91 %). "Regional updates are fast" is
really "the mandatory full platen stroke sets the floor"; region size adds only
~1 s per 5 rows. A product truth to state, not a closure failure.

## 6. K11 - cycle life (PSEUDO-QUANTITATIVE)

`estimated_cycles_to_failure = 99,774,552` is a false-precision point estimate. It
is `(eps_endurance/eps)^m x 1e6` with **two asserted constants**: eps_endurance =
0.3 % and Basquin m = 8. The strain (0.169 %) is calculated; the two constants are
not sourced to FDM PLA.

| eps_endurance | m | cycles |
|---:|---:|---:|
| 0.30 % | 8 | 9.98e7 (published) |
| 0.20 % | 8 | 3.89e6 |
| 0.15 % | 8 | 3.90e5 |
| 0.30 % | 12 | 9.97e8 |

A conservative FDM endurance (0.2 %) drops the bound 25x. **Minimal residual:** the
honest statement is **">=1e6 cycles is plausible; the bound spans 4e5-1e9 across
defensible FDM constants."** For context the number is not the product-life driver: a
full map cycles each detent once per row (~80x), so 1e6 detent cycles is ~12.5k full
maps. The real risk is creep and layer adhesion, not high-cycle fatigue.

## 7. Attacks that failed (recorded as evidence)

- **K6 closed-form arithmetic** - could not break it; reproduces
  `test09/analyze.schedule()` to 1e-15 s and the floor is a true bound.
- **K10 completeness** - the bound correctly includes the full stroke; no missing
  term found.
- **E1 driver substitution** - electrically sound in kind (dual H-bridge for dual
  H-bridge); the attack is on its *price* basis, not its topology.
- **K1 core re-size trend** - critical load genuinely rises with core radius in the
  repo's own model; the attack is that it costs toe step height, not that the model
  is wrong.

## 8. Residuals that survive attack (for the final readiness register)

| id | Residual | Exact quantity needed |
|---|---|---|
| K1-service | **BROKEN**: service load is 0.39-3.27 N/column depending on base contact | base contact model (conforming vs tripod) or a core sized for 3.3 N |
| K1-abuse | localized 5 N point load | printed core crush/shear at the toe |
| K5-basis | **BROKEN**: margin $17-$75 depending on spares/E6 basis | a sourcing quote for the four bundled lines and a spares policy |
| K7 | matched <=$1.86 motor, or <=$1.23 with E5+E6 restored | purchase+sample one lot; verify step angle/winding/torque |
| K6-rate | loaded torque-speed point at >=268 pps (~804 rpm) | a pull-out/torque-speed curve for the 8 mm 18 deg PM stepper |
| K6-dwell | realised loaded engage/settle dwell (25/15 ms assumed) | one loaded row-cycle timing measurement |
| K8-free | **BROKEN**: free length at extension (12 vs 40 mm) | guide-capture length/tier geometry or a free-length coupon |
| K8-shear | printed guide-wall shear strength | printed guide shear test at the 0.10 mm gate |
| K9 | angular margin under +/-0.05 mm tolerance | as-printed rotor radius/core offset (delegated [DND-45](/DND/issues/DND-45)) |
| K11-span | cycle bound 4e5-1e9 across FDM constants | printed-leaf creep/fatigue coupon |
| R1 | per-cell error q (P(all correct) at q=1e-4 is 52.7 %) | counted coupon failures; q <= 1.57e-6 for 99 % |
| R2 | 40 mm travel vs a real miniature | one measured representative miniature height |

## 9. Bottom line for the readiness verdict

Three of the six claimed closures (K1, K5, K8) are **broken** as published; one (K6)
is a **reframing** that quietly substitutes a dwell assumption for the rate question;
one (K11) is a **pseudo-quantitative point estimate**; and only K10 is a clean
analytic bound. None of this kills S5 - the architecture survives - but the
readiness statement must not carry the DND-44 closure headlines as written. The
robust planning figures are: **cost $482.95 (not $424.95)**, **service buckling load
up to 3.27 N (not 0.39 N)**, **lateral gate exceeded at extension (not 0.01 mm at
1 N)**, **time conditional on a dwell AND a >=268 pps loaded rate**, and **cycle
life ">=1e6, order unknown"**.

Run the attacks: `python 06-experiments/test12_winner_convergence/falsifier_checks.py`
