#!/usr/bin/env python3
"""Create genuine Bambu projects, then reopen/reslice WITHOUT external profiles."""
from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as E,importlib.util,shutil,re
import numpy as np,trimesh
P=Path(__file__).resolve().parents[1];M=P/'metadata';NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';E.register_namespace('',NS)
spec=importlib.util.spec_from_file_location('shared',P.parent/'build-bambu-projects.py');shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
def input_project(name,out):
 rows=json.loads((M/'layout.json').read_text())[name];bounds=trimesh.load(P/'components'/f'{name}.stl').bounds
 offset=np.array([128,128,0.]);offset[:2]-=bounds.mean(axis=0)[:2]
 model=E.Element(f'{{{NS}}}model',unit='millimeter');res=E.SubElement(model,f'{{{NS}}}resources');build=E.SubElement(model,f'{{{NS}}}build');cfg=E.Element('config');overrides={}
 for i,p in enumerate(rows,1):
  mesh=trimesh.load(P/'components'/(p['source']+'.stl'),force='mesh');mesh.apply_translation(np.r_[p['center_xy'],0.]+offset)
  ob=E.SubElement(res,f'{{{NS}}}object',id=str(i),type='model',name=p['name']);me=E.SubElement(ob,f'{{{NS}}}mesh');vs=E.SubElement(me,f'{{{NS}}}vertices');fs=E.SubElement(me,f'{{{NS}}}triangles')
  for x,y,z in mesh.vertices:E.SubElement(vs,f'{{{NS}}}vertex',x=f'{x:.9g}',y=f'{y:.9g}',z=f'{z:.9g}')
  for a,b,c in mesh.faces:E.SubElement(fs,f'{{{NS}}}triangle',v1=str(a),v2=str(b),v3=str(c))
  E.SubElement(build,f'{{{NS}}}item',objectid=str(i));co=E.SubElement(cfg,'object',id=str(i))
  vals=dict(name=p['name'],enable_support='0',extruder='1')
  if p['source'] in ['A-screw-supported','B-pin','C-pin-18-upright']:
   vals.update(brim_type='outer_only',brim_width='3',brim_object_gap='0.12',sparse_infill_density='100%')
  if p['source']=='C-pin-18-horizontal':vals.update(brim_type='outer_only',brim_width='2',brim_object_gap='0.12',sparse_infill_density='100%',bridge_angle='180')
  overrides[p['name']]=vals
  for k,v in vals.items():E.SubElement(co,'metadata',key=k,value=v)
  E.SubElement(co,'part',id=str(i),subtype='normal_part')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/model_settings.config',E.tostring(cfg,encoding='utf-8',xml_declaration=True))
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 return offset.tolist(),overrides
def objects(z):
 return {next(m.get('value') for m in o.findall('metadata') if m.get('key')=='name'):{m.get('key'):m.get('value') for m in o.findall('metadata')} for o in E.fromstring(z.read('Metadata/model_settings.config')).findall('object')}
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--bambu',type=Path,required=True);ap.add_argument('--resources',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);ap.add_argument('--plate',choices=['A-first','BC-comparisons'],required=True);a=ap.parse_args()
 exe=a.bambu.resolve();scratch=a.scratch.resolve();scratch.mkdir(parents=True,exist_ok=True)
 version=subprocess.run([str(exe),'--help'],capture_output=True,text=True,cwd=scratch);assert '02.08.02.61' in version.stdout
 printer,ps=shared.resolve(a.resources,'machine','Bambu Lab X1 Carbon 0.4 nozzle');filament,fs=shared.resolve(a.resources,'filament','Generic PLA');process,rs=shared.resolve(a.resources,'process','0.12mm Fine @BBL X1C')
 with zipfile.ZipFile(P.parent/'2026-10-19-microstepper-frame-v3/microstepper-frame-v3.3mf') as z:baseline=json.loads(z.read('Metadata/project_settings.config'))
 exclude={'name','type','from','version','inherits','include','instantiation','setting_id','compatible_printers'}
 for c in [process,filament]:
  for k in set(c)-exclude:
   if k in baseline:c[k]=baseline[k]
 printer['printer_settings_id']='Bambu Lab X1 Carbon 0.4 nozzle'
 process.update(name=a.plate+' minimal frame X1C PLA',print_settings_id=a.plate+' minimal frame X1C PLA',layer_height='0.12',initial_layer_print_height='0.12',wall_generator='arachne',wall_loops='2',line_width='0.45',outer_wall_line_width='0.45',inner_wall_line_width='0.45',min_bead_width='75%',min_feature_size='10%',sparse_infill_density='25%',sparse_infill_pattern='gyroid',top_shell_layers='5',bottom_shell_layers='5',enable_support='0',support_type='normal(auto)',support_on_build_plate_only='1',raft_layers='0',brim_type='no_brim',brim_width='0',print_sequence='by layer',enable_prime_tower='0',xy_contour_compensation='0',xy_hole_compensation='0',elefant_foot_compensation='0',enable_arc_fitting='0',seam_position='aligned',outer_wall_speed=['15','15'],inner_wall_speed=['20','20'],small_perimeter_speed=['15','15'],small_perimeter_threshold=['20','20'],initial_layer_speed=['15','15'],initial_layer_infill_speed=['15','15'],sparse_infill_speed=['40','40'],internal_solid_infill_speed=['30','30'],top_surface_speed=['20','20'],bridge_speed=['15','15'],default_acceleration=['1000','1000'],outer_wall_acceleration=['500','500'],inner_wall_acceleration=['1000','1000'],initial_layer_acceleration=['500','500'],curr_bed_type='Textured PEI Plate')
 for n,c in [('printer',printer),('process',process),('filament',filament)]: (scratch/(n+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 offset,ov=input_project(a.plate,scratch/'input.3mf');target=P/(a.plate+'.3mf');common=['--arrange','0','--orient','0','--slice','0']
 cmd=[str(exe),'--datadir',str(scratch/'studio-data'),'--load-settings',str(scratch/'printer.json')+';'+str(scratch/'process.json'),'--load-filaments',str(scratch/'filament.json'),*common,'--export-3mf',target.name,'--outputdir',str(scratch),str(scratch/'input.3mf')]
 r=subprocess.run(cmd,capture_output=True,text=True,cwd=scratch);(scratch/'slice.log').write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr)[-5000:];shutil.copy2(scratch/target.name,target)
 reopened=scratch/'reopen';reopened.mkdir(exist_ok=True)
 cmd2=[str(exe),'--datadir',str(reopened/'studio-data'),*common,'--export-3mf',target.name,'--outputdir',str(reopened),str(target)]
 r2=subprocess.run(cmd2,capture_output=True,text=True,cwd=scratch);(reopened/'slice.log').write_text(r2.stdout+r2.stderr);assert r2.returncode==0,(r2.stdout+r2.stderr)[-5000:]
 with zipfile.ZipFile(target) as z1,zipfile.ZipFile(reopened/target.name) as z2:
  s1=json.loads(z1.read('Metadata/project_settings.config'));s2=json.loads(z2.read('Metadata/project_settings.config'));o1,o2=objects(z1),objects(z2)
  diff={k:[s1.get(k),s2.get(k)] for k in set(s1)|set(s2) if s1.get(k)!=s2.get(k)}
  assert not diff,diff
  for name,vals in ov.items():
   for key,value in vals.items():assert o1[name].get(key)==o2[name].get(key)==value,(name,key,value)
  (M/(a.plate+'-settings.json')).write_text(json.dumps(s1,indent=2)+'\n')
  clean=lambda t:'\n'.join(x for x in t.splitlines() if not x.startswith('; generated by'))
  g1=z1.read('Metadata/plate_1.gcode').decode();g2=z2.read('Metadata/plate_1.gcode').decode()
  equality=clean(g1)==clean(g2)
  stats=[s for s in g1.splitlines() if re.search(r'(total estimated time|total filament|model printing time)',s)]
 record=dict(bambu_version='02.08.02.61',plate_translation_mm=offset,object_settings=ov,project_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),reopened_project_sha256=hashlib.sha256((reopened/target.name).read_bytes()).hexdigest(),reopened_without_external_profiles=True,settings_differences=diff,gcode_equal_except_timestamp=equality,stats=stats,profile_provenance=dict(printer=ps,filament=fs,process=rs),physical_test='NOT PERFORMED')
 (M/(a.plate+'-build.json')).write_text(json.dumps(record,indent=2)+'\n');print(a.plate,stats,'reopened',equality)
if __name__=='__main__':main()
