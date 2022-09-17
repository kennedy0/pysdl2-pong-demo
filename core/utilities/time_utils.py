TIMESTEP_30FPS = 1 / 30
TIMESTEP_60FPS = 1 / 60
TIMESTEP_120FPS = 1 / 120
TIME_SNAP_EPSILON = .0002


def snap_delta(delta: float) -> float:
    """ Snap the delta time to known refresh rates if it's very close.
    https://medium.com/@tglaiel/how-to-make-your-game-run-at-60fps-24c61210fe75
    """
    if abs(delta - TIMESTEP_120FPS) < TIME_SNAP_EPSILON:
        delta = TIMESTEP_120FPS
    elif abs(delta - TIMESTEP_60FPS) < TIME_SNAP_EPSILON:
        delta = TIMESTEP_60FPS
    elif abs(delta - TIMESTEP_30FPS) < TIME_SNAP_EPSILON:
        delta = TIMESTEP_30FPS

    return delta
