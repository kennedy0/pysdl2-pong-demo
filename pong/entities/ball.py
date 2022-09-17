import random
from typing import Optional, TYPE_CHECKING

from core.datatypes.point import Point
from core.datatypes.vector2 import Vector2
from core.entity import Entity
from core.actor import Actor
from core.sound import Sound
from core.sprite import Sprite
from core.utilities import math_utils
from pong import constants

if TYPE_CHECKING:
    from pong.entities.computer_paddle import ComputerPaddle
    from pong.entities.player_paddle import PlayerPaddle
    from pong.entities.score import Score


class Ball(Actor):
    def __init__(self) -> None:
        super().__init__()

        # Collision
        self.width = 6
        self.height = 6
        self.pivot.set_center()

        # Sprite
        self.sprite = Sprite("ball.png")
        self.sprite.pivot.set_center()

        # Movement
        self.direction = Vector2.zero()
        self.speed = 0
        self.start_speed = 2
        self.angle = 0
        self.max_angle = 60

        # Entity references
        self.score: Optional[Score] = None
        self.player_paddle: Optional[PlayerPaddle] = None
        self.computer_paddle: Optional[ComputerPaddle] = None

        # Audio
        self.bounce_sound = Sound("bounce.wav")
        self.player_score_sound = Sound("score_player.wav")
        self.computer_score_sound = Sound("score_computer.wav")

        # Misc
        self.scored = False
        self.score_position = Point.zero()

    @property
    def velocity(self) -> Vector2:
        return self.direction * self.speed

    def initialize(self) -> None:
        self.score = Entity.find("Score")
        self.player_paddle = Entity.find("Player")
        self.computer_paddle = Entity.find("Computer")
        self.reset_ball()

    def update(self) -> None:
        # Check for collisions with the edge of the screen
        self.check_for_score()
        self.check_for_edge_bounce()

        # Move
        self.move_x(self.velocity.x, self.on_collide_x)
        self.move_y(self.velocity.y, self.on_collide_y)

    def draw(self) -> None:
        self.sprite.draw(self.position)

    def reset_ball(self) -> None:
        """ Reset the ball's position in the center of the screen. """
        self.scored = False
        self.stop_ball()
        self.x = constants.SCREEN_WIDTH / 2
        self.y = constants.SCREEN_HEIGHT / 2

    def stop_ball(self) -> None:
        """ Stop the ball's movement. """
        self.speed = self.start_speed
        self.direction = Vector2.zero()

    def launch_ball(self) -> None:
        """ Launch the ball in a random direction. """
        # Randomly pick left or right
        if random.random() < .5:
            direction = Vector2.left()
        else:
            direction = Vector2.right()

        self.speed = self.start_speed
        self.direction = direction
        self.calculate_score_position()
        self.bounce_sound.play()

    def check_for_score(self) -> None:
        """ Score when the ball gets to the left or right edge of the screen. """
        if self.bbox.left <= 0 and self.direction.x < 0:
            self.scored = True
            self.stop_ball()
            self.score.increase_player_2_score()
            self.computer_paddle.reset_move_target()
            self.computer_score_sound.play()
        elif self.bbox.right >= constants.SCREEN_WIDTH and self.direction.x > 0:
            self.scored = True
            self.stop_ball()
            self.score.increase_player_1_score()
            self.computer_paddle.reset_move_target()
            self.player_score_sound.play()

    def check_for_edge_bounce(self) -> None:
        """ Bounce when the ball gets to the top or bottom edge of the screen. """
        if self.bbox.top <= 0 and self.direction.y < 0:
            self.direction.y *= -1
            self.bounce_sound.play()
        elif self.bbox.bottom >= constants.SCREEN_HEIGHT and self.direction.y > 0:
            self.direction.y *= -1
            self.bounce_sound.play()

    def on_collide_x(self, entity: Entity) -> None:
        """ Check for collisions with a paddle. """
        if entity.has_tag("paddle"):
            self.on_hit_paddle(entity)
        else:
            self.direction.x *= -1
        self.bounce_sound.play()

    def on_collide_y(self, entity: Entity) -> None:
        """ Change direction if the ball hits anything. """
        self.direction.y *= -1
        self.bounce_sound.play()

    def on_hit_paddle(self, paddle: Entity) -> None:
        """ Change the direction and speed of the ball. """
        # The point that the ball hit the paddle - relative to its center position
        # Range from top to bottom is -1 to 1
        contact_point = math_utils.remap(self.position.y, paddle.bbox.top, paddle.bbox.bottom, -1, 1)
        contact_point = math_utils.clamp(contact_point, -1, 1)

        # Calculate new angle
        if self.direction.x > 0:
            # Hit while moving right
            self.direction = Vector2.left()
            angle = self.max_angle * contact_point * -1
        else:
            # Hit while moving left
            self.direction = Vector2.right()
            angle = self.max_angle * contact_point

        self.angle = math_utils.snap_to_interval(angle, 15)

        # Set new direction
        self.direction.rotate(self.angle)
        self.calculate_score_position()

        # Increase the speed
        self.speed += .1

    def calculate_score_position(self) -> None:
        """ Calculate the position that the ball will be when it crosses the goal line.
        This is used by the computer paddle when it picks a position to defend.
        """
        direction = self.direction.copy()
        position = Vector2(*self.position)

        player = self.player_paddle  # type: PlayerPaddle
        computer = self.computer_paddle  # type: ComputerPaddle
        while True:
            # Update position
            position += direction
            bbox = self.bbox_at(int(position.x), int(position.y))

            # Handle edge bounce
            if bbox.top <= 0 and direction.y < 0:
                direction.y *= -1
            elif bbox.bottom >= constants.SCREEN_HEIGHT and direction.y > 0:
                direction.y *= -1

            # Exit if we're at the point where the paddle could touch the ball
            if direction.x < 0 and bbox.left <= player.bbox.right + 1:
                break
            if direction.x > 0 and bbox.right >= computer.bbox.left - 1:
                break

        self.score_position = position
