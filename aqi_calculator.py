"""AQI calculation utilities based on EPA breakpoint methodology."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class AqiBand:
    low_conc: float
    high_conc: float
    low_index: int
    high_index: int


# EPA AQI breakpoints for PM2.5 and PM10
PM25_BREAKPOINTS = [
    AqiBand(0.0, 12.0, 0, 50),
    AqiBand(12.1, 35.4, 51, 100),
    AqiBand(35.5, 55.4, 101, 150),
    AqiBand(55.5, 150.4, 151, 200),
    AqiBand(150.5, 250.4, 201, 300),
    AqiBand(250.5, 350.4, 301, 400),
    AqiBand(350.5, 500.4, 401, 500),
]

PM10_BREAKPOINTS = [
    AqiBand(0, 54, 0, 50),
    AqiBand(55, 154, 51, 100),
    AqiBand(155, 254, 101, 150),
    AqiBand(255, 354, 151, 200),
    AqiBand(355, 424, 201, 300),
    AqiBand(425, 504, 301, 400),
    AqiBand(505, 604, 401, 500),
]


def _sub_index(concentration: float, bands: list[AqiBand]) -> Optional[int]:
    """Calculate AQI sub-index for one pollutant concentration."""
    for band in bands:
        if band.low_conc <= concentration <= band.high_conc:
            return round(
                ((band.high_index - band.low_index) / (band.high_conc - band.low_conc))
                * (concentration - band.low_conc)
                + band.low_index
            )
    return None


def aqi_category(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


def health_advisory(category: str) -> str:
    guidance: Dict[str, str] = {
        "Good": "Air quality is good. Outdoor activity is safe for most people.",
        "Moderate": "Air quality is acceptable. Unusually sensitive people should limit prolonged outdoor exertion.",
        "Unhealthy for Sensitive Groups": "Sensitive groups should reduce prolonged outdoor activity.",
        "Unhealthy": "Everyone may begin to experience health effects; limit outdoor activity.",
        "Very Unhealthy": "Health alert: everyone should avoid prolonged outdoor exertion.",
        "Hazardous": "Emergency conditions: avoid outdoor activity and follow local public health guidance.",
    }
    return guidance.get(category, "No advisory available.")


def calculate_aqi(pm25: float, pm10: float) -> Tuple[int, str, str]:
    """Calculate overall AQI from PM2.5 and PM10 sub-indices."""
    pm25_index = _sub_index(pm25, PM25_BREAKPOINTS) or 0
    pm10_index = _sub_index(pm10, PM10_BREAKPOINTS) or 0
    overall = max(pm25_index, pm10_index)
    category = aqi_category(overall)
    advisory = health_advisory(category)
    return overall, category, advisory
