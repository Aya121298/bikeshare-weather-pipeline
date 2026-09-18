# Data Model

This project uses a **star schema**: one central fact table surrounded by
dimension tables that describe the context of each event.

- **Fact table** — records events (bike trips). Large, numeric, mostly IDs.
- **Dimension tables** — describe the who/what/where/when. Small, descriptive.

Fact tables link to dimension tables via IDs, so descriptive details live in
one place instead of being repeated across millions of rows.

## Fact Table

### `fact_trips`
One row = one bike trip.

| Column | Type | Description |
|---|---|---|
| trip_id | string | Unique identifier for the trip |
| start_station_id | int | FK → dim_station |
| end_station_id | int | FK → dim_station |
| date_id | int | FK → dim_date |
| start_time | timestamp | Trip start time |
| end_time | timestamp | Trip end time |
| trip_duration_seconds | int | Duration of the trip |
| bike_type | string | e.g. classic, electric |

## Dimension Tables

### `dim_station`
One row = one bike station.

| Column | Type | Description |
|---|---|---|
| station_id | int | Primary key |
| station_name | string | Human-readable station name |
| latitude | float | Station latitude |
| longitude | float | Station longitude |

### `dim_date`
One row = one calendar day. Standard date dimension enabling easy
grouping/filtering (weekday vs weekend, month, year) without doing date
math in every query.

| Column | Type | Description |
|---|---|---|
| date_id | int | Primary key |
| full_date | date | The actual date |
| day_of_week | string | e.g. Monday |
| month | int | 1-12 |
| year | int | e.g. 2026 |
| is_weekend | boolean | True if Saturday/Sunday |

### `dim_weather`
One row = one weather reading for one date. Kept separate from `dim_date`
because weather comes from a different source (a different API, different
refresh logic) even though it shares the same grain (one row per day).
Keeping it separate also means hourly weather or multiple cities could be
added later without redesigning `dim_date`.

| Column | Type | Description |
|---|---|---|
| date_id | int | FK → dim_date |
| temperature_c | float | Daily temperature |
| precipitation_mm | float | Daily precipitation |
| wind_speed_kmh | float | Daily wind speed |
| weather_condition | string | e.g. clear, rain, snow |

## Relationships

\`\`\`
fact_trips.start_station_id  -> dim_station.station_id
fact_trips.end_station_id    -> dim_station.station_id
fact_trips.date_id           -> dim_date.date_id
dim_weather.date_id          -> dim_date.date_id
\`\`\`