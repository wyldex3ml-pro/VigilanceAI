import asyncio
from datetime import datetime
from uuid import uuid4

from triage_engine import StreamEvent, LocalTriageEngine


async def main():
    engine = LocalTriageEngine()

    event = StreamEvent(
        event_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        media_type="text",
        payload="Suspicious package left unattended",
        source="mock_camera_or_feed",
    )

    result = await engine.score_event(event)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())