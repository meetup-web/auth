from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    ForeignKey,
    LargeBinary,
    MetaData,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import registry

from auth.domain.session.session import Session
from auth.domain.user.user import User
from auth.infrastructure.outbox.outbox_message import OutboxMessage

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)

USERS_TABLE = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("user_id", UUID, primary_key=True),
    Column("username", String(255), unique=True, nullable=False),
    Column("password", LargeBinary, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


SESSIONS_TABLE = Table(
    "sessions",
    MAPPER_REGISTRY.metadata,
    Column("session_id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.user_id"), nullable=False),
    Column("expires_at", DateTime(timezone=True), nullable=False),
)


OUTBOX_TABLE = Table(
    "outbox",
    MAPPER_REGISTRY.metadata,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)


def map_user_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        User,
        USERS_TABLE,
        properties={
            "_entity_id": USERS_TABLE.c.user_id,
            "_username": USERS_TABLE.c.username,
            "_password": USERS_TABLE.c.password,
            "_created_at": USERS_TABLE.c.created_at,
        },
    )


def map_session_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Session,
        SESSIONS_TABLE,
        properties={
            "_entity_id": SESSIONS_TABLE.c.session_id,
            "_user_id": SESSIONS_TABLE.c.user_id,
            "_expires_at": SESSIONS_TABLE.c.expires_at,
        },
    )


def map_outbox_table() -> None:
    MAPPER_REGISTRY.map_imperatively(OutboxMessage, OUTBOX_TABLE)
