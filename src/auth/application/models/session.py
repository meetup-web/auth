from dataclasses import dataclass
from datetime import datetime

from auth.domain.session.session_id import SessionId
from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class SessionReadModel:
    session_id: SessionId
    user_id: UserId
    expires_at: datetime
