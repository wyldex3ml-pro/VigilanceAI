import json
from pathlib import Path
from threading import Lock

EVENTS_FILE = Path("events.json")
MAX_EVENTS = 20

lock = Lock()


def load_events():
    with lock:
        if not EVENTS_FILE.exists():
            return []

        with open(EVENTS_FILE, "r") as file:
            return json.load(file)


def save_event(event: dict):
    with lock:
        if not EVENTS_FILE.exists():
            events = []
        else:
            with open(EVENTS_FILE, "r") as file:
                events = json.load(file)

        events.insert(0, event)
        events = events[:MAX_EVENTS]

        with open(EVENTS_FILE, "w") as file:
            json.dump(events, file, indent=4)


def get_events():
    return load_events()