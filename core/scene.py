from __future__ import annotations

from typing import Iterator, Optional, TypeVar, TYPE_CHECKING

from core.entity_list import EntityList
from core.actor import Actor

if TYPE_CHECKING:
    from core.engine import Engine


T = TypeVar('T')


class Scene:
    def __init__(self) -> None:
        self._engine = None
        self._entities = EntityList(self)

    @property
    def engine(self) -> Optional[Engine]:
        """ A reference to the engine.
        If this is not the currently running scene in the engine, the value will be None.
        """
        return self._engine

    @property
    def entities(self) -> EntityList:
        """ A list of entities that belong to this scene. """
        return self._entities

    @property
    def actors(self) -> Iterator[Actor]:
        for entity in self.entities.of_type(Actor):
            yield entity

    def load_entities(self) -> None:
        """ Load entities into the scene. This is called right before 'start'. """
        pass

    def start(self, engine: Engine) -> None:
        """ Called when the engine loads the scene. """
        self._engine = engine

    def update(self) -> None:
        """ Update loop. """
        self.entities.update()
        self.entities.after_update()

    def draw(self) -> None:
        """ Draw loop. """
        self.entities.draw()

    def end(self) -> None:
        """ Called before the engine loads the next scene. """
        self._engine = None
