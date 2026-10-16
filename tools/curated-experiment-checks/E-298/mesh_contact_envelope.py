#!/usr/bin/env python3
"""Independent actual STL vertical-ray contact-envelope screen, finite sampling."""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
HERE=Path(__file__).resolve().parent

def heights(m,r,theta):
    rr,tt=np.meshgrid(r,np.radians(theta),indexing='ij')
    x=(rr*np.cos(tt)).ravel();y=(rr*np.sin(tt)).ravel();z=np.zeros_like(x)+6.2
    for tri in m.triangles:
        if tri[:,2].max()<6.2-1e-5:continue
        a,b,c=tri
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-12:continue
        ids=np.flatnonzero((x>=tri[:,0].min()-1e-9)&(x<=tri[:,0].max()+1e-9)&(y>=tri[:,1].min()-1e-9)&(y<=tri[:,1].max()+1e-9))
        xx=x[ids];yy=y[ids]
        u=((b[1]-c[1])*(xx-c[0])+(c[0]-b[0])*(yy-c[1]))/den
        v=((c[1]-a[1])*(xx-c[0])+(a[0]-c[0])*(yy-c[1]))/den
        keep=(u>=-1e-8)&(v>=-1e-8)&(u+v<=1+1e-8)
        zz=u*a[2]+v*b[2]+(1-u-v)*c[2]
        ii=ids[keep];z[ii]=np.maximum(z[ii],zz[keep])
    return (z-6.2).reshape(len(r),len(theta))

def main():
    # Include inner/outer region and actual crown radial center; .25deg angular.
    theta=np.arange(0,180,.25);r=np.arange(.60,1.8001,.02)
    idx=np.arange(len(theta));out={'method':'Finite vertical-ray heights on actual STL triangles; max of opposing height fields','radial_step_mm':.02,'theta_phase_step_deg':.25,'variants':[]}
    for name in ['point48','point60','point60skew']:
        p=HERE/'cad'/'parts'/(name+'.stl');m=trimesh.load(p,force='mesh')
        h=heights(m,r,theta)
        D=np.array([np.max(h+h[:,(k-idx)%len(theta)]) for k in idx])
        prev=np.roll(D,1);nxt=np.roll(D,-1)
        local=(D>3.36+1e-7)&(prev>=D-1e-7)&(nxt>=D-1e-7)
        maximum=np.isclose(D,D.max(),atol=1e-6)
        result={'name':name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'envelope_min_max_mm':[float(D.min()),float(D.max())],
                'maximum_plateau_sample_phases_deg':theta[maximum].tolist(),
                'additional_local_trap_sample_phases_deg':theta[local&~maximum].tolist(),
                'full_insert_sample_phases_deg':theta[D<=3.36].tolist(),
                'phase_deg':theta.tolist(),'separation_envelope_mm':D.round(7).tolist()}
        out['variants'].append(result)
    (HERE/'mesh-contact-envelope.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k not in ['phase_deg','separation_envelope_mm','full_insert_sample_phases_deg','maximum_plateau_sample_phases_deg']} for x in out['variants']],indent=2))
if __name__=='__main__':main()
