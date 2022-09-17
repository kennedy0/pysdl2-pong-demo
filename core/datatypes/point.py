from __future__ import annotations

from copy import deepcopy


class Point:
    def __init__(self, x: float, y: float) -> None:
        self._x = int(x)
        self._y = int(y)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = int(value)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = int(value)

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter(self.to_tuple())

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Point | float) -> Point:
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return Point(self.x * other, self.y * other)

    def __truediv__(self, other: Point | float) -> Point:
        if isinstance(other, Point):
            return Point(self.x / other.x, self.y / other.y)
        else:
            return Point(self.x / other, self.y / other)

    def copy(self) -> Point:
        """ Return a copy of this point. """
        return deepcopy(self)

    def to_tuple(self) -> tuple[int, int]:
        """ Return a copy of this point as a tuple. """
        return self.x, self.y

    @staticmethod
    def zero() -> Point:
        return Point(0, 0)

    @staticmethod
    def one() -> Point:
        return Point(1, 1)

    @staticmethod
    def up() -> Point:
        return Point(0, -1)

    @staticmethod
    def down() -> Point:
        return Point(0, 1)

    @staticmethod
    def left() -> Point:
        return Point(-1, 0)

    @staticmethod
    def right() -> Point:
        return Point(1, 0)
