def sign(n: float) -> int:
    """ Return the sign of a number. """
    if n < 0:
        return -1
    else:
        return 1


def round_to_int(n: float) -> int:
    """ Round a float to an int. """
    return int(round(n))


def clamp(value: float, min_value: float, max_value: float) -> float:
    """ Returns the value clamped to the inclusive range of min and max. """
    return max(min_value, min(value, max_value))


def remap(value: float, old_min: float, old_max: float, new_min: float, new_max: float) -> float:
    """ Remaps a number from one range to another. """
    if old_min == old_max:
        return new_min

    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min


def snap_to_interval(value: float, interval: int) -> int:
    """ Snap a number to the nearest interval. """
    return round_to_int(value / float(interval)) * interval
