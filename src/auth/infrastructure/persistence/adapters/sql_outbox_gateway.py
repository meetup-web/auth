from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.infrastructure.outbox.outbox_gateway import OutboxGateway
from auth.infrastructure.outbox.outbox_message import OutboxMessage


class SqlOutboxGateway(OutboxGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def select(self) -> list[OutboxMessage]:
        statement = select(OutboxMessage)
        cursor_result = await self._session.execute(statement)
        return list(cursor_result.scalars().all())

    def add(self, message: OutboxMessage) -> None:
        self._session.add(message)

    async def delete(self, message: OutboxMessage) -> None:
        await self._session.delete(message)
