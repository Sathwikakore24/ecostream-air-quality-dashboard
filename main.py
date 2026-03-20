"""EcoStream Flask application entrypoint."""

from __future__ import annotations

import threading
import time
from typing import Any, Dict

import pandas as pd
from flask import Flask, jsonify, render_template_string, request

from aqi_calculator import calculate_aqi
from dashboard import build_map_figure, build_trend_figure, default_dashboard_html
from data_fetcher import fetch_sensor_data, generate_sensor_catalog
from data_processor import clean_sensor_data
from database_manager import (
    get_latest_snapshot,
    get_recent_readings,
    init_db,
    insert_readings,
)


REFRESH_SECONDS = 30
AQI_ALERT_THRESHOLD = 150

app = Flask(__name__)
SENSORS = generate_sensor_catalog()


def ingestion_loop() -> None:
    """Background thread that fetches, processes, and stores data every interval."""
    while True:
        raw_rows = fetch_sensor_data(SENSORS)
        cleaned = clean_sensor_data(raw_rows)
        if cleaned.empty:
            time.sleep(REFRESH_SECONDS)
            continue
        cleaned[["aqi", "aqi_category", "health_advisory"]] = cleaned.apply(
            lambda row: pd.Series(calculate_aqi(row["pm25"], row["pm10"])),
            axis=1,
        )
        insert_readings(cleaned)
        time.sleep(REFRESH_SECONDS)


def summarize_kpis(snapshot_df: pd.DataFrame) -> Dict[str, Any]:
    if snapshot_df.empty:
        return {
            "avg_aqi": "--",
            "worst_category": "--",
            "sensor_count": 0,
            "health_advisory": "No readings available yet.",
            "last_update": "--",
        }
    snapshot_df["timestamp"] = pd.to_datetime(snapshot_df["timestamp"], utc=True, errors="coerce")
    worst_idx = snapshot_df["aqi"].idxmax()
    worst_row = snapshot_df.loc[worst_idx]
    return {
        "avg_aqi": int(round(snapshot_df["aqi"].mean(), 0)),
        "worst_category": worst_row["aqi_category"],
        "sensor_count": int(snapshot_df["sensor_id"].nunique()),
        "health_advisory": worst_row["health_advisory"],
        "last_update": str(snapshot_df["timestamp"].max()),
    }


def compute_alert(snapshot_df: pd.DataFrame) -> Dict[str, str]:
    if snapshot_df.empty:
        return {"message": ""}
    high = snapshot_df[snapshot_df["aqi"] >= AQI_ALERT_THRESHOLD]
    if high.empty:
        return {"message": ""}
    locations = ", ".join(high["location"].tolist())
    return {
        "message": (
            f"Alert: AQI exceeded {AQI_ALERT_THRESHOLD} at {len(high)} location(s): {locations}. "
            "Sensitive groups should avoid prolonged outdoor activity."
        )
    }


@app.route("/")
def home() -> str:
    return render_template_string(default_dashboard_html())


@app.route("/api/dashboard-data")
def dashboard_data():
    pollutant = request.args.get("pollutant", "pm25")
    if pollutant not in {"pm25", "pm10", "co2", "temperature", "humidity"}:
        pollutant = "pm25"

    snapshot = get_latest_snapshot()
    history = get_recent_readings(hours=24)

    payload = {
        "kpis": summarize_kpis(snapshot),
        "alert": compute_alert(snapshot),
        "map_figure": build_map_figure(snapshot),
        "trend_figure": build_trend_figure(history, pollutant),
    }
    return jsonify(payload)


def main() -> None:
    init_db()
    thread = threading.Thread(target=ingestion_loop, daemon=True)
    thread.start()
    app.run(debug=True, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
