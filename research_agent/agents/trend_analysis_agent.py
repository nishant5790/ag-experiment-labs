"""Trend Analysis Agent — analyzes publication trends and emerging topics.

Prompt config lives in prompts/agents/trend_analysis.yml.
"""
import asyncio

from agno.tools.arxiv import ArxivTools
from pydantic import BaseModel

from research_agent.agents._base import build_agent
from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    paperswithcode_tool,
    huggingface_tool,
)


class YearlyCount(BaseModel):
    year: int
    paper_count: int


class EmergingTopic(BaseModel):
    topic: str
    growth_rate: float | None = None
    first_seen_year: int | None = None
    representative_papers: list[str] = []


class TrendAnalysisOutput(BaseModel):
    topic: str
    timeframe: dict
    publication_timeline: list[YearlyCount]
    emerging_topics: list[EmergingTopic]
    declining_topics: list[str]
    hot_keywords: list[str]
    leading_venues: list[str]
    leading_institutions: list[str]
    summary: str
    statistics: dict


trend_analysis_agent_ag = build_agent(
    prompt_name="trend_analysis",
    tools=[
        ArxivTools(enable_search_arxiv=True, enable_read_arxiv_papers=False),
        semantic_scholar_tool,
        openalex_tool,
        paperswithcode_tool,
        huggingface_tool,
    ],
    output_schema=TrendAnalysisOutput,
)


if __name__ == "__main__":
    query = "Analyze research trends for 'graph neural networks for drug discovery' over the last decade."
    asyncio.run(trend_analysis_agent_ag.aprint_response(query, stream=True))
