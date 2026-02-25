"""LoopedAI ID authentication and user management.

Handles user registration, ID validation, and Telegram linking
using a lightweight SQLite database.
"""

import os
import sqlite3
import uuid
from datetime import datetime

DB_PATH = os.getenv("LOOPEDAI_DB_PATH", "/opt/loopedai-bot/loopedai.db")


def _get_conn():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            looped_id TEXT PRIMARY KEY,
            telegram_id TEXT UNIQUE,
            name TEXT NOT NULL,
            email TEXT,
            registered_at TEXT NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            looped_id TEXT NOT NULL,
            query_text TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (looped_id) REFERENCES users(looped_id)
        )
    """)
    conn.commit()
    conn.close()


def register_user(name: str, email: str = None, telegram_id: str = None) -> str:
    """Register a new user and return their LoopedAI ID.

    Args:
        name: User's display name.
        email: Optional email address.
        telegram_id: Optional Telegram user ID to pre-link.

    Returns:
        The generated LoopedAI ID (format: LAI-XXXXXXXX).
    """
    conn = _get_conn()
    looped_id = f"LAI-{uuid.uuid4().hex[:8].upper()}"
    conn.execute(
        "INSERT INTO users (looped_id, telegram_id, name, email, registered_at) VALUES (?, ?, ?, ?, ?)",
        (looped_id, telegram_id, name, email, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
    return looped_id


def validate_id(looped_id: str) -> bool:
    """Check if a LoopedAI ID is valid and active."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT active FROM users WHERE looped_id = ? AND active = 1",
        (looped_id.upper(),),
    ).fetchone()
    conn.close()
    return row is not None


def link_telegram(looped_id: str, telegram_id: str) -> bool:
    """Link a Telegram user ID to a LoopedAI ID.

    Returns True if successful, False if ID not found or inactive.
    """
    conn = _get_conn()
    cur = conn.execute(
        "UPDATE users SET telegram_id = ? WHERE looped_id = ? AND active = 1",
        (telegram_id, looped_id.upper()),
    )
    conn.commit()
    success = cur.rowcount > 0
    conn.close()
    return success


def is_telegram_linked(telegram_id: str) -> str | None:
    """Check if a Telegram user is already linked to a LoopedAI ID.

    Returns the LoopedAI ID if linked, None otherwise.
    """
    conn = _get_conn()
    row = conn.execute(
        "SELECT looped_id FROM users WHERE telegram_id = ? AND active = 1",
        (telegram_id,),
    ).fetchone()
    conn.close()
    return row["looped_id"] if row else None


def log_query(looped_id: str, query_text: str):
    """Log a user query for analytics."""
    conn = _get_conn()
    conn.execute(
        "INSERT INTO queries (looped_id, query_text, timestamp) VALUES (?, ?, ?)",
        (looped_id, query_text, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def list_users():
    """List all registered users."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT looped_id, name, email, telegram_id, registered_at, active FROM users ORDER BY registered_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def deactivate_user(looped_id: str) -> bool:
    """Deactivate a user's access."""
    conn = _get_conn()
    cur = conn.execute(
        "UPDATE users SET active = 0 WHERE looped_id = ?", (looped_id.upper(),)
    )
    conn.commit()
    conn.close()
    return cur.rowcount > 0
