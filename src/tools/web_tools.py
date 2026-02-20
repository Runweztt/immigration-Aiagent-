"""Web tools for the Immigration AI Agent system."""

from crewai.tools import BaseTool


class WebSearchTool(BaseTool):
    """Tool for searching immigration information on the web."""

    name: str = "web_search"
    description: str = "Search for immigration news, policy updates, and legal information on the web"

    async def _run(self, query: str) -> str:
        """Run the web search tool.

        Args:
            query: Search query related to immigration topics.

        Returns:
            Search results as a string.
        """
        return f"Mock search results for: {query}"
