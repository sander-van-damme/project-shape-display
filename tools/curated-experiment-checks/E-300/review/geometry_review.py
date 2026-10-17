#!/usr/bin/env python3
"""Independent exported-mesh checks. No pair is silently excluded.

The tilted row is a rigid body; every rotor remains vertical on its fixed shaft.
The two cup heights may differ, modelling two independent print/stack errors.
These are geometric finite-pose checks, not a friction or physical proof.
"""
from pathlib import Path
import importlib.util, itertools, hashlib, json, math
import numpy as np
import trimesh as tm
import manifold3d as md

HERE=Path(__file__).resolve().parent; CAD=HERE.parent/'cad'
spec=importlib.util.spec_from_file_location('e300',CAD/'generate.py')
g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
NAMES=['frame-back','frame-front','row-selector','column-selector','input-shaft',
       'male-rotor','female-rotor','screw','pin','column-holder','hand-key','screw-tree']
loaded_hashes={}
for n in NAMES:
    loaded_hashes[n]=hashlib.sha256((CAD/'parts'/(n+'.stl')).read_bytes()).hexdigest()
    g.MESHES[n]=tm.load(CAD/'parts'/(n+'.stl'),force='mesh')
    assert g.MESHES[n].is_watertight,n

def solid(m):
    out=md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
    assert out.status()==md.Error.NoError,out.status()
    return out

cache={}; checks=0; failures=[]; states=[]; intended_cone_contacts=[]
def cached(m):
    key=hashlib.sha256(m.vertices.tobytes()+m.faces.tobytes()).digest()
    if key not in cache: cache[key]=solid(m)
    return cache[key]

def check(parts,label):
    global checks
    states.append(label)
    for (an,a),(bn,b) in itertools.combinations(parts.items(),2):
        if np.any(a.bounds[1] < b.bounds[0]+1e-7) or np.any(b.bounds[1] < a.bounds[0]+1e-7): continue
        checks+=1
        volume=abs((cached(a)^cached(b)).volume())
        if volume>1e-5:
            # Coincident analytical cones are tessellated independently. Only a
            # lower/upper pair whose tiny overlap disappears with <=0.003 mm
            # axial opening is classified as intended conical surface contact.
            # No frame/fork/shaft pair is exempt, and deep cone overlap fails.
            cone_pair=(an.startswith('lower-') and bn==an.replace('lower-','upper-'))
            if cone_pair and volume<.01:
                relieved=abs((cached(a)^cached(g.shift(b,[0,0,.003]))).volume())
                if relieved<1e-7:
                    intended_cone_contacts.append(dict(state=label,a=an,b=bn,
                        intersection_volume_mm3=volume,vanishes_after_axial_opening_mm=.003))
                    continue
            failures.append(dict(state=label,a=an,b=bn,intersection_volume_mm3=volume))

def moving(a): return {n:m for n,m in a.items() if 'holder' not in n}

for r,c0,c1 in itertools.product([0,1],repeat=3):
    check(g.assembly(r,(c0,c1)),f'mask_{r}{c0}{c1}')

# Capture float endpoints on unselected pairs: this tests socket floors, shaft
# clearance and frame/selector collisions at the actual widened groove limits.
# Closed pairs cannot take arbitrary independent float because cone contact
# couples their heights; their physically loaded state is checked below.
for r,c0,c1,lf,uf in itertools.product([0,1],[0,1],[0,1],[-.24,.24],[-.24,.24]):
    a=g.assembly(r,(c0,c1))
    for j,c in enumerate([c0,c1]):
        if r and c:continue
        a[f'lower-{j}']=g.shift(a[f'lower-{j}'],[0,0,lf])
        a[f'upper-{j}']=g.shift(a[f'upper-{j}'],[0,0,uf])
    check(a,f'capture_float_{r}{c0}{c1}_{lf}_{uf}')

for path in ['all','row','columns']:
    for t in np.linspace(0,1,31):
        r,c=(t,(t,t)) if path=='all' else ((t,(1,0)) if path=='row' else (1,(t,1-t)))
        check(moving(g.assembly(float(r),tuple(map(float,c)))),f'stroke_{path}_{t:.4f}')

# Both rotation directions, selected screw lead, and independently spinning inputs.
for r,c0,c1 in itertools.product([0,1],repeat=3):
    for alpha in [-90,-45,45,90]:
        selected=[bool(r and c) for c in [c0,c1]]
        phase=tuple(90+alpha if on else 90 for on in selected)
        travel=tuple(-3*alpha/360 if on else 0 for on in selected)
        a=g.assembly(r,(c0,c1),phase=phase,travels=travel)
        for j,x in enumerate([-g.P/2,g.P/2]):
            for n in [f'input-{j}',f'lower-{j}']:
                a[n]=g.shift(g.rotate(g.shift(a[n],[-x,0,0]),[0,0,1],alpha),[x,0,0])
        check(a,f'drive_{r}{c0}{c1}_{alpha}')

# Arbitrary relative phases with no preliminary input rotation: smooth cones should
# close in each case. This is finite sampling plus rotational-symmetry inspection.
for ph in [0,7,23,45,89,135,179,213,271,337]:
    check(g.assembly(1,(1,1),phase=(ph,ph+37),
                     travels=(-3*(ph-90)/360,-3*(ph+37-90)/360)),f'static_close_phase_{ph}')

# Model two unequal contact heights using a rigid tilted row. The row rotates;
# shafts and rotor axes do not. Upper cups/column forks translate by matching dz.
tilts=[]
for theta in [-3,-1.5,0,1.5,3]:
    a=moving(g.assembly(1,(1,1)))
    a['row']=g.shift(g.rotate(g.MESHES['row-selector'],[0,1,0],theta),[0,0,g.R+g.S])
    offsets=[]
    for j,x in enumerate([-g.P/2,g.P/2]):
        dz=-math.sin(math.radians(theta))*x; offsets.append(dz)
        for n in [f'lower-{j}',f'upper-{j}',f'column-{j}']:
            a[n]=g.shift(a[n],[0,0,dz])
    check(a,f'row_rigid_tilt_{theta}')
    tilts.append(dict(angle_deg=theta,lower_base_dz_mm=offsets,
                      relative_contact_height_mm=offsets[1]-offsets[0],rotor_axis_tilt_deg=0))

# Arbitrarily tilting an unloaded centred groove at fixed rotor heights is not
# assumed feasible: diagonal flange/fork contact is measured separately below.

# Fully force-loaded closure takes up BOTH capture clearances. Cups rise 0.24
# against column forks; lower cones then rise 0.24 to close them; the row must
# rise another 0.24 to contact the lower flange, plus .04 holder seat play.
# Nominal total row travel is 3.52, before any force-induced elastic displacement.
loaded=[]
for theta in [0]:
    a=g.assembly(1,(1,1))
    row=g.shift(g.rotate(g.MESHES['row-selector'],[0,1,0],theta),[0,0,g.R+g.S])
    for j,x in enumerate([-g.P/2,g.P/2]):
        dz=.28-math.sin(math.radians(theta))*x
        for n in [f'lower-{j}',f'upper-{j}']:a[n]=g.shift(a[n],[0,0,dz])
        # Column height errors are imposed by translating its fork by the same
        # contact-height mismatch, while its load-taking capture gap stays .24.
        a[f'column-{j}']=g.shift(a[f'column-{j}'],[0,0,dz-.24])
        if f'column-holder-{j}' in a:
            a[f'column-holder-{j}']=g.shift(a[f'column-holder-{j}'],[0,0,dz-.28])
    targets=cached(a['lower-0'])+cached(a['lower-1'])
    lo,hi=0.,.7
    for _ in range(28):
        mid=(lo+hi)/2
        if abs((cached(g.shift(row,[0,0,mid]))^targets).volume())>1e-7:hi=mid
        else:lo=mid
    a['row']=g.shift(row,[0,0,max(0,lo-1e-5)])
    check(a,f'force_loaded_closed_tilt_{theta}')
    loaded.append(dict(angle_deg=theta,row_extra_stroke_before_load_mm=lo,
                       column_capture_taken_up_mm=.24,lower_rotor_base_shift_mm=.28,
                       column_holder_play_taken_up_mm=.04))

# Concrete optional unequal-height trial: 0.10-mm tape on the first ON holder's
# upper reaction face moves that holder, column and cup down 0.10 mm. The upper
# face remains at its original ceiling; the first input/output axes stay vertical.
# The tape patch itself is not a CAD part and its physical thickness is measured
# by the owner. This checks whether the displaced solids have room to move.
shim=.10;theta=-math.degrees(math.asin(shim/g.P))
a=g.assembly(1,(1,1))
for j in [0,1]:
    error=-shim if j==0 else 0.
    for n in [f'lower-{j}',f'upper-{j}']:a[n]=g.shift(a[n],[0,0,.28+error])
    a[f'column-{j}']=g.shift(a[f'column-{j}'],[0,0,.04+error])
    a[f'column-holder-{j}']=g.shift(a[f'column-holder-{j}'],[0,0,error])
row=g.shift(g.rotate(g.MESHES['row-selector'],[0,1,0],theta),[0,0,g.R+g.S])
targets=cached(a['lower-0'])+cached(a['lower-1']);lo,hi=0.,.7
for _ in range(28):
    mid=(lo+hi)/2
    if abs((cached(g.shift(row,[0,0,mid]))^targets).volume())>1e-7:hi=mid
    else:lo=mid
a['row']=g.shift(row,[0,0,max(0,lo-1e-5)])
check(a,'force_loaded_one_holder_shim_0.10')
shim_result=dict(shim_mm=shim,row_angle_deg=theta,row_extra_stroke_mm=lo,
                 holder_displacements_mm=[-shim,0],tape_patch_geometry_included=False)

# Actual contact prevents further upward row travel. Measure the first fork/flange
# intersection with cones stationary, rather than claiming overtravel is free.
contact_limits=[]
base=moving(g.assembly(1,(1,1)))
for theta in [-3,0,3]:
    row=g.shift(g.rotate(g.MESHES['row-selector'],[0,1,0],theta),[0,0,g.R+g.S])
    targets=cached(base['lower-0'])+cached(base['lower-1'])
    lo,hi=0.,.5
    for _ in range(28):
        mid=(lo+hi)/2
        if abs((cached(g.shift(row,[0,0,mid]))^targets).volume())>1e-7: hi=mid
        else:lo=mid
    contact_limits.append(dict(angle_deg=theta,first_capture_contact_central_dz_mm=lo))

# Geometric envelope against fixed frame, including unloaded row reserve travel.
frame=cached(g.MESHES['frame-back'])+cached(g.MESHES['frame-front'])
sweeps=[]
for name,base,dz in [('row',g.assembly(0,(0,0))['row'],3.75),
                     ('column-0',g.assembly(0,(0,0))['column-0'],-3),
                     ('column-1',g.assembly(0,(0,0))['column-1'],-3)]:
    eps=.00001
    segment=md.Manifold.cube([2*eps,2*eps,abs(dz)+2*eps]).translate([-eps,-eps,min(0,dz)-eps])
    sweep=cached(base).minkowski_sum(segment)
    volume=abs((sweep^frame).volume()); checks+=1
    sweeps.append(dict(part=name,travel_mm=dz,frame_intersection_volume_mm3=volume))
    if volume>1e-5:failures.append(dict(state='continuous_selector_sweep',a=name,b='frame',intersection_volume_mm3=volume))

# Conical screw support and actual amount of available axial play before frame
# contact, with collision of the upper rotor separately reported.
a=g.assembly(0,(0,0)); screw=cached(a['screw-0']); rotor=cached(a['upper-0'])
axial=[]
for direction,bound in [('down',-.5),('up',.5)]:
    lo,hi=0.,abs(bound)
    for _ in range(28):
        mid=(lo+hi)/2; dz=mid if direction=='up' else -mid
        if abs((screw.translate([0,0,dz])^frame).volume())>1e-7:hi=mid
        else:lo=mid
    dz=lo if direction=='up' else -lo
    axial.append(dict(direction=direction,first_frame_contact_dz_mm=dz,
                      upper_rotor_intersection_at_contact_mm3=abs((screw.translate([0,0,dz])^rotor).volume())))

# Frame halves close laterally around the captured moving pieces, holders removed.
a=moving(g.assembly(0,(0,0)))
front=[n for n in a if n=='frame-front' or n.startswith(('column','upper','screw','pin'))]
for dy in np.linspace(0,15,31):
    check({n:g.shift(m,[0,float(dy),0]) if n in front else m for n,m in a.items()},f'frame_mating_y_{dy:.2f}')

assert all(loaded_hashes[n]==hashlib.sha256((CAD/'parts'/(n+'.stl')).read_bytes()).hexdigest() for n in NAMES),'CAD changed during review; rerun on stable meshes'
record=dict(evidence='Finite-pose mesh booleans, nominal CAD only; no physical qualification.',
            checks=checks,states=states,unexpected_intersections=failures,exclusions=[],
            intended_cone_contact_tessellation=intended_cone_contacts,
            row_tilt_fixed_vertical_rotors=tilts,capture_contact_limits=contact_limits,
            fully_force_loaded_closure=loaded,
            unequal_contact_height_shim_trial=shim_result,
            rejected_diagnostic_proxy='Translating entire locked columns/holders +/-0.133 mm caused 0.0512 mm3 frame interference; this is not treated as an arbitrary-height tolerance pass. Concrete one-sided 0.10-mm shim checked separately.',
            continuous_selector_sweeps=sweeps,screw_axial_support=axial,
            mesh_sha256=loaded_hashes)
(HERE/'geometry-review.json').write_text(json.dumps(record,indent=2)+'\n')
groups={}
for f in failures:
    key=f['a']+'/'+f['b']
    if key not in groups:groups[key]=dict(count=0,max_volume_mm3=0,example_state=f['state'])
    groups[key]['count']+=1;groups[key]['max_volume_mm3']=max(groups[key]['max_volume_mm3'],f['intersection_volume_mm3'])
print(json.dumps(dict(checks=checks,poses=len(states),failure_count=len(failures),failures_by_pair=groups,
                     capture_contact_limits=contact_limits,force_loaded=loaded),indent=2))
assert not failures,f'{len(failures)} unexpected intersections'
