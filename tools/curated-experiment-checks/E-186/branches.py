"""E-186: ideal differential constraints and finite friction-brake handovers.
SI units, Python 3 + NumPy. All numerical physical inputs are bounded assumptions.
No generated gear geometry, calibrated process distribution or hardware qualification.
"""
import itertools
import json
import math
import numpy as np


def solve_constraints(A, b, n):
    A = np.asarray(A, dtype=float).reshape(-1, n)
    b = np.asarray(b, dtype=float)
    q = np.linalg.lstsq(A, b, rcond=None)[0]
    return bool(np.max(np.abs(A @ q-b), initial=0) < 1e-10), n-int(np.linalg.matrix_rank(A)), q


def tree(leaves):
    assert leaves >= 2 and leaves & (leaves-1) == 0
    n = 2*leaves-1
    A = []
    for i in range(leaves-1):
        row = np.zeros(n)
        row[i], row[2*i+1], row[2*i+2] = -2, 1, 1
        A.append(row)
    return A, n


def topology_checks():
    states = []
    # q=(carrier, work, second output); all eight ground-contact combinations.
    for held in itertools.product((False, True), repeat=3):
        A = [[-2, 1, 1]] + [np.eye(3)[i] for i, yes in enumerate(held) if yes]
        ok, dof, q = solve_constraints(A, [0]*len(A), 3)
        assert ok
        states.append({'grounded_C_W_D': held, 'free_dof': dof})
    assert states[4]['free_dof'] == 1  # source grounded alone
    assert states[3]['free_dof'] == 0  # both branches grounded, source free
    assert not solve_constraints([[-2,1,1],[1,0,0],[0,1,0],[0,0,1]], [0,1,0,0],3)[0]
    # Planetary ratio changes speed/torque, not this rank defect.
    for a in (.25, .5, .75):
        ok, dof, q = solve_constraints([[-1,a,1-a],[1,0,0]], [0,0],3)
        assert ok and dof == 1
        witness = np.array([0,1,-a/(1-a)])
        assert abs(np.dot([-1,a,1-a],witness)) < 1e-12
    trees=[]
    for leaves in (2,4,8,16,32,64):
        A,n=tree(leaves)
        ok,dof,_=solve_constraints(A+[np.eye(n)[0]], [0]*(len(A)+1),n)
        assert ok and dof == leaves-1
        # Hold all but one terminal; root speed 1 gives last terminal speed N.
        hold=[np.eye(n)[i] for i in range(leaves-1,n-1)]
        ok,free,q=solve_constraints(A+[np.eye(n)[0]]+hold,[0]*len(A)+[1]+[0]*len(hold),n)
        assert ok and free==0 and abs(q[-1]-leaves)<1e-8
        trees.append({'leaves':leaves,'root_held_free_dof':dof,'single_free_leaf_speed':float(q[-1])})
    return {'states':states,'trees':trees}


def transition(W, Jd, B, v, direction, stage, radius=.002):
    """Constant carrier speed. Swap grounded friction brakes, no gear loss.
    Progress work angular speed 0..v/r; dummy=2*carrier-work.
    direction converts gravity into progress torque; W is net downward N.
    Mass choice matches E-185 bound, not a measured load population.
    """
    M=max(.002,W/9.81)
    Jw=M*radius**2+1e-8
    J=Jw+Jd
    L=direction*W*radius
    speed=v/radius
    start = stage=='start'
    bw,bd=(0,B) if start else (B,0)
    alpha=(-L-bw+bd)/J
    if (start and alpha<=0) or (not start and alpha>=0):
        return {'state':'no_transition'}
    u0,u1=(0,speed) if start else (speed,0)
    t=(u1-u0)/alpha
    x=(u0+u1)*t/2
    xd=speed*t-x
    lam=Jw*alpha+L+bw
    source=2*lam*(speed/2)*t
    heat=bw*x+bd*xd
    potential=L*x
    delta=.5*Jw*(u1*u1-u0*u0)+.5*Jd*((speed-u1)**2-(speed-u0)**2)
    assert abs(source-heat-potential-delta)<1e-9
    # Separate constrained three-axis Newton solve validates reduced equation.
    A=np.array([[1.,1.,-2.],[0,0,1.]])
    mass=np.diag([Jw,Jd,1e-6])
    force=np.array([-L-bw,-bd,0.])
    mat=np.block([[mass,-A.T],[A,np.zeros((2,2))]])
    full=np.linalg.solve(mat,np.r_[force,[0.,0.]])
    assert np.allclose(full[:3],[alpha,-alpha,0.],rtol=1e-9,atol=1e-7)
    assert abs(full[4]-2*lam)<1e-9
    # Midpoint integration is exact for constant acceleration, not contact accuracy.
    for steps in (8,32,128):
        dt=t/steps;u=u0;pos=0.;qd=0.
        for _ in range(steps):
            mid=u+alpha*dt/2
            pos+=mid*dt;qd+=(speed-mid)*dt;u+=alpha*dt
        assert abs(pos-x)<1e-9 and abs(qd-xd)<1e-9
    return {'state':'finite','time_s':t,'work_travel_mm':x*radius*1000,
            'brake_heat_J':heat,'source_work_J':source,'source_torque_Nm':2*lam,
            'kinetic_change_J':delta,'gravity_work_J':potential}


def fixed_source_release(W1,W2,delay,Jextra=2e-8,r=.002):
    # Carrier already held, outputs initially stationary. No source-stop impulse.
    J1=max(.002,W1/9.81)*r*r+Jextra/2
    J2=max(.002,W2/9.81)*r*r+Jextra/2
    a=-(W1-W2)*r/(J1+J2)
    q=.5*a*delay*delay
    energy=.5*(J1+J2)*(a*delay)**2+(W1-W2)*r*q
    assert abs(energy)<1e-12
    return r*q*1000


def finite_move(distance, W, Jd, B, v, direction, radius=.002):
    """Reach arbitrary short moves by exchanging friction brakes before full speed.
    Ideal instantaneous commanded torque changes; actual contact remains unbuilt.
    """
    if distance==0:return {'time_s':0.,'peak_m_s':0.}
    J=max(.002,W/9.81)*radius**2+1e-8+Jd
    aa=radius*(B-direction*W*radius)/J
    ab=radius*(B+direction*W*radius)/J
    if min(aa,ab)<=0:return None
    peak=min(v,math.sqrt(2*distance/(1/aa+1/ab)))
    ramp=.5*peak**2*(1/aa+1/ab)
    t=peak/aa+peak/ab+max(0.,distance-ramp)/peak
    return {'time_s':t,'peak_m_s':peak}


def outage_descent(W, Jsource_per_head, B, v, delay, radius=.002):
    """Symmetric bus cut; all dummy brakes remain grounded, outputs descend.
    Jsource_per_head is carrier inertia/(4*engaged_heads), referred to work.
    Brake torque steps on after delay. No spring/actuator dynamics qualification.
    """
    Jw=max(.002,W/9.81)*radius**2+1e-8
    J=Jw+Jsource_per_head
    L=W*radius
    u=v/radius
    ad=L/J
    x1=u*delay+.5*ad*delay**2
    u1=u+ad*delay
    if B<=L:return {'state':'no_arrest'}
    decel=(B-L)/J
    x2=u1**2/(2*decel)
    initial=.5*J*u*u
    assert abs(initial+L*(x1+x2)-B*x2)<1e-9
    return {'state':'first_stop','travel_mm':radius*(x1+x2)*1000,
            'time_s':delay+u1/decel,'brake_heat_J':B*x2}


def schedule(v, W, Jd, B):
    # Four signed traversals per bank: empty approach up, loaded up/down,
    # empty return down. Grants independent brake control and synchronized bus.
    # Each leg rest-to-rest: L/v + (t_accel+t_decel)/2 when trapezoid fits.
    legs=[]
    for load,d in ((.002*9.81,1),(W,1),(W,-1),(.002*9.81,-1)):
        a=transition(load,Jd,B,v,d,'start')
        b=transition(load,Jd,B,v,d,'stop')
        if a['state']!='finite' or b['state']!='finite':return None
        if a['work_travel_mm']+b['work_travel_mm']>40:return None
        legs.append(.04/v+(a['time_s']+b['time_s'])/2)
    service=.10+sum(legs)
    for h in range(1,6401):
        T=6+math.ceil(6400/h)*service
        if T<30:
            return {'service_s':service,'H':h,'map_s':T,
                    'channel_dollar_ceiling_shared250':250/h,
                    'channel_dollar_ceiling_site002':(250-6400*.02)/h,
                    'ideal_peak_load_power_W':h*W*v}
    return None


def run():
    topology=topology_checks()
    for v in (.1,.2,.3):
        for old,new in itertools.product(range(21), repeat=2):
            d=1 if new>=old else -1
            move=finite_move(abs(new-old)*.002,1,1e-8,.003,v,d)
            full=finite_move(.04,1,1e-8,.003,v,d)
            assert move is not None and move['time_s']<=full['time_s']+1e-12
            assert move['peak_m_s']<=v
    short_move=finite_move(.002,1,1e-8,.003,.3,1)
    sweep=[]
    for W,Jd,B,v,d,stage in itertools.product((.02,1,10),(1e-8,1e-6,1e-5),(.003,.01,.03),(.1,.3),(1,-1),('start','stop')):
        result=transition(W,Jd,B,v,d,stage)
        sweep.append({'W':W,'Jd':Jd,'B':B,'v':v,'direction':d,'stage':stage,**result})
    finite=[r for r in sweep if r['state']=='finite']
    base={f'{d}_{stage}':transition(1,1e-8,.003,.1,d,stage) for d,stage in itertools.product((1,-1),('start','stop'))}
    # Friction radius/normal-force box with coherent low mu and radius bias.
    capacities=[]
    for mu,radius,F in itertools.product((.1,.3),(.003,.006), (1.,5.)):
        cap=mu*radius*.9*F
        capacities.append({'mu':mu,'radius_m':radius,'normal_N':F,'capacity_Nm':cap,
                           'both_signs_1N':cap>.002,'both_signs_10N':cap>.020})
    schedules={}
    for v in (.1,.2,.3):
        schedules[str(v)]=schedule(v,1,1e-8,.003)
    return {'topology':topology,'base_transitions':base,'short_2mm_at_bus03':short_move,
            'sweep':{'cases':len(sweep),'finite':len(finite),'no_transition':len(sweep)-len(finite),
                     'over40mm_single_transition':sum(x['work_travel_mm']>40 for x in finite),
                     'max_transition_mm':max(x['work_travel_mm'] for x in finite)},
            'grounded_source_unbraked_pair_mm':{str(t):fixed_source_release(1,.02,t) for t in (.001,.005,.02)},
            'brake_capacity_corners':capacities,'schedules':schedules,
            'outage_down':[{ 'Jsource_per_head':j,'delay_s':t,**outage_descent(1,j,.003,.1,t)}
                           for j,t in itertools.product((1e-8,1e-6,1e-4),(.001,.005,.02))],
            'direct_E185_control':{'H':82,'loaded_s':.13780,'empty_return_s':.06305},
            'checks':'constraint rank, affine incompatibility, independent KKT dynamics, signed work, 8/32/128 integration'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
