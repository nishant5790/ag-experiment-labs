"""Cross-Domain Innovation Agent — proposes ideas transferred from adjacent fields.

Prompt config lives in prompts/agents/cross_domain.yml.
"""
import asyncio

from agno.tools.arxiv import ArxivTools

from research_agent.agents._base import build_agent
from research_agent.tools import semantic_scholar_tool, openalex_tool


cross_domain_agent_ag = build_agent(
    prompt_name="cross_domain",
    tools=[
        ArxivTools(enable_search_arxiv=True, enable_read_arxiv_papers=False),
        semantic_scholar_tool,
        openalex_tool,
    ],
)


if __name__ == "__main__":
    asyncio.run(cross_domain_agent_ag.aprint_response(
        "Propose cross-domain innovations for time-series forecasting in finance.",
        stream=True,
    ))
