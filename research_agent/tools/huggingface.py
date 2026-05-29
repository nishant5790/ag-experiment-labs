import requests
import json

def huggingface_tool(query: str, max_results: int = 5) -> str:
    """
    Search for machine learning datasets and models on HuggingFace.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"https://huggingface.co/api/datasets?search={query}&limit={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        results = response.json()
        formatted = [
            {
                "id": r.get("id"),
                "downloads": r.get("downloads")
            } for r in results
        ]
        return json.dumps(formatted, indent=2)
    except Exception as e:
        return f"Error querying HuggingFace: {str(e)}"
