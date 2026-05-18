"""Web search tools using Tavily API."""
from tavily import TavilyClient
from agno.tools import tool
from langfuse import observe

# Tavily Web Search Tool
@observe(as_type="tool", name="tavily-web-search")
def search_web(query: str, max_results: int = 3) -> str:
    """Search the web for travel information using Tavily."""
    tavily_client = TavilyClient()
    response = tavily_client.search(query=query, max_results=max_results)
    
    results = []
    for result in response.get("results", []):
        results.append(f"- {result.get('title', 'No title')}: {result.get('content', 'No content')}")
    
    return "\n".join(results) if results else "No results found."


# Wrap the search_web function as an agno tool
@tool
def web_search_tool(query: str, max_results: int = 3) -> str:
    """Search the web for travel information."""
    return search_web(query, max_results)

