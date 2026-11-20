# Bikeshare & Weather Analytics Pipeline

An end-to-end data pipeline that combines bike-share trip data with daily
weather data to show how weather affects ridership. It demonstrates batch and
incremental ingestion, dimensional modeling, orchestration, and automated testing.

![Dashboard](docs/dashboard.png)

## The problem
[One sentence: e.g. "Trip data and weather data live in separate sources, so
there's no easy way to see how rain or temperature changes demand."]

## What I built
- **Ingestion:** Python scripts pull [trip data source] and [weather API/source]
  in batch and incremental loads
- **Modeling:** dbt models turn raw data into a [star schema] with
  [fact_trips, dim_date, dim_weather, ...]
- **Orchestration:** Airflow DAGs schedule and run the whole pipeline daily
- **Quality:** automated tests in `tests/` and dbt tests, run through GitHub Actions
- **Deployment:** everything runs in Docker with one command
- **Dashboard:** [tool] dashboard showing [2-3 key views]

## Architecture
![Architecture](docs/architecture.png)
`Sources → Python extraction → [warehouse] → dbt models → Dashboard`
                     orchestrated by Airflow

## Tech stack
Python · Airflow · dbt · Docker · [warehouse: PostgreSQL?] · GitHub Actions · [dashboard tool]

## Key results
- [Number] trips and [number] days of weather processed
- [N] dbt/data quality tests passing
- Insight: [e.g. "Ridership drops ~X% on days with rain"]

## Run it locally
1. `git clone https://github.com/Aya121298/bikeshare-weather-pipeline`
2. `cp .env.example .env` and fill in your values
3. `docker compose up` [adjust to your real command]
4. Open Airflow at `http://localhost:8080` and trigger the DAG

## Project structure
`extraction/` ingestion scripts · `dags/` Airflow DAGs · `dbt/` models and tests ·
`dashboard/` dashboard files · `docker/` container setup · `tests/` unit tests · `docs/` diagrams

## License
MIT
