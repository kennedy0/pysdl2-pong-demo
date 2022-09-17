from enum import Enum

from core.entity import Entity
from core.time import Time


class GameState(Enum):
    WAITING = 0
    PLAYING = 1
    SCORED = 3


class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.state = GameState.WAITING
        self.ball = None
        self.score = None
        self.wait_timer = 0
        self.wait_timer_max = 3

    def initialize(self) -> None:
        self.ball = Entity.find("Ball")

    def start(self) -> None:
        self.reset_state()

    def update(self) -> None:
        match self.state:
            case GameState.WAITING:
                self.handle_waiting_state()
            case GameState.PLAYING:
                self.handle_playing_state()
            case GameState.SCORED:
                self.handle_scored_state()

    def reset_state(self):
        self.state = GameState.WAITING
        self.wait_timer = self.wait_timer_max

    def handle_waiting_state(self):
        self.wait_timer -= Time.delta_time
        if self.wait_timer <= 0:
            self.ball.launch_ball()
            self.state = GameState.PLAYING

    def handle_playing_state(self):
        if self.ball.scored:
            self.state = GameState.SCORED

    def handle_scored_state(self):
        self.ball.reset_ball()
        self.reset_state()
        self.state = GameState.WAITING
