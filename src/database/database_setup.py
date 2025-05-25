import psycopg2
import os
import time


def get_database_connection():
    retries = 10
    delay=2
    for attempt in range(retries):
        try:
            connection = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host="database",
                port="5432"
            )
            cursor = connection.cursor()
            print("Database connection established.")
            return cursor, connection
        except psycopg2.OperationalError as e:
            print(f"Database connection failed (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)

def setup_database():
    cursor, connection = get_database_connection()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                        discord_ID TEXT PRIMARY KEY,
                        steam_id TEXT,
                        score TEXT,
                        last_updated TIMESTAMP,
                        team TEXT
                   );
                   """)
    connection.commit()
    print("Database Initialized.")
    cursor.close()
    connection.close()

def print_all():
    cursor, connection = get_database_connection()
    cursor.execute("SELECT discord_id, steam_id, score FROM users;")
    rows = cursor.fetchall()

    if not rows:
        print("No data found in the 'users' table.")
    else:
        print("Users:")
        for row in rows:
            print(f"{row[0]}|{row[1]}|{row[2]}")
    cursor.close()
    connection.close()