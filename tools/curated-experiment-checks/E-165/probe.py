#!/usr/bin/env python3
"""E-165 finite sheet sections and bounded feed screen. Units: mm, N, MPa.
Prescribed elastic shapes are tested for intersection, NOT solved contact states.
All modulus/drag/imperfection boxes are assumptions, not process distributions.
"""
import itertools
import json
import math

H, PATCH, WIDTH, PITCH = 40.0, 20.0, 2.0, 5.08


def smooth(u):
    u = min(1., max(0., u))
    return u*u*(3-2*u)


def section(j, n, t, gap, h, closed, z, tail=2.):
    """y coordinate or None; even sheets grounded, odd sheets move with runner.
    Ground fingers bend from patch top to a spine above the entire moving sweep.
    Moving fingers bend from bottom attachment to patch, then have free straight tips.
    Sheet bodies have finite y thickness t and x width WIDTH, not zero-width lines.
    """
    offset = j-n
    opened = offset*(t+gap)
    packed = offset*(t+(1-closed)*gap)
    if j % 2 == 0:
        root = H+PATCH+tail+2
        if not 0 <= z <= root:
            return None
        return packed+(opened-packed)*smooth((z-PATCH)/(root-PATCH))
    root, tip = h-H-tail, h+PATCH+tail
    if not root <= z <= tip:
        return None
    return opened+(packed-opened)*smooth((z-root)/(-root))


def collision(n, t=.05, gap=.1, h=40., closed=1., steps=256):
    worst = (0., None)
    # Analytic breakpoints plus uniform samples within the upper shared extent.
    zs = {0., PATCH, h+PATCH+2, 30.}
    zs.update((h+PATCH+2)*i/steps for i in range(steps+1))
    for z in sorted(zs):
        ys = [section(j,n,t,gap,h,closed,z) for j in range(2*n+1)]
        for j in range(2*n):
            if ys[j] is None or ys[j+1] is None:
                continue
            overlap = t-abs(ys[j+1]-ys[j])
            if overlap > worst[0]+1e-12:
                worst = overlap, {'z':z,'layers':[j,j+1], 'y':[ys[j],ys[j+1]]}
    return {'overlap_mm':worst[0], 'witness':worst[1]}


def sheet_graph(cells, n, bridges=(), locked=()):
    """Axial incremental constraints: rigid ties and ideal no-slip clamps.
    Each node's connected component shares displacement, not absolute height.
    Grounded combs share a fixed spine. Removed bridges contribute no edge.
    This tests topology only; it grants rigid frames and adequate clamp force.
    """
    parent = {}

    def root(node):
        parent.setdefault(node, node)
        if parent[node] != node:
            parent[node] = root(parent[node])
        return parent[node]

    def tie(a, b):
        parent[root(a)] = root(b)

    for i in range(cells):
        runner = ('runner', i)
        root(runner)
        for j in range(2*n+1):
            leaf = ('leaf', i, j)
            tie(leaf, 'ground' if j % 2 == 0 else runner)
        if i in locked:
            # A sticking local interface grounds the runner's axial increment.
            tie(('leaf', i, 1), ('leaf', i, 0))
    for i, k in bridges:
        # Even one remaining rigid ligament on one moving sheet couples runners.
        tie(('leaf', i, 1), ('leaf', k, 1))
    return {node: root(node) for node in list(parent)}


def compatible(graph, increments):
    values = {graph['ground']: 0.}
    for i, delta in enumerate(increments):
        component = graph[('runner', i)]
        if component in values and values[component] != delta:
            return False
        values[component] = delta
    return True


def connectivity_witness():
    results = {}
    for name, bridges in (('permanent', ((0,1),(1,2))),
                          ('removed', ()), ('residual_0_1', ((0,1),))):
        graph = sheet_graph(3, 2, bridges)
        reachable = [list(h) for h in itertools.product((0.,H), repeat=3)
                     if compatible(graph, h)]
        local = []
        for selected in range(3):
            held = [i for i in range(3) if i != selected]
            locked_graph = sheet_graph(3, 2, bridges, held)
            move = [H if i == selected else 0. for i in range(3)]
            if compatible(locked_graph, move):
                local.append(selected)
        results[name] = {'reachable_endpoint_maps': reachable,
                         'locally_movable_cells_neighbors_locked': local}
    # Explicit counterexamples, not a stored cardinality.
    assert len(results['permanent']['reachable_endpoint_maps']) == 2
    assert results['permanent']['locally_movable_cells_neighbors_locked'] == []
    assert len(results['removed']['reachable_endpoint_maps']) == 8
    assert results['removed']['locally_movable_cells_neighbors_locked'] == [0,1,2]
    assert len(results['residual_0_1']['reachable_endpoint_maps']) == 4
    assert results['residual_0_1']['locally_movable_cells_neighbors_locked'] == [2]
    # Board-tile consequence without enumerating 2**40 maps.
    for name, bridges in (('removed', ()), ('one_residual_bridge', ((19,20),))):
        graph = sheet_graph(40, 2, bridges)
        free = {graph[('runner', i)] for i in range(40)} - {graph['ground']}
        results[name+'_40_cell_tile'] = {'axial_dofs': len(free),
                                         'reachable_endpoint_maps': 2**len(free)}
    assert results['removed_40_cell_tile']['axial_dofs'] == 40
    assert results['one_residual_bridge_40_cell_tile']['axial_dofs'] == 39
    # A supported zero increment remains compatible for every clamp pattern.
    for locks in itertools.product((False, True), repeat=3):
        graph = sheet_graph(3, 2, locked=[i for i, on in enumerate(locks) if on])
        assert compatible(graph, [0.,0.,0.])
    return results


def euler(E,t,length,K=1.):
    return math.pi**2*E*WIDTH*t**3/(12*(K*length)**2)


def feed_limit(E,t,length,gap,imperfection,K=1.):
    """Pinned sinusoidal-mode magnification w=e/(1-P/Pcr), as an explicit model.
    Lateral allowance gap/2. K variants are alternative end-restraint scenarios.
    Does not claim nonlinear post-contact capacity; zero allowance means no clear feed.
    """
    pcr=euler(E,t,length,K)
    return pcr*max(0., 1-2*imperfection/gap)


def self_check():
    assert smooth(0)==0 and smooth(1)==1
    for n in (1,2,3,6,12):
        assert collision(n,closed=0)['overlap_mm']<1e-10
        for h in (0,20,40):
            lo,hi=h-H-2,h+PATCH+2
            assert min(hi,PATCH)-max(lo,0)==PATCH
            # Carrier remains below all ground fingers; spine above moving tip.
            assert lo<=-2 and hi<=62
    assert collision(1)['overlap_mm']==0
    assert collision(2)['overlap_mm']==0
    assert collision(3)['overlap_mm']>.01
    # Independent analytic witness for inner grounded layer 4 and moving layer 5.
    s=smooth(10/44)
    yg=.05+.1*s
    ym=.1
    assert abs(section(4,3,.05,.1,40,1,30)-yg)<1e-12
    assert abs(section(5,3,.05,.1,40,1,30)-ym)<1e-12
    assert .05-abs(ym-yg)>.01
    # Euler Rayleigh quotient for a pinned sine: quadrature independent of formula.
    N=4096; E=200000.; t=.05; L=42.; I=WIDTH*t**3/12
    num=den=0.
    for k in range(N):
        x=(k+.5)*L/N
        num+=(math.pi/L)**4*math.sin(math.pi*x/L)**2*L/N
        den+=(math.pi/L)**2*math.cos(math.pi*x/L)**2*L/N
    assert abs(E*I*num/den/euler(E,t,L)-1)<1e-12
    assert abs(euler(E,2*t,L)/euler(E,t,L)-8)<1e-12
    assert feed_limit(E,t,L,.1,.05)==0
    # Fixed-guided beam force/work identity for prescribed lower flexure.
    d=.1; a=2.; k=12*E*I/a**3
    assert abs(.5*k*d*d-6*E*I*d*d/a**3)<1e-12


def main():
    self_check()
    results={}
    # Witness at full height plus refinement: sampled maximum is not certified max.
    results['section_collisions']={n:collision(n) for n in (1,2,3,6,12)}
    results['refinement_n3']={s:collision(3,steps=s)['overlap_mm'] for s in (64,256,1024)}
    results['exact_n3_z30_overlap_mm']=.1*smooth(10/44)
    # All 8 combinations of 0/40 mm on 3 adjacent cells, independently open/closed.
    # Slots remove transverse ligaments below a rigid shared spine; x extent is fixed.
    states=0
    for heights in itertools.product((0,40),repeat=3):
        for clamps in itertools.product((0,1),repeat=3):
            for h,c in zip(heights,clamps):
                assert collision(2,h=h,closed=c,steps=64)['overlap_mm']<1e-10
                assert h-H-2<=-2 and h+PATCH+2<=62
            states+=1
    results['neighbor_witness']={'height_maps':8, 'clamp_maps':8,
        'states_checked':states,
        'minimum_x_clearance_with_2p8_carriers_mm':PITCH-2.8,
        'overlap_mm':PATCH, 'spine_rigid_assumption':True}
    results['sheet_connectivity']=connectivity_witness()
    results['feed']=[{'E_MPa':E,'t_mm':t,'Pcr_leaf_N':euler(E,t,42),
        'clear_feed_leaf_N':feed_limit(E,t,42,.1,.01),
        'per_interface_drag_limit_N':feed_limit(E,t,42,.1,.01)/2}
        for E,t in ((2000,.05),(200000,.05),(2000,.4))]
    # Coherent geometry bounds: all 2n interface gaps narrow together.
    # Each neighboring surface has bounded deviation w; b is relative anchor/slot bias.
    results['clearance_boxes']=[{'nominal_gap_mm':g,'surface_bound_mm':w,
        'relative_bias_mm':b,'worst_gap_mm':g-2*w-b,
        'required_stroke_upper_bound_n2_mm':4*(g+2*w+b)}
        for g,w,b in ((.1,.01,.02),(.1,.03,.04),(.1,.05,.05),(.2,.03,.04))]
    # Sensitivity only; fractions of corners have no statistical meaning.
    corners=[]
    for E,t,K,e,g in itertools.product((2000,200000),(.05,.1,.4),(.5,1,2),(.0,.01,.05),(.1,.2)):
        corners.append(feed_limit(E,t,42,g,e,K))
    results['feed_length_sensitivity_N']={L:euler(200000,.05,L) for L in (42,62,64)}
    results['feed_corner_count']=len(corners)
    results['feed_corner_range_N']=[min(corners),max(corners)]
    results['n2_clamp_scenarios']=[{'load_N':F,'mu':mu,'squeeze_N':F/(4*mu),
        'pressure_MPa':F/(4*mu*WIDTH*PATCH)} for F in (1,10) for mu in (.05,.2,.4)]
    # n2: moving offsets -1,+1; each must shift gap at shortest 2-mm lower flexure.
    results['lower_flexure_n2']=[{'E_MPa':E,'t_mm':t,
        'strain':3*t*.1/2**2,'each_end_force_N':E*WIDTH*t**3*.1/2**3}
        for E,t in ((200000,.05),(2000,.4))]
    results['inventory']={}
    for n in (1,2,3,6,12):
        # 40 columns/tile, 160 tiles: stays below 256-mm bed width before fixtures.
        sheet_area=160*40*PITCH*((n+1)*66+n*68)/1e6
        results['inventory'][n]={'moving_leaves':6400*n,'friction_interfaces':12800*n,
            'local_clamps':6400,'stationary_comb_sheets':160*(n+1),
            'temporary_moving_carrier_sheets':160*n,'moving_leaf_attachments':6400*n,
            'rectangle_sheet_area_m2':sheet_area,
            'sheet_only_budget_USD_per_m2':250/sheet_area,
            'open_stack_plus_two_0p8_cheeks_mm':(2*n+1)*.05+2*n*.1+1.6}
    # Frame discrepancy: simply supported common beam, uniformly spread 10 N/cell.
    # A deflection beyond small-deflection validity is a diagnostic, not a prediction.
    Eframe=2000.; If=5*10**3/12
    results['common_frame_deflection_diagnostic_mm']={span:5*(10/PITCH)*span**4/(384*Eframe*If)
        for span in (40*PITCH,10*PITCH,4*PITCH)}
    results['timing']={}
    for step in (.45,.50,.55):
        heads=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*step<30)
        results['timing'][step]={'heads':heads,'time_s':6+math.ceil(6400/heads)*step}
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    main()
