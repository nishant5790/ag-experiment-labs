"""Citation Graph Agent — builds the citation graph for a topic.

Prompt config lives in prompts/agents/citation_graph.yml.
"""
import asyncio

from pydantic import BaseModel

from research_agent.agents._base import build_agent
from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
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


citation_graph_agent_ag = build_agent(
    prompt_name="citation_graph",
    tools=[semantic_scholar_tool, openalex_tool, crossref_tool],
    output_schema=CitationGraphOutput,
)


if __name__ == "__main__":
    query = "Build a citation graph around 'retrieval augmented generation for scientific literature'."
    asyncio.run(citation_graph_agent_ag.aprint_response(query, stream=True))
