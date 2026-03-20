"""Data cleaning and shaping helpers."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd


NUMERIC_COLUMNS = ["pm25", "pm10", "co2", "temperature", "humidity", "lat", "lon"]


def clean_sensor_data(rows: List[Dict[str, float | str]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
    df = df.dropna(subset=["sensor_id", "location", "timestamp", "pm25", "pm10", "lat", "lon"])
    df = df.sort_values("timestamp")
    return df
