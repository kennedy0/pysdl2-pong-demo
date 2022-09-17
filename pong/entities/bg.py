from core.entity import Entity
from core.sprite import Sprite


class Bg(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.sprite = Sprite("bg.png")

    def draw(self) -> None:
        self.sprite.draw(self.position)
