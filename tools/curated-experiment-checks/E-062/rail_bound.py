"""Simply supported discrete-load screen; mm, N, MPa. Assumed bounds, no FEA.
Supports translate with the commanded rail; support/yoke compliance is omitted.
"""
from math import pi, isclose
from itertools import product


def point_deflection(x, a, length, force, ei):
    if x > a:
        return point_deflection(length-x, length-a, length, force, ei)
    b = length-a
    return force*b*x*(length**2-b**2-x**2)/(6*length*ei)


def full(n, pitch, force, modulus, width, depth):
    length = n*pitch
    ei = modulus*width*depth**3/12
    # Equal forces at cell centers: reflection symmetry puts maximum at center.
    return sum(point_deflection(length/2, (i+.5)*pitch, length, force, ei)
               for i in range(n))


def checks():
    # Independent central load formula, Maxwell reciprocity and support limits.
    L, E, I, P = 100., 1500., 2*8**3/12, 3.
    assert isclose(point_deflection(L/2,L/2,L,P,E*I),P*L**3/(48*E*I))
    for x,a in product((0.,13.,50.,81.,100.), repeat=2):
        assert isclose(point_deflection(x,a,L,P,E*I),point_deflection(a,x,L,P,E*I),abs_tol=1e-12)
    assert point_deflection(0,30,L,P,E*I)==point_deflection(L,30,L,P,E*I)==0
    assert full(8,5.08,0,E,2,8)==0
    assert isclose(full(8,5.08,P,2*E,2,8),full(8,5.08,P,E,2,8)/2)
    # Fixed total load/length -> uniform-load limit; convergence of quadrature.
    exact=5*P*L**3/(384*E*I)
    errors=[abs(full(n,L/n,P/n,E,2,8)-exact) for n in (10,20,40,80)]
    assert all(b<a for a,b in zip(errors,errors[1:]))
    assert errors[-1]/exact < .0002
    print('PASS central-load, reciprocity, supports, zero, stiffness and UDL convergence', errors)


def main():
    checks()
    pitch, width, allowance = 5.08, 2., .1
    valve = 1.5*pi/4 + 1. # E-061 1-mm seat; 1.5 MPa; spring+drag 1 N
    endpoint = valve/2
    print('endpoint selected load N',endpoint)
    # Preload is per shoe, present on every cell even when no valve opens.
    for modulus, depth, preload in product((500.,1500.,3000.),(4.,8.,12.),(0.,.1)):
        admissible=[n for n in range(1,81) if full(n,pitch,endpoint+preload,modulus,width,depth)<=allowance]
        n=max(admissible,default=0)
        print('E,h,preload',modulus,depth,preload,'max cells/span',n,'span mm',n*pitch,
              '80-cell sag mm',round(full(80,pitch,endpoint+preload,modulus,width,depth),6))
    E,h,pre=1500.,8.,.1
    for n in (8,10,12,80):
        L=n*pitch;ei=E*width*h**3/12
        dense=full(n,pitch,endpoint+pre,E,width,h)
        sparse=full(n,pitch,pre,E,width,h)+endpoint*L**3/(48*ei)
        print('reference n,dense,sparse mm',n,dense,sparse)
    # Required depth at full span; cubic stiffness scaling, not a packaging pass.
    for E in (500.,1500.,3000.):
        required=(full(80,pitch,endpoint+.1,E,width,1)/allowance)**(1/3)
        print('80-cell depth required mm',E,required)
    print('No yield, strength, creep, contact, support-yoke or dynamics qualification.')

if __name__=='__main__':
    main()
