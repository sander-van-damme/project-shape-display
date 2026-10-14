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


def joined_stock(c, force=.2, eccentricity=0., kerf=1.):
    """Three finite coaxial pieces, with flush butt seats (no hidden spigots).

    Bond/fixture design and material properties are deliberately unqualified.
    Positive pressure means compression; a negative full-contact prediction
    requires bond tension OR redistribution/opening, not a compression pass.
    """
    area=c.width**2-c.inner**2
    inertia=(c.width**4-c.inner**4)/12
    bending=force*eccentricity*c.width/(2*inertia)
    return dict(piece_z_mm=[(0.,c.nut),(c.nut,c.length-c.roof),
                            (c.length-c.roof,c.length)],
                tube_mm3=area*c.cavity_length,
                ends_mm3=[c.nut*(c.width**2-math.pi*d*d/4)+c.roof*c.width**2
                          for d in (c.cutter_major,c.cutter_minor)],
                contact_area=area, full_contact_pressure=[force/area-bending,force/area+bending],
                kern_mm=inertia/(area*c.width/2),
                # Total consumed feed length before stock-end/batch losses.
                cut_feed_mm=c.cavity_length+kerf, kerf_mm3=area*kerf,
                cut_faces=2, joins=2)


def process_ledger(c, n):
    """Operation inventory, NOT measured cycle time/yield or complete labor.

    10--30 s is a common sensitivity per named manual operation, not a prior.
    Mold example grants 16 cavities; its tooling and automatic reset aren't free.
    References at 4096/6400 scale this SAME body, not fitting finer pitches.
    """
    stock=joined_stock(c)
    plates=math.ceil(n/packing(c)[1]['total'])
    return dict(cells=n,
        same_body_liters=[n*c.volume(d)/1e6 for d in (c.cutter_major,c.cutter_minor)],
        half_degree_mold_liters=[n*c.volume(d,.5)/1e6 for d in (c.cutter_major,c.cutter_minor)],
        integral=dict(pieces=n,joins=0,plates=plates,removal_inspection_sites=n,
                      active_h=[plates*5/60+joins(n,1,t) for t in (10,30)]),
        stock=dict(pieces=3*n,joins=2*n,cuts=n,cut_faces=2*n,
                   feed_m=n*stock['cut_feed_mm']/1000,
                   kerf_liters=n*stock['kerf_mm3']/1e6,
                   # Cut/deburr counted as one operation plus two joins.
                   active_h=[joins(n,3,t) for t in (10,30)]),
        open_top_mold=dict(pieces=2*n,joins=n,cavity_cycles=n,
                          cycles_at_16=math.ceil(n/16),core_pulls=n,former_unscrews=n,
                          core_pull_mm=c.cavity_length,former_retreat_mm=c.nut,
                          former_turns=c.nut/3,
                          # Core pull/reset, unscrew/reset, eject/trim, cap join.
                          active_h=[joins(n,4,t) for t in (10,30)]))


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
        joined_stock=joined_stock(c,.2,c.width/2),
        process_ledger=[process_ledger(c,n) for n in (1024,4096,6400)],
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
    s=joined_stock(c)
    # Pieces tile the full length without an inaccessible inserted joint.
    assert s['piece_z_mm'][0][0]==0 and s['piece_z_mm'][-1][1]==c.length
    for a,b in zip(s['piece_z_mm'],s['piece_z_mm'][1:]): assert a[1]==b[0]
    for bore,ends in zip((c.cutter_major,c.cutter_minor),s['ends_mm3']):
        assert math.isclose(s['tube_mm3']+ends,c.volume(bore),abs_tol=1e-9)
    # Independently integrate full-contact normal traction on four rectangles.
    # Midpoint quadrature is exact for force; x^2 moment converges with mesh.
    F,e=.2,c.width/2
    A=c.width**2-c.inner**2; I=(c.width**4-c.inner**4)/12
    errors=[]
    for k in (20,40,80):
        resultant=moment=0.
        strips=[(-c.width/2,c.width/2,-c.width/2,-c.inner/2),
                (-c.width/2,c.width/2,c.inner/2,c.width/2),
                (-c.width/2,-c.inner/2,-c.inner/2,c.inner/2),
                (c.inner/2,c.width/2,-c.inner/2,c.inner/2)]
        for x0,x1,y0,y1 in strips:
            da=(x1-x0)*(y1-y0)/k
            for j in range(k):
                x=x0+(j+.5)*(x1-x0)/k
                pressure=F/A+F*e*x/I
                resultant+=pressure*da; moment+=pressure*da*x
        assert math.isclose(resultant,F,abs_tol=1e-12)
        errors.append(abs(moment-F*e))
    assert errors[2]<errors[1]<errors[0] and errors[-1]/(F*e)<1e-4
    assert joined_stock(c,F,s['kern_mm'])['full_contact_pressure'][0]>-1e-12
    assert joined_stock(c,F,e)['full_contact_pressure'][0]<0
    assert joined_stock(c,F,0)['full_contact_pressure'][0]>0
    ledger=process_ledger(c,1024)
    assert ledger['stock']['feed_m']==128 and ledger['stock']['joins']==2048
    assert ledger['open_top_mold']['cycles_at_16']==64
    assert math.isclose(ledger['stock']['active_h'][1],25.6)
    print(f'{count} rigid core-section checks; independent volume/energy, draft failure, footprint, joined-seat equilibrium/convergence and labor anchors pass')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    if args.check: check()
    else: print(json.dumps(report(),indent=2))
