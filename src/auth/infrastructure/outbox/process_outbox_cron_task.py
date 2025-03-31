from dishka import FromDishka
from dishka.integrations.taskiq import inject

from auth.infrastructure.outbox.outbox_processor import OutboxProcessor


@inject
async def process_outbox(outbox_processor: FromDishka[OutboxProcessor]) -> None:
    await outbox_processor.process()
