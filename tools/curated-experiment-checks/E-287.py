#!/usr/bin/env python3
"""Supported cage necessary conditions. Allocated geometry/material/load, not FEA
or physical validation. Units mm, N, MPa; no probabilistic manufacturing claims.
Run: python tools/curated-experiment-checks/E-287.py
"""
from math import isclose, sqrt, radians, sin, cos

PITCH=12.7
BODY=10.9+.2+2*52*(10.9-10.2+.2)/82  # E-277 sufficient projection
N=8
FRAME_RESERVE=.2  # per-side rigid body/frame gap, not an earned process margin
INNER=(N-1)*PITCH+BODY+2*FRAME_RESERVE
BAR, HEIGHT, SHEET, GAP=2.2,8.,.8,.4
SPAN=INNER+BAR  # ring edge corner reaction center separation
OUTER=INNER+2*(BAR+SHEET)
H=176.  # lower ring bottom -42 to top guide 134
E=70000.  # competing assumed metal modulus, not a selected alloy rating
G=E/(2*(1+.33))
POINTS=[SPAN/2+(i-(N-1)/2)*PITCH for i in range(N)]


def point_midspan(load, length, points, modulus, inertia):
    return sum(load*min(x,length-x)*(3*length**2-4*min(x,length-x)**2)
               /(48*modulus*inertia) for x in points)


def guide_midspan(steps):
    # E-286 perforated 12x2 strips, extended seats to actual ring centerlines.
    dx=SPAN/steps
    d=0.
    for k in range(steps):
        x=(k+.5)*dx
        cut=any(abs(x-a)<5.4 for a in POINTS)
        inertia=2*(12**3-(10.8**3 if cut else 0))/12
        moment=N*.05*x/2-sum(.05*(x-a) for a in POINTS if a<x)
        d+=moment*min(x,SPAN-x)/2/(2000*inertia)*dx
    assert point_midspan(.05,SPAN,POINTS,2000,2*12**3/12)<d
    assert d<point_midspan(.05,SPAN,POINTS,2000,2*(12**3-10.8**3)/12)
    return d


def run():
    extra=OUTER+GAP-N*PITCH
    assert isclose(PITCH-BODY+extra,2*(BAR+SHEET+FRAME_RESERVE)+GAP)
    print('body/inner/ring span/module outer',BODY,INNER,SPAN,OUTER)
    print('added boundary/nominal pitch footprint/enclosure/top seam',extra,32*PITCH+3*extra,4*OUTER+3*GAP,PITCH-10.3+extra)
    guide=guide_midspan(64000)
    assert abs(guide-guide_midspan(32000))/guide<.002
    # Each strip carries 8*.05N, half to each ring side. Eight strip reactions.
    side_force=N*.05/2
    ring_I=HEIGHT*BAR**3/12
    ring=point_midspan(side_force,SPAN,POINTS,E,ring_I)
    # Two guides loaded in same direction: 64*.05*2N. Two shear walls parallel
    # to force transfer to bottom. Perfect corners, no fastener slip/buckling.
    lateral=N*N*.05*2
    shell_I=2*SHEET*SPAN**3/12
    shell=lateral*H**3/(3*E*shell_I)+lateral*H/(2*G*SHEET*SPAN)
    post_I=(3**4-(3-2*.8)**4)/12
    posts=(lateral/4)*H**3/(3*E*post_I)
    total=guide+ring+shell
    print('guide/ring/shell sum/post-only lateral mm',guide,ring,shell,total,posts)
    print('remaining .1mm joint budget / F per site at .1 (linear)',.1-total,.05*.1/total)
    assert total<.1 and posts>.1
    # Joint error correlations add, not root-sum-square. No sourced distribution.
    for joint in (0.,.02,.05):
        print('common series joint allowance and displacement',joint,total+joint)
    # Ring bending cross-check: midpoint point load is an upper bound for all
    # same-sign forces with constant section. UDL is not treated as exact.
    assert ring < (N*side_force)*SPAN**3/(48*E*ring_I)
    assert isclose(point_midspan(1,10,[5],2,3),10**3/(48*2*3))
    # Thrust: eight short box spines to lower ring, then panels/corner mounts.
    # Constant minimum I removes 2.8mm-width material from both horizontal faces
    # along entire length, a conservative global bending idealization.
    box_I=(12*24**3-10*22**3)/12
    removed=2*(2.8/12+2.8*11.5**2)
    spine=point_midspan(.338,SPAN,POINTS,2000,box_I-removed)
    lower_ring=point_midspan(N*.338/2,SPAN,POINTS,E,BAR*HEIGHT**3/12)
    panel_axial=N*N*.338*H/(E*4*SHEET*SPAN)
    print('payload thrust spine/lower ring/panel axial mm',spine,lower_ring,panel_axial)
    # Sockets: all 64 lie inside rings. Tool enters through two 2.8mm bores;
    # reach from lower-ring underside excludes tool compliance and exact socket fit.
    # Spines rest ON lower ring at -34, not intersecting its -42..-34 stock.
    print('edge socket to ring inner edge',INNER/2-(N-1)*PITCH/2)
    tool_corner=2/(sqrt(3)/2)
    print('nominal tip radial bore clearance/reach mm',(2.8-tool_corner)/2,32+4)
    assert tool_corner<2.8
    # Fixed 25.4mm bank covers each module in two parity groups per row.
    addresses={(r,c+2*k) for r in range(8) for c in (0,1) for k in range(4)}
    assert len(addresses)==64
    # Frame governs extraction envelope; residual gap is .4 and drift .1.
    def clearance(angle):
        a=radians(angle)
        return GAP-.1-OUTER*(sin(a)+cos(a)-1)/2
    lo,hi=0.,1.
    for _ in range(60):
        mid=(lo+hi)/2
        if clearance(mid)>0: lo=mid
        else: hi=mid
    print('sufficient extraction yaw deg/lift mm',lo,188+2-(-42))
    assert clearance(0)>0 and clearance(hi)<=0
    # Installed shelves beneath outer ring lip; lift pads beneath inner lip.
    # 1mm pads +1mm shelf allocation leave .2mm nominal transverse separation;
    # no fastener, load-spreading or actual registration qualification.
    assert BAR-1.-1. > 0
    stages=[('installed',1,0,0),('cradle loaded',1,1,0),
            ('mounts released',0,1,0),('bench supported',0,1,1),
            ('cradle withdrawn',0,0,1)]
    assert all(base or cradle or bench for _,base,cradle,bench in stages)
    print('support-state allocation',stages)
    # Ideal four 1x8mm cradle pads below inner lip: loads include shell/rings,
    # body+screw diagnostic, and polymer spines. No attachment/proof pass.
    ring_vol=( (INNER+2*BAR)**2-INNER**2 )*HEIGHT
    # Four sides, overlapping corners conservatively double-counted.
    panel_vol=4*OUTER*H*SHEET
    spine_vol=N*SPAN*(12*24-10*22)
    metal_kg=(3*ring_vol+panel_vol)*2.7e-6
    spine_kg=spine_vol*1.24e-6
    weight=N*N*.338+(metal_kg+spine_kg)*9.81
    print('module shell+rings kg / polymer spines kg / cradle N,MPa',metal_kg,spine_kg,weight,weight/32)
    for board in (32,64,80):
        modules=(board//8)**2
        # Monolithic machined rings count as 3; assembled bars would count12
        # plus12 corner joints/module. Minimum mounts/connections remain allocated.
        joints=3*4+2*8*2+8*2+4+4 # ring-panel,guide seats,spines,seams,mounts
        assert joints==68
        print('sites/modules/panels/rings/spines/guide seats/interfaces',board**2,modules,4*modules,3*modules,8*modules,32*modules,joints*modules)
        print('shell metal kg / added frame touch h20-60s',metal_kg*modules,[joints*modules*s/3600 for s in (20,60)])
    # Dollar ceilings only: 798 is E-276 optimistic four-spindle machine,
    # which already has unspecified frame allocation. This is incremental room,
    # NOT additive total BOM or quote. Superseded frame must be netted explicitly.
    for budget in (500,1000,1500):
        print('budget / gross incremental room per16 modules',budget,(budget-798)/16)
    print('No price, yield, fatigue, support/repair or speed qualification.')

if __name__=='__main__':
    run()
