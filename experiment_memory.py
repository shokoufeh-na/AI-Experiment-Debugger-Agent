
import sqlite3
import json
from datetime import datetime, timezone

DB_NAME = "experiments.db"


def initialize_database():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                experiment_name TEXT NOT NULL,
                metrics TEXT NOT NULL,
                ai_analysis TEXT NOT NULL
            )
        """)


def save_experiment(name, metrics, ai_analysis):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            INSERT INTO experiments
            (created_at, experiment_name, metrics, ai_analysis)
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                name,
                json.dumps(metrics),
                json.dumps(ai_analysis)
            )
        )
        return cursor.lastrowid


def get_experiments():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT * FROM experiments
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]
