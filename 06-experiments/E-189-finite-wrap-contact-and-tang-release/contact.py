"""Finite curved-beam sliding-contact screen; N, mm, radians internally.

Requires numpy. This is a small-displacement planar beam approximation with
guided radial endpoints, not a qualified helical wrap spring or static-friction
release model. Contact nodes obey a unilateral rigid mandrel and fully mobilized
Coulomb friction. No guessed contact-pressure distribution or capstan gain.
"""
import json
import math
import numpy as np


class Coil:
    def __init__(self, n=90, interference=.05, hub=3., diameter=.3,
                 young=200000., mu=.1, slip=1., end_clearance=.05):
        self.n, self.i, self.hub, self.mu, self.slip = n, interference, hub, mu, slip
        self.r = hub + diameter/2 - interference
        self.h = self.r * 6*math.pi/n
        self.d = diameter
        area, second = math.pi*diameter**2/4, math.pi*diameter**4/64
        self.ea, self.ei = young*area, young*second
        self.ga = young/(2*1.3)*area*6/7
        # DOFs per node: outward displacement w, tangent v, R*section rotation b.
        self.k = np.zeros((3*(n+1), 3*(n+1)))
        h, r = self.h, self.r
        self.rows = [np.array([1/(2*r), -1/h, 0, 1/(2*r), 1/h, 0]),
                     np.array([-1/h, -1/(2*r), 1/(2*r), 1/h, -1/(2*r), 1/(2*r)]),
                     np.array([0, 0, -1/(h*r), 0, 0, 1/(h*r)])]
        ke = sum(h*stiff*np.outer(b,b) for stiff,b in
                 zip([self.ea,self.ga,self.ei],self.rows))
        for j in range(n):
            self.k[3*j:3*j+6,3*j:3*j+6] += ke
        self.ends = {0: interference+end_clearance,
                     3*n: interference+end_clearance, 1: 0., 2: 0.}
        self.contacts = np.arange(1,n)
        self.radial = 3*self.contacts
        self.tangent = self.radial+1
        self.cache = {}

    def solve(self, opening_end=None):
        fixed = dict(self.ends)
        if opening_end is not None:
            fixed[3*self.n+1] = opening_end
        prescribed = np.array(sorted(fixed))
        free = np.array([j for j in range(len(self.k)) if j not in fixed])
        key = opening_end is not None
        if key not in self.cache:
            inv = np.linalg.inv(self.k[np.ix_(free,free)])
            force = np.zeros((len(self.k),len(self.contacts)))
            force[self.radial,np.arange(len(self.contacts))] = 1.
            force[self.tangent,np.arange(len(self.contacts))] = self.slip*self.mu
            response = np.zeros_like(force)
            response[free] = inv@force[free]
            self.cache[key] = inv,force,response
        inv,force,response = self.cache[key]
        x = np.zeros(len(self.k))
        x[prescribed] = [fixed[j] for j in prescribed]
        x[free] = inv@(-self.k[np.ix_(free,prescribed)]@x[prescribed])
        base = x.copy()
        compliance = response[self.radial]
        active = set(np.flatnonzero(x[self.radial] < self.i))
        visited = set()
        for iteration in range(500):
            state = tuple(sorted(active))
            if state in visited:
                raise RuntimeError('contact active set cycle; no accepted solution')
            visited.add(state)
            a = np.array(state,dtype=int)
            normal = np.zeros(len(self.contacts))
            if len(a):
                normal[a] = np.linalg.solve(compliance[np.ix_(a,a)],
                                            self.i-base[self.radial[a]])
            x = base+response@normal
            gap = x[self.radial]-self.i
            negative = [j for j in a if normal[j]<-1e-8]
            if negative:
                active.remove(min(negative,key=lambda j:normal[j]))
                continue
            missing = [j for j in range(len(normal)) if j not in active and gap[j]<-1e-9]
            if missing:
                active.add(min(missing,key=lambda j:gap[j]))
                continue
            residual = self.k@x-force@normal
            assert np.max(np.abs(residual[free]))<2e-7, (np.max(np.abs(residual[free])), np.max(abs(x)), np.max(normal))
            assert np.min(normal)>-1e-8 and np.min(gap)>-1e-8
            assert np.max(np.abs(normal*gap))<1e-7
            # Reconstruct material centerline, with a declared .4-mm axial pitch.
            # This polar reconstruction exposes the linear model's omitted strain.
            theta = np.linspace(0,6*math.pi,self.n+1)
            w,v,b = x.reshape(-1,3).T
            angle = theta+v/self.r
            radius = self.r+w
            strains, rotation = [], []
            for j in range(self.n):
                dofs=x[3*j:3*j+6]
                eps, shear, curvature = [float(row@dofs) for row in self.rows]
                # Exact length of reconstructed polar interpolant at midpoint.
                rp=(w[j+1]-w[j])/self.h
                ap=1/self.r+(v[j+1]-v[j])/(self.h*self.r)
                exact=math.hypot(rp,(radius[j]+radius[j+1])/2*ap)-1
                strains.append(abs(exact-eps))
                rotation.append(abs((b[j]+b[j+1])/(2*self.r)))
            return dict(x=x,normal=normal,reaction=residual,
                        torque_Nmm=float(self.slip*self.mu*self.hub*sum(normal)),
                        contact_nodes=len(a),min_gap_mm=float(min(gap)),
                        energy_mJ=float(x@self.k@x/2),
                        max_rotation_rad=max(rotation),
                        max_strain_discrepancy=max(strains),
                        radial_error_ratio=float(max(abs(w))/self.r),
                        max_free_residual_N=float(max(abs(residual[free]))),
                        active_iterations=iteration+1)
        raise RuntimeError('active set limit')


def sweep(n=90, interference=.05, mu=.1, slip=1):
    coil=Coil(n=n,interference=interference,mu=mu,slip=slip)
    initial=coil.solve()
    start=float(initial['x'][3*n+1])
    states=[]
    for opening in np.linspace(0,2.5,26):
        result=coil.solve(start-opening)
        states.append(dict(opening_mm=float(opening),
                           tang_force_N=float(-result['reaction'][3*n+1]),
                           **{k:v for k,v in result.items() if k not in ['x','normal','reaction']}))
    return dict(n=n,interference_mm=interference,mu=mu,slip=slip,
                start_end_mm=start,states=states)


if __name__=='__main__':
    print(json.dumps(sweep(),indent=2))
