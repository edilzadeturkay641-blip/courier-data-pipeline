import requests
import pandas as pd


def fetch_weather(city, latitude, longitude, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,precipitation_sum,wind_speed_10m_max",
        "timezone": "Asia/Baku"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    return pd.DataFrame({
        "city": city,
        "weather_date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_mean"],
        "rain": data["daily"]["precipitation_sum"],
        "wind_speed": data["daily"]["wind_speed_10m_max"]
    })


def get_weather_data():

    cities = {
        "Baku": (40.4093, 49.8671),
        "Ganja": (40.6828, 46.3606),
        "Sumgait": (40.5897, 49.6686),
        "Mingachevir": (40.7703, 47.0496),
        "Shaki": (41.1919, 47.1706),
        "Lankaran": (38.7543, 48.8506)
    }

    all_weather = []

    for city, (lat, lon) in cities.items():

        weather_df = fetch_weather(
            city=city,
            latitude=lat,
            longitude=lon,
            start_date="2025-01-01",
            end_date="2026-01-10"
        )

        all_weather.append(weather_df)

    return pd.concat(
        all_weather,
        ignore_index=True
    )