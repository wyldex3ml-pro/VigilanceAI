import asyncio
import os
from typing import Literal, Optional

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

from app.logger_config import logger
from app.triage_engine import StreamEvent, TriageResult


load_dotenv()


class RouterResult(BaseModel):
    event_id: str
    final_route: Literal["local_only", "cloud_ai"]
    cloud_used: bool
    cloud_summary: Optional[str] = None
    reason: str


class DynamicFallbackRouter:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            logger.warning("GEMINI_API_KEY not found. Cloud routing disabled.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            logger.info("Gemini router initialized successfully.")

    async def route_event(
        self,
        event: StreamEvent,
        triage: TriageResult,
    ) -> RouterResult:
        if not triage.route_to_cloud_ai:
            return RouterResult(
                event_id=event.event_id,
                final_route="local_only",
                cloud_used=False,
                reason="Local triage was enough. Cloud API skipped.",
            )

        if self.client is None:
            return RouterResult(
                event_id=event.event_id,
                final_route="local_only",
                cloud_used=False,
                reason="Cloud routing unavailable. API key missing.",
            )

        prompt = f"""
You are VigilanceAI, a security event analyst.

Analyze this mock portfolio event briefly.

Media type: {event.media_type}
Payload: {event.payload}
Local risk score: {triage.risk_score}
Local reason: {triage.reason}

Return:
1. Risk interpretation
2. Recommended next action
3. Whether human review is needed
"""

        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model="gemini-2.5-flash",
                contents=prompt,
            )

            return RouterResult(
                event_id=event.event_id,
                final_route="cloud_ai",
                cloud_used=True,
                cloud_summary=response.text,
                reason="High-risk event routed to Gemini.",
            )

        except Exception as e:
            logger.error(
                "Gemini routing failed | id=%s | error=%s",
                event.event_id,
                e,
            )

            return RouterResult(
                event_id=event.event_id,
                final_route="local_only",
                cloud_used=False,
                reason=f"Cloud failed. Fallback kept local. Error: {e}",
            )