import os
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "app.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        )
    """)

    cur.execute("SELECT COUNT(*) as count FROM notes")
    count = cur.fetchone()["count"]

    if count == 0:
        cur.executemany(
            "INSERT INTO notes (title) VALUES (?)",
            [
                ("First note",),
                ("Second note",),
                ("Third note",),
            ]
        )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "Hello! Flask app with SQLite database is working."


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM notes ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    return jsonify([
        {"id": row["id"], "title": row["title"]}
        for row in rows
    ])


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)