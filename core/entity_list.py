from __future__ import annotations

from typing import Iterator, TypeVar, TYPE_CHECKING

from core.entity import Entity

if TYPE_CHECKING:
    from core.scene import Scene


T = TypeVar('T')


class EntityList:
    def __init__(self, scene: Scene) -> None:
        # The scene that this entity list belongs to
        self._scene = scene

        # List of entities
        self._entities: list[Entity] = list()

        # Lists for add / remove queue
        self._to_add: list[Entity] = list()
        self._to_remove: list[Entity] = list()

        # Sets to quickly check list membership
        self._current: set[Entity] = set()
        self._adding: set[Entity] = set()
        self._removing: set[Entity] = set()

    def __len__(self) -> int:
        return len(self._entities)

    def __iter__(self) -> Iterator[Entity]:
        for entity in self._entities:
            yield entity

    @property
    def scene(self) -> Scene:
        """ The scene that this entity list belongs to. """
        return self._scene

    def of_type(self, entity_type: T) -> Iterator[T]:
        if not issubclass(entity_type, Entity):
            raise RuntimeError(f"{entity_type} is not inherited from {Entity}")

        for entity in self._entities:
            if isinstance(entity, entity_type):
                yield entity

    def add(self, entity: Entity) -> None:
        """ Add an entity to the list. """
        if entity not in self._current and entity not in self._adding:
            self._to_add.append(entity)
            self._adding.add(entity)

    def remove(self, entity: Entity) -> None:
        """ Remove an entity from the list. """
        if entity in self._current and entity not in self._removing:
            self._to_remove.append(entity)
            self._removing.add(entity)

    def update_list(self) -> None:
        """ This handles all of the logic for adding and removing entities from the list.
        The process is deferred until the start of the next frame.
        """
        # Add queued entities
        for entity in self._to_add:
            self._entities.append(entity)
            self._current.add(entity)
            entity.scene = self.scene

        # Remove queued entities
        for entity in self._to_remove:
            self._entities.remove(entity)
            self._current.remove(entity)
            entity.scene = None

        # Awake and start
        for entity in self._to_add:
            entity.initialize()

        for entity in self._to_add:
            entity.start()

        # Clear lists
        self._to_add.clear()
        self._adding.clear()
        self._to_remove.clear()
        self._removing.clear()

    def update(self) -> None:
        """ Update loop. """
        self.update_list()
        for entity in self._entities:
            entity.update()

    def after_update(self) -> None:
        """ Called immediately after update. """
        for entity in self._entities:
            entity.after_update()

    def draw(self) -> None:
        """ Draw loop. """
        for entity in self._entities:
            entity.draw()
