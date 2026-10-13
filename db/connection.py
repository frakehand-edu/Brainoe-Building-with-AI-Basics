import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        database_path = Path(current_app.config["DATABASE"])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                choice_a TEXT NOT NULL,
                choice_b TEXT NOT NULL,
                choice_c TEXT NOT NULL,
                choice_d TEXT NOT NULL,
                correct_choice TEXT NOT NULL CHECK (correct_choice IN ('a', 'b', 'c', 'd')),
                explanation TEXT NOT NULL,
                source_name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        connection.commit()
    finally:
        connection.close()


def close_db(exception: BaseException | None = None) -> None:
    database = g.pop("db", None)
    if database is not None:
        database.close()
