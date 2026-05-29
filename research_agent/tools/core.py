import requests
import json

def core_tool(query: str, max_results: int = 5, api_key: str = "") -> str:
    """
    Search for open access research papers using the CORE API.
    Requires an API key.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
        api_key: The CORE API Key (if available).
    """
    if not api_key:
        return "CORE API requires an api_key to function. Please provide one or rely on other tools."
    try:
        url = f"https://api.core.ac.uk/v3/search/works?q={query}&limit={max_results}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return json.dumps(response.json().get("results", []), indent=2)
    except Exception as e:
        return f"Error querying CORE: {str(e)}"
