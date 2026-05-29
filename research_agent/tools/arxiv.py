import requests

def arxiv_tool(query: str, max_results: int = 5) -> str:
    """
    Search for scientific papers on arXiv.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error querying arXiv: {str(e)}"
