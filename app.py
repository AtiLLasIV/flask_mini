import os
from flask import Flask, jsonify
import psycopg

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                )
            """)

            cur.execute("SELECT COUNT(*) FROM notes")
            count = cur.fetchone()[0]

            if count == 0:
                cur.execute(
                    "INSERT INTO notes (title) VALUES (%s), (%s), (%s)",
                    ("First note", "Second note", "Third note")
                )

        conn.commit()


@app.route("/")
def home():
    return "Hello! Flask app with PostgreSQL database is working."


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/notes")
def get_notes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title FROM notes ORDER BY id")
            rows = cur.fetchall()

    return jsonify([
        {"id": row[0], "title": row[1]}
        for row in rows
    ])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("APP_PORT", "5001")))
