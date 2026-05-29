import requests
import json

def crossref_tool(query: str, max_results: int = 5) -> str:
    """
    Search for papers and DOIs using the Crossref API.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://api.crossref.org/works?query={query}&rows={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = [
            {
                "title": item.get("title", [""])[0] if item.get("title") else "",
                "URL": item.get("URL"),
                "author": item.get("author", [])
            } for item in data.get("message", {}).get("items", [])
        ]
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error querying Crossref: {str(e)}"
