"""
Download a month of Divvy (Chicago bike-share) trip data and save the
raw CSV locally. Transformation into the fact_trips table happens later,
in dbt — this script's only job is safely getting the raw data.
"""

import io
import zipfile
import requests

# Matches the June 2024 month we already pulled weather data for
TRIP_DATA_URL = "https://divvy-tripdata.s3.amazonaws.com/202406-divvy-tripdata.zip"
OUTPUT_PATH = "extraction/trips_raw_202406.csv"


def download_trip_data(url: str, output_path: str) -> None:
    """
    Download a zipped CSV of trip data and extract it directly to disk,
    without ever saving the zip file itself.
    """
    response = requests.get(url)
    response.raise_for_status()  # crash loudly if the download failed

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        # Divvy's zip files contain exactly one CSV — find its name
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as source_file:
            with open(output_path, "wb") as target_file:
                target_file.write(source_file.read())


if __name__ == "__main__":
    download_trip_data(TRIP_DATA_URL, OUTPUT_PATH)
    print(f"Saved raw trip data to {OUTPUT_PATH}")