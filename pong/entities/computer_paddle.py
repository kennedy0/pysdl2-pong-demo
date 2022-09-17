import random
from enum import Enum
from typing import Optional, TYPE_CHECKING

from core.datatypes.point import Point
from core.entity import Entity
from core.time import Time
from core.utilities import math_utils
from pong import constants
from pong.entities.paddle import Paddle

if TYPE_CHECKING:
    from pong.entities.ball import Ball
    from pong.entities.player_paddle import PlayerPaddle


class ComputerState(Enum):
    WAITING = "WAITING"
    THINKING = "THINKING"
    MOVING = "MOVING"


class ComputerPaddle(Paddle):
    def __init__(self):
        super().__init__()
        self._state = ComputerState.WAITING

        self.move_target = None

        self.ball: Optional[Ball] = None
        self.player_paddle: Optional[PlayerPaddle] = None

        self.think_timer_max = 0.5
        self.think_timer_min = 0.2
        self.think_timer = 0.0

    def initialize(self) -> None:
        self.x = 300
        self.y = 90
        self.ball = Entity.find("Ball")
        self.player_paddle = Entity.find("Player")

    def update(self) -> None:
        match self._state:
            case ComputerState.WAITING:
                self.handle_waiting_state()
            case ComputerState.THINKING:
                self.handle_thinking_state()
            case ComputerState.MOVING:
                self.handle_moving_state()

    def set_state(self, state: ComputerState):
        """ Set the state of the computer. """
        # If we are trying to enter the move state, but the position change is small enough, go to waiting state.
        # This prevents jittery movement
        if state == ComputerState.MOVING:
            if abs(self.move_target.y - self.position.y) < 4:
                state = ComputerState.WAITING

        self._state = state

    def handle_waiting_state(self):
        """ Handle the WAITING state. """
        # Enter thinking state if the ball is coming towards the computer
        if self.ball.direction.x > 0:
            self.reset_think_timer()
            self.set_state(ComputerState.THINKING)

    def reset_think_timer(self):
        """ Reset the thinking timer.
        The timer will reset quicker if the ball is closer to the computer.
        """
        timer_scale = math_utils.remap(self.ball.position.x, self.player_paddle.x, self.x, 1, 0.5)
        self.think_timer = max(self.think_timer_max * timer_scale, self.think_timer_min)

    def handle_thinking_state(self):
        """ Handle the THINKING state. """
        if self.think_timer > 0:
            self.think_timer -= Time.delta_time
            return

        # Pick a defense position
        self.pick_defense_position()
        self.set_state(ComputerState.MOVING)

    def pick_defense_position(self):
        """ Pick a defense position.
        This is close to the ball's score position, but introduces some error.
        """
        # The exact position it should be in
        position = self.ball.score_position.copy()

        # The maximum amount of error
        error = 10

        # Scale the error by the current angle of the ball.
        # The greater the angle, the more error there should be.
        angle_error_multiplier = math_utils.remap(abs(self.ball.angle / self.ball.max_angle), 0, 1, .5, 1)
        error *= angle_error_multiplier

        # Scale the error by the distance from the ball
        # The further away the ball is, the more error there should be.
        distance_error_multiplier = math_utils.remap(self.ball.position.x, self.player_paddle.x, self.x, 1, 0)
        error *= distance_error_multiplier

        # Scale the error by the ball speed
        # The higher the speed, the more error there should be
        # Speed = 1, Error = 1.1
        # Speed = 2, Error = 1.2
        # etc.
        speed_error = (self.ball.speed / 10) + 1
        error *= speed_error

        # Randomly decide if the error will be in the positive or negative direction
        if random.random() > 0.5:
            error *= -1

        # Add error to position
        position.y += error
        self.move_target = position

    def handle_moving_state(self):
        """ Handle the MOVING state. """
        # Calculate the difference between the current position and the target position
        move_delta = self.move_target.y - self.position.y

        # If the delta is close enough to zero, return to waiting (prevents jitter)
        if abs(move_delta) < 2:
            self.set_state(ComputerState.WAITING)

        # If the paddle is at the edge of the screen, return to waiting
        if self.bbox.top == 0 or self.bbox.bottom == constants.SCREEN_HEIGHT:
            self.set_state(ComputerState.WAITING)

        # Move
        move_direction = math_utils.sign(move_delta)
        move_amount = min(self.move_speed, abs(move_delta))
        self.move_y(move_amount * move_direction)

    def reset_move_target(self) -> None:
        """ Reset the move target close to the starting position. """
        self.move_target = Point(300, random.randint(80, 100))
        self.set_state(ComputerState.MOVING)

    def on_collide(self, other: Entity) -> None:
        # Always go to the WAITING state if the computer hits the ball.
        if other.name == "Ball":
            self.set_state(ComputerState.WAITING)
