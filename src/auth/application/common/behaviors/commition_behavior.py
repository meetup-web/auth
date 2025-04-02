from bazario.asyncio import HandleNext, PipelineBehavior

from auth.application.common.markers.command import Command
from auth.application.ports.transaction_manager import TransactionManager


class CommitionBehavior[C: Command, R](PipelineBehavior[C, R]):
    def __init__(self, transaction_manager: TransactionManager) -> None:
        self._transaction_manager = transaction_manager

    async def handle(self, request: C, handle_next: HandleNext[C, R]) -> R:
        response = await handle_next(request)

        await self._transaction_manager.commit()

        return response
