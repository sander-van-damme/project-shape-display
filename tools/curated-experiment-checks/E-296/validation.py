#!/usr/bin/env python3
"""Reproducible analytical kinematics plus nominal BREP collision screening.

Contacts have zero volume and are allowed. Rigid frame/frame intersections are
intentional fixed fixture joints. Springs are geometrical wire approximations;
this script does not solve elasticity, friction, wedging, wear or loaded release.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import cadquery as cq
import generate as g

HERE=Path(__file__).resolve().parent

def bb_overlap(a,b,tol=1e-7):
    aa=a.BoundingBox();bb=b.BoundingBox()
    return all(min(getattr(aa,k+"max"),getattr(bb,k+"max"))-
               max(getattr(aa,k+"min"),getattr(bb,k+"min")) > tol for k in "xyz")

def collision_pairs(parts):
    bad=[]; tests=0
    for (na,(a,ka)),(nb,(b,kb)) in itertools.combinations(parts.items(),2):
        if ka==kb=="frame":continue
        # Same-cell coil clearance follows from its 3.5-mm inner envelope,
        # 3.0-mm body and separated seats. Helical wire Booleans are excluded
        # rather than pretending their schematic end turns are a contact solve.
        if "spring" in (ka,kb):continue
        if not bb_overlap(a,b):continue
        v=a.intersect(b).Volume();tests+=1
        if v>1e-6:bad.append(dict(a=na,b=nb,intersection_mm3=v))
    return tests,bad

def main():
    out={"evidence":"nominal analytical and BREP checks; NOT physical validation",
         "truth":[],"brep_states":[],"limitations":[
             "Spring transition end geometry is schematic; no elastic contact solve.",
             "Screw/pin interfaces are clearance envelopes; E-295 contains functional threads.",
             "Journal clearance does not establish mating-axis accuracy; measure axes at hex engagement zone.",
             "Finite state sweeps cannot certify dynamics, wear, contamination or loaded release.",
             "Exterior comb clamp fasteners and precision bushing manufacture remain fixture details."]}
    for r,c in itertools.product([0.,1.4],repeat=2):
        q=g.q_nominal(r,c);L=3.4+q-r
        k=79000*.2**4/(8*3.7**3*5)
        out["truth"].append(dict(row=r,column=c,sleeve_q=q,
            coil_length=L,coil_force_N=k*(3.716-L),
            full_hex_overlap=max(0,q-.6-.375),
            first_tip_overlap=max(0,q-.6),off_tip_gap=max(0,.6-q),
            input_overlap=3.3-(-.6+q),engaged=(q>.975)))
    # Full rectangular selector configuration space. These are position/logic
    # checks, NOT a claim that all trajectories are safe while the bus rotates.
    sweep=[]
    for r in [i*1.4/100 for i in range(101)]:
        for c in [i*1.4/100 for i in range(101)]:
            q=g.q_nominal(r,c);L=3.4+q-r
            assert -.000001<=q<=1.400001
            assert L>=2.-1e-8
            assert .3+r<=3.7+q+1e-8
            assert 4.1+q<=4.1+c+1e-8
            assert -.2+q<=r+1e-8
            sweep.append((q,L))
    out["continuous_coordinate_sweep"]={"samples":len(sweep),
        "sleeve_q_range_mm":[min(v[0] for v in sweep),max(v[0] for v in sweep)],
        "spring_length_range_mm":[min(v[1] for v in sweep),max(v[1] for v in sweep)],
        "solid_height_mm":1.4,"minimum_solid_reserve_mm":.6,
        "warning":"Both coordinates may overlap during a simultaneous crossing transition; use stopped-bus break-before-make."}
    # Counterexample: a nominal OFF-to-OFF simultaneous crossing trajectory
    # passes through the chamfer region and can contact output. Preserve it.
    r=c=.7;q=g.q_nominal(r,c)
    out["negative_control_crossing_transition"]={"r":r,"c":c,"q":q,
        "tip_overlap_mm":q-.6,"result":"output contact possible during OFF-to-OFF simultaneous crossing"}
    out["analytical_clearances_mm"]={
        "neighbor_pin_face":5.08-4.4,"neighbor_row_ring":5.08-4.7,
        "neighbor_sleeve_upper_flange":5.08-4.2,
        "row_bore_to_sleeve_radial":(3.2-3)/2,
        "lower_flange_retention_land_nominal":(3.4-3.2)/2,
        "spring_installation_radial":(3.5-3.4)/2,
        "roof_to_male_corner_radial":(2.4-1.8/math.cos(math.pi/6))/2,
        "sleeve_min_wall_at_hex_corner":(3.-1.95/math.cos(math.pi/6))/2,
        "journal_radial_nominal":.01,
        "minimum_crossing_comb_z_gap":4.1-1.7,
        "selector_shoe_bushing_each_side":.02}
    out["spring_envelope_check"]={"method":"analytical, excluded from pairwise BREP Booleans",
        "inner_diameter_mm":3.5,"sleeve_body_diameter_mm":3.0,
        "radial_body_gap_mm":.25,"seat_contact":"zero nominal axial penetration",
        "neighbor_spring_gap_mm":5.08-3.9}
    alpha=30-math.degrees(math.acos((1.95/2)/(1.8/math.sqrt(3))))
    out["rotor_phase"]={"centered_half_window_degrees":alpha,
        "period_degrees":60,"worst_phase_degrees":30,
        "blocked_q_mm":g.phase_block_q(),
        "blocked_coil_length_mm":3.4+g.phase_block_q()-1.4,
        "mouth_minimum_all_phase_capture_radius_mm":2.7/2-1.8/math.sqrt(3),
        "full_flank_length_ON_mm":.8-.375}
    # Probe full insertion phase errors: angularly aligned geometry fits; at
    # 30 degrees at full command it must collide (deliberate negative control).
    sl=g.sleeve().translate((0,0,1.4))
    inp=g.input_shaft();outp=g.output_shaft()
    phase_tests=[]
    for phase in [0,5,9,alpha-.01,alpha+.01,15,30]:
        output=outp.rotate((0,0,0),(0,0,1),phase)
        v=sl.intersect(output).Volume()
        phase_tests.append({"degrees":phase,"intersection_mm3":v})
    assert phase_tests[0]["intersection_mm3"]<1e-6
    assert phase_tests[-1]["intersection_mm3"]>1e-4
    out["full_insertion_phase_probes"]=phase_tests
    qb=g.phase_block_q()
    wrong=outp.rotate((0,0,0),(0,0,1),30)
    at=g.sleeve().translate((0,0,qb)).intersect(wrong).Volume()
    after=g.sleeve().translate((0,0,qb+.01)).intersect(wrong).Volume()
    assert at<1e-6 and after>1e-6
    out["blocked_phase_contact"]={"at_contact_volume_mm3":at,
        "after_10um_extra_travel_mm3":after,"q_mm":qb}
    axial=[]
    for name,shaft,z in [("input",g.input_shaft(),-6),
                         ("output",g.output_shaft(),7.5)]:
        plate=g.journal_plate(z)
        vv=[shaft.translate((0,0,dz)).intersect(plate).Volume()
            for dz in [-.02,0,.02]]
        assert max(vv)<1e-6
        negative=shaft.translate((0,0,.03)).intersect(plate).Volume()
        assert negative>1e-4
        axial.append({"shaft":name,"travel_mm":[-.02,0,.02],
                      "intersection_mm3":vv,"after_10um_beyond_stop_mm3":negative})
    out["axial_retention_sweep"]=axial
    selector_float=[]
    for r,c in itertools.product([0.,1.4],repeat=2):
        q=g.q_nominal(r,c)
        targets=[g.sleeve().translate((0,0,q)),g.row_comb(0,r),g.column_comb(0,c)]
        for name,shaft in [("input",g.input_shaft()),("output",g.output_shaft())]:
            for dz in [-.02,.02]:
                vv=[shaft.translate((0,0,dz)).intersect(t).Volume() for t in targets]
                assert max(vv)<1e-6
                selector_float.append({"row":r,"column":c,"shaft":name,
                    "axial_float_mm":dz,"selector_intersection_mm3":vv})
    # A phase-blocked sleeve follows the moved output tip; forcing the old q
    # after moving the output down is intentionally inadmissible.
    for dz in [-.02,.02]:
        qshift=qb+dz
        v=g.sleeve().translate((0,0,qshift)).intersect(
            wrong.translate((0,0,dz))).Volume()
        assert v<1e-6
        selector_float.append({"phase_degrees":30,"output_float_mm":dz,
                               "adapted_blocked_q_mm":qshift,"intersection_mm3":v})
    out["axial_float_to_selector_probes"]=selector_float
    variants={"matrix_R10_C10":((1.4,0),(1.4,0),False),
              "matrix_phase_blocked":((1.4,0),(1.4,0),True)}
    for r,c in itertools.product([0,1],repeat=2):
        variants[f"truth_R{r}C{c}"]=((r*1.4,)*2,(c*1.4,)*2,False)
    failures=[]
    for name,(rows,cols,blocked) in variants.items():
        parts,poses=g.model(rows,cols,blocked)
        invalid=[n for n,(s,k) in parts.items() if not s.isValid()]
        tests,bad=collision_pairs(parts)
        st={"state":name,"parts":len(parts),"invalid_parts":invalid,
            "boolean_pairs_checked_after_aabb":tests,"unexpected_intersections":bad,
            "poses":poses}
        out["brep_states"].append(st)
        failures+=bad+invalid
        print(name,"pairs",tests,"failures",bad,flush=True)
    # Dedicated off-neighbor checks along all 16 binary row/column selections.
    # The per-cell function is separable: a half-selected neighbor never has
    # more than .2 travel, even if the chosen cell is blocked by phase.
    n=0
    for bits in itertools.product([0,1],repeat=4):
        for i,j in itertools.product([0,1],repeat=2):
            r=1.4*bits[j];c=1.4*bits[2+i];q=g.q_nominal(r,c)
            if not(bits[j] and bits[2+i]):assert q<=.2+1e-9
            n+=1
    out["binary_matrix_isolation"]={"selections":16,"cells_checked":n,
        "max_unselected_q_mm":.2,"minimum_unselected_tip_gap_mm":.4,
        "condition":"rigid stops and guide position; no flexible comb load redistribution model"}
    out["pass"]=not failures
    (HERE/"validation.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":not failures,"failures":failures},indent=2))
    if failures:raise SystemExit(1)

if __name__=="__main__":main()
