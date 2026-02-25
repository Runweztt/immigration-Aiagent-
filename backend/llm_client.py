"""Anthropic Claude client — thin wrapper for immigration queries.

Keeps the Anthropic API logic in one place. The API key is passed in,
never stored on disk.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

SYSTEM_PROMPT = (
    "You are an expert UK immigration solicitor assistant. "
    "Provide accurate, detailed guidance on UK immigration processes, "
    "including Indefinite Leave to Remain (ILR), British citizenship, "
    "settled and pre-settled status, visa applications, work permits, "
    "family visas, student visas, and Home Office procedures. "
    "Reference current UK immigration rules, the Immigration Act, "
    "and Home Office guidance where relevant. "
    "Always clarify that your advice is informational and recommend "
    "consulting a qualified UK immigration solicitor (OISC regulated) "
    "for legal decisions. "
    "Structure your response with clear sections when appropriate."
)


@dataclass
class LLMResponse:
    """Structured LLM response."""

    text: str
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    @property
    def estimated_cost(self) -> float:
        """Estimate USD cost (Claude 3.5 Sonnet pricing)."""
        return (self.input_tokens * 3 + self.output_tokens * 15) / 1_000_000


def query_claude(
    api_key: str,
    user_message: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 2048,
) -> LLMResponse:
    """Send a query to Claude and return the structured response.

    Args:
        api_key: Anthropic API key.
        user_message: The user's immigration question.
        model: Claude model ID.
        max_tokens: Maximum response tokens.

    Returns:
        LLMResponse with text and token usage.

    Raises:
        requests.HTTPError: If the API returns an error status.
        requests.ConnectionError: If the API is unreachable.
        requests.Timeout: If the request times out.
    """
    headers = {
        "x-api-key": api_key,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": user_message}],
    }

    resp = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    data = resp.json()
    usage = data.get("usage", {})

    return LLMResponse(
        text=data["content"][0]["text"],
        input_tokens=usage.get("input_tokens", 0),
        output_tokens=usage.get("output_tokens", 0),
    )
