# Immigration AI Agent

An AI-powered multi-agent system that assists immigrants with visa information, application guidance, and lawyer recommendations. Built with CrewAI and Python.

## Overview

This system uses a **multi-agent architecture** powered by **CrewAI** to help users navigate the immigration process:

- **Understand Your Situation**: Extracts your nationality, visa status, and goals from natural language
- **Plain Language Explanations**: Rewrites complex legal jargon into simple terms anyone can understand
- **Up-to-Date Research**: Finds the latest immigration rules, processing times, and policy changes
- **Step-by-Step Guidance**: Generates personalized checklists with forms, documents, and deadlines
- **Compliance Verification**: Cross-checks all advice against official government sources
- **Lawyer Recommendations**: Matches you with immigration attorneys by speciality and location

### Important Note

This is a proof-of-concept system using mocked tool data. For production use, real API integrations (USCIS, lawyer directories) would be required.

## Quick Start

```bash
git clone https://github.com/Runweztt/immigration-ai-agent-.git
cd immigration-ai-agent-
uv venv && source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync --dev
cp .env.example .env  # Edit with your API keys
python src/main.py
```

## Architecture

The system processes each query through 6 specialized agents in sequence:

```
User Query → Intake → Plain Language → Research → Application Guide → Compliance → Lawyer Match → Results
```

### Core Components
- **6 AI Agents** (`src/agents/`): Each with a specific role in the immigration assistance pipeline
- **6 Tasks** (`src/tasks/`): Define what each agent should accomplish
- **3 Domain Tools** (`src/tools/`): Immigration lookup, lawyer directory, and form guide
- **LLM Layer** (`src/llm/`): Factory pattern supporting OpenAI and Ollama with automatic fallback
- **API Server** (`src/api/`): FastAPI endpoint at `POST /immigration-advice/`

## Development

### Prerequisites
- Python 3.11 or higher
- UV package manager (recommended) or pip
- OpenAI API key (optional) or Ollama installation

### Testing
```bash
pytest tests/unit/ -v
pytest tests/ --cov=src
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
