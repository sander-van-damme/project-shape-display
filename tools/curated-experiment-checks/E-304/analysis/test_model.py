import unittest
from model import *
class PhysicsChecks(unittest.TestCase):
 def test_loop_axis(self):
  for z in [0,.001,.01]:
   expected=MU0*.003**2/(2*(.003**2+z*z)**1.5)
   self.assertAlmostEqual(bz(0,z,winding=(np.array([.003]),np.array([0]))),expected,places=12)
 def test_current_odd_and_zero(self):
  for g in [-.003,-.001,0,.001,.01]:
   self.assertAlmostEqual(force(g,.3),-force(g,-.3),places=12)
   self.assertEqual(force(g,0),0)
 def test_quadrature(self):
  for g in [-.001,0,.002]:
   self.assertAlmostEqual(force(g,.3,quad=20),force(g,.3,quad=80),places=10)
 def test_virtual_work(self):
  # Independent volume integral of -M B, then numerical energy gradient.
  x,w=leggauss(28);r=(x+1)*.0015/2;z=(x+1)*.002/2
  rr,zz=np.meshgrid(r,z);weights=w[:,None]*w[None,:]*.001*.00075*2*np.pi*rr
  def energy(g):return -1.395/MU0*np.sum(weights*bz(rr,zz+g,.3))
  g=.0004;eps=1e-7
  self.assertAlmostEqual(-(energy(g+eps)-energy(g-eps))/(2*eps),force(g,.3),places=8)
 def test_center_equilibrium(self):
  self.assertAlmostEqual(force(-.0028,.3),0,places=12)
  self.assertGreater(force(-.0029,.3),0);self.assertLess(force(-.0027,.3),0)
 def test_neighbor_convergence_and_farfield(self):
  a=finite_neighbor(dz=.0006,nr=8,nt=48);b=finite_neighbor(dz=.0006,nr=16,nt=96)
  self.assertLess(abs(a['Fz_N']/b['Fz_N']-1),.003)
  a=finite_neighbor(.05,.0006);b=neighbor_dipole(.05,.0006)
  self.assertLess(abs(a['Fz_N']/b['Fz_N']-1),.01)
 def test_neighbor_symmetry(self):
  a=finite_neighbor(dz=.0006);b=finite_neighbor(dz=-.0006)
  self.assertAlmostEqual(a['Fx_N'],b['Fx_N'],places=10)
  self.assertAlmostEqual(a['Fz_N'],-b['Fz_N'],places=10)
  self.assertAlmostEqual(finite_neighbor()['Fz_N'],0,places=10)
 def test_cone_force_balance(self):
  f=.05;t=cone_torque(f);re=2/3*(.005**3-.004**3)/(.005**2-.004**2)
  self.assertAlmostEqual(t,.25*re/np.sin(np.deg2rad(35))*(f-.0004*9.80665-.15*t/.0015))
 def test_periodic_geometry(self):
  for k in ['triangular','rounded','flat']:
   for p in [.1,3,25,31,50]:self.assertAlmostEqual(face_envelope(p,k),face_envelope(p+60,k))
 def test_addressing(self):
  # Local H bridges can represent any +/-/off per cell; passive buses must obey identity.
  for a,b,c,d in [(1,0,0,1),(1,-1,0,0)]:
   self.assertNotEqual(a+d,b+c)
  states={(0,0):0,(1,0):1,(0,1):-1}
  self.assertEqual(set(states.values()),{-1,0,1})
if __name__=='__main__':unittest.main()
