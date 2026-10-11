"""E-183: optimistic recoil/relay EPM circuit; SI; no calibrated hysteresis.

Run with Python's standard library. JSON is disposable. All scenario endpoints
are bounds, not random samples. Finite iron, leakage and pulse dynamics omitted.
"""
from dataclasses import dataclass, replace
from itertools import product
import json
import math

MU0 = 4e-7 * math.pi


@dataclass(frozen=True)
class Circuit:
    length: float = .005
    soft_area: float = 1e-6
    hard_area: float = 1e-6
    pole_area: float = 4e-6
    br_soft: float = 1.24
    br_hard: float = 1.24
    mu_soft: float = 4.0
    mu_hard: float = 1.05
    hc: float = 51700.0

    def solve(self, gap, state, ampere_turns=0.):
        """Parallel hard/soft magnet branches feed two series armature gaps.

        Only soft branch is wound. V is top-to-bottom magnetic potential.
        State +/-1 is a *stipulated* full remanence relay, not AlNiCo minor loops.
        """
        ph = MU0 * self.mu_hard * self.hard_area / self.length
        ps = MU0 * self.mu_soft * self.soft_area / self.length
        pg = MU0 * self.pole_area / (2 * gap)
        sh = self.hard_area * self.br_hard
        ss = state * self.soft_area * self.br_soft
        v = (sh + ss + ps * ampere_turns) / (ph + ps + pg)
        flux_h = sh - ph * v
        flux_s = ss + ps * (ampere_turns - v)
        flux_g = pg * v
        hs = (ampere_turns - v) / self.length
        force = flux_g**2 / (MU0 * self.pole_area)
        return dict(v=v, hs=hs, hh=-v/self.length, flux_h=flux_h,
                    flux_s=flux_s, flux_g=flux_g, force=force,
                    gain=(1-ps/(ph+ps+pg))/self.length)

    def limits(self, gap, write_ratio=0.):
        """Onset isolation and stipulated post-write full-remanence field.

        ratio=0 grants instantaneous full reversal at Hc. Positive ratios are
        competing constitutive assumptions, NOT fitted material predictions.
        """
        on, off = self.solve(gap, 1), self.solve(gap, -1)
        a = on['gain']
        half_set = (self.hc-off['hs'])/a
        half_reset = (self.hc+on['hs'])/a
        write_set = half_set if write_ratio == 0 else max(half_set, (write_ratio*self.hc-on['hs'])/a)
        write_reset = half_reset if write_ratio == 0 else max(half_reset, (write_ratio*self.hc+off['hs'])/a)
        return dict(half_set=half_set,half_reset=half_reset,
                    write_set=write_set,write_reset=write_reset,
                    safe_half=min(half_set, half_reset),
                    required_full=max(write_set, write_reset),
                    on_demag=-on['hs'], on_force=on['force'],
                    off_force=off['force'])


def window(circuits_and_gaps, write_ratio=0., current_error=0., parasite=0.):
    """Same amplitude for either sign; arbitrary cell state and gap.

    parasite is total extra half-site AT / nominal single-line AT.
    Selected fields each lose current_error; half site gains error+parasite.
    """
    lim = [c.limits(g, write_ratio) for c,g in circuits_and_gaps]
    lower = max(x['required_full'] for x in lim)/(2*(1-current_error))
    upper = min(x['safe_half'] for x in lim)/(1+current_error+parasite)
    # Also allow independently optimized signed amplitudes; do not reject a
    # circuit solely for an avoidable symmetric-driver restriction.
    signs={}
    for sign in ['set','reset']:
        lo=max(x['write_'+sign] for x in lim)/(2*(1-current_error))
        hi=min(x['half_'+sign] for x in lim)/(1+current_error+parasite)
        signs[sign]=dict(lower_AT=lo,upper_AT=hi,passes=lo<hi)
    return dict(lower_AT=lower, upper_AT=upper, passes=lower < upper,
                asymmetric=signs,asymmetric_passes=all(x['passes'] for x in signs.values()))


def relay(c, gap, state, excitation):
    """Optimistic nonaccumulating relay; reject unstable post-pulse states."""
    h = c.solve(gap, state, excitation)['hs']
    if state*h < -c.hc:
        state = -state
    if state*c.solve(gap, state, excitation)['hs'] < -c.hc:
        return None
    return state


def check():
    c = Circuit()
    for g,s,f in product([.00005,.0002,.001],[-1,1],[-300,0,300]):
        q=c.solve(g,s,f)
        assert abs(q['flux_h']+q['flux_s']-q['flux_g']) < 2e-21
        # Independent reluctance-loop equations, with magnet source MMFs.
        rh=c.length/(MU0*c.mu_hard*c.hard_area)
        rs=c.length/(MU0*c.mu_soft*c.soft_area)
        assert math.isclose(q['v']+rh*q['flux_h'],
                            c.br_hard*c.length/(MU0*c.mu_hard),rel_tol=1e-12)
        assert math.isclose(q['v']+rs*q['flux_s'],
                            s*c.br_soft*c.length/(MU0*c.mu_soft)+f,abs_tol=1e-10)
    assert c.solve(.0002,-1)['force']==0
    # Zero-field energy potential after eliminating circuit fluxes: S²/(2D).
    def potential(g):
        S=c.soft_area*c.br_soft+c.hard_area*c.br_hard
        D=MU0*((c.mu_soft*c.soft_area+c.mu_hard*c.hard_area)/c.length
               +c.pole_area/(2*g))
        return .5*S*S/D
    g=.0002; dx=1e-9
    derivative=(potential(g+dx)-potential(g-dx))/(2*dx)
    assert math.isclose(derivative,c.solve(g,1)['force'],rel_tol=1e-8)
    assert math.isclose(Circuit(soft_area=2e-6,hard_area=2e-6,pole_area=8e-6)
                        .solve(g,1)['force'],2*c.solve(g,1)['force'])
    assert c.solve(1e-10,1)['force']>c.solve(g,1)['force']
    assert abs(c.solve(1e6,1)['flux_g'])<1e-14
    # Exhaust all 3x3 initial states, selected rows, column masks and signs.
    # A valid pulse plus clearing to zero leaves every half site unchanged.
    g=.00005; w=window([(c,g)]); assert w['passes']
    f=(w['lower_AT']+w['upper_AT'])/2
    histories=0
    for bits in product([-1,1],repeat=9):
        for row,mask,sign in product(range(3),range(8),[-1,1]):
            for idx,s in enumerate(bits):
                r,k=divmod(idx,3)
                cols=(mask>>k)&1
                applied=sign*f*((r==row)+cols)
                out=relay(c,g,s,applied)
                expected=sign if r==row and cols else s
                assert out==expected
                assert relay(c,g,out,0)==expected
            histories+=1
    # Local two-state invariance above inductively covers any sequence of
    # transactions in this relay law, not physical minor-loop accumulation.
    # Concrete failed history: a valid SET also supplies a destructive RESET
    # half-pulse elsewhere when the same amplitude is used for both signs.
    assert relay(c,.0002,-1,280)==1
    assert relay(c,.0002,1,-140)==-1
    assert window([(c,.0002)])['asymmetric_passes']
    assert relay(c,.0002,1,-120)==-1
    assert relay(c,.0002,1,-60)==1
    assert relay(c,.0005,1,0)==-1
    assert relay(c,.0005,-1,0)==-1
    # Closed gap unbiased limit recovers write_ratio<2.
    assert window([(c,1e-12)],write_ratio=1.99)['passes']
    assert not window([(c,1e-12)],write_ratio=2.01)['passes']
    return dict(array_transactions=histories,force_energy_relative_error=
                abs(derivative/c.solve(gap=.0002,state=1)['force']-1))


def main():
    checks=check()
    c=Circuit()
    nominal=[]
    for length,gap in product([.005,.01,.02],[.00005,.0001,.0002,.0005,.001]):
        cc=replace(c,length=length)
        nominal.append(dict(length_mm=length*1000,gap_mm=gap*1000,
            **cc.limits(gap),window=window([(cc,gap)])))
    boxes=[]
    # Bounds, not distributions; shared batch plus differential part mismatch.
    # Endpoints are sensitivity scenarios, not certified global extrema.
    for length in [.005,.02]:
        for tag,e,brerr,hcerr,ie,par in [
            ('nominal',0,0,0,0,0),('tight',.00001,.03,.05,.03,.02),
            ('wide',.00005,.10,.15,.05,.05)]:
            cg=[]
            for gb,batch,diff,h,mus in product([-1,1],[-1,1],[-1,1],[-1,1],[3,4.5]):
                cc=replace(c,length=length,mu_soft=mus,
                           br_soft=c.br_soft*(1+batch*brerr+diff*brerr),
                           br_hard=c.br_hard*(1+batch*brerr-diff*brerr),
                           hc=c.hc*(1+h*hcerr))
                for g in [.0001,.0002]:
                    cg.append((cc,g+gb*e))
            for ratio in [0,1.5,2,240/51.7]:
                boxes.append(dict(length_mm=1000*length,scenario=tag,
                    write_ratio=ratio,corners=len(cg),
                    **window(cg,ratio,ie,par)))
    bias=[]
    for common in [-.00005,0,.00005]:
        bias.append(dict(common_gap_bias_um=common*1e6,
            **window([(c,g+common) for g in [.0001,.0002]])))
    timing=[]
    for step in [.5,1,2]:
        strokes=math.ceil(40/step)
        for banks in [1,4,8,16]:
            # Separate sign stages per displacement increment; set+reset each.
            row_transactions=4*strokes*math.ceil(80/banks)
            # 10 ms/stroke shared mechanics, 6 s preparation/proof/retry reserve.
            reserve=6+2*strokes*.01
            timing.append(dict(step_mm=step,banks=banks,
                row_transactions=row_transactions,
                row_transaction_ceiling_ms=1000*(30-reserve)/row_transactions))
    # Exact gap boundaries for matched magnet flux sources, relay law.
    def boundary(h):
        d=(c.mu_soft*c.soft_area+c.mu_hard*c.hard_area)/c.length
        return c.pole_area/(2*(2*c.br_soft*c.soft_area/(MU0*c.length*h)-d))
    critical=dict(selection_gap_mm=1000*boundary(c.hc/2),
                  remanence_gap_mm=1000*boundary(c.hc))
    # Optimistic frozen-remanence work over a 1-mm armature stroke. Actual
    # switch/erasure and spring losses can invalidate/reduce this allowance.
    def energy(g):
        S=c.br_soft*c.soft_area+c.br_hard*c.hard_area
        D=MU0*((c.mu_soft*c.soft_area+c.mu_hard*c.hard_area)/c.length
               +c.pole_area/(2*g))
        return .5*S*S/D
    work=energy(.00105)-energy(.00005)
    quadrature=[]
    for n in [64,256,1024]:
        dx=.001/n
        trap=dx*sum(c.solve(.00005+i*dx,1)['force']*
                    (.5 if i in [0,n] else 1) for i in range(n+1))
        quadrature.append(dict(intervals=n,relative_error=abs(trap/work-1)))
    print(json.dumps(dict(checks=checks,nominal=nominal,uncertainty_corners=boxes,
                         common_gap_bias=bias,timing=timing,critical=critical,
                         full_stroke_windows=[dict(length_mm=l*1000,
                             **window([(replace(c,length=l),g) for g in [.00005,.00105]]))
                             for l in [.005,.01,.02]],
                         frozen_stroke_work_mJ=work*1000,
                         work_quadrature=quadrature),indent=2))


if __name__=='__main__':
    main()
