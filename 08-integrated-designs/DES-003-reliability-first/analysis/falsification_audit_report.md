# Falsification Audit Report: DES-003 & Q-009

## 1. Executive Summary
This audit evaluates the reliability-first baseline (DES-003) and the FDM critical-fit calibration (Q-009). The design is analytically consistent but physically unvalidated. The primary risk is the narrow geometric margin (0.09 mm) between latch excursion and the owned half-lane, which may be consumed by FDM tolerance stack-up. Regional coupling remains an open risk with no empirical stiffness data.

## 2. Constants Audit
| Constant | Value | Source | Consistency |
| :--- | :--- | :--- | :--- |
| `PITCH_MM` | 5.08 mm | `a1_coupon_readiness.py` | Consistent across all analysis/SCAD |
| `LATCH_T_MM` | 0.45 mm | `a1_coupon_readiness.py` | Consistent |
| `SERVICE_LOAD_N` | 3.27 N | `a1_coupon_readiness.py` | Consistent |
| `MIN_FEATURE_MM` | 0.44 mm | `a1_coupon_readiness.py` | Matches fabrication process limit |

## 3. Claim Falsification Table
| Claim | Status | Category | Evidence / Gap |
| :--- | :--- | :--- | :--- |
| Latch fits in owned half-lane | **Validated (Analytic)** | Calculated | $0.65\text{mm} \le 0.74\text{mm}$ (Margin: $0.09\text{mm}$) |
| Design is printable on X1C | **Validated (Analytic)** | CAD-derived | Min feature $0.44\text{mm} \ge 0.44\text{mm}$ |
| Optical on/off contrast $\ge 2\times$ | **Open** | Calculated | Model predicts $7.72\times$; requires physical validation |
| Regional coupling $\le 0.10\text{mm}$ | **Open** | Inferred | Required stiffness calculated; no measured $k$ |
| Latch snap force $\ge 7.14\text{N}$ | **Open** | Calculated | $R1$ kill line defined; requires physical test |
| Full span fits X1C bed | **Validated (Analytic)** | CAD-derived | $210\text{mm} \le 256\text{mm}$ |

## 4. Quantitative Acceptance/Rejection Gates

### A. Geometric Fit (Coupon B)
- **Acceptance:** Latch excursion $\le 0.74\text{mm}$ (with $\pm 0.05\text{mm}$ tolerance).
- **Rejection:** Any interference $> 0.00\text{mm}$ with neighbouring cell body.

### B. Force/Motion (Coupon A/B)
- **Snap Force (R1):** $\text{Mean Force} \ge 7.14\text{N}$. Reject if $< 7.14\text{N}$.
- **Contrast Ratio (R4):** $\text{On/Off Ratio} \ge 2.0$. Reject if $< 2.0$.
- **Coupling Motion (Q5):** $\text{Max Displacement} \le 0.10\text{mm}$ under $3.27\text{N}$ load. Reject if $> 0.10\text{mm}$.

## 5. Hidden Failure Modes & Risks
1. **Tolerance Exhaustion:** The $0.09\text{mm}$ margin is extremely tight for FDM. Thermal shrinkage or over-extrusion could cause immediate mechanical interference.
2. **Stiffness Assumption:** The regional coupling analysis assumes a linear stiffness $k$. Plastic deformation or creep under service load could invalidate the $0.10\text{mm}$ gate.
3. **Surface Roughness:** Optical return calculations assume ideal reflectances. FDM layer lines may diffuse the spot, reducing the $7.72\times$ ratio.

## 6. Verification Instructions
1. **Print Coupon A:** Measure snap-off force using a calibrated load cell. Verify $\ge 7.14\text{N}$.
2. **Print Coupon B:** Apply $3.27\text{N}$ to a boundary cell; measure displacement of the central cell using a dial indicator. Verify $\le 0.10\text{mm}$.
3. **Optical Pass:** Use the reader gantry to measure return intensity of "on" vs "off" states on a printed array. Verify ratio $\ge 2.0$.
