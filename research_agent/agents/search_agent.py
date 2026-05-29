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

# Import the required tools from the tools module
from research_agent.tools import (
    arxiv_tool,
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
    pubmed_tool,
    github_tool,
    paperswithcode_tool,
    huggingface_tool,
)


class SearchAgentOutput(BaseModel):
    title: str = Field(..., description="A concise title for the discovered research topic or finding set.")
    summary: str = Field(..., description="A concise synthesis of the most relevant findings.")
    links: dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of source names or paper/resource titles mapped to their URLs.",
    )

search_agent = Agent(
    name="Search Agent",
    role="Discover all relevant scientific knowledge related to the topic while maximizing recall and minimizing irrelevant results.",
    model=Gemini(id="gemini-2.5-flash"),
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
        "Filter out irrelevant or low-quality results before presenting your findings.",
        "Return the final response with title, summary, and links fields.",
        "Use links as a dictionary where each key is a descriptive source name and each value is the URL.",
    ],
    tools=[
        arxiv_tool,
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
)


if __name__ == "__main__":
    """Test the search agent with a sample query."""
    query = "What are the latest advancements in natural language processing for scientific literature review?"
    response = asyncio.run(search_agent.aprint_response(query, stream=True))
    # print(response.content.model_dump())