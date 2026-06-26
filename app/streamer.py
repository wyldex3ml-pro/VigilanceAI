import asyncio
import random
import uuid
from datetime import UTC, datetime

from app.event_store import save_event
from app.logger_config import logger
from app.metrics import get_metrics, update_metrics
from app.queue_metrics import queue_metrics
from app.router import DynamicFallbackRouter
from app.triage_engine import LocalTriageEngine, StreamEvent
from app.vector_store import vector_store
from app.websocket_bridge import add_ws_event
from app.worker_pool import WorkerPool


MOCK_TEXTS = [
    "Person walking near restricted area",
    "Normal office activity detected",
    "Suspicious package left unattended",
    "Vehicle entered parking zone",
    "Crowd gathering near main gate",
]

MOCK_IMAGES = [
    "data/images/frame_001.jpg",
    "data/images/frame_002.jpg",
    "data/images/frame_003.jpg",
    "data/images/frame_004.jpg",
]


async def generate_mock_event() -> StreamEvent:
    media_type = random.choice(["text", "image"])
    payload = random.choice(MOCK_TEXTS) if media_type == "text" else random.choice(MOCK_IMAGES)

    return StreamEvent(
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(UTC).isoformat(),
        media_type=media_type,
        payload=payload,
        source="mock_camera_or_feed",
        priority_hint="unknown",
    )


async def process_event(
    event: StreamEvent,
    triage_engine: LocalTriageEngine,
    router: DynamicFallbackRouter,
):
    triage = await triage_engine.score_event(event)
    route_result = await router.route_event(event, triage)

    event_record = {
        "timestamp": event.timestamp,
        "event_id": event.event_id,
        "media_type": event.media_type,
        "payload": event.payload,
        "risk_level": triage.risk_level,
        "risk_score": triage.risk_score,
        "cloud_used": route_result.cloud_used,
        "route": route_result.final_route,
    }

    save_event(event_record)
    vector_store.add_event(event_record)

    add_ws_event(
        {
            "type": "event",
            "data": event_record,
        }
    )

    update_metrics(route_result.cloud_used)
    metrics = get_metrics()

    logger.info(
        "Pipeline Event | id=%s | risk=%s | route=%s",
        event.event_id,
        triage.risk_level,
        route_result.final_route,
    )

    logger.info(
        "Metrics | total=%s | local=%s | cloud=%s | savings=%s%%",
        metrics["total_events"],
        metrics["local_only"],
        metrics["cloud_calls"],
        metrics["savings_percent"],
    )


async def producer(pool: WorkerPool, delay_seconds: float = 1.0):
    while True:
        event = await generate_mock_event()
        await pool.queue.put(event)
        queue_metrics.queue_added()

        logger.info(
            "Event queued | id=%s | queue_size=%s",
            event.event_id,
            queue_metrics.get()["queue_size"],
        )

        await asyncio.sleep(delay_seconds)


async def main():
    logger.info("Starting VigilanceAI concurrent worker pipeline")

    triage_engine = LocalTriageEngine()
    router = DynamicFallbackRouter()
    pool = WorkerPool(workers=4)

    async def process_with_shared_services(event: StreamEvent):
        await process_event(event, triage_engine, router)

    producer_task = asyncio.create_task(producer(pool, delay_seconds=1.0))
    worker_task = asyncio.create_task(pool.start(process_with_shared_services))

    await asyncio.gather(producer_task, worker_task)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user")