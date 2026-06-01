"""Paper Search Agent — discovers relevant scientific knowledge.

Prompt config lives in prompts/agents/search.yml.
"""
import asyncio

from agno.tools.arxiv import ArxivTools
from pydantic import BaseModel

from research_agent.agents._base import build_agent
from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
    pubmed_tool,
    github_tool,
    paperswithcode_tool,
    huggingface_tool,
)


class SearchAgentOutput(BaseModel):
    topic: str
    search_queries: list[str]
    papers: list[dict]
    surveys: list[dict]
    datasets: list[dict]
    repositories: list[dict]
    patents: list[dict]
    statistics: dict


search_agent_ag = build_agent(
    prompt_name="search",
    tools=[
        ArxivTools(enable_search_arxiv=True, enable_read_arxiv_papers=False),
        semantic_scholar_tool,
        openalex_tool,
        crossref_tool,
        pubmed_tool,
        github_tool,
        paperswithcode_tool,
        huggingface_tool,
    ],
    output_schema=SearchAgentOutput,
)


if __name__ == "__main__":
    query = "What are the latest advancements in natural language processing for scientific literature review?"
    asyncio.run(search_agent_ag.aprint_response(query, stream=True))
