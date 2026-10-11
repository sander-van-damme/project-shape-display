"""E-166: inextensible planar hook, frictionless rack edge, N/mm units.
Deterministic numerical branch evidence, not hardware validation. Python + numpy.
"""
import json
import math
import numpy as np


def tri(diag, off, rhs):
    d, b = diag.copy(), rhs.copy()
    for i in range(1, len(d)):
        if d[i-1] <= 0:
            raise ValueError('nonpositive pivot')
        q = off[i-1] / d[i-1]
        d[i] -= q * off[i-1]
        b[i] -= q * b[i-1]
    if d[-1] <= 0:
        raise ValueError('nonpositive pivot')
    x = b.copy()
    x[-1] /= d[-1]
    for i in range(len(d)-2, -1, -1):
        x[i] = (b[i]-off[i]*x[i+1])/d[i]
    return x


def evaluate(th, EI, L, F=0., r=.4, H=0.):
    n = len(th)
    ds = L/n
    w = np.ones(n); w[-1] = .5
    sn, cs = np.sin(th), np.cos(th)
    dy, dz = ds*w*cs, -ds*w*sn
    y = ds*np.dot(w, sn)
    z = ds*(.5+np.dot(w, cs))
    dt = np.diff(np.r_[0., th])
    k = EI/ds
    U = .5*k*np.dot(dt, dt) - H*y
    g = k*dt.copy(); g[:-1] -= k*dt[1:]
    diag = np.full(n, 2*k); diag[-1] = k
    off = np.full(n-1, -k)
    g -= H*dy; diag += H*ds*w*sn
    # The rack edge at fixed lateral coordinate r slides on the rigid hook.
    # z_contact=z-(r-y)*tan(th[-1]); downward dead load has potential -F*z_contact.
    T = math.tan(th[-1]); S = 1+T*T
    q = r-y
    U += F*(L-z+q*T)
    g += F*(-dz-dy*T); g[-1] += F*q*S
    diag += F*ds*w*(cs+sn*T)
    # Hessian consists of a tridiagonal part plus last-row/column coupling.
    col = np.zeros(n-1); col[-1] = off[-1]
    col -= F*dy[:-1]*S
    diag[-1] += F*(-2*dy[-1]*S+2*q*S*T)
    return U, g, diag, off, col, y, z


def equilibrium(EI, L, F=0., r=.4, H=0., n=64, initial=None):
    th = np.zeros(n) if initial is None else initial.copy()
    for iteration in range(50):
        U,g,d,o,b,y,z = evaluate(th,EI,L,F,r,H)
        try:
            ag = tri(d[:-1],o[:-1],g[:-1])
            ab = tri(d[:-1],o[:-1],b)
            schur = d[-1]-np.dot(b,ab)
            if schur <= 0:
                return None
            last = (g[-1]-np.dot(b,ag))/schur
            step = np.r_[ag-ab*last,last]
        except ValueError:
            return None
        if max(abs(g)) < 2e-9:
            return {'theta':th,'y':y,'z':z,'a':(r-y)/math.cos(th[-1]),
                    'tip_angle':th[-1], 'residual':float(max(abs(g)))}
        alpha = 1.
        while alpha > 1e-8:
            candidate = th-alpha*step
            if max(abs(candidate)) < .8:
                v = evaluate(candidate,EI,L,F,r,H)[0]
                if v <= U-1e-4*alpha*np.dot(g,step)+1e-13:
                    th = candidate; break
            alpha *= .5
        else:
            return None
    raise AssertionError('Newton did not converge')


def branch(EI=266.6666666667,L=12.,r=.4,e=1.,n=64,step=.005):
    old = None
    for i in range(1,10001):
        F = i*step*EI/L**2  # dimensionless load step
        a = equilibrium(EI,L,F,r,n=n,initial=None if old is None else old['theta'])
        if a is None or a['a'] >= e:
            return {'last_supported_F':(i-1)*step*EI/L**2,'next_F':F,
                    'event':'branch_not_found' if a is None else 'toe_runoff',
                    'last_a':None if old is None else old['a'],
                    'next_a':None if a is None else a['a'],
                    'last_angle':None if old is None else old['tip_angle']}
        old = a
    raise AssertionError('no event')


def release(EI=266.6666666667,L=12.,r=.4,e=1.,clearance=.1,n=64):
    lo,hi = 0., 10*EI/L**2
    for _ in range(60):
        H = -(lo+hi)/2
        a = equilibrium(EI,L,H=H,n=n)
        if a is None:
            hi = -H; continue
        toe = a['y']+e*math.cos(a['tip_angle'])
        if toe > r-clearance:lo=-H
        else:hi=-H
    a = equilibrium(EI,L,H=-hi,n=n)
    assert a is not None
    a['H']=-hi
    return a


def rectangle(y0,y1,z0,z1):
    return np.array([[y0,z0],[y1,z0],[y1,z1],[y0,z1]])


def bodies(a,L=12.,t=.2,e=1.):
    hook_t=t
    th=np.r_[0.,a['theta']]; ds=L/(len(th)-1)
    y=np.r_[0.,np.cumsum(ds*.5*(np.sin(th[:-1])+np.sin(th[1:])))]
    z=np.r_[0.,np.cumsum(ds*.5*(np.cos(th[:-1])+np.cos(th[1:])))]
    normal=np.c_[np.cos(th),-np.sin(th)]
    p=np.c_[y,z]
    left,right=p-t/2*normal,p+t/2*normal
    pieces=[np.array([left[i],right[i],right[i+1],left[i+1]]) for i in range(len(th)-1)]
    v=normal[-1]; down=np.array([math.sin(th[-1]),math.cos(th[-1])])
    pieces.append(np.array([p[-1],p[-1]+e*v,p[-1]+e*v+hook_t*down,p[-1]+hook_t*down]))
    return pieces


def overlap(a,b):
    for p in (a,b):
        edges=np.roll(p,-1,axis=0)-p
        for edge in edges:
            normal=np.array([-edge[1],edge[0]])
            if np.linalg.norm(normal)<1e-12:continue
            x,y=a@normal,b@normal
            if min(max(x),max(y))-max(min(x),min(y)) <= 1e-10:return False
    return True


def linear_runoff(EI=266.6666666667,L=12.,r=.4,e=1.):
    """Independent continuum small-angle beam-column/contact solution."""
    lo,hi=0.,2.
    for _ in range(80):
        v=(lo+hi)/2
        if math.cosh(v)-v*math.sinh(v)>r/e:lo=v
        else:hi=v
    return EI/L**2*v*v


def verify():
    # Energy derivatives reconstructed by central differences, not the force code.
    th=np.linspace(-.001,-.03,8)
    args=(266.6666667,12.,.5,.4,-.1)
    U,g,d,o,b,*_=evaluate(th,*args)
    M=np.diag(d)+np.diag(o,1)+np.diag(o,-1)
    M[:-1,-1]=b;M[-1,:-1]=b
    eps=1e-5; grad=[]; hess=[]
    for j in range(8):
        q=np.zeros(8);q[j]=eps
        ep=evaluate(th+q,*args);em=evaluate(th-q,*args)
        grad.append((ep[0]-em[0])/(2*eps))
        hess.append((ep[1]-em[1])/(2*eps))
    assert max(abs(g-np.array(grad)))<1e-7
    assert np.max(abs(M-np.array(hess).T))<1e-6
    # Infinitesimal load reduces to a pure end moment Fr.
    a=equilibrium(266.6666667,12.,1e-5,n=128)
    expected=-1e-5*.4*12**2/(2*266.6666667)
    assert abs(a['y']/expected-1)<.0001
    # Unloaded tiny transverse force has cantilever displacement HL^3/(3EI).
    a=equilibrium(266.6666667,12.,H=-1e-5,n=128)
    assert abs(a['y']/(-1e-5*12**3/(3*266.6666667))-1)<.0001
    assert not overlap(rectangle(0,1,0,1),rectangle(1,2,0,1))
    assert overlap(rectangle(0,1,0,1),rectangle(.5,2,.5,2))


def main():
    verify()
    converged=[{'n':n,**branch(n=n,step=s),'step':s} for n,s in [(32,.01),(64,.005),(128,.0025),(256,.00125)]]
    sections=[]
    for E,t in [(200000,.1),(200000,.2),(200000,.4),(2000,.4),(2000,.8)]:
        EI=E*2*t**3/12
        a=release(EI=EI)
        sections.append({'E':E,'t':t,'EI':EI,**branch(EI=EI),
                         'release_N':-a['H'],'release_strain':t/2*max(abs(np.diff(np.r_[0,a['theta']])))/(12/64)})
    # Coherent corners are alternative constructed banks, not independent draws.
    corners=[]
    for E in [160000,220000]:
        for t in [.18,.22]:
            for L in [11.5,12.5]:
                for r in [.3,.5]:
                    for e in [.9,1.1]:
                        EI=E*2*t**3/12
                        corners.append(branch(EI,L,r,e,step=.01))
    loaded=[]
    for F in [.02,1.,1.75]:
        a=equilibrium(266.6666666667,12.,F,n=128)
        contact_z=a["z"]-(.4-a["y"])*math.tan(a["tip_angle"])
        shape=bodies(a)
        tooth=rectangle(.4,1.6,contact_z-2,contact_z)
        assert a["a"] < 1 and not any(overlap(p,tooth) for p in shape)
        loaded.append({"F":F,"contact_a":a["a"],"drop":contact_z-12,
                       "horizontal_reaction":F*math.tan(a["tip_angle"]),
                       "strain":.1*max(abs(np.diff(np.r_[0,a["theta"]])))/(12/128)})
    rel=release()
    # Sampled release phases, with old rack lifted 1 mm. Union of five rack
    # teeth over all five initial heights: nine relative tooth positions.
    # Spacing 10 mm, thickness 2 mm; exact convex section collision per phase.
    collisions=0
    min_tooth_gap=float('inf')
    for i in range(65):
        a=equilibrium(266.6666667,12.,H=rel['H']*i/64)
        shape=bodies(a)
        for j in range(-4,5):
            bottom=12.-1.+10*j
            tooth=rectangle(.4,1.6,bottom-2,bottom)
            collisions+=sum(overlap(p,tooth) for p in shape)
        hook=shape[-1]
        min_tooth_gap=min(min_tooth_gap,float(min(hook[:,1])-11))
    # Withdrawn hook has y<rack edge, hence every intermediate 40-mm translation
    # and all 20 unequal five-state moves clear without a time discretization.
    opened=bodies(rel)
    max_y=max(float(max(p[:,0])) for p in opened)
    assert max_y < .4 and collisions==0
    # Finite rear obstacle: free face y=-.2, z=[11.8,12.8].
    stop=rectangle(-1.,-.2,11.8,12.8)
    blocked=[]
    for i in range(65):
        a=equilibrium(266.6666667,12.,H=rel['H']*i/64)
        if any(overlap(p,stop) for p in bodies(a)):
            blocked.append(i)
    assert blocked
    print(json.dumps({'self_checks':'passed','linear_runoff_N':linear_runoff(),'loaded_contacts':loaded,'convergence':converged,'sections':sections,
        'coherent_corners':{'count':len(corners),'min_last_supported_N':min(x['last_supported_F'] for x in corners),'max_last_supported_N':max(x['last_supported_F'] for x in corners),'events':sorted(set(x['event'] for x in corners))},
        'release_geometry':{'force_N':-rel['H'],'tip_y':rel['y'],'tip_z':rel['z'],'angle':rel['tip_angle'],'max_body_y':max_y,'sampled_release_collisions':collisions,'old_tooth_gap':min_tooth_gap,'rear_stop_blocked_phases':len(blocked),'first_blocked_phase':blocked[0]/64,'clear_unequal_transitions':20}},indent=2))

if __name__=='__main__':main()
