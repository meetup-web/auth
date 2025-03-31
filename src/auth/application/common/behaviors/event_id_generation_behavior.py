from bazario.asyncio import HandleNext, PipelineBehavior

from auth.application.ports.id_generator import IdGenerator
from auth.domain.shared.events import DomainEvent


class EventIdGenerationBehavior(PipelineBehavior[DomainEvent, None]):
    def __init__(self, id_generator: IdGenerator) -> None:
        self._id_generator = id_generator

    async def handle(
        self,
        request: DomainEvent,
        handle_next: HandleNext[DomainEvent, None],
    ) -> None:
        request.set_event_id(
            self._id_generator.generate_event_id(),
        )

        return await handle_next(request)
