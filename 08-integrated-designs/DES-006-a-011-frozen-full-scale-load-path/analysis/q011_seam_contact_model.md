# Q-011 seam/contact compliance bound

**Evidence class: calculated sensitivity model; not FEA and not physical validation.**

This artifact tests whether the missing DES-006 seam, support seating, bearing,
and rotor/post hard-stop terms can be bounded from the frozen information. Run
from the repository root:

```text
python3 08-integrated-designs/DES-006-a-011-frozen-full-scale-load-path/analysis/q011_seam_contact_model.py
```

## Model and boundary conditions

The cell datum is treated as one translational output port. The frozen rail
beam and shaft torsion equations are retained unchanged from
`q011_frozen_load_path.py`. Each omitted interface is an effective linear
spring in series with that port:

\[
\delta_{missing}=F(1/k_{seam}+1/k_{support}+1/k_{bearing}+1/k_{stop})
\]

where `k` is in N/mm and the resulting displacement is in mm. The model uses
the declared 100 N incidental-hand force for a conservative all-terms-loaded
envelope; it also prints a service-force sensitivity case at 3.27 N. All four
terms are assumed collinear and additive. This is deliberately conservative
and does not claim the real load shares this way.

The boundary conditions are the frozen two-end simply supported rail, 80-cell
shaft torsion screen, and the existing 0.09 mm credited alignment allowance.
The 0.60 mm drawing-level stack is not silently substituted into the spring
model. The model contains no preload, friction, contact area, fastener
stiffness, printed-part modulus, bearing housing geometry, stop crush, or
nonlinear gap/contact law because those inputs are not frozen in DES-006.

## Reproduced result

The script reports:

| Quantity | Result | Classification |
|---|---:|---|
| 100 N rail + shaft baseline | 0.12919 mm | calculated from frozen equations |
| Remaining allowance to `<0.10 mm` | -0.02919 mm | calculated; already negative |
| Required missing displacement at 100 N | `<0 mm` | calculated; impossible for nonnegative compliance |
| Required missing equivalent stiffness at 100 N | no finite positive value | calculated; gate fails before omitted terms |
| 3.27 N rail + shaft baseline | 0.06897 mm | calculated sensitivity |
| Service allowance before fixed stack | 0.03103 mm | calculated sensitivity |

For sensitivity only (not claimed DES-006 values), assigning 10,000 N/mm to
each of the four missing springs adds 0.04000 mm at 100 N. Assigning an
extremely stiff 100,000 N/mm to each still adds 0.00400 mm, so the 100 N
combined result remains above the gate even when omitted compliance tends to
zero. The service case with the existing 0.09 mm credited stack also remains
above the gate. These points expose the direction and scale of the terms; they
do not source or validate stiffness.

## Term disposition

| Omitted term | Numeric bound from this model | Status and reason |
|---|---:|---|
| Cartridge seam opening/local tilt | none; parameterised as `100/k_seam` | **Unresolved**: clamp preload, contact friction, seam section, and load eccentricity are absent |
| Rail support seating | none; parameterised as `100/k_support` | **Unresolved**: support land, fastener/contact preload, and seating gap are absent |
| Bearing housing compliance | none; parameterised as `100/k_bearing` | **Unresolved**: bearing type, fit, housing section, and radial preload are absent |
| Rotor/post hard-stop compliance | none; parameterised as `100/k_stop` | **Unresolved**: stop material, contact pressure, land geometry, and crush/wear law are absent |

The model therefore demonstrates that a more elaborate contact calculation
cannot produce a defensible numeric bound from the current frozen inputs alone.
It also demonstrates that bounding these terms to zero would not rescue the
100 N integration screen: the retained rail-plus-shaft baseline is already
0.02919 mm over the gate. The 0.60 mm drawing-level stack remains
unvalidated, not a pass margin.

## Disposition and cheapest falsification

**Q-011 / DES-006 disposition: HOLD; reject integration against the `<0.10 mm`
screen for the current frozen load path.** This is an analytical hold/reject,
not a hardware result. No physical testing was performed.

The cheapest falsification is a single instrumented 5x5 cartridge/seam coupon
with the frozen 20 mm clamp land and M4 clamp pattern, loaded at the cell datum
to 3.27 N and 100 N while measuring seam opening and datum displacement. In
parallel, record bearing radial play and post/stop displacement under 3.27 N.
Those measurements would supply `k_seam`, `k_support`, `k_bearing`, and
`k_stop` (or expose a gap/slip nonlinearity) for rerunning this same script.
Until those inputs exist, any numeric stiffness chosen here would be an
assumption rather than a bound.
