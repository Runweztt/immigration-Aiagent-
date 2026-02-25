# 🌍 Immigration AI Agent

A multi-agent AI system built with **CrewAI** and **Anthropic Claude** that provides comprehensive immigration guidance — from intake analysis to lawyer matching.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-blueviolet)
![Anthropic](https://img.shields.io/badge/LLM-Claude%20Sonnet%204-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Overview

Immigration AI Agent is an intelligent, multi-agent system that breaks down complex immigration queries into specialized tasks. Each agent focuses on a specific domain — intake extraction, legal research, plain-language translation, application guidance, compliance verification, and lawyer matching — delivering structured, actionable immigration advice.

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────────┐
│               CrewAI Orchestrator               │
│            (Sequential Processing)              │
└─────────────────────────────────────────────────┘
    │
    ├── 1.  Intake Specialist
    │       Extracts nationality, visa type, status, desired outcome
    │
    ├── 2.  Plain Language Advisor
    │       Simplifies legal jargon into everyday language
    │
    ├── 3.  Research Analyst
    │       Researches eligibility, processing times, policy changes
    │
    ├── 4.  Application Guide
    │       Creates step-by-step filing instructions
    │
    ├── 5.  Compliance Verifier
    │       Validates accuracy against official sources
    │
    └── 6.  Lawyer Matchmaker
            Recommends attorneys by specialty, location & language
```

---

##  Project Structure

```
immigration-ai-agent/
├── src/
│   ├── main.py                 # Entry point & crew orchestration
│   ├── utils.py                # Configuration & logging utilities
│   ├── agents/
│   │   ├── intake_agent.py             # Extracts user context
│   │   ├── plain_language_agent.py     # Simplifies terminology
│   │   ├── immigration_research_agent.py  # Policy & eligibility research
│   │   ├── application_guide_agent.py  # Step-by-step guidance
│   │   ├── compliance_agent.py         # Accuracy verification
│   │   └── lawyer_match_agent.py       # Attorney recommendations
│   ├── tasks/
│   │   ├── intake_task.py
│   │   ├── simplify_language_task.py
│   │   ├── research_immigration_task.py
│   │   ├── guide_application_task.py
│   │   ├── compliance_check_task.py
│   │   └── lawyer_match_task.py
│   ├── tools/
│   │   ├── immigration_tools.py   # Immigration lookup tool
│   │   ├── web_tools.py           # Web search tool
│   │   ├── database_interface.py  # Abstract DB interface
│   │   ├── database_tools.py      # Case data operations
│   │   ├── mock_database.py       # In-memory mock database
│   │   └── logging_tools.py       # Audit logging
│   └── llm/
│       ├── llm_factory.py     # LLM provider factory
│       ├── claude_llm.py      # Anthropic adapter
│       ├── openai_llm.py      # OpenAI adapter
│       ├── ollama_llm.py      # Ollama adapter
│       ├── config.py          # LLM configuration
│       └── circuit_breaker.py # Provider availability checks
├── tests/
│   ├── conftest.py
│   ├── integration/
│   │   ├── test_api.py
│   │   └── test_agent_system.py
│   └── test_matrix.py
├── .env                       # API keys & config (not committed)
├── pyproject.toml
└── README.md
```

---

##  Quick Start

### Prerequisites

- **Python 3.11+**
- **[uv](https://docs.astral.sh/uv/)** (recommended) or pip
- **Anthropic API Key** ([get one here](https://console.anthropic.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/healthcare-aigent.git
cd Immigration-aigent
```

### 2. Set Up the Environment

```bash
uv venv
uv pip install -e .[dev]
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# LLM Provider
LLM_PROVIDER=ANTHROPIC
ANTHROPIC_API_KEY=your-api-key-here
ANTHROPIC_MODEL_NAME=claude-sonnet-4-20250514

# Optional: Fallback providers
OPENAI_API_KEY=your-openai-key
OLLAMA_MODEL_NAME=llama3
```

### 4. Run the Agent

```bash
uv run python -m src.main
```

---

##  Example Query

The default demo query in `main.py`:

```
I am a Nigerian citizen currently in the United States on an F-1 student visa.
My visa expires in 3 months and I just graduated with a Master's degree in
Computer Science. I want to stay and work in the US. What are my options?
I might need a lawyer in New York who speaks Yoruba.
```

### Sample Output Sections

| Section | Description |
|---------|-------------|
| **Intake Summary** | Extracted nationality, visa type, status, and goals |
| **Plain Language** | Legal terms translated to simple English |
| **Research Findings** | Eligibility, processing times, policy updates |
| **Application Guide** | Forms, documents, fees, and filing steps |
| **Compliance Check** | Verification with confidence scores |
| **Lawyer Recommendations** | Matched attorneys with specialties and ratings |

---

##  Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run integration tests only
uv run pytest tests/integration/
```

---

##  LLM Provider Support

| Provider | Status | Use Case |
|----------|--------|----------|
| **Anthropic (Claude)** |  Primary | Cloud-based, high accuracy |
| **OpenAI (GPT)** |  Supported | Alternative cloud provider |
| **Ollama (Llama)** |  Supported | Local/private deployment |

The system includes automatic fallback — if the primary provider is unavailable, it will try alternatives.

---

##  Disclaimer

> ** Important:** This tool provides general immigration guidance only and does **not** constitute legal advice. Immigration laws change frequently. Always consult a qualified immigration attorney and verify information on official government websites ([USCIS.gov](https://www.uscis.gov), [State.gov](https://www.state.gov)) before taking any action.

---

##  License

This project is licensed under the MIT License.

---

##  Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
