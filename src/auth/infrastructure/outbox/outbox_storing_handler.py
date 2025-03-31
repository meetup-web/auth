from uuid import UUID

from bazario.asyncio import NotificationHandler

from auth.domain.shared.events import DomainEvent
from auth.infrastructure.outbox.outbox_gateway import OutboxGateway
from auth.infrastructure.outbox.outbox_message import OutboxMessage
from auth.infrastructure.outbox.outbox_serialization import to_json


class OutboxStoringHandler(NotificationHandler[DomainEvent]):
    def __init__(self, outbox_gateway: OutboxGateway) -> None:
        self._outbox_gateway = outbox_gateway

    async def handle(self, notification: DomainEvent) -> None:
        message = OutboxMessage(
            data=to_json(notification),
            message_id=UUID(str(notification.event_id)),
            event_type=notification.event_type,
        )
        self._outbox_gateway.add(message)
