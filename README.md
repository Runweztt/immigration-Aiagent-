#  Immigration AI Agent

An intelligent **multi-agent immigration assistant** powered by [CrewAI](https://www.crewai.com/), with a premium **React** web interface. Three specialised AI agents collaborate in sequence — **Intake → Research → Response** — to deliver personalised immigration guidance in plain language.

> **Note:** The production backend (FastAPI server, Supabase DB, Telegram bot) lives in its own **separate repository** and is **not covered here**. Everything documented below is the core AI agent system and the frontend — fully clonable and buildable on its own.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Frontend — React Web Interface](#frontend--react-web-interface)
- [Core AI System — `src/`](#core-ai-system--src)
  - [Agents](#agents--srcagents)
  - [Tasks](#tasks--srctasks)
  - [Tools](#tools--srctools)
  - [LLM Layer](#llm-layer--srcllm)
  - [API Server](#api-server--srcapi)
  - [Utilities](#utilities--srcutilspy)
  - [Entry Point](#entry-point--srcmainpy)
- [Scripts](#scripts--scripts)
- [Tests](#tests--tests)
- [Documentation](#documentation--frontenddocs)
- [Configuration Files](#configuration-files)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [License](#license)

---

## Architecture Overview

```
User ──▶ React Frontend ──▶ API Server ──▶ CrewAI Crew
                                              │
                              ┌────────────────┼────────────────┐
                              ▼                ▼                ▼
                        Intake Agent    Research Agent    Response Agent
                              │                │                │
                         Intake Task    Research Task     Response Task
                              │                │                │
                              └───── LLM Layer (Claude / OpenAI / Ollama) ─────┘
```

The system follows a **sequential pipeline**: each agent handles one phase and passes its output to the next.

---

## Project Structure

```
immigration-aigent/
│
├── frontend/                  # React + Vite web interface
│   ├── index.html             # HTML entry point (Tailwind config, premium theme)
│   ├── init.js                # Initialisation script
│   ├── package.json           # NPM dependencies & scripts
│   ├── vite.config.js         # Vite dev-server & API proxy config
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── postcss.config.js      # PostCSS plugins
│   ├── docs/                  # Project documentation (17 guides)
│   └── src/
│       ├── main.jsx           # React DOM bootstrap
│       ├── App.jsx            # Root component — step-based routing
│       ├── index.css          # Global styles
│       └── components/
│           ├── RegistrationForm.jsx  # User registration form
│           ├── SuccessPage.jsx       # Post-registration success view
│           ├── Dashboard.jsx         # Main dashboard UI
│           └── Layout.jsx            # Shared page layout wrapper
│
├── src/                       # Core CrewAI multi-agent system
│   ├── __init__.py
│   ├── main.py                # Entry point — orchestrates the crew
│   ├── utils.py               # Logging, config, path helpers
│   ├── agents/                # Specialised CrewAI agents (7 files)
│   ├── tasks/                 # Task definitions for each agent (7 files)
│   ├── tools/                 # Custom tools for agents (6 files)
│   ├── llm/                   # LLM abstraction layer (8 files)
│   └── api/                   # Lightweight FastAPI server
│
├── scripts/                   # Developer scripts
│   ├── __init__.py
│   └── lint.py                # Automated linting with Ruff
│
├── tests/                     # Pytest test suite
│   ├── conftest.py            # Shared fixtures & markers
│   ├── pytest.ini             # Pytest configuration
│   ├── test_environment.py    # Environment validation tests
│   ├── test_matrix.py         # Cross-provider test matrix
│   ├── unit/                  # Unit tests (6 files)
│   ├── integration/           # Integration tests (4 files)
│   └── performance/           # Performance benchmarks
│
├── .env.example               # Template for environment variables
├── pyproject.toml             # Python project config & dependencies
├── CLAUDE.md                  # AI assistant coding conventions
├── .pre-commit-config.yaml    # Pre-commit hook config
├── .gitignore                 # Git ignore rules
└── .gitattributes             # Git attributes
```

---

## Frontend — React Web Interface

**Tech stack:** React 18 · Vite 5 · Tailwind CSS 3 · Framer Motion · Lucide Icons · Axios

The frontend is a **premium, dark-themed** single-page application with glassmorphism effects, smooth animations, and a custom `Outfit` font.

### Files & What They Do

| File | Purpose |
|------|---------|
| `index.html` | HTML shell — loads Tailwind via CDN, defines the custom premium colour palette (`dark`, `gold`, `blue`, `light`), and sets up glassmorphism CSS classes. |
| `vite.config.js` | Configures Vite to run on **port 3000** and proxy all `/api` requests to the backend at `http://localhost:8000`. |
| `package.json` | Declares dependencies: `react`, `react-dom`, `lucide-react` (icons), `framer-motion` (animations), `axios` (HTTP client). Dev deps include Vite, Tailwind, PostCSS, and Autoprefixer. |
| `tailwind.config.js` | Extends Tailwind with the premium colour palette and Outfit font family. |
| `postcss.config.js` | Registers `tailwindcss` and `autoprefixer` as PostCSS plugins. |
| `src/main.jsx` | Bootstraps the React app into the `#root` div with `StrictMode`. |
| `src/App.jsx` | **Root component** — manages a 3-step flow using local state: `register` → `success` → `dashboard`. Renders the appropriate component based on the current step, all wrapped in a shared `Layout`. |
| `src/index.css` | Global CSS — imported by `main.jsx`. |
| `src/components/Layout.jsx` | Shared page layout wrapper — provides consistent structure around every view. Accepts an `isFullWidth` prop for the dashboard. |
| `src/components/RegistrationForm.jsx` | Multi-field registration form — collects user information and submits it. Calls `onSafeSuccess` on successful submission. |
| `src/components/SuccessPage.jsx` | Animated success screen shown after registration — displays user data and a button to proceed to the dashboard. |
| `src/components/Dashboard.jsx` | Main dashboard view — the primary interface users interact with after registering. |

### How the Frontend Flow Works

```
1. User lands on RegistrationForm
2. Fills out details → submits → onSafeSuccess fires
3. App navigates to SuccessPage (shows confirmation)
4. User clicks "Proceed" → App navigates to Dashboard
5. Dashboard communicates with backend API via /api proxy
```

---

## Core AI System — `src/`

The `src/` directory contains the **CrewAI multi-agent system** — the intelligence behind the assistant. It is fully self-contained and can be run independently of the backend.

### Entry Point — `src/main.py`

The orchestrator. It:

1. Loads environment config via `dotenv`.
2. Initialises the LLM using the factory (`get_llm`).
3. Creates the 3 core agents via `create_immigration_crew(llm)`.
4. Defines the task sequence: **Intake → Research → Response**.
5. Builds a `Crew` and runs it sequentially via `crew.kickoff()`.
6. Returns the final response string.

Can be run directly: `python -m src.main` for a built-in test query.

---

### Agents — `src/agents/`

Each agent is a specialised CrewAI `Agent` with a defined role, goal, and backstory.

| File | Agent | Role |
|------|-------|------|
| `intake_agent.py` | **IntakeAgent** | Extracts user context (name, nationality, visa type, desired outcome) from the raw query. |
| `immigration_research_agent.py` | **ImmigrationResearchAgent** | Researches immigration requirements, eligibility, processing times, and application steps. |
| `response_agent.py` | **ResponseAgent** | Synthesises all prior agent outputs into a single, concise, user-friendly response. |
| `compliance_agent.py` | **ComplianceAgent** | Verifies accuracy of information and flags potential issues. |
| `application_guide_agent.py` | **ApplicationGuideAgent** | Generates step-by-step application instructions. |
| `lawyer_match_agent.py` | **LawyerMatchAgent** | Recommends immigration lawyers based on the user's case type. |
| `plain_language_agent.py` | **PlainLanguageAgent** | Translates legal jargon into accessible, everyday language. |
| `__init__.py` | `create_immigration_crew()` | Factory function — assembles the 3 core agents (Intake, Research, Response) into a list. |

> The 3-agent pipeline (Intake → Research → Response) is the **optimised default**. The remaining agents are available for extended workflows.

---

### Tasks — `src/tasks/`

Tasks define what each agent should accomplish. Each task class wraps a CrewAI `Task` with a specific description, expected output, and assigned agent.

| File | Task | Description |
|------|------|-------------|
| `intake_task.py` | **IntakeTask** | Extracts structured user profile data from the raw immigration query. |
| `research_immigration_task.py` | **ResearchImmigrationTask** | Researches visa requirements, eligibility criteria, and timelines. |
| `response_task.py` | **ResponseTask** | Produces the final user-facing answer. |
| `compliance_check_task.py` | **ComplianceCheckTask** | Cross-checks research output for accuracy and compliance. |
| `guide_application_task.py` | **GuideApplicationTask** | Generates detailed application step-by-step guides. |
| `lawyer_match_task.py` | **LawyerMatchTask** | Matches the case to relevant immigration attorneys. |
| `simplify_language_task.py` | **SimplifyLanguageTask** | Rewrites legal language into plain English. |
| `__init__.py` | Exports | Re-exports all task classes for easy importing. |

---

### Tools — `src/tools/`

Custom CrewAI tools that agents can invoke during task execution.

| File | Purpose |
|------|---------|
| `immigration_tools.py` | Core immigration-specific tools — visa lookup tables, eligibility checks, document requirement generators. The main toolset used by agents during research. |
| `database_tools.py` | Tools for querying and storing immigration case data in a database. |
| `database_interface.py` | Abstract database interface — defines the contract for data access operations. |
| `mock_database.py` | In-memory mock database for testing and development — no external DB required. |
| `web_tools.py` | Tools for fetching live immigration data from external web sources. |
| `logging_tools.py` | Logging utilities for agent activity tracking. |
| `__init__.py` | Package init. |

---

### LLM Layer — `src/llm/`

A robust, provider-agnostic LLM abstraction with **automatic fallback** and **circuit-breaker** resilience.

| File | Purpose |
|------|---------|
| `config.py` | Centralised LLM configuration — reads provider settings from environment variables, defines model defaults, timeouts, and retry policies. |
| `base.py` | Abstract base class for all LLM adapters — defines the common interface (`generate`, `get_crewai_llm`). |
| `claude_llm.py` | **Anthropic Claude adapter** — wraps the `anthropic` SDK for Claude models. Default provider. |
| `openai_llm.py` | **OpenAI adapter** — wraps the `openai` SDK for GPT models. Available as primary or fallback. |
| `ollama_llm.py` | **Ollama adapter** — connects to a locally running Ollama instance for fully offline usage. |
| `llm_factory.py` | **Factory** — selects and instantiates the correct LLM adapter based on the `LLM_PROVIDER` env var. Entry point: `get_llm()`. |
| `fallback.py` | **Fallback chain** — if the primary provider fails, automatically tries the next provider in the chain (Claude → OpenAI → Ollama). |
| `circuit_breaker.py` | **Circuit breaker pattern** — tracks failures per provider and temporarily disables unhealthy providers to avoid cascading timeouts. Includes `is_ollama_available()` and `is_openai_available()` health checks. |
| `__init__.py` | Exports key classes and functions. |

**Provider priority:** Claude (cloud) → OpenAI (cloud) → Ollama (local)

---

### API Server — `src/api/`

A lightweight **FastAPI** server that exposes the agent system as an HTTP endpoint.

| File | Purpose |
|------|---------|
| `api_server.py` | Defines the FastAPI app with a single `POST /immigration-advice/` endpoint. Accepts a JSON body `{ "text": "..." }`, passes it to `process_immigration_query()`, and returns structured guidance (intake summary, research findings, application guide, compliance check, lawyer recommendations). |
| `__init__.py` | Package init. |

Run with: `uvicorn src.api.api_server:app --port 8000 --reload`

---

### Utilities — `src/utils.py`

Shared helper functions used across the system:

- **`setup_project_paths()`** — Adds project root and `src/` to `sys.path` for clean imports.
- **`configure_logging()`** — Sets up logging with configurable level, format, and optional file output.
- **`load_config()`** — Loads all configuration from `.env` into a typed dictionary.

---

## Scripts — `scripts/`

| File | Purpose |
|------|---------|
| `lint.py` | Automated linting pipeline — runs `ruff check --fix` → `ruff format` → `ruff check` (final validation). Uses `uv run` to execute within the project's virtual environment. Run via `uv run lint` or `python scripts/lint.py`. |
| `__init__.py` | Package init. |

---

## Tests — `tests/`

A comprehensive **Pytest** test suite with unit, integration, and performance test categories.

### Configuration

| File | Purpose |
|------|---------|
| `conftest.py` | Shared fixtures — provides `mock_env_vars`, `mock_immigration_query`, `mock_case_data`, and service-availability checks (`ollama_available`, `openai_available`). Registers custom markers: `integration`, `llm`, `slow`. Automatically skips integration tests when no LLM service is available. |
| `pytest.ini` | Pytest settings — configures test paths, verbose output, short tracebacks, and async mode. |
| `test_environment.py` | Validates that the development environment is correctly configured. |
| `test_matrix.py` | Cross-provider test matrix — tests the system across all supported LLM providers. |

### Unit Tests — `tests/unit/`

| File | What It Tests |
|------|---------------|
| `test_agents.py` | Verifies agent creation, configuration, roles, and tool assignment. |
| `test_tasks.py` | Tests task definitions, descriptions, expected outputs, and agent bindings. |
| `test_tools.py` | Validates tool functionality — immigration lookups, database operations. |
| `test_llm_adapters.py` | Tests each LLM adapter (Claude, OpenAI, Ollama) in isolation with mocked APIs. |
| `test_llm_factory.py` | Tests the LLM factory — correct provider selection, environment variable handling, error cases. |
| `test_llm_fallback.py` | Tests the fallback chain — verifies automatic provider switching on failure. |

### Integration Tests — `tests/integration/`

| File | What It Tests |
|------|---------------|
| `test_agent_system.py` | End-to-end test — runs the full agent crew against a real query. |
| `test_api.py` | Tests the FastAPI endpoint with real HTTP requests. |
| `test_llm_connectivity.py` | Validates connectivity to each configured LLM provider. |
| `test_llm_factory_integration.py` | Full integration test of the LLM factory with real providers. |

### Running Tests

```bash
# Unit tests only
pytest tests/unit/ -v

# All tests with coverage
pytest tests/ --cov=src

# Skip integration tests (no API keys needed)
pytest tests/unit/ -v -m "not integration"
```

---

## Documentation — `frontend/docs/`

The `docs/` directory contains 17 comprehensive guides covering every aspect of the project:

| Document | Topic |
|----------|-------|
| `architecture.md` | System architecture and component design |
| `installation.md` | Full installation guide |
| `setup.md` | Environment setup and configuration |
| `development.md` | Development workflow and practices |
| `development_environment.md` | IDE setup, tooling, and environment details |
| `crewai.md` | CrewAI framework integration guide |
| `technical_implementation.md` | Detailed technical implementation notes |
| `testing.md` | Testing strategy, conventions, and commands |
| `linting.md` | Linting setup and Ruff configuration |
| `language.md` | LLM language and prompt engineering notes |
| `ollama.md` | Ollama local LLM setup and usage |
| `uv_migration.md` | Migration guide to the `uv` package manager |
| `ci_cd.md` | CI/CD pipeline documentation |
| `Ansible.md` | Ansible deployment automation |
| `tdd_vibe_coding.md` | TDD methodology and development philosophy |
| `progress.md` | Project progress log and milestones |
| `CLAUDE.md` | AI assistant interaction guidelines |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python project metadata, dependencies (CrewAI, LangChain, FastAPI, Anthropic, OpenAI, Ollama, etc.), Ruff linter/formatter settings, UV config, and pytest options. Requires **Python ≥ 3.11, < 3.13**. |
| `.env.example` | Template for required environment variables — copy to `.env` and fill in your API keys. |
| `.pre-commit-config.yaml` | Pre-commit hooks configuration for automated code quality checks. |
| `.gitignore` | Ignores virtual environments, caches, `.env`, IDE files, and the `backend/` directory (separate repo). |
| `.gitattributes` | Git line-ending and binary file handling rules. |
| `CLAUDE.md` | Coding conventions and operational directives for AI-assisted development — documents docstring style, commit strategy, linting, and safety rules. |

---

## Getting Started

### Prerequisites

- **Python 3.11+** (< 3.13)
- **Node.js 18+** and **npm**
- **uv** (recommended) or **pip** for Python dependency management
- At least one LLM provider API key (Anthropic recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Runweztt/immigration-Aiagent-.git
cd immigration-aigent
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Install Python Dependencies

```bash
# With uv (recommended)
uv sync

# Or with pip
pip install -e ".[dev]"
```

### 4. Run the AI Agent (CLI)

```bash
# Direct execution
python -m src.main

# Or via the installed script
immigration-ai-agent
```

### 5. Run the API Server

```bash
uvicorn src.api.api_server:app --port 8000 --reload
```

### 6. Start the Frontend

```bash
cd frontend
npm install
npm run dev
# Opens at http://localhost:3000
```

### 7. Run Tests

```bash
# Unit tests
pytest tests/unit/ -v

# Full suite with coverage
pytest tests/ --cov=src
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | Your Anthropic API key for Claude |
| `ANTHROPIC_MODEL_NAME` | ❌ | Claude model (default: `claude-sonnet-4-20250514`) |
| `LLM_PROVIDER` | ❌ | Provider: `ANTHROPIC`, `OPENAI`, or `OLLAMA` (default: `ANTHROPIC`) |
| `OPENAI_API_KEY` | ❌ | OpenAI API key (optional fallback) |
| `OPENAI_MODEL_NAME` | ❌ | OpenAI model (default: `gpt-3.5-turbo`) |
| `OLLAMA_BASE_URL` | ❌ | Ollama server URL (default: `http://localhost:11434`) |
| `OLLAMA_MODEL_NAME` | ❌ | Ollama model (default: `llama3`) |
| `LOG_LEVEL` | ❌ | Logging level (default: `INFO`) |
| `LOG_FILE` | ❌ | Path to log file (default: console only) |

---

## License

This project is maintained by **Runweztt** (amarikwat@gmail.com).
