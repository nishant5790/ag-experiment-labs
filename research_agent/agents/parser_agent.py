"""Paper Parser Agent — extracts structured fields from papers.

Prompt config lives in prompts/agents/paper_parser.yml.
"""
import asyncio

from agno.tools.arxiv import ArxivTools

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, openalex_tool


parser_agent_ag = build_agent(
    prompt_name="paper_parser",
    tools=[
        ArxivTools(enable_search_arxiv=True, enable_read_arxiv_papers=True),
        semantic_scholar_tool,
        openalex_tool,
    ],
)


if __name__ == "__main__":
    asyncio.run(parser_agent_ag.aprint_response(
        "Parse: 'Attention Is All You Need' (Vaswani et al., 2017).", stream=True))
