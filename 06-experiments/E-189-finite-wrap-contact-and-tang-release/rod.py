"""Geometrically exact constant-strain planar rod with nodal mandrel contact.

Exact element arcs are checked for mandrel penetration between contact nodes.
Units N, mm. A planar developed helix approximation: axial pitch/torsion, wire
section contact compliance and interturn interaction are explicitly omitted.
Requires numpy and scipy. Fully sliding contact, NOT arbitrary static friction.
"""
import json
import math
import numpy as np
from scipy.linalg import solve_banded


def newton_banded(fun,z):
    """Exact complex-step local Jacobian; coloring exploits adjacent-node support."""
    z=z.copy()
    n=len(z)
    calls=0
    for iteration in range(100):
        f=fun(z);calls+=1
        if max(abs(f))<1e-7:return z,calls
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
            if np.linalg.norm(ft)<merit or max(abs(ft))<1e-7:
                z=trial
                break
            scale/=2
        else:raise RuntimeError(('Newton line search',float(max(abs(f)))))
    raise RuntimeError(('Newton iteration limit',float(max(abs(fun(z)))),float(max(abs(z)))))


class Coil:
    def __init__(self,n=60,interference=.05,hub=3.,diameter=.3,
                 young=200000.,mu=.1,slip=1.,end_clearance=.05,anchor="start",clamped=True):
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
        self.last=None

    def energy_gradient(self,x):
        # Exact constant-strain arc elements avoid displacement/shear locking.
        p=x.reshape(-1,3)
        angle=np.linspace(0,6*math.pi,self.n+1)+p[:,1]/self.r
        radius=self.r+p[:,0]
        er=np.stack([np.cos(angle),np.sin(angle)],axis=1)
        et=np.stack([-np.sin(angle),np.cos(angle)],axis=1)
        position=radius[:,None]*er
        psi=angle+p[:,2]/self.r
        dpsi=psi[1:]-psi[:-1]
        mid=(psi[1:]+psi[:-1])/2
        tangent=np.stack([-np.sin(mid),np.cos(mid)],axis=1)
        normal=np.stack([np.cos(mid),np.sin(mid)],axis=1)
        chord=position[1:]-position[:-1]
        # sinc and its logarithmic derivative, including straight-element limit.
        small=np.abs(dpsi)<1e-4
        sinc=np.empty_like(dpsi);ld=np.empty_like(dpsi)
        z=dpsi[small]
        sinc[small]=1-z*z/24+z**4/1920
        ld[small]=-z/12-z**3/720-z**5/30240
        z=dpsi[~small]
        sinc[~small]=np.sin(z/2)/(z/2)
        ld[~small]=.5/np.tan(z/2)-1/z
        length=self.h*sinc
        axial=np.sum(chord*tangent,axis=1)/length
        shear=np.sum(chord*normal,axis=1)/length
        eps=axial-1
        curvature=dpsi/self.h-1/self.r
        energy=self.h/2*np.sum(self.ea*eps**2+self.ga*shear**2+self.ei*curvature**2)
        force=(self.h*self.ea*eps/length)[:,None]*tangent+(self.h*self.ga*shear/length)[:,None]*normal
        gm=self.h*(-self.ea*eps*shear+self.ga*shear*axial)
        gd=-self.h*(self.ea*eps*axial+self.ga*shear**2)*ld+self.ei*curvature
        left=gm/2-gd;right=gm/2+gd
        g=np.zeros_like(p)
        g[:-1,0]-=np.sum(force*er[:-1],axis=1)
        g[1:,0]+=np.sum(force*er[1:],axis=1)
        g[:-1,1]+=(-np.sum(force*et[:-1],axis=1)*radius[:-1]+left)/self.r
        g[1:,1]+=(np.sum(force*et[1:],axis=1)*radius[1:]+right)/self.r
        g[:-1,2]+=left/self.r
        g[1:,2]+=right/self.r
        return energy,g.ravel(),dict(strain=eps,shear=shear,curvature=curvature)

    def geometry(self,x):
        p=x.reshape(-1,3)
        angle=np.linspace(0,6*math.pi,self.n+1)+p[:,1]/self.r
        radius=self.r+p[:,0]
        positions=np.stack([radius*np.cos(angle),radius*np.sin(angle)],axis=1)
        psi=angle+p[:,2]/self.r
        fields=self.energy_gradient(x)[2]
        minimum=float(min(radius))
        closure=0.
        for j in range(self.n):
            k=fields['curvature'][j]+1/self.r
            stretch=fields['strain'][j]+1
            shear=fields['shear'][j]
            # All tested elements retain positive curvature; a straight limit
            # is covered by the element energy tests, not this arc check.
            if abs(k)<1e-10:raise RuntimeError('straight arc geometry needs explicit segment check')
            v0=np.array([stretch*math.cos(psi[j])+shear*math.sin(psi[j]),
                         stretch*math.sin(psi[j])-shear*math.cos(psi[j])])/k
            center=positions[j]-v0
            v1=np.array([stretch*math.cos(psi[j+1])+shear*math.sin(psi[j+1]),
                         stretch*math.sin(psi[j+1])-shear*math.cos(psi[j+1])])/k
            closure=max(closure,float(np.linalg.norm(center+v1-positions[j+1])))
            arc_radius=float(np.linalg.norm(v0))
            start=math.atan2(v0[1],v0[0]);finish=start+psi[j+1]-psi[j]
            target=math.atan2(-center[1],-center[0])
            lo,hi=sorted([start,finish])
            m=math.ceil((lo-target)/(2*math.pi))
            if target+2*math.pi*m<=hi:
                minimum=min(minimum,abs(float(np.linalg.norm(center))-arc_radius))
        assert closure<1e-9
        return dict(min_arc_gap_mm=minimum-(self.hub+self.d/2),arc_closure_mm=closure,
                    min_angular_increment_rad=float(min(np.diff(angle))))

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
        for iteration in range(4*self.n):
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
            if err>2e-7: raise RuntimeError(('nonlinear residual',float(err)))
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
            geometry=self.geometry(x)
            self.last=(x.copy(),set(active))
            return dict(x=x,reaction=reaction,normal=normal,
                        torque_Nmm=float(torque),
                        contact_nodes=len(active),min_gap_mm=float(min(x[3:-3:3]-self.i)),
                        energy_mJ=float(energy),max_strain=float(max(abs(fields['strain']))),
                        max_shear=float(max(abs(fields['shear']))),
                        max_bending_MPa=float(self.young*self.d/2*max(abs(fields['curvature']))),
                        max_director_rad=float(max(abs(x[2::3]/self.r))),
                        balance_Nmm=balance,residual_N=float(err),root_calls=calls,**geometry)
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
    previous=0.
    for opening in openings:
        # Follow the commanded branch; large unconstrained Newton jumps can land
        # on unrelated wrapped configurations. These are quasistatic load steps.
        steps=max(1,math.ceil(abs(opening-previous)/.1))
        for intermediate in np.linspace(previous,opening,steps+1)[1:]:
            result=coil.solve(start+direction*intermediate)
        previous=opening
        states.append(dict(opening_mm=float(opening),
                           generalized_force_N=float(direction*result['reaction'][3*coil.command+1]),
                           tang_arc_mm=float(opening*(coil.r+coil.ends[0])/coil.r),
                           tang_force_N=float(direction*result['reaction'][3*coil.command+1]*coil.r/(coil.r+coil.ends[0])),**clean(result)))
    return dict(n=n,interference_mm=interference,mu=mu,slip=slip,
                start_end_mm=start,states=states)


if __name__=='__main__':
    print(json.dumps(sweep(),indent=2))
