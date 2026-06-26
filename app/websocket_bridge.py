import json
from pathlib import Path
from threading import Lock

WEBSOCKET_EVENTS_FILE = Path("websocket_events.json")
MAX_WS_EVENTS = 50

lock = Lock()


def get_ws_events():
    with lock:
        if not WEBSOCKET_EVENTS_FILE.exists():
            return []

        with open(WEBSOCKET_EVENTS_FILE, "r") as file:
            return json.load(file)


def add_ws_event(event: dict):
    with lock:
        if not WEBSOCKET_EVENTS_FILE.exists():
            events = []
        else:
            with open(WEBSOCKET_EVENTS_FILE, "r") as file:
                events = json.load(file)

        events.insert(0, event)
        events = events[:MAX_WS_EVENTS]

        with open(WEBSOCKET_EVENTS_FILE, "w") as file:
            json.dump(events, file, indent=4)


def clear_ws_events():
    with lock:
        with open(WEBSOCKET_EVENTS_FILE, "w") as file:
            json.dump([], file, indent=4)