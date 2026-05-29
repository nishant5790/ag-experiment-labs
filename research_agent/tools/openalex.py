import requests
import json

def openalex_tool(query: str, max_results: int = 5) -> str:
    """
    Search for papers and works using the OpenAlex API.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://api.openalex.org/works?search={query}&per-page={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = [
            {
                "title": w.get("title"), 
                "publication_year": w.get("publication_year"), 
                "doi": w.get("doi")
            } for w in data.get("results", [])
        ]
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error querying OpenAlex: {str(e)}"
