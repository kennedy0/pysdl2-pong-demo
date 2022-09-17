from pathlib import Path

import sdl2.ext
import sdl2.sdlmixer
from PIL import Image

from core.engine import Engine


CONTENT_ROOT = Path(__file__).parent.parent / "content"


class Content:
    __loaded_content = dict()

    @classmethod
    def full_content_path(cls, content_path: str) -> Path:
        """ Returns the full path to the content. """
        full_path = CONTENT_ROOT / content_path
        if not full_path.exists():
            raise FileNotFoundError(f"{full_path.as_posix()} does not exist")
        return full_path

    @classmethod
    def load_texture(cls, content_path: str) -> sdl2.ext.Texture:
        if content_path not in cls.__loaded_content:
            # Load image
            image_file = cls.full_content_path(content_path)

            # Convert from PIL Image to SDL surface
            image = Image.open(image_file).convert("RGBA")
            surface = sdl2.ext.pillow_to_surface(image)

            # Create texture
            engine = Engine.instance()
            renderer = engine.renderer.sdlrenderer
            texture = sdl2.ext.Texture(renderer, surface)

            # Cache content
            cls.__loaded_content[content_path] = texture

        return cls.__loaded_content[content_path]

    @classmethod
    def load_font(cls, content_path: str, size: int, color: sdl2.ext.Color) -> sdl2.ext.ttf.FontTTF:
        key = f"{content_path}.{size}.{color.r}.{color.g}.{color.b}.{color.a}"
        if key not in cls.__loaded_content:
            font_file = cls.full_content_path(content_path)
            cls.__loaded_content[key] = sdl2.ext.ttf.FontTTF(font_file.as_posix(), size, color)

        return cls.__loaded_content[key]

    @classmethod
    def load_audio(cls, content_path: str):
        if content_path not in cls.__loaded_content:
            audio_file = cls.full_content_path(content_path)
            audio = sdl2.sdlmixer.Mix_LoadWAV(audio_file.as_posix().encode("utf-8"))
            cls.__loaded_content[content_path] = audio

        return cls.__loaded_content[content_path]
