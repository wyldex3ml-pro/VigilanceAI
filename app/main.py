import asyncio

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import authenticate_user, create_access_token
from app.event_store import get_events
from app.metrics import get_metrics
from app.queue_metrics import queue_metrics
from app.websocket_bridge import get_ws_events
from app.websocket_manager import websocket_manager

app = FastAPI(
    title="VigilanceAI API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "VigilanceAI API Running",
        "status": "healthy",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        return {"error": "Invalid username or password"}

    token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/metrics")
def metrics():
    return get_metrics()


@app.get("/events")
def events():
    return get_events()


@app.get("/queue")
def queue():
    return queue_metrics.get()


@app.get("/search")
def search(query: str, limit: int = 5):
    return {
        "message": "Semantic search is available in local/Qdrant-enabled mode.",
        "query": query,
        "limit": limit,
    }


@app.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await websocket_manager.connect(websocket)

    last_event = None

    try:
        while True:
            events = get_ws_events()

            if events:
                latest = events[0]

                if latest != last_event:
                    await websocket.send_json(latest)
                    last_event = latest

            await asyncio.sleep(1)

    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)