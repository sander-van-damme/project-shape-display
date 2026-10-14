#!/usr/bin/env python3
"""Bounded assembly observations and operation ledger; no hardware/yield claims."""
from itertools import product
from math import ceil, isclose

LEAD = 3.0
# Required measurement/process bounds, not measured printer or sensor accuracy.
LEAD_ERROR, GAIN_ERROR, READ_ERROR, LOST_MOTION = .06, .002, .1, .3


def band(turns):
    return ((LEAD-LEAD_ERROR)*turns*(1-GAIN_ERROR)-2*READ_ERROR-LOST_MOTION*(1+GAIN_ERROR),
            (LEAD+LEAD_ERROR)*turns*(1+GAIN_ERROR)+2*READ_ERROR+LOST_MOTION*(1+GAIN_ERROR))


def trace(lead, gain=0, bias=0, noise=0, lost=0):
    # Direct screw-collar displacement relative to fixed nut; same batch bias
    # cancels within each segment. No commanded Z is substituted for observation.
    result = []
    for turns in (2, 16, -2, 2):
        a = bias - noise
        b = bias + (lead*turns + lost)*(1+gain) + noise
        result.append(abs(b-a))
    return result


def accepts(samples, torque=.7, read_ok=True):
    return read_ok and torque <= 1.5 and all(
        lo-1e-9 <= z <= hi+1e-9
        for z, (lo, hi) in zip(samples, (band(t) for t in (2,16,2,2))))


def check():
    good = list(product((2.94,3,3.06),(-.002,0,.002),(-.15,0,.15),(-.1,0,.1),(-.3,0,.3)))
    for p,g,b,e,l in good:
        assert accepts(trace(p,g,b,e,l))
    jam = trace(.5)
    wrong_lead = trace(2.7)
    damaged_same_lead = trace(3)
    assert not accepts(jam)
    assert band(2)[0] <= wrong_lead[0] <= band(2)[1]
    assert not accepts(wrong_lead)
    assert accepts(damaged_same_lead)  # decisive indistinguishable fault witness
    assert not accepts(trace(3), torque=1.6)
    assert not accepts(trace(3), read_ok=False)
    # An imposed Z feed could generate the good trace with a stripped thread.
    assert accepts(trace(3))
    turns = (64-2)/3
    assert isclose(turns*3,62)
    auto = (turns+4)/2 + 7  #120rpm, reverse proof, seek/dock/read/retract allowance
    print('good corners',len(good),'bands',band(2),band(16))
    print('faults: jam rejected; lead2.7 rejected; same-lead damage ACCEPTED')
    print('insertion turns',turns,'automatic cycle seconds',auto)
    for n in (1024,6400):
        print('N',n,'nominal manual touches',5*n,'fixture touches',4*n)
        for y in (1,.8):
            attempts=ceil(n/y); rejects=attempts-n
            for label,thread in (('manual-fast',5),('manual-mid',15),('manual-slow',30),('fixture',None)):
                extra_setup=4 if thread is None else 0
                hands=10 if thread is None else 9+thread+4
                assembly=extra_setup+(attempts*hands+rejects*60)/3600
                serial=extra_setup+(attempts*(hands+(auto if thread is None else 0))+rejects*60)/3600
                # Common manufacturing handling, install, frame/electrical setup,
                # four channels and two assumed 289-up production streams.
                low=8+4/6+(attempts*20+n*8)/3600+2*ceil(attempts/289)*5/60
                high=16+4*.5+(attempts*60+n*20)/3600+2*ceil(attempts/289)*5/60
                print(y,label,'assembly_h',round(assembly,2),'serial_h',round(serial,2),
                      'whole_maker_h',[round(low+assembly,2),round(high+assembly,2)])
        print('threading break-even seconds',10+4*3600/n-13)
    # Intervals, not prevalence: identical observations defeat every deterministic
    # classifier operating on these channels, irrespective of a timing improvement.
    assert trace(3) == damaged_same_lead

if __name__ == '__main__':
    check()
