
from google.genai._interactions.types import deep_research_agent_config_param
import os
import sys
import asyncio

# Add the project root to sys.path to allow absolute imports like 'research_agent.tools'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from agno.agent import Agent
from agno.models.google import Gemini
from pydantic import BaseModel, Field
from typing import TypedDict
from agno.db.sqlite import SqliteDb
from agno.tools.arxiv import ArxivTools

db = SqliteDb(
    db_file=os.path.join(project_root, "research_agent/storage/search.db"),
    session_table="search_session",
)

# Import the required tools from the tools module
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


search_agent_ag = Agent(
    name="Search Agent",
    role="Discover all relevant scientific knowledge related to the topic while maximizing recall and minimizing irrelevant results.",
    model=Gemini(id="gemini-2.5-flash"),
    db=db,
    description=(
        "You are an expert scientific research agent responsible for comprehensive literature "
        "and resource discovery. Your goal is to maximize the recall of relevant knowledge "
        "while minimizing noise and irrelevant results."
    ),
    instructions=[
        "Generate effective and comprehensive search strategies before querying.",
        "Expand research queries to include synonyms, related terms, and broader/narrower concepts.",
        "Discover relevant scientific papers using sources like arXiv, Semantic Scholar, OpenAlex, CrossRef, and PubMed.",
        "Discover systematic reviews and surveys.",
        "Discover relevant benchmarks for evaluating methodologies.",
        "Discover related datasets on HuggingFace.",
        "Discover code repositories and implementations on GitHub and PapersWithCode.",
        "Discover relevant patents.",
        "Cross-reference findings across multiple sources to ensure high recall.",
        "Return the final response using the exact structure defined in the SearchAgentOutput schema.",
        "Include a topic string, search_queries list, statistics dictionary, and categorized lists for papers, surveys, datasets, repositories, and patents.",
    ],
    tools=[
        ArxivTools(
            enable_search_arxiv=True,
            enable_read_arxiv_papers=False, 
        ),
        semantic_scholar_tool,
        openalex_tool,
        crossref_tool,
        pubmed_tool,
        github_tool,
        paperswithcode_tool,
        huggingface_tool,
    ],
    output_schema=SearchAgentOutput,
    structured_outputs=False,
    use_json_mode=True,
    markdown=False,
    stream_events=True
)


if __name__ == "__main__":
    """Test the search agent with a sample query."""
    query = "What are the latest advancements in natural language processing for scientific literature review?"
    response = asyncio.run(search_agent_ag.aprint_response(query, stream=True))

    # response = search_agent.run(query)
    # print(response)
    
