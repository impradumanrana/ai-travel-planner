import os
import requests
from collections import defaultdict
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError("OPENWEATHER_API_KEY is missing. Add it inside your .env file.")


def get_coordinates(place_name: str):
    """
    Convert place name into latitude and longitude using OpenWeather Geocoding API.
    """
    url = "https://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q": place_name,
        "limit": 1,
        "appid": API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
    except RequestException as error:
        raise RuntimeError(
            "Could not connect to OpenWeather Geocoding API. "
            "Check your internet connection and OPENWEATHER_API_KEY."
        ) from error

    data = response.json()

    if not data:
        raise ValueError(f"Could not find location: {place_name}")

    location = data[0]

    return {
        "name": location.get("name", place_name),
        "country": location.get("country", ""),
        "lat": location["lat"],
        "lon": location["lon"],
    }


def get_weather_forecast(lat: float, lon: float):
    """
    Get 5-day / 3-hour weather forecast from OpenWeather.
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
    except RequestException as error:
        raise RuntimeError(
            "Could not connect to OpenWeather Forecast API. "
            "Check your internet connection and OPENWEATHER_API_KEY."
        ) from error

    return response.json()


def group_forecast_by_day(forecast_json, days_limit=5):
    """
    Convert 3-hour forecast entries into daily summaries.
    """
    daily_data = defaultdict(list)

    for item in forecast_json["list"]:
        date = item["dt_txt"].split(" ")[0]
        daily_data[date].append(item)

    summaries = []

    for date in sorted(daily_data):
        entries = daily_data[date]
        temps = [entry["main"]["temp"] for entry in entries]
        humidity_values = [entry["main"]["humidity"] for entry in entries]
        wind_values = [entry["wind"]["speed"] for entry in entries]

        weather_descriptions = [
            entry["weather"][0]["description"] for entry in entries
        ]

        rain_count = 0
        snow_count = 0

        for entry in entries:
            main_weather = entry["weather"][0]["main"].lower()

            if "rain" in main_weather or "rain" in entry:
                rain_count += 1

            if "snow" in main_weather or "snow" in entry:
                snow_count += 1

        most_common_weather = max(
            set(weather_descriptions),
            key=weather_descriptions.count
        )

        if rain_count >= 2:
            day_type = "rainy"
        elif snow_count >= 1:
            day_type = "snowy"
        elif max(temps) >= 30:
            day_type = "hot"
        elif min(temps) <= 10:
            day_type = "cold"
        else:
            day_type = "pleasant"

        summaries.append({
            "date": date,
            "min_temp": round(min(temps), 1),
            "max_temp": round(max(temps), 1),
            "avg_humidity": round(sum(humidity_values) / len(humidity_values)),
            "avg_wind_speed": round(sum(wind_values) / len(wind_values), 1),
            "weather": most_common_weather,
            "rain_slots": rain_count,
            "snow_slots": snow_count,
            "day_type": day_type,
        })

    return summaries[:days_limit]


def get_destination_weather(place_name: str, days_limit=5):
    """
    Main weather tool function used by the agent.
    """
    location = get_coordinates(place_name)
    forecast = get_weather_forecast(location["lat"], location["lon"])
    daily_summary = group_forecast_by_day(forecast, days_limit=days_limit)

    return {
        "location": location,
        "daily_weather": daily_summary,
        "forecast_days": len(daily_summary),
    }
