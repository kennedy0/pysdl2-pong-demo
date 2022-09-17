from __future__ import annotations


class Time:
    # Time since the last frame, scaled by the time scale (in seconds)
    delta_time = 0.0

    # Real time since the last frame (in seconds)
    real_delta_time = 0.0

    # This controls the rate that time passes
    time_scale = 1.0

    @classmethod
    def update(cls, delta: float) -> None:
        """ Update the time. """
        cls.real_delta_time = delta
        cls.delta_time = delta * cls.time_scale
