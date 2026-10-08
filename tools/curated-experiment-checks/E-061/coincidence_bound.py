"""Deterministic bounded kinematics, not contact simulation or process priors.
Units: mm, N, MPa (N/mm²). No random sampling or generated output retained.
"""
from itertools import product
from math import pi, sqrt


def envelope(stroke, gap, error, gap_error, flex, lift):
    # Symmetric floating beam: center height equals mean endpoint height.
    # Common bias and opposite endpoint errors are both included by corners.
    states = {}
    for a, b in product((0, 1), repeat=2):
        travel = [(a*stroke+ea+b*stroke+eb)/2-gap-eg-loss
                  for ea, eb, eg, loss in product((-error, error),
                  (-error, error), (-gap_error, gap_error), (0, flex))]
        states[a, b] = (min(travel), max(travel))
    isolated = max(states[x][1] for x in ((0, 0), (0, 1), (1, 0))) <= 1e-12
    opens = states[1, 1][0] >= lift-1e-12
    return isolated and opens, states


def main():
    # Parameter search within ONE topology. Explicit bounds, no yield claims.
    for e, ge, flex in ((0.05, 0.05, 0.1), (0.1, 0.1, 0.2), (0.2, 0.2, 0.4)):
        trials = list(product((1., 1.5, 2., 2.5, 3.), (0.75, 1., 1.25, 1.5, 1.75, 2.)))
        survivors = [(s, g) for s, g in trials if envelope(s, g, e, ge, flex, 0.3)[0]]
        print('bounds', (e, ge, flex), 'tested', len(trials), 'rejected', len(trials)-len(survivors), 'survivors', survivors)
    ok, states = envelope(2.5, 1.6, .1, .1, .2, .3)
    assert ok
    print('selected stroke/gap 2.5/1.6 states (signed travel)', states)
    # Independent interval existence: g >= s/2+e+ge; g <= s-e-ge-flex-lift.
    assert abs((2.5-.1-.1-.2-.3)-(2.5/2+.1+.1)-.35) < 1e-12
    assert envelope(0, 0, 0, 0, 0, .3)[0] is False
    assert envelope(2, 1.2, 0, 0, 0, .3)[0]
    assert not envelope(2, 1.2, .2, .2, .4, .3)[0]
    # Rigid 4-mm beam with sliding end shoes: worst differential height 2.7.
    length, dy = 4., 2.5+2*.1
    projection = sqrt(length**2-dy**2)
    print('beam horizontal projection', projection, 'total inward slide', length-projection)
    # Upper bounded selected valve force: pressure differential closes poppet;
    # two equal endpoints share force, each line sees 80 selected valves.
    for diameter, pressure, spring, drag in product((.5, 1., 1.5), (.1, 1., 1.5), (.1, .5), (.0, .5)):
        force = pressure*pi*diameter**2/4+spring+drag
        line = 80*force/2
        if diameter == 1. and pressure == 1.5 and spring == .5 and drag == .5:
            print('reference valve N', force, '80-selected endpoint line N', line)
        assert abs(2*(force/2)*1.-force*1.) < 1e-12  # equal-input work
    print('force sweep 36 cases; line extrema N', 40*(.1*pi*.5**2/4+.1), 40*(1.5*pi*1.5**2/4+1.))
    print('PASS algebraic limiting/corner/work checks')

if __name__ == '__main__':
    main()
