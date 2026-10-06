---
status: complete
builds-on: [E-006, E-007, A-004, P-006]
---

# E-008: A-004 Coupler Isolation and Hidden Cost Analysis

## Objective
Determine if the `A-004` tile coupler architecture plausibly delivers the required regional-update isolation (10x reduction vs `DES-003`) and quantify associated costs and reliability penalties.

## 1. Isolation Model (Analytical)

### Assumptions
- **Service Load ($F_{service}$):** 3.27 N (design-calculated input carried by `E-006`; not a physical measurement).
- **Motion Gate ($\delta_{gate}$):** 0.10 mm (proposed in `Q-005`/`E-006`).
- **Coupler Transfer Fraction ($\alpha_{coupler}$):** The fraction of the active region's disturbance transmitted through a *disengaged* coupler to a stationary neighbour.
- **Baseline Coupling ($\alpha_{base}$):** 5% (0.05) as used in `E-006` sensitivity.

### Regional Boundary Analysis
The required support stiffness $k$ to maintain the gate is:
$$k = \frac{F_{service} \times \alpha \times \text{Perimeter}}{\delta_{gate}}$$

| Region | Perimeter (cells) | $k_{req}$ ($\alpha = 5\%$, `DES-003`) | $k_{req}$ ($\alpha = 0.5\%$, `A-004` target) |
|---|---|---|---|
| 5x5 | 16 | 26.16 N/mm | 2.62 N/mm |
| 10x10 | 36 | 58.86 N/mm | 5.89 N/mm |
| 20x20 | 76 | 124.26 N/mm | 12.43 N/mm |

**Inferred Isolation Benefit:**
If $\alpha_{coupler} \le 0.5\%$, the required stiffness drops by 10x. This makes the 20x20 update case plausible even with modest support stiffness (e.g., 15-20 N/mm), which is significantly easier to achieve than the 124.26 N/mm required by the baseline.

**Plausibility of $\alpha_{coupler} \le 0.5\%$:**
- **Geometry-derived:** A disengaged mechanical coupler (e.g., a sliding pin or clutch) typically relies on clearance and surface friction. If the coupler is fully disengaged, the transfer is dominated by the stiffness of the disengaged interface (e.g., plastic-on-plastic contact). 
- **Inferred:** 0.5% coupling is a stringent requirement. It implies that the "off" state of the coupler must be nearly perfectly rigid-body decoupled. Any residual elastic path (e.g., the coupler housing itself) will contribute to $\alpha_{coupler}$.

## 2. Hidden Cost and Reliability Penalty

### Resource Quantification (8x8 Grid)
- **Coupler Count:** 64 units.
- **Purchased Cost:** 
  - Low bound: 64 $\times$ \$3 = \$192
  - High bound: 64 $\times$ \$6 = \$384
  - *Note: This represents a ~90% to 180% increase in purchased component cost over the `DES-003` baseline (~\$210).*
- **Moving Interfaces:** 64 additional couplers. Each is a potential point of failure; whether they require separate actuators is architecture-dependent and unresolved.

### Reliability Analysis
- **Jam Propagation:** In a shared power bus, a single coupler jamming in the "engaged" position or mechanically seizing could lock the entire drive shaft/belt. This converts a local tile failure into a system-wide outage.
- **Backlash Propagation:** If each coupler contributes a modest backlash $\epsilon$, the cumulative error across a row of 8 tiles is $8\epsilon$. For $\epsilon = 0.02\text{ mm}$, total backlash is 0.16 mm, exceeding the 0.10 mm gate. This impacts the precision of the *active* region updates.
- **Assembly Yield:** The probability of a "perfect" 64-coupler assembly is $P_{tile}^{64}$. If $P_{tile} = 0.99$ (1% defect rate), total yield is $\sim 53\%$.

## 3. Comparison vs E-007 Gate

| Metric | E-007 Gate (10x Reduction) | A-004 Analysis | Verdict |
|---|---|---|---|
| Isolation | $\alpha \le 0.5\%$ | Plausible but unmeasured | **Unresolved** |
| Cost | "Not a free improvement" | \$192–\$384 added cost | **FAIL (High Penalty)** |
| Reliability | "Jam propagation" | System-wide failure risk | **FAIL (Critical Risk)** |

## Verdict
**FAIL / REJECTED**

While the `A-004` architecture can analytically satisfy the regional isolation gate by reducing $\alpha$, it does so at an unacceptable cost in both budget and reliability. The transition from a gantry-based system (`DES-003`) to a shared-bus system with 64 couplers introduces a catastrophic failure mode (single-point jam) and a significant cost penalty that outweighs the isolation benefit.

## Next Action
Abandon `A-004` as a baseline contender. Return to `DES-003` and prioritize the "coupon-B protocol" (as suggested in `E-007`) to measure actual coupling and stiffness, seeking a way to reach the 0.10 mm gate without introducing 64 points of failure.

## Validation Report

### Mathematical Validation

The stiffness requirement formula $k = \frac{F_{service} \times \alpha \times \text{Perimeter}}{\delta_{gate}}$ was verified for the following cases:
- **Inputs:** $F_{service} = 3.27\text{ N}$, $\delta_{gate} = 0.10\text{ mm}$.
- **5x5 (P=16):** $k_{0.05} = 26.16\text{ N/mm}$, $k_{0.005} = 2.62\text{ N/mm}$. (**Verified**)
- **10x10 (P=36):** $k_{0.05} = 58.86\text{ N/mm}$, $k_{0.005} = 5.89\text{ N/mm}$. (**Verified**)
- **20x20 (P=76):** $k_{0.05} = 124.26\text{ N/mm}$, $k_{0.005} = 12.43\text{ N/mm}$. (**Verified**)

**Verdict:** Calculations are mathematically consistent.

### Cost and Resource Verification

- **Claim:** Added cost of $\$192–\$384 for 64 couplers.
- **Source:** `A-004` states "$3–6/coupler" for a 64-tile design.
- **Calculation:** $64 \times 3 = 192$; $64 \times 6 = 384$.
- **Evidence Label:** `sourced-class` (screening allowances).

**Verdict:** Verified.

### Technical Plausibility and Risks

- **Isolation ($\alpha \le 0.5\%$):** Labeled as `unresolved` in this analysis. The requirement for nearly perfect rigid-body decoupling is high and lacks experimental evidence.
- **Reliability (Jam/Backlash):** Labeled as `inferred`. Mechanical jam propagation in a shared-bus architecture is a known catastrophic failure mode for this topology. Backlash accumulation ($8 \times 0.02\text{ mm} = 0.16\text{ mm}$) exceeds the 0.10 mm gate.

**Verdict:** Plausible risks; conclusions are supported by mechanical first principles.

### Final Validation Verdict

**ANALYTICALLY CONSISTENT, NOT VALIDATED**

The arithmetic and stated risk analysis are reproducible, but the isolation benefit and jam behavior remain unmeasured. The evidence supports retaining `A-004` as rejected/unresolved for baseline selection, not a verified hardware rejection. A coupler coupon is still required before assigning a measured reliability or isolation verdict.
