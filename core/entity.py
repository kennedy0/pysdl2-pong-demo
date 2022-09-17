from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from core.datatypes.pivot import Pivot
from core.datatypes.point import Point
from core.datatypes.rect import Rect

from core.engine import Engine
if TYPE_CHECKING:
    from core.scene import Scene


class Entity:
    def __init__(self) -> None:
        self._name = None
        self._tags = set()
        self._scene = None

        # Position
        self._x = 0
        self._y = 0

        # Collision
        self._width = 0
        self._height = 0
        self._pivot = Pivot()

    @property
    def name(self) -> str:
        """ The name of this entity. """
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def scene(self) -> Optional[Scene]:
        """ The scene that this entity belongs to. """
        return self._scene

    @scene.setter
    def scene(self, value: Optional[Scene]) -> None:
        self._scene = value

    @property
    def x(self) -> int:
        """ The X position of this entity. """
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        """ The Y position of this entity. """
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def position(self) -> Point:
        return Point(self.x, self.y)

    @property
    def width(self) -> int:
        """ The width of the bounding box. """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        """ The height of the bounding box. """
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def pivot(self) -> Pivot:
        """ The pivot point of the bounding box. """
        return self._pivot

    @property
    def bbox(self) -> Rect:
        """ The bounding box for this entity. """
        return self.bbox_at(self.x, self.y)

    def bbox_at(self, x: int, y: int) -> Rect:
        """ Return a copy of this entity's bounding box at a given position. """
        return Rect(
            x - int(self.pivot.x * self.width),
            y - int(self.pivot.y * self.height),
            self.width,
            self.height
        )

    def has_tag(self, tag: str) -> bool:
        """ Check if a tag is on this entity. """
        return tag in self._tags

    def add_tag(self, tag: str) -> None:
        """ Add a tag to this entity. """
        self._tags.add(tag)

    def initialize(self) -> None:
        """ Called after this entity is created.
        Use this to initialize values, and set up references between entities.
        """
        pass

    def start(self) -> None:
        """ This runs after initialize, just before the first update.
        Use this to pass information back and forth between entities.
        """
        pass

    def update(self) -> None:
        """ Update loop. """
        pass

    def after_update(self) -> None:
        """ Called immediately after update. """
        pass

    def draw(self) -> None:
        """ Draw loop. """
        pass

    def on_collide(self, other: Entity) -> None:
        """ Called when this entity collides with another entity. """
        pass

    @classmethod
    def find(cls, entity_name: str) -> Optional[Entity]:
        """ Find an entity in the current scene. """
        engine = Engine.instance()
        for entity in engine.scene.entities:
            if entity.name == entity_name:
                return entity
