---
status: complete
builds-on: [DES-004, ADR-005, E-012]
---

# E-013: DES-004 axle-pin sourcing and fit screen

## Disposition

**UNRESOLVED against both cost gates; fit not released.** Public catalogue
observations checked on 2026-10-07 are materially above the gates before
freight/tax, and no source supplies a delivered 6,720-piece quote plus
drawing-level end-treatment evidence. This is a sourcing and analytical
screen only: no purchase, production commitment, or physical validation
follows.

## Quantity and gates

DES-004 requires 6,400 installed pins plus 5% stock = **6,720 delivered
pieces**. Using the ADR-005 retained purchased baseline of $370 and its $500
ceiling:

| Case | Calculation | Maximum delivered axle price |
|---|---:|---:|
| Nominal, 6,400 installed | (500 - 370) / 6,400 | **$0.02031 per installed pin** |
| Conservative, 6,720 delivered plus $23 service spares | (500 - 370 - 23) / 6,720 | **$0.01592 per delivered pin** |

Packaging, freight, tax, inspection, and any sample order consume the same
allowance unless separately funded. At the current target prices, the
nominal BOM is $498 and the conservative BOM is $729, but both are estimates,
not quotes.

## Public sourcing observations (not quotations)

| Source and observation date | Material / finish | Size and tolerance | End treatment | Pack / price | Availability / lead time | 6,720-piece implication |
|---|---|---|---|---|---|---|
| Zoro Select DP7X01010h8-100P1, 2026-10-07, [product page](https://www.zoro.com/zoro-select-dowel-pin-ss-m1x10mm-l-pk100-dp7x01010h8-100p1/i/G3373772/) | 18-8 stainless, plain, B80 | 1 mm × 10 mm; -0.014/-0.000 mm diameter; ±0.250 mm length; ISO 2338B h8 | Not stated; drawing/deburr unresolved | $7.79/100 = $0.07790/pin; 68 packs = 6,800 pins, **$529.72** before freight/tax | No 6,720-piece stock promise or lead time stated | 26.1× nominal gate and 4.9× conservative gate before freight |
| Fastener Mart PBU533-600, 2026-10-07, [product page](https://www.fastenermart.com/iso-2338-dowel-pins.html) | A1 stainless, h8, ISO 2338 Form B | 1 mm × 10 mm; h8; numeric limits not exposed on page | Form B; detailed chamfer/deburr unresolved | 100-pack $7.96; 2,000-pack $113.37 ($0.056685); four cartons = 8,000 pins, **$453.48** before freight/tax | 2,000-piece carton is stated; stock/lead time not stated | 22.4× nominal gate and 3.56× conservative gate before freight; 1,280 excess |
| Grainger 1TU62, 2026-10-07, [product page](https://www.grainger.com/product/Dowel-Pin-1TU62) | 18-8 stainless, plain, B80 | 1 mm × 10 mm; -0.014/-0.000 mm diameter; ±0.250 mm length; ISO 2338B h8 | Not stated; drawing/deburr unresolved | $15.88/100 = $0.15880/pin; 68 packs = 6,800 pins, **$1,079.84** before freight/tax | No usable 6,720-piece stock promise; lead time unresolved | 53.1× nominal gate and 10.0× conservative gate |
| Vital Parts DOW2338A-1-10-A1, 2026-10-07, [product page](https://www.vital-parts.co.uk/chamfered-parallel-pins-iso-2338a/4402-dow2338a-1-10-a1) | A1 stainless, m6 | 1 mm × 10 mm; m6; ISO 2338A | Chamfered; exact chamfer/deburr acceptance not stated | 5,000+ tier £0.23 ex VAT; 6,720 = **£1,545.60** before delivery/VAT | Up to 813 in stock, 1,113 dispatch within 2 days; above that production at 14+ days | Price and m6 fit class both fail current screen; redesign would be required |

Zoro is the lowest public price with the explicit h8/slip-fit class and
Fastener Mart has the lowest public USD carton tier. Neither is a delivered
quote or availability promise for 6,720 pieces. Catalogue observations are
not supplier commitments.

## Drawing-level fit screen

The integrated DES-004 coupon CAD and analytical gate define the current
screen geometry: candidate pin **Ø1.00 mm × 10.00 mm**, printed rotor bore
**Ø1.40 mm**, **0.40 mm nominal diametral clearance**, worst-case analytical
clearance **0.30 mm** after the stated ±0.05 mm bore/axle assumptions, and an
**8.00 mm** frame + rotor + retainer stack. These are CAD/assumption values,
not measured production dimensions. The coupon has no released production
drawing for pin retention or end treatment.

| Item | Current analytical value/evidence | Status before release |
|---|---|---|
| Pin nominal diameter | Ø1.00 mm candidate | Supplier drawing required |
| Rotor bore | Ø1.40 mm coupon CAD | Production tolerance/roundness unknown |
| Diametral clearance | 0.40 mm nominal; 0.30 mm stated worst-case screen | Calculation only; print measurement required |
| Pin length / retained stack | 10.00 mm candidate over 8.00 mm coupon stack; 2.00 mm nominal end margin | Length tolerance, free length and retention faces unresolved |
| Retention | Passive retainer concept is not dimensioned in a released production drawing | Specify shoulders/end stops and insertion direction |
| End treatment | Reviewed pages do not state chamfer/deburr dimensions/acceptance | Require drawing/certificate and inspection method |
| Material/finish | 18-8/A1 stainless plain catalogue classes | Corrosion/wear requirement open; no silent music-wire substitution |
| Fit/function | Rotor through five stops and retain 3.27 N design load | No physical measurement; separate validation gate |

The h8/Form B catalogue classes are directionally compatible with a rotating
axle. Their stated or standard-class tolerances do not prove the assumed
0.30 mm envelope because production bore tolerance, straightness, end
geometry, and retention interfaces remain unspecified. Any m6 source requires
a new hole/fit and assembly analysis. Integral printed axles remove a
purchased line only by adding 6,400 wear/creep interfaces and are not a
reliability or cost-gate pass.

## Cost-reduction screen

The only credible route toward $0.02031/$0.01592 is a made-to-print bulk
quote or cut/deburr route. Cutting in-house adds tooling, deburring,
inspection, corrosion and handling risk. Pre-cut h8 stainless lowers assembly
and maintainability risk but is not cost viable on observed retail tiers.
Removing axles or reducing axle count would redesign the rotary mechanism and
is out of scope. Printed integral axles are rejected from the purchased-cost
pass until wear, creep, fit, replacement and cycle-life evidence exists.

## Cheapest reproducible next sourcing route

Issue the same built-to-print RFQ to at least three industrial pin/turned-part
suppliers for **6,720 pieces plus a separately priced 100-piece sample**:

`Ø1.000 mm nominal, slip-fit axle pin, L=10.000 mm; supplier to state diameter tolerance, cut-length tolerance, material/grade and finish, end chamfer/deburr dimensions, lot inspection/certificate, MOQ, pack quantity, lead time, packaging, tax and delivered freight.`

Required closure evidence is (1) a delivered quote below $0.02031/pin nominal
or $0.01592/pin conservative, (2) confirmed stock/MOQ/lead time and freight,
and (3) a supplier drawing/certificate checked against the Ø1.40 mm coupon
bore, 8.00 mm stack, retention and 0.30 mm analytical worst-case clearance.
Physical fit and cycling remain separate validation work.

## Handoff

DES-004 cost status does **not** change: nominal $498 and conservative $729
remain planning calculations, not delivered-cost passes; the conservative
case remains above the $500 ceiling. The current DES-004 CAD/BOM baseline is
unchanged and is the rollback state if bulk sourcing or fit fails.
