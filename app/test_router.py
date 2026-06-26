import asyncio
from datetime import datetime, UTC
from uuid import uuid4

from router import DynamicFallbackRouter
from triage_engine import LocalTriageEngine, StreamEvent


async def main():
    event = StreamEvent(
        event_id=str(uuid4()),
        timestamp=datetime.now(UTC).isoformat(),
        media_type="text",
        payload="Suspicious package left unattended",
        source="mock_camera_or_feed",
        priority_hint="unknown",
    )

    triage_engine = LocalTriageEngine()
    triage = await triage_engine.score_event(event)

    router = DynamicFallbackRouter()
    result = await router.route_event(event, triage)

    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())