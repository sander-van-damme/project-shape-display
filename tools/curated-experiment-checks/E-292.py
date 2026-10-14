#!/usr/bin/env python3
"""Fixed circular-pupil, incoherent paraxial projector screen, not real optics.

Units mm, angular frequency cycles per radian (paraxial slope). Standard library.
No guessed process distribution. Camera/aberrations/noise/indirect paths omitted.
"""
import json
import math

WAVELENGTH = .00055  # assumed monochromatic green, not measured source
D = 300.


def otf(aperture, frequency, inverse_defocus, samples=512):
    """Normalized complex-pupil autocorrelation (real by radial symmetry).

    P(x,y)=exp(i*pi*delta*(x*x+y*y)/lambda) inside radius a/2.
    Two pupils are displaced by s=lambda*frequency. Integrate their overlap;
    phase difference is 2*pi*delta*frequency*x. Preserve contrast reversals.
    """
    if frequency == 0:
        return 1.
    radius = aperture/2
    shift = WAVELENGTH*frequency
    if shift >= aperture:
        return 0.
    extent = radius-shift/2
    step = extent/samples
    total = sum(math.sqrt(max(0., radius**2-((i+.5)*step+shift/2)**2))
                * math.cos(2*math.pi*inverse_defocus*frequency*(i+.5)*step)
                for i in range(samples))
    return 4*step*total/(math.pi*radius**2)


def analytic_focus(aperture, frequency):
    u = WAVELENGTH*frequency/aperture
    return 0. if u >= 1 else 2/math.pi*(math.acos(u)-u*math.sqrt(1-u*u))


def screen(stroke, dq):
    near, far = D-stroke, D
    # Harmonic focus minimizes maximum absolute inverse-distance defocus.
    t0 = 2*near*far/(near+far)
    delta = (1/near-1/far)/2
    frequency = 1/(4*dq)  # finest reflected-Gray bit repeats 0011
    apertures = [.05*(30/.05)**(i/240) for i in range(241)]
    offsets = [delta*i/40 for i in range(41)]
    scored = [(min(otf(a,frequency,d) for d in offsets),a) for a in apertures]
    score,a = max(scored)
    coarse = [otf(a,frequency,d) for d in offsets]
    fine = [otf(a,frequency,d,1024) for d in offsets]
    # Separate diameter diagnostic, deliberately NOT PSF width addition or MTF.
    # Angular geometric circle=a*delta; in-focus Airy first-zero diameter=2.44*l/a.
    equal_a = math.sqrt(2.44*WAVELENGTH/delta)
    diameter_angle = math.sqrt(2.44*WAVELENGTH*delta)
    # Each diameter <= one bin requires these mutually compatible apertures.
    lower_a, upper_a = 2.44*WAVELENGTH/dq, dq/delta
    return dict(stroke_mm=stroke, angular_bin=dq, focus_distance_mm=t0,
                max_inverse_defocus_per_mm=delta,
                required_aperture_for_Airy_le_bin_mm=lower_a,
                maximum_aperture_for_defocus_le_bin_mm=upper_a,
                one_bin_diameter_conditions_compatible=lower_a<=upper_a,
                balanced_aperture_mm=equal_a,
                balanced_diagnostic_diameter_mm_at_z25=275*diameter_angle,
                best_sampled_aperture_mm=a,
                best_sampled_min_signed_fundamental_transfer=score,
                finest_bit_only_fundamental=a<=3*WAVELENGTH*frequency,
                finest_bit_peak_endpoint_contrast=(4/math.pi*abs(otf(a,frequency,delta))
                    if a<=3*WAVELENGTH*frequency else None),
                focus_transfer=otf(a,frequency,0),
                endpoint_transfer=otf(a,frequency,delta),
                max_quadrature_difference=max(abs(x-y) for x,y in zip(coarse,fine)),
                projector_z0_bin_mm=D-8/(8/D+dq))


def main():
    # Independent closed-form overlap area, cutoff and conjugate symmetry.
    errors=[]
    for a in (.2,1,4,12):
        for fraction in (0,.01,.1,.3,.7,.99,1,1.1):
            f=fraction*a/WAVELENGTH
            errors.append(abs(otf(a,f,0,2048)-analytic_focus(a,f)))
            assert otf(a,f,.0002)==otf(a,f,-.0002)
    assert max(errors)<3e-6
    assert otf(1,1/WAVELENGTH,0)==0
    rows=[]
    for stroke in (40.,50.):
        for name,dq in [('old_2048_bins_in_0.05',.05/2048)]+[
            (str(p)+'mm_four_caps',max(w,(3*p+w)*1080/1920)/250/1080)
            for p,w in ((5.08,4.4),(6.35,4.4),(12.7,10.3))]:
            row=screen(stroke,dq);row['field']=name
            assert row['max_quadrature_difference']<1e-4
            rows.append(row)
    # Binning control: same optics model, fewer absolute addresses.
    control=screen(50.,.0005)
    assert control['best_sampled_min_signed_fundamental_transfer']>.5
    print(json.dumps(dict(assumptions='550nm incoherent uniform circular pupil; '
        'paraxial on-axis; harmonic focus; perfect camera, no noise/aberrations',
        search='241 log apertures .05..30mm; 41 inverse-depth offsets; '
        '512/1024 quadrature; sampled design screen, not global bound',
        focused_overlap_max_error=max(errors),rows=rows,
        coarse_control=control),indent=2))


if __name__=='__main__':
    main()
