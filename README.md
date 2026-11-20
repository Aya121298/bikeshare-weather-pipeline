# Bikeshare & Weather Analytics Pipeline

A data pipeline that combines bike-share trip data with daily weather data
to analyze how weather affects ridership. Built to demonstrate batch and
incremental ingestion, dimensional modeling, and orchestration.

## Stack
Python · PostgreSQL 15 · Apache Airflow 2.9 · dbt · Docker Compose

## Pipeline
1. `extraction/extract_trips.py`: pulls bike-share trip data from [source]
2. `extraction/extract_weather.py`: pulls daily weather data from [source]
3. `extraction/load_raw.py`: loads both into raw tables in PostgreSQL
4. `dbt/`: [describe your models once you check the folder]
5. `dags/`: Airflow DAG(s) that schedule the pipeline

## Run locally
1. `cp .env.example .env` and set the Postgres credentials
2. `docker compose -f docker/docker-compose.yml --env-file .env up`
3. Open Airflow at http://localhost:8080

## Status
Work in progress. Planned: data quality tests, CI with GitHub Actions,
and a dashboard on top of the modeled tables.

## License
MIT
