"""Telegram bot — lightweight frontend, zero API keys.

All business logic (auth, rate limiting, Claude queries) is delegated
to the FastAPI backend on localhost:8000. This bot only handles
Telegram message routing and response formatting.
"""

from __future__ import annotations

import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
API_BASE = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


# ── Telegram Handlers ─────────────────────────────────────────────────


async def cmd_start(update: Update, _ctx: ContextTypes.DEFAULT_TYPE):
    """Handle /start — check if user is already verified."""
    tid = str(update.effective_user.id)

    try:
        resp = requests.post(f"{API_BASE}/auth/verify", json={"telegram_id": tid}, timeout=10)
        data = resp.json()
    except requests.ConnectionError:
        await update.message.reply_text("⚠️ Backend is offline. Please try again later.")
        return

    if data.get("status") == "verified":
        await update.message.reply_text(
            f"✅ Welcome back! (ID: {data['looped_id']})\n\nSend your UK immigration question."
        )
    else:
        await update.message.reply_text(
            "🇬🇧 *LoopedAI UK Immigration Assistant*\n\n"
            "Enter your *LoopedAI ID* to get started.\n"
            "Format: `LAI-XXXXXXXX`\n\n"
            "_Don't have one? Contact support to register._",
            parse_mode="Markdown",
        )


async def handle_message(update: Update, _ctx: ContextTypes.DEFAULT_TYPE):
    """Route messages: authenticate or process query."""
    tid = str(update.effective_user.id)
    text = update.message.text.strip()

    # Check if already verified
    try:
        verify = requests.post(f"{API_BASE}/auth/verify", json={"telegram_id": tid}, timeout=10)
        status = verify.json()
    except requests.ConnectionError:
        await update.message.reply_text("⚠️ Backend is offline.")
        return

    # ── Verified user → process query ──
    if status.get("status") == "verified":
        await _send_query(update, tid, text)
        return

    # ── Trying to authenticate with LAI ID ──
    if text.upper().startswith("LAI-"):
        try:
            link = requests.post(
                f"{API_BASE}/auth/link",
                json={"looped_id": text, "telegram_id": tid},
                timeout=10,
            )
            if link.status_code == 200:
                await update.message.reply_text(
                    "✅ *Access Granted!*\n\n"
                    "You're connected. Just type your UK immigration question.\n\n"
                    "_Example: I have ILR and want to apply for British citizenship_",
                    parse_mode="Markdown",
                )
            else:
                await update.message.reply_text("❌ Invalid LoopedAI ID. Check and try again.")
        except requests.ConnectionError:
            await update.message.reply_text("⚠️ Backend is offline.")
        return

    # ── Not authenticated ──
    await update.message.reply_text(
        "🔐 Please enter your LoopedAI ID first.\nFormat: `LAI-XXXXXXXX`",
        parse_mode="Markdown",
    )


async def _send_query(update: Update, telegram_id: str, query: str):
    """Send query to backend and return formatted response."""
    await update.message.reply_text("⏳ Thinking...")

    try:
        resp = requests.post(
            f"{API_BASE}/query",
            json={"telegram_id": telegram_id, "text": query},
            timeout=120,
        )

        if resp.status_code == 200:
            data = resp.json()
            reply = data["response"]
            remaining = data.get("queries_remaining", "?")
            footer = f"\n\n─── _{remaining} queries remaining today_ ───"
            reply += footer
        elif resp.status_code == 429:
            reply = f"⏳ {resp.json().get('detail', 'Rate limit reached. Try again tomorrow.')}"
        elif resp.status_code == 401:
            reply = "🔐 Session expired. Send /start to reconnect."
        else:
            reply = "⚠️ Service temporarily unavailable."

    except requests.Timeout:
        reply = "⏰ Request timed out. Try a shorter question."
    except requests.ConnectionError:
        reply = "⚠️ Backend is offline."
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        reply = "⚠️ Something went wrong."

    # Telegram 4096-char limit — split long messages
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i : i + 4000])


# ── Main ──────────────────────────────────────────────────────────────


def main():
    """Start the Telegram bot."""
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 LoopedAI Bot starting (backend: %s)", API_BASE)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
