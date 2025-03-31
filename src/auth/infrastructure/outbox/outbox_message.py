from dataclasses import dataclass
from uuid import UUID


@dataclass
class OutboxMessage:
    data: str | bytes
    event_type: str
    message_id: UUID
