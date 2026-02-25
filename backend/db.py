"""Database client — abstracts Supabase with SQLite fallback.

Uses Supabase when configured, otherwise falls back to SQLite for
local development. All DB access goes through this module.
"""

from __future__ import annotations

import logging
import sqlite3
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


class DBClient(ABC):
    """Abstract database interface."""

    @abstractmethod
    def init_schema(self) -> None: ...

    @abstractmethod
    def register_user(self, name: str, email: Optional[str] = None) -> str: ...

    @abstractmethod
    def validate_id(self, looped_id: str) -> bool: ...

    @abstractmethod
    def link_telegram(self, looped_id: str, telegram_id: str) -> bool: ...

    @abstractmethod
    def get_linked_user(self, telegram_id: str) -> Optional[str]: ...

    @abstractmethod
    def log_query(self, looped_id: str, query: str, tokens: int = 0, cost: float = 0.0) -> None: ...

    @abstractmethod
    def get_query_count_today(self, looped_id: str) -> int: ...

    @abstractmethod
    def list_users(self) -> list[dict]: ...

    @abstractmethod
    def deactivate_user(self, looped_id: str) -> bool: ...


def _generate_id() -> str:
    """Generate a unique LoopedAI ID."""
    return f"LAI-{uuid.uuid4().hex[:8].upper()}"


def _utcnow() -> str:
    """ISO timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


# ── SQLite Implementation ─────────────────────────────────────────────


class SQLiteClient(DBClient):
    """SQLite-backed database for local development."""

    def __init__(self, db_path: str = "loopedai.db"):
        self._path = db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def init_schema(self) -> None:
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    looped_id   TEXT PRIMARY KEY,
                    telegram_id TEXT UNIQUE,
                    name        TEXT NOT NULL,
                    email       TEXT,
                    plan        TEXT DEFAULT 'free',
                    daily_limit INTEGER DEFAULT 20,
                    active      INTEGER DEFAULT 1,
                    created_at  TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS queries (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    looped_id   TEXT NOT NULL REFERENCES users(looped_id),
                    query_text  TEXT NOT NULL,
                    tokens_used INTEGER DEFAULT 0,
                    cost_usd    REAL DEFAULT 0.0,
                    created_at  TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_queries_date
                    ON queries(looped_id, created_at);
            """)
        logger.info("SQLite schema initialized at %s", self._path)

    def register_user(self, name: str, email: Optional[str] = None) -> str:
        lid = _generate_id()
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO users (looped_id, name, email, created_at) VALUES (?, ?, ?, ?)",
                (lid, name, email, _utcnow()),
            )
        return lid

    def validate_id(self, looped_id: str) -> bool:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT 1 FROM users WHERE looped_id = ? AND active = 1",
                (looped_id.upper(),),
            ).fetchone()
        return row is not None

    def link_telegram(self, looped_id: str, telegram_id: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE users SET telegram_id = ? WHERE looped_id = ? AND active = 1",
                (telegram_id, looped_id.upper()),
            )
        return cur.rowcount > 0

    def get_linked_user(self, telegram_id: str) -> Optional[str]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT looped_id FROM users WHERE telegram_id = ? AND active = 1",
                (telegram_id,),
            ).fetchone()
        return row["looped_id"] if row else None

    def log_query(self, looped_id: str, query: str, tokens: int = 0, cost: float = 0.0) -> None:
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO queries (looped_id, query_text, tokens_used, cost_usd, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (looped_id, query, tokens, cost, _utcnow()),
            )

    def get_query_count_today(self, looped_id: str) -> int:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with self._conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM queries WHERE looped_id = ? AND created_at >= ?",
                (looped_id, today),
            ).fetchone()
        return row["cnt"] if row else 0

    def list_users(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT looped_id, name, email, telegram_id, plan, daily_limit, active, created_at "
                "FROM users ORDER BY created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def deactivate_user(self, looped_id: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute(
                "UPDATE users SET active = 0 WHERE looped_id = ?",
                (looped_id.upper(),),
            )
        return cur.rowcount > 0


# ── Supabase Implementation ───────────────────────────────────────────


class SupabaseClient(DBClient):
    """Supabase-backed database for production."""

    def __init__(self, url: str, key: str):
        from supabase import create_client

        self._client = create_client(url, key)
        logger.info("Supabase client initialized")

    def init_schema(self) -> None:
        # Schema managed via Supabase Dashboard migrations
        logger.info("Supabase schema managed externally — skipping init")

    def register_user(self, name: str, email: Optional[str] = None) -> str:
        lid = _generate_id()
        self._client.table("users").insert({
            "looped_id": lid,
            "name": name,
            "email": email,
            "created_at": _utcnow(),
        }).execute()
        return lid

    def validate_id(self, looped_id: str) -> bool:
        res = (
            self._client.table("users")
            .select("looped_id")
            .eq("looped_id", looped_id.upper())
            .eq("active", True)
            .execute()
        )
        return len(res.data) > 0

    def link_telegram(self, looped_id: str, telegram_id: str) -> bool:
        res = (
            self._client.table("users")
            .update({"telegram_id": telegram_id})
            .eq("looped_id", looped_id.upper())
            .eq("active", True)
            .execute()
        )
        return len(res.data) > 0

    def get_linked_user(self, telegram_id: str) -> Optional[str]:
        res = (
            self._client.table("users")
            .select("looped_id")
            .eq("telegram_id", telegram_id)
            .eq("active", True)
            .execute()
        )
        return res.data[0]["looped_id"] if res.data else None

    def log_query(self, looped_id: str, query: str, tokens: int = 0, cost: float = 0.0) -> None:
        self._client.table("queries").insert({
            "looped_id": looped_id,
            "query_text": query,
            "tokens_used": tokens,
            "cost_usd": cost,
            "created_at": _utcnow(),
        }).execute()

    def get_query_count_today(self, looped_id: str) -> int:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%dT00:00:00")
        res = (
            self._client.table("queries")
            .select("id", count="exact")
            .eq("looped_id", looped_id)
            .gte("created_at", today)
            .execute()
        )
        return res.count or 0

    def list_users(self) -> list[dict]:
        res = (
            self._client.table("users")
            .select("looped_id, name, email, telegram_id, plan, daily_limit, active, created_at")
            .order("created_at", desc=True)
            .execute()
        )
        return res.data

    def deactivate_user(self, looped_id: str) -> bool:
        res = (
            self._client.table("users")
            .update({"active": False})
            .eq("looped_id", looped_id.upper())
            .execute()
        )
        return len(res.data) > 0


# ── Factory ────────────────────────────────────────────────────────────


def create_db(supabase_url: str = "", supabase_key: str = "", sqlite_path: str = "loopedai.db") -> DBClient:
    """Create the appropriate DB client based on available config.

    Returns SupabaseClient if credentials are provided, otherwise SQLite.
    Idempotent — safe to call multiple times.
    """
    if supabase_url and supabase_key:
        return SupabaseClient(supabase_url, supabase_key)
    logger.info("No Supabase credentials — using SQLite fallback")
    return SQLiteClient(sqlite_path)
