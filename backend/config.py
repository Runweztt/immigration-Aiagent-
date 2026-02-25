"""Centralized configuration — single source of truth for all settings.

All secrets load from environment variables. On VPS, the .env file
should only contain the Supabase URL and service_role key. The Anthropic
key is fetched from Supabase Vault at runtime.
"""

import os
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    """Immutable application configuration."""

    # Supabase
    supabase_url: str = field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    supabase_key: str = field(default_factory=lambda: os.getenv("SUPABASE_SERVICE_KEY", ""))

    # Telegram
    telegram_token: str = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN", ""))

    # Anthropic (fallback: load from env if Vault unavailable)
    anthropic_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"))

    # Backend
    api_host: str = "127.0.0.1"
    api_port: int = 8000

    # Rate limiting
    daily_query_limit: int = 20
    max_tokens_per_query: int = 2048


@lru_cache(maxsize=1)
def get_config() -> Config:
    """Return a cached, immutable Config instance."""
    return Config()
