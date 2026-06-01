import os
import sys
import asyncio

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from agno.team import Team
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb

from research_agent.agents.search_agent import search_agent_ag
from research_agent.agents.citation_graph_agent import citation_graph_agent_ag
from research_agent.agents.trend_analysis_agent import trend_analysis_agent_ag


db = SqliteDb(
    db_file=os.path.join(project_root, "research_agent/storage/discovery_team.db"),
    session_table="discovery_team_session",
)


# Reuse the existing comprehensive search agent as the Paper Search Agent.
paper_search_agent_ag = search_agent_ag
paper_search_agent_ag.name = "Paper Search Agent"


discovery_team = Team(
    name="Discovery Team",
    members=[
        paper_search_agent_ag,
        citation_graph_agent_ag,
        trend_analysis_agent_ag,
    ],
    model=Gemini(id="gemini-2.5-flash"),
    db=db,
    description=(
        "The Discovery Team is responsible for the knowledge-discovery phase of the "
        "research workflow. It collaborates to surface the most relevant prior work, "
        "map the citation landscape, and characterize the temporal evolution of a "
        "research topic. with all the refernce link and sources "
    ),
    instructions=[
        "Coordinate the three member agents to produce a comprehensive discovery report on the user's topic.",
        "Delegate to Paper Search Agent first to gather an initial corpus of papers, surveys, datasets, repositories, and patents.",
        "Pass the discovered seed papers to Citation Graph Agent to identify seminal works, influential authors, and research clusters.",
        "Invoke Trend Analysis Agent to build a publication timeline, detect emerging/declining sub-topics, and surface hot keywords, venues, and institutions.",
        "Synthesize the outputs of all three members into a single cohesive discovery summary for the user.",
        "Highlight key papers, top authors, dominant venues, current trends, and any notable gaps observed across the discovery results",
        "always include the refrences and links "
    ],
    add_datetime_to_context=True,
    add_member_tools_to_context=False,
    markdown=True,
    stream_events=True,
)


if __name__ == "__main__":
    query = (
        "graph neural networks for drug discovery"
    )
    asyncio.run(discovery_team.aprint_response(query, stream=True))
