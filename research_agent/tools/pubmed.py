import requests
import json

def pubmed_tool(query: str, max_results: int = 5) -> str:
    """
    Search for biomedical literature using the PubMed API.
    
    Args:
        query: The search query.
        max_results: The maximum number of results to return.
    """
    try:
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax={max_results}"
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        id_list = response.json().get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return "No results found on PubMed."
        
        ids = ",".join(id_list)
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids}&retmode=json"
        summary_resp = requests.get(summary_url, timeout=10)
        summary_resp.raise_for_status()
        return json.dumps(summary_resp.json().get("result", {}), indent=2)
    except Exception as e:
        return f"Error querying PubMed: {str(e)}"
