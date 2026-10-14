#!/usr/bin/env python3
"""Coarse column section, rigid tooling access and manufacturing ledger.

All mechanics/process inputs are explicit scenarios, not qualified PLA/X1C
properties. No FEA, thread strength, printability or production yield claim.
"""
import argparse
from dataclasses import dataclass
import json
import math


@dataclass(frozen=True)
class Column:
    width: float = 10.3
    wall: float = .8
    length: float = 136.
    nut: float = 10.
    roof: float = 2.
    # E-263 explicit radial relief, NOT historical trial-5 implicit slop.
    cutter_major: float = 3.5
    cutter_minor: float = 1.7
    screw_major: float = 3.2

    @property
    def inner(self):
        return self.width - 2*self.wall

    @property
    def cavity_length(self):
        return self.length - self.nut - self.roof

    def cavity_width(self, z, draft_deg=0.):
        assert self.nut <= z <= self.length-self.roof
        return self.inner-2*(self.length-self.roof-z)*math.tan(math.radians(draft_deg))

    def volume(self, bore, draft_deg=0.):
        """Exact section volume for cylindrical thread-volume bound, mm^3."""
        top = self.inner
        bottom = self.cavity_width(self.nut, draft_deg)
        if bottom <= 0:
            raise ValueError('Draft closes the cavity')
        # Integral of square, linearly tapered core cross section.
        cavity = self.cavity_length*(top*top+top*bottom+bottom*bottom)/3
        return self.width**2*self.length-cavity-math.pi*bore**2*self.nut/4

    def core(self, draft_deg, axis_error=.2, cavity_width_error=.1):
        bottom = self.cavity_width(self.nut, draft_deg)
        return dict(draft_deg=draft_deg, bottom_width=bottom,
                    bottom_wall=(self.width-bottom)/2,
                    screw_clearance=(bottom-self.screw_major-cavity_width_error)/2-axis_error,
                    # Neither end of a CLOSED body lets this core through.
                    closed_bottom_gap=self.cutter_major-math.sqrt(2)*self.inner,
                    closed_top_gap=-self.inner,
                    liters_1024=[1024*self.volume(bore,draft_deg)/1e6
                                 for bore in (self.cutter_major,self.cutter_minor)])


def roof_strip(force, span=8.7, thickness=2., breadth=1., modulus=1000.):
    """Simply supported beam strip with central point force, N/mm/MPa.

    Deliberately discards adjacent plate width and two-edge support. This is a
    strip surrogate, NOT a rigorous upper bound for an anisotropic printed roof.
    Force is placed on this one strip; no borrowed load-sharing assumption.
    """
    inertia=breadth*thickness**3/12
    return dict(stress=1.5*force*span/(breadth*thickness**2),
                deflection=force*span**3/(48*modulus*inertia))


def load_demands(c, force, eccentricity=0.):
    area=c.width**2-c.inner**2
    inertia=(c.width**4-c.inner**4)/12
    return dict(shell_area=area, shell_inertia=inertia,
                shell_max_normal_stress=force/area+force*eccentricity*c.width/(2*inertia),
                nut_net_average=force/(c.width**2-math.pi*c.cutter_major**2/4),
                roof=roof_strip(force,span=c.inner,thickness=c.roof),
                # Optimistic whole annular cap-seat area; actual contact unknown.
                cap_seat_average=force/area)


def packing(c, plate=256., margin=10., gap=3.):
    """Explicit two-strip footprint, not optimal nesting or a slicing result.

    First strip has horizontal long columns. In the unused width, add columns
    rotated 90 degrees. Includes gap between groups; no braces/brims/screws.
    """
    usable=plate-2*margin
    across=math.floor((usable+gap)/(c.width+gap))
    remaining=usable-c.length-gap
    rotated=math.floor((remaining+gap)/(c.width+gap)) if remaining>=c.width else 0
    assert c.length<=usable
    rectangles=[]
    for i in range(across):
        y=i*(c.width+gap)
        rectangles.append((0.,y,c.length,y+c.width))
    for i in range(rotated):
        x=c.length+gap+i*(c.width+gap)
        rectangles.append((x,0.,x+c.width,c.length))
    return rectangles,dict(horizontal=across,rotated=rotated,total=len(rectangles),
                           plates_1024=math.ceil(1024/len(rectangles)))


def joins(cells, per_cell, seconds):
    return cells*per_cell*seconds/3600


def report():
    c=Column()
    _,packed=packing(c)
    low=c.volume(c.cutter_major); high=c.volume(c.cutter_minor)
    return dict(evidence='Section calculations and rigid-core geometry; unqualified process scenarios',
        cell_mm3=[low,high], board_liters=[1024*low/1e6,1024*high/1e6],
        core=[c.core(a) for a in (0.,.5,1.)],
        max_draft_screw_clear_deg=math.degrees(math.atan((c.inner-c.screw_major-.1-2*.2)/(2*c.cavity_length))),
        load={str(f):load_demands(c,f,c.width/2) for f in (.2,9.81)},
        roof_modulus_250=roof_strip(.2,modulus=250),
        roof_half_thickness=roof_strip(.2,thickness=1),
        packing=packed,
        ideal_deposition_h={str(q):1024*low/q/3600 for q in (5.,10.,15.)},
        plate_handling_h_5min=packed['plates_1024']*5/60,
        joins_h={str(n):{str(j):[joins(n,j,t) for t in (10,30)] for j in (1,2)}
                 for n in (1024,4096,6400)},
        # Cap-only adds to inherited four-spindle labor; not a complete new total.
        cap_plus_inherited_h=[10.94+joins(1024,1,10),23.69+joins(1024,1,30)],
        material_kg_scenario=[1024*low/1e6*1.24,1024*high/1e6*1.24],
        # This is column material only, no stock/thread/guide quote.
        material_usd_scenario=[1024*low/1e6*1.24*20,1024*high/1e6*1.24*30])


def check():
    c=Column()
    # Independent tube + bottom + roof volume decomposition, no double counting.
    for bore in (c.cutter_major,c.cutter_minor):
        v=(c.width**2-c.inner**2)*c.length+(c.inner**2-math.pi*bore**2/4)*c.nut+c.inner**2*c.roof
        assert math.isclose(c.volume(bore),v,abs_tol=1e-9)
    # Simpson integral exactly integrates the quadratic tapered cavity area.
    count=0
    for angle in (0.,.25,.5,1.):
        z0=c.nut; z1=c.length-c.roof; zm=(z0+z1)/2
        void=(z1-z0)*(c.cavity_width(z0,angle)**2+4*c.cavity_width(zm,angle)**2+c.cavity_width(z1,angle)**2)/6
        independent=c.width**2*c.length-void-math.pi*c.cutter_major**2*c.nut/4
        assert math.isclose(c.volume(c.cutter_major,angle),independent,abs_tol=1e-9)
        # After upward extraction, every overlapping square-core section is no
        # wider than its cavity section. Cap must be absent; thread former is
        # separate and removed by unscrewing, not credited by this check.
        for dz in (.01,1.,20.,124.):
            for i in range(101):
                z=z0+(z1-z0)*i/100
                local=z-dz
                if z0<=local<=z1:
                    assert c.cavity_width(local,angle)<=c.cavity_width(z,angle)+1e-12
                    count+=1
    assert c.core(1.)['screw_clearance']>0
    assert c.core(1.5)['screw_clearance']<0
    # Volume becomes invalid as the tapered core degenerates.
    try: c.volume(c.cutter_major,3.)
    except ValueError: pass
    else: raise AssertionError('closed cavity not rejected')
    assert c.core(0)['closed_bottom_gap']<0 and c.core(0)['closed_top_gap']<0
    # Strip compliance independently recovered from strain energy (Castigliano).
    F,L,E,I=.2,8.7,1000.,2**3/12
    strain_energy=F**2*L**3/(96*E*I)
    assert math.isclose(2*strain_energy/F,roof_strip(F)['deflection'])
    assert math.isclose(roof_strip(2*F)['deflection'],2*roof_strip(F)['deflection'])
    assert math.isclose(roof_strip(F,thickness=1)['deflection'],8*roof_strip(F)['deflection'])
    rects,p=packing(c)
    assert p['total']==24 and p['plates_1024']==43
    for a in rects:
        assert min(a)>=0 and max(a)<=236
        for b in rects:
            if a==b: continue
            assert a[2]+3<=b[0]+1e-10 or b[2]+3<=a[0]+1e-10 or a[3]+3<=b[1]+1e-10 or b[3]+3<=a[1]+1e-10
    for n in (1024,4096,6400):
        assert math.isclose(joins(n,2,10),2*joins(n,1,10))
    print(f'{count} rigid core-section checks; independent volume/energy, draft failure, footprint and labor anchors pass')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    if args.check: check()
    else: print(json.dumps(report(),indent=2))
