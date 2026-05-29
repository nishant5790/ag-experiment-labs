import requests
import json

def github_tool(query: str, max_results: int = 5) -> str:
    """
    Search for code repositories on GitHub.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://api.github.com/search/repositories?q={query}&per_page={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        items = response.json().get("items", [])
        results = [
            {
                "name": item.get("name"),
                "html_url": item.get("html_url"),
                "description": item.get("description"),
                "stars": item.get("stargazers_count")
            } for item in items
        ]
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error querying GitHub: {str(e)}"
