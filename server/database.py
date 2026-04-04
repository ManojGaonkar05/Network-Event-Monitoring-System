"""SQLite persistence for monitoring snapshots."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "network_logs.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                latency REAL,
                packet_loss REAL,
                status TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def insert_log(
    node_id: str,
    latency: float | None,
    packet_loss: float | None,
    status: str,
) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO logs (node_id, latency, packet_loss, status)
            VALUES (?, ?, ?, ?)
            """,
            (node_id, latency, packet_loss, status),
        )
        conn.commit()
