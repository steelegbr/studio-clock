import json
import logging
from datetime import timedelta
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.utils import timezone

from studioclock.models import Clock

logger = logging.getLogger(__name__)
REQUEST_TIMEOUT_SECONDS = 3
POLL_INTERVAL = timedelta(days=1)
OPEN_METEO_GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CONDITIONS = {
    0: ("Clear sky", "bi-sun-fill"),
    1: ("Mainly clear", "bi-sun-fill"),
    2: ("Partly cloudy", "bi-cloud-sun-fill"),
    3: ("Overcast", "bi-cloud-fill"),
    45: ("Fog", "bi-cloud-fog-fill"),
    48: ("Rime fog", "bi-cloud-fog-fill"),
    51: ("Light drizzle", "bi-cloud-drizzle-fill"),
    53: ("Drizzle", "bi-cloud-drizzle-fill"),
    55: ("Heavy drizzle", "bi-cloud-drizzle-fill"),
    56: ("Freezing drizzle", "bi-cloud-sleet-fill"),
    57: ("Heavy freezing drizzle", "bi-cloud-sleet-fill"),
    61: ("Light rain", "bi-cloud-rain-fill"),
    63: ("Rain", "bi-cloud-rain-fill"),
    65: ("Heavy rain", "bi-cloud-rain-fill"),
    66: ("Freezing rain", "bi-cloud-sleet-fill"),
    67: ("Heavy freezing rain", "bi-cloud-sleet-fill"),
    71: ("Light snow", "bi-cloud-snow-fill"),
    73: ("Snow", "bi-cloud-snow-fill"),
    75: ("Heavy snow", "bi-cloud-snow-fill"),
    77: ("Snow grains", "bi-cloud-snow-fill"),
    80: ("Light rain showers", "bi-cloud-rain-fill"),
    81: ("Rain showers", "bi-cloud-rain-fill"),
    82: ("Heavy rain showers", "bi-cloud-rain-fill"),
    85: ("Light snow showers", "bi-cloud-snow-fill"),
    86: ("Heavy snow showers", "bi-cloud-snow-fill"),
    95: ("Thunderstorm", "bi-cloud-lightning-rain-fill"),
    96: ("Thunderstorm with hail", "bi-cloud-lightning-rain-fill"),
    99: ("Heavy thunderstorm with hail", "bi-cloud-lightning-rain-fill"),
}


def _fetch_json(url):
    request = Request(url, headers={"User-Agent": "StudioClock/1.0"})
    with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise TypeError("Weather API response must be an object")
    return result


def _resolve_location(location):
    query = urlencode(
        {"name": location, "count": 1, "language": "en", "format": "json"}
    )
    results = _fetch_json(f"{OPEN_METEO_GEOCODING_URL}?{query}").get("results") or []
    if not results or not isinstance(results[0], dict):
        raise ValueError(f"No weather location found for {location!r}")

    result = results[0]
    latitude = float(result["latitude"])
    longitude = float(result["longitude"])
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError("Weather location coordinates are out of range")
    return latitude, longitude


def _build_forecast(data):
    daily = data.get("daily")
    if not isinstance(daily, dict):
        raise TypeError("Weather API response is missing daily forecasts")

    dates = daily.get("time")
    codes = daily.get("weather_code")
    highs = daily.get("temperature_2m_max")
    lows = daily.get("temperature_2m_min")
    if not all(
        isinstance(values, list) and len(values) >= 2
        for values in (dates, codes, highs, lows)
    ):
        raise ValueError("Weather API response does not contain two forecast days")

    days = []
    for index, label in enumerate(("Today", "Tomorrow")):
        code = int(codes[index])
        condition, icon = WEATHER_CONDITIONS.get(
            code, ("Unknown conditions", "bi-cloud-fill")
        )
        days.append(
            {
                "label": label,
                "date": str(dates[index]),
                "condition": condition,
                "icon": icon,
                "high": float(highs[index]),
                "low": float(lows[index]),
            }
        )
    return days


def weather_payload(clock: Clock) -> dict:
    if not clock.weather_location:
        return {
            "available": False,
            "location": "",
            "unit": "",
            "days": [],
            "poll_interval_seconds": int(POLL_INTERVAL.total_seconds()),
        }

    now = timezone.now()
    if (
        clock.weather_last_polled_at
        and now < clock.weather_last_polled_at + POLL_INTERVAL
    ):
        return _payload_from_clock(clock)

    try:
        if clock.weather_latitude is None or clock.weather_longitude is None:
            clock.weather_latitude, clock.weather_longitude = _resolve_location(
                clock.weather_location
            )

        query = urlencode(
            {
                "latitude": clock.weather_latitude,
                "longitude": clock.weather_longitude,
                "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                "temperature_unit": clock.weather_units,
                "timezone": "auto",
                "forecast_days": 2,
            }
        )
        forecast = _build_forecast(_fetch_json(f"{OPEN_METEO_FORECAST_URL}?{query}"))
        clock.weather_forecast = forecast
        clock.weather_last_polled_at = now
        clock.save(
            update_fields=[
                "weather_latitude",
                "weather_longitude",
                "weather_forecast",
                "weather_last_polled_at",
            ]
        )
    except (
        URLError,
        TimeoutError,
        OSError,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ):
        logger.warning(
            "Unable to update weather forecast for clock %s", clock.pk, exc_info=True
        )
        clock.weather_last_polled_at = now
        clock.save(
            update_fields=[
                "weather_latitude",
                "weather_longitude",
                "weather_last_polled_at",
            ]
        )

    return _payload_from_clock(clock)


def _payload_from_clock(clock: Clock) -> dict:
    return {
        "available": bool(clock.weather_forecast),
        "location": clock.weather_location,
        "unit": "°F" if clock.weather_units == Clock.WeatherUnits.FAHRENHEIT else "°C",
        "days": clock.weather_forecast,
        "poll_interval_seconds": int(POLL_INTERVAL.total_seconds()),
    }
