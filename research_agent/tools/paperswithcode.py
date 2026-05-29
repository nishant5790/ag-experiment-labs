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
        response = requests.get(url, timeout=10, headers={"Accept": "application/json"})
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "text/html" in content_type:
            return (
                "PapersWithCode API is currently unavailable (returns HTML). "
                "The API may be behind Cloudflare protection. "
                f"Try browsing https://paperswithcode.com/search?q_meta=&q_type=&q={query} directly."
            )
        results = response.json().get("results", [])
        return json.dumps(results[:max_results], indent=2)
    except requests.exceptions.JSONDecodeError:
        return (
            "PapersWithCode API returned a non-JSON response. "
            "The API endpoint may have changed or is temporarily unavailable."
        )
    except Exception as e:
        return f"Error querying PapersWithCode: {str(e)}"
