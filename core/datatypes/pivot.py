class Pivot:
    """ A data type that represents a pivot point inside a rectangle.
    0    X    1
    +----+----+  0
    |    |    |
    +----+----+  Y
    |    |    |
    +----+----+  1
    """
    def __init__(self) -> None:
        self._x = 0
        self._y = 0

    @property
    def x(self) -> float:
        """ The X value for the pivot. """
        return self._x

    @property
    def y(self) -> float:
        """ The Y value for the pivot. """
        return self._y

    def set(self, x: float, y: float) -> None:
        """ Set the pivot point.
        Range for X and Y are 0-1.
        """
        if x < 0 or x > 1 or y < 0 or y > 1:
            raise RuntimeError(f"Pivot point values must be in range 0 to 1.")
        self._x = x
        self._y = y

    def set_center_left(self) -> None:
        self.set(0, .5)

    def set_center(self) -> None:
        self.set(.5, .5)

    def set_center_right(self) -> None:
        self.set(1, .5)
