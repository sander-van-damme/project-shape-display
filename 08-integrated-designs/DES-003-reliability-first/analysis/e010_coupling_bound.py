"""
Script: e010_coupling_bound.py
Purpose: compute peak displacement and coupling bounds for regional updates
Author: opencode AI
"""

# Assumptions and constants are encoded next to values. This is a screening
# bound, not a finite-element model and not physical validation.
# Candidate stiffness sensitivities in N/mm (inferred; not measured).
stiffnesses = [10, 32.7, 50]
# Coupling fractions to evaluate
coupling_fractions = [0.01, 0.05, 0.10]
# Updates sizes (side length)
sizes = [5, 10, 20]

# Total force assumed for sensitivity only: 1000 N for 5x5, scaled by area.
# Provenance: unresolved; this value is not established by the DES-003 CAD.
base_force_5x5 = 1000

def peak_disp(k: float, f_frac: float, size: int) -> float:
    # Area scales with size squared
    area_scale = (size * size) / (5 * 5)
    total_force = base_force_5x5 * area_scale
    return (f_frac * total_force) / k

print("Stiffness and coupling displacement bounds")
print(f"{'Size':>6} {'k (N/mm)':>8} {'Coupling':>10} {'Disp (mm)':>10}")
for sz in sizes:
    for k in stiffnesses:
        for cf in coupling_fractions:
            disp = peak_disp(k, cf, sz)
            print(f"{sz:6} {k:8.2f} {cf:10.2%} {disp:10.4f}")

# Compute max coupling that keeps displacement below 0.01 mm for each k, size
limit = 0.01
print('\nMaximum coupling fraction to keep displacement <', limit, 'mm')
for sz in sizes:
    for k in stiffnesses:
        # f_frac * (base_force_5x5 * area_scale) / k = limit
        # f_frac = (limit * k) / (base_force_5x5 * area_scale)
        area_scale = (sz * sz) / (5 * 5)
        total_force = base_force_5x5 * area_scale
        f_frac = (limit * k) / total_force
        print(f"Size {sz:2} k N/mm {k:>6.1f} --> max coupling {f_frac:.4%}")
