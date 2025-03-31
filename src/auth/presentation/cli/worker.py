import asyncio
from concurrent.futures import ThreadPoolExecutor

from click import option
from dishka import FromDishka
from dishka.integrations.click import inject
from taskiq.api.scheduler import run_scheduler_task
from taskiq.cli.worker.run import shutdown_broker
from taskiq.receiver.receiver import Receiver
from taskiq.schedule_sources import LabelScheduleSource
from taskiq.scheduler.scheduler import TaskiqScheduler
from taskiq_aio_pika.broker import AioPikaBroker


@option("--max_concurrency", "-m", type=int, default=10)
@option("--max_async_tasks", "-a", type=int, default=100)
@option("--shutdown_timeout", "-s", type=int, default=5)
@inject
def start_worker(
    max_concurrency: int,
    max_async_tasks: int,
    shutdown_timeout: int,
    *,
    broker: FromDishka[AioPikaBroker],
) -> None:
    shutdown_event = asyncio.Event()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    broker.is_worker_process = True

    try:
        with ThreadPoolExecutor(max_concurrency) as pool:
            reciever = Receiver(
                broker=broker, executor=pool, max_async_tasks=max_async_tasks
            )
            loop.run_until_complete(reciever.listen(shutdown_event))
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown_broker(broker, shutdown_timeout))


@inject
def start_tasks(
    *,
    broker: FromDishka[AioPikaBroker],
) -> None:
    scheduler = TaskiqScheduler(
        broker=broker, sources=[LabelScheduleSource(broker=broker)]
    )
    asyncio.run(run_scheduler_task(scheduler=scheduler, run_startup=True))
