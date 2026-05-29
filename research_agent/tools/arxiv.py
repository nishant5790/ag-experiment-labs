import time
import requests

def arxiv_tool(query: str, max_results: int = 5) -> str:
    """
    Search for scientific papers on arXiv.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    headers = {"User-Agent": "research-agent/1.0 (academic use)"}
    for attempt in range(2):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 429:
                if attempt == 0:
                    time.sleep(3)
                    continue
                return "arXiv rate limit exceeded. Please try again in a few seconds."
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            return f"Error querying arXiv: {str(e)}"
        except Exception as e:
            return f"Error querying arXiv: {str(e)}"
    return "arXiv rate limit exceeded. Please try again in a few seconds."
