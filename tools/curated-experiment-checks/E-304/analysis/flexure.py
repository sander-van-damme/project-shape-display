import numpy as np
# 2D planar Euler Bernoulli frame, x,z; flexure line segments.
def solve(thick=.5,b=3.6,E=2000,n=6,L=3.2,p=.9):
 pts=[]
 for j in range(n):
  pair=[(-L/2,j*p),(L/2,j*p)] if j%2==0 else [(L/2,j*p),(-L/2,j*p)]
  for pt in pair:
   if not pts or pt!=pts[-1]:pts.append(pt)
 N=len(pts);K=np.zeros((3*N,3*N)); members=[]
 for i in range(N-1):
  dx,dz=np.array(pts[i+1])-pts[i];l=np.hypot(dx,dz);c,s=dx/l,dz/l;A=b*thick;I=b*thick**3/12
  k=E/l*np.array([[A,0,0,-A,0,0],[0,12*I/l**2,6*I/l,0,-12*I/l**2,6*I/l],[0,6*I/l,4*I,0,-6*I/l,2*I],[-A,0,0,A,0,0],[0,-12*I/l**2,-6*I/l,0,12*I/l**2,-6*I/l],[0,6*I/l,2*I,0,-6*I/l,4*I]])
  t=np.array([[c,s,0,0,0,0],[-s,c,0,0,0,0],[0,0,1,0,0,0],[0,0,0,c,s,0],[0,0,0,-s,c,0],[0,0,0,0,0,1]])
  ix=np.arange(3*i,3*i+6);K[np.ix_(ix,ix)]+=t.T@k@t;members.append((ix,t,k,I))
 fixed=[0,1,2,3*N-3,3*N-1];free=np.array([i for i in range(3*N) if i not in fixed]);f=np.zeros(3*N);f[-2]=-1;u=np.zeros(3*N);u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free]);stress=[]
 for ix,t,k,I in members:
  ff=k@t@u[ix];stress.append(max(abs(ff[2]),abs(ff[5]))*thick/2/I)
 return {'k_N_mm':-1/u[-2],'stress_MPa_per_N':max(stress),'points':pts,'u_per_N':u.tolist()}
if __name__=='__main__':
 for t in [.35,.40,.45]:
  s=solve(t);print(t,s['k_N_mm'],s['stress_MPa_per_N'],s['k_N_mm']*1.4*s['stress_MPa_per_N'])
