import requests
import json

def paperswithcode_tool(query: str, max_results: int = 5) -> str:
    """
    Search for papers with code implementations on PapersWithCode.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://paperswithcode.com/api/v1/papers/?q={query}&items_per_page={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error querying PapersWithCode: {str(e)}"
