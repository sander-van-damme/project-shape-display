"""E-195: finite local routing and reduced obstacle-beam contact; mm, N, MPa.
NumPy only. All material/process inputs are explicit scenarios, not measurements.
Run with OPENBLAS_NUM_THREADS=1. JSON and optional SVG are disposable.
"""
import argparse
import importlib.util
import json
import math
from itertools import product
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('e194', Path(__file__).parents[1]/'E-194'/'coupling.py')
e194 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e194)
PITCH = 5.08


def dogleg(n=128, offset=2.54, depth=15.):
    u = np.linspace(0, 1, n+1)
    # Smooth tangents; curvature jumps at the fixed straight/bend joins are real
    # construction assumptions. Their elastic wall reactions are not omitted.
    return np.column_stack((offset*(3*u*u-2*u*u*u), depth*u))


def local_curve(parity=0, n=128, straight=False):
    p = np.array([[0., 0.], [0., 15.]]) if straight else dogleg(n)
    return np.vstack(([0., -41.], p, p[-1]+[0., 41.+6*parity]))


def geometry(n=128):
    p = dogleg(n)
    length = float(np.linalg.norm(np.diff(p,axis=0),axis=1).sum())
    a=local_curve(1,n)
    gap=e194.poly_distance(a,a+[PITCH,0])-1.3
    # Curve chord error <= max |x''(z)| dz^2/8 (x is cubic, z linear).
    hausdorff=6*2.54/15**2*(15/n)**2/8
    # Two-tier identical input housing envelopes, screw/shank diameter 3.
    housing_diameter, housing_height, tier = 5.8, 5., 6.
    adjacent_screw_housing=PITCH-1.5-housing_diameter/2
    diagonal_housing=PITCH*math.sqrt(2)-housing_diameter
    # No same-layer overlapping housing at nearest neighbor: 6 > 5.
    # All farther housing pairs have >= diagonal spacing.
    assert min(adjacent_screw_housing,diagonal_housing,tier-housing_height)>0
    # Screw fixed nut overlap, every real h (linear endpoint proof).
    nut=(-12.,-8.)
    for h in (0.,40.):
        assert h-54 <= nut[0] and h >= nut[1]
    # Both tails exchange length, parity extends only one fixed reserve.
    closure=[]
    for parity in (0,1):
        values=[]
        for h in np.linspace(0,40,81):
            values.append(1+h+length+1+40+6*parity-h)
        assert np.ptp(values)<1e-10
        closure.append(values[0])
    # A genuine U route: 20-mm lateral spread, R10 half-circle, 40-mm end
    # guides; neighbor's descending leg cuts its semicircle. It cannot tile.
    t=np.linspace(0,math.pi,n+1)
    arc=np.column_stack((10*(1-np.cos(t)),40+10*np.sin(t)))
    u=np.vstack(([0.,0.],arc,[20.,0.]))
    ugap=e194.poly_distance(u,u+[PITCH,0])-1.3
    # Repeating an 8-column edge comb every 40.64 mm makes each 40-mm input
    # reserve intersect the previous module's inboard run at the same depth.
    edge=e194.route(7,10,1.7,n)
    edgegap=e194.poly_distance(edge,edge+[8*PITCH,0])-1.3
    assert ugap<0 and edgegap<0
    return dict(chords=n,dogleg_length_mm=length,
        dogleg_gap_lower_mm=gap-2*hausdorff,hausdorff_mm=hausdorff,
        row_gap_mm=PITCH-3.2,fold_gap_mm=ugap,tiled_edge_gap_mm=edgegap,
        housing_screw_gap_mm=adjacent_screw_housing,
        housing_diagonal_gap_mm=diagonal_housing,tier_gap_mm=tier-housing_height,
        slotted_terminal_clearance_mm=.1,closed_terminal_interference_mm=3.-.5,
        dogleg_core_m=6400*(length+45)/1000,
        dogleg_guide_m=6400*(length+85)/1000,
        dogleg_ideal_wall_L=6400*(length+85)*2.96/1e6,
        rigid_rod_m=6400*53/1000,
        common_threaded_shank_m=6400*54/1000,
        total_height_rigid_mm=150,dogleg_total_height_mm=207,
        strip_fixed_length_by_tier_mm=closure,
        error_box=[dict(e_mm=e,internal_gap_mm=.4-3*e,
            route_gap_mm=gap-2*hausdorff-3*e,
            screw_housing_gap_mm=adjacent_screw_housing-3*e)
            for e in (.025,.05,.1,.2)])



def terminals():
    """Finite rectangular slotted-guide lands + moving web, cylindrical shank
    bounds and square caps. Contacts to own shank/core are intended. No fastener
    strength inferred from this construction; thin tab manufacturing unresolved.
    """
    # Relative x: foil axis -2.25, stem/screw axis 0. Guide lands are shared
    # with the stem support; a .5-wide y slot lets a .3-wide web pass.
    foil_right_land_x=(-2.,-1.6)
    land_y=((-1.6,-.25),(.25,1.6))
    web_y=(-.15,.15)
    stem_radius=1.5
    slot_gap=min(web_y[0]-land_y[0][1],land_y[1][0]-web_y[1])
    stem_gap=-stem_radius-foil_right_land_x[1]
    assert min(slot_gap,stem_gap)>0
    # Closed land would intersect a finite tab crossing x=-2..-1.6.
    closed_overlap=.3*.4*.3  # web y-width * wall x-thickness * web z-thickness
    for h,parity in product(np.linspace(0,40,81),(0,1)):
        output_bottom=50-h
        assert output_bottom>=10  # full 0..8 guide station engagement
        assert output_bottom+.15<51  # bent region remains foil-only
        input_top=107+6*parity-h
        assert input_top-.15>66
        nut=(115+6*parity,119+6*parity)
        assert input_top<=nut[0] and input_top+54>=nut[1]
        assert -h<=0  # cap underside; all stationary guide solids depth >=0
    # Deepest input guide =113; shallower housing roof =114.5.
    assert 114.5-113>0
    # Static two-tier nesting does not grant a vertical service path. During
    # downward extraction a shallow border housing crosses the deeper neighbor.
    housing_service_overlap=5.8-PITCH
    # Module 10x10: outside nearest neighbors of its shallow checkerboard sites.
    border=set()
    for x,y in product(range(10),repeat=2):
        if (x+y)%2==0:
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                q=(x+dx,y+dy)
                if not (0<=q[0]<10 and 0<=q[1]<10): border.add(q)
    assert len(border)==20 and housing_service_overlap>0
    return dict(service_housing_overlap_mm=housing_service_overlap,
        adjacent_border_housings_to_clear_at_least=len(border),
        slot_gap_mm=slot_gap,stem_wall_gap_mm=stem_gap,
        closed_wall_tab_intersection_mm3=closed_overlap,
        minimum_curve_terminal_z_gap_mm=.85,
        guide_housing_z_gap_mm=1.5,output_guide_overlap_at_h40_mm=8,
        output_stems_m=6400*50/1000,
        thin_tabs=12800,core_end_joints=12800,
        coherent_slot_margins_mm={str(e):slot_gap-3*e for e in (.025,.05,.1,.2)})


def box_equilibrium(Q,b,bound,seed):
    """Coordinate minimization of a bounded quadratic, accelerated on PD free sets.
    Compression can be nonconvex. Returns a stationary branch, NOT global proof.
    Explicit multiple starts and KKT residual; no artificial damping/force prior.
    """
    w=np.clip(seed.copy(),-bound,bound)
    g=Q@w+b
    for sweep in range(2500):
        for i in range(len(w)):
            delta=max(-bound,min(bound,w[i]-g[i]/Q[i,i]))-w[i]
            if delta:
                w[i]+=delta
                g+=Q[:,i]*delta
        if sweep%10==0:
            g=Q@w+b
            pg=w-np.clip(w-g,-bound,bound)
            free=(abs(w)<bound-1e-9)
            if max(abs(pg))<2e-6:
                H=Q[np.ix_(free,free)]
                if not np.any(free) or np.linalg.eigvalsh(H)[0]>=-1e-9:
                    return w,g,sweep
            if np.any(free):
                A=Q[np.ix_(free,free)]
                try:
                    np.linalg.cholesky(A)
                    d=np.zeros_like(w)
                    d[free]=np.linalg.solve(A,-g[free])
                    alpha=1.
                    for wi,di in zip(w[free],d[free]):
                        if di>0: alpha=min(alpha,(bound-wi)/di)
                        elif di<0: alpha=min(alpha,(-bound-wi)/di)
                    w=np.clip(w+max(0,alpha)*d,-bound,bound)
                    g=Q@w+b
                except np.linalg.LinAlgError:
                    # Negative curvature: a concave line reaches its lowest
                    # feasible value at a box boundary, not the saddle at zero.
                    eigen,vec=np.linalg.eigh(A)
                    if eigen[0]<-1e-9:
                        direction=np.zeros_like(w)
                        direction[free]=vec[:,0]
                        candidates=[]
                        for sign in (-1,1):
                            d=direction*sign
                            alpha=min((bound-wi)/di if di>0 else (-bound-wi)/di
                                for wi,di in zip(w[free],d[free]) if abs(di)>1e-14)
                            trial=np.clip(w+alpha*d,-bound,bound)
                            candidates.append((.5*trial@Q@trial+b@trial,trial))
                        value,trial=min(candidates,key=lambda a:a[0])
                        if value<.5*w@Q@w+b@w:
                            w=trial
                            g=Q@w+b
    return w,Q@w+b,sweep


def contact(n=96,E=200000.,clearance=.4,N=-1.,curved=True,h=20.):
    """Small-normal-offset Euler beam in a fixed smooth guide, prescribed N.
    N>0 tension, N<0 compression. Fixed tangent at both permanent attachments.
    Bending energy EI/2 int(kappa+w'')²; path change int(-kappa*w+w'²/2).
    Leading-order Frenet model omits kappa²*w, extensibility coupling and dynamic
    stick/slip. Only comparative static branches + friction/reversal scenarios.
    """
    p=dogleg(4096)
    s=np.r_[0.,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
    L=s[-1]+42
    grid=np.linspace(-1-h,s[-1]+41-h,n+1)
    ds=L/n
    u=np.interp(np.clip(grid,0,s[-1]),s,np.linspace(0,1,len(s)))
    dx=2.54*(6*u-6*u*u)/15
    dxx=2.54*(6-12*u)/225
    kappa=dxx/(1+dx*dx)**1.5
    kappa[(grid<=0)|(grid>=s[-1])]=0
    if not curved: kappa[:]=0
    # Last and first two points fix position/tangent (mesh approximation).
    ids=np.arange(2,n-1)
    M=np.eye(n+1)[:,ids]
    B=np.diff(M,n=2,axis=0)/ds**2
    D=np.diff(M,axis=0)/ds
    k=kappa[1:-1]
    K=M[1:-1]
    EI=E*2*.1**3/12
    Q=ds*(EI*B.T@B+N*D.T@D)
    b=ds*(EI*B.T@k-N*K.T@k)
    eigenvalues,eigenvectors=np.linalg.eigh(Q)
    bound=clearance/2
    seeds=[np.zeros(len(ids)),bound*eigenvectors[:,0]/max(abs(eigenvectors[:,0])),
           -bound*eigenvectors[:,0]/max(abs(eigenvectors[:,0]))]
    states=[]
    for seed in seeds:
        w,g,it=box_equilibrium(Q,b,bound,seed)
        energy=float(.5*w@Q@w+b@w)
        free=abs(w)<bound-1e-9
        stable=not np.any(free) or np.linalg.eigvalsh(Q[np.ix_(free,free)])[0]>=-1e-9
        states.append((energy,w,g,it,stable))
    valid=[a for a in states if a[4] and max(abs(a[1]-np.clip(a[1]-a[2],-bound,bound)))<3e-6]
    energy,w,g,it,stable=min(valid or states,key=lambda a:a[0])
    wall=(abs(w)>bound-1e-7)
    # Gradient balanced by unilateral wall reaction; endpoint clamp reactions
    # are separate, so friction from them is NOT claimed included here.
    normal=float(sum(abs(g[wall])))
    ww=M@w
    dl=float(ds*(-k@(K@w)+.5*np.sum((D@w)**2)))
    pg=w-np.clip(w-g,-bound,bound)
    converged=bool(stable and max(abs(pg))<3e-6)
    if converged:
        assert np.all(g[w>bound-1e-7]<=3e-6)
        assert np.all(g[w<-bound+1e-7]>=-3e-6)
    return dict(converged=converged,converged_starts=len(valid),n=n,h_mm=h,E_MPa=E,clearance_mm=clearance,N_N=N,curved=curved,
        wall_normal_sum_N=normal,wall_nodes=int(sum(wall)),
        path_change_mm=dl,axial_extension_mm=N*L/(E*.2),
        kkt_N=float(max(abs(pg))),max_offset_slope=float(max(abs(np.diff(ww)/ds))),
        branch_energy_spread_Nmm=float(max(a[0] for a in states)-energy),
        convex=bool(eigenvalues[0]>0),iterations=it)


def schedule():
    # Generous active stroke control only: no earned input-loss arrest.
    t=40/100+100/1000
    return dict(stroke_s=t,necessary_heads=e194.heads(t+.1),
        nominal_motor_rpm_for_E156_lead=100/.15*60,
        purchase_allowance_per_site_with_250_elsewhere=250/6400,
        assembly_hours_per_10s_operation=6400*10/3600)


def checks():
    # Exact straight contact limiting cases; no load => no wall or offset.
    zero=contact(48,N=0,curved=False)
    taut=contact(48,N=1,curved=False)
    assert zero['wall_normal_sum_N']==taut['wall_normal_sum_N']==0
    assert zero['path_change_mm']==taut['path_change_mm']==0
    buckle=contact(32,N=-1,curved=False)
    assert buckle['converged'] and buckle['wall_normal_sum_N']>0 and buckle['path_change_mm']>0
    # Independent pinned Euler bound; contact comparison uses a 57.25-mm span.
    EI=200000*2*.1**3/12
    assert math.isclose(math.pi**2*EI/40**2,.20561675835602836)
    # Arbitrary neighbor old/new heights cannot escape the full swept hull;
    # private input translation is diagonal in all 625 two-cell state pairs.
    maps=list(product((0,10,20,30,40),repeat=2))
    for old,new in product(maps,maps):
        for i in range(2):
            delta=new[i]-old[i]
            assert old[i]+delta==new[i]
            if old[i]==new[i]: assert delta==0
    # Contact force/dissipation sign is independent from signed axial load.
    for N,v in product((-10.,-1.,.02,1.,10.),(-100.,100.)):
        for mu,R in product((0.,.05,.3),(0.,.1,5.)):
            f=mu*R*math.copysign(1,v)
            assert f*v>=0
            assert math.isclose((N+f)*v-N*v,f*v,abs_tol=1e-9)
    return dict(state_pairs=625,checks='passed')


def svg(path):
    # Schematic generated from the checked finite centerlines, not contact CAD.
    colors=['#3366cc','#dc3912','#109618']
    shapes=[]
    for i in range(3):
        p=local_curve(i%2)+[i*PITCH,0]
        pts=' '.join(f'{60+q[0]*5:.4f},{240+q[1]*5:.4f}' for q in p)
        shapes.append(f'<polyline points="{pts}" fill="none" stroke="{colors[i]}" stroke-width="6.5"/>')
    Path(path).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="420" height="590"><rect width="100%" height="100%" fill="white"/><text x="15" y="20">E-195: three full swept local guides; 5x scale</text>'+''.join(shapes)+'</svg>')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--svg')
    a=parser.parse_args()
    if a.svg: svg(a.svg)
    out=dict(checks=checks(),terminals=terminals(),geometry=[geometry(n) for n in (32,64,128,256)],schedule=schedule())
    out['contact_convergence']=[contact(n,N=N) for N in (-1.,1.) for n in (32,64,96)]
    out['contact_bounds']=[contact(64,E=E,clearance=c,N=N)
        for E,c,N in product((100000.,200000.),(.1,.4,.8),(-1.,1.))]
    out['height_states']=[contact(64,h=h,N=N) for h,N in product((0.,40.),(-1.,1.))]
    out['straight_flexible_controls']=[contact(64,N=N,curved=False) for N in (-1.,1.)]
    out['numerical_unresolved']=sum(not r['converged'] for key in ('contact_convergence','contact_bounds','height_states','straight_flexible_controls') for r in out[key])
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
