"""Utility functions for the immigration AI multi-agent system."""

import logging
import os
import sys
from typing import Any

from dotenv import load_dotenv


def setup_project_paths() -> None:
    """Set up project paths in the system path.

    This function adds the project root and src directory to the system path,
    allowing imports to be made relative to the project root.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        logging.debug(f"Added project root to system path: {project_root}")

    src_dir = os.path.join(project_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        logging.debug(f"Added src directory to system path: {src_dir}")


def configure_logging(
    level: int = logging.INFO,
    log_file: str | None = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
) -> None:
    """Configure logging for the application.

    Args:
        level: The logging level to use
        log_file: Optional path to a log file
        log_format: The format string for log messages
    """
    handlers = [logging.StreamHandler()]

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(level=level, format=log_format, handlers=handlers)

    logging.info(f"Logging configured with level: {logging.getLevelName(level)}")
    if log_file:
        logging.info(f"Log file: {log_file}")


def load_config() -> dict[str, Any]:
    """Load configuration variables from .env file.

    Returns:
        Dictionary containing configuration variables
    """
    load_dotenv()

    config = {
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "anthropic_model_name": os.getenv("ANTHROPIC_MODEL_NAME", "claude-sonnet-4-20250514"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_model_name": os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
        "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "ollama_model_name": os.getenv("OLLAMA_MODEL_NAME", "llama3"),
        "llm_provider": os.getenv("LLM_PROVIDER", "ANTHROPIC"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_file": os.getenv("LOG_FILE", None),
    }

    return config
