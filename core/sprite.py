import sdl2.ext
import sdl2.render
import sdl2.sdlimage

from core.content import Content
from core.engine import Engine
from core.datatypes.pivot import Pivot
from core.datatypes.point import Point


class Sprite:
    def __init__(self, content_path: str) -> None:
        self._engine = Engine.instance()
        self._texture = Content.load_texture(content_path)
        self._width = self._texture.size[0]
        self._height = self._texture.size[1]
        self._pivot = Pivot()

    @property
    def width(self) -> int:
        """ The width of the sprite. """
        return self._width

    @property
    def height(self) -> int:
        """ The height of the sprite. """
        return self._height

    @property
    def pivot(self) -> Pivot:
        """ The pivot point for the sprite. """
        return self._pivot

    def draw(self, position: Point) -> None:
        """ Draw the sprite at a given position. """
        pivot_offset = Point(self.pivot.x * self.width, self.pivot.y * self.height)
        draw_position = position - pivot_offset
        self._engine.renderer.copy(
            src=self._texture,
            srcrect=None,
            dstrect=draw_position.to_tuple(),
            angle=0,
            center=None,
            flip=sdl2.render.SDL_FLIP_NONE
        )
