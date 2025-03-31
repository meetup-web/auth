from enum import StrEnum
from typing import Final

from faststream.rabbit import RabbitBroker

from auth.infrastructure.outbox.outbox_message import OutboxMessage
from auth.infrastructure.outbox.outbox_publisher import OutboxPublisher


class ExchangeName(StrEnum):
    AUTH = "auth_exchange"


class RabbitmqOutboxPublisher(OutboxPublisher):
    _CONTENT_TYPE: Final[str] = "application/json"

    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def publish(self, message: OutboxMessage) -> None:
        await self._broker.publish(
            message=message.data,
            exchange=ExchangeName.AUTH,
            routing_key=message.event_type,
            message_id=message.message_id.hex,
            content_type=self._CONTENT_TYPE,
            persist=True,
        )
