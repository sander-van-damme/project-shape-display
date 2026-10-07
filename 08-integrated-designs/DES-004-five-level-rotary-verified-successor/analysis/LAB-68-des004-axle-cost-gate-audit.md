---
status: complete
builds-on: [DES-004]
---

# LAB-68: independent audit of the DES-004 axle cost gate

Date basis: 2026-10-06. This is an independent calculation and sourcing
review. No physical testing, purchase, or procurement approval was performed.

## Verdict

**CONDITIONAL PASS for continued candidate work; reject as a procurement or
production cost pass.** The intended scenario arithmetic is correct, but the
CSV is not safely machine-readable as an additive BOM, and the axle price,
fit, availability, freight, and manufacturing route remain unresolved.

## Recomputed checks

The DES-003 source BOM sums to $370.00 when `qty * unit_usd` is applied once
to its 17 purchased rows. The intended DES-004 calculations are:

```text
nominal       370 + 6400*0.020                         = 498
conservative  370 + 6400*0.050 + 320*0.050 + 9+12+2 = 729
```

The 5% stock quantity is 320 pins, making 6,720 ordered pins total. The
conservative axle purchase is therefore $336 at its stated allowance, not
$320; the CSV's separate $320 installed and $16 stock rows represent that
correctly. The nominal $498 total is inside the stated $400–500 last-resort
band. The conservative $729 total fails the stated $500 ceiling.

## Failed or weakened checks

1. **CSV additive-BOM check: failed.** `Nominal DES-004 purchased total` and
   `Conservative DES-004 purchased total` are ordinary rows with `qty=1` and
   `ext_usd` equal to the subtotal. Summing `ext_usd` by scenario produces
   $996 nominal and $1,458 conservative, double-counting the component rows.
   The intended totals can be reproduced only by special-casing the total-row
   text. Add a `row_type` field (for example `component`/`subtotal`) or move
   totals into a separate reconciliation table, then rerun the checker.

2. **Axle price gate: unresolved, and the conservative case is not viable at
   the quoted target.** The nominal ceiling is `(500-370)/6400 = $0.0203125`
   per delivered installed pin. The conservative ceiling including the three
   $23 service spares is `(500-370-23)/6720 = $0.0159226` per delivered axle,
   including freight and packaging. Both are below the cited retail examples;
   neither example proves that the required axle geometry is available.

3. **Supplier observation is time-sensitive.** The cited Grainger page
   identifies a 1 mm × 10 mm, 18-8 stainless press-fit pin, but its displayed
   $3.02 sale price is marked as ending 2026-09-02; the same page displays a
   $3.55 web price. This does not invalidate the retail-order illustration,
   but the $3.02 observation must be dated or replaced before reuse. The Zoro
   URL was not independently accessible in this audit; preserve an archived
   quote/screenshot or treat its price and tolerance as unverified.

4. **Fit and availability: unresolved.** DES-004 supplies no axle diameter,
   free length, engagement length, hole tolerance, bearing/retainer geometry,
   end treatment, or corrosion requirement. A 1 mm × 10 mm catalog pin is
   evidence of a product class only, not evidence of compatibility. A supplier
   quote must specify 6,720 pieces plus any sample quantity, delivered price,
   MOQ/stock, lead time, material/finish, diameter and cut-length tolerances,
   chamfer/debur condition, and packaging. The drawing-level fit check must
   follow that quote.

5. **Printed-part exclusion: accepted only as a scope boundary.** The $370,
   axle-only delta comparison excludes printed rotor/follower pairs, retainers,
   vane features, material, failed prints, print time, and assembly labor. This
   is internally consistent with a purchased-component cost gate, but it must
   not be presented as total build cost or a production estimate. Integral
   printed axles cannot substitute for metal pins without a changed reliability
   and manufacturing gate.

## Required follow-up

- Make the CSV unambiguously additive and rerun the arithmetic check.
- Obtain a delivered quote for 6,720 pins (plus separately priced samples if
  required) and retain dated evidence.
- Freeze the axle/rotor drawing dimensions and perform the fit/tolerance check.
- Keep the verdict conditional until quote, availability, and fit are closed;
  do not claim procurement approval or physical validation.

The parent cost conclusion is therefore endorsed only as **conditional pass for
continued candidate work**. The embedded BOM schema defect is a required
correction, but it does not change the intended $498 nominal or $729
conservative scenario totals.
