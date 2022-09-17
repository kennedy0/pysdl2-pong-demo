import sdl2.ext

from core.datatypes.point import Point
from core.entity import Entity
from core.text import Text
from pong import constants


class Score(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.player_1_score = 0
        self.player_2_score = 0
        self.player_1_score_text = Text("m5x7.ttf", 32, sdl2.ext.Color(255, 253, 242))
        self.player_2_score_text = Text("m5x7.ttf", 32, sdl2.ext.Color(255, 253, 242))
        self.score_spacing = 32

    def initialize(self) -> None:
        self.x = constants.SCREEN_WIDTH / 2
        self.y = 8

        self.player_1_score_text.pivot.set_center_right()
        self.player_2_score_text.pivot.set_center_left()

    def start(self) -> None:
        self.set_player_1_score(0)
        self.set_player_2_score(0)

    def set_player_1_score(self, score: int) -> None:
        self.player_1_score = score
        self.player_1_score_text.text = self.player_1_score

    def set_player_2_score(self, score: int) -> None:
        self.player_2_score = score
        self.player_2_score_text.text = self.player_2_score

    def increase_player_1_score(self):
        self.set_player_1_score(self.player_1_score + 1)

    def increase_player_2_score(self):
        self.set_player_2_score(self.player_2_score + 1)

    def draw(self) -> None:
        pos_1 = Point(self.position.x - self.score_spacing / 2, self.position.y)
        pos_2 = Point(self.position.x + self.score_spacing / 2 + 1, self.position.y)
        self.player_1_score_text.draw(pos_1)
        self.player_2_score_text.draw(pos_2)
