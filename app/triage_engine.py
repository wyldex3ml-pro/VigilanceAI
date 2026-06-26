from typing import Literal

from pydantic import BaseModel, Field


class StreamEvent(BaseModel):
    event_id: str
    timestamp: str
    media_type: Literal["text", "image"]
    payload: str
    source: str
    priority_hint: str = "unknown"


class TriageResult(BaseModel):
    event_id: str
    risk_score: float = Field(ge=0.0, le=1.0)
    risk_level: Literal["low", "medium", "high"]
    route_to_cloud_ai: bool
    reason: str


class LocalTriageEngine:
    def __init__(self):
        self.high_risk_keywords = [
            "suspicious",
            "restricted",
            "unattended",
            "crowd",
            "package",
        ]

        self.medium_risk_keywords = [
            "vehicle",
            "parking",
            "gate",
            "entered",
        ]

    async def score_event(self, event: StreamEvent) -> TriageResult:
        text = event.payload.lower()

        risk_score = 0.1
        reason = "No strong risk indicators detected."

        if event.media_type == "image":
            risk_score = 0.4
            reason = "Image event assigned medium base risk for local monitoring."

        if any(keyword in text for keyword in self.high_risk_keywords):
            risk_score = 0.85
            reason = "High-risk keyword detected, handled locally to protect API quota."

        elif any(keyword in text for keyword in self.medium_risk_keywords):
            risk_score = 0.55
            reason = "Medium-risk keyword detected in event payload."

        if risk_score >= 0.90:
            risk_level = "high"
            route_to_cloud_ai = True
        elif risk_score >= 0.75:
            risk_level = "high"
            route_to_cloud_ai = False
        elif risk_score >= 0.40:
            risk_level = "medium"
            route_to_cloud_ai = False
        else:
            risk_level = "low"
            route_to_cloud_ai = False

        return TriageResult(
            event_id=event.event_id,
            risk_score=risk_score,
            risk_level=risk_level,
            route_to_cloud_ai=route_to_cloud_ai,
            reason=reason,
        )