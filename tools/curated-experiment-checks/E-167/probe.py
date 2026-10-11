#!/usr/bin/env python3
"""E-167 finite bayonet gate screen. mm, N, seconds; bounds, not process priors."""
import itertools
import json
import math

P = 5.08

def rectangle(hx, hy, angle=0., dx=0., dy=0.):
    c, s = math.cos(angle), math.sin(angle)
    return [(dx+c*x-s*y, dy+s*x+c*y)
            for x,y in [(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]]

def intersect(a, b):
    """Strict positive-area convex polygon intersection by separating axes."""
    for poly in (a,b):
        for u,v in zip(poly, poly[1:]+poly[:1]):
            axis = (u[1]-v[1], v[0]-u[0])
            pa = [x*axis[0]+y*axis[1] for x,y in a]
            pb = [x*axis[0]+y*axis[1] for x,y in b]
            if min(max(pa),max(pb))-max(min(pa),min(pb)) <= 1e-10:
                return False
    return True

def box(x0,x1,y0,y1,z0,z1):
    return (rectangle((x1-x0)/2,(y1-y0)/2,dx=(x0+x1)/2,dy=(y0+y1)/2),z0,z1)

def gate(a=.8,s=.65,pocket=.65,depth=.4):
    # Aperture is union of full-width x slot |y|<s and central |x|,|y|<a.
    # Raised rails leave a pocket around locked lug |x|<pocket.
    result=[]
    for sign in (-1,1):
        y0,y1=sorted((sign*max(a,s),sign*P/2))
        result.append(box(-P/2,P/2,y0,y1,-1.2,0))
        for xs in (-1,1):
            x0,x1=sorted((xs*a,xs*P/2))
            yy0,yy1=sorted((sign*s,sign*a))
            if a>s:
                result.append(box(x0,x1,yy0,yy1,-1.2,0))
            x0,x1=sorted((xs*pocket,xs*P/2))
            result.append(box(x0,x1,y0,y1,0,depth))
    return result

def collisions(angle,z,solids,half=2.,width=.45,dx=0.,dy=0.,thickness=1.2):
    poly=rectangle(half,width,angle,dx,dy)
    return sum(min(z+thickness,z1)-max(z,z0)>1e-9 and intersect(poly,p)
               for p,z0,z1 in solids)

def path_checks(n,lift=.6):
    solids=gate()
    counts={'poses':0,'collisions':0}
    def check(angle,shift):
        for j in range(5):
            counts['poses']+=1
            counts['collisions']+=collisions(angle,shift+10*j,solids)
    for old,new in itertools.permutations(range(5),2):
        for k in range(n+1):
            t=k/n
            check(math.pi/2,-10*old+lift*t)       # lift from pocket
            check(math.pi/2*(1-t),-10*old+lift)  # turn into slit
            check(0,-10*(old+(new-old)*t)+lift)  # traverse any rung
            check(math.pi/2*t,-10*new+lift)      # turn over shelf
            check(math.pi/2,-10*new+lift*(1-t))  # seat pocket
    assert counts['collisions']==0
    # Seated rotation hits pocket walls; elevated rotation is clear.
    assert collisions(math.pi/4,0,solids)>0
    assert collisions(math.pi/4,.6,solids)==0
    # Unturned axial transfer intersects plate: deliberate fault witness.
    assert collisions(math.pi/2,-.6,solids)>0
    return counts

def bounds(e):
    # Relative centre x/y +-e, independent edge error +-e on moving and gate.
    # Bank-common shape/registration errors can place every cell at one corner.
    # Worst errors share e for conservative competing scenarios, not random priors.
    slot=.65-.45-3*e
    pocket=.65-.45-3*e
    shaft=.8-.6-3*e
    radial=P/2-math.hypot(2+e,.45+e)-math.sqrt(2)*e
    support=2-.8-3*e
    lift=.6-.4-2*e # differential stroke shortfall and pocket depth growth
    return dict(error=e,slot=slot,pocket=pocket,shaft=shaft,radial=radial,
                support=support,lift=lift)

def verify_corners(e):
    # Actual manufactured rectangles vs solids at all 64 coherent corner cases.
    totals={'corners':0,'slot_failures':0,'pocket_failures':0}
    for dx,dy,dl,dw,da,ds in itertools.product((-e,e),repeat=6):
        solids=gate(a=.8+da,s=.65+ds,pocket=.65+ds)
        totals['corners']+=1
        totals['slot_failures']+=bool(collisions(0,-.6,solids,2+dl,.45+dw,dx,dy))
        totals['pocket_failures']+=bool(collisions(math.pi/2,.1,solids,2+dl,.45+dw,dx,dy))
    return totals

def surface(n):
    moving=4.8
    neighbors=[rectangle(2.4,2.4,dx=x*P,dy=y*P)
               for x,y in itertools.product((-1,0,1),repeat=2) if x or y]
    phases=[i*math.pi/2/n for i in range(n+1)]
    hits=[a for a in phases if any(intersect(rectangle(moving/2,moving/2,a),b)
                                 for b in neighbors)]
    analytical=math.pi/4-math.acos((2*P/moving-1)/math.sqrt(2))
    # Independent support-function first-contact equation.
    assert abs(hits[0]-analytical)<=math.pi/2/n+1e-12
    return {'first_collision_deg':math.degrees(hits[0]),
            'analytic_first_contact_deg':math.degrees(analytical),
            'isolated_rotating_top_max_width':2*P/(1+math.sqrt(2)),
            'both_rotating_max_width':P/math.sqrt(2),
            'projection_intrusion_at_45':moving/math.sqrt(2)-(P-moving/2)}

def cap_route(lift,n=256):
    # 2-mm square cap; 44 mm above stem shift. Unchanged neighbors locked.
    # Check actual polygons and z intervals vs all five neighbor heights/lugs.
    hits=0
    poses=0
    for state,other in itertools.product(range(5),repeat=2):
        for step in range(n+1):
            angle=math.pi/2*step/n
            poly=rectangle(2.4,2.4,angle)
            z=44-10*state+lift
            for dx,dy in ((P,0),(-P,0),(0,P),(0,-P)):
                neighbor_top=44-10*other
                if min(z,neighbor_top)>max(z-2,neighbor_top-2)+1e-9:
                    hits+=intersect(poly,rectangle(2.4,2.4,dx=dx,dy=dy))
                for j in range(5):
                    lugz=10*(j-other)
                    if min(z,lugz+1.2)>max(z-2,lugz)+1e-9:
                        hits+=intersect(poly,rectangle(2,.45,math.pi/2,dx,dy))
                poses+=1
    return dict(poses=poses,collisions=hits,
                cap_to_stem_radial_margin=P-4.8/math.sqrt(2)-1.4,
                diagonal_active_cap_gap=math.sqrt(2)*P-2*4.8/math.sqrt(2))

def timing(lift=.6):
    def travel(d,v,a):
        return 2*math.sqrt(d/a) if d<=v*v/a else d/v+v/a
    # Axial 40-mm stroke plus two lift/seat moves; two 90-degree turns.
    linear=travel(40,300,3000)+2*travel(lift,300,3000)
    out=[]
    for omega in (360,720,1440): # deg/s; acceleration 7200 deg/s^2
        service=linear+2*travel(90,omega,7200)+.05
        h=next(h for h in range(1,6401) if 6+math.ceil(6400/h)*service<30)
        out.append(dict(omega_deg_s=omega,service_s=service,heads=h,
                        map_s=6+math.ceil(6400/h)*service))
    return out

def structural():
    # Euler is an ideal elastic diagnostic, not a printed-column allowable.
    result=[]
    for radius,modulus,k in itertools.product((.6,1.2,1.4),(1000,2000,3000),(1,2)):
        inertia=math.pi*radius**4/4
        critical=math.pi**2*modulus*inertia/(k*44)**2
        result.append(dict(radius=radius,E_MPa=modulus,effective_length_factor=k,
                           euler_N=critical,gate_land_mm=2-(radius+.2)))
    return result

def main():
    assert not intersect(rectangle(1,1),rectangle(1,1,dx=2))
    assert intersect(rectangle(1,1),rectangle(1,1,dx=1.99))
    # Union-aperture holdout: a wide slot must not create inverted shoulders.
    assert collisions(0,-.6,gate(a=.7,s=.8,pocket=.8),width=.75)==0
    # Width threshold holdouts independent of a grid search.
    for d in (2*P/(1+math.sqrt(2))-.001,2*P/(1+math.sqrt(2))+.001):
        hit=intersect(rectangle(d/2,d/2,math.pi/4),rectangle(d/2,d/2,dx=P))
        assert hit==(d>2*P/(1+math.sqrt(2)))
    corners={str(e):verify_corners(e) for e in (.025,.05,.1,.15)}
    assert corners['0.05']['slot_failures']==0
    assert corners['0.1']['slot_failures']>0
    data={'paths':{str(n):path_checks(n) for n in (16,64,256)},
          'interlevel_gate_paths':path_checks(64,2.3),
          'surface':{str(n):surface(n) for n in (64,256,1024)},
          'bounded_scenarios':[bounds(e) for e in (.025,.05,.1,.15)],
          'angular_clearance_at_e_005':{str(d):.65-.1-(.45+.05)*math.cos(math.radians(d))
                 -(2+.05)*math.sin(math.radians(d)) for d in (0,1,2,3)},
          'stem_elastic_scenarios':structural(),
          'actual_geometry_corners':corners,'timing_short_lift':timing(),
          'timing_interlevel_lift':timing(2.3),
          'cap_short_lift':cap_route(.6),'cap_interlevel_lift':cap_route(2.3),
          'nominal_contact_area_mm2':2*(2-.8)*.9,
          'mean_contact_MPa_at_10N':10/(2*(2-.8)*.9),
          'pocket_gravity_energy_mJ_for_10g':.01*9.81*.4,
          'full_lug_inventory':6400*5,
          'cost_per_cell_at_250_shared':250/6400}
    assert data['cap_short_lift']['collisions']>0
    assert data['cap_interlevel_lift']['collisions']==0
    print(json.dumps(data,indent=2))

if __name__=='__main__':
    main()
