"""Deterministic necessary bounds; SI internally, no calibrated fluid/process prior."""
import math


def bounds(d_mm, k_mpa, dead_mm3, dp_mpa, force=10, height_mm=40):
    area = math.pi * (d_mm * 1e-3)**2 / 4
    bulk = k_mpa * 1e6
    dead = dead_mm3 * 1e-9
    dp = dp_mpa * 1e6
    # Constant-load piston; intermediate compliance releases volume C_i delta-p.
    jump = dead * dp / bulk / area
    # Incremental force on sealed full-stroke chamber, rigid walls.
    sag = force * height_mm * 1e-3 / (bulk * area)
    return area, jump, sag


def main():
    n = 0
    for d in (2, 3, 4):
        for k in (10, 100, 1000):
            for dead in (1, 10, 100):
                for dp in (.1, 1):
                    a, jump, sag = bounds(d, k, dead, dp)
                    assert math.isclose(a * jump, dead * 1e-9 * dp / k)
                    assert math.isclose(sag * k * 1e6 * a / .04, 10)
                    assert math.isclose(bounds(d,k*2,dead,dp)[1], jump/2)
                    assert math.isclose(bounds(d,k,dead*2,dp)[1], jump*2)
                    n += 1
    a, jump, sag = bounds(3,100,10,1)
    assert bounds(3,100,0,1)[1] == 0
    assert bounds(3,100,10,0)[1] == 0
    assert math.isclose(bounds(3,100,10,-1)[1], -jump)
    print(f'{n} bounded cases; conservation, limits, sign and scaling pass')
    print('3-mm bore, 10-mm3 intermediate, 1-MPa pressure difference:')
    for k in (10,100,1000):
        a,j,s=bounds(3,k,10,1)
        print(f'K={k} MPa: one pulse={j*1e3:.6f} mm, 80 refreshed pulses={80*j*1e3:.6f} mm, 10-N sag={s*1e3:.6f} mm')
    budget_m=.1e-3  # illustrative diagnostic, not a requirement
    allowed_dead=budget_m*a*100e6/(80*1e6)
    leak=budget_m*a/(4*3600)
    volume=6400*a*.04
    print(f'80-pulse 0.1-mm budget: dead volume <= {allowed_dead*1e9:.6f} mm3 at K=100 MPa')
    print(f'4-hour 0.1-mm drift: leak <= {leak*1e12:.6f} nL/s per cell')
    assert math.isclose(volume/30*6e4, (volume*1e3)/.5)
    print(f'Full-board stroke fluid={volume*1e6:.6f} mL; under-30-s flow > {volume/30*6e4:.6f} L/min')
    print(f'10-N chamber pressure={10/a/1e6:.6f} MPa; 6400 lifts at 10 N need {6400*10*.04/30:.6f} W ideal average')


if __name__ == '__main__':
    main()
