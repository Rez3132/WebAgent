import sqlite3
from pathlib import Path
from threading import Lock
from typing import Any

DB_PATH = Path(__file__).parent / "reza_agent.db"
_lock = Lock()


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with _lock, _conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                goal TEXT NOT NULL,
                status TEXT NOT NULL,
                result TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS approvals (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )


def execute(sql: str, params: tuple = ()) -> None:
    with _lock, _conn() as conn:
        conn.execute(sql, params)
        conn.commit()


def fetchone(sql: str, params: tuple = ()) -> dict[str, Any] | None:
    with _lock, _conn() as conn:
        row = conn.execute(sql, params).fetchone()
        return dict(row) if row else None


def fetchall(sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    with _lock, _conn() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
