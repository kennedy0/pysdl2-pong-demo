import sdl2.video
import sdl2.ext

from core.engine import Engine
from pong import constants
from pong.scenes.game_scene import GameScene


def run() -> None:
    # Create engine
    window = create_window("Pong", 1280, 720)
    renderer = create_renderer(window, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    engine = Engine(window, renderer)

    # Start game
    first_scene = GameScene()
    engine.run(first_scene)


def create_window(title: str, width: int, height: int) -> sdl2.ext.Window:
    """ Create a window. """
    flags = 0
    flags |= sdl2.video.SDL_WINDOW_HIDDEN
    flags |= sdl2.video.SDL_WINDOW_RESIZABLE

    window = sdl2.ext.Window(title, size=(width, height), flags=flags)
    return window


def create_renderer(window: sdl2.ext.Window, virtual_width: int, virtual_height: int) -> sdl2.ext.Renderer:
    """ Create a renderer. """
    flags = 0
    flags |= sdl2.render.SDL_RENDERER_ACCELERATED
    flags |= sdl2.render.SDL_RENDERER_PRESENTVSYNC

    renderer = sdl2.ext.Renderer(window, logical_size=(virtual_width, virtual_height), flags=flags)
    return renderer
