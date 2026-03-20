"""SQLite persistence and query helpers."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd


DB_PATH = Path("ecostream.db")


def init_db(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS air_quality_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                location TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                timestamp TEXT NOT NULL,
                pm25 REAL NOT NULL,
                pm10 REAL NOT NULL,
                co2 REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                aqi INTEGER NOT NULL,
                aqi_category TEXT NOT NULL,
                health_advisory TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_air_quality_timestamp ON air_quality_readings(timestamp)"
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_air_quality_sensor ON air_quality_readings(sensor_id)")
        conn.commit()


def insert_readings(df: pd.DataFrame, db_path: Path = DB_PATH) -> None:
    if df.empty:
        return
    to_store = df.copy()
    to_store["timestamp"] = to_store["timestamp"].astype(str)
    with sqlite3.connect(db_path) as conn:
        to_store.to_sql("air_quality_readings", conn, if_exists="append", index=False)


def get_recent_readings(hours: int = 24, db_path: Path = DB_PATH) -> pd.DataFrame:
    query = """
    SELECT *
    FROM air_quality_readings
    WHERE timestamp >= datetime('now', ?)
    ORDER BY timestamp ASC
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=(f"-{hours} hours",))


def get_latest_snapshot(db_path: Path = DB_PATH) -> pd.DataFrame:
    query = """
    SELECT t1.*
    FROM air_quality_readings t1
    INNER JOIN (
        SELECT sensor_id, MAX(timestamp) AS max_ts
        FROM air_quality_readings
        GROUP BY sensor_id
    ) t2
      ON t1.sensor_id = t2.sensor_id
     AND t1.timestamp = t2.max_ts
    ORDER BY t1.sensor_id
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn)


def get_location_history(sensor_id: str, hours: int = 24, db_path: Path = DB_PATH) -> pd.DataFrame:
    query = """
    SELECT *
    FROM air_quality_readings
    WHERE sensor_id = ?
      AND timestamp >= datetime('now', ?)
    ORDER BY timestamp ASC
    """
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(query, conn, params=(sensor_id, f"-{hours} hours"))


def get_available_sensors(db_path: Path = DB_PATH) -> list[str]:
    query = "SELECT DISTINCT sensor_id FROM air_quality_readings ORDER BY sensor_id"
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(query).fetchall()
    return [row[0] for row in rows]
