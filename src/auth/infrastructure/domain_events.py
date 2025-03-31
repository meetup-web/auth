from collections.abc import Iterable

from auth.application.ports.event_raiser import DomainEventsRaiser
from auth.domain.shared.events import DomainEvent, DomainEventAdder


class DomainEvents(DomainEventAdder, DomainEventsRaiser):
    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def add_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def raise_events(self) -> Iterable[DomainEvent]:
        events = tuple(self._events)
        self._events.clear()

        return events
