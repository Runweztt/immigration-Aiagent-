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
pytest tests/unit/ -v
pytest tests/ --cov=src
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
