import json
from pathlib import Path
from threading import Lock

QUEUE_METRICS_FILE = Path("queue_metrics.json")

lock = Lock()


def default_queue_metrics():
    return {
        "queue_size": 0,
        "events_processed": 0,
        "active_workers": 0,
    }


class QueueMetrics:
    def _read(self):
        if not QUEUE_METRICS_FILE.exists():
            return default_queue_metrics()

        with open(QUEUE_METRICS_FILE, "r") as file:
            return json.load(file)

    def _write(self, data):
        with open(QUEUE_METRICS_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def queue_added(self):
        with lock:
            data = self._read()
            data["queue_size"] += 1
            self._write(data)

    def queue_removed(self):
        with lock:
            data = self._read()
            data["queue_size"] = max(0, data["queue_size"] - 1)
            self._write(data)

    def worker_started(self):
        with lock:
            data = self._read()
            data["active_workers"] += 1
            self._write(data)

    def worker_finished(self):
        with lock:
            data = self._read()
            data["active_workers"] = max(0, data["active_workers"] - 1)
            data["events_processed"] += 1
            self._write(data)

    def get(self):
        with lock:
            return self._read()


queue_metrics = QueueMetrics()