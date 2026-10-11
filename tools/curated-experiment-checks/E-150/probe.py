#!/usr/bin/env python3
"""Compile/run E-150 in run-owned scratch; stdout JSON is disposable.
Python stdlib + NumPy + C++17 compiler. No process distributions or CAD claims.
"""
import concurrent.futures
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
import numpy as np

HERE = Path(__file__).resolve().parent
# N W0 W1 mu kt kframe/kg amplitude phase direction Q frequency dt on off v0 kb
BASE = [6, 1, 1, .1, 20e6, .001, 1, 0, 1, 40, 40000, 5e-8, .03, .12, 0, 0]
KEYS = ['N','W','neighbor_W','mu','kt','coupling','amplitude','phase',
        'direction','Q','frequency','dt','on','off','v0','bridge']

def params(**kw):
    p = BASE.copy()
    for k,v in kw.items(): p[KEYS.index(k)] = v
    return p

def checks_and_bounds():
    # Exact translated finite runner/pad envelopes, with conservative 10-um
    # tangential mode bound, at endpoints and all extrema of the affine sweep.
    min_land = min(x for q in (0,.04) for x in
                   (q+.002-.0005-1e-5, -.0005-(q-.042)-1e-5))
    assert min_land > .00148
    # Contact compression is material deformation; x does not enlarge runner.
    # Hard side pad 1x1x.4 mm at x=+/-1 mm; adjacent cells translated 5.08 mm.
    pad_clearance = .00508-2*(.001+.0004+1e-5)
    assert pad_clearance > .002
    # A front/back yoke can skirt a 2-mm square runner, but this does NOT
    # establish its required stiffness, modal mass, guide or docking package.
    yoke_runner_gap = .0016-.001-1e-5
    assert yoke_runner_gap > 0
    # Soft metal cantilever comparison, explicitly selected E and dimensions.
    E,b,L,ks = 200e9,.002,.01,60e3
    h=(4*ks*L**3/(E*b))**(1/3)
    preload = [{"N":N,"spring_compression_mm":N/ks*1e3,
                "cantilever_stress_MPa":6*N*L/(b*h*h)/1e6,
                "stored_spring_J_pair":N*N/ks,
                "contact_compression_um":N/60e6*1e6}
               for N in (6,60)]
    # Independent 2-foot static solve checks parked AND docked gap sensitivity.
    for kb in (0,60e6,600e6):
        for dock in (0,25e6):
            dg=1e-8
            K=np.eye(2)*(60e6+ks+dock)+kb*np.ones((2,2))
            x=np.linalg.solve(K,np.full(2,-60e6*dg/2))
            dN=60e6*(x+dg/2)
            analytic=.5*60e6*(ks+dock+2*kb)/(60e6+ks+dock+2*kb)*dg
            assert np.max(np.abs(dN-analytic))<1e-12
    # Permanent-resident-friction + translating captured head comparator:
    # head must supply useful lift and friction, absorb on lowering if W>C.
    control=[]
    for N,W,m in ((6,1,.12),(6,0,.02),(60,10,1.1)):
        C=2*.1*N
        control.append(dict(N=N,W=W,raise_force_N=W+C,
                            lower_signed_up_force_N=W-C,
                            heat_per_40mm_J=C*.04,
                            coast_from_down_0p1_mps_mm=m*.1**2/(2*(C-W))*1e3))
    schedule=[]
    for v in (.025,.05,.059,.075,.1,.2):
        # Extra 30-ms startup and 120-ms off/proof budget, neither earned.
        site=.04/v+.05+.03+.12
        H=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*site<30)
        schedule.append(dict(v=v,H=H,head_purchase_ceiling=250/H))
    # E-149 ideal sliding comparator at the old imposed amplitudes.
    theta=(np.arange(65536)+.5)*2*np.pi/65536
    N=60;Na=90;U=2*np.pi*40000*1e-6
    normals=np.maximum(N+Na*np.cos(theta[:,None]+[0,np.pi]),0)
    velocities=U*np.cos(theta[:,None]+[0,np.pi])
    ideal=float(np.mean(np.sum(.1*normals*np.sign(velocities),axis=1)))
    assert abs(ideal-10.401)<.001
    return dict(min_land_mm=min_land*1e3,pad_clearance_mm=pad_clearance*1e3,
                yoke_runner_gap_mm=yoke_runner_gap*1e3,leaf_thickness_mm=h*1e3,
                soft_preload=preload,direct_sliding=control,schedule=schedule,
                docked_soft_total_gap_for_20pct_preload_um=1.2/(.5*60e6*(60e3+25e6)/(60e6+60e3+25e6))*1e6,
                bridge_total_gap_for_20pct_preload_um=[
                    dict(kb=kb, tolerance_um=1.2/(.5*60e6*(60e3+2*kb)/(60e6+60e3+2*kb))*1e6)
                    for kb in (0,60e6,600e6)],
                ideal_E149_stall_N=ideal)

def main():
    cases={
      'nominal':params(), 'zero':params(W=0,neighbor_W=0),
      'lower':params(direction=-1), 'strong':params(N=60,W=10,neighbor_W=10),
      'strong_lower':params(N=60,W=10,neighbor_W=10,direction=-1),
      'isolated_loaded_neighbor':params(coupling=0),
      'unloaded_neighbor':params(neighbor_W=0),
      'weak_friction':params(mu=.02), 'strong_friction':params(mu=.3),
      'soft_tangent':params(kt=2e6), 'hard_tangent':params(kt=60e6),
      'frame_003':params(coupling=.03), 'frame_01':params(coupling=.1),
      'frame_01_unloaded':params(coupling=.1,neighbor_W=0),
      'long_ringdown':params(Q=200),
      'bridge':params(bridge=60e6),
      'stiff_bridge':params(bridge=600e6,dt=2.5e-8),
      'stiff_bridge_lower':params(bridge=600e6,direction=-1,dt=2.5e-8),
      'stall_fixture':params()+[1],
      'frame_01_unloaded_fine':params(coupling=.1,neighbor_W=0,dt=2.5e-8),
      'stiff_bridge_fine':params(bridge=600e6,dt=1.25e-8),
      'strong_fine':params(N=60,W=10,neighbor_W=10,dt=2.5e-8),
      'drive_disabled':params(amplitude=0),
      'zero_coast':params(W=0,neighbor_W=0,amplitude=0,v0=.1,on=.000025),
      'loss_of_hold':params(mu=.02,amplitude=0),
      'conservative':params(W=0,neighbor_W=0,amplitude=0,v0=.0001,Q=1e99,on=.001,off=.001),
      'long_drive':params(on=.09),
      'converge_100ns':params(dt=1e-7),
      'converge_25ns':params(dt=2.5e-8),
      'converge_12p5ns':params(dt=1.25e-8),
    }
    for preload,phase,coupling in ((.8,-.2,.001),(.8,.2,.03),(1.2,-.2,.03),(1.2,.2,.001)):
        cases[f'common_{preload}_{phase}_{coupling}']=params(N=6*preload,phase=phase,coupling=coupling)
    # Independent mirrored zero-load trajectory (external downward loads absent).
    cases['zero_reverse']=params(W=0,neighbor_W=0,direction=-1)
    scratch=os.environ.get('PAPERCLIP_RUN_SCRATCH_DIR') or os.environ.get('PAPERCLIP_SCRATCH_DIR')
    with tempfile.TemporaryDirectory(prefix='E-150-',dir=scratch) as temp:
        exe=str(Path(temp)/'contact')
        subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',
                        str(HERE/'contact.cpp'),'-o',exe],check=True)
        def run(item):
            name,p=item
            r=json.loads(subprocess.check_output([exe,*map(str,p)]))
            assert all(math.isfinite(x) for x in r.values()),name
            assert r['max_foot_t']<1e-5,name
            assert r['max_normal_mode']<1e-5,name
            return name,dict(parameters=dict(zip(KEYS+['external_stall'],p)),**r)
        results=dict(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(run,cases.items()))
    assert results['drive_disabled']['neighbor_max']<1e-12
    assert results['isolated_loaded_neighbor']['neighbor_max']<1e-12
    assert abs(results['zero']['y_drive']+results['zero_reverse']['y_drive'])<1e-10
    assert abs(results['conservative']['energy_residual_J'])<1e-10
    assert results['weak_friction']['final_v']<-.1
    coast=results['zero_coast']
    assert abs(coast['y_drive']+coast['post_max']-.02*.1**2/(2*1.2))<1e-6
    assert results['stall_fixture']['y_drive']==0
    assert results['stall_fixture']['work_J']>0
    assert results['stiff_bridge_fine']['min_total_N']>12
    assert abs(results['frame_01_unloaded']['neighbor_max']-
               results['frame_01_unloaded_fine']['neighbor_max'])<1e-6
    coarse=results['converge_100ns'];fine=results['converge_12p5ns']
    assert abs(coarse['v_drive']-fine['v_drive'])<.001
    assert abs(fine['energy_residual_J'])/fine['positive_driver_J']<.004
    print(json.dumps(dict(bounds=checks_and_bounds(),cases=results),indent=2))

if __name__=='__main__': main()
