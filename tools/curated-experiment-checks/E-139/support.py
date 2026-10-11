#!/usr/bin/env python3
"""E-139: finite cam walls/roller fits, free-input work, and coherent bounds.
Units mm, N, N mm except explicitly SI-labelled energy/inertia calculations.
No process priors, contact impact law, friction arrest or hardware qualification.
"""
import itertools
import json
import math
import numpy as np

R = .4


def law(u):
    u = np.asarray(u)
    t = np.clip((u-2)/4, 0, 1)
    h = 1-np.cos(np.pi*t)
    s = np.where((u>2)&(u<6), np.pi/4*np.sin(np.pi*t), 0.)
    k = np.where((u>2)&(u<6), np.pi**2/16*np.cos(np.pi*t), 0.)
    return h, s, k


def walls(n=256, gap=.1, lo_bias=0., hi_bias=0., warp=0.):
    # Exact normal offsets of analytic pitch curve, then finite straight edges.
    u = np.linspace(-1, 9, 5*n+1)
    h, s, _ = law(u)
    normal = np.stack((-s, np.ones_like(s)), axis=1)/np.sqrt(1+s*s)[:, None]
    curve = np.stack((u, h), axis=1)
    lo = curve-(R+gap-lo_bias)*normal
    hi = curve+(R+gap-hi_bias)*normal
    hi[:, 1] += warp
    assert np.all(np.diff(lo[:, 0])>0) and np.all(np.diff(hi[:, 0])>0)
    return lo, hi


def disk_above(poly, x, r):
    """Exact minimum disk-center height above finite polyline; tangent + vertices.
    Returns height and derivative with respect to x on the maximizing branch.
    No proxy bounding boxes replace wall/roller contact.
    """
    dx = poly[:, 0]-x
    valid = np.abs(dx)<r
    roots = np.sqrt(r*r-dx[valid]**2)
    values = poly[valid, 1]+roots
    deriv = dx[valid]/roots
    a, b = poly[:-1], poly[1:]
    slopes = (b[:, 1]-a[:, 1])/(b[:, 0]-a[:, 0])
    tangent_x = x+r*slopes/np.sqrt(1+slopes*slopes)
    active = (tangent_x>=a[:, 0]) & (tangent_x<=b[:, 0])
    lines = a[active, 1]+slopes[active]*(x-a[active, 0])+r*np.sqrt(1+slopes[active]**2)
    values = np.concatenate((values, lines))
    deriv = np.concatenate((deriv, slopes[active]))
    i = int(np.argmax(values))
    return float(values[i]), float(deriv[i])


def fit(lo, hi, u, r=R):
    bottom, slope = disk_above(lo, u, r)
    # Reflect upper boundary vertically; max reflected support gives min ceiling.
    reflected = hi * np.array([1., -1.])
    minus_top, _ = disk_above(reflected, u, r)
    return bottom, -minus_top-bottom, slope


def contact_checks():
    result = []
    for n in [32, 128, 512]:
        lo0, hi0 = walls(n, gap=0)
        lo, hi = walls(n)
        phases = np.linspace(0, 8, 8*n+1)
        data = np.array([fit(lo, hi, u) for u in phases])
        ideal = np.array([fit(lo0, hi0, u)[0] for u in phases])
        error = float(np.max(np.abs(ideal-law(phases)[0])))
        assert data[:, 1].min()>0
        assert np.max(np.abs(data[[0, -1], 0]-[-.1, 1.9]))<1e-12
        work = float(np.trapz(data[:, 2], phases))
        # Reverse the actual generated contact trace: signed travel and work.
        reverse_work = float(np.trapz(data[::-1, 2], phases[::-1]))
        assert abs(work+reverse_work)<1e-12
        result.append(dict(wall_subdivision=n, unique_poses=len(phases),
            zero_clearance_height_error_mm=error,
            minimum_vertical_fit_mm=float(data[:, 1].min()),
            work_error_at_1N_Nmm=abs(work-2)))
    # Cam tab x=[10-u,11-u], y=[1.4,2.4], z=[-1,0] strikes ground
    # blocks x=[1,2] and [11,12] at u=8 and u=0 respectively.
    tab=np.array([[10,1.4,-1],[11,2.4,0.]])
    blocks=[np.array([[1,1.4,-1],[2,2.4,0.]]),
            np.array([[11,1.4,-1],[12,2.4,0.]])]
    # Conservative body box, exact backplate/bridge/neck boxes.
    bodies=[tab,np.array([[-1,-.6,-1.5],[9,.6,3.5]]),
            np.array([[-1,.6,-1.5],[9,1.2,3.5]]),
            np.array([[8.5,.6,-1],[11,1.2,0.]]),
            np.array([[10,1.2,-1],[11,1.4,0.]])]
    for u in phases:
        for body,block in itertools.product(bodies,blocks):
            moved=body-np.array([u,0,0])
            overlap=np.maximum(0,np.minimum(moved[1],block[1])-np.maximum(moved[0],block[0]))
            assert np.prod(overlap)==0
        assert tab[0,0]-u-blocks[0][1,0]>=0
        assert blocks[1][0,0]-(tab[1,0]-u)>=0
    mid = fit(lo, hi, 4.)
    # Two independently translated copies: low centers exactly 12 and 32 mm.
    levels = [[base, base+2, base] for base in [12.,32.]]
    # Circle contact with neighboring pin at same or different retained height.
    # Same axial layer is required for engagement; z differences avoid collision.
    neighbor = {}
    for dh in [0.,20.,-20.]:
        x,z = 5.08,-.1+dh
        bottom, width, _ = fit(lo,hi,x)
        # Body z bounds -1.5,3.5; a far-away disk clears body entirely.
        outside_body = z-R>3.5 or z+R< -1.5
        neighbor[str(dh)] = dict(clears=bool(outside_body or bottom<=z<=bottom+width),
            lower_contact_center_mm=bottom, pin_center_mm=z)
    assert not neighbor['0.0']['clears']
    assert neighbor['20.0']['clears'] and neighbor['-20.0']['clears']
    return dict(convergence=result, retained_cycles_mm=levels,
        mid_loaded_height_mm=mid[0], mid_vertical_fit_mm=mid[1],
        mid_input_force_per_load=mid[2],
        mid_normal_per_load=math.sqrt(1+mid[2]**2), neighbor_at_low_input=neighbor)


def bounded_geometry():
    out=[]
    phases=np.linspace(0,8,97)
    for e in [0.,.025,.05,.1]:
        cases=[]
        signs=[(0,0,0,0)] if e==0 else itertools.product([-1,1], repeat=4)
        for br,bl,bh,bw in signs:
            lo,hi=walls(64,lo_bias=bl*e,hi_bias=bh*e,warp=bw*e)
            data=np.array([fit(lo,hi,u,R+br*e) for u in phases])
            cases.append((float(data[:,1].min()),float(np.max(np.abs(data[:,2])))))
        out.append(dict(bound_mm=e,coherent_corner_cases=len(cases),
            worst_vertical_fit_mm=min(c[0] for c in cases),
            max_slope=max(c[1] for c in cases),
            interfering_cases=sum(c[0]<-1e-9 for c in cases)))
    return out


def free_input():
    # Independent ideal smooth, zero-clearance check, release from u=4 at rest.
    # SI: m_c=cam/input effective mass; m_o=output mass, F=total imposed load.
    rows=[]
    for force, mc in itertools.product([.2,1.,10.],[.005,.02,.1]):
        mo=.01
        phases=np.linspace(2.000001,4,2001)
        h,s,k=law(phases)
        drop=(1-h)*.001
        speed2=2*force*drop/(mc+mo*s*s)
        curv=k*1000  # 1/mm -> 1/m
        accel=(-force*s-mo*s*curv*speed2)/(mc+mo*s*s)
        zacc=curv*speed2+s*accel
        normal=(force+mo*zacc)*np.sqrt(1+s*s)
        # Lower-wall contact remains compressive on this descending half-path.
        assert normal.min()>0
        energy_error=np.max(np.abs(.5*(mc+mo*s*s)*speed2+force*h*.001-force*.001))
        v=math.sqrt(2*force*.001/mc)
        rows.append(dict(load_N=force,input_mass_kg=mc,
            min_lower_normal_N=float(normal.min()),energy_error_J=float(energy_error),
            low_dwell_speed_m_s=v,dwell_traverse_s=.002/v,
            kinetic_energy_at_input_stop_mJ=force))
    # Constraint g=z-h(u)=0 has Jacobian [-h',1]; all conjugate rows are parallel.
    slope=math.pi/4
    jac=np.array([[-slope,1.],[slope,-1.]])
    tangent=np.array([1.,slope])
    assert np.linalg.norm(jac@tangent)<1e-14 and np.linalg.matrix_rank(jac)==1
    # Independent finite difference and force-work check.
    eps=1e-5
    fd=(law(4+eps)[0]-law(4-eps)[0])/(2*eps)
    assert abs(fd-slope)<1e-9
    # A constant balancing force F0 merely changes F to residual F-F0.
    balance={str(f):-(f-1.)*slope for f in [.2,1.,10.]}
    return dict(release_phase_mm=4,available_drop_mm=1,
        conjugate_constraint_rank=int(np.linalg.matrix_rank(jac)),
        unpowered_generalized_force_at_1N_N=-slope,
        balancing_1N_residual_input_force_N=balance,scenarios=rows)


def travelling_pallet():
    # Ground-guided rocking arm: center of radius-.4 nose at (L cos t,L sin t).
    # A horizontal platform rests on the nose; its vertical guide reacts laterally.
    # Stops t=0,pi/6 bound a 2mm lift; no invented intermediate brake/return.
    L=4.; radius=.4
    theta=np.linspace(0,math.pi/6,257)
    contact=np.stack((L*np.cos(theta),L*np.sin(theta)+radius),axis=1)
    # Nose tangent lies within platform x=[3,4.5], thickness .6, y width .8.
    assert contact[:,0].min()>3 and contact[:,0].max()<4.5
    # Arm capsule r=.2 below its nose: .2mm clearance under platform except nose.
    assert radius>.2
    # Circular lug/ground seat tips in a separate axial layer. Both radius .15.
    lug_radius=.15
    delta=2*math.asin(lug_radius)
    lug=np.stack((np.cos(theta),np.sin(theta)),axis=1)
    seats=np.array([[math.cos(-delta),math.sin(-delta)],
                    [math.cos(math.pi/6+delta),math.sin(math.pi/6+delta)]])
    gaps=np.linalg.norm(lug[:,None,:]-seats[None,:,:],axis=2)-2*lug_radius
    assert gaps.min()>-1e-12 and abs(gaps[0,0])<1e-12 and abs(gaps[-1,1])<1e-12
    high_normal=(lug[-1]-seats[1])/(2*lug_radius)
    high_tangent=np.array([-math.sin(theta[-1]),math.cos(theta[-1])])
    # Upper stop pushes toward decreasing angle, same sign as downward load.
    assert float(high_normal@high_tangent)<0
    moment=L*np.cos(theta)
    work=np.trapz(moment,theta)
    # All points backdrive toward lower angular stop; high stop cannot resist it.
    assert moment.min()>0
    return dict(lift_mm=float(contact[-1,1]-contact[0,1]),
        input_torque_per_load_Nmm=[float(moment.min()),float(moment.max())],
        arm_radius_mm=.2,platform_x_mm=[3,4.5],nose_radius_mm=radius,
        work_error_at_1N_Nmm=float(abs(work-2)),
        high_stop_normal_moment_per_N_mm=float(high_normal@high_tangent),
        high_endpoint_retained=False)


def board():
    out=[]
    for cycle_s in [.01,.05,.1]:
        cell_s=.05+20*cycle_s
        heads=next(n for n in range(1,6401) if 6+math.ceil(6400/n)*cell_s<30)
        out.append(dict(complete_2mm_cycle_s=cycle_s,
            map_80_heads_s=6+80*cell_s,min_heads=heads,
            free_cells_head_allowance_USD=250/heads))
    return dict(cells=6400,step_count=20,ideal_field_work_at_1N_J=256,
        two_cam_walls=12800,roller_axes=6400,
        optimistic_local_allowance_with_250_shared_USD=250/6400,
        illustrative_step_schedule=out,
        direct_40mm_cam_ramp_mm=80,direct_40mm_cam_stroke_mm=84,
        direct_40mm_cam_body_width_mm=86)


def main():
    print(json.dumps(dict(evidence='finite geometry and conservative calculations; no measurements',
        contacts=contact_checks(),bounded_geometry=bounded_geometry(),
        free_input=free_input(),travelling_pallet=travelling_pallet(),board=board()),indent=2))

if __name__=='__main__':
    main()
