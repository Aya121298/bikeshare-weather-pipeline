"""
Load raw CSV files into Postgres (raw schema).

Everything lands as TEXT: the raw layer stores data exactly as it was
received. Converting types (dates, numbers) happens later, in dbt.
"""

import csv
import os

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

# table name in Postgres -> CSV file to load into it
CSV_FILES = {
    "weather_daily": "extraction/weather_output.csv",
    "trips": "extraction/trips_raw_202406.csv",
}


def get_connection():
    """Open a connection to Postgres using the values from .env."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def load_csv(conn, csv_path: str, table_name: str) -> None:
    """Recreate raw.<table_name> and fill it with the CSV's contents."""
    # Read just the header row so the table columns match the file
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        header = next(csv.reader(f))

    columns = sql.SQL(", ").join(
        sql.SQL("{} TEXT").format(sql.Identifier(col)) for col in header
    )

    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
        cur.execute(
            sql.SQL("DROP TABLE IF EXISTS raw.{}").format(sql.Identifier(table_name))
        )
        cur.execute(
            sql.SQL("CREATE TABLE raw.{} ({})").format(
                sql.Identifier(table_name), columns
            )
        )

        # COPY streams the whole file into Postgres in one fast operation
        copy_sql = sql.SQL(
            "COPY raw.{} FROM STDIN WITH (FORMAT csv, HEADER true)"
        ).format(sql.Identifier(table_name)).as_string(conn)
        with open(csv_path, "r", encoding="utf-8") as f:
            cur.copy_expert(copy_sql, f)

        cur.execute(
            sql.SQL("SELECT COUNT(*) FROM raw.{}").format(sql.Identifier(table_name))
        )
        row_count = cur.fetchone()[0]

    conn.commit()
    print(f"Loaded {row_count} rows into raw.{table_name}")


if __name__ == "__main__":
    conn = get_connection()
    try:
        for table_name, csv_path in CSV_FILES.items():
            load_csv(conn, csv_path, table_name)
    finally:
        conn.close()