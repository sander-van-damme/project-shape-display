"""Deterministic necessary-condition screen; all scenario values are assumptions.
Run from any directory. No probability, supplier price or hardware claim.
"""
import json
from math import ceil, pi

N, TRAVEL = 80, 40.0  # cells/axis, mm
# Shared scenario shifts apply to every cell, not independent random draws.
SCENARIOS = {
    'favorable': dict(v=400., rpm=6000., index=.025, contact=.04, read=.01, overhead=2., retry=0),
    'reference': dict(v=200., rpm=3000., index=.05, contact=.08, read=.02, overhead=4., retry=1),
    'adverse': dict(v=80., rpm=1000., index=.10, contact=.16, read=.04, overhead=8., retry=8),
}
# Descriptors distinguish physical principles; lanes are parameter variants.
FAMILIES = {
    'rack_pawl': dict(memory='positive tooth latch', energy='linear gripper', load='pawl into local grid', bought_cells=0, interfaces=3),
    'screw': dict(memory='thread angle', energy='rotary socket', load='nut into local grid', bought_cells=0, interfaces=2),
    'hydraulic_lock': dict(memory='trapped liquid', energy='pressure/return manifold', load='fluid and closed valve', bought_cells=1, interfaces=3),
}

def motion(family, s, lead):
    if family == 'screw':
        return TRAVEL / lead * 60. / s['rpm']
    # Rack gripper must return; fluid supply must refill: no free reset.
    return 2 * TRAVEL / s['v']

def evaluate(family, lanes, scenario, lead=1., region=(80, 80), reserve=200.):
    s = SCENARIOS[scenario]
    stations = region[0] * ceil(region[1] / lanes)
    dwell = motion(family, s, lead) + s['contact'] + s['read']
    seconds = s['overhead'] + stations * (dwell + s['index']) + s['retry'] * dwell
    # Reserve is for all common frame/motion/power/sensing/electronics hardware.
    # Residual must buy head assemblies AND any repeated bought cell parts.
    residual = 500. - reserve
    return dict(family=family, lanes=lanes, scenario=scenario, lead_mm=lead,
                stations=stations, seconds=round(seconds, 4), timing_pass=seconds < 30.,
                residual_dollars=residual, max_head_dollars_if_cells_free=round(residual / lanes, 4),
                max_cell_dollars_if_heads_free=round(residual / (N*N), 6),
                repeated_interfaces=FAMILIES[family]['interfaces'] * N*N)

def checks():
    # Independent hand calculation: 80*(.2+.04+.01+.025)+2 = 24 seconds.
    assert evaluate('rack_pawl',80,'favorable')['seconds'] == 24.
    assert evaluate('rack_pawl',40,'favorable')['seconds'] == 46.
    assert evaluate('rack_pawl',80,'favorable',region=(1,1))['stations'] == 1
    assert evaluate('rack_pawl',8,'favorable',region=(5,5))['stations'] == 5
    assert motion('screw',SCENARIOS['favorable'],1.) == .4
    assert motion('screw',SCENARIOS['favorable'],4.) == .1
    assert all(evaluate(f,80,'adverse')['seconds'] > evaluate(f,80,'reference')['seconds'] for f in FAMILIES)
    # Self-locking necessary friction bound for a square thread, ignoring collars.
    assert abs(4/(pi*3) - .4244131816) < 1e-9

if __name__ == '__main__':
    checks()
    rows = [evaluate(f,h,s,lead) for f in FAMILIES for h in (8,16,40,80)
            for lead in ((1.,2.,4.) if f == 'screw' else (1.,)) for s in SCENARIOS]
    print(json.dumps(dict(seed=None, enumeration='exhaustive finite grid', descriptors=FAMILIES,
        scenarios=SCENARIOS, configurations=len(rows),
        timing_survivors=[r for r in rows if r['timing_pass']],
        timing_rejections=len([r for r in rows if not r['timing_pass']]),
        results=rows),indent=2))
