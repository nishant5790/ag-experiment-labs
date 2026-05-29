import time
import json
import requests

def semantic_scholar_tool(query: str, max_results: int = 5) -> str:
    """
    Search for papers using the Semantic Scholar API.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={max_results}&fields=title,authors,year,abstract,url"
    headers = {"User-Agent": "research-agent/1.0 (academic use)"}
    for attempt in range(2):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 429:
                if attempt == 0:
                    time.sleep(3)
                    continue
                return "Semantic Scholar rate limit exceeded. Consider requesting an API key at https://www.semanticscholar.org/product/api"
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
        except requests.exceptions.HTTPError as e:
            return f"Error querying Semantic Scholar: {str(e)}"
        except Exception as e:
            return f"Error querying Semantic Scholar: {str(e)}"
    return "Semantic Scholar rate limit exceeded. Consider requesting an API key at https://www.semanticscholar.org/product/api"
