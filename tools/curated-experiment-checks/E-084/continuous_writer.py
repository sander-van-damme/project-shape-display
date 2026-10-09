"""Initial continuous-writer necessary bounds; no finite coupler or hardware claim.
Explicit assumptions: 3440 full-row transactions, 24s transport/programming
allocation, 5.08mm pitch, independent equal banks, no turnarounds or speed cap.
"""
import json
import math


def screen(banks, width_mm, gate_accel, proof_s=0.):
    period=24*banks/3440
    speed=.00508/period
    contact=width_mm/1000/speed
    gate_time=2*math.sqrt(.0012/gate_accel)
    # Independent alternating lanes may change outside their own contact window.
    # A single shared setter must still produce one word per period.
    lanes=math.floor((gate_time+proof_s+contact)/period)+1
    dog_d=.0012
    return dict(banks=banks,contact_width_mm=width_mm,gate_accel=gate_accel,
        proof_ms=proof_s*1000,period_ms=period*1000,speed_m_s=speed,
        contact_ms=contact*1000,gate_ms=gate_time*1000,
        independent_lanes=lanes,independent_gate_drives=80*banks*lanes,
        shared_setter_throughput_pass=gate_time+proof_s<period,
        # Cycloid x=d*(u-sin(2*pi*u)/(2*pi)), 0<=u<=1.
        cam_peak_accel_m_s2=2*math.pi*dog_d/contact**2,
        cam_peak_slope=2*1.2/width_mm,
        cam_average_feed_force_per_selected_N=.3*1.2/width_mm)


def checks():
    # Independent integral identities for cycloid displacement and energy.
    # Trapezoid numerical integration of dx/du over unit duration.
    errors=[]
    for n in (100,200,400):
        d=.0012
        slopes=[d*(1-math.cos(2*math.pi*i/n)) for i in range(n+1)]
        integral=(sum(slopes)-.5*(slopes[0]+slopes[-1]))/n
        errors.append(abs(integral-d))
        assert math.isclose(integral,d,abs_tol=1e-14)
    x=screen(1,2.,20.)
    y=screen(2,2.,20.)
    assert math.isclose(y['period_ms'],2*x['period_ms'])
    assert math.isclose(y['cam_peak_accel_m_s2'],x['cam_peak_accel_m_s2']/4)
    assert not x['shared_setter_throughput_pass']
    assert screen(4,2.,20.)['shared_setter_throughput_pass']
    # Buffering cannot turn insufficient average production into a sustained pass.
    assert math.floor(24/(x['gate_ms']/1000)) < 3440
    assert x['independent_lanes']==3
    return dict(cycloid_integral_errors_m=errors,shared_setter_negative_control='pass')


if __name__=='__main__':
    print(json.dumps(dict(checks=checks(),scenarios=[screen(b,w,a,p)
        for b in (1,2,4,8) for w in (1.,2.,4.) for a in (20.,100.) for p in (0.,.001)]),indent=2))
