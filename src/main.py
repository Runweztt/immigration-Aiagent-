"""Main module for the Immigration AI Agent system.

This module serves as the primary entry point for running the immigration AI agent crew.
It defines the main workflow for processing an immigration query, from initializing
the language model and agents to executing the tasks and returning the final results.
"""

import os

from crewai import Crew, LLM, Process
from dotenv import load_dotenv

from src.agents import create_immigration_crew
from src.tasks import (
    ComplianceCheckTask,
    GuideApplicationTask,
    IntakeTask,
    LawyerMatchTask,
    ResearchImmigrationTask,
    SimplifyLanguageTask,
)


def process_immigration_query(query: str, user_context: dict | None = None) -> dict:
    """Processes an immigration query using the immigration agent crew.

    This function orchestrates the entire workflow. It initializes the language model
    using CrewAI's native LLM format, creates the specialized agents, defines the
    sequence of tasks, and runs the crew to get the processed results.

    Args:
        query: A string containing the user's immigration question or scenario.
        user_context: Optional dict with user details (name, country, location).

    Returns:
        A dictionary containing the structured results from each task in the workflow.
    """
    load_dotenv()

    # Use CrewAI's native LLM format for proper Anthropic integration
    model_name = os.getenv("ANTHROPIC_MODEL_NAME", "claude-sonnet-4-20250514")
    llm = LLM(
        model=f"anthropic/{model_name}",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        max_tokens=1024,
    )

    # Create agents
    agents_list = create_immigration_crew(llm)
    (
        intake_agent,
        plain_language_agent,
        research_agent,
        guide_agent,
        compliance_agent,
        lawyer_agent,
    ) = agents_list

    # Create tasks — each description includes {query} placeholder for the user's input
    tasks = [
        IntakeTask(intake_agent),
        SimplifyLanguageTask(plain_language_agent),
        ResearchImmigrationTask(research_agent),
        GuideApplicationTask(guide_agent),
        ComplianceCheckTask(compliance_agent),
        LawyerMatchTask(lawyer_agent),
    ]

    # Build inputs with user context
    ctx = user_context or {}
    inputs = {
        "query": query,
        "user_name": ctx.get("name", "Not provided"),
        "user_country": ctx.get("country", "Not provided"),
        "user_location": ctx.get("location", "Not provided"),
    }

    # Create and run the crew, passing the user query and context as input
    crew = Crew(agents=agents_list, tasks=tasks, process=Process.sequential, verbose=True)
    result = crew.kickoff(inputs=inputs)

    # Build structured output from task results
    task_names = [
        "intake_summary",
        "plain_language",
        "research_findings",
        "application_guide",
        "compliance_check",
        "lawyer_recommendations",
    ]
    output = {}
    for i, name in enumerate(task_names):
        if i < len(result.tasks_output):
            output[name] = result.tasks_output[i].raw
        else:
            output[name] = "No output"

    return output


def main():
    """Defines the main entry point for the application.

    This function provides a sample immigration query and calls the processing function
    to demonstrate the system's functionality. It then prints the final results.
    """
    query = """
    I am a Nigerian citizen currently in the United States on an F-1 student visa.
    My visa expires in 3 months and I just graduated with a Master's degree in
    Computer Science. I want to stay and work in the US. What are my options?
    I might need a lawyer in New York who speaks Yoruba.
    """

    result = process_immigration_query(query)

    print("\n" + "=" * 80)
    print("IMMIGRATION AI AGENT — RESULTS")
    print("=" * 80)
    for section, content in result.items():
        print(f"\n{'─' * 40}")
        print(f"📋 {section.replace('_', ' ').upper()}")
        print(f"{'─' * 40}")
        print(content[:500] if len(content) > 500 else content)
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
