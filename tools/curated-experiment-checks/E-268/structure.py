#!/usr/bin/env python3
"""Supported slotted beds: conditional mm/N/MPa beam screens, not hardware QA.

All loads, elastic moduli, edge errors and budgets are labelled scenarios.
No strength, creep, print-yield or safe-speed claim. See canonical E-268.
"""
import itertools
import json
import math
import support as s


def center_point_sum(length, sites, loads, EI):
    """Closed-form center displacement from point loads, AWC figure 8."""
    return sum(F * min(x, length-x) *
               (3*length**2-4*min(x, length-x)**2)/(48*EI)
               for x, F in zip(sites, loads))


def integrated_curvature(length, sites, loads, EI, steps=16000):
    """Separate solution of EI*y''=M with y(0)=y(L)=0, midpoint integration.

    Integrate moment twice and solve the unknown initial slope. Does not use
    the point-load displacement or virtual-unit-load expressions.
    """
    left = sum(F*(length-x)/length for x, F in zip(sites, loads))
    dx = length/steps
    y_end = y_mid = 0.
    for k in range(steps):
        x = (k+.5)*dx
        M = left*x-sum(F*max(0., x-a) for a,F in zip(sites,loads))
        curvature = M/EI
        y_end += (length-x)*curvature*dx
        if x < length/2:
            y_mid += (length/2-x)*curvature*dx
    return y_end/2-y_mid


def row_constant(p, count, force, modulus, inertia):
    L = p*count
    return center_point_sum(L, [(i+.5)*p for i in range(count)],
                            [force]*count, modulus*inertia)


def guide(p, slot, modulus, edge_loss=0., H=.1, torque=0., stroke=50):
    """Aperture side ligament, point contact midway along 4.64-mm edge.

    One rail bears all transverse reaction; no equal-load-sharing credit.
    Simply supported local edge, plus fully fixed control (4x stiffer).
    Slot/hole edge shifts towards each other sum to edge_loss.
    """
    a=4.64; t=2.; b=p-slot; w=(b-a)/2-edge_loss
    # E-261 guide centers 40 apart, top max is stroke+3 above upper center.
    Rlo=H*(stroke+3)/40
    Rhi=-H-Rlo
    # Conservative allocation of the whole anti-rotation couple to lower bed;
    # two opposed contacts separated by pin width, not an extra mechanism.
    F=Rlo+abs(torque)/4.4
    if w<=0:
        return dict(connected=False,ligament_mm=w)
    I=t*w**3/12
    d=F*a**3/(48*modulus*I)
    stress=F*a*w/(8*I)
    # Global disconnected-rail control: grant no ladder-frame shear coupling.
    # Gross solid strip is the opposite optimistic control, not a guide pass.
    return dict(connected=True,ligament_mm=w,lower_N=Rlo,upper_N=Rhi,
                edge_contact_N=F,local_simple_mm=d,local_fixed_mm=d/4,
                nominal_edge_MPa=stress,
                rail16_mm=row_constant(p,16,Rlo,modulus,I),
                gross16_mm=row_constant(p,16,Rlo,modulus,t*b**3/12),
                sliding_drag_N=.3*(abs(Rlo)+abs(Rhi)))


def crossrail(p, count, E, F=.05, width=1., depth=10.):
    """Interior crossrail segment: two adjacent bays each give nF/2 per row.

    Grounded at both segment ends. End rails carry half this load. Ground
    connections and panel joints remain unconstructed, not rigid by evidence.
    """
    P=count*F
    I=width*depth**3/12
    return dict(deflection_mm=row_constant(p,count,P,E,I),
                nominal_MPa=(count*P*p*count/8)*(depth/2)/I,
                total_segment_N=count*P,
                per_end_N=count*P/2)


def checks():
    # Independent curvature integration, asymmetric loads and point/UDL limits.
    for L,sites,loads in [(100,[50],[1]), (100,[17,63],[.3,.7]),
                          (101.6,[(i+.5)*6.35 for i in range(16)],[.05]*16)]:
        got=center_point_sum(L,sites,loads,70000*3)
        assert math.isclose(got,integrated_curvature(L,sites,loads,70000*3),rel_tol=2e-7)
    assert math.isclose(center_point_sum(100,[50],[1],12),100**3/(48*12))
    count=1000; L=100.; E=70000.; I=3.; q=.01
    point=row_constant(L/count,count,q*L/count,E,I)
    assert math.isclose(point,5*q*L**4/(384*E*I),rel_tol=2e-6)
    # No slot / no hole matches existing beam quadrature; SI conversion control.
    d=row_constant(6.35,16,.05,1000,5.45*2**3/12)
    assert math.isclose(d,s.beam(6.35,16,.9,3.6,2,1000,.05,mode='solid')[0],rel_tol=2e-7)
    assert math.isclose(1*.1**3/(48*70e9*(.002*.000305**3/12))*1000,
                        1*100**3/(48*70000*(2*.305**3/12)))
    for stroke,H in itertools.product((40,50),(.02,.1,.5)):
        g=guide(6.35,1.1,1000,H=H,stroke=stroke)
        assert math.isclose(g['lower_N']+g['upper_N']+H,0,abs_tol=1e-12)
        assert math.isclose(g['upper_N']*40+H*(40+stroke+3),0,abs_tol=1e-12)
    g=guide(6.35,1.1,1000)
    assert math.isclose(guide(6.35,1.1,2000)['local_simple_mm']*2,g['local_simple_mm'])
    assert math.isclose(guide(6.35,1.1,1000,H=.2)['local_simple_mm'],2*g['local_simple_mm'])
    assert not guide(5.08,.7,200000)['connected']
    assert guide(6.35,1.1,1000,edge_loss=.2)['local_simple_mm']>24*g['local_simple_mm']
    # Single changed thrust load moves an unchanged center of the shared strip.
    n=16; L=n*6.35; E=70000.; I=(6.35-1.1-3.6)*2**3/12
    neighbor=center_point_sum(L,[L/2-6.35/2],[.2],E*I)
    assert neighbor>0
    return dict(curvature_closed_form=True,UDL_limit=True,SI_units=True,
                reaction_balance=True,edge_scaling=True,
                changed_site_center_net_control_mm=neighbor)


def main():
    thrust=[]
    for p,slot,n,E,t in itertools.product((6.35,5.08),(1.1,), (8,16),
                                         (1000,3000,70000,200000),(2,4,6)):
        # Fine .7-mm slot gives generous clearance above .666-mm ray envelope.
        if p==5.08: slot=.7
        d,stress=s.beam(p,n,slot,3.6,t,E,.05)
        net=row_constant(p,n,.05,E,(p-slot-3.6)*t**3/12)
        thrust.append(dict(pitch=p,slot=slot,count=n,E_MPa=E,t_mm=t,
                           variable_mm=d,net_control_mm=net,nominal_MPa=stress))
    guides=[dict(pitch=p,slot=slot,E_MPa=E,edge_loss_mm=loss,
                 **guide(p,slot,E,loss))
            for p,slot in ((6.35,1.1),(5.08,.7))
            for E,loss in itertools.product((1000,3000,70000,200000),(0.,.1,.2))]
    optics=[dict(pitch=p,**s.optical_bay(n,t,stroke=S,pitch=p,error=e,crossbar=rib))
            for p,e,rib in ((6.35,.1,1.),(5.08,.05,.2))
            for n,t,S in itertools.product((8,16),(2,6),(40,50))]
    assert all(x['blocked_samples']==0 for x in optics)
    assert all(x['required_slot_mm'] < (1.1 if x['pitch']==6.35 else .7) for x in optics)
    rails=[dict(pitch=p,count=n,E_MPa=E,width_mm=1. if p==6.35 else .2,
                **crossrail(p,n,E,width=1. if p==6.35 else .2))
           for p,n,E in itertools.product((6.35,5.08),(8,16),(1000,70000,200000))]
    ledger={n:{'pairs':n*n,'guide_apertures':2*n*n,'lower_guide_side_ligaments':2*n*n,
               'thrust_seats':n*n,'two_slotted_layer_row_spans_16':2*n*n//16,
               'two_slotted_layer_row_spans_8':2*n*n//8,
               'two_slotted_layer_panels_16square':2*(n//16)**2,
               'two_slotted_layer_panels_8square':2*(n//8)**2,
               'ground_grid_nodes_16':(n//16+1)**2,
               'ground_grid_nodes_8':(n//8+1)**2,
               'seconds_10_per_pair_hours':10*n*n/3600}
            for n in (64,80)}
    print(json.dumps(dict(checks=checks(),thrust=thrust,guides=guides,
                         guide_torque_case=guide(6.35,1.1,70000,torque=.35),
                         optics=optics,crossrails=rails,ledger=ledger),indent=2))


if __name__=='__main__':
    main()
