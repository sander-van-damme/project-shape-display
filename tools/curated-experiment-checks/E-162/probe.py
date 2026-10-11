"""E-162: finite sphere/cylinder geometry, implicit elastic/Coulomb time step.
Python 3 + NumPy. SI units. Bounds, not calibrated materials or a CAD assembly.
"""
import argparse
import json
import math
from dataclasses import dataclass
import numpy as np

A = math.radians(20)

@dataclass
class Model:
    R: float = .0015
    r: float = .0005
    e: float = .00005
    preload: float = 30.
    kp: float = 1.e4
    kc: float = 1.e6
    mu: float = .2
    mub: float = .02
    rb: float = .00025
    ka: float = 2.5e-5
    ca: float = 1.e-6
    bias: float = 0.
    mismatch: float = 0.
    gap_error: float = 0.
    mass: float = .02
    rotor: float = .005

    def inertia(self):
        # Spherical ball .1 g, isotropic inertia; carrier 2 g, holder J=1e-8.
        ib = .4*.0001*self.r**2
        return np.array([self.mass, self.rotor, 1e-8+ib+.0001*self.e**2,
                         .002, .002, ib/self.r**2, ib/self.r**2])

    def geometry(self, q):
        # q=[z,R*theta,alpha,qrad1,qrad2,r*phi1,r*phi2].
        # Both spheres rotate around radial swivel axes; first is bolted to ground.
        rows, gaps, centers = [], [], []
        for i, sig in enumerate((1., -1.)):
            a = A+self.bias if i == 0 else q[2]
            c, s = math.cos(a), math.sin(a)
            C = np.array([sig*(self.R+self.r+q[3+i]), sig*self.e*c, self.e*s])
            rho = math.hypot(C[0], C[1]); n = np.array([C[0]/rho,C[1]/rho,0.])
            tangent = np.array([-n[1],n[0],0.]); vertical = np.array([0.,0.,1.])
            axis = np.array([0.,-sig*s,c]); swivel = np.array([sig,0.,0.])
            # Relative roller-surface minus shaft-surface velocity.
            J = np.zeros((3,7)); J[:,0] = -vertical; J[:,1] = -tangent
            J[:,3+i] = np.array([sig,0.,0.])
            J[:,5+i] = np.cross(axis,-n)
            if i == 1:
                J[:,2] = np.array([0.,-sig*self.e*s,self.e*c])+np.cross(swivel,-self.r*n)
            rows.append(np.array([n@J, tangent@J, vertical@J]))
            gaps.append(rho-self.R-self.r); centers.append(C)
        return np.array(rows), np.array(gaps), np.array(centers)

    def radial_equilibrium(self, alpha):
        q = np.zeros(7); q[2] = alpha
        for i,a in enumerate((A+self.bias,alpha)):
            rho = self.R+self.r-self.preload/self.kc
            q[3+i] = math.sqrt(rho*rho-(self.e*math.cos(a))**2)-self.R-self.r
        return q

    def setup(self, speed, parked=False):
        alpha = (-A if parked else A)+self.bias+self.mismatch
        q = self.radial_equilibrium(alpha)
        B,g,_ = self.geometry(q)
        rest = q.copy()
        for i in range(2):
            rest[3+i] -= self.preload*B[i,0,3+i]/self.kp
            rest[3+i] += self.gap_error
        rest[2] = -A+self.bias
        v = np.zeros(7)
        if speed:
            v[0] = speed
            # Fixed roller's zero-slip velocity determines shaft and first spin.
            ix=[1,5]
            v[ix] = np.linalg.solve(B[0,1:,ix].T,-B[0,1:,0]*speed)
            v[6] = -np.dot(B[1,1:,6], B[1,1:]@v)/np.dot(B[1,1:,6],B[1,1:,6])
        return q,v,rest


def energy(m,q,v,rest,F):
    _,g,_=m.geometry(q)
    return (float(.5*np.dot(m.inertia()*v,v))+F*q[0]
            +.5*m.ka*(q[2]-rest[2])**2
            +.5*m.kp*np.sum(np.maximum(q[3:5]-rest[3:5],0)**2)
            +.5*m.kc*np.sum(np.minimum(g,0)**2))


def disc_minimum(H, eigen, U, b, cap):
    if cap <= 0: return np.zeros(2)
    beta=U.T@b
    free=-beta/eigen
    if np.linalg.norm(free)<=cap: return U@free
    # Exact metric projection, scalar KKT multiplier for the friction disc.
    lo=0.; hi=np.linalg.norm(beta)/cap
    for _ in range(28):
        lam=(lo+hi)/2
        if np.sum((beta/(eigen+lam))**2)>cap*cap: lo=lam
        else: hi=lam
    return U@(-beta/(eigen+hi))


def step(m,q,v,rest,F,h,tol=1e-9):
    mass=m.inertia(); K=np.array([0.,0.,m.ka,m.kp,m.kp,0.,0.])
    # Compression-only preload springs; a misplaced seat cannot pull a roller.
    K[3:5]*=(q[3:5]>rest[3:5])
    damp=np.array([0.,0.,m.ca,0.,0.,0.,0.])
    W=1/(mass+h*damp+h*h*K)
    ext=-K*(q-rest); ext[0]-=F
    vel=W*(mass*v+h*ext)
    B,g,_=m.geometry(q)
    # Normal compliance and Coulomb discs, plus returned swivel thrust friction.
    P=np.zeros((2,3)); pb=0.; residual=1.
    normal_den=np.sum(B[:,0,:]**2*W,axis=1)+1/(h*h*m.kc)
    Hs=[(b[1:]*W)@b[1:].T for b in B]
    eig=[np.linalg.eigh(H) for H in Hs]
    for iteration in range(4000):
        old=vel.copy()
        for i in range(2):
            bn=B[i,0]
            pn=max(0.,P[i,0]-(bn@vel+g[i]/h+P[i,0]/(h*h*m.kc))/normal_den[i])
            vel+=W*bn*(pn-P[i,0]); P[i,0]=pn
            pt=disc_minimum(Hs[i],*eig[i],B[i,1:]@vel-Hs[i]@P[i,1:],m.mu*pn)
            vel+=W*(B[i,1:].T@(pt-P[i,1:])); P[i,1:]=pt
        # Thrust load comes from the actual grounded preload spring, not a brake.
        thrust=m.kp*max(q[4]+h*vel[4]-rest[4],0.)
        cap=h*m.mub*m.rb*thrust
        newpb=float(np.clip(pb-vel[2]/W[2],-cap,cap))
        vel[2]+=W[2]*(newpb-pb); pb=newpb
        residual=float(np.max(np.abs(vel-old)*np.sqrt(mass)))
        if residual<tol: break
    heat=h*m.ca*vel[2]**2 - np.sum(P[:,1:]*(B[:,1:,:]@vel)) - pb*vel[2]
    return q+h*vel,vel,P,float(heat),residual,iteration+1


def run(m,F,speed,h=.0002,duration=.15,parked=False):
    q,v,rest=m.setup(speed,parked); E0=energy(m,q,v,rest,F)
    unconverged=0
    heat=0.; maxrise=0.; mindrop=0.; maxN=0.; minN=1e9; separated=0
    maxres=0.; maxit=0; peakv=0.; end='time'; angle_min=q[2]
    for j in range(round(duration/h)):
        q,v,P,dheat,res,it=step(m,q,v,rest,F,h)
        unconverged+=int(res>=1e-9)
        heat+=dheat; maxres=max(maxres,res); maxit=max(maxit,it)
        maxrise=max(maxrise,q[0]); mindrop=min(mindrop,q[0]); angle_min=min(angle_min,q[2])
        maxN=max(maxN,float(P[:,0].max()/h)); minN=min(minN,float(P[:,0].min()/h))
        separated+=int(np.all(P[:,0]<1e-12)); peakv=max(peakv,float(np.max(np.linalg.norm(m.geometry(q)[0][:,1:]@v,axis=1))))
        if abs(q[0])>=.02: end='40mm_midstroke_boundary'; break
    return dict(F=F,speed=speed,t=(j+1)*h,end=end,z_mm=q[0]*1e3,
                excursion_mm=[mindrop*1e3,maxrise*1e3],alpha_deg=math.degrees(q[2]),
                min_alpha_deg=math.degrees(angle_min),v_z=v[0],v_s=v[1],
                alpha_rate=v[2],normal_N=[minN,maxN],both_separated_steps=separated,
                peak_slip_m_s=peakv,kinetic_mJ=.5*float(np.dot(m.inertia()*v,v))*1e3,
                energy_numerical_loss_mJ=(E0-energy(m,q,v,rest,F)-heat)*1e3,
                heat_mJ=heat*1e3,solver_residual=maxres,solver_iterations=maxit,unconverged_steps=unconverged,numerically_resolved=(unconverged==0))


def geometry_checks():
    m=Model(); maxerr=0.; contact_error=0.
    for a in np.linspace(-A,A,21):
        q=m.radial_equilibrium(a); B,g,C=m.geometry(q)
        assert np.max(np.abs(g+m.preload/m.kc))<1e-15
        for k in (2,3,4):
            dq=np.zeros(7); dq[k]=1e-8
            fd=(m.geometry(q+dq)[1]-m.geometry(q-dq)[1])/2e-8
            maxerr=max(maxerr,float(np.max(np.abs(fd-B[:,0,k]))))
        for i in range(2):
            n=C[i].copy(); n[2]=0; n/=np.linalg.norm(n)
            shaft_point=m.R*n+np.array([0,0,C[i,2]])
            roller_point=C[i]-m.r*n
            contact_error=max(contact_error,float(np.linalg.norm(roller_point-shaft_point-g[i]*n)))
    assert maxerr<1e-8 and contact_error<1e-15
    # Material point finite difference: rotate the old contact radius about the
    # swivel axis, rather than differentiate a moving geometric witness point.
    q=m.radial_equilibrium(.13); B,_,C=m.geometry(q)
    n=C[1].copy(); n[2]=0; n/=np.linalg.norm(n)
    eps=1e-6; base=-m.r*n; axis=np.array([-1.,0.,0.])
    material=[]
    for sign in (-1,1):
        qp=q.copy(); qp[2]+=sign*eps
        cp=m.geometry(qp)[2][1]
        t=sign*eps
        rot=base*math.cos(t)+np.cross(axis,base)*math.sin(t)+axis*(axis@base)*(1-math.cos(t))
        material.append(cp+rot)
    fd=(material[1]-material[0])/(2*eps)
    tangent=np.array([-n[1],n[0],0.]); frame=np.array([n,tangent,[0,0,1.]])
    material_error=float(np.max(np.abs(frame@fd-B[1,:,2])))
    assert material_error<1e-11
    # Exact centered ideal rows and signed matched rolling velocities.
    m=Model(e=0)
    for speed in (-.1,.1):
        q,v,_=m.setup(speed); B,_,_=m.geometry(q)
        assert np.max(np.abs(B@v))<1e-12
        assert abs(v[1]-speed/math.tan(A))<1e-12
    # Direct power identity from generalized contact Jacobian (also checks units).
    q=m.radial_equilibrium(-A); B,_,_=m.geometry(q)
    v=np.array([.1,.2,.3,.004,.005,.6,.7]); forces=np.arange(6).reshape(2,3)
    assert abs(np.sum(forces*(B@v))-v@np.einsum('ijk,ij->k',B,forces))<1e-14
    return dict(gap_jacobian_error=maxerr,contact_witness_error_m=contact_error,material_velocity_error=material_error)


def static(m,F,angle=-A):
    q=m.radial_equilibrium(angle+m.bias); B,g,_=m.geometry(q)
    # Four tangential forces balance shaft z/s and both free roller spins;
    # four unknowns, four equations. Normal forces separately preload holders.
    Bt=B[:,1:,:].reshape(4,7)
    rhs=np.array([F,0.,0.,0.])
    lam=np.linalg.solve(Bt[:,[0,1,5,6]].T,rhs)
    qalpha=float(Bt[:,2]@lam + m.preload*B[1,0,2])
    spin=B[1,1:,6]; lateral=np.array([-spin[1],spin[0]])/np.linalg.norm(spin)
    if lateral[1]<0: lateral=-lateral
    coefficient=float(lateral@B[1,1:,2])
    return dict(contact_motion_mm_per_rad=coefficient*1e3,normal_motion_mm_per_rad=B[1,0,2]*1e3,
                tangent_N=lam.reshape(2,2).tolist(),swivel_contact_mNm=qalpha*1e3,
                friction_utilization=max(np.linalg.norm(lam.reshape(2,2),axis=1))/(m.mu*m.preload),
                thrust_stiction_mNm=m.mub*m.rb*m.preload*1e3,
                release_spring_mNm=m.ka*2*A*1e3)


def static_envelope(m,F):
    _,_,rest=m.setup(0)
    feasible=[]; traction_angles=[]; min_return=1e9
    for degrees in np.linspace(-80,19.9,1000):
        q=m.radial_equilibrium(math.radians(degrees))
        def forces(q):
            B,g,_=m.geometry(q); N=-m.kc*g
            Bt=B[:,1:,:].reshape(4,7)
            tang=np.linalg.solve(Bt[:,[0,1,5,6]].T,[F,0,0,0])
            generalized=np.einsum('ij,i->j',B[:,0,:],N)+Bt.T@tang
            generalized[3:5]-=m.kp*(q[3:5]-rest[3:5])
            generalized[2]+=m.ka*(rest[2]-q[2])
            return generalized,N,tang
        for _ in range(8):
            f=forces(q)[0][3:5]
            if np.max(np.abs(f))<1e-8:break
            jac=np.zeros((2,2))
            for i in range(2):
                qp=q.copy(); qp[3+i]+=1e-8
                jac[:,i]=(forces(qp)[0][3:5]-f)/1e-8
            q[3:5]-=np.linalg.solve(jac,f)
        force,N,tang=forces(q)
        assert np.max(np.abs(force[3:5]))<1e-7
        traction=(np.linalg.norm(tang.reshape(2,2),axis=1)<=m.mu*N).all() and min(N)>0
        cap=m.mub*m.rb*abs(m.kp*(q[4]-rest[4]))
        if traction:
            traction_angles.append(degrees)
            min_return=min(min_return,abs(force[2])-cap)
            if abs(force[2])<=cap:feasible.append(degrees)
    return dict(traction_interval_deg=[min(traction_angles),max(traction_angles)] if traction_angles else [],
                static_interval_deg=[min(feasible),max(feasible)] if feasible else [],
                minimum_swivel_excess_mNm=min_return*1e3 if traction_angles else None,
                angle_grid_deg=.1)


def controls():
    m=Model(); _,v,_=m.setup(1.)
    meff=float(np.dot(m.inertia()*v,v))
    delay=math.sqrt(2*.0004*.002/30)
    jaw={}
    for name,mass in [('output_only',.02),('same_reflected_mass',meff)]:
        speed=.1+10/mass*delay
        jaw[name]=dict(zero_delay_mm=1e3*.5*mass*.1**2/(12-10),
                       delayed_mm=1e3*(.1*delay+.5*10/mass*delay**2+.5*mass*speed**2/(12-10)))
    return dict(aligned_reflected_mass_kg=meff,weak_30ms_1N_mm=1e3*(-.1*.03-.5*.03**2/meff),
                jaw_delay_ms=delay*1e3,jaw=jaw)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--suite',choices=['quick','nominal','bounds','convergence'],default='quick'); args=ap.parse_args()
    out={'checks':geometry_checks(),'controls':controls(),'static_envelope':{name:static_envelope(m,10) for name,m in [('weak',Model()),('strong_negative_offset',Model(e=-.0002,ka=.003,ca=1e-5)),('strong_nominal',Model(ka=.003,ca=1e-5))]},'static':{str(e):static(Model(e=e),10.) for e in (-.0002,-.00005,0,.00005,.0002)}}
    if args.suite=='quick':
        out['runs']=[run(Model(),F,-.1) for F in (0,.02,1,10)]
    elif args.suite=='nominal':
        out['runs']={name:[run(m,F,v) for F in (0,.02,1,10) for v in (-.1,0,.1)] for name,m in
                     [('plain',Model()),('strong_return',Model(ka=.003,ca=1e-5))]}
        out['neighbor']=[run(Model(),F,0,parked=True) for F in (0,.02,1,10)]
    elif args.suite=='bounds':
        cases=[('centered',Model(e=0)),('eccentric_200um',Model(e=.0002)),('reverse_eccentric',Model(e=-.0002)),
               ('low_thrust_friction',Model(mub=.002)),('high_thrust_friction',Model(mub=.1)),
               ('coherent_loose',Model(preload=24,mu=.1,bias=math.radians(2),gap_error=.0001)),
               ('coherent_tight',Model(preload=36,mu=.4,bias=math.radians(-2),gap_error=-.0001)),
               ('local_mismatch',Model(mismatch=math.radians(1))),
               ('preload_lost',Model(gap_error=.004)),
               ('strong_loose',Model(ka=.003,ca=1e-5,preload=24,mu=.1,bias=math.radians(2),gap_error=.0001)),
               ('strong_reverse_eccentric',Model(ka=.003,ca=1e-5,e=-.0002)),
               ('strong_heavy',Model(ka=.003,ca=1e-5,mass=1.1,rotor=.05)),
               ('strong_soft_contact',Model(ka=.003,ca=1e-5,kc=5e5)),
               ('strong_stiff_contact',Model(ka=.003,ca=1e-5,kc=2e6))]
        out['runs']={name:[run(m,F,-.1) for F in (0,10)] for name,m in cases}
    else:
        out['runs']={name:[dict(h=h,**run(m,F,-.1,h=h,duration=.03)) for h in (.0004,.0002,.0001,.00005)]
                     for name,m,F in [('plain',Model(),1),('strong',Model(ka=.003,ca=1e-5),1),('strong_10N',Model(ka=.003,ca=1e-5),10)]}
    if args.suite=='convergence':
        meff=out['controls']['aligned_reflected_mass_kg']
        for result in out['runs']['plain']:
            t=result['t']; h=result['h']
            exact_discrete=1e3*(-.1*t-(t*t+h*t)/(2*meff))
            assert abs(result['z_mm']-exact_discrete)<1e-5
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
