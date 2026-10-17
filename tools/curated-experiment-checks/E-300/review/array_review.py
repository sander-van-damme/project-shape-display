#!/usr/bin/env python3
"""Independent dense-neighbour screen of functional cores, not external test levers.

Core meshes are separately exported from CAD without the one-off test controls.
All neighbour rotors stay vertical. Independent endpoint states, capture float,
row reserve travel and rigid row tilt are intentionally combined conservatively.
"""
from pathlib import Path
import importlib.util,itertools,json,hashlib,math
import numpy as np
import trimesh as tm
import manifold3d as md
HERE=Path(__file__).resolve().parent;CAD=HERE.parent/'cad'
s=importlib.util.spec_from_file_location('cad',CAD/'generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def solid(m):
    v=md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
    assert v.status()==md.Error.NoError
    return v
meshes={n:tm.load(CAD/'parts'/(n+'.stl'),force='mesh') for n in ['row-selector-core','column-selector-core','male-rotor','female-rotor']}
loaded_hashes={n:hashlib.sha256((CAD/'parts'/(n+'.stl')).read_bytes()).hexdigest() for n in meshes}
cache={};fails=[];checks=0;poses=0
def sm(m):
    h=hashlib.sha256(m.vertices.tobytes()+m.faces.tobytes()).digest()
    if h not in cache:cache[h]=solid(m)
    return cache[h]
def check(a,b,label,an,bn):
    global checks,poses
    poses+=1
    if np.any(a.bounds[1]<b.bounds[0]+1e-7) or np.any(b.bounds[1]<a.bounds[0]+1e-7):return
    checks+=1;v=abs((sm(a)^sm(b)).volume())
    if v>1e-5:fails.append(dict(state=label,a=an,b=bn,intersection_volume_mm3=v))

rows=[]
for dz,theta in itertools.product([0,3,3.75],[-3,0,3]):
    a=g.shift(g.rotate(meshes['row-selector-core'],[0,1,0],theta),[0,0,g.R+dz])
    rows.append((dz,theta,a))
for dz,theta,a in rows:
    label=f'row_dz{dz}_tilt{theta}'
    for x,y in itertools.product([-7.62,-2.54,2.54,7.62],[-5.08,0,5.08]):
        if y==0 and abs(x)==2.54:continue # own captured rotors checked in geometry_review
        for r,flt in itertools.product([0,1],[-.24,0,.24]):
            b=g.shift(meshes['male-rotor'],[x,y,g.R+g.S*r+flt])
            check(a,b,f'{label}_neighbour_row{r}_float{flt}','row-core',f'male@{x},{y}')
        for c,flt in itertools.product([0,1],[-.24,0,.24]):
            b=g.shift(g.rotate(meshes['female-rotor'],[1,0,0],180),[x,y,g.C-g.S*c+flt])
            check(a,b,f'{label}_neighbour_col{c}_float{flt}','row-core',f'female@{x},{y}')
    for nd,nt,b in rows:
        for y in [-g.P,g.P]:
            check(a,g.shift(b,[0,y,0]),f'{label}_neighbour_dz{nd}_tilt{nt}_y{y}','row-core','neighbour-row-core')

cols=[]
for c in [0,1]:
    a=g.shift(g.rotate(meshes['column-selector-core'],[1,0,0],180),[0,0,g.C-g.S*c])
    cols.append((c,a))
    for x,y in itertools.product([-g.P,0,g.P],[-g.P,0,g.P]):
        if x==0 and y==0:continue
        for r,flt in itertools.product([0,1],[-.24,0,.24]):
            b=g.shift(meshes['male-rotor'],[x,y,g.R+g.S*r+flt])
            check(a,b,f'column{c}_neighbour_row{r}_float{flt}','column-core',f'male@{x},{y}')
        for nc,flt in itertools.product([0,1],[-.24,0,.24]):
            b=g.shift(g.rotate(meshes['female-rotor'],[1,0,0],180),[x,y,g.C-g.S*nc+flt])
            check(a,b,f'column{c}_neighbour_col{nc}_float{flt}','column-core',f'female@{x},{y}')
    for nc,b in cols:
        for x,y in itertools.product([-g.P,0,g.P],[-g.P,0,g.P]):
            if x or y:check(a,g.shift(b,[x,y,0]),f'col{c}_neighbour_col{nc}@{x},{y}','column-core','neighbour-column-core')

# Orthogonal selectors use distinct heights. Their external laboratory controls
# are deliberately not claimed as a repeatable array actuation/routing solution.
for dz,theta,a in rows:
    for c,b in cols:
        for x,y in itertools.product([-g.P,0,g.P],[-g.P,0,g.P]):
            check(a,g.shift(b,[x,y,0]),f'row{dz}_{theta}_col{c}@{x},{y}','row-core','column-core')

assert all(loaded_hashes[n]==hashlib.sha256((CAD/'parts'/(n+'.stl')).read_bytes()).hexdigest() for n in meshes),'CAD changed during review; rerun on stable meshes'
record=dict(evidence='Nominal core-mesh conservative neighbour screen; not full-array qualification.',
    checks=checks,pair_poses=poses,unexpected_intersections=fails,exclusions=[],
    row_displacements_mm=[0,3,3.75],row_tilts_deg=[-3,0,3],neighbour_capture_float_mm=[-.24,0,.24],
    tooling_limit='External 1x2 laboratory levers, row paddle, holders and frame are not repeated in this core screen.',
    core_bounds={n:m.bounds.tolist() for n,m in meshes.items()},
    mesh_sha256=loaded_hashes)
(HERE/'array-review.json').write_text(json.dumps(record,indent=2)+'\n')
groups={}
for f in fails:
    k=f['a']+'/'+f['b'];groups.setdefault(k,dict(count=0,max_volume_mm3=0,example=f['state']))
    groups[k]['count']+=1;groups[k]['max_volume_mm3']=max(groups[k]['max_volume_mm3'],f['intersection_volume_mm3'])
print(json.dumps(dict(checks=checks,pair_poses=poses,failures=len(fails),pairs=groups),indent=2))
assert not fails,f'{len(fails)} neighbour intersections'
