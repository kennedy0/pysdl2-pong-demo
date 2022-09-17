from core.scene import Scene

from pong.entities.bg import Bg
from pong.entities.ball import Ball
from pong.entities.computer_paddle import ComputerPaddle
from pong.entities.game_manager import GameManager
from pong.entities.player_paddle import PlayerPaddle
from pong.entities.score import Score


class GameScene(Scene):
    def load_entities(self) -> None:
        game_manager = GameManager()
        self.entities.add(game_manager)

        bg = Bg()
        bg.name = "Background"
        self.entities.add(bg)

        score = Score()
        score.name = "Score"
        self.entities.add(score)

        ball = Ball()
        ball.name = "Ball"
        self.entities.add(ball)

        player = PlayerPaddle()
        player.name = "Player"
        player.add_tag("paddle")
        self.entities.add(player)

        computer = ComputerPaddle()
        computer.name = "Computer"
        computer.add_tag("paddle")
        self.entities.add(computer)
