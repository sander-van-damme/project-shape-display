"""E-138: fixed-M finite cylinders; SI internally, no steel or process model."""
import json
import math
from functools import lru_cache
import numpy as np

MU0 = 4e-7 * math.pi
BR = 1.21  # Arnold N35 typical; sensitivity is a scenario, not a grade tolerance.
R = .002
L = .002
P = .00508

@lru_cache(None)
def surface(nt, nz):
    theta = (np.arange(nt) + .5) * 2 * math.pi / nt
    z = (np.arange(nz) + .5) * L / nz - L / 2
    th, zz = np.meshgrid(theta, z)
    pts = np.column_stack((R*np.cos(th.ravel()), R*np.sin(th.ravel()), zz.ravel()))
    # Unit-direction pole charges, sigma=M dot n, times physical side area.
    q = BR/MU0 * R*(2*math.pi/nt)*(L/nz) * np.column_stack((np.cos(th.ravel()), np.sin(th.ravel())))
    return pts, q

def coupling(offset, nt=64, nz=12):
    """U=a.T C b; a/b=(cos phase,sin phase); no spurious pair factor 1/2."""
    pts, q = surface(nt, nz)
    dst = pts + np.asarray(offset)
    out = np.zeros((2, 2))
    for i in range(0, len(pts), 128):
        dist = np.linalg.norm(pts[i:i+128, None, :] - dst[None, :, :], axis=2)
        out += q[i:i+128].T @ ((1/dist) @ q)
    return MU0/(4*math.pi)*out

def capacity(c):
    # For each head angle, maximize over receiver angle; singular values bound
    # that torque amplitude through a complete head revolution.
    s = np.linalg.svd(c, compute_uv=False)
    return [float(s[-1]*1000), float(s[0]*1000)]

def checks():
    conv = []
    for nt,nz in [(32,6),(64,12),(128,24)]:
        c = coupling((0,0,L+.0003),nt,nz)
        n = coupling((P,0,0),nt,nz)
        conv.append({'mesh':[nt,nz], 'target_Nmm':capacity(c), 'resident_Nmm':capacity(n)})
    assert np.max(np.abs(c - np.eye(2)*c[0,0])) < 1e-12
    assert abs(conv[-1]['target_Nmm'][0]/conv[-2]['target_Nmm'][0]-1)<.002
    assert abs(conv[-1]['resident_Nmm'][1]/conv[-2]['resident_Nmm'][1]-1)<.002
    # Far-field independent dipole energy, axial and off-axis.
    m=BR/MU0*math.pi*R*R*L
    errs=[]
    for v in [np.array([0.,0.,.1]),np.array([.1,0.,0.]),np.array([.06,.08,.1])]:
        d=np.linalg.norm(v); u=v/d
        dip=MU0*m*m/(4*math.pi*d**3)*(np.eye(2)-3*np.outer(u[:2],u[:2]))
        errs.append(float(np.linalg.norm(coupling(tuple(v))-dip)/np.linalg.norm(dip)))
    assert max(errs)<.003
    # Reciprocity and independent finite derivative of U with receiver angle.
    off=(.0002, .0001, L+.0005)
    c=coupling(off)
    assert np.allclose(c,coupling(tuple(-v for v in off)).T,rtol=1e-10,atol=1e-14)
    a=np.array([math.cos(.7),math.sin(.7)])
    def energy(b): return float(a@c@np.array([math.cos(b),math.sin(b)]))
    b=.3; eps=1e-5
    tau=-float(a@c@np.array([-math.sin(b),math.cos(b)]))
    assert abs(tau+(energy(b+eps)-energy(b-eps))/(2*eps))<1e-11
    angles=np.linspace(0,2*math.pi,4097)
    torques=np.array([-float(a@c@np.array([-math.sin(t),math.cos(t)])) for t in angles])
    assert abs(float(np.trapz(torques,angles)))<1e-12
    assert np.linalg.norm(coupling((0,0,L+.001))) < np.linalg.norm(coupling((0,0,L+.0003)))
    return {'convergence':conv,'far_dipole_relative_errors':errs,'energy_reciprocity_checks':'pass'}

def run():
    result={'checks':checks()}
    cases=[]
    # Coherent bank gap/registration scenarios, not Monte Carlo process priors.
    for gap in [.0003,.0006,.001]:
        for dx in [0.,.00025,.0005]:
            target=coupling((dx,0,L+gap))
            neighbors=[coupling((dx+sx*P,sy*P,L+gap)) for sx,sy in [(1,0),(-1,0),(0,1),(0,-1)]]
            cases.append({'gap_mm':gap*1000,'head_offset_mm':dx*1000,
                          'target_Nmm_min_max':capacity(target),
                          'worst_head_to_neighbor_Nmm':max(capacity(c)[1] for c in neighbors)})
    result['head_cases']=cases
    resident=[coupling((sx*P,sy*P,0)) for sx,sy in [(1,0),(-1,0),(0,1),(0,-1)]]
    phases=np.linspace(0,2*math.pi,1441)
    adverse=[]
    for phase in phases:
        tangent=np.array([-math.sin(phase),math.cos(phase)])
        # Independently choose each parked rotor phase against selected motion.
        adverse.append(sum(np.linalg.norm(c.T@tangent) for c in resident)*1000)
    analytic=2*math.sqrt(2)*float(np.linalg.norm(np.diag(resident[0])))*1000
    assert abs(max(adverse)-analytic)<1e-10
    tangent=np.array([-math.sin(math.pi/4),math.cos(math.pi/4)])
    witness=[(c.T@tangent)/np.linalg.norm(c.T@tangent) for c in resident]
    # With tau=-a_perp C b, these fixed parked phases oppose positive rotation.
    witness_torque=-sum(float(tangent@c@b) for c,b in zip(resident,witness))*1000
    assert abs(witness_torque+analytic)<1e-10
    result['four_resident_neighbors']={'one_pair_Nmm_min_max':capacity(resident[0]),
         'fixed_parked_phase_deg':[float(math.degrees(math.atan2(b[1],b[0]))) for b in witness],
         'analytic_adverse_sum_Nmm':analytic,
         'worst_adverse_sum_Nmm':float(max(adverse)), 'selected_phase_deg':float(phases[np.argmax(adverse)]*180/math.pi)}
    result['remanence_factors']={str(f):f*f for f in [.9,1.,1.1]}
    result['attraction_pressure_bound']=[{'B_T':b,'force_6mm2_N':b*b*6e-6/(2*MU0),
        'two_gap_AT_0.3mm':b*2*.0003/MU0,'two_gap_AT_1mm':b*2*.001/MU0} for b in [.2,.4,.8]]
    result['rack']={'torque_Nmm_at_1_3.27_10N':[3.6*f for f in [1,3.27,10]],
        'turns_per_40mm':40/(2*math.pi*3.6),'work_J_board_at_1_3.27_10N':[256*f for f in [1,3.27,10]]}
    times=[]
    for v in [.1,.4,1.]:
        for dwell in [.005,.020]:
            # Explicit conditional allocations, not earned by magnetic calculation.
            k=next(k for k in range(1,6401) if 6+math.ceil(6400/k)*(.04/v+dwell)<30)
            times.append({'speed_m_s':v,'event_s':dwell,'heads':k,'time_s':6+math.ceil(6400/k)*(.04/v+dwell)})
    result['conditional_schedule']=times
    result['stationary_magnet_volume_cm3']=6400*math.pi*R*R*L*1e6
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
