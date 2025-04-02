from dataclasses import dataclass

from bazario.markers import Notification

from auth.domain.user.user_id import UserId


@dataclass(frozen=True)
class UserLoggedIn(Notification):
    user_id: UserId
