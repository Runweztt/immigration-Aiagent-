"""Rate limiter — enforces per-user daily query limits.

Uses the DB client to check usage, so it works identically
with both SQLite and Supabase backends.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from backend.db import DBClient

logger = logging.getLogger(__name__)


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""

    allowed: bool
    remaining: int
    limit: int
    message: str = ""


def check_rate_limit(db: DBClient, looped_id: str, daily_limit: int = 20) -> RateLimitResult:
    """Check if a user has remaining queries for today.

    Args:
        db: Database client instance.
        looped_id: The user's LoopedAI ID.
        daily_limit: Maximum queries per day.

    Returns:
        RateLimitResult with allowed status and remaining count.
    """
    used = db.get_query_count_today(looped_id)
    remaining = max(0, daily_limit - used)

    if remaining <= 0:
        return RateLimitResult(
            allowed=False,
            remaining=0,
            limit=daily_limit,
            message=f"Daily limit reached ({daily_limit} queries). Resets at midnight UTC.",
        )

    return RateLimitResult(
        allowed=True,
        remaining=remaining - 1,  # Account for the current query
        limit=daily_limit,
    )
