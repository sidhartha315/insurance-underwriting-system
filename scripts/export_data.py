import sqlite3
import csv
import json
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "insurance.db"

OUTPUT_DIR = BASE_DIR / "outputs" / "datasets"
CSV_DIR = OUTPUT_DIR / "csv"
JSON_DIR = OUTPUT_DIR / "json"
SQL_DIR = OUTPUT_DIR / "sql"

# Create output folders
CSV_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR.mkdir(parents=True, exist_ok=True)
SQL_DIR.mkdir(parents=True, exist_ok=True)


def export_database():

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # Get all database tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = [row["name"] for row in cursor.fetchall()]

    print("\nDATABASE EXPORT STARTED")
    print("=" * 45)

    for table in tables:

        cursor.execute(f'SELECT * FROM "{table}"')

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        # Export CSV
        csv_path = CSV_DIR / f"{table}.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)

            for row in rows:
                writer.writerow([row[column] for column in columns])

        # Export JSON
        json_path = JSON_DIR / f"{table}.json"

        json_records = [
            dict(row) for row in rows
        ]

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(
                json_records,
                file,
                indent=4,
                default=str
            )

        print(f"{table}: {len(rows)} records exported")

    # Export SQL seed file
    sql_path = SQL_DIR / "insurance_seed.sql"

    with open(sql_path, "w", encoding="utf-8") as file:
        for statement in connection.iterdump():
            file.write(statement + "\n")

    connection.close()

    print("=" * 45)
    print("DATABASE EXPORT COMPLETED")
    print(f"CSV files : {CSV_DIR}")
    print(f"JSON files: {JSON_DIR}")
    print(f"SQL file  : {sql_path}")


if __name__ == "__main__":
    export_database()