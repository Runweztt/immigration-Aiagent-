"""FastAPI backend server — all business logic lives here.

The Telegram bot talks to this server on localhost:8000.
This server handles: auth, rate limiting, Claude calls, and query logging.
No API keys are stored in the bot — they live here only.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.config import get_config
from backend.db import DBClient, create_db
from backend.llm_client import query_claude
from backend.rate_limiter import check_rate_limit

logger = logging.getLogger(__name__)

# ── Module-level state (initialized on startup) ───────────────────────

_db: DBClient | None = None


def _get_db() -> DBClient:
    """Get the initialized DB client."""
    if _db is None:
        raise RuntimeError("DB not initialized — server not started")
    return _db


# ── Lifespan ──────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Initialize DB on startup, cleanup on shutdown."""
    global _db
    cfg = get_config()
    _db = create_db(cfg.supabase_url, cfg.supabase_key)
    _db.init_schema()
    logger.info("Backend ready — DB initialized")
    yield
    logger.info("Backend shutting down")


# ── App ───────────────────────────────────────────────────────────────


app = FastAPI(
    title="LoopedAI Immigration API",
    version="2.0.0",
    lifespan=lifespan,
)


# ── Models ────────────────────────────────────────────────────────────


class VerifyRequest(BaseModel):
    telegram_id: str


class LinkRequest(BaseModel):
    looped_id: str
    telegram_id: str


class QueryRequest(BaseModel):
    telegram_id: str
    text: str


class StatusResponse(BaseModel):
    status: str
    looped_id: str | None = None
    remaining: int | None = None


# ── Endpoints ─────────────────────────────────────────────────────────


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


@app.post("/auth/verify", response_model=StatusResponse)
async def verify_user(req: VerifyRequest):
    """Check if a Telegram user is linked to a LoopedAI ID."""
    db = _get_db()
    looped_id = db.get_linked_user(req.telegram_id)

    if looped_id:
        return StatusResponse(status="verified", looped_id=looped_id)
    return StatusResponse(status="needs_id")


@app.post("/auth/link", response_model=StatusResponse)
async def link_user(req: LinkRequest):
    """Validate a LoopedAI ID and link it to a Telegram account."""
    db = _get_db()

    if not db.validate_id(req.looped_id):
        raise HTTPException(status_code=404, detail="Invalid LoopedAI ID")

    if not db.link_telegram(req.looped_id, req.telegram_id):
        raise HTTPException(status_code=400, detail="Could not link account")

    return StatusResponse(status="verified", looped_id=req.looped_id.upper())


@app.post("/query")
async def process_query(req: QueryRequest):
    """Process an immigration query through Claude.

    Validates user, checks rate limit, calls Claude, logs the query.
    """
    db = _get_db()
    cfg = get_config()

    # 1. Verify user
    looped_id = db.get_linked_user(req.telegram_id)
    if not looped_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # 2. Check rate limit
    limit = check_rate_limit(db, looped_id, cfg.daily_query_limit)
    if not limit.allowed:
        raise HTTPException(status_code=429, detail=limit.message)

    # 3. Call Claude
    try:
        result = query_claude(
            api_key=cfg.anthropic_key,
            user_message=req.text,
            model=cfg.anthropic_model,
            max_tokens=cfg.max_tokens_per_query,
        )
    except Exception as e:
        logger.error("Claude API error: %s", e)
        raise HTTPException(status_code=502, detail="AI service temporarily unavailable")

    # 4. Log query
    db.log_query(looped_id, req.text, result.total_tokens, result.estimated_cost)

    return {
        "response": result.text,
        "tokens_used": result.total_tokens,
        "cost_usd": round(result.estimated_cost, 6),
        "queries_remaining": limit.remaining,
    }
