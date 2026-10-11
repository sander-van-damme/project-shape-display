#!/usr/bin/env python3
"""E-151 necessary-condition screens; mm, N, MPa. No hardware priors."""
import itertools
import json
import math


def plastic_drag(E, sy, b, t, R):
    """Stabilized symmetric curvature cycle, work per feed length [N]."""
    return b * sy / R * max(t - 2 * sy * R / E, 0) ** 2


def fiber_cycle(E, sy, b, t, R, fibers=128, steps=128):
    # 1-mm material length; midpoint section fibers; elastic-perfect-plastic law.
    y = [(i + .5) * t / fibers - t / 2 for i in range(fibers)]
    plastic = [0.] * fibers
    stress = [0.] * fibers
    strain = [0.] * fibers
    area = b * t / fibers
    records = []
    for cycle in range(3):
        work = heat = 0.
        start_energy = sum(s*s/(2*E)*area for s in stress)
        for a, z in zip([0., 1/R, 0., -1/R], [1/R, 0., -1/R, 0.]):
            for k in range(1, steps+1):
                curvature = a + (z-a)*k/steps
                for i, yi in enumerate(y):
                    eps = curvature * yi
                    trial = E * (eps-plastic[i])
                    sig = max(-sy, min(sy, trial))
                    p = eps-sig/E
                    heat += sy*abs(p-plastic[i])*area
                    work += .5*(stress[i]+sig)*(eps-strain[i])*area
                    plastic[i], stress[i], strain[i] = p, sig, eps
        energy = sum(s*s/(2*E)*area for s in stress)
        records.append(dict(work_N=work, dissipation_N=heat,
                            elastic_change_N=energy-start_energy,
                            residual_N=work-heat-energy+start_energy))
    return records[-1]


def arch_height(r, l=4.):
    return math.sqrt(l*l-r*r)


def first_channels(events, local_s, reserve=6.):
    for h in range(1, events+1):
        if reserve + math.ceil(events/h)*local_s < 30:
            return h
    raise ValueError("No schedule under 30 s")


def factorization_check(n):
    # Exact witness with n terms: term k owns column k. Others <= zero.
    a = [[40. if i == k else 0. for k in range(n)] for i in range(n)]
    b = [[0. if j == k else -40. for j in range(n)] for k in range(n)]
    h = [[max(a[i][k]+b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    assert h == [[40. if i == j else 0. for j in range(n)] for i in range(n)]
    # Any rank-one term obeys rectangle identity; two 40-mm diagonals force
    # offdiagonal sum 80. With |error|<=e and no term exceeding target+e,
    # this contradicts offdiagonal sum <=2e whenever e<20 mm.
    for i in range(n):
        for j in range(n):
            for k in range(n):
                assert a[i][k]+b[k][i]+a[j][k]+b[k][j] == a[i][k]+b[k][j]+a[j][k]+b[k][i]
    return dict(size=n, minimum_terms_below_20mm_error=n,
                physical_row_column_registers=2*n*n,
                independent_coordinates_after_gauge=2*n*n-n,
                candidate_support_intersections=n**3)


def main():
    out = {}
    # Independent constitutive check vs exact integrated hysteresis area.
    nominal = (200000., 200., 3., .25, 3.)
    exact = plastic_drag(*nominal)
    refinements = []
    for n in (32, 64, 128, 256):
        r = fiber_cycle(*nominal, fibers=n, steps=n)
        refinements.append(dict(resolution=n, exact_N=exact, **r))
    assert abs(refinements[-1]['dissipation_N']-exact) < .001
    assert abs(refinements[-1]['residual_N']) < .001
    assert abs(fiber_cycle(200000., 200., 3., .25, 1000.)['dissipation_N']) < 1e-10
    assert plastic_drag(200000., 200., 3., .25, 1000.) == 0
    assert abs(plastic_drag(2e12, 200., 3., .25, 3.)/(200*3*.25**2/3)-1) < 1e-7
    out['plastic_refinement'] = refinements
    # Two named material scenarios, not claims about actual PLA or a metal alloy.
    materials = [('polymer_low', 2000., 20.), ('polymer_high', 2000., 50.),
                 ('metal_low', 200000., 200.), ('metal_high', 200000., 500.)]
    rows = []
    for name, E, sy in materials:
        for cap in (.005, .02):
            b, t = 3., .4
            R = t/(2*cap)
            rows.append(dict(material=name, strain_cap=cap, radius_mm=R,
                             drag_N=plastic_drag(E, sy, b, t, R)))
    out['strain_bound_best_sections'] = rows
    # Coherent material/geometry/assembly boxes. No fractions interpreted as yield.
    forces = []
    strains = []
    for b,t,R,E,sy in itertools.product((2.9,3.1),(.2,.3),(2.8,3.2),
                                       (160000.,240000.),(160.,240.)):
        forces.append(plastic_drag(E,sy,b,t,R)); strains.append(t/(2*R))
    out['plastic_32_corners'] = dict(drag_N=[min(forces),max(forces)],
                                     outer_strain=[min(strains),max(strains)])
    # Optimistic constant-drag surrogate only; NOT conversion-front cut dynamics.
    out['nominal_front'] = dict(drag_N=exact, outer_strain=.25/6,
        plastic_work_full_map_J=256*exact,
        surrogate_zero_load_coast_mm=1000*.5*.02*.1**2/exact,
        surrogate_10N_coast_mm=1000*.5*1.1*.1**2/(exact-10))
    # Beaded arch: common loop fixes r1+r2, leaves antisymmetric mode free.
    l,r=4.,2.
    h=arch_height(r,l)
    curvature=-2*l*l/h**3
    differences=[]
    for dx in (.1,.01,.001):
        v=arch_height(r+dx,l)+arch_height(r-dx,l)
        differences.append((dx,(v-2*h)*2/dx**2))
    assert abs(differences[-1][1]-curvature)<1e-6
    # virtual-work gradient for asymmetric loads, and all positive-load corners.
    slope=(10.-1.)*r/h
    fd=(arch_height(r+1e-5)+10*arch_height(r-1e-5)
        -arch_height(r-1e-5)-10*arch_height(r+1e-5))/(2e-5)
    assert abs(fd-slope)<1e-8
    curvatures=[]
    for L,R,W in itertools.product((3.9,4.1),(1.9,2.1),(.02,1.,10.)):
        curvatures.append(-2*W*L*L/arch_height(R,L)**3)
    out['bead_shared_loop'] = dict(height_mm=h, equal_1N_curvature_N_per_mm=curvature,
        refinement=differences, unequal_1_10N_slope_N=slope,
        coherent_curvature_range=[min(curvatures),max(curvatures)],
        energy_change_at_0p5mm_Nmm=arch_height(2.5)+arch_height(1.5)-2*h,
        zero_load_exchange_energy_mJ=.5*.02*.1**2*1000)
    out['factor_support']=[factorization_check(n) for n in (2,8,80)]
    schedules=[]
    for v in (.05,.1,.2):
        for return_stroke in (False,True):
            local=.04/v*(2 if return_stroke else 1)+.10
            H=first_channels(6400,local)
            schedules.append(dict(v_m_s=v, empty_return=return_stroke, local_s=local,
                heads=H,time_s=6+math.ceil(6400/H)*local,
                bought_head_ceiling_with_250_shared_USD=250/H))
    out['front_schedules']=schedules
    out['ledgers']=dict(cells=6400,pitch_mm=5.08,travel_mm=40,
        die_contacts_if_four_each=25600,former_assembly_hours_10_to_30s=[6400*10/3600,6400*30/3600],
        free_heads_cell_ceiling_USD=250/6400,
        strip_volume_L_at_80x3x0p25mm=6400*80*3*.25/1e6,
        all_cells_1_10N_frame_load_N=[6400,64000],
        allowance_per_12800_factor_register=250/12800,
        expected_missed_cells_if_p_1e_4=6400*1e-4)
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
