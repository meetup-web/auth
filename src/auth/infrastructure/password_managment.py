from typing import Final

from bcrypt import checkpw, gensalt, hashpw

from auth.application.ports.password_checker import PasswordChecker
from auth.application.ports.password_hasher import PasswordHasher


class CryptoPasswordManager(PasswordHasher, PasswordChecker):
    _ENCODING: Final[str] = "utf-8"

    def hash_password(self, password: str) -> bytes:
        return hashpw(password.encode(self._ENCODING), gensalt())

    def check_password(self, password: str, hashed_password: bytes) -> bool:
        return checkpw(password.encode(self._ENCODING), hashed_password)
