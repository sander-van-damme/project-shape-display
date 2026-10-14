#!/usr/bin/env python3
"""Exact interval wall/base screen; dimensions are scenarios, not measured parts."""
import argparse
from pathlib import Path

SQUARE = 25.4

def interval(base, left, right, clearance=0):
    """Admissible base-centre interval, including clearance on each side."""
    return left + base / 2 + clearance, right - base / 2 - clearance

def check():
    for thickness, expected in [(5.08,20.32),(6.35,19.05),(12.7,12.7),(1,24.4)]:
        left,right=thickness/2,SQUARE-thickness/2
        assert abs(right-left-expected)<1e-10
        for base in (25,25.4,32):
            lo,hi=interval(base,left,right)
            assert hi<lo  # no lateral placement, not merely wrong centre
    assert abs((25.4-.4)-25)<1e-10
    assert interval(25,.2,25.2)==(12.7,12.7)  # exact tangency, no reserve
    # Moving both 1-mm walls outward preserves central corridor but loses neighbors.
    for left,right,expected in [(-25.4,-1,24.4),(0,25.4,25.4),(26.4,50.8,24.4)]:
        assert abs(right-left-expected)<1e-10
    s=25.4+1+2*.2
    lo,hi=interval(25.4,.5,s-.5,.2)
    assert abs(hi-lo)<1e-10
    assert abs(16*s+1-429.8)<1e-10
    print('PASS: interval exclusion, exact-fit boundary, neighbor loss, expanded-grid control')

def figure(path):
    from html import escape
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="1030" viewBox="0 0 1040 1030">',
         '<rect width="1040" height="1030" fill="white"/>',
         '<style>text{font-family:sans-serif;fill:#222} .grid{stroke:#5470a0;stroke-dasharray:5 4}</style>']
    def text(x,y,value,size=16):
        svg.append(f'<text x="{x}" y="{y}" font-size="{size}">{escape(value)}</text>')
    text(30,30,'Wall / floor interface: dimensioned top views',24)
    text(30,58,'Orange: assumed Ø25.4-mm bases. Dashed blue: game grid. Same scale in all panels.')
    cases=[('Full quarter-square walls centred on grid lines',25.4,6.35,False),
           ('Thin walls centred on grid lines',25.4,1,False),
           ('Walls outside the central corridor consume adjacent squares',25.4,1,True),
           ('Separate 1-mm wall lanes: expanded 26.8-mm square spacing',26.8,1,False)]
    scale=5
    for n,(title,s,t,outward) in enumerate(cases):
        cy=180+n*220
        def x(v):return 330+v*scale
        text(30,cy-85,title,19)
        for v in (-s,0,s,2*s):
            svg.append(f'<line x1="{x(v)}" x2="{x(v)}" y1="{cy-65}" y2="{cy+65}" class="grid"/>')
        walls=[(-t,0),(s,s+t)] if outward else [(-t/2,t/2),(s-t/2,s+t/2)]
        for left,right in walls:
            svg.append(f'<rect x="{x(left)}" y="{cy-65}" width="{(right-left)*scale}" height="130" fill="#555"/>')
        for cx in (-s/2,s/2,1.5*s):
            svg.append(f'<circle cx="{x(cx)}" cy="{cy}" r="{12.7*scale}" fill="#df9e45" fill-opacity="0.4" stroke="#b15d00"/>')
        left,right=walls[0][1],walls[1][0]
        text(735,cy-15,f'Clear: {right-left:.2f} mm')
        text(735,cy+10,f'Grid: {s:.2f} mm')
        text(735,cy+35,f'Wall: {t:.2f} mm')
        svg.append(f'<path d="M{x(left)},{cy+78} v10 M{x(left)},{cy+83} H{x(right)} M{x(right)},{cy+78} v10" fill="none" stroke="black"/>')
        text(x(left),cy+108,f'{right-left:.2f} mm between faces',14)
    text(30,985,'Geometry only: vertical walls extend through base height. No print or hardware qualification.',15)
    text(30,1010,'Expanded grid is a conditional interface control, not a selected product.',15)
    svg.append('</svg>');path.write_text('\n'.join(svg))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--figure',type=Path);a=p.parse_args()
    check()
    for t in (5.08,6.35,12.7,1,.4):
        print(f'wall {t:g} mm: clear {SQUARE-t:.2f} mm; max base with .2 mm/side reserve {SQUARE-t-.4:.2f} mm')
    if a.figure:figure(a.figure)
