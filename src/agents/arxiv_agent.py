from agno.agent import Agent
from agno.tools.arxiv import ArxivTools
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
load_dotenv()

arxiv_agent = Agent(
    name="Arxiv agent",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[ArxivTools(all=True)],
    db=SqliteDb(
        session_table="arxiv_session",
        db_file = "tmp/arxiv.db",
    ),
    instructions=[
        "Use the Arxiv tool to search for research papers on the given topic.",
        "Provide a detailed summary of the most relevant papers, including their titles, authors, and links to the papers.",
        "Focus on recent papers (published within the last 5 years) and ensure that the summaries are concise and informative."
    ],
    add_datetime_to_context=True,

)


if __name__ == "__main__":
    # Example usage
    topic = "Artificial Intelligence in Healthcare"
    response = arxiv_agent.print_response(topic,markdown=True,)

    print(response)