from sqlalchemy.connectors import asyncio
from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from agno.db.base import SessionType

load_dotenv()

def scrape_webpage(url: str) -> str:
    """Scrapes the text content from a given URL using BeautifulSoup.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        str: The extracted text content of the webpage, or an error message.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.extract()
            
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"

def pdf_scraper(url: str) -> str:
    """Scrapes the text content from a given URL using BeautifulSoup.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        str: The extracted text content of the webpage, or an error message.
    """
    pass

db = SqliteDb(
        session_table="arxiv_session",
        db_file = "tmp/arxiv.db",
    )

arxiv_agent = Agent(
    name="Arxiv agent",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[ArxivTools(all=True), scrape_webpage],
    db=db,
    instructions=[
        "Use the Arxiv tool to search for research papers on the given topic.",
        "extract all data in markdown format with links to the papers and sources using the scrape_webpage tool to get more detailed information from the paper links or other URLs.",
    ],
    add_datetime_to_context=True,
    save_response_to_file="output/arxiv.md",
    stream_events=True,

    

)


if __name__ == "__main__":
    # Example usage
    # print(scrape_webpage(url="https://arxiv.org/abs/2304.04780v1"))
    topic = "Artificial Intelligence in Healthcare"
    response = arxiv_agent.print_response(topic,markdown=True)

    print("\n verifing db content")
    all_sessions = db.get_sessions(session_type=SessionType.AGENT)
    # print( all_sessions[0].get_messages())
    # print(all_sessions[0].model_dump_json(indent=2))
    print(f"Total sessions: {len(all_sessions)}")

    
    # Get a trace
trace = db.get_trace(run_id=response.run_id)

if trace:
    print(f"Trace ID: {trace.trace_id}")
    print(f"Name: {trace.name}")
    print(f"Duration: {trace.duration_ms}ms")
    print(f"Status: {trace.status}")
    print(f"Total Spans: {trace.total_spans}")
    print(f"Errors: {trace.error_count}")



    