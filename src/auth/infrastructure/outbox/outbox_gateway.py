from abc import ABC, abstractmethod

from auth.infrastructure.outbox.outbox_message import OutboxMessage


class OutboxGateway(ABC):
    @abstractmethod
    async def select(self) -> list[OutboxMessage]: ...
    @abstractmethod
    def add(self, message: OutboxMessage) -> None: ...
    @abstractmethod
    async def delete(self, message: OutboxMessage) -> None: ...
