"""Main module for the Immigration AI Agent system.

This module serves as the primary entry point for running the immigration AI agent crew.
It defines the main workflow for processing an immigration query using 3 consolidated
agents: Intake, Research, and Response.
"""

import os

from crewai import Crew, LLM, Process
from dotenv import load_dotenv

from src.agents import create_immigration_crew
from src.tasks import (
    IntakeTask,
    ResearchImmigrationTask,
    ResponseTask,
)


from src.llm.llm_factory import get_llm


def process_immigration_query(query: str, user_context: dict | None = None) -> str:
    """Processes an immigration query using the immigration agent crew.

    This function orchestrates the entire workflow. It initializes the language model,
    creates the 3 specialized agents, defines the sequence of tasks, and runs the
    crew to produce a single concise response.

    Args:
        query: A string containing the user's immigration question or scenario.
        user_context: Optional dict with user details (name, country, location).

    Returns:
        A string containing the final immigration response for the user.
    """
    load_dotenv()

    # Use the centralized LLM factory
    llm = get_llm(temperature=0.3)

    # Create 3 consolidated agents
    agents_list = create_immigration_crew(llm)
    intake_agent, research_agent, response_agent = agents_list

    # Create tasks
    tasks = [
        IntakeTask(intake_agent),
        ResearchImmigrationTask(research_agent),
        ResponseTask(response_agent),
    ]

    # Build inputs with user context
    ctx = user_context or {}
    inputs = {
        "query": query,
        "user_name": ctx.get("name", "Not provided"),
        "user_country": ctx.get("country", "Not provided"),
        "user_location": ctx.get("location", "Not provided"),
    }

    # Create and run the crew
    crew = Crew(agents=agents_list, tasks=tasks, process=Process.sequential, verbose=True)
    result = crew.kickoff(inputs=inputs)

    # Return the final response (last task's output)
    return result.raw


def main():
    """Entry point for testing the system directly."""
    query = (
        "Hi my name is Emmanuel Amarikwa from Nigeria living in Rwanda. "
        "I want to transfer my study from African Leadership University to "
        "Trent University Canada. What is the requirement?"
    )

    user_context = {
        "name": "Emmanuel Amarikwa",
        "country": "Nigeria",
        "location": "Kigali, Rwanda",
    }

    result = process_immigration_query(query, user_context)

    print("\n" + "=" * 60)
    print("IMMIGRATION AI AGENT — RESPONSE")
    print("=" * 60)
    print(result)
    print("=" * 60)


if __name__ == "__main__":
    main()
