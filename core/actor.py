from __future__ import annotations
from core.entity import Entity
from core.utilities import math_utils

from typing import Callable, Optional


class Actor(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Fractional position for movement
        self._x_remainder = 0
        self._y_remainder = 0

    def move_x(self, amount: float, collision_callback: Optional[Callable] = None) -> None:
        """ Move the actor horizontally.
        An optional collision callback can be provided. If so, it will run after the entity's built-in 'on_collide'.
        """
        # Add movement amount to remainder
        self._x_remainder += amount

        # Round remainder to get total movement
        move = math_utils.round_to_int(self._x_remainder)

        # Handle movement
        if move != 0:
            # Subtract the movement amount from the remainder
            self._x_remainder -= move

            # Get the movement direction
            direction = math_utils.sign(move)

            # Move one pixel at a time
            while move != 0:
                new_x = self.x + direction

                # Check for collisions
                collisions = self.check_collisions(new_x, self.y)
                for entity in collisions:
                    self.on_collide(entity)
                    entity.on_collide(self)
                    if collision_callback:
                        collision_callback(entity)
                if collisions:
                    break

                # Move
                self.x = new_x
                move -= direction

    def move_y(self, amount: float, collision_callback: Optional[Callable] = None) -> None:
        """ Move the actor vertically.
        An optional collision callback can be provided. If so, it will run after the entity's built-in 'on_collide'.
        """
        # Add movement amount to remainder
        self._y_remainder += amount

        # Round remainder to get total movement
        move = math_utils.round_to_int(self._y_remainder)

        # Handle movement
        if move != 0:
            # Subtract the movement amount from the remainder
            self._y_remainder -= move

            # Get the movement direction
            direction = math_utils.sign(move)

            # Move one pixel at a time
            while move != 0:
                new_y = self.y + direction

                # Check for collisions
                collisions = self.check_collisions(self.x, new_y)
                for entity in collisions:
                    self.on_collide(entity)
                    entity.on_collide(self)
                    if collision_callback:
                        collision_callback(entity)
                if collisions:
                    break

                # Move
                self.y = new_y
                move -= direction

    def check_collisions(self, x: int, y: int) -> list[Entity]:
        """ Check to see if the actor will have a collision with another entity at a specific position. """
        collisions = []
        for actor in self.scene.actors:
            if actor == self:
                continue
            if self.bbox_at(x, y).intersects(actor.bbox):
                collisions.append(actor)
        return collisions
