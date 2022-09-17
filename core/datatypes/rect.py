from __future__ import annotations

from core.datatypes.point import Point


class Rect:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self) -> int:
        """ The X position of the top-left corner of the rectangle. """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        """ The Y position of the top-left corner of the rectangle. """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def width(self) -> int:
        """ The width of the rectangle. """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        """ The height of the rectangle. """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
    
    @property
    def top(self) -> int:
        """ The Y position of the top edge of the rectangle. """
        return self.y

    @property
    def bottom(self) -> int:
        """ The Y position of the bottom edge of the rectangle. """
        return self.y + self.height

    @property
    def left(self) -> int:
        """ The X position of the left edge of the rectangle. """
        return self.x

    @property
    def right(self) -> int:
        """ The X position of the right edge of the rectangle. """
        return self.x + self.width

    @property
    def location(self) -> Point:
        """ The X and Y position of the top-left corner of the rectangle. """
        return Point(self.x, self.y)

    @property
    def size(self) -> Point:
        """ The width and height of the rectangle. """
        return Point(self.width, self.height)

    def intersects(self, other: Rect) -> bool:
        """ Check if this rectangle intersects another. """
        return (
            other.left < self.right and
            self.left < other.right and
            other.top < self.bottom and
            self.top < other.bottom
        )

    @classmethod
    def empty(cls) -> Rect:
        """ Returns a rectangle with x=0, y=0, width=0, height=0. """
        return Rect(0, 0, 0, 0)
