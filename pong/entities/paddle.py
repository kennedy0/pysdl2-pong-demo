from core.actor import Actor
from core.sprite import Sprite
from pong import constants


class Paddle(Actor):
    def __init__(self) -> None:
        super().__init__()

        self.width = 4
        self.height = 24
        self.pivot.set_center()

        self.sprite = Sprite("player_red.png")
        self.sprite.pivot.set_center()

        self.move_speed = 2

    def after_update(self) -> None:
        self.keep_in_bounds()

    def keep_in_bounds(self) -> None:
        """ Force the paddle to stay in bounds of the screen. """
        while self.bbox.top < 0:
            self.y += 1
        while self.bbox.bottom > constants.SCREEN_HEIGHT:
            self.y -= 1

    def draw(self) -> None:
        self.sprite.draw(self.position)
