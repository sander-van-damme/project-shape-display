"""Same limits as the retained Uno trial; all positions are commanded steps."""
import math
FULL_STEPS = 20  # provisional: verify one actual revolution BEFORE fitting pin
MICROSTEPS = 8
STEPS_PER_REV = FULL_STEPS * MICROSTEPS
PIN_LIMIT = STEPS_PER_REV // 2
IDLE_MS = 30000
MAX_RUN_MS = 120000


def plan_move(pin_mode, position, revs):
    if not math.isfinite(revs) or abs(revs) > 1:
        raise ValueError('distance must be finite and <= 1 revolution')
    value = revs * STEPS_PER_REV
    steps = int(value + .5) if value >= 0 else int(value - .5)
    if not steps or (pin_mode and abs(position + steps) > PIN_LIMIT):
        raise ValueError('zero distance or PIN limit +/-0.5 revolution')
    return steps


def speed(value):
    if not math.isfinite(value) or not 2 <= value <= 120:
        raise ValueError('speed 2..120 rpm')
    return value


def cycles(value):
    if not math.isfinite(value) or not 1 <= value <= 20 or value != int(value):
        raise ValueError('cycles must be integer 1..20')
    return int(value)
