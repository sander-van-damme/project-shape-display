"""E-305: finite air-core winding / uniformly axially magnetized cylinder.
SI internally. External coil field only. No invented steel permeability multiplier.
Exact circular-loop Biot-Savart field, integrated over both magnet end faces.
"""
import numpy as np
from scipy.special import ellipk, ellipe
from numpy.polynomial.legendre import leggauss
MU0=4e-7*np.pi

def turns(layers=7, axial=20, pitch=.00018, inner=.0024):
    r,z=np.meshgrid(inner+(np.arange(layers)+.5)*pitch,
                    -(np.arange(axial)+.5)*pitch)
    return r.ravel(),z.ravel()

def bz(r,z,amps=1.,winding=None):
    """Coil occupies -3.6 <= z <= 0 mm; positive current gives +Bz."""
    a,zc=turns() if winding is None else winding
    r=np.asarray(r)[...,None];z=np.asarray(z)[...,None]-zc
    q=(a+r)**2+z*z;d=(a-r)**2+z*z;k2=4*a*r/q
    return np.sum(MU0*amps/(2*np.pi*np.sqrt(q))*(ellipk(k2)+(a*a-r*r-z*z)/d*ellipe(k2)),axis=-1)

def force(gap,amps=1.,diameter=.003,thickness=.002,br=1.395,quad=40,winding=None):
    """gap: signed lower magnet face height relative to top winding edge.
    Negative gap means insertion in bore; positive force is upward, away from coil.
    Magnet's N face is upper (+z); uniformly magnetized, recoil mu_r~1 omitted.
    """
    x,w=leggauss(quad);r=(x+1)*diameter/4;dr=diameter/4
    return float(br/MU0*np.sum(w*2*np.pi*r*dr*(bz(r,gap+thickness,amps,winding)-bz(r,gap,amps,winding))))

def winding_properties(winding=None,wire=.00015,leads=.1):
    a,z=turns() if winding is None else winding
    length=float(2*np.pi*sum(a));area=np.pi*wire**2/4
    resistance=1.724e-8*(length+leads)/area
    mass=8960*area*length
    # Wheeler multilayer approximation: dimensions in inches, inductance microhenry.
    rm=np.mean(a)/.0254;length_axial=(max(z)-min(z)+.00018)/.0254
    build=(max(a)-min(a)+.00018)/.0254
    L=1e-6*.8*rm**2*len(a)**2/(6*rm+9*length_axial+10*build)
    return dict(turns=len(a),wire_length_m=length+leads,resistance_20C_ohm=resistance,
                copper_mass_g=mass*1000,heat_capacity_J_K=mass*385,inductance_H_estimate=L)

def magnet_axis(gap,diameter=.003,thickness=.002,br=1.395):
    r=diameter/2
    return br/2*((gap+thickness)/np.sqrt((gap+thickness)**2+r*r)-gap/np.sqrt(gap*gap+r*r))

def cone_torque(fmag,mu=.25,alpha_deg=35,ri=.004,ro=.005,mass=.0004,
                slide_mu=.15,spline_radius=.0015):
    """Torque available while closing/sliding spline under load. N*m.
    Conservative axial guide friction mu_s*T/r_s included, no stationary selector.
    Existing screw support drag is already in E-303 torque scenarios.
    """
    re=2/3*(ro**3-ri**3)/(ro**2-ri**2)
    k=mu*re/np.sin(np.deg2rad(alpha_deg))
    return max(0,fmag-mass*9.80665)*k/(1+k*slide_mu/spline_radius)

def neighbor_dipole(pitch=.00508,dz=0.,br=1.395,diameter=.003,thickness=.002):
    """Parallel axial point-dipole estimate; finite-size error NOT bounded."""
    m=br/MU0*np.pi*(diameter/2)**2*thickness
    r=np.hypot(pitch,dz);c=dz/r
    bz_neigh=MU0*m/(4*np.pi*r**3)*(3*c*c-1)
    fz=3*MU0*m*m/(4*np.pi*r**4)*c*(3-5*c*c)
    fx=3*MU0*m*m/(4*np.pi*r**4)*(pitch/r)*(1-5*c*c)
    return dict(Bz_T=bz_neigh,Fz_N=fz,Fx_N=fx)

def finite_neighbor(pitch=.00508,dz=0.,br=1.395,diameter=.003,thickness=.002,nr=8,nt=48):
    """Magnetic surface-charge double quadrature for two parallel finite cylinders.
    No dipole approximation; recoil mu_r~1. Field at target center, total force.
    Axial faces carry +/- M. Equal area annular quadrature and azimuthal midpoints.
    """
    rr=(np.arange(nr)+.5)/nr*(diameter/2)**2
    phi=(np.arange(nt)+.5)*2*np.pi/nt
    xx=(np.sqrt(rr)[:,None]*np.cos(phi)).ravel()
    yy=(np.sqrt(rr)[:,None]*np.sin(phi)).ravel()
    da=np.pi*(diameter/2)**2/(nr*nt);mag=br/MU0;F=np.zeros(3);B=np.zeros(3)
    for s in [-1,1]:
      for t in [-1,1]:
        dx=pitch+xx[:,None]-xx[None,:];dy=yy[:,None]-yy[None,:]
        zz=dz+(t-s)*thickness/2;rr3=(dx*dx+dy*dy+zz*zz)**1.5
        c=MU0/(4*np.pi)*mag**2*s*t*da**2
        F+=c*np.array([np.sum(dx/rr3),np.sum(dy/rr3),np.sum(zz/rr3)])
      d=np.stack([pitch-xx,-yy,np.full_like(xx,dz-s*thickness/2)],axis=1)
      B+=MU0/(4*np.pi)*mag*s*da*np.sum(d/np.linalg.norm(d,axis=1)[:,None]**3,axis=0)
    return dict(Bz_T=float(B[2]),Fz_N=float(F[2]),Fx_N=float(F[0]))

def core_surrogate(gap,amps,nd=.15,bs=2.0,core_r=.0015,core_length=.008):
    """Uniform cylindrical core, demagnetizing-factor/saturation sensitivity ONLY.
    No material B-H data fitting, remanence, local pole saturation or hysteresis.
    Must not be interpreted as validated core force or a rigorous bound.
    """
    x,w=leggauss(20);r=(x+1)*core_r/2;wr=w*2*r/core_r**2*core_r/2
    zz=(x+1)*core_length/2-core_length;wz=w/2
    R,Z=np.meshgrid(r,zz);W=wz[:,None]*wr[None,:]
    pmwind=(np.full(80,.0015),gap+(np.arange(80)+.5)*.002/80)
    hpm=float(np.sum(W*bz(R,Z,1.395/MU0*.002/80,pmwind))/MU0)
    hc=float(np.sum(W*bz(R,Z,amps))/MU0)
    mc=bs/MU0*np.tanh((hpm+hc)/(nd*bs/MU0))
    cw=(np.full(100,core_r),-(np.arange(100)+.5)*core_length/100)
    fc=force(gap,mc*core_length/100,winding=cw)
    return dict(force_N=fc+force(gap,amps),core_M_A_m=mc,Hpm_average_A_m=hpm,Hcoil_average_A_m=hc)

def face_envelope(phase_deg,kind='triangular',n=6,height=.0006,flat_fraction=.12):
    """Ideal periodic opposed face ramp required axial separation.
    One full period, symmetric peaks/valleys. A geometric screening surrogate,
    not a claimed recreation of E-298's mesh or a rigid-contact dynamics solver.
    """
    phase=(np.asarray(phase_deg)*n/360)%1
    t=1-abs(2*phase-1)
    if kind=='rounded': return height*(1-np.cos(2*np.pi*phase))/2
    if kind=='flat': return height*np.minimum(t/(1-flat_fraction),1)
    return height*t
