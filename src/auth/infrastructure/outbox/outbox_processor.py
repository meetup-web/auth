from auth.infrastructure.outbox.outbox_gateway import OutboxGateway
from auth.infrastructure.outbox.outbox_publisher import OutboxPublisher
from auth.infrastructure.persistence.transaction import Transaction


class OutboxProcessor:
    def __init__(
        self,
        transaction: Transaction,
        outbox_gateway: OutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> None:
        self._transaction = transaction
        self._outbox_gateway = outbox_gateway
        self._outbox_publisher = outbox_publisher

    async def process(self) -> None:
        messages = await self._outbox_gateway.select()

        for message in messages:
            await self._outbox_publisher.publish(message)
            await self._outbox_gateway.delete(message)

        await self._transaction.commit()
