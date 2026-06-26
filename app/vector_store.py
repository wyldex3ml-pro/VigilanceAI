import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from app.logger_config import logger

load_dotenv()

COLLECTION_NAME = "vigilance_events"


class VectorStore:
    def __init__(self):
        qdrant_host = os.getenv("QDRANT_HOST", "localhost")
        qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        self.client = QdrantClient(
            host=qdrant_host,
            port=qdrant_port,
            api_key=qdrant_api_key,
        )

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_size = 384

        try:
            self.client.get_collection(COLLECTION_NAME)
            logger.info("Qdrant collection already exists.")

        except Exception:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )
            logger.info("Created new Qdrant collection.")

    def build_text(self, event: dict) -> str:
        return (
            f"Media type: {event['media_type']}. "
            f"Payload: {event['payload']}. "
            f"Risk level: {event['risk_level']}. "
            f"Risk score: {event['risk_score']}. "
            f"Route: {event['route']}."
        )

    def add_event(self, event: dict):
        text = self.build_text(event)
        vector = self.model.encode(text).tolist()

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=event["event_id"],
                    vector=vector,
                    payload=event,
                )
            ],
        )

        logger.info("Event stored in Qdrant | id=%s", event["event_id"])

    def search(self, query: str, limit: int = 5):
        query_vector = self.model.encode(query).tolist()

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
        )

        return [
            {
                "score": point.score,
                "event": point.payload,
            }
            for point in results.points
        ]


vector_store = VectorStore()