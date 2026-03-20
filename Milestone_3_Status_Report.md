# Milestone 3 - Status Report 1

**Course Project:** EcoStream - Real-Time Urban Air Quality Monitoring and Analytics Dashboard  
**Student:** [Your Name]  
**Due Date:** 03/20/2026  

---

## 1) Repository Link

**Repository URL:** [Paste your GitHub/GitLab link here]

The repository contains the current implementation of the Flask-based dashboard system and related modules for data ingestion, processing, AQI computation, storage, and visualization.

> Add a screenshot of your repository homepage and commit activity.

---

## 2) Evidence of Commits

Below is a commit evidence summary (replace with your actual commit list from Git):

1. **Initial project scaffold**  
   - Added project structure and Python entrypoint.
2. **Implemented AQI calculation module**  
   - Added pollutant breakpoint logic, AQI category mapping, and health advisory generation.
3. **Implemented data ingestion and simulation**  
   - Added sensor catalog and simulated real-time readings at multiple city locations.
4. **Implemented data cleaning and validation**  
   - Added timestamp normalization, numeric parsing, and invalid row filtering.
5. **Implemented SQLite persistence layer**  
   - Added schema creation, insert/read helpers, and query functions for latest snapshot and history.
6. **Implemented Flask dashboard and API route**  
   - Added interactive dashboard UI and `/api/dashboard-data` endpoint with Plotly chart payloads.
7. **Dependency/runtime fixes**  
   - Installed required packages and resolved JSON serialization issue in Plotly figure output.

> Add:
> - screenshot of `git log --oneline`
> - screenshot of commit graph/history page
> - screenshot showing multiple files/modules changed

---

## 3) Implemented Modules (with Evidence)

The following modules are currently implemented and integrated:

- **`main.py`**  
  - Flask app startup, routing, background ingestion loop, KPI and alert aggregation.
- **`data_fetcher.py`**  
  - Multi-sensor simulated data stream (`PM2.5`, `PM10`, `CO2`, temperature, humidity) refreshed every 30s.
- **`data_processor.py`**  
  - DataFrame creation, type cleaning, null handling, and timestamp standardization.
- **`aqi_calculator.py`**  
  - EPA-style AQI computation for PM2.5 and PM10 with category + health advisory output.
- **`database_manager.py`**  
  - SQLite table initialization, inserts, recent-history queries, latest sensor snapshot retrieval.
- **`dashboard.py`**  
  - Plotly heatmap and trend figure builders plus browser-rendered dashboard HTML UI.

**Demo evidence available from current run:**
- Application is running at `http://127.0.0.1:5000/`
- API endpoint `GET /api/dashboard-data?pollutant=pm25` returns:
  - valid KPI payload
  - sensor count = 10
  - average AQI value
  - map and trend chart data

> Add screenshots:
> 1. Running Flask terminal output  
> 2. Dashboard browser page (map + KPI cards)  
> 3. API JSON response (optional but recommended)

---

## 4) What Is Complete

The following components are complete for this milestone stage:

- Project architecture for Option A (Flask + Plotly + SQLite)
- Core real-time ingestion loop (simulated source)
- Data cleaning and validation pipeline
- AQI calculation + category/advisory logic
- SQLite storage schema and query layer
- Initial interactive dashboard UI (KPI cards, map, trend chart, alert banner)
- Pollutant selector and periodic auto-refresh behavior
- Base dependency setup via `requirements.txt`

---

## 5) What Is In Progress

The following components are currently under development:

- Comparative location analysis (side-by-side sensor comparison)
- Historical trend comparison against previous week averages
- User-configurable threshold alerts from the UI
- Optional real API integration (in addition to simulator fallback)
- UI polish and performance optimization for smoother updates under continuous runtime

---

## 6) Problems Encountered and Solutions

### Problem 1: Missing runtime dependency (`plotly`)
- **Why it occurred:** The module was referenced before package installation in the local environment.
- **Resolution:** Installed dependencies using `pip install -r requirements.txt`.

### Problem 2: Flask API returned HTTP 500 during JSON response
- **Why it occurred:** Plotly figure dictionaries contained NumPy arrays, which are not directly JSON serializable by Flask’s default encoder.
- **Resolution:** Converted Plotly figure objects using `json.loads(fig.to_json())` before returning in API payload.

### Problem 3: Reliability of live data source in early stage
- **Why it occurred:** External APIs can be unavailable or inconsistent during development.
- **Resolution:** Implemented a simulated data fallback stream so dashboard and storage pipelines can be tested continuously while API integration is still in progress.

---

## Progress Summary

Development has started successfully and aligns with the approved design plan. The project already includes functioning core modules (ingestion, processing, AQI analytics, database persistence, and initial dashboard visualization). The system is actively running in real time with modular code organization and clear next tasks for milestone continuation.

