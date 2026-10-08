"""Exact axis-aligned envelope screen, mm. Bounds, not FDM distributions."""
import importlib.util
import itertools
import json
from pathlib import Path
spec = importlib.util.spec_from_file_location('pawl', Path(__file__).parents[1]/'E-052/pawl_sweep.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def hit(a, b):
    return all(min(a[2*i+1], b[2*i+1]) > max(a[2*i], b[2*i])+1e-9 for i in range(3))


def geometry(e, b, q, wall, shelf=None):
    shelf = wall if shelf is None else shelf
    c=.1
    # Minimum E-052 section; tiny positive margin avoids boundary-only witness.
    o=.4+e+.02; r=max(.8,o+e+c)+.02; L=.8
    failures, section=p.screen(1.6,r,L,o,2.,2.,e+c+.02,e)
    if failures: return {'failures':['x_'+f for f in failures]}
    x0=e+c; tip=x0+1.6+r; start=tip-o; stroke=o+e+c
    # Rails lie beside the rack in y, not behind it in x.
    inner=b/2+e/2+c
    wing=inner+q+e/2
    outer=wing+e/2+c
    width=2*(outer+wall+e/2)
    if width > p.PITCH+1e-9: return {'failures':['y_pitch'], 'width_y':round(width,4)}
    # Pawl/wing z in [-2,0]; uncertainty +/-e/2. Two shelf pairs
    # surround that swept slab. Slot clearance is NOT a preload/load proof.
    zlo=-2-e/2-c; zhi=e/2+c
    left=start-e/2; right=start+stroke+L+e/2
    solids=[]
    for sign in (-1,1):
        yl,yh=sorted((sign*inner,sign*(outer+wall)))
        solids.extend([(left,right,yl,yh,zlo-shelf,zlo),
                       (left,right,yl,yh,zhi,zhi+shelf)])
        yl,yh=sorted((sign*outer,sign*(outer+wall)))
        solids.append((left,right,yl,yh,zlo-shelf,zhi+shelf))
    # All shifts are extrema of affine boxes. Swept box exact for x-only
    # translation. Vertical rack union deliberately includes web and all teeth.
    checks=0
    for dr,dp,dz,common in itertools.product((-e/2,e/2),repeat=4):
        rack=(x0-e/2,tip+e/2,-b/2+dr,b/2+dr,-45,45)
        pawl=(left,right,-wing+dp,wing+dp,-2+dz,dz)
        for solid in solids:
            assert not hit(rack,solid)
            assert not hit(pawl,solid)
            assert solid[2]+common >= -p.PITCH/2-1e-9
            assert solid[3]+common <= p.PITCH/2+1e-9
            checks+=1
        assert min(wing+dp,outer)-max(inner,-wing+dp) >= q-1e-9
        assert min(-inner,wing+dp)-max(-outer,-wing+dp) >= q-1e-9
    # Track extends across whole swept wing: longitudinal bearing L remains
    # available at both extremes and therefore every intermediate translation.
    for dp,s in itertools.product((-e/2,e/2),(0,stroke)):
        assert min(right,start+dp+s+L)-max(left,start+dp+s) >= L-1e-9
    assert abs(width-(b+4*e+4*c+2*q+2*wall))<1e-9
    return {'failures':[], 'width_x':section['width'], 'width_y':round(width,4),
            'rack_width':b,'bearing_width_each':q,'wall':wall,'shelf':shelf,
            'stroke':round(stroke,4),'lift':section['lift'],
            'track_length':round(right-left,4),'slot_vertical_play':round(e+2*c,4),
            'box_checks':checks,
            # Best possible force split and full 0.8-mm longitudinal width.
            # Contact is at least c from the outer-wall cantilever root.
            'shelf_stress_lower_bound_10N_MPa':round(3*10*c/(L*shelf**2),4)}


def run():
    assert hit((0,1,0,1,0,1),(.5,2,.5,2,.5,2))
    assert not hit((0,1,0,1,0,1),(1,2,0,1,0,1))
    out={}
    for name,e in p.ERRORS.items():
        population=[geometry(e,b,q,w) for b,q,w in itertools.product((1.6,2.,2.4),(.4,.6,.8),(.4,.6,.8))]
        survivors=[x for x in population if not x['failures']]
        out[name]={'candidates':len(population),'survivors':len(survivors),
                   'failure_counts':{r:sum(r in x['failures'] for x in population) for r in sorted({r for x in population for r in x['failures']})},
                   'witnesses':survivors,
                   'load_screen_survivors_at_8MPa': {str(F):sum(x['shelf_stress_lower_bound_10N_MPa']*F/10<=8 for x in survivors) for F in (1,10,100)}}
    # Adverse y-bound and improved-wall holdouts, independent closed form.
    assert not geometry(.35,1.6,.4,.4)['failures']
    assert geometry(.35,1.6,.4,.6)['failures']==['y_pitch']
    assert geometry(.371,1.6,.4,.4)['failures']==['y_pitch']
    assert not geometry(.369,1.6,.4,.4)['failures']
    out['decoupled_middle']=geometry(.35,1.6,.4,.4,.8)
    assert not out['decoupled_middle']['failures']
    assert out['decoupled_middle']['shelf_stress_lower_bound_10N_MPa']<8
    return out

if __name__=='__main__': print(json.dumps(run(),indent=2))
