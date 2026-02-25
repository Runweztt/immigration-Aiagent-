"""LoopedAI Telegram Bot.

Simplified Telegram bot that gates access behind LoopedAI IDs.
Users enter their ID once, then all messages go straight to the
Immigration AI Agent — no unnecessary questions.
"""

import os
import logging

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

from loopedai_auth import (
    init_db,
    is_telegram_linked,
    link_telegram,
    log_query,
    validate_id,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IMMIGRATION_API = os.getenv(
    "IMMIGRATION_API_URL", "http://localhost:8000/immigration-advice/"
)


# ── Handlers ──────────────────────────────────────────────────────────


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start — check if user is already linked."""
    telegram_id = str(update.effective_user.id)
    existing = is_telegram_linked(telegram_id)

    if existing:
        await update.message.reply_text(
            f"✅ Welcome back! (ID: {existing})\n\n"
            "Send your immigration question and I'll help you right away."
        )
    else:
        await update.message.reply_text(
            "🌍 *Welcome to LoopedAI Immigration Assistant*\n\n"
            "Enter your *LoopedAI ID* to get started.\n"
            "Format: `LAI-XXXXXXXX`\n\n"
            "_Don't have one? Contact support to register._",
            parse_mode="Markdown",
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages — authenticate or process query."""
    telegram_id = str(update.effective_user.id)
    text = update.message.text.strip()

    # ── Already authenticated ──
    existing = is_telegram_linked(telegram_id)
    if existing:
        await _process_query(update, existing, text)
        return

    # ── Trying to authenticate with LoopedAI ID ──
    if text.upper().startswith("LAI-"):
        looped_id = text.upper()
        if validate_id(looped_id):
            link_telegram(looped_id, telegram_id)
            await update.message.reply_text(
                "✅ *Access Granted!*\n\n"
                "You're connected. Just type your immigration question.\n\n"
                "_Example: I'm on an F-1 visa and want to apply for OPT_",
                parse_mode="Markdown",
            )
        else:
            await update.message.reply_text(
                "❌ Invalid LoopedAI ID. Please check and try again.\n"
                "Contact support if you need a new ID."
            )
        return

    # ── Not authenticated, not an ID ──
    await update.message.reply_text(
        "🔐 Please enter your LoopedAI ID first.\n"
        "Format: `LAI-XXXXXXXX`",
        parse_mode="Markdown",
    )


async def _process_query(update: Update, looped_id: str, query: str):
    """Send user's immigration query to the API and return the response."""
    await update.message.reply_text("⏳ Processing your query...")
    log_query(looped_id, query)

    try:
        resp = requests.post(
            IMMIGRATION_API,
            json={"text": query},
            timeout=120,
        )
        if resp.status_code == 200:
            result = resp.json()
            reply = _format_response(result)
        else:
            logger.error(f"API returned {resp.status_code}: {resp.text[:200]}")
            reply = "⚠️ Service temporarily unavailable. Please try again shortly."
    except requests.Timeout:
        reply = "⏰ The request timed out. Please try a shorter question."
    except requests.ConnectionError:
        reply = "⚠️ Could not reach the immigration service. It may be starting up."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        reply = "⚠️ Something went wrong. Please try again."

    # Telegram has a 4096-char message limit — split if needed
    for i in range(0, len(reply), 4000):
        await update.message.reply_text(reply[i : i + 4000], parse_mode="Markdown")


def _format_response(result: dict) -> str:
    """Format the multi-agent response for Telegram."""
    sections = [
        ("📋 *Intake Summary*", "intake_summary"),
        ("📖 *Plain Language*", "plain_language"),
        ("🔍 *Research Findings*", "research_findings"),
        ("📝 *Application Guide*", "application_guide"),
        ("✅ *Compliance Check*", "compliance_check"),
        ("⚖️ *Lawyer Recommendations*", "lawyer_recommendations"),
    ]
    parts = []
    for title, key in sections:
        content = result.get(key)
        if content and str(content).strip():
            parts.append(f"{title}\n{content}")

    return "\n\n───\n\n".join(parts) if parts else "No results found for your query."


# ── Main ──────────────────────────────────────────────────────────────


def main():
    """Start the Telegram bot."""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN not set in .env")
        return

    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 LoopedAI Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
