#!/usr/bin/env python3
"""Build and reopen/reslice configured X1C project. No runtime downloaded by script.
Requires official Bambu Studio02.08.02.61, resources, numpy, trimesh.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,zipfile,xml.etree.ElementTree as E,importlib.util,shutil
import numpy as np
import trimesh
HERE=Path(__file__).resolve().parents[1];REPO=HERE.parents[1]
METADATA=HERE/'metadata'; NS='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
E.register_namespace('',NS)
spec=importlib.util.spec_from_file_location('shared_builder',HERE.parent/'build-bambu-projects.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)

def mesh_project(out):
 layout=json.loads((METADATA/'layout.json').read_text());bounds=np.array(json.loads((METADATA/'geometry.json').read_text())['bounds_mm'])
 offset=np.array([128,128,0.]);offset[:2]-=bounds.mean(axis=0)[:2]
 model=E.Element(f'{{{NS}}}model',unit='millimeter');res=E.SubElement(model,f'{{{NS}}}resources');build=E.SubElement(model,f'{{{NS}}}build')
 cfg=E.Element('config')
 for i,p in enumerate(layout,1):
  m=trimesh.load(HERE/'components'/(p['name']+'.stl'),force='mesh');m.apply_translation(np.r_[p['position_mm'],0.]+offset)
  ob=E.SubElement(res,f'{{{NS}}}object',id=str(i),type='model',name=p['name']);me=E.SubElement(ob,f'{{{NS}}}mesh');vs=E.SubElement(me,f'{{{NS}}}vertices');fs=E.SubElement(me,f'{{{NS}}}triangles')
  for x,y,z in m.vertices:E.SubElement(vs,f'{{{NS}}}vertex',x=f'{x:.9g}',y=f'{y:.9g}',z=f'{z:.9g}')
  for a,b,c in m.faces:E.SubElement(fs,f'{{{NS}}}triangle',v1=str(a),v2=str(b),v3=str(c))
  E.SubElement(build,f'{{{NS}}}item',objectid=str(i));co=E.SubElement(cfg,'object',id=str(i))
  for k,v in dict(name=p['name'],enable_support='0',extruder='1').items():E.SubElement(co,'metadata',key=k,value=v)
  E.SubElement(co,'part',id=str(i),subtype='normal_part')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('3D/3dmodel.model',E.tostring(model,encoding='utf-8',xml_declaration=True));z.writestr('Metadata/model_settings.config',E.tostring(cfg,encoding='utf-8',xml_declaration=True))
  z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
  z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 return offset.tolist()

def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--bambu',type=Path,required=True);ap.add_argument('--resources',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);a=ap.parse_args()
 exe=a.bambu.resolve();scratch=a.scratch.resolve();scratch.mkdir(parents=True,exist_ok=True)
 version=subprocess.run([str(exe),'--help'],capture_output=True,text=True,cwd=scratch);assert '02.08.02.61' in version.stdout
 printer,ps=shared.resolve(a.resources,'machine','Bambu Lab X1 Carbon 0.4 nozzle');filament,fs=shared.resolve(a.resources,'filament','Generic PLA');process,rs=shared.resolve(a.resources,'process','0.16mm Optimal @BBL X1C')
 printer['printer_settings_id']='Bambu Lab X1 Carbon 0.4 nozzle'
 process.update(name='E-303 friction screen X1C PLA',print_settings_id='E-303 friction screen X1C PLA',layer_height='0.16',initial_layer_print_height='0.20',wall_generator='arachne',wall_loops='3',line_width='0.42',outer_wall_line_width='0.42',inner_wall_line_width='0.45',initial_layer_line_width='0.5',sparse_infill_density='20%',sparse_infill_pattern='gyroid',top_shell_layers='5',bottom_shell_layers='5',enable_support='0',support_type='normal(auto)',support_on_build_plate_only='1',raft_layers='0',brim_type='no_brim',brim_width='0',print_sequence='by layer',enable_prime_tower='0',xy_contour_compensation='0',xy_hole_compensation='0',elefant_foot_compensation='0',enable_arc_fitting='0',outer_wall_speed=['20','20'],inner_wall_speed=['30','30'],small_perimeter_speed=['20','20'],initial_layer_speed=['20','20'],initial_layer_infill_speed=['20','20'],sparse_infill_speed=['50','50'],internal_solid_infill_speed=['40','40'],top_surface_speed=['20','20'],bridge_speed=['20','20'],default_acceleration=['1000','1000'],outer_wall_acceleration=['500','500'],inner_wall_acceleration=['1000','1000'],initial_layer_acceleration=['500','500'],curr_bed_type='Textured PEI Plate')
 filament.update(nozzle_temperature=['210'],nozzle_temperature_initial_layer=['210'],hot_plate_temp=['55'],hot_plate_temp_initial_layer=['55'],textured_plate_temp=['55'],textured_plate_temp_initial_layer=['55'],fan_min_speed=['100'],fan_max_speed=['100'],close_fan_the_first_x_layers=['1'],full_fan_speed_layer=['2'])
 for n,c in [('printer',printer),('process',process),('filament',filament)]: (scratch/(n+'.json')).write_text(json.dumps(c,indent=2)+'\n')
 offset=mesh_project(scratch/'input.3mf');target=HERE/'clutch-friction-screen.3mf'
 common=['--arrange','0','--orient','0','--slice','0']
 cmd=[str(exe),'--datadir',str(scratch/'studio-data'),'--load-settings',str(scratch/'printer.json')+';'+str(scratch/'process.json'),'--load-filaments',str(scratch/'filament.json'),*common,'--export-3mf',target.name,'--outputdir',str(scratch),str(scratch/'input.3mf')]
 r=subprocess.run(cmd,capture_output=True,text=True,cwd=scratch);(scratch/'slice.log').write_text(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr)[-5000:];shutil.copy2(scratch/target.name,target)
 reopened=scratch/'reopen';reopened.mkdir(exist_ok=True)
 cmd2=[str(exe),'--datadir',str(reopened/'studio-data'),*common,'--export-3mf',target.name,'--outputdir',str(reopened),str(target)]
 r2=subprocess.run(cmd2,capture_output=True,text=True,cwd=scratch);(reopened/'slice.log').write_text(r2.stdout+r2.stderr);assert r2.returncode==0,(r2.stdout+r2.stderr)[-5000:]
 with zipfile.ZipFile(target) as z1,zipfile.ZipFile(reopened/target.name) as z2:
  s1=json.loads(z1.read('Metadata/project_settings.config'));s2=json.loads(z2.read('Metadata/project_settings.config'))
  diff={k:[s1.get(k),s2.get(k)] for k in set(s1)|set(s2) if s1.get(k)!=s2.get(k)}
  (METADATA/'saved-settings.json').write_text(json.dumps(s1,indent=2)+'\n')
  clean=lambda t:'\n'.join(x for x in t.splitlines() if not x.startswith('; generated by'))
  equality=clean(z1.read('Metadata/plate_1.gcode').decode())==clean(z2.read('Metadata/plate_1.gcode').decode())
  assert not diff,diff
 record=dict(bambu_version='02.08.02.61',printer='Bambu Lab X1 Carbon 0.4 nozzle',plate_translation_mm=offset,project_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),reopened_project_sha256=hashlib.sha256((reopened/target.name).read_bytes()).hexdigest(),reopened_without_external_profiles=True,settings_differences=diff,gcode_equal_except_timestamp=equality, gcode_difference_note="Slicer path/seam ordering and estimates may change on reopen; both archives require independent geometric toolpath review",profile_provenance=dict(printer=ps,filament=fs,process=rs),physical_test='NOT PERFORMED')
 (METADATA/'build-and-reopen.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
if __name__=='__main__':main()
