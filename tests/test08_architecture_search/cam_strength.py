"""Optional NumPy beam buckling screen for the stepped cam itself.

Not FEA qualification: assumes a perfectly clamped root, elastic material,
centred axial load and no imperfections. Actual toe load is eccentric, hence
this result must NOT be promoted to a rated load. Each section uses its weakest
principal bending inertia even when that axis rotates along the cam.
"""
import json
import argparse
import math
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent


def critical_load(inertias, length, modulus):
    n=len(inertias); le=length/n
    stiffness=np.zeros((2*n+2,2*n+2)); geometric=np.zeros_like(stiffness)
    kb=np.array([[12,6*le,-12,6*le],[6*le,4*le**2,-6*le,2*le**2],
                 [-12,-6*le,12,-6*le],[6*le,2*le**2,-6*le,4*le**2]],float)/le**3
    kg=np.array([[36,3*le,-36,3*le],[3*le,4*le**2,-3*le,-le**2],
                 [-36,-3*le,36,-3*le],[3*le,-le**2,-3*le,4*le**2]],float)/(30*le)
    for i,inertia in enumerate(inertias):
        ix=np.arange(2*i,2*i+4)
        stiffness[np.ix_(ix,ix)]+=modulus*inertia*kb
        geometric[np.ix_(ix,ix)]+=kg
    # Root translation/rotation removed; free tip.
    eigenvalues=np.linalg.eigvals(np.linalg.solve(stiffness[2:,2:],geometric[2:,2:]))
    return 1/max(float(v.real) for v in eigenvalues if abs(v.imag)<1e-8 and v.real>0)


def main():
    p=json.loads((HERE/'params.json').read_text()); c=p['cam']; t=p['terrain']
    parser=argparse.ArgumentParser(); parser.add_argument('--core-radius',type=float)
    args=parser.parse_args()
    if args.core_radius is not None: c['core_radius_mm']=args.core_radius
    e=p['loads']['elastic_modulus_mpa']; length=t['travel_mm']
    uniform=critical_load([1]*40,length,e)
    exact=math.pi**2*e/(4*length**2)
    assert abs(uniform/exact-1)<1e-5, (uniform,exact)
    runs=[]
    for resolution in [.04,.02,.01]:
        r=c['radius_mm']; xy=np.arange(-r+resolution/2,r,resolution)
        x,y=np.meshgrid(xy,xy); radius=np.hypot(x,y)
        angle=np.arctan2(y,x)*180/math.pi
        sector=np.floor(((angle+180/t['levels'])%360)/(360/t['levels'])).astype(int)
        sections=[]
        for k in range(1,t['levels']):
            mask=(radius<=r)&((sector>=k)|(radius<=c['core_radius_mm']))
            xx=x[mask]; yy=y[mask]; dx=xx-xx.mean(); dy=yy-yy.mean()
            tensor=np.array([[sum(dy*dy),-sum(dx*dy)],[-sum(dx*dy),sum(dx*dx)]])*resolution**2
            sections.append(dict(level_band=k,area_mm2=len(xx)*resolution**2,
                                 weakest_inertia_mm4=float(np.linalg.eigvalsh(tensor)[0])))
        inertia=[sections[min(len(sections)-1,int((i+.5)/40*len(sections)))]['weakest_inertia_mm4'] for i in range(40)]
        runs.append(dict(section_sample_mm=resolution,sections=sections,
                         idealized_critical_load_n=critical_load(inertia,length,e)))
    mesh_convergence={str(n):critical_load([sections[min(len(sections)-1,int((i+.5)/n*len(sections)))]['weakest_inertia_mm4'] for i in range(n)],length,e) for n in [20,40,80]}
    result=dict(model='Euler-Bernoulli geometric-stiffness eigenproblem, clamped-free, 40 elements',
                core_radius_mm=c['core_radius_mm'],beam_mesh_convergence_n=mesh_convergence,
                numpy_version=np.__version__,uniform_beam_check_relative_error=uniform/exact-1,
                convergence=runs,
                qualification='Not a service-load rating. Root compliance, eccentric load, creep and print defects excluded.')
    (HERE/'results').mkdir(exist_ok=True)
    filename='cam_strength.json' if args.core_radius is None else f'cam_strength_core_{args.core_radius:g}.json'
    (HERE/'results'/filename).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
