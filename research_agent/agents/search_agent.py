import os
import sys

# Add the project root to sys.path to allow absolute imports like 'research_agent.tools'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agno.agent import Agent
from agno.models.google import Gemini

# Import the required tools from the tools module
from research_agent.tools import (
    arxiv_tool,
    semantic_scholar_tool,
    openalex_tool,
    crossref_tool,
    core_tool,
    pubmed_tool,
    github_tool,
    paperswithcode_tool,
    huggingface_tool,
    kaggle_tool,
)

search_agent = Agent(
    name="Search Agent",
    role="Discover all relevant scientific knowledge related to the topic while maximizing recall and minimizing irrelevant results.",
    model=Gemini(id="gemini-2.5-pro"),
    description=(
        "You are an expert scientific research agent responsible for comprehensive literature "
        "and resource discovery. Your goal is to maximize the recall of relevant knowledge "
        "while minimizing noise and irrelevant results."
    ),
    instructions=[
        "Generate effective and comprehensive search strategies before querying.",
        "Expand research queries to include synonyms, related terms, and broader/narrower concepts.",
        "Discover relevant scientific papers using sources like arXiv, Semantic Scholar, OpenAlex, CrossRef, CORE, and PubMed.",
        "Discover systematic reviews and surveys.",
        "Discover relevant benchmarks for evaluating methodologies.",
        "Discover related datasets on HuggingFace and Kaggle.",
        "Discover code repositories and implementations on GitHub and PapersWithCode.",
        "Discover relevant patents.",
        "Cross-reference findings across multiple sources to ensure high recall.",
        "Filter out irrelevant or low-quality results before presenting your findings."
    ],
    tools=[
        arxiv_tool,
        semantic_scholar_tool,
        openalex_tool,
        crossref_tool,
        core_tool,
        pubmed_tool,
        github_tool,
        paperswithcode_tool,
        huggingface_tool,
        kaggle_tool,
    ],
    markdown=True,
)
