# EcoStream: Real-Time Urban Air Quality Monitoring & Analytics Dashboard

Real-time urban air quality monitoring and analytics dashboard built with **Flask**, **Plotly**, and **SQLite** (Option A).

## What this project does

- Simulates multi-sensor air-quality readings (10 fixed locations) and refreshes data every ~30 seconds.
- Cleans/validates incoming data and standardizes timestamps.
- Computes **AQI** using EPA-style breakpoint logic (PM2.5 + PM10) and generates:
  - AQI category (e.g., `Good`, `Moderate`, `Hazardous`)
  - health advisory message
- Stores readings and AQI results in `ecostream.db` (SQLite).
- Serves a dashboard web UI with:
  - Live AQI map (Plotly scatter mapbox)
  - Trend chart for a selected pollutant
  - KPI cards (avg AQI, worst category, sensor count, last update)
  - Threshold alert banner when AQI exceeds a configured level

## Implemented modules

- `main.py` - Flask app entrypoint + background ingestion thread + API/UI routes
- `data_fetcher.py` - sensor catalog + simulated readings
- `data_processor.py` - data cleaning + type conversion
- `aqi_calculator.py` - AQI computation + category + advisory
- `database_manager.py` - SQLite schema + insert/query helpers
- `dashboard.py` - Plotly figure builders + HTML dashboard template

## Routes / API

- `GET /`  
  Returns the dashboard page.

- `GET /api/dashboard-data?pollutant=<pollutant>`  
  Returns JSON payload with KPIs, alert message, and chart figure data.
  - `pollutant` can be one of: `pm25`, `pm10`, `co2`, `temperature`, `humidity`

## How to run locally

### Prerequisites

- Python 3.x
- pip

### Install dependencies

```powershell
cd "c:\Users\kores\Downloads\Dashboard"
python -m pip install -r requirements.txt
```

### Start the server

```powershell
python main.py
```

Open in a browser:
`http://127.0.0.1:5000/`

## Notes

- This repo uses **simulated sensor data** by default (no physical IoT hardware integration).
- `ecostream.db` is generated/updated at runtime and is ignored by Git via `.gitignore`.
