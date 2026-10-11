"""Geometrically exact planar Cosserat rod with nodal mandrel contact.

Midpoint elements in polar coordinates preserve nonpenetration between nodes.
Units N, mm. A planar developed helix approximation: axial pitch/torsion, wire
section contact compliance and interturn interaction are explicitly omitted.
Requires numpy and scipy. Fully sliding contact, NOT arbitrary static friction.
"""
import json
import math
import numpy as np
from scipy.optimize import root
from scipy.linalg import solve_banded


def newton_banded(fun,z):
    """Exact complex-step local Jacobian; coloring exploits adjacent-node support."""
    z=z.copy()
    n=len(z)
    calls=0
    for iteration in range(100):
        f=fun(z);calls+=1
        if max(abs(f))<5e-8:return z,calls
        derivatives=[]
        for color in range(11):
            dz=np.zeros(n,dtype=complex);dz[color::11]=1e-25j
            derivatives.append(np.imag(fun(z+dz))/1e-25)
        calls+=11
        ab=np.zeros((11,n))
        for j in range(n):
            rows=np.arange(max(0,j-5),min(n,j+6))
            ab[5+rows-j,j]=derivatives[j%11][rows]
        dz=solve_banded((5,5),ab,-f)
        scale=min(1.,1./max(abs(dz)))
        merit=np.linalg.norm(f)
        for backtrack in range(25):
            trial=z+scale*dz
            ft=fun(trial);calls+=1
            if np.linalg.norm(ft)<merit or max(abs(ft))<5e-8:
                z=trial
                break
            scale/=2
        else:raise RuntimeError(('Newton line search',float(max(abs(f)))))
    raise RuntimeError('Newton iteration limit')


class Coil:
    def __init__(self,n=60,interference=.05,hub=3.,diameter=.3,
                 young=200000.,mu=.1,slip=1.,end_clearance=.05,anchor="start",clamped=True,quadrature=3):
        self.n,self.i,self.hub,self.mu,self.slip=n,interference,hub,mu,slip
        self.r=hub+diameter/2-interference
        self.h=self.r*6*math.pi/n
        self.d,self.young=diameter,young
        area,second=math.pi*diameter**2/4,math.pi*diameter**4/64
        self.ea,self.ei=young*area,young*second
        self.ga=young/(2*1.3)*area*6/7
        # Each node: radius increment w, R*angle increment a, R*director beta.
        # Tight tang clamped to local tangent, both endpoints radially guided.
        self.anchor=0 if anchor=="start" else n
        self.command=n if anchor=="start" else 0
        self.ends={0:interference+end_clearance,3*n:interference+end_clearance,3*self.anchor+1:0.}
        if clamped: self.ends[3*self.anchor+2]=0.
        self.quadrature=quadrature
        self.qpoints,self.qweights=np.polynomial.legendre.leggauss(quadrature)
        self.last=None

    def energy_gradient(self,x):
        p=x.reshape(-1,3)
        delta=(p[1:]-p[:-1])/self.h
        wp,ap,bp=delta.T
        gradient=np.zeros_like(p)
        energy=0.
        samples={k:[] for k in ['strain','shear','curvature']}
        points,weights=self.qpoints,self.qweights
        for z,weight in zip(points/2,weights/2):
            w,a,b=((.5-z)*p[:-1]+(.5+z)*p[1:]).T
            rho=1+w/self.r
            c,s=np.cos(b/self.r),np.sin(b/self.r)
            t=rho*(1+ap)
            eps=t*c-wp*s-1
            shear=wp*c+t*s
            curvature=(ap+bp)/self.r
            en,sh,mo=self.ea*eps,self.ga*shear,self.ei*curvature
            energy+=weight*self.h/2*np.sum(en*eps+sh*shear+mo*curvature)
            dm=np.zeros_like(delta)
            dd=np.zeros_like(delta)
            dm[:,0]=(en*c+sh*s)*(1+ap)/self.r
            dm[:,2]=(-en*shear+sh*(eps+1))/self.r
            dd[:,0]=-en*s+sh*c
            dd[:,1]=(en*c+sh*s)*rho+mo/self.r
            dd[:,2]=mo/self.r
            gradient[:-1]+=weight*(self.h*(.5-z)*dm-dd)
            gradient[1:]+=weight*(self.h*(.5+z)*dm+dd)
            for key,value in zip(samples,[eps,shear,curvature]):samples[key].append(value)
        return energy,gradient.ravel(),{k:np.concatenate(v) for k,v in samples.items()}

    def quadrature_holdout(self,x):
        """Five-point integration of the SAME interpolant, not a new solution."""
        p=x.reshape(-1,3)
        delta=(p[1:]-p[:-1])/self.h
        wp,ap,bp=delta.T
        energy=0.
        points,weights=np.polynomial.legendre.leggauss(5)
        for z,weight in zip(points/2,weights/2):
            w,a,b=((.5-z)*p[:-1]+(.5+z)*p[1:]).T
            c,s=np.cos(b/self.r),np.sin(b/self.r)
            t=(1+w/self.r)*(1+ap)
            eps=t*c-wp*s-1
            shear=wp*c+t*s
            curvature=(ap+bp)/self.r
            energy+=weight*self.h/2*np.sum(self.ea*eps**2+self.ga*shear**2+self.ei*curvature**2)
        return float(energy)

    def solve(self,opening_end=None):
        fixed=dict(self.ends)
        if opening_end is not None: fixed[3*self.command+1]=opening_end
        prescribed=set(fixed)
        if self.last is None:
            x=np.zeros(3*(self.n+1))
            x[0::3]=max(0,self.i)
            x[1::3]=np.linspace(0,-6*math.pi*self.i*self.r/(self.r+self.i),self.n+1)
            x[1::3]-=x[3*self.anchor+1]
            active=set(range(1,self.n)) if self.i>0 else set()
        else:
            x,active=self.last[0].copy(),set(self.last[1])
        visited=set()
        calls=0
        for iteration in range(200):
            state=tuple(sorted(active))
            if state in visited: raise RuntimeError('active set cycle')
            visited.add(state)
            held=dict(fixed)
            held.update({3*j:self.i for j in active})
            free=np.array([j for j in range(len(x)) if j not in held])
            for j,v in held.items(): x[j]=v
            radial=np.array([3*j for j in sorted(active)],dtype=int)
            def residual(z):
                y=x.astype(np.result_type(z.dtype,float))
                y[free]=z
                _,g,_=self.energy_gradient(y)
                normal=g[radial].copy()
                g[radial+1]-=self.slip*self.mu*normal*self.hub/self.r
                g[radial+2]+=self.slip*self.mu*normal*self.d/(2*self.r)
                return g[free]
            solution,ncalls=newton_banded(residual,x[free])
            calls+=ncalls
            x[free]=solution
            err=max(abs(residual(solution)))
            if err>2e-7:
                def jacobian(z):
                    return np.array([np.imag(residual(z+1e-25j*e))/1e-25 for e in np.eye(len(z))]).T
                sol=root(residual,solution,jac=jacobian,method='hybr',options={'xtol':1e-11,'maxfev':5000})
                calls+=sol.nfev
                x[free]=sol.x
                err=max(abs(residual(sol.x)))
            if err>2e-7: raise RuntimeError(('nonlinear residual',sol.message,err))
            energy,g,fields=self.energy_gradient(x)
            bad=[j for j in active if g[3*j]<-1e-7]
            if bad:
                active.remove(min(bad,key=lambda j:g[3*j]))
                continue
            missing=[j for j in range(1,self.n) if j not in active and x[3*j]<self.i-1e-8]
            if missing:
                active.add(min(missing,key=lambda j:x[3*j]))
                continue
            normal=np.zeros(self.n+1)
            if len(radial): normal[radial//3]=g[radial]
            reaction=g.copy()
            reaction[0::3]-=normal
            reaction[1::3]-=self.slip*self.mu*normal*self.hub/self.r
            reaction[2::3]+=self.slip*self.mu*normal*self.d/(2*self.r)
            freephysical=[j for j in range(len(x)) if j not in prescribed]
            assert max(abs(reaction[freephysical]))<2e-7
            assert min(normal)>-1e-7
            assert min(x[3:-3:3]-self.i)>-1e-8
            assert max(abs(normal[1:-1]*(x[3:-3:3]-self.i)))<1e-7
            # Independent global angular balance: a -> a+R*dphi, beta unchanged.
            # Include the circular section contact couple -(d/2)*friction.
            torque=self.slip*self.mu*self.hub*np.sum(normal)
            balance=float(self.r*np.sum(reaction[1::3])+torque)
            assert abs(balance)<2e-6
            self.last=(x.copy(),set(active))
            return dict(x=x,reaction=reaction,normal=normal,
                        torque_Nmm=float(torque),hub_torque_Nmm=float(self.slip*self.mu*self.hub*sum(normal)),
                        contact_nodes=len(active),min_gap_mm=float(min(x[3:-3:3]-self.i)),
                        energy_mJ=float(energy),max_strain=float(max(abs(fields['strain']))),
                        holdout_energy_mJ=self.quadrature_holdout(x),
                        max_shear=float(max(abs(fields['shear']))),
                        max_bending_MPa=float(self.young*self.d/2*max(abs(fields['curvature']))),
                        max_director_rad=float(max(abs(x[2::3]/self.r))),
                        balance_Nmm=balance,residual_N=float(err),root_calls=calls)
        raise RuntimeError('contact active set limit')


def clean(result):
    return {k:v for k,v in result.items() if k not in ['x','reaction','normal']}


def sweep(n=60,interference=.05,mu=.1,slip=1,openings=None,**kw):
    coil=Coil(n=n,interference=interference,mu=mu,slip=slip,**kw)
    first=coil.solve()
    start=float(first['x'][3*coil.command+1])
    direction=-1 if coil.command==n else 1
    states=[]
    if openings is None: openings=np.linspace(0,2.5,26)
    for opening in openings:
        result=coil.solve(start+direction*opening)
        states.append(dict(opening_mm=float(opening),
                           tang_force_N=float(direction*result['reaction'][3*coil.command+1]),**clean(result)))
    return dict(n=n,interference_mm=interference,mu=mu,slip=slip,
                start_end_mm=start,states=states)


if __name__=='__main__':
    print(json.dumps(sweep(),indent=2))
