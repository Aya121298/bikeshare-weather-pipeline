"""
Extract daily weather data from the Open-Meteo API and save it locally
as a CSV, matching the dim_weather table in our data model.
"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load variables from .env (WEATHER_API_BASE_URL, etc.)
load_dotenv()

WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL")

# Chicago coordinates — change these if you pick a different city
# to match your bike-share data source
LATITUDE = 41.8781
LONGITUDE = -87.6298


def fetch_weather(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily weather for a date range and return it as a DataFrame
    shaped to match the dim_weather table.
    """
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,precipitation_sum,wind_speed_10m_max,weather_code",
        "timezone": "America/Chicago",
    }

    response = requests.get(WEATHER_API_BASE_URL, params=params)
    response.raise_for_status()  # crash loudly if the API call failed

    data = response.json()["daily"]

    df = pd.DataFrame({
        "full_date": data["time"],
        "temperature_c": data["temperature_2m_mean"],
        "precipitation_mm": data["precipitation_sum"],
        "wind_speed_kmh": data["wind_speed_10m_max"],
        "weather_code": data["weather_code"],
    })

    return df


if __name__ == "__main__":
    # Pull one month of data as a test run
    weather_df = fetch_weather(start_date="2024-06-01", end_date="2024-06-30")

    output_path = "extraction/weather_output.csv"
    weather_df.to_csv(output_path, index=False)

    print(f"Saved {len(weather_df)} rows to {output_path}")
    print(weather_df.head())