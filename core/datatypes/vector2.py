from __future__ import annotations

from copy import deepcopy
from math import cos, sin, radians, sqrt


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    def __str__(self) -> str:
        return f"Vector2({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

    def __iter__(self):
        return iter(self.to_tuple())

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vector2 | float) -> Vector2:
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other: Vector2 | float) -> Vector2:
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    @property
    def length(self) -> float:
        """ The length of this vector. """
        return sqrt(self.x * self.x + self.y * self.y)

    @property
    def normalized(self) -> Vector2:
        """ Return a normalized copy of this vector. """
        v = self.copy()
        v.normalize()
        return v

    def to_tuple(self) -> tuple[float, float]:
        """ Return a copy of this vector as a tuple. """
        return self.x, self.y

    def copy(self) -> Vector2:
        """ Return a copy of this vector. """
        return deepcopy(self)

    def normalize(self) -> None:
        """ Normalize this vector. """
        if self.length == 0:
            self.x = 0
            self.y = 0
        else:
            scale = 1 / self.length
            self.x *= scale
            self.y *= scale

    def rotate(self, angle: float) -> None:
        """ Rotate this vector clockwise. """
        x = self.x * cos(radians(angle)) - self.y * sin(radians(angle))
        y = self.x * sin(radians(angle)) + self.y * cos(radians(angle))
        self.x = x
        self.y = y

    @staticmethod
    def zero() -> Vector2:
        return Vector2(0, 0)

    @staticmethod
    def one() -> Vector2:
        return Vector2(1, 1)

    @staticmethod
    def up() -> Vector2:
        return Vector2(0, -1)

    @staticmethod
    def down() -> Vector2:
        return Vector2(0, 1)

    @staticmethod
    def left() -> Vector2:
        return Vector2(-1, 0)

    @staticmethod
    def right() -> Vector2:
        return Vector2(1, 0)
