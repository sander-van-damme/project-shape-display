---
status: complete
builds-on: [E-291]
---

# Fixed-focus depth and diffraction screen

**Paraxial wave-optics calculation, not measured lens performance.** Run
`python3 tools/curated-experiment-checks/E-292.py`. This tests the
E-291 finite-depth obligation, not another code or threshold. Assume a spatially
incoherent monochromatic 550-nm projector, uniform unobstructed circular pupil,
fixed focus, on-axis small field, and perfect camera. Omit aberrations, temporal
noise, pixel aperture, indirect light, finite-pupil terrain clipping and cap tilt. Actual projector coherence,
pupils, spectrum and field aberrations need characterization; these assumptions
are not sourced specifications for a selected engine.

[Edmund Optics' depth-of-field discussion](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/depth-of-field-and-depth-of-focus/)
explains why useful depth must specify spatial frequency and contrast, and why
stopping down trades defocus against diffraction. Its
[Airy-disk reference](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/limitations-on-resolution-and-contrast-the-airy-disk/)
gives the circular-aperture diffraction scale. [MIT 2.71 lecture 23](https://ocw.mit.edu/courses/2-71-optics-spring-2009/617bf42581d8ab552f32fc53adbfd7e7_vcqPRPkyWPU.pdf)
derives incoherent transfer from pupil autocorrelation. Sources accessed
2026-10-14; they supply optical methods, not our hardware qualification.

Let distance `t=300-z`, aperture diameter `a`, wavelength `lambda=.00055 mm`.
The harmonic focus `t0=2*t_near*t_far/(t_near+t_far)` minimizes the maximum
absolute inverse-distance defocus `delta=|1/t-1/t0|`. For S40/S50, its maximum
is .000256410/.000333333 per mm. The geometric defocus-circle angular diameter
is `a*delta`; the **in-focus** Airy first-zero angular diameter is
`2.44*lambda/a`. These are different diagnostics, **not additive blur widths,
probability distributions or an out-of-focus PSF**. Requiring each to fit one
angular bin dq requires simultaneously

```
a >= 2.44*lambda/dq     and     a <= dq/delta_max.
```

This is a conservative one-bin design criterion, not a necessary condition for
all subpixel inference or Gray-code decoding. The wave calculation below avoids
mistaking that diameter criterion for actual contrast transfer.

Inside pupil radius `R=a/2`, use phase `pi*delta*(x²+y²)/lambda`. At angular
frequency nu, its normalized autocorrelation displaces the pupils by
`s=lambda*nu`. For s<a the signed transfer is

```
4/(pi*R²) * integral[x=0..R-s/2]
 sqrt(R²-(x+s/2)²) * cos(2*pi*delta*nu*x) dx;
```

it is zero at/above the diffraction cutoff s=a. Retaining the sign exposes
contrast reversals that an absolute MTF would hide. The finest Gray bit repeats
every four bins, so its fundamental is `nu=1/(4*dq)`. A fundamental-transfer
screen is not the complete square-wave response, all-bit decoder or false-height
rate; boundary pixels still need explicit unknown handling.

Search 241 logarithmic apertures .05–30mm and 41 inverse-depth offsets at the
harmonic focus; maximize the minimum **signed** fundamental transfer. This is a
bounded sampled search of this lens family, not a global optical impossibility
proof. S40 retains the S50-sized fields as a common-hardware comparison.

| Code/field | Best sampled minimum transfer S40 / S50 | S50 aperture mm | S50 endpoint finest-bit peak contrast |
|---|---:|---:|---:|
|Original .05/2048 angular bin|.00624 / .00366|5.902|.00466|
|5.08-mm four-cap field|.02517 / .01751|3.752|.02229|
|6.35-mm four-cap field|.03989 / .02886|3.197|.03674|
|12.7-mm four-cap field|.18822 / .14879|2.087|.18944|

For these four S50 apertures, the third and higher odd harmonics of the finest
bit lie beyond the pupil cutoff. In a periodic interior, its complementary
square-wave difference becomes a sinusoid, whose maximum normalized contrast is
`4/pi*abs(OTF(nu))`. The last column is therefore a **forward optical response**
for these selected apertures, not a guessed box footprint: at the endpoint even
the best stripe phase fails the existing .5 bit-contrast acceptance. It is not a
full finite-field decoder replay or proof that every aperture, focus choice or
subpixel method fails. Camera blur and measurement noise have not been charged.

Independent checks: focused pupil overlap agrees with the analytic circular
transfer curve within1.17e-6 over32 cases; zero frequency, diffraction cutoff and
defocus-sign symmetry agree. Doubling integration512→1024 samples changes the
selected fine-field curves by at most1.52e-6. These check numerical evaluation,
not real lens model error or a certified continuous search optimum.

At S50, the old one-bin diameter criterion would need aperture≥54.97mm for
in-focus diffraction and≤.07324mm for endpoint defocus: no overlap. Balancing
those two diameter diagnostics gives a2.006mm aperture and .18393mm at the
25-mm terrain plane; **do not convert this into a measured height error**.
The wave result, rather than this diameter comparison alone, supports parking
the inherited sharp-bin approximation.

**Lower-resolution control:** dq=.0005, same D300/b8/S50 and circular pupil,
gives minimum fundamental transfer .74589 at a1.927mm. Yet its zero-start height
bin is5.521mm before camera uncertainty. Its one-bin diameter criterion still
fails, demonstrating why that criterion alone must not reject a reader. Coarser
codes can preserve useful contrast, but do not preserve the previous fine height
interval. No acceptance of5.5mm terrain error is implied.

**Decision:** park fixed-focus sharp-pixel absolute readback as currently
constructed. Do not tune decoder thresholds or add projection pixels to repair
missing optical contrast. Reopening needs a materially different depth/precision
trade: a calibrated lower-frequency estimator, a refocused/depth-partitioned
reader with measured focus/exposure costs, or a different baseline/observation
geometry that rechecks occlusion. The next useful investigation is whether
larger baseline can buy height sensitivity with coarser patterns *without losing
low caps beside high terrain*; it is not permission for a new aperture sweep.
No camera/projector/lens was selected or priced. The 24-frame timing, whole-board
resident parts, unchanged-neighbor support, hidden-cap unknowns, neutral
preparation and optional unprinted E-281 remain unchanged. E-291 retains24 frames
at assumed0.1s/frame: local1/4/8 groups cost2.4/9.6/19.2s; dense scans of
1024/4096/6400 cells cost614.4/2457.6/3840s before motion/exposure/retries, against
the~30s gameplay reference. Minimum/raised neutral retain their actual40/50mm
travel and paid preparation. No new resident parts or assembly operations; the
1024/4096/6400 threaded pairs retain unresolved support/manufacture/service.
Custom optics remain unpriced against~$500 purchased-parts,~$1000 finished-value
and$1000–1500 demonstrator references; no purchased budget or hardware pass.
A hypothetical focus stack multiplies acquisition and adds settling/calibration;
none of those operations may be hidden inside the assumed0.1s frame time.
