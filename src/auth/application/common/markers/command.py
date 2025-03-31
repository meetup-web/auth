from dataclasses import dataclass

from bazario import Request


@dataclass(frozen=True)
class Command[TRes](Request[TRes]): ...
