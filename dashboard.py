"""Dashboard HTML and chart-building helpers."""

from __future__ import annotations

import json
from typing import Any, Dict

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_map_figure(snapshot_df: pd.DataFrame) -> Dict[str, Any]:
    if snapshot_df.empty:
        return json.loads(go.Figure().to_json())
    fig = px.scatter_mapbox(
        snapshot_df,
        lat="lat",
        lon="lon",
        color="aqi",
        size="aqi",
        hover_name="location",
        hover_data={"sensor_id": True, "aqi_category": True, "lat": False, "lon": False},
        color_continuous_scale="YlOrRd",
        zoom=10,
        height=450,
        title="Live AQI Heatmap",
    )
    fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=40, b=0))
    return json.loads(fig.to_json())


def build_trend_figure(history_df: pd.DataFrame, pollutant: str) -> Dict[str, Any]:
    if history_df.empty:
        return json.loads(go.Figure().to_json())
    plot_df = history_df.copy()
    plot_df["timestamp"] = pd.to_datetime(plot_df["timestamp"], utc=True, errors="coerce")
    fig = px.line(
        plot_df,
        x="timestamp",
        y=pollutant,
        color="location",
        title=f"{pollutant.upper()} Trend (Last 24h)",
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return json.loads(fig.to_json())


def default_dashboard_html() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>EcoStream Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f6f8fb; color: #1f2937; }
    header { padding: 16px 24px; background: #111827; color: #fff; }
    .layout { padding: 16px 24px; display: grid; gap: 16px; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
    .card { background: #fff; border-radius: 10px; padding: 14px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
    .title { font-size: 12px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
    .value { margin-top: 6px; font-size: 24px; font-weight: bold; }
    .advisory { font-size: 14px; line-height: 1.4; }
    .panel { background: #fff; border-radius: 10px; padding: 8px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
    .controls { display: flex; gap: 10px; align-items: center; background: #fff; padding: 12px; border-radius: 10px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
    select, button { padding: 6px 10px; }
    .alert { padding: 10px; border-radius: 8px; background: #fef3c7; color: #92400e; display: none; }
  </style>
</head>
<body>
  <header>
    <h2 style="margin:0;">EcoStream: Real-Time Urban Air Quality Dashboard</h2>
    <small id="updatedAt">Waiting for first data update...</small>
  </header>
  <main class="layout">
    <div class="cards">
      <div class="card">
        <div class="title">Average AQI</div>
        <div class="value" id="avgAqi">--</div>
      </div>
      <div class="card">
        <div class="title">Worst Category</div>
        <div class="value" id="worstCategory">--</div>
      </div>
      <div class="card">
        <div class="title">Monitored Sensors</div>
        <div class="value" id="sensorCount">--</div>
      </div>
      <div class="card">
        <div class="title">Health Advisory</div>
        <div class="advisory" id="healthAdvisory">--</div>
      </div>
    </div>
    <div id="alertBox" class="alert"></div>
    <section class="panel"><div id="mapChart"></div></section>
    <div class="controls">
      <label for="pollutant">Pollutant:</label>
      <select id="pollutant">
        <option value="pm25">PM2.5</option>
        <option value="pm10">PM10</option>
        <option value="co2">CO2</option>
        <option value="temperature">Temperature</option>
        <option value="humidity">Humidity</option>
      </select>
      <button onclick="refreshData()">Refresh now</button>
    </div>
    <section class="panel"><div id="trendChart"></div></section>
  </main>
  <script>
    async function refreshData() {
      const pollutant = document.getElementById("pollutant").value;
      const res = await fetch(`/api/dashboard-data?pollutant=${pollutant}`);
      const payload = await res.json();

      document.getElementById("avgAqi").innerText = payload.kpis.avg_aqi;
      document.getElementById("worstCategory").innerText = payload.kpis.worst_category;
      document.getElementById("sensorCount").innerText = payload.kpis.sensor_count;
      document.getElementById("healthAdvisory").innerText = payload.kpis.health_advisory;
      document.getElementById("updatedAt").innerText = `Last update: ${payload.kpis.last_update}`;

      const alertBox = document.getElementById("alertBox");
      if (payload.alert.message) {
        alertBox.style.display = "block";
        alertBox.innerText = payload.alert.message;
      } else {
        alertBox.style.display = "none";
      }

      Plotly.react("mapChart", payload.map_figure.data, payload.map_figure.layout, {responsive: true});
      Plotly.react("trendChart", payload.trend_figure.data, payload.trend_figure.layout, {responsive: true});
    }

    document.getElementById("pollutant").addEventListener("change", refreshData);
    refreshData();
    setInterval(refreshData, 30000);
  </script>
</body>
</html>
"""
