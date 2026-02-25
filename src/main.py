"""Main module for the Immigration AI Agent system.

This module serves as the primary entry point for running the immigration AI agent crew.
It defines the main workflow for processing an immigration query, from initializing
the language model and agents to executing the tasks and returning the final results.
"""

from crewai import Crew, Process

from src.agents import create_immigration_crew
from src.llm.llm_factory import LLMFactory, LLMType
from src.tasks import (
    ComplianceCheckTask,
    GuideApplicationTask,
    IntakeTask,
    LawyerMatchTask,
    ResearchImmigrationTask,
    SimplifyLanguageTask,
)


def process_immigration_query(query: str) -> dict:
    """Processes an immigration query using the immigration agent crew.

    This function orchestrates the entire workflow. It initializes the language model
    using the LLMFactory, creates the specialized agents, defines the sequence of tasks,
    and runs the crew to get the processed results.

    Args:
        query: A string containing the user's immigration question or scenario.

    Returns:
        A dictionary containing the structured results from each task in the workflow.
    """
    # Initialize the appropriate LLM using the factory
    llm = LLMFactory.create_llm(LLMType.CLOUD_FAST)

    # Create agents
    agents = create_immigration_crew(llm)

    # Create tasks
    tasks = [
        IntakeTask(),
        SimplifyLanguageTask(),
        ResearchImmigrationTask(),
        GuideApplicationTask(),
        ComplianceCheckTask(),
        LawyerMatchTask(),
    ]

    # Create and run the crew
    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=True)
    result = crew.kickoff()

    return {
        "intake_summary": result[0],
        "plain_language": result[1],
        "research_findings": result[2],
        "application_guide": result[3],
        "compliance_check": result[4],
        "lawyer_recommendations": result[5],
    }


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
    print("Processing complete:", result)


if __name__ == "__main__":
    main()
