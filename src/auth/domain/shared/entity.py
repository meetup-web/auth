from collections.abc import Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from auth.domain.shared.events import DomainEvent, DomainEventAdder


class Entity[TEntityID: Hashable]:
    def __init__(
        self,
        entity_id: TEntityID,
        event_adder: "DomainEventAdder",
    ) -> None:
        self._entity_id = entity_id
        self._event_adder = event_adder

    def add_event(self, event: "DomainEvent") -> None:
        self._event_adder.add_event(event)

    @property
    def entity_id(self) -> TEntityID:
        return self._entity_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented

        return bool(other.entity_id == self.entity_id)

    def __hash__(self) -> int:
        return hash(self.entity_id)
