"""Data source module for fetching/simulating sensor readings."""

from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Dict, List


def generate_sensor_catalog() -> List[Dict[str, float | str]]:
    """Create a fixed list of city sensors with coordinates."""
    return [
        {"sensor_id": "S01", "location": "Downtown", "lat": 40.7128, "lon": -74.0060},
        {"sensor_id": "S02", "location": "Uptown", "lat": 40.7306, "lon": -73.9352},
        {"sensor_id": "S03", "location": "Midtown", "lat": 40.7549, "lon": -73.9840},
        {"sensor_id": "S04", "location": "Harbor", "lat": 40.7001, "lon": -74.0122},
        {"sensor_id": "S05", "location": "University", "lat": 40.7295, "lon": -73.9965},
        {"sensor_id": "S06", "location": "West End", "lat": 40.7750, "lon": -73.9800},
        {"sensor_id": "S07", "location": "East Side", "lat": 40.7736, "lon": -73.9566},
        {"sensor_id": "S08", "location": "Industrial Zone", "lat": 40.6782, "lon": -73.9442},
        {"sensor_id": "S09", "location": "Airport", "lat": 40.6413, "lon": -73.7781},
        {"sensor_id": "S10", "location": "Green Park", "lat": 40.7851, "lon": -73.9683},
    ]


def fetch_sensor_data(sensors: List[Dict[str, float | str]]) -> List[Dict[str, float | str]]:
    """
    Simulate real-time readings.
    This can later be replaced with API integrations.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    rows: List[Dict[str, float | str]] = []
    for sensor in sensors:
        rows.append(
            {
                **sensor,
                "timestamp": timestamp,
                "pm25": round(random.uniform(5.0, 170.0), 1),
                "pm10": round(random.uniform(10.0, 220.0), 1),
                "co2": round(random.uniform(360.0, 1200.0), 1),
                "temperature": round(random.uniform(16.0, 38.0), 1),
                "humidity": round(random.uniform(25.0, 90.0), 1),
            }
        )
    return rows
