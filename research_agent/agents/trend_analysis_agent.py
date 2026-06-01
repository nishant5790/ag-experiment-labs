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
from agno.tools.arxiv import ArxivTools
from pydantic import BaseModel

from research_agent.tools import (
    semantic_scholar_tool,
    openalex_tool,
    paperswithcode_tool,
    huggingface_tool,
)


db = SqliteDb(
    db_file=os.path.join(project_root, "research_agent/storage/trend_analysis.db"),
    session_table="trend_analysis_session",
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
    timeframe: dict  # {"start_year": ..., "end_year": ...}
    publication_timeline: list[YearlyCount]
    emerging_topics: list[EmergingTopic]
    declining_topics: list[str]
    hot_keywords: list[str]
    leading_venues: list[str]
    leading_institutions: list[str]
    summary: str
    statistics: dict


trend_analysis_agent_ag = Agent(
    name="Trend Analysis Agent",
    role=(
        "Analyze temporal publication trends, emerging sub-topics, and the velocity "
        "of research activity around a given topic."
    ),
    model=Gemini(id="gemini-2.5-flash"),
    db=db,
    description=(
        "You are an expert research trend analyst. You quantify how a research area "
        "has evolved over time, detect emerging and declining sub-topics, identify hot "
        "keywords, and surface the venues and institutions driving the field."
    ),
    instructions=[
        "Query arXiv, Semantic Scholar, OpenAlex, PapersWithCode, and HuggingFace to gather time-stamped works on the topic.",
        "Build a yearly publication timeline (year -> paper_count) covering at least the last 5-10 years when data allows.",
        "Detect emerging topics by year-over-year growth in mentions or new keyword appearance.",
        "Detect declining topics whose frequency has dropped meaningfully.",
        "Extract hot keywords from recent (last 1-2 years) paper titles and abstracts.",
        "Identify leading venues (conferences/journals) and leading institutions by publication volume.",
        "Provide a concise narrative summary of how the field is evolving.",
        "Return the response using the exact TrendAnalysisOutput schema, including a statistics dict.",
    ],
    tools=[
        ArxivTools(
            enable_search_arxiv=True,
            enable_read_arxiv_papers=False,
        ),
        semantic_scholar_tool,
        openalex_tool,
        paperswithcode_tool,
        huggingface_tool,
    ],
    output_schema=TrendAnalysisOutput,
    structured_outputs=False,
    use_json_mode=True,
    markdown=False,
    stream_events=True,
)


if __name__ == "__main__":
    query = "Analyze research trends for 'graph neural networks for drug discovery' over the last decade."
    asyncio.run(trend_analysis_agent_ag.aprint_response(query, stream=True))
