#!/usr/bin/env python3
"""E-287: explicit-hole coupled Morley plate; mm/N/MPa. Numerical screen only.
Requires numpy, scipy, scikit-fem (tested versions printed). No generated files.
Explicit polygonal circles and square-cut geometry controls; no certified bounds.
"""
import argparse
import json
import importlib.util
import numpy as np
import scipy
import skfem
from scipy.sparse.linalg import splu
from skfem import MeshTri, Basis, ElementTriMorley, BilinearForm, LinearForm
from skfem.helpers import dd, ddot, trace
from pathlib import Path

spec = importlib.util.spec_from_file_location('strip', Path(__file__).with_name('E-287-sheet.py'))
strip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(strip)
L, P, N, T, E, NU = 406.4, 12.7, 32, 6., 70000., .33
D = E*T**3/(12*(1-NU**2))


def solve_plate(hole=3.6, refine=0, edges='simple', circular=False):
    # Quarter symmetry: 16x16 complete cells. Mirror w, zero normal slope on
    # x=0,y=0; outer x=L/2,y=L/2 supported or clamped. Hole boundaries free.
    H = L/2
    a = hole if hole else 3.6  # same solid-control triangulation
    axis = np.unique(np.concatenate([np.array([j*P, (j+.5)*P-a/2,
                       (j+.5)*P+a/2, (j+1)*P]) for j in range(N//2)]))
    m = MeshTri.init_tensor(axis, axis)
    if hole:
        mid = m.p[:, m.t].mean(axis=1)
        inside = np.all(np.abs(mid % P-P/2) < hole/2-1e-8, axis=0)
        m = m.remove_elements(np.flatnonzero(inside))
    m = m.refined(refine)
    if circular and hole:
        nodes = np.unique(m.facets[:,m.boundary_facets()])
        nodes = nodes[np.all((m.p[:,nodes]>1e-8)&(m.p[:,nodes]<H-1e-8),axis=0)]
        xy = m.p.copy()
        centers = (np.floor(xy[:,nodes]/P)+.5)*P
        radial = xy[:,nodes]-centers
        xy[:,nodes] = centers+radial*(hole/2/np.linalg.norm(radial,axis=0))
        m = MeshTri(xy,m.t)
    b = Basis(m, ElementTriMorley(), intorder=4)
    @BilinearForm
    def stiffness(u,v,w):
        return D*((1-NU)*ddot(dd(u),dd(v))+NU*trace(dd(u))*trace(dd(v)))
    K = stiffness.assemble(b)
    outer = b.get_dofs(lambda x: np.isclose(x[0],H) | np.isclose(x[1],H))
    sym = b.get_dofs(lambda x: np.isclose(x[0],0) | np.isclose(x[1],0))
    fixed = np.union1d(outer.all() if edges=='clamped' else outer.all('u'), sym.all('u_n'))
    free = np.setdiff1d(np.arange(b.N),fixed)
    lu = splu(K[free][:,free].tocsc())
    area = float(b.dx.sum())
    @LinearForm
    def unit(v,w): return v
    unitload = unit.assemble(b)
    # Resident weight smeared over remaining material; discrete collar stress
    # is deliberately excluded. Fixed total resident and bed weight in controls.
    bed_force = (L*L-N*N*np.pi*3.6**2/4)*T*strip.RHO*9.81
    loads = {'resident':unitload*(N*N*.06/4/area),
             'bed_weight':unitload*(bed_force/4/area),
             'dense_extra':unitload*(N*N*(.338-.06)/4/area)}
    # 16 miniatures, each 20 g on 25.4 mm square; mirror four placements.
    # Scenario, not measured miniature mass/distribution. Also cluster same mass.
    for layout in ['spread','cluster']:
        starts = [2*P,10*P] if layout=='spread' else [0,2*P]
        def on_patch(x):
            mask = np.zeros(x.shape[1:],dtype=bool)
            for sx in starts:
                for sy in starts:
                    mask |= (x[0]>=sx)&(x[0]<=sx+2*P)&(x[1]>=sy)&(x[1]<=sy+2*P)
            return mask
        @LinearForm
        def patch(v,w): return on_patch(w.x)*v
        f = patch.assemble(b)
        # Four 20 g minis per quarter: normalize by translational work.
        massload = f[b.nodal_dofs[0]].sum()
        loads[layout] = f*(4*.020*9.81/massload)
    out = {}
    solutions = {}
    for name, f in loads.items():
        u = np.zeros(b.N)
        u[free] = lu.solve(f[free])
        resid = K@u-f
        assert np.linalg.norm(resid[free])/np.linalg.norm(f[free]) < 1e-5
        solutions[name] = u
        out[name] = float(u[b.nodal_dofs[0]].max())
    base = solutions['resident']+solutions['bed_weight']
    out['baseline'] = float(base[b.nodal_dofs[0]].max())
    for name in ['spread','cluster','dense_extra']:
        out['baseline_plus_'+name] = float((base+solutions[name])[b.nodal_dofs[0]].max())
    # Whole-sheet reaction balance, excluding derivative generalized loads.
    f = loads['resident']+loads['bed_weight']
    reaction = (K@base-f)[b.nodal_dofs[0]].sum()
    assert abs(reaction+f[b.nodal_dofs[0]].sum())/(bed_force/4+N*N*.06/4)<1e-5
    out.update(hole=hole,circular=circular,area_quarter_mm2=area,refine=refine,edges=edges,dofs=int(b.N),triangles=int(m.nelements),
               total_baseline_N=N*N*.06+bed_force)
    return out


def service():
    # State-order proof only: grip/contact and damage are NOT qualified here.
    bodies = set(range(1024)); stored = set(); guides = 2
    screw_bed_and_keeper = True
    def may_remove_guide():
        return not bodies and screw_bed_and_keeper
    assert not may_remove_guide()
    for i in range(1024):
        assert guides==2 and screw_bed_and_keeper
        gripped = True  # physical prerequisite, not inferred from motor command
        assert gripped  # release thread only after shared tool takes body
        bodies.remove(i); stored.add(i)
        if i<1023:
            assert not may_remove_guide()  # one jammed body blocks removal
    assert may_remove_guide() and len(stored)==1024
    guides -= 1
    assert guides==1 and screw_bed_and_keeper
    return {'body_transfer_actions':2048,
            'transfer_hours_10_30s':[2048*s/3600 for s in [10,30]],
            'thread_disengage_reengage_events':2048,
            'storage_trays':32,'channels_per_tray':32,
            'tray_stack_litres':32*406.4*150*16/1e6,
            'over_body_sleeve_gap_each_side_mm':(10.8-10.3)/2,
            'known_bad_target':'guide removal blocked until body/fragments safely cleared',
            'resident_N':1024*.06}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--refine',type=int,default=0)
    p.add_argument('--hole',type=float,default=3.6)
    p.add_argument('--edges',choices=['simple','clamped'],default='simple')
    p.add_argument('--circle',action='store_true')
    p.add_argument('--check',action='store_true'); args=p.parse_args()
    if args.check:
        solid=solve_plate(0,args.refine)
        analytical=strip.solid_plate(N,P,T,solid['total_baseline_N']/N**2)
        assert abs(solid['baseline']/analytical-1)<.02
        r,lo,hi=strip.midpoint(N,P,3.6,T,.06,'vertical')
        assert lo<r<hi
        print(json.dumps({'solid':solid,'navier_baseline':analytical,
                          'independent_strip_resident':r,'service':service(),
                          'versions':[np.__version__,scipy.__version__,skfem.__version__]},indent=2))
    else:
        print(json.dumps(solve_plate(args.hole,args.refine,args.edges,args.circle),indent=2))
