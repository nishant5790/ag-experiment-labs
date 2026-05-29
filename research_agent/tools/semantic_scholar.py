import requests
import json

def semantic_scholar_tool(query: str, max_results: int = 5) -> str:
    """
    Search for papers using the Semantic Scholar API.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={max_results}&fields=title,authors,year,abstract,url"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except Exception as e:
        return f"Error querying Semantic Scholar: {str(e)}"
