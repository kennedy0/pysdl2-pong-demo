from __future__ import annotations

import sdl2
import sdl2.ext
import sdl2.render
import sdl2.timer
import sdl2.video
from typing import Optional, TYPE_CHECKING

from core.input import Input
from core.time import Time
from core.utilities import time_utils

if TYPE_CHECKING:
    from core.scene import Scene


TIMESTEP = 1 / 60


class Engine:
    __instance = None

    def __new__(cls, *args, **kwargs) -> Engine:
        if cls.__instance is None:
            cls.__instance = super(Engine, cls).__new__(cls)
        return cls.__instance

    def __init__(self, window: sdl2.ext.Window, renderer: sdl2.ext.Renderer) -> None:
        # Main window
        self._window = window

        # Rendering context
        self._renderer = renderer

        # Tracks whether or not the event loop is running
        self._running = False

        # Time
        self._last_tick_time = 0
        self._accumulator = 0

        # Fps
        self._fps = 0
        self._frame_counter = 0
        self._fps_timer = 0

        # Scene
        self._scene = None
        self._next_scene = None

    @classmethod
    def instance(cls) -> Optional[Engine]:
        return cls.__instance

    @property
    def window(self) -> sdl2.ext.Window:
        """ The main window for the application. """
        return self._window

    @property
    def renderer(self) -> sdl2.ext.Renderer:
        """ The rendering context for the window. """
        return self._renderer

    @property
    def scene(self) -> Optional[Scene]:
        """ The current scene. """
        return self._scene

    @scene.setter
    def scene(self, value: Scene) -> None:
        self._next_scene = value

    def run(self, first_scene: Scene) -> None:
        """ Runs the main event loop for the core. """
        # Load the first scene
        self.scene = first_scene

        # Show the window
        self.window.show()

        # Main event loop
        self._running = True
        while self._running:
            # Calculate time delta
            tick = sdl2.timer.SDL_GetTicks64()
            delta_ms = tick - self._last_tick_time
            delta = time_utils.snap_delta(delta_ms / 1000.0)
            self._last_tick_time = tick

            # Increment the fps timer and delta time accumulator
            self._fps_timer += delta
            self._accumulator += delta

            # Update at fixed time step
            while self._accumulator > TIMESTEP:
                Time.update(TIMESTEP)
                self._frame_counter += 1
                self._accumulator -= TIMESTEP
                self.update()
                self.draw()

            self.update_fps()

    def update(self) -> None:
        """ Main update loop. """
        # Handle events
        self.handle_events()

        # Update scene
        if self.scene:
            self.scene.update()

        # Transition scene
        if self._scene != self._next_scene:
            self.transition_scene()

    def handle_events(self) -> None:
        """ Handle SDL events. """
        for event in sdl2.ext.get_events():
            match event.type:
                case sdl2.SDL_QUIT:
                    self._running = False
                case sdl2.SDL_KEYDOWN | sdl2.SDL_KEYUP:
                    Input.update(event)

    def transition_scene(self) -> None:
        """ Called after a scene ends, before the next scene starts. """
        if self.scene:
            self.scene.end()

        self._scene = self._next_scene

        if self.scene:
            self.scene.load_entities()
            self.scene.entities.update_list()
            self.scene.start(self)

    def draw(self) -> None:
        """ Main draw loop. """
        # Clear screen
        self.renderer.clear(sdl2.ext.Color(0, 0, 0))

        # Draw scene
        if self.scene:
            self.scene.draw()

        # Render to screen
        self.renderer.present()

    def update_fps(self) -> None:
        """ Update the fps. """
        if self._fps_timer >= 1.0:
            self._fps = self._frame_counter
            self._frame_counter = 0
            self._fps_timer -= 1.0
            self.window.title = f"Pong [ {self._fps} fps ]"
