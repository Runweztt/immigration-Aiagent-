# 🔒 LoopedAI Immigration Backend

Secure FastAPI backend + Telegram bot for the UK Immigration AI Agent. Powers the CrewAI 6-agent pipeline with authentication, rate limiting, and query logging.

## Overview

This backend serves as the **secure orchestration layer** between Telegram users and the CrewAI agent system:

- **Zero-Key Bot**: Telegram bot holds no API keys — delegates everything to the FastAPI backend
- **Authentication**: Users verify with a LoopedAI ID (`LAI-XXXXXXXX`) before accessing the system
- **Rate Limiting**: 20 queries per user per day (configurable)
- **Agent Pipeline**: Routes queries through 6 CrewAI agents (intake → research → guide → compliance → solicitor)
- **Audit Logging**: Every query logged with token usage and cost
- **Dual Database**: SQLite for development, Supabase for production (same interface)

### Important Note

This backend connects to the [Immigration AI Agent](https://github.com/Runweztt/immigration-Aiagent-) system in `src/`. It requires the full agent codebase to be deployed alongside.

## Architecture

```
Telegram User → bot.py (zero keys) → api_server.py → CrewAI (6 agents) → Claude API
                                           ↓
                                    SQLite / Supabase
```

### Core Components
- **api_server.py**: FastAPI with auth, rate limiting, and query endpoints
- **bot.py**: Telegram bot that delegates to the backend via localhost HTTP
- **llm_client.py**: Bridge to CrewAI `process_immigration_query()` pipeline
- **db.py**: Abstract DB interface (SQLite + Supabase implementations)
- **rate_limiter.py**: Stateless daily query limiter
- **config.py**: Frozen settings singleton, loads from `.env`
- **admin_cli.py**: CLI for user registration and management

## Quick Start

```bash
git clone https://github.com/Runweztt/backend_loopedAi_agent.git
cd backend_loopedAi_agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your API keys
```

## User Management

```bash
# Register a new user
python3 -m backend.admin_cli register "John Doe"

# List all users
python3 -m backend.admin_cli list

# Deactivate a user
python3 -m backend.admin_cli deactivate LAI-XXXXXXXX
```

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/auth/verify` | POST | Check if Telegram user is linked |
| `/auth/link` | POST | Link LoopedAI ID to Telegram |
| `/query` | POST | Run query through 6-agent pipeline |

## Development

### Prerequisites
- Python 3.11 or higher
- Anthropic API key (Claude)
- Telegram Bot Token

### Running Locally
```bash
export PYTHONPATH=$(pwd)/..
python3 -m uvicorn backend.api_server:app --host 127.0.0.1 --port 8000 &
python3 -m backend.bot
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
