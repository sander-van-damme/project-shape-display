---
status: complete
builds-on: [DES-004, ADR-005, E-012]
---

# E-013: DES-004 axle-pin sourcing and fit screen

## Disposition

**UNRESOLVED against both cost gates; fit not released.** No public source
checked on 2026-10-06 provides a delivered 6,720-piece quote at either gate,
and no source supplies enough drawing-level end-treatment information to close
the fit check. This is a sourcing and analytical screen only: no purchase,
production commitment, or physical validation follows.

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

| Source and observation date | Material / finish | Size and tolerance | End treatment | Pack / price | Availability / lead time | Fit and cost implication |
|---|---|---|---|---|---|---|
| Grainger 1TU62, observed 2026-10-06, [product page](https://www.grainger.com/product/Dowel-Pin-1TU62) | 18-8 stainless, plain | 1 mm × 10 mm; diameter -0.014/-0.000 mm; length ±0.250 mm; ISO 2338B h8 | Not stated on page; drawing must be obtained; deburr/chamfer unresolved | 100-pack, $15.88/pack = $0.15880/pin before freight | Page exposes order quantity but no usable 6,720-piece stock promise; lead time unresolved | Exact nominal size and slip-fit class, but 68 packs = 6,800 pins and $1,079.84 before freight. Fails nominal and conservative gates by large margin. A 100-piece pack is a possible sample quantity, not a fit certificate. |
| Vital Parts DOW2338A-1-10-A1, observed 2026-10-06, [product page](https://www.vital-parts.co.uk/chamfered-parallel-pins-iso-2338a/4402-dow2338a-1-10-a1) | A1 stainless (303 equivalent) | 1 mm × 10 mm; m6 tolerance band; ISO 2338A | Chamfered parallel pin; exact chamfer dimensions and deburr acceptance not stated | 5,000+ tier £0.23 each, ex VAT; 6,720 = £1,545.60 before delivery/VAT | Page showed up to 813 in stock, 1,113 available for dispatch within 2 days, and quantities above that available for production at 14+ days | Chamfer is useful for assembly, but m6 is an interference/press-fit style rather than the retained slip-clearance assumption; hole and assembly process would need a controlled change. Price is already >$0.02/pin before currency conversion and freight. |
| Hardware Specialty ISO8734-1X10-C1 and ISO2338-1m6X10-A1, observed 2026-10-06, [ISO8734](https://www.hardwarespecialty.com/Product/1303771), [ISO2338](https://www.hardwarespecialty.com/Product/954076) | Stainless steel, passivated; ISO8734 listing reports 460–560 HV30; ISO2338 listing 210–280 HV30 | 1 mm × 10 mm | Standard-specific end treatment not fully exposed; quote/drawing required | No public price shown; contact/quote | Stock and lead time unresolved | Shows that both hardened and unhardened/passivated catalog classes exist, but supplies no reproducible delivered cost or availability evidence. Not a gate result. |

The Grainger observation is the strongest reproducible USD comparison. Its
catalog class is a **slip-fit** pin, so it is directionally compatible with a
rotating axle; the page does not establish actual lot availability, packaging
freight, chamfer, or deburr condition. The Vital Parts item is not silently
substituted because its m6 fit class conflicts with the current analytical
slip-clearance assumption.

## Drawing-level fit screen

The retained analytical geometry is unchanged: candidate pin **Ø1.00 mm ×
10.00 mm**, **0.30 mm assumed worst-case diametral axle/bore clearance**, and
**8.00 mm retained stack**. E-012's clearance is a tolerance-screen
assumption, not a measured process capability.

The only observed catalog item with an explicitly compatible slip class is
Grainger 1TU62. Its stated -0.014/-0.000 mm diameter tolerance and ±0.250 mm
length tolerance do not invalidate the assumed 0.30 mm envelope, but they do
not prove it either because the matching rotor-bore tolerance, actual end
geometry, and retention/stack interfaces remain unspecified. The 10 mm
nominal length is consistent with the candidate; the ±0.25 mm length range
must be checked against the 8 mm retained stack and end clearances. No
catalog page reviewed supplies a complete drawing-level deburr/chamfer
specification or certificate for this application. Therefore fit status is
**UNRESOLVED**, not PASS.

Any press-fit/m6 source would require a new hole/fit and assembly analysis;
that would be a design change and is outside this screen. Integral printed
axles are excluded: they remove purchased cost only by introducing unresolved
wear, creep, friction, and replacement risks at 6,400 interfaces.

## Cheapest reproducible next sourcing route

Issue the same built-to-print RFQ to at least three industrial pin/turned-part
suppliers and request a delivered price to the project location for **6,720
pieces plus a separately priced 100-piece sample**:

`Ø1.000 mm nominal, slip-fit axle pin, L=10.000 mm; supplier to state diameter tolerance, cut-length tolerance, material/grade and finish, end chamfer/deburr dimensions, lot inspection/certificate, MOQ, pack quantity, lead time, and freight.`

Retain Grainger 1TU62 as the dimensional/slip-fit fallback for a sample or
fit coupon only, not as a cost-gate source. The missing evidence required to
close this task is (1) a written delivered quote below $0.02031/pin nominal
or $0.01592/pin conservative, (2) confirmed stock/MOQ/lead time and freight,
and (3) a supplier drawing or certificate that can be checked against the
Ø1.40 mm rotor bore, 8.00 mm retained stack, and E-012's assumed 0.30 mm
worst-case diametral clearance. Physical fit and cycling remain separate
validation work.
