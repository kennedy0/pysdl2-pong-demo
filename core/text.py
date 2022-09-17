from typing import Optional

import sdl2.ext
import sdl2.render
import sdl2.sdlimage

from core.content import Content
from core.engine import Engine
from core.datatypes.pivot import Pivot
from core.datatypes.point import Point


class Text:
    def __init__(self, font_content_path: str, font_size: int, font_color: sdl2.ext.Color) -> None:
        self._engine = Engine.instance()
        self._font = Content.load_font(font_content_path, font_size, font_color)
        self._text = ""
        self._texture = None
        self._pivot = Pivot()

    @property
    def text(self) -> str:
        """ The text to be rendered. """
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if not isinstance(value, str):
            value = str(value)
        self._text = value
        self._update_texture()

    @property
    def width(self) -> int:
        """ The width of the rendered text. """
        if self._texture:
            return self._texture.size[0]
        else:
            return 0

    @property
    def height(self) -> int:
        """ The height of the rendered text. """
        if self._texture:
            return self._texture.size[1]
        else:
            return 0

    @property
    def pivot(self) -> Pivot:
        """ The pivot point for the text. """
        return self._pivot

    def draw(self, position: Point) -> None:
        """ Draw the sprite at a given position. """
        if self._texture:
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

    def _update_texture(self) -> None:
        """ Update the texture when the text changes. """
        engine = Engine.instance()
        renderer = engine.renderer.sdlrenderer
        surface = self._font.render_text(self.text)
        self._texture = sdl2.ext.Texture(renderer, surface)
