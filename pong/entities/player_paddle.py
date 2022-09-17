import sdl2

from core.input import Input
from core.sprite import Sprite
from pong.entities.paddle import Paddle


class PlayerPaddle(Paddle):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite("player_green.png")
        self.sprite.pivot.set_center()

    def initialize(self) -> None:
        self.x = 20
        self.y = 90

    def update(self) -> None:
        self.handle_input()

    def handle_input(self) -> None:
        if Input.get_key(sdl2.SDLK_UP):
            self.move_y(-self.move_speed)
        if Input.get_key(sdl2.SDLK_DOWN):
            self.move_y(self.move_speed)
