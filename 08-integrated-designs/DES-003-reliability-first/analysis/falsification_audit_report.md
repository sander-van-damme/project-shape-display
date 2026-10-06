# Falsification audit: DES-003

Evidence is calculation, CAD-derived geometry and assumptions only. There is no physical validation.

## Corrected findings

| Claim | Disposition | Evidence and correction |
|---|---|---|
| Five-level terrain capability | **Fail as drawn** | The placed latch has only 0 and 40 mm states. The analyses use a five-level 0/10/20/30/40 mm workload, so the three intermediate levels are absent. |
| Eight-head purchased cost | **Lower bound: $370** | `bom_a1.csv` totals $370, or $429.20 after the repository's 1.16 delivery uplift. The former $181 claim counted one writer, prong and reader despite requiring eight. Driver count, power sizing and loom detail remain unresolved, so $370 is not a complete quote. |
| Full-map time below 30 s | **Conditional calculation** | The model gives 18.278 s with eight heads at the assumed 1.0 m/s traverse. Toggle force/speed, registration, settling and miss rate are unmeasured. |
| Latch excursion fits its half-lane | **Nominal pass; worst-case fail** | Nominal excursion is 0.65 mm in a 0.74 mm lane (+0.09 mm). `a1_hardening.py` gives a -0.11 mm worst-case tolerance margin, so the old “validated” label was incorrect. |
| Printable on X1C | **Unresolved** | Several 0.44–0.45 mm features sit at the assumed process floor; the 1 mm printed hinge pin fails the 5 mm sourced pin rule. Bed fit of coupon/segment geometry does not establish mechanism printability. |
| Optical classification | **Open** | The photometric model predicts 7.72× on/off return, but reflectance, lighting, alignment and wear are unmeasured. |
| Regional isolation | **Open** | CAD establishes geometric separation only. Effective stiffness, coupling, peak neighbour displacement and residual displacement are unmeasured. The 0.10 mm value is a proposed test gate, not a product requirement. |
| Snap-force gate | **Corrected: mean must be at most 7.14 N** | With a 10 N usable writer and 40% assumed spread, the mean limit is `10 / 1.4 = 7.14 N`; any snap above 10 N is also a rejection. The former report reversed this inequality. |
| Full display fits the X1C bed | **Fail monolithically; modular only** | The field is 406.4 mm, larger than the 256 mm bed. The 210 mm figure applies to coupon-C rail segments, not the full span. |

## Promotion blockers

DES-003 must not be treated as a qualified product baseline until a five-level mechanism is defined and the following are closed: complete eight-head electrical/BOM reconciliation; worst-case fit coupon; loaded snap-force and life measurements; optical confusion testing; full-span registration; and loaded regional-disturbance measurements. Readback reduces silent-error risk but does not validate the mechanics or sensing.

## Reproduction

Run from the repository root:

```sh
python3 08-integrated-designs/DES-003-reliability-first/analysis/reliability_mask_checks.py
python3 08-integrated-designs/DES-003-reliability-first/analysis/a1_promotion_cost.py --gate
python3 08-integrated-designs/DES-003-reliability-first/analysis/a1_coupon_readiness.py --gate
python3 08-integrated-designs/DES-003-reliability-first/analysis/a1_hardening.py --gate
```
