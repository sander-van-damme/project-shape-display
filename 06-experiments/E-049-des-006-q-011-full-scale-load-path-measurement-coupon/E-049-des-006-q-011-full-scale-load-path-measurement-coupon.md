---
status: active
builds-on: [Q-011, DES-006, E-047]
---

# E-049: DES-006/Q-011 full-scale load-path measurement coupon

## Decision question and evidence boundary

Can the frozen DES-006 load path be measured with a frame-referenced cell
datum motion below the existing `<0.10 mm` operational screen after seam,
support seating, bearing/housing, rotor/post-stop, and cartridge-registration
terms are included?

This packet defines a physical experiment. It does **not** create a product
requirement, convert the inherited `<0.10 mm` screen into a specification, or
claim that the hardware has been tested. The 100 N case is an accidental-
handling survivability observation only, as requested by Q-011; it is not the
service acceptance case.

The experiment can establish evidence for the tested coupon, assembly state,
load vectors, and instrument uncertainty. It cannot by itself establish
complete-display yield, lifetime, creep, dynamic impact response, neighboring
module coupling outside the coupon, or production capability.

## Smallest representative coupon

Use one full-span DES-006 load-path coupon with the following interfaces. The
geometry is deliberately the smallest one that retains both the global span
and the mid-span cartridge seam; a seam-only 5x5 coupon cannot measure the
rail/shaft/support contribution and is insufficient for this question.

| Item | Coupon definition | Evidence class |
|---|---|---|
| Cell pitch and span | 5.08 mm pitch; 80-cell, 406.4 mm active span | inherited/CAD-derived arithmetic |
| Rail | 25 x 25 mm solid square aluminium rail, nominal `L=406.4 mm` | DES-006 structural assumption |
| Rail supports | two production-representative end supports, including actual seating, fasteners, and datum interfaces | required hardware interface; to be recorded before test |
| Cartridge modules | two 5x5 cartridges meeting at the rail mid-span seam; actual clamp lands, M4 clamps, registration features, and media/cartridge interfaces | DES-006 candidate interface |
| Shaft | 8.00 mm solid steel shaft with end bearings and the nine bearing stations at 50.8 mm pitch | DES-006 candidate interface |
| Rotor/post | at least one instrumented central rotor/post at the seam-adjacent station and one control rotor/post at a non-seam station; 3.00 mm rotor body, 2.00 mm reaction radius, actual indexed stop | DES-006 candidate interface |
| Cell datum | a marked cell datum on each instrumented rotor/cartridge, with a rigid optical target or probe seat tied to the cell surface, not to the moving shaft | test datum definition |
| Frame reference | independent rigid reference beam/plate attached to the two rail support bodies, with no sensor bracket attached to cartridge, shaft, bearing, or rotor | test fixture requirement |

The coupon shall be built from the intended material/process. If printed
cartridge or stop parts are used, record material, print orientation, layer
height, infill/wall settings, print date, and any post-processing. Do not
substitute a rigid dummy for the seam, bearing housing, or stop when measuring
the load path. A rigid dummy may be used outside the measured interfaces only
to protect the fixture.

Before fabrication, issue a dimensioned coupon drawing that reconciles the
DES-006 notation of an 80-cell span with its two 5x5 cartridge interfaces.
The packet uses the frozen interface names but does not assume that the
notation is dimensionally self-consistent; fabrication is blocked until the
drawing explicitly shows the full 406.4 mm span, cartridge boundaries, and
instrumented cell locations.

### Assembly states and sample count

The minimum decision sample is **three independently assembled states** of the
same coupon geometry (`N=3`). For each state, disassemble and reassemble the
cartridges, supports, bearing housings, and rotor/post interfaces using the
declared assembly procedure; record clamp torque/preload where available.
Run three preload/service cycles per state. A single first assembly is a
fixture shakedown only and cannot close Q-011. If only one physical coupon is
available, the three reassemblies are useful pilot evidence but must be
reported as `N=1 hardware / N=3 assembly states`, not as three independent
coupons or production-yield evidence.

## Declared load vectors and sequence

All forces are applied through calibrated load cells and a spherical-ended or
otherwise self-aligning contact that reproduces the stated point and radius.
The force vector is expressed in the coupon frame; define `+z` as normal to
the rail/cell datum and `+y` as the tangential writer direction. Record the
actual vector, contact point, and torque from the load-cell channels.

1. **Zero and preload:** zero sensors after thermal soak; apply 0.5 N seating
   preload at the instrumented service cell, release to 0 N, and repeat twice.
   The preload is for repeatable contact seating and is not a requirement.
2. **Service case:** apply `F_service = [0, 0, 3.27] N` at the declared
   3.00 x 3.00 mm cell-contact area. Also run the worst-direction lateral
   orientation permitted by the fixture, with the same magnitude, if that
   direction is not collinear with `+z`. Hold 10 s at peak and unload to 0 N.
3. **Writer case:** apply the DES-006 writer vector
   `F_writer = [0, 2.00, 0] N` at the 2.00 mm reaction radius, with the
   resulting `T_z = 4.00 N mm` recorded rather than inferred. Test the
   rotor/post indexed stop in both approach directions if both are used in
   operation. Hold 10 s at peak and unload.
4. **Combined writer/service diagnostic:** where the fixture can safely
   superpose them, apply the 3.27 N service contact while the writer reaction
   is applied. Otherwise run the two cases in the same assembled state and
   report them separately; do not claim a combined bound from separate tests.
5. **100 N accidental-handling observation:** after service and writer tests,
   apply a quasi-static 100 N load at the declared rail/cell handling point
   and direction, ramping no faster than 10 N/s, hold 10 s, then unload. This
   is a survivability observation only. It does not inherit the `<0.10 mm`
   operational screen and is not a pass/fail product requirement.

Use a 60 s unloaded dwell after every peak and a 10 min final unloaded dwell.
Do not reset the displacement zero between peak and unload; zeroing would hide
permanent set.

## Fixture and measurement channels

The coupon sits on a metrology table or equivalent stiff base. The rail end
supports are attached to a rigid fixture plate. The frame-reference beam is
independently surveyed against the table and carries all displacement sensor
references. Before loading, verify that fixture compliance under a dummy load
is at least 5x lower than the 0.10 mm screen or measure and subtract it with a
separate rigid-coupon calibration. A load-cell reaction frame must not share a
flexible bracket with the displacement reference.

Required channels, sampled synchronously at at least 100 Hz during ramps and
at least 10 Hz during holds:

| Channel group | Minimum instrumentation | Purpose |
|---|---|---|
| Direct cell datum | 3-axis optical/DIC target or three orthogonal LVDT probes from the frame reference to the instrumented cell datum; duplicate one axis with an independent sensor | decisive datum motion and sensor repeatability |
| Seam | paired targets/probes on both cartridge sides, normal and tangential to the seam, plus relative rotation from two points separated by at least 20 mm | seam opening and local tilt |
| Supports | probes from frame reference to each rail support/rail end, at least vertical and lateral | support seating and rigid-body motion |
| Bearing/housing | radial probes at both end bearings and the seam-adjacent intermediate bearing housing | housing/play motion separate from shaft motion |
| Rotor/post-stop | probe or DIC targets spanning rotor body and post/stop, with the rotor angle logged | post/stop clearance, contact slip, and local compliance |
| Registration | targets on cartridge datum/fiducials and rail/frame reference at both sides of the seam | cartridge-to-rail registration term |
| Load/torque | calibrated 3-axis load cell plus torque channel or force couple; encoder for rotor angle | declared vector and actual peak/load history |

Measure rigid-body table/frame motion with at least two reference targets. The
reported cell datum is the cell target relative to the interpolated frame
reference, not a sensor reading relative to a moving cartridge or shaft.

## Reduction and acceptance equations

For each channel, subtract the pre-load baseline from the synchronized peak
record after applying only a documented fixture/reference correction:

```text
d_i(t) = x_i(t) - x_i(preload baseline)
d_peak = max_t ||d_datum(t)||_2
d_residual = ||x_datum(final unloaded dwell) - x_datum(preload baseline)||_2
```

Use the peak over the complete ramp, hold, and unload record for `d_peak`;
also report the peak during the hold separately. For the direct operational
screen, the measurement passes only when, for every service and declared
writer case and every instrumented datum:

```text
d_peak + U95(d_peak) < 0.10 mm
d_residual + U95(d_residual) < 0.10 mm
```

The strict inequality preserves the existing screen wording. `U95` is the
expanded uncertainty at approximately 95% coverage, calculated before looking
at the result:

```text
U95 = 2 * sqrt(u_sensor^2 + u_reference^2 + u_load^2
              + u_repeatability^2 + u_temperature^2)
```

Use calibration certificates or pre-test repeatability to populate each
standard uncertainty. `u_repeatability` comes from the three zero/preload
repeats and is not replaced by the scatter of only successful runs. Report
the largest uncertainty component and the measured margin
`M = 0.10 - (d_peak + U95)`.

The diagnostic channels shall also be reduced as frame-referenced relative
motions. Report the signed component along the datum displacement vector and
the 3-D norm for seam, support, bearing/housing, rotor/post-stop, and
registration. For an explicit conservative attribution bound, use the
nonnegative scalar projection magnitudes:

```text
D_terms = D_seam + D_support + D_bearing + D_stop + D_registration
D_bound = D_global_frame + D_terms + U95_terms
```

`D_bound` is a worst-case diagnostic sum, not an independent requirement and
not a license to double-count rigid-body motion. The direct datum equation is
the acceptance result; the term sum is used to identify which interface must
be corrected if the direct result fails. A term is **bounded** only when its
channel has a traceable frame reference, its load/contact state is recorded,
and its uncertainty is included. A zero or unmeasured term is unresolved, not
zero.

For the 100 N observation, report peak displacement, permanent set, visible
damage, clamp slip, bearing play change, stop damage, and post-test function.
Do not apply the `<0.10 mm` pass equation to that case.

## Stop conditions and recovery

Stop the current ramp and unload safely if any of the following occurs:

- force, torque, or displacement channel saturates or loses synchronization;
- load overshoot exceeds 10% of the declared case or the contact leaves the
  intended point/area;
- sudden displacement exceeds 0.50 mm, a force drop exceeds 10% without a
  commanded unload, or any clamp/support/stop visibly slips;
- cracking, delamination, permanent rotor/post interference, bearing seizure,
  fastener loosening, or other damage is observed;
- temperature changes by more than 2 C from the zeroed condition without a
  documented correction.

Photograph and preserve the state after a stop. Mark the run invalid for the
affected load case if the declared vector or reference was lost; do not
silently retry until the failure disappears. A valid retry requires a new
baseline and an explanation of the corrective action. If the direct datum
motion exceeds 0.10 mm but no stop condition occurs, complete the safe hold
and unload so the failure magnitude and permanent set remain measurable.

## Decision criteria

| Result | Decision |
|---|---|
| All three independent assembly states pass service and writer direct-datum equations, with positive margin, no unbounded term, and residual motion within the stated equation | **Analytical screen is physically supported for this coupon and tested states; Q-011 may advance to a broader qualification decision.** This is not complete-display validation. |
| Any state fails the direct equation, has non-positive margin, or has an unresolved seam/support/bearing/stop/registration channel | **Q-011 remains HOLD.** Do not average away the failing state. Correct the load path or fixture and repeat. |
| Service/writer passes but 100 N produces damage or loss of function | Record **accidental-handling survivability failure** separately; it does not change the service-screen requirement, but it blocks any claim that the assembly tolerates the 100 N observation. |
| One coupon or one assembly state only | **Pilot/instrument qualification evidence**, not a Q-011 closure. |

The experiment does not authorize changing DES-006 geometry, converting the
100 N case into a product requirement, or declaring the full display qualified.
Any architecture-level change required to obtain margin belongs in a separate
design decision.

## Evidence record and reproducibility

Archive the frozen drawing or dimensioned test sketch, assembly traveler,
material/process record, sensor serial numbers and calibration dates, fixture
calibration, raw synchronized data, analysis notebook/script, uncertainty
budget, photographs, and run disposition. Record actual dimensions, clamp
torques, bearing fits/play, stop gap/contact width, and support seating before
the first load. No value may be back-filled from the nominal DES-006 table.

Evidence classes for the final report must remain explicit:

- geometry and interface values: measured or CAD-derived, labelled separately;
- force/torque/displacement traces: physical measurement for this coupon only;
- uncertainty: calculated from calibration/repeatability inputs;
- acceptance: calculated from measured traces and the declared screen;
- complete-display, lifetime, production-yield, and dynamic-impact claims:
  unresolved unless separately tested.

## Current disposition

**Experiment definition complete; hardware evidence pending.** E-049 provides
the smallest full-span instrumented coupon and a falsifiable protocol. It does
not close Q-011 or validate DES-006. The decisive next action is to fabricate
or assemble the one full-span coupon, qualify the reference fixture, and run
three independent assembly states under the declared service and writer
vectors.
