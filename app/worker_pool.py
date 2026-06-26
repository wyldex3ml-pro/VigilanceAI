import asyncio

from app.logger_config import logger
from app.queue_metrics import queue_metrics


class WorkerPool:
    def __init__(self, workers: int = 4):
        self.queue = asyncio.Queue()
        self.workers = workers

    async def start(self, process_function):
        tasks = []

        for worker_id in range(1, self.workers + 1):
            task = asyncio.create_task(
                self.worker(worker_id, process_function)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

    async def worker(self, worker_id: int, process_function):
        logger.info("Worker-%s started", worker_id)

        while True:
            event = await self.queue.get()

            queue_metrics.queue_removed()
            queue_metrics.worker_started()

            try:
                await process_function(event)

            except Exception as e:
                logger.error(
                    "Worker-%s failed | error=%s",
                    worker_id,
                    e,
                )

            finally:
                queue_metrics.worker_finished()
                self.queue.task_done()