import os
import sys
import asyncio

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from pydantic import BaseModel

from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
)


db = SqliteDb(
    db_file=os.path.join(project_root, "research_agent/storage/citation_graph.db"),
    session_table="citation_graph_session",
)


class CitationEdge(BaseModel):
    source: str
    target: str
    relation: str  # "cites" | "cited_by"


class SeminalPaper(BaseModel):
    title: str
    authors: list[str] = []
    year: int | None = None
    citation_count: int | None = None
    doi: str | None = None
    url: str | None = None
    reason: str | None = None


class CitationGraphOutput(BaseModel):
    topic: str
    seed_papers: list[dict]
    seminal_papers: list[SeminalPaper]
    citation_edges: list[CitationEdge]
    influential_authors: list[str]
    research_clusters: list[dict]
    statistics: dict


citation_graph_agent_ag = Agent(
    name="Citation Graph Agent",
    role=(
        "Build and analyze the citation graph for a research topic, identifying "
        "seminal papers, influential authors, and research clusters."
    ),
    model=Gemini(id="gemini-2.5-flash"),
    db=db,
    description=(
        "You are an expert bibliometric analyst. You construct citation networks "
        "from seed papers, trace forward (cited_by) and backward (references) links, "
        "and surface the most influential works and authors in a field."
    ),
    instructions=[
        "Start from a small set of seed papers relevant to the user's topic.",
        "Use Semantic Scholar, OpenAlex, and CrossRef to retrieve citation metadata, references, and citation counts.",
        "Trace backward citations (what each seed paper cites) and forward citations (papers that cite each seed paper).",
        "Identify seminal papers based on high citation counts, recurring appearance across references, and topical centrality.",
        "Identify influential authors based on author frequency across the most cited works.",
        "Group papers into research clusters when they share authors, references, or sub-topics.",
        "Return the response using the exact CitationGraphOutput schema.",
        "Populate seed_papers, seminal_papers, citation_edges (source -> target with 'cites' or 'cited_by'), influential_authors, research_clusters, and a statistics dict.",
    ],
    tools=[
        semantic_scholar_tool,
        openalex_tool,
        crossref_tool,
    ],
    output_schema=CitationGraphOutput,
    structured_outputs=False,
    use_json_mode=True,
    markdown=False,
    stream_events=True,
)


if __name__ == "__main__":
    query = "Build a citation graph around 'retrieval augmented generation for scientific literature'."
    asyncio.run(citation_graph_agent_ag.aprint_response(query, stream=True))
