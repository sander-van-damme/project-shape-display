#!/usr/bin/env python3
"""E-196: ideal conservation bounds, not electrochemical/contact simulation.
Standard library; deterministic corners, no calibrated manufacturing priors.
Units: geometry mm, N, s; gas law internally SI; j in A/cm^2.
"""
import itertools
import json
import math

FARADAY = 96485.33212  # C/mol
GAS_R = 8.314462618  # J/(mol K)
CU_MOLAR = 63.546  # g/mol
CU_RHO = 0.00896  # g/mm^3
CU_QV = 2 * FARADAY * CU_RHO / CU_MOLAR  # C/mm^3, Cu(II), eta=1
N = 6400
H = 40.0
P_ATM = 101325.0
TEMP = 298.15
OVERHEAD = 6.0  # explicit optimistic complete-map allowance; not demonstrated


def growth_speed(j, eta=1.0):
    return eta * (j / 100.0) / CU_QV  # mm/s, normal to active surface


def bulk(load, modulus=110000.0, stress=100.0):
    # Optimistic solid circular pinned-pinned strut: I=A^2/(4*pi).
    # Buckling is only a sizing comparison; full lateral guidance could remove it.
    area = max(load / stress, math.sqrt(4 * load * H**2 / (math.pi * modulus)))
    q = CU_QV * area * H
    return dict(load_N=load, area_mm2=area, diameter_mm=math.sqrt(4*area/math.pi),
                Q_cell_C=q, sum_cell_current_A=N*q/(30-OVERHEAD))


def gas(area, load, extra_load=0.1, h=H, dead=1.0, temp=TEMP):
    a_si = area * 1e-6
    p = P_ATM + load / a_si
    # Retain a baseline dead-volume inventory; charge only the added stroke.
    q = 4 * FARADAY * p * a_si * h * 1e-3 / (3 * GAS_R * temp)
    h2 = (h + dead) * p / (p + extra_load / a_si) - dead
    return dict(area_mm2=area, load_N=load, pressure_Pa=p, Q_cell_C=q,
                sum_cell_current_A=N*q/(30-OVERHEAD),
                drop_mm=h-h2, stiffness_N_per_mm=(P_ATM*a_si+load)/(h+dead))


def key(gap, depth, width, j, error=0.0, eta=1.0, r=1.2, strength=10.0):
    # One-sided deposition fills a finite annular groove in an insulating frame.
    # Initially bare finished shaft r; full stripping restores the same envelope.
    d = gap + depth
    vol = math.pi * ((r + d)**2-r*r) * width
    q = CU_QV * vol / eta
    # c and k each receive two independent facing-surface errors of +/-e.
    # Enumerate realizable radius corners; no IID averaging or yield claim.
    corners=[]
    for er,el,eo in itertools.product((-error,error),repeat=3):
        shaft,lip,outer=r+er,r+gap+el,r+d+eo
        clear,overlap=lip-shaft,outer-lip
        cap=min(2*math.pi*shaft*width,
                math.pi*max(0.0,outer**2-lip**2))*strength
        corners.append((clear,overlap,cap,outer+.5<2.54))
    clear=min(x[0] for x in corners)
    overlap=min(x[1] for x in corners)
    cap=min(x[2] for x in corners)
    return dict(gap_mm=gap, depth_mm=depth, width_mm=width, j_A_cm2=j,
                error_mm=error, clear_mm=clear, overlap_mm=overlap,
                capacity_N=cap, Q_one_way_cell_C=q,
                sum_cell_current_roundtrip_A=2*N*q/(30-OVERHEAD),
                ideal_map_s=OVERHEAD+2*d/growth_speed(j,eta),
                # Grant arbitrary growth speed control, eta and stripping symmetry.
                radial_screen=clear>1e-12 and overlap>1e-12 and all(x[3] for x in corners))


def synthesized_key(error, j, load=1.0, strength=10.0, r=1.2):
    # Continuous radial sizing holdout against coarse grid; 1 um reserve is
    # deliberately optimistic and unqualified. Exact worst bearing corner.
    c=2*error+.001
    k=error+math.sqrt((r+c+error)**2+load/(math.pi*strength))-(r+c)+.001
    w=max(.1,load/(2*math.pi*(r-error)*strength)+.001)
    return key(c,k,w,j,error,r=r,strength=strength)


def annulus_intersection(a, b):
    """Exact axisymmetric box intersection (ri,ro,zlo,zhi), mm^3."""
    ri, ro = max(a[0],b[0]), min(a[1],b[1])
    dz = max(0.0,min(a[3],b[3])-max(a[2],b[2]))
    return math.pi*max(0.0,ro*ro-ri*ri)*dz if ro>ri else 0.0


def checks():
    # Independent molar mass balance for 1 mm^3 and one coulomb.
    assert math.isclose((CU_QV/(2*FARADAY))*CU_MOLAR, CU_RHO)
    assert math.isclose(growth_speed(1)*100*CU_QV, 1.0)
    # Radial growth: integrate actual changing cylindrical area/current;
    # midpoint integration is exact for area linear in radius.
    r,w,d,j = 1.2,0.25,0.10,1.0
    exact_q = CU_QV*math.pi*((r+d)**2-r*r)*w
    residuals=[]
    for steps in (1,10,100,1000):
        dt=(d/growth_speed(j))/steps
        q=sum(j/100*2*math.pi*(r+(i+.5)*d/steps)*w*dt for i in range(steps))
        residuals.append(abs(q-exact_q))
        assert math.isclose(q,exact_q,rel_tol=1e-12)
    # Concrete locked/clear section: at z=0..w metal occupies groove, then
    # a 0.01 mm upward shift intersects its grounded upper lip. Stripped shaft
    # clears all lip sweeps through 40 mm. No adhesion/contact strength granted.
    gap,depth,w = .05,.05,.25
    lip=(r+gap,r+gap+depth+.5,w,w+1)
    deposit=(r,r+gap+depth,0,w)
    assert annulus_intersection(deposit,lip)==0
    moved=(deposit[0],deposit[1],.01,w+.01)
    locked_overlap=annulus_intersection(moved,lip)
    assert locked_overlap>0
    lower_lip=(lip[0],lip[1],-1,0)
    assert math.isclose(annulus_intersection((r,r+gap+depth,-.01,w-.01),lower_lip),locked_overlap)
    for z in (-40,-1,0,.01,1,40):
        assert annulus_intersection((0,r,z,z+50),lip)==0
    # Gas n conserved with load change; finite-difference stiffness converges.
    g=gas(math.pi,1.0)
    p=g['pressure_Pa']; a=math.pi*1e-6
    stiffness_errors=[]
    for dh in (.1,.01,.001):
        dp=p*((H+1)/(H+1-dh)-1)
        stiffness_errors.append(abs(dp*a/dh-g['stiffness_N_per_mm']))
    assert stiffness_errors[-1]<stiffness_errors[0]/90
    assert gas(math.pi,1,extra_load=0)['drop_mm']==0
    assert gas(math.pi,1,h=0)['Q_cell_C']==0
    g2=gas(math.pi,1,extra_load=.1)
    h2=H-g2['drop_mm']
    assert math.isclose(p*(H+1),(p+.1/a)*(h2+1),rel_tol=1e-12)
    # Euler and stress sizing independent back substitution.
    for load in (.1,1,10):
        x=bulk(load); area=x['area_mm2']
        pe=math.pi**2*110000*(area*area/(4*math.pi))/H**2
        assert pe>=load*(1-1e-12) and load/area<=100
    for e in (.005,.025,.05):
        holdout=synthesized_key(e,10)
        assert holdout['radial_screen'] and holdout['capacity_N']>1
    return dict(radial_charge_residual_C=residuals,
                gas_stiffness_error_N_per_mm=stiffness_errors,
                locked_lip_intersection_mm3=locked_overlap)


def main():
    grid=[key(c,k,w,j,e,eta) for c,k,w,j,e,eta in itertools.product(
        (.005,.01,.025,.05,.1),(.01,.025,.05,.1),(.1,.25,1),
        (.175,1,10),(.005,.025,.05),(.5,1))]
    summaries=[]
    for e,j in itertools.product((.005,.025,.05),(.175,1,10)):
        cases=[x for x in grid if x['error_mm']==e and x['j_A_cm2']==j
               and x['radial_screen'] and x['capacity_N']>=1]
        passing=[x for x in cases if x['ideal_map_s']<30]
        summaries.append(dict(e_mm=e,j_A_cm2=j,geometry_capacity_cases=len(cases),
                              passing=len(passing),best_s=min((x['ideal_map_s'] for x in cases),default=None)))
    # Illustrative gas retention decay and shared temperature shift, not priors.
    decay=[dict(half_life_s=t,time_to_0p1mm_s=-math.log(1-.1/(H+1))*t/math.log(2))
           for t in (30,300,3600)]
    target=.1; extra=.1
    needed_effective_force=extra*((H+1)/target-1)
    out=dict(checks=checks(),Cu_C_per_mm3=CU_QV,
             bulk=[bulk(w) for w in (.1,1,10)],
             axial_growth_40mm_s={str(j):H/growth_speed(j) for j in (.175,1,10)},
             gas=[gas(a,w) for a,w in itertools.product((math.pi,4*math.pi),(.1,1,10))],
             gas_decay=decay,gas_temperature_5K_shift_mm=(H+1)*5/TEMP,
             gas_effective_force_for_0p1mm_N=needed_effective_force,
             gas_required_radius_at_load1_mm=math.sqrt((needed_effective_force-1)/(P_ATM*1e-6)/math.pi),
             nominal_keys=[key(.05,.05,.25,j) for j in (.175,1,10)],
             grid_cases=len(grid),grid_summary=summaries,
             continuous_holdout=[synthesized_key(e,j) for e,j in itertools.product((.005,.025,.05),(1,10))],
             # A micron-scale switch may control a dry latch; it is not a grown support.
             thin_neck_roundtrip_s={str(j):2*.001/growth_speed(j) for j in (.175,1,10)})
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
