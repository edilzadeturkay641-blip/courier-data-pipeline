from api import get_weather_data
from db import get_engine

try:
    weather = get_weather_data()

    print(weather.head())
    print(weather.shape)

    engine = get_engine()

    weather.to_sql(
        "weather",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Weather loaded successfully! - load_api.py:19")

except Exception as e:
    print("ERROR: - load_api.py:22")
    print(e)