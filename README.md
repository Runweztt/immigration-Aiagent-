# 🌍 Immigration AI Agent

An intelligent multi-agent immigration assistant powered by **CrewAI**, **Supabase**, and **FastAPI** — accessible via a premium **React web interface** and **Telegram**.

## Architecture

```
immigration-aigent/
├── backend/              # FastAPI server, CrewAI agents, Supabase DB, Telegram bot
│   ├── src/              # Core CrewAI system (agents, tasks, tools, LLM)
│   ├── db/               # Supabase database client
│   ├── bot/              # Telegram bot
│   ├── server.py         # FastAPI entry point
│   └── config.py         # Centralized settings
├── frontend/             # React + Vite web interface
│   ├── src/              # React components
│   └── package.json
├── docs/                 # Project documentation
├── .env                  # Environment variables (not committed)
└── pyproject.toml        # Python dependencies
```

## Quick Start

### 1. Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
ANTHROPIC_API_KEY=your-key
TELEGRAM_BOT_TOKEN=your-token
INTERNAL_API_KEY=your-secret-key
```

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn backend.server:app --port 8000 --reload
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Telegram Bot

```bash
python -m backend.bot.telegram_bot
```

## How It Works

1. **Register** on the web app (name, email, country)
2. **Get a link code** to optionally connect Telegram
3. **Ask immigration questions** via web chat or Telegram
4. The **CrewAI engine** runs 3 agents in sequence:
   - 🔍 **Intake Agent** — extracts your situation details
   - 📚 **Research Agent** — finds requirements, forms, fees
   - ✍️ **Response Agent** — delivers a clear, actionable answer

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, Python 3.12+ |
| AI Engine | CrewAI, LangChain |
| Auth & Database | Supabase |
| LLM Providers | Claude (Anthropic), OpenAI, Ollama |
| Telegram | python-telegram-bot |


