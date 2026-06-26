import json
from pathlib import Path

METRICS_FILE = Path("metrics.json")


def get_metrics():
    if not METRICS_FILE.exists():
        return {
            "total_events": 0,
            "local_only": 0,
            "cloud_calls": 0,
            "savings_percent": 0.0,
        }

    with open(METRICS_FILE, "r") as f:
        return json.load(f)


def update_metrics(cloud_used: bool):
    metrics = get_metrics()

    metrics["total_events"] += 1

    if cloud_used:
        metrics["cloud_calls"] += 1
    else:
        metrics["local_only"] += 1

    metrics["savings_percent"] = round(
        (metrics["local_only"] / metrics["total_events"]) * 100,
        2,
    )

    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=4)