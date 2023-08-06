import csv
import sqlite3


# Read data from CSV and insert into SQLite database
def read_csv_and_insert_to_db(csv_file: str, database_file: str, table_name: str) -> None:
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    with open(csv_file, "r") as f:
        csv_reader = csv.DictReader(f)
        headers = csv_reader.fieldnames

        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(headers)})")

        for row in csv_reader:
            values = [row[header] for header in headers]
            placeholders = ", ".join(["?"] * len(headers))
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

    conn.commit()
    conn.close()


# Export data from SQLite database to CSV
def export_db_to_csv(database_file: str, table_name: str, csv_file: str) -> None:
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    with open(csv_file, "w", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([description[0] for description in cursor.description])
        csv_writer.writerows(rows)

    conn.close()
